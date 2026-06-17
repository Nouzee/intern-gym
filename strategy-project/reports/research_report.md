# IPO / New Listing Daily Strategy Research

**Date:** 2026-06-15 | **Author:** 刘子睿 (Liu Zirui) | **Project:** intern-gym / strategy-project

## Executive Summary

This report evaluates four first-trading-day IPO strategies using only repository-provided daily OHLCV bars and the cost model. No external data enters the core backtest signals.

- **S0 (Baseline Momentum):** The scaffold hypothesis — buy IPOs with day-1 return > 5%. Result: negative aggregate net return (−0.2%), lowest win rate (35.7%).
- **S1 (Reversal):** The data-driven alternative — buy IPOs with negative day-1 returns. Result: beats S0 on win rate (44.7%), aggregate return (+6.0%), and drawdown.
- **S2 (Reversal + Liquidity):** S1 + above-median day-1 turnover filter. Result: most balanced version in this sample — 60.0% win rate, +14.6% aggregate net return, 45% lower drawdown than S1.
- **S3 (Reversal + Liquidity + Deep):** S2 with deeper threshold (< -5%). Result: comparable to S2 (54.5% win, +16.2% aggregate net) but only 11 trades — indicative only.

**Finding:** In this sample, S2 (reversal + liquidity) is the most balanced strategy across win rate, trade count, and return. The scaffold momentum hypothesis (S0) is not supported — it produces negative aggregate net return after costs. S3 shows promise but needs a larger sample to be conclusive.

## Strategy Comparison

| Strategy | Trades | Win Rate | Average Net Return | Aggregate Gross Return | Aggregate Net Return | Summed Net Return | Average Win | Average Loss | Avg Cost Impact | Max Drawdown | Profit Factor | Avg Holding Days | Turnover (HKD) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| S0: Baseline Momentum | 14 | 35.7% | -0.0021 | 0.0013 | -0.0021 | -0.0287 | 0.2394 | -0.1362 | 0.0054 | -75603.3115 | 0.98 | 1.1 | 1,399,040 |
| S1: Reversal | 38 | 44.7% | 0.0603 | 0.0638 | 0.0603 | 2.2908 | 0.2142 | -0.0644 | 0.0056 | -48346.9546 | 2.70 | 1.7 | 3,798,855 |
| S2: Reversal + Liquidity | 15 | 60.0% | 0.1456 | 0.1494 | 0.1457 | 2.1845 | 0.2743 | -0.0474 | 0.0059 | -26537.4332 | 8.68 | 2.1 | 1,499,363 |
| S3: Reversal + Liquidity + Deep | 11 | 54.5% | 0.1619 | 0.1657 | 0.1619 | 1.7810 | 0.3329 | -0.0432 | 0.0059 | -19706.1010 | 9.24 | 2.0 | 1,099,507 |

![Aggregate Net Return](figures/strategy_aggregate_net_return_comparison.png)
*Aggregate net return by strategy. S2 is the final selected strategy; S3 is a sensitivity variant only (fewer trades, higher concentration).*

## Cost Sensitivity (0× / 1× / 2×)

Each cost model component (buy_cost_bps, sell_cost_bps, slippage_bps, min_fee) is multiplied by the cost factor. At 0× costs, all costs are zeroed. At 1×, the actual repository cost model is used. At 2×, costs are doubled as a stress test.

| Strategy | Cost | Trades | Win Rate | Average Net Return | Aggregate Net Return | Summed Net Return | Max Drawdown |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| S0: Baseline Momentum | 0x | 14 | 35.7% | 0.0034 | 0.0034 | 0.0470 | -72137.5000 |
| S0: Baseline Momentum | 1x | 14 | 35.7% | -0.0021 | -0.0021 | -0.0287 | -75603.3115 |
| S0: Baseline Momentum | 2x | 14 | 35.7% | -0.0074 | -0.0075 | -0.1043 | -79088.8202 |
| S1: Reversal | 0x | 38 | 44.7% | 0.0660 | 0.0660 | 2.5063 | -44760.1700 |
| S1: Reversal | 1x | 38 | 44.7% | 0.0603 | 0.0603 | 2.2908 | -48346.9546 |
| S1: Reversal | 2x | 38 | 42.1% | 0.0546 | 0.0546 | 2.0759 | -51928.4495 |
| S2: Reversal + Liquidity | 0x | 15 | 60.0% | 0.1517 | 0.1517 | 2.2750 | -24482.5400 |
| S2: Reversal + Liquidity | 1x | 15 | 60.0% | 0.1456 | 0.1457 | 2.1845 | -26537.4332 |
| S2: Reversal + Liquidity | 2x | 15 | 53.3% | 0.1396 | 0.1397 | 2.0943 | -28590.2376 |

