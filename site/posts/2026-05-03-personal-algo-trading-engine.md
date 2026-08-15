---
title: "Personal Algo/AI Trading Engine"
subtitle: What the field actually does, and what to build for a quick budge.
date: 2026-05-03
tags: trading, ai, python, projects
draft: false
---

A tour of the personal algo-trading landscape from 2015 to 2026, the broker API
layer today, three strategies worth backtesting, an honest assessment of where
AI actually helps, and a 90-day plan with halt rules.

## 1. The Landscape, 2015 → 2026

**2015–2020 — the Quantopian era.** A hosted platform with shared S&P 500 data
fostered *massive* overfitting. It shut down progressively: live trading in
2017, paper trading in 2019, contests and community in 2020. Robinhood acquired
the tech.

**2020–2022 — the diaspora.** Traders scattered to QuantConnect/LEAN,
Backtrader, vectorbt, no-code platforms (Composer, Streak, Smallcase), and
API-first brokers like Alpaca and Zerodha Kite Connect.

**2022–2026 — the LLM-augmented era.** LLMs accelerated *research* — filings
and earnings summaries via OpenBB and LangChain agents — but per backtests,
GPT-4/5- and Claude-4-class models **underperform a simple buy-and-hold
baseline on most universes**.

The typical 2026 stack:

```
API-first broker  +  vectorized research env  +  event-driven execution
                 +  optional LLM layer (summarization only)
```

## 2. The Broker API Layer (SG/US + India)

- **Zerodha Kite Connect** — data APIs cut to ₹500/mo; order/account APIs now
  free. 10 req/sec, 3,000 WebSocket instruments, static-IP requirement for
  order APIs (~Aug 2025). No native paper trading.
- **Moomoo OpenAPI** — multi-language SDKs, built-in paper trading via the
  OpenD gateway process. April 2026 "API Skills" lets personal AI agents
  translate natural language into strategies — the first broker-native agentic
  retail layer.
- **Alpaca** — free paper trading with real-time data; enforces the PDT rule
  even in paper. Ranked #1 retail algo broker 2026.
- **IBKR** — the institutional-adjacent reserve option.

> Recommendation: Moomoo SG + Kite Connect free tier, and keep the code
> broker-agnostic behind a thin adapter.

## 3. Platforms

- Backtesting: **QuantConnect free tier** *or* local **vectorbt** — pick one.
- Skip QuantConnect's paid live nodes ($60/mo is a **72% annual drag on a $1k
  book**).
- Streak free tier as India training wheels; Tickertape for fundamentals;
  avoid paid smallcases.

## 4. Three Strategies

All tuned for capital preservation, long horizon, wide stops.

### A — 200-Day SMA Trend Filter (Faber)

Hold the index ETF above the 200-SMA, move to cash below it.

| Metric        | Strategy | Buy & hold |
|---------------|----------|------------|
| CAGR          | ~6.45%   | ~7%        |
| Max drawdown  | **28%**  | 56%        |

The cost: whipsaws in choppy markets (messy COVID March 2020 flips).

### B — Quality + Momentum ETF Tilt

50/50 QUAL/JOET plus MTUM/VFMO, rebalanced quarterly. The quality premium is
~3.2%/yr since 1963. Fails in regime reversals.

### C — Volatility-Triggered Tranched Deployment

Keep a 20–30% cash reserve; deploy in thirds at VIX>30, −10% drawdown, and
−20% drawdown. Targets the missed-dislocation problem; drags in quiet years.

> Suggested build: **B as the core, A as the kill switch, plus C's reserve
> bucket.**

## 5. AI's Actual Role

| Tier | Role            | Verdict |
|------|-----------------|---------|
| 1    | Research assistant | ✅ supported by evidence (FinGPT ~88% F1 sentiment) |
| 2    | Signals         | ⚠️ ~45–53% movement-prediction accuracy; LLM strategies returned 4.7–18% vs Berkshire's 42% |
| 3    | Agents          | ❌ the plumbing exists; the signals don't work |

**Don't use LLMs as traders.** Ernie Chan's advice holds: ML for risk
management and allocation only, not strategy building. Use AI at Tier 1 —
OpenBB plus a weekly LLM digest.

## 6. Risk and Backtesting

- 74–89% of retail traders lose money; SEBI: **93% of Indian retail F&O traders
  lost money** (FY22–24).
- Lopez de Prado's failure list: overfitting, survivorship bias, look-ahead
  bias, storytelling, transaction costs, outlier dependency.
- Position sizing dominates: at 1% risk/trade, ruin risk is ~0.005%; at 5%,
  it's 13.6% — a **2,700× increase**.
- Use walk-forward analysis and the Deflated Sharpe Ratio.
- SPIVA: 94.1% of active large-cap funds underperform over 20 years. Benchmark
  against the index; halt if lagging >3% annualized after 6 months.

## 7. Recommended Stack + 90-Day Plan

**Stack (~$0–30/mo):** Moomoo SG + Kite Connect ($0) · OpenBB + Tickertape ·
vectorbt or QuantConnect free · thin Python adapter · Streak optional · LLM API
$5–20/mo.

**Phases:**

1. **Week 0** — reading + account setup
2. **Weeks 1–2** — paper-only Strategy A
3. **Weeks 3–6** — tiny live trades ($250–500 US / ₹15–25k India) at 1% sizing
4. **Weeks 7–12** — add the reserve bucket and scale

**Halt rules:** >3% annualized lag after 6 months · single-trade losses >10%
with a sell signal · monthly drawdown >15%. No F&O, no crypto, no ML signals
for 12 months.

**At $10k+:** QuantConnect Researcher tier, vectorbt-pro, a mean-reversion
Strategy D, and IBKR for covered calls.
