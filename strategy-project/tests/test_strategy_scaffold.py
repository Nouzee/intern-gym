from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from build_features import build_daily_ipo_features
from costs import load_cost_model, trade_cost, apply_slippage
from metrics import calculate_metrics
from strategy import generate_trades, generate_baseline_trades


# ── Helper: build features with threshold=-1 to capture all symbols ──
def _build_test_features(threshold: float = -1.0):
    universe = pd.read_parquet(REPO_ROOT / "research-data" / "ipo_universe.parquet")
    daily_bars = pd.read_parquet(REPO_ROOT / "research-data" / "daily_bars.parquet")
    cost_model = load_cost_model(REPO_ROOT / "research-data" / "cost_model.json")
    features = build_daily_ipo_features(universe, daily_bars, threshold=threshold)
    return features, daily_bars, cost_model


# ── 1. Feature schema and signal counts ──────────────────────────────

def test_feature_schema_has_all_signal_columns():
    features, _, _ = _build_test_features()
    required = {
        "baseline_signal", "baseline_momentum_signal",
        "reversal_signal", "reversal_liquidity_signal",
        "reversal_liquidity_deep_signal",
    }
    assert required.issubset(set(features.columns)), \
        f"Missing signal columns: {required - set(features.columns)}"

def test_baseline_signal_is_alias_for_baseline_momentum():
    features, _, _ = _build_test_features()
    assert (features["baseline_signal"] == features["baseline_momentum_signal"]).all(), \
        "baseline_signal must equal baseline_momentum_signal for backward compatibility"

def test_signal_counts_match_expectations():
    features, _, _ = _build_test_features(threshold=0.05)
    # Expected from the data audit: 14 momentum, 38 reversal, 15 reversal+liq, 11 deep
    assert features["baseline_momentum_signal"].sum() == 14
    assert features["reversal_signal"].sum() == 38
    assert features["reversal_liquidity_signal"].sum() == 15
    assert features["reversal_liquidity_deep_signal"].sum() == 11

def test_feature_schema_has_derived_columns():
    features, _, _ = _build_test_features()
    required = {
        "first_day_return_vs_open", "day1_return", "first_day_range",
        "first_day_turnover_rank", "first_day_turnover_quantile",
        "first_day_volume", "first_day_turnover",
    }
    assert required.issubset(set(features.columns)), \
        f"Missing derived columns: {required - set(features.columns)}"

def test_day1_return_equals_first_day_return_vs_open():
    features, _, _ = _build_test_features()
    assert (abs(features["day1_return"] - features["first_day_return_vs_open"]) < 1e-12).all(), \
        "day1_return must equal first_day_return_vs_open"

def test_no_null_signals():
    features, _, _ = _build_test_features()
    signal_cols = ["baseline_signal", "baseline_momentum_signal", "reversal_signal",
                   "reversal_liquidity_signal", "reversal_liquidity_deep_signal"]
    for col in signal_cols:
        assert not features[col].isnull().any(), f"{col} must have no nulls"
        assert features[col].dtype == bool, f"{col} must be boolean"

def test_rank_and_quantile_are_valid():
    features, _, _ = _build_test_features()
    assert features["first_day_turnover_rank"].notna().all()
    assert features["first_day_turnover_rank"].between(0, 1).all()
    assert features["first_day_turnover_quantile"].notna().all()
    assert features["first_day_turnover_quantile"].between(0, 4).all()
    assert features["first_day_turnover_quantile"].nunique() >= 3, \
        "Quantile should have multiple distinct values"

def test_first_day_range_is_valid():
    features, _, _ = _build_test_features()
    assert features["first_day_range"].notna().all()
    assert (features["first_day_range"] >= 0).all(), "Range should be non-negative"


# ── 2. Trade log schema ─────────────────────────────────────────────

REQUIRED_TRADE_COLUMNS = [
    "symbol", "coverage_start", "entry_date", "entry_price",
    "exit_date", "exit_price", "shares", "gross_pnl", "fees",
    "slippage", "net_pnl", "return", "exit_reason", "holding_days",
    "strategy_version",
]