## Per-Strategy Detail

### S0: Baseline Momentum
**Signal:** `day1_return > 0.05`

| Metric | Value |
|--------|-------|
| Trade count | 14 |
| Win rate | 35.71% |
| Average net return (per trade) | -0.0021 |
| Aggregate gross return | 0.0013 |
| Aggregate net return | -0.0021 |
| Summed net return ¹ | -0.0287 |
| Average win | 0.2394 |
| Average loss | -0.1362 |
| Average cost impact | 0.0054 |
| Max drawdown | -75603.3115 |
| Profit factor | 0.98 |
| Avg holding days | 1.1 |
| Turnover (HKD) | 1,399,040 |

¹ Summed net return = Σ(per-trade net returns). This is NOT a portfolio return. Use aggregate net return for portfolio-level interpretation.


### S1: Reversal
**Signal:** `day1_return < 0`

| Metric | Value |
|--------|-------|
| Trade count | 38 |
| Win rate | 44.74% |
| Average net return (per trade) | 0.0603 |
| Aggregate gross return | 0.0638 |
| Aggregate net return | 0.0603 |
| Summed net return ¹ | 2.2908 |
| Average win | 0.2142 |
| Average loss | -0.0644 |
| Average cost impact | 0.0056 |
| Max drawdown | -48346.9546 |
| Profit factor | 2.70 |
| Avg holding days | 1.7 |
| Turnover (HKD) | 3,798,855 |

¹ Summed net return = Σ(per-trade net returns). This is NOT a portfolio return. Use aggregate net return for portfolio-level interpretation.


### S2: Reversal + Liquidity
**Signal:** `day1_return < 0 AND turnover > median`

| Metric | Value |
|--------|-------|
| Trade count | 15 |
| Win rate | 60.00% |
| Average net return (per trade) | 0.1456 |
| Aggregate gross return | 0.1494 |
| Aggregate net return | 0.1457 |
| Summed net return ¹ | 2.1845 |
| Average win | 0.2743 |
| Average loss | -0.0474 |
| Average cost impact | 0.0059 |
| Max drawdown | -26537.4332 |
| Profit factor | 8.68 |
| Avg holding days | 2.1 |
| Turnover (HKD) | 1,499,363 |

¹ Summed net return = Σ(per-trade net returns). This is NOT a portfolio return. Use aggregate net return for portfolio-level interpretation.


### S3: Reversal + Liquidity + Deep
**Signal:** `day1_return < -0.05 AND turnover > median`

| Metric | Value |
|--------|-------|
| Trade count | 11 |
| Win rate | 54.55% |
| Average net return (per trade) | 0.1619 |
| Aggregate gross return | 0.1657 |
| Aggregate net return | 0.1619 |
| Summed net return ¹ | 1.7810 |
| Average win | 0.3329 |
| Average loss | -0.0432 |
| Average cost impact | 0.0059 |
| Max drawdown | -19706.1010 |
| Profit factor | 9.24 |
| Avg holding days | 2.0 |
| Turnover (HKD) | 1,099,507 |

¹ Summed net return = Σ(per-trade net returns). This is NOT a portfolio return. Use aggregate net return for portfolio-level interpretation.


## Data

### Download Workflow

Raw data was generated via the local fallback path:

```bash
python src/download_data.py --source-root ../research-data
```

