# External Data Audit

**Date:** 2026-06-15 | **Author:** 刘子睿 (Liu Zirui) | **Project:** intern-gym / strategy-project

## Scope

This audit covers the 10-symbol pilot external data collection stored in:

- `data/external/ipo_info.csv`
- `data/external/grey_market.csv`

No additional data was collected beyond this pilot. The remaining 55 symbols have no external data.

---

## Field Coverage — IPO Info (10 symbols)

| Field | Count | Coverage | Source Quality |
|-------|:-----:|:--------:|:--------------:|
| `symbol` | 10 | 100% | N/A (key) |
| `company_name` | 10 | 100% | All from third-party financial media (HK StockStar, AASTOCKS, Futu) |
| `official_listing_date` | 10 | 100% | Third-party media citing HKEX filings |
| `offer_price` | 10 | 100% | Confirmed via multiple third-party sources |
| `offer_price_low` | 4 | 40% | Only reported when final price differs from midpoint |
| `offer_price_high` | 4 | 40% | Same as low |
| `public_subscription_multiple` | 10 | 100% | Third-party media citing HKEX allotment results |
| `one_lot_success_rate` | 10 | 100% | Third-party media |
| `sponsor` | 10 | 100% | Third-party media |
| `industry` | 10 | 100% | Third-party media |

### Source Type Classification

| Type | Count | Examples |
|------|:-----:|----------|
| **Third-party media** | 10 | HK StockStar, AASTOCKS, HKET, Futu News, Yahoo Finance HK |
| **Official (HKEXnews direct)** | 0 | No direct PDFs retrieved — all via media intermediaries |
| **Estimated** | 1 | 02723.HK grey market close estimated from 一手盈利 data |
| **Missing** | 0 | Fields left blank when unavailable |

---

## Field Coverage — Grey Market (10 symbols)

| Field | Count | Coverage | Notes |
|-------|:-----:|:--------:|-------|
| `grey_market_date` | 10 | 100% | Date of grey market session |
| `grey_market_close` | 9 | **90%** | 02723.HK estimated; all others sourced from broker quotes |
| `grey_market_return_pct` | 9 | **90%** | Same caveat |
| `grey_market_turnover_hkd` | 5 | **50%** | Only available when explicitly reported by broker |
| `primary_platform` | 10 | 100% | 辉立 (Phillip) primary; 富途 (Futu) fallback |

---

## Estimated Values

| Symbol | Field | Method | Reliability |
|--------|-------|--------|:-----------:|
| 02723.HK | grey_market_close | Back-solved from reported 一手盈利 (~HKD 9,350 per lot) | Low — approximate |
| 02723.HK | grey_market_return_pct | Derived from estimated close | Low — approximate |

These estimated values are flagged in `source_note` with the word "est." and should not be treated as exact.

---

## Why External Data Is Not Used in Core Backtest

1. **Coverage incompleteness:** Only 10 of 65 symbols have external data. Using it as a signal would bias the backtest toward well-covered (hot) IPOs.
2. **Uneven source quality:** Data comes from third-party media summaries, not direct exchange filings. No HKEXnews PDF was directly parsed. This makes data provenance weaker than the repository-provided OHLCV bars.
3. **Grey market lookahead risk:** Grey market data is only available on the grey market trading day (business day before listing). Using it in signals requires timestamp-aware alignment that the current pipeline does not implement.
4. **Non-standardized prices:** Grey market quotes come from different broker dark pools (辉立, 富途, 耀才) with different participant bases. There is no single "official" grey market price.
5. **Reproducibility:** External data collection depends on manual web search. Another researcher running the pipeline in a different environment may find different sources or stale links. The core backtest must be reproducible from `data/raw/` files alone.
6. **Methodological separation:** Per the project specification, IPO fundamentals and grey-market data are "not provided" and must be "independently researched." The instructions explicitly state that candidates should use these only as supplementary context.

---

## Why Missing Values Are Left Blank (Not Zero-Filled)

1. **Zero-filling creates fictitious data.** A blank field means "we do not know." Filling it with 0 would mean "we know it is zero" — a false claim.
2. **Zero has semantic meaning.** A subscription multiple of 0 would imply no one subscribed (impossible for a listed IPO). A grey market return of 0 would imply flat grey market trading — a specific claim requiring evidence.
3. **Per the project instructions:** "Do not fill missing public data with zero. Leave missing values blank and explain coverage limitations in the report."
4. **Downstream safety:** If external data were ever to be used in signals (not recommended), blank cells naturally propagate as `NaN` through pandas operations, triggering explicit handling rather than silently producing incorrect results.

---

## Data Provenance

| Source Tier | Source Name | Symbols Sourced | Type |
|:-----------:|-------------|:---:|------|
| 1 (Highest) | HKEXnews (披露易) | 0 | Official exchange filing (not directly retrieved) |
| 2 | AASTOCKS IPO Plus | 4 | HK financial data aggregator |
| 3 | HKET / hket (經濟日報) | 3 | HK financial media |
| 4 | Futu (富途) | 1 | Broker research page |
| 5 | HK StockStar (證券之星) | 5 | Mainland financial media |
| 6 | Yahoo Finance HK | 1 | Aggregator |
| — | Estimated | 1 | Calculated from secondary info |

---

## Recommendations

1. **Do not expand external data collection** beyond the 10-symbol pilot. The marginal benefit for a 65-symbol research project is low given the source quality constraints.
2. **Use external data only as case studies** in the research report narrative (e.g., explaining why certain symbols had extreme day-1 returns).
3. **Acknowledge source limitations** explicitly: all data is third-party, no direct HKEXnews PDFs were parsed, and one grey market value is estimated.
4. **Full external data coverage is possible** but requires automated retrieval from HKEXnews or a structured API, which is beyond the scope of an internship research project.