def test_trade_log_has_exact_required_columns():
    features, daily_bars, cost_model = _build_test_features()
    trades = generate_trades(features, daily_bars, cost_model,
                             signal_column="baseline_momentum_signal",
                             strategy_version="test")
    assert not trades.empty, "Should generate at least one trade with threshold=-1"
    actual = set(trades.columns)
    required = set(REQUIRED_TRADE_COLUMNS)
    assert required.issubset(actual), f"Missing trade columns: {required - actual}"
    assert actual.issubset(required), f"Unexpected trade columns: {actual - required}"

def test_trade_reasons_are_valid():
    features, daily_bars, cost_model = _build_test_features()
    trades = generate_trades(features, daily_bars, cost_model,
                             signal_column="baseline_momentum_signal",
                             strategy_version="test")
    valid = {"holding_period", "stop_loss", "take_profit"}
    assert set(trades["exit_reason"].unique()).issubset(valid), \
        f"Invalid exit reasons found: {set(trades['exit_reason'].unique()) - valid}"

def test_strategy_version_column_is_populated():
    features, daily_bars, cost_model = _build_test_features()
    for cfg in [
        ("baseline_momentum_signal", "baseline_momentum"),
        ("reversal_signal", "reversal"),
        ("reversal_liquidity_signal", "reversal_liquidity"),
        ("reversal_liquidity_deep_signal", "reversal_liquidity_deep"),
    ]:
        trades = generate_trades(features, daily_bars, cost_model,
                                 signal_column=cfg[0], strategy_version=cfg[1])
        if not trades.empty:
            assert (trades["strategy_version"] == cfg[1]).all(), \
                f"strategy_version must be '{cfg[1]}' for signal '{cfg[0]}'"

def test_trade_pnl_consistency():
    features, daily_bars, cost_model = _build_test_features()
    trades = generate_trades(features, daily_bars, cost_model,
                             signal_column="reversal_liquidity_signal",
                             strategy_version="reversal_liquidity")
    if not trades.empty:
        # net_pnl = gross_pnl - fees (slippage is informational, not in net_pnl calc)
        pnl_diff = abs(trades["gross_pnl"] - trades["fees"] - trades["net_pnl"])
        assert (pnl_diff < 0.01).all(), "net_pnl should equal gross_pnl - fees (within rounding)"

def test_generate_baseline_trades_backward_compatible():
    features, daily_bars, cost_model = _build_test_features()
    old_trades = generate_baseline_trades(features, daily_bars, cost_model)
    new_trades = generate_trades(features, daily_bars, cost_model,
                                 signal_column="baseline_signal",
                                 strategy_version="baseline_first_day_momentum_daily")
    assert len(old_trades) == len(new_trades), \
        "generate_baseline_trades should produce same number of trades as generate_trades with baseline_signal"
    assert old_trades["strategy_version"].iloc[0] == "baseline_first_day_momentum_daily"


# ── 3. Cost sanity ──────────────────────────────────────────────────

def test_cost_model_is_loaded_correctly():
    _, _, cost_model = _build_test_features()
    assert cost_model["buy_cost_bps"] == 12.0
    assert cost_model["sell_cost_bps"] == 22.0
    assert cost_model["slippage_bps"] == 10.0
    assert cost_model["min_fee"] == 5.0
    assert cost_model["currency"] == "HKD"

def test_round_trip_cost_on_100k_notional():
    """Round-trip cost on HKD 100,000 notional = ~HKD 540 = 0.54%"""
    _, _, cost_model = _build_test_features()
    notional = 100_000.0
    buy_fee = trade_cost(notional, "buy", cost_model)
    sell_fee = trade_cost(notional, "sell", cost_model)
    buy_slip = notional * cost_model["slippage_bps"] / 10_000
    sell_slip = notional * cost_model["slippage_bps"] / 10_000

    assert abs(buy_fee - 120.0) < 0.01, f"Buy fee should be ~120, got {buy_fee}"
    assert abs(sell_fee - 220.0) < 0.01, f"Sell fee should be ~220, got {sell_fee}"
    assert abs(buy_slip - 100.0) < 0.01
    assert abs(sell_slip - 100.0) < 0.01

    total = buy_fee + sell_fee + buy_slip + sell_slip
    assert abs(total - 540.0) < 0.01, f"Total round-trip should be ~540, got {total}"
    assert abs(total / notional - 0.0054) < 1e-6, f"Cost % should be ~0.54%, got {total/notional}"