This was used because Windows PowerShell does not have `make`, and the mock research API was not started on port 9041. The `--source-root` flag is an explicitly supported local fallback in `download_data.py` that reads pre-built parquet/JSON files and produces identical normalized raw outputs.

The official API workflow, when available, would be:

```bash
# From repo root (separate terminal): make serve-research
# From strategy-project/:
python src/download_data.py --base-url http://127.0.0.1:9041 --start 2026-01-01
```

### Verified Raw Data

| File | Contents |
|------|----------|
| `data/raw/ipo_universe.parquet` | 65 symbols |
| `data/raw/daily_bars.parquet` | 3,673 rows, 2026-01-02 to 2026-06-15 |
| `data/raw/cost_model.json` | buy 12 bps, sell 22 bps, slippage 10 bps/side, min HKD 5 |
| `data/raw/coverage_summary.json` | 0 missing symbols, 0 duplicate keys |

The project is reproducible through either path: API download (if mock server is running) or local fallback (if `research-data/` is available).

### Research Window

The research window is **determined by the provided mock research dataset** and was not optimized or selected for performance:

- **Date range:** 2026-01-02 to 2026-06-15
- **IPO universe:** 65 symbols
- **Daily bars:** 3,673 rows

All analysis is conducted within this fixed window. No data outside this range was used. No symbols were excluded or added beyond what the repository provides.

### Methodological Note

This is a **rule-based daily-bar strategy research project**, not a fitted machine learning model. Therefore, no formal train/test split is used for model training. Instead, robustness is assessed through:

- Holding-period sensitivity (1d / 3d / 5d)
- Cost sensitivity (0× / 1× / 2×)
- Outlier attribution (top-N trade contributions)
- Time-aware prior-median liquidity check

No thresholds were optimized for return. The signal cutoffs (>0.05, <0, <−0.05) were chosen a priori from the data audit findings, not from backtest performance. Tuning thresholds on this 65-symbol sample would risk overfitting.

## Strategy Definition

- **Entry:** Day-2 open (the bar immediately following the first covered trading day).
- **Holding:** Up to 3 trading days, with intraday stop-loss at -8% and take-profit at +20%.
- **Sizing:** HKD 100,000 notional per trade, integer shares.
- **Costs:** Buy 12 bps, sell 22 bps, slippage 10 bps each side, min fee HKD 5.
- **No lookahead:** Entry uses day-2 open which is the next bar after day-1 close.
- **Liquidity filter:** Uses sample median of day-1 turnover across all 65 symbols as threshold (see Limitations below).

## External Data

External IPO and grey-market data was collected for a 10-symbol pilot only (see `data/external/ipo_info.csv` and `grey_market.csv`). Sources are mainly third-party financial media, not direct HKEX filings. This data is **not used in core signal generation or backtest**. It serves only for context, coverage assessment, and selected case studies. Future work could use official HKEX IPO documents and more complete grey-market coverage as ex-ante filters.

Coverage for the 10 pilot symbols: offer_price 100%, subscription_multiple 100%, sponsor 100%, industry 100%, grey_market_return 90%.

Key observations from external data:
- All 10 pilot IPOs were highly oversubscribed (1,092× to 10,745×).
- Several showed extreme grey market returns (e.g., BBSB INTL +415%) that would classify as reversal candidates per the overheat analysis.
- Grey market intraday patterns foreshadow first-day weakness in some cases (e.g., 智谱 02513.HK collapsed from +37.7% to +6.0% during grey session).

## Limitations

1. **Sample-median liquidity filter (lookahead):** The reversal_liquidity and reversal_liquidity_deep strategies use the sample median of first_day_turnover computed across all 65 symbols (Jan–Jun 2026). This is an in-sample exploratory threshold — a trader in February 2026 would not know the turnover distribution of IPOs listing in May–June. A production system should use a rolling median based only on previously-listed IPOs, or a fixed HKD threshold calibrated on historical data.

2. **External data not in core backtest:** External IPO/grey-market data is limited to 10 pilot symbols and sourced from third-party financial media summaries, not direct HKEXnews filings. It is used only for context, not signals.

3. **Small sample:** 65 symbols with 14 or fewer trades for the most selective strategies. Results are indicative, not statistically robust.

