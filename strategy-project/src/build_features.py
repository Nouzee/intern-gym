from __future__ import annotations

import argparse
import json

import pandas as pd

from paths import PROCESSED_DIR, RAW_DIR


def build_daily_ipo_features(universe: pd.DataFrame, daily_bars: pd.DataFrame, *, threshold: float = 0.05) -> pd.DataFrame:
    daily = normalize_daily(daily_bars)
    universe = universe.copy()
    universe["symbol"] = universe["symbol"].astype(str).str.upper()
    rows = []

    for symbol, group in daily.groupby("symbol", sort=True):
        bars = group.sort_values("trade_date").reset_index(drop=True)
        if len(bars) < 2:
            continue
        first = bars.iloc[0]
        entry = bars.iloc[1]
        first_day_return = safe_return(float(first["close"]), float(first["open"]))
        first_open = float(first["open"])
        first_day_range = (float(first["high"]) - float(first["low"])) / first_open if first_open else 0.0
        listing_row = universe[universe["symbol"] == symbol].head(1)
        coverage_start = str(first["trade_date"])
        name = ""
        if not listing_row.empty:
            coverage_start = str(listing_row.iloc[0].get("coverage_start") or coverage_start)
            name = str(listing_row.iloc[0].get("name") or "")
        momentum_signal = bool(first_day_return > threshold and float(entry["open"]) > 0)
        reversal_signal = bool(first_day_return < 0 and float(entry["open"]) > 0)
        rows.append(
            {
                "symbol": symbol,
                "name": name,
                "coverage_start": coverage_start,
                "trade_date_1": str(first["trade_date"]),
                "first_day_open": first_open,
                "first_day_close": float(first["close"]),
                "first_day_high": float(first["high"]),
                "first_day_low": float(first["low"]),
                "first_day_return_vs_open": first_day_return,
                "day1_return": first_day_return,
                "first_day_range": first_day_range,
                "first_day_volume": int(first["volume"]),
                "first_day_turnover": float(first["turnover"]),
                "entry_date": str(entry["trade_date"]),
                "entry_open": float(entry["open"]),
                "baseline_signal": momentum_signal,
                "baseline_momentum_signal": momentum_signal,
                "reversal_signal": reversal_signal,
                "reversal_liquidity_signal": False,
                "reversal_liquidity_deep_signal": False,
            }
        )

    result = pd.DataFrame(rows)

    # Post-hoc features that need cross-sectional information
    if not result.empty:
        median_turnover = result["first_day_turnover"].median()
        result["first_day_turnover_rank"] = result["first_day_turnover"].rank(pct=True)

        # Robust qcut: fall back to manual binning if duplicates prevent 5 unique bins
        try:
            result["first_day_turnover_quantile"] = pd.qcut(
                result["first_day_turnover"], 5, labels=False, duplicates="drop"
            )
        except ValueError:
            result["first_day_turnover_quantile"] = pd.cut(
                result["first_day_turnover"], bins=5, labels=False
            )

        result["reversal_liquidity_signal"] = (
            result["reversal_signal"] & (result["first_day_turnover"] > median_turnover)
        )
        result["reversal_liquidity_deep_signal"] = (
            (result["first_day_return_vs_open"] < -0.05)
            & (result["first_day_turnover"] > median_turnover)
            & (result["entry_open"] > 0)
        )

    return result


def normalize_daily(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    result["symbol"] = result["symbol"].astype(str).str.upper()
    result["trade_date"] = result["trade_date"].astype(str).str.replace("-", "", regex=False)
    for column in ("open", "high", "low", "close", "volume", "turnover"):
        result[column] = pd.to_numeric(result[column], errors="coerce").fillna(0)
    return result


def safe_return(end: float, start: float) -> float:
    return end / start - 1.0 if start else 0.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build daily first-trading-day IPO features.")
    parser.add_argument("--threshold", type=float, default=0.05)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    universe = pd.read_parquet(RAW_DIR / "ipo_universe.parquet")
    daily = pd.read_parquet(RAW_DIR / "daily_bars.parquet")
    features = build_daily_ipo_features(universe, daily, threshold=args.threshold)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    features.to_parquet(PROCESSED_DIR / "features.parquet", index=False)
    print(json.dumps({
        "rows": int(len(features)),
        "baseline_momentum_signal": int(features["baseline_momentum_signal"].sum()),
        "reversal_signal": int(features["reversal_signal"].sum()),
        "reversal_liquidity_signal": int(features["reversal_liquidity_signal"].sum()),
        "reversal_liquidity_deep_signal": int(features["reversal_liquidity_deep_signal"].sum()),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