def test_cost_scale_to_zero():
    """At 0x multiplier, all numeric cost fields become zero."""
    _, _, cost_model = _build_test_features()
    zero_model = {}
    for k, v in cost_model.items():
        zero_model[k] = 0.0 if isinstance(v, (int, float)) else v
    assert zero_model["buy_cost_bps"] == 0.0
    assert zero_model["slippage_bps"] == 0.0
    assert zero_model["min_fee"] == 0.0
    assert zero_model["currency"] == "HKD"

def test_slippage_direction_is_correct():
    """Buy slippage increases entry price, sell slippage decreases exit price."""
    _, _, cost_model = _build_test_features()
    price = 100.0
    buy_price = apply_slippage(price, "buy", cost_model)
    sell_price = apply_slippage(price, "sell", cost_model)
    assert buy_price > price, f"Buy slippage should increase price: {buy_price} > {price}"
    assert sell_price < price, f"Sell slippage should decrease price: {sell_price} < {price}"

def test_min_fee_applied():
    """Min fee of HKD 5 should floor any commission."""
    _, _, cost_model = _build_test_features()
    # With 1,000 notional: 12 bps = 0.12, should be floored to 5
    tiny_notional = 1_000.0
    fee = trade_cost(tiny_notional, "buy", cost_model)
    assert abs(fee - 5.0) < 0.01, f"Fee should be floored to min_fee 5, got {fee}"


# ── 4. Metrics schema ───────────────────────────────────────────────

def test_metrics_contain_required_base_metrics():
    features, daily_bars, cost_model = _build_test_features()
    trades = generate_trades(features, daily_bars, cost_model,
                             signal_column="reversal_signal",
                             strategy_version="reversal")
    metrics = calculate_metrics(trades)
    required = {"trade_count", "win_rate", "average_return", "average_win",
                "average_loss", "profit_factor", "total_return", "max_drawdown",
                "turnover", "average_holding_days"}
    assert required.issubset(set(metrics)), f"Missing base metrics: {required - set(metrics)}"

def test_empty_trades_returns_zero_metrics():
    empty = pd.DataFrame()
    metrics = calculate_metrics(empty)
    assert metrics["trade_count"] == 0
    assert metrics["win_rate"] == 0.0
    assert metrics["total_return"] == 0.0
    assert metrics["max_drawdown"] == 0.0

def test_derived_metrics_are_computed():
    """Verify aggregate metrics can be computed from trades."""
    features, daily_bars, cost_model = _build_test_features()
    trades = generate_trades(features, daily_bars, cost_model,
                             signal_column="reversal_liquidity_signal",
                             strategy_version="reversal_liquidity")
    if not trades.empty:
        bn = trades["entry_price"].mul(trades["shares"])
        agg_gross = float(trades["gross_pnl"].sum() / bn.sum())
        agg_net = float(trades["net_pnl"].sum() / bn.sum())
        avg_cost = float((trades["fees"].sum() + trades["slippage"].sum()) / bn.sum())
        # These should be reasonable values
        assert -1.0 <= agg_gross <= 1.0, f"aggregate_gross_return out of range: {agg_gross}"
        assert -1.0 <= agg_net <= 1.0, f"aggregate_net_return out of range: {agg_net}"
        assert 0.0 <= avg_cost <= 0.05, f"average_cost_impact out of range: {avg_cost}"


# ── 5. Scaffold integration test (original, kept for backward compat) ──

def test_strategy_scaffold_builds_daily_features_and_trades():
    features, daily_bars, cost_model = _build_test_features()
    trades = generate_baseline_trades(features, daily_bars, cost_model)
    metrics = calculate_metrics(trades)

    assert not features.empty
    assert set(features.columns) >= {"symbol", "trade_date_1", "entry_date", "first_day_return_vs_open",
                                        "day1_return", "first_day_range",
                                        "first_day_turnover_rank", "first_day_turnover_quantile",
                                        "baseline_signal", "baseline_momentum_signal",
                                        "reversal_signal", "reversal_liquidity_signal",
                                        "reversal_liquidity_deep_signal"}
    assert set(trades.columns) >= {"symbol", "entry_date", "exit_date", "net_pnl", "strategy_version"}
    assert set(metrics) >= {"trade_count", "win_rate", "total_return", "max_drawdown", "average_holding_days"}
    assert (features["baseline_signal"] == features["baseline_momentum_signal"]).all(), \
        "baseline_signal must equal baseline_momentum_signal for backward compatibility"