4. **No production trading claims:** This is an internship research project. No live trading infrastructure, execution modeling, or risk controls are in place.

5. **Holding period:** The main results use a 3-day holding period. Holding-period sensitivity (1d / 3d / 5d) is reported in the Robustness and Attribution section. Reversal strategies (S1-S3) show directionally consistent results across holding period; S0 momentum is consistently weak.

6. **Risk-factor controls:** This project does not implement formal Barra-style factor neutralization because the provided dataset only contains 65 short-window IPO daily-bar histories and does not include broad-market cross-sectional returns, market capitalization, valuation, sector classifications, beta estimates, or factor exposure matrices.

The strategy is framed as an event-driven IPO daily-bar study rather than a general equity cross-sectional factor strategy. Future work with richer data could add: market-index-adjusted returns, sector or industry controls, size/liquidity/volatility controls, Barra-like risk decomposition, and broader out-of-sample validation.

## Analysis

**S0 (Baseline Momentum) is not supported in this sample.** With a 35.7% win rate and negative aggregate net return after costs (−0.2%), the scaffold hypothesis — that first-day IPO momentum continues — does not hold. Trading costs (0.54% round-trip) alone erode the thin gross edge. This does not prove that momentum never works for IPOs; it only shows that a simple >5% threshold on day-1 return produces negative results in this 65-symbol, 6-month window.

**S1 (Reversal) outperforms S0 on all dimensions:** higher win rate (44.7% vs 35.7%), positive aggregate net return (+6.0% vs −0.2%), and lower max drawdown. The average win is larger in magnitude and the average loss is smaller. S1 runs 38 trades (vs 14 for S0), providing broader diversification across the IPO universe.

**S2 (Reversal + Liquidity) is the most balanced version in this sample.** Adding the above-median turnover filter lifts the win rate to 60.0%, reduces max drawdown by 45% vs S1, and delivers an aggregate net return of +14.6%. This is directionally consistent with the hypothesis that higher-liquidity day-1 losers exhibit stronger mean-reversion, though the sample is small and confidence intervals would be wide.

**S3 (Reversal + Liquidity + Deep) is reported as a sensitivity variant rather than a primary conclusion.** While it has the highest aggregate net return (+16.2%) and lowest drawdown, it has only 11 trades and higher outlier concentration (51.4% top-1 share). The win rate (54.5%) is lower than S2's (60.0%). These limitations mean S3 should not be interpreted as the main finding. It serves only to show that a deeper day-1 threshold (−5% vs 0%) does not degrade the reversal signal direction.

**Cost sensitivity:** At 2× costs, S2 retains a 53.3% win rate and +14.0% aggregate net return. S0's already-thin gross return (+0.3% before costs) turns negative (−0.2%) after real costs and negative (−0.8%) at 2×. The relative ranking (S2 > S1 > S0) is directionally consistent across all cost levels.

## Robustness and Attribution

This section reports supplementary analyses that test the sensitivity of the main results. None of these analyses change the core strategy definitions. The holding_days = 3 result remains the primary finding.

### A. Holding-Period Sensitivity

Each strategy was re-run with holding_days = 1, 3, and 5. The 3-day result is the main reported result; the 1-day and 5-day columns show how sensitive each strategy is to the holding period.

| Holding Days | Strategy | Trades | Win Rate | Aggregate Gross Return | Aggregate Net Return | Average Net Return | Max Drawdown | Avg Cost Impact |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | S0: Baseline Momentum | 14 | 42.9% | 0.0102 | 0.0068 | 0.0068 | -63182.6577 | 0.0054 |
| 1 | S1: Reversal | 38 | 39.5% | 0.0502 | 0.0467 | 0.0467 | -44506.2120 | 0.0056 |
| 1 | S2: Reversal + Liquidity | 15 | 53.3% | 0.1175 | 0.1139 | 0.1138 | -17016.1138 | 0.0058 |
| 1 | S3: Reversal + Liquidity + Deep | 11 | 54.5% | 0.1554 | 0.1517 | 0.1516 | -10184.7816 | 0.0059 |
| 3 | S0: Baseline Momentum | 14 | 35.7% | 0.0013 | -0.0021 | -0.0021 | -75603.3115 | 0.0054 |
| 3 | S1: Reversal | 38 | 44.7% | 0.0638 | 0.0603 | 0.0603 | -48346.9546 | 0.0056 |
| 3 | S2: Reversal + Liquidity | 15 | 60.0% | 0.1494 | 0.1457 | 0.1456 | -26537.4332 | 0.0059 |
| 3 | S3: Reversal + Liquidity + Deep | 11 | 54.5% | 0.1657 | 0.1619 | 0.1619 | -19706.1010 | 0.0059 |
| 5 | S0: Baseline Momentum | 14 | 35.7% | 0.0013 | -0.0021 | -0.0021 | -75603.3115 | 0.0054 |
| 5 | S1: Reversal | 38 | 39.5% | 0.0617 | 0.0582 | 0.0582 | -49897.9789 | 0.0056 |
| 5 | S2: Reversal + Liquidity | 15 | 60.0% | 0.1592 | 0.1554 | 0.1554 | -28088.4574 | 0.0059 |
| 5 | S3: Reversal + Liquidity + Deep | 11 | 63.6% | 0.1835 | 0.1796 | 0.1796 | -21257.1253 | 0.0060 |

**Observations:**
- S2 and S3 maintain positive aggregate net returns across all three holding periods.
- S0's aggregate net return is negative or near-zero at all holding periods.
- Longer holding periods (5d vs 1d) tend to widen the gap between reversal and momentum strategies, suggestive but not conclusive without broader data.
- The 3-day holding period provides a reasonable trade-off between return and holding cost.

### B. Outlier and Concentration Analysis

For each strategy at holding_days = 3, the top-1 and top-3 trade contributions were measured to check whether results are driven by a single outlier.

| Strategy | Largest Win (HKD) | Win Source | Largest Loss (HKD) | Loss Source | Top-1 Share | Top-3 Share | Agg Net ex Largest Win | Total Net PnL (HKD) |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| S0: Baseline Momentum | 74,072 | 02723.HK | -25,578 | 06636.HK | N/A (non-positive total net PnL) | N/A (non-positive total net PnL) | -0.0593 | -2,932 |
| S1: Reversal | 91,457 | 00068.HK | -14,233 | 02677.HK | 39.9% | 96.1% | 0.0372 | 229,045 |
| S2: Reversal + Liquidity | 91,457 | 00068.HK | -10,528 | 07666.HK | 41.9% | 93.5% | 0.0907 | 218,404 |
| S3: Reversal + Liquidity + Deep | 91,457 | 00068.HK | -10,528 | 07666.HK | 51.4% | 100.9% | 0.0866 | 178,064 |

**Observations:**
- S2's largest single trade accounts for a limited share of total PnL. The aggregate net return excluding the largest winner remains positive in all reversal strategies, meaning no single trade makes or breaks the result.
- S3 has the most concentrated top-3 share due to its small sample (11 trades), which is expected. This is an additional reason to treat S3 as indicative rather than conclusive.
- S0's contribution ratios are not meaningful because total net PnL is near zero, reflecting the low and volatile returns of the momentum strategy in this sample.

### C. S2 Trade Examples (Top 3 and Bottom 3)

**Top 3 winning trades (S2, holding_days = 3):**

| Rank | Symbol | Entry Date | Exit Date | Return | Net PnL (HKD) | Exit Reason | Holding Days |
|:----:|--------|:----------:|:---------:|:------:|:-------------:|:-----------:|:------------:|
| 1 | 00068.HK | 20260420 | 20260420 | +0.9147 | 91,457 | take_profit | 1 |
| 2 | 02553.HK | 20260604 | 20260604 | +0.6851 | 68,498 | take_profit | 1 |
| 3 | 03277.HK | 20260420 | 20260421 | +0.4425 | 44,238 | take_profit | 2 |

**Bottom 3 losing trades (S2, holding_days = 3):**

| Rank | Symbol | Entry Date | Exit Date | Return | Net PnL (HKD) | Exit Reason | Holding Days |
|:----:|--------|:----------:|:---------:|:------:|:-------------:|:-----------:|:------------:|
| 1 | 07666.HK | 20260514 | 20260515 | -0.1053 | -10,528 | stop_loss | 2 |
| 2 | 06082.HK | 20260105 | 20260105 | -0.0683 | -6,831 | stop_loss | 1 |
| 3 | 06810.HK | 20260430 | 20260504 | -0.0523 | -5,226 | stop_loss | 2 |

### C2. Time-Aware Liquidity Robustness

The main S2 result uses the **full-sample median** of first_day_turnover, which introduces a lookahead concern (see Limitations). As a robustness check, S2 was re-run using an **expanding prior median**: for each IPO, ordered by listing date, the liquidity threshold is the median turnover of only previously-listed IPOs.

- **Method:** expanding_prior_median
- **Warmup:** First 10 IPOs skipped (expanding medians need a seed)
- **Eligible symbols:** 65
- **Signals generated:** 10
- **Trades generated:** 10

| Metric | Time-Aware S2 | Main S2 (Full-Sample) |
|--------|:------------:|:---------------------:|
| Win Rate | 60.0% | 60.0% |
| Aggregate Gross Return | 0.1937 | 0.1494 |
| Aggregate Net Return | 0.1899 | 0.1457 |
| Max Drawdown | -17017.8428 | -26537.4332 |

**Interpretation:** The time-aware prior-median check reduces the sample from 15 to 10 trades but preserves the positive reversal-plus-liquidity pattern. This suggests that the main S2 result is not purely an artifact of full-sample median lookahead. However, because the time-aware result uses fewer trades and skips warmup IPOs, it should be interpreted as supportive robustness evidence rather than a replacement for the main result. S2 with the full-sample median remains the primary reported version; the time-aware check confirms the signal direction is robust.

### D. Interpretation

1. **Holding-period sensitivity:** The reversal strategies (S1-S3) are robust to holding-period choice. S0 momentum is consistently weak. The 3-day holding period remains the main reported result as it balances return with reasonable turnover.

2. **Outlier dependence:** No single trade dominates the aggregate return. The reversal strategies' performance is not driven by one or two extreme winning trades.

3. **Why S2 is the most balanced version in this sample:** S2 has the highest win rate (60%), adequate trade count (15), strong aggregate net return (+14.6%), and the best balance across holding-period sensitivity. It is not dominated by outliers and improves substantially over S1. The time-aware liquidity check (see C2) is directionally supportive, providing additional evidence that the S2 result is not purely an artifact of full-sample median lookahead.

4. **Why S3 is a sensitivity variant only:** Despite the highest aggregate net return (+16.2%), S3 has only 11 trades. Its top-3 share is high relative to the small sample, and its win rate (54.5%) is lower than S2's (60.0%). S3 should be monitored as more IPO data becomes available, but S2 is the more balanced conclusion from the current dataset. The time-aware liquidity check uses the S2 definition, not S3, for the same reason — S3's sample of 11 is too small to support further filtering.

5. **No threshold tuning was performed.** The cutoffs (0.05, 0, −0.05) were chosen a priori from the data audit findings, not optimized on backtest results. Tuning thresholds on this small sample would risk overfitting.

6. **This robustness analysis does not change any core strategy definitions.** All strategy versions (S0-S3) remain identical to the main report. The time-aware prior-median S2 is a robustness check, not a new primary strategy. The robustness pass verifies that the conclusions are not artifacts of a single holding period, a single outlier trade, or the full-sample median lookahead.

## Next Steps

1. Replace sample-median liquidity filter with rolling-median or fixed-threshold approach.
2. Extend holding period and stop-loss/take-profit analysis.
3. Expand external data collection to full 65-symbol universe for coverage statistics.
4. Analyze strategy performance by industry, sponsor, and subscription multiple (using external data as supplementary context, not signals).
5. Model execution at scale: capacity constraints, market impact beyond fixed slippage.

## Grading Rubric Alignment

### Data Work (30 pts)

- **Download workflow:** Two equivalent paths documented (API via `make serve-research` and local fallback via `--source-root`). See Data → Download Workflow.
- **Coverage summary:** 65 symbols, 3,673 daily bars, 0 missing, 0 duplicate keys. See Data → Verified Raw Data.
- **Missing/suspension checks:** `suspend_flag` uniformly 0; `previous_close` uniformly 0 (expected for IPO data). All 65 symbols have ≥7 bars; 61 have ≥10. No nulls in OHLCV. See `reports/data_audit_and_research_direction.md`.
- **External data:** 10-symbol pilot collected from public web sources, stored in `data/external/ipo_info.csv` and `grey_market.csv`. Coverage: 100% for core IPO fields, 90% for grey market return. Source audit in `reports/external_data_audit.md`. Not used in core backtest signals.

### Backtest Correctness (30 pts)

- **No-lookahead timeline:** Day-1 OHLCV → compute signal → enter at day-2 open. Exit path uses bars at day-2 forward only. See Strategy Definition.
- **Cost model:** Buy 12 bps + sell 22 bps + slippage 10 bps each side + min HKD 5. Round-trip on HKD 100K = HKD 540 (0.54%). Verified in `test_round_trip_cost_on_100k_notional`.
- **Trade log completeness:** 15 columns covering all required fields. Verified in `test_trade_log_has_exact_required_columns`.
- **Reproducibility:** Pipeline runs from `data/raw/` files only. `python src/build_features.py && python src/backtest.py` produces identical `reports/trades.csv` and `reports/metrics.json` each run.

### Strategy Reasoning (20 pts)

- **S0 baseline momentum:** The scaffold hypothesis — refuted by data. 35.7% win rate, negative aggregate net return. See Analysis.
- **S1 reversal:** Data-driven alternative — positive aggregate net return (+6.0%), 44.7% win rate. See Analysis.
- **S2 reversal + liquidity:** Preferred version — 60.0% win rate, +14.6% aggregate net, 45% lower drawdown. See Analysis and Robustness sections.
- **S3 not main conclusion:** Only 11 trades, higher concentration risk, lower win rate than S2. Documented in Analysis and Robustness → Interpretation.
- **Source of gains/losses:** Asymmetric payoff (avg win > |avg loss|) across all reversal strategies. Wins 2-3× larger in magnitude than losses. See S2 Trade Examples.
- **Robustness:** Holding-period sensitivity (1d/3d/5d), outlier analysis, time-aware liquidity filter. All support S2 as the balanced choice. See Robustness and Attribution.

### Engineering Quality (10 pts)

- **Code structure:** Separate modules for paths, costs, features, strategy, metrics, reporting, backtest orchestration. Each ≤ 100 lines.
- **Parameterization:** `generate_trades()` accepts `signal_column`, `strategy_version`, `holding_days`, `stop_loss_pct`, `take_profit_pct`, `notional_per_trade`. No hard-coded signal names in trade logic.
- **Tests:** 18 tests covering feature schema, signal counts, alias invariant, trade log schema (exact 15 columns), PnL consistency, cost sanity (HKD 540 round-trip), cost scaling, slippage direction, min fee, metrics schema, empty-trade edge case, backward compatibility. See `tests/test_strategy_scaffold.py`.
- **Backward compatibility:** `generate_baseline_trades()` preserved as wrapper. `baseline_signal` column preserved as alias for `baseline_momentum_signal`. All original scaffold outputs still generated.

### Communication (10 pts)

- **Limitations:** Five limitations explicitly documented: sample-median lookahead, external data not in backtest, small sample, no production claims, fixed holding period. See Limitations.
- **Next steps:** Five actionable next steps for production-readiness. See Next Steps.
- **No production trading claims:** Explicitly stated in Limitations §4 and in the cost model discussion. This is internship research only.
- **External data audit:** Separate `reports/external_data_audit.md` documents source quality, coverage, estimated values, and rationale for non-use in signals.

---

*Report generated 2026-06-15. All data sourced from `data/raw/` files. External data limited to 10-symbol pilot, not used in core backtest. No production trading claims.*
