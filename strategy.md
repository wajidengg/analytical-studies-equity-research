NSE Reversal Scanner — Project Plan
1. Goal

Build a simple, professional NSE reversal-scanning system that:

Scans a fixed stock universe.
Generates reversal signals using the existing V6 logic.
Produces a clean shortlist rather than overwhelming output.
Runs automatically on trading days.
Gives the signal before market close, leaving time for manual review.
Keeps backtesting and live scanning separate.
Can optionally incorporate ML later without making ML the core strategy.
2. Recommended Project Structure

Keep the project small and modular:

nse-reversal-scanner/
│
├── config.py
├── data.py
├── indicators.py
├── strategy.py
├── backtest.py
├── report.py
├── run_scanner.py
│
├── data/
│   └── cache/
│
├── output/
│   ├── signals/
│   ├── reports/
│   └── backtests/
│
├── tests/
│   └── test_strategy.py
│
├── requirements.txt
└── README.md

What each file does

config.py

All settings in one place:

Universe
RSI settings
EMA settings
ATR settings
Score threshold
Holding period
Risk settings
Test dates
Output paths


Avoid scattering constants throughout the code.

data.py

Only handles market data:

download data
clean OHLCV
cache data
load historical data
load NIFTY


indicators.py

Only calculates indicators:

RSI
ATR
EMA
MACD
volume averages
support
52-week low


strategy.py

The heart of the scanner:

candlestick patterns
divergence
reversal conditions
scoring
classification
signal generation


This should contain the actual trading logic and as little infrastructure code as possible.

backtest.py

Handles:

entry simulation
stop/target
holding period
portfolio simulation
benchmark comparison
drawdown
performance statistics


report.py

Turns results into useful output:

daily signal report
CSV files
summary tables
ranking


run_scanner.py

The simple entry point:

python run_scanner.py


It orchestrates everything but shouldn't contain strategy logic.

3. Keep Backtest and Live Scanner Separate

This is important.

Use the same strategy engine, but have two different execution paths:

                 strategy.py
                     │
          ┌──────────┴──────────┐
          │                     │
      backtest.py          run_scanner.py
          │                     │
     Historical data       Today's data
          │                     │
       Results             Live signals


This prevents the live scanner from becoming tangled with backtesting code.

4. Daily Workflow

The eventual workflow should be extremely simple:

Market data
     ↓
Universe scan
     ↓
Indicators
     ↓
Reversal conditions
     ↓
Score
     ↓
Quality filters
     ↓
Rank signals
     ↓
Daily report
     ↓
Manual review
     ↓
Optional trade


The system should assist your decision, not automatically trade initially.

5. Timing

For a daily NSE scanner, I would prefer generating the final signal around 2:45–3:00 PM IST, rather than exactly at 3:00 PM.

That gives you some time to review.

For example:

2:45 PM
    ↓
Download latest data
    ↓
Run scanner
    ↓
Rank candidates
    ↓
2:50–2:55 PM
Review shortlist
    ↓
3:00 PM+
Decision


However, be very careful about the meaning of the latest candle.

If you use the current day's candle before market close, OHLC values are still changing.

Therefore distinguish between:

Confirmed signal

Uses the previous completed daily candle.

Intraday/pre-close signal

Uses the partially formed current candle.

For a robust system, I would initially use the completed previous candle.

That makes the live scanner consistent with the historical backtest.

6. Recommended Daily Output

Don't generate a giant CSV and expect yourself to inspect everything.

Generate a small ranked report such as:

NSE REVERSAL SCANNER
Date: 24-Aug-2026

1. HDFCBANK
   Score: 78
   Classification: CONFIRMED
   Pattern: Bullish Engulfing
   RSI: 32 → 38
   Volume: 1.9x
   Support: YES
   EMA20 Reclaim: YES
   Risk: ₹X
   Target: ₹X

2. INFY
   Score: 72
   Classification: CONFIRMED
   Pattern: Morning Star
   ...

3. SBIN
   Score: 65
   Classification: EARLY
   ...


Then optionally save the full technical data to CSV.

The human-facing report should be short.

7. Don't Overweight Candlestick Patterns

The current project should treat:

Hammer
Bullish Engulfing
Morning Star

as components of a reversal setup, not standalone buy signals.

A candle becomes much more interesting when combined with things such as:

Downtrend
+
Support
+
Oversold/recovering RSI
+
Improving volume
+
Bullish candle
+
Momentum improvement


The location/context is generally more important than simply identifying a candle.

8. ML — Is It Advisable?

Yes, but not yet as the main decision-maker.

Don't replace the existing strategy with:

Indicators → ML → BUY


Instead, eventually test:

Existing scanner
      ↓
Candidate signals
      ↓
ML probability/ranking
      ↓
Human review


This is a much safer project direction.

Good ML use

ML could estimate:

P(positive return over next 5 days)
P(hit target before stop)
expected return
probability of large drawdown


Or simply rank the existing signals:

HDFCBANK  78% confidence
INFY      71%
SBIN      64%
...

Avoid initially

Don't build a huge model using hundreds of indicators.

That makes overfitting very easy.

Start with the existing signal as the baseline and ask:

Can ML improve the ranking of signals without destroying out-of-sample performance?

9. Most Important ML Rule

Never train ML using your 2026 test results.

Your current philosophy is correct:

Training / development
        ↓
Validation
        ↓
Frozen model
        ↓
2026 OOS test


If you use the 2026 results to choose:

RSI threshold
score threshold
candle weighting
ML features
model type


then 2026 is no longer a clean out-of-sample test.

10. Future ML Architecture

When ready, keep it as a separate module:

ml/
├── features.py
├── train.py
├── predict.py
└── model.pkl


The existing scanner remains usable even if ML is disabled.

For example:

Scanner
   ↓
92 candidates
   ↓
ML ranking
   ↓
Top 5 candidates


rather than making the entire system dependent on ML.

11. Automation

Eventually the project should run automatically.

A simple production workflow:

Scheduler
    ↓
run_scanner.py
    ↓
data download
    ↓
signal generation
    ↓
ranking
    ↓
report
    ↓
CSV / HTML / notification


You could eventually receive something like:

NSE Reversal Scanner — 2:50 PM

3 high-quality setups found

1. HDFCBANK — 81 — CONFIRMED
2. SBIN     — 76 — CONFIRMED
3. INFY     — 68 — EARLY


The first version should simply save a report locally. Notifications can be added later.

12. Automation Infrastructure

For a personal project:

Local computer

Use:

cron


on Linux/macOS, or:

Task Scheduler


on Windows.

Cloud

Later, move it to a small cloud server or scheduled workflow.

The important thing is that the scanner itself shouldn't care where it runs.

That's why run_scanner.py should be the single entry point.

13. Data Reliability

This deserves special attention.

Your backtest showed issues such as:

TMCV → insufficient history
IRFC → shorter history
RVNL → shorter history


Don't silently treat missing data as normal.

Create a small data-quality report:

Symbol      Status
HDFCBANK    OK
INFY        OK
TMCV        INSUFFICIENT_HISTORY
IRFC        LIMITED_HISTORY


For production, also log:

download time
last available candle
missing sessions
NaN values
failed downloads
number of stocks scanned

14. Backtest Lessons From V6

The V6 result is useful as a baseline.

Your overall result was approximately:

92 trades
46.74% win rate
Profit factor: 0.976
Average return: -0.040%
Expectancy: -0.0236 R
Maximum drawdown: ~13.14%


The interesting part was the classification split:

EARLY
81 trades
Expectancy: negative

CONFIRMED
8 trades
75% win rate
Profit factor: 3.47
positive expectancy

STRONG_CONFIRMED
3 trades
too few trades to draw conclusions


The CONFIRMED sample is interesting, but only 8 trades means it is nowhere near enough evidence to conclude that the classification is genuinely superior.

This is exactly where future validation should focus.

15. What I Would Build Next

Don't add 20 new indicators.

Build the project in this order:

1. Clean project structure
        ↓
2. Separate data / strategy / backtest
        ↓
3. Make V6 reproducible
        ↓
4. Add automated daily scanner
        ↓
5. Create concise ranked report
        ↓
6. Improve data validation
        ↓
7. Collect live/paper-trading results
        ↓
8. Build ML experiment separately
        ↓
9. Compare ML vs baseline


The key principle is:

Keep the core scanner simple, reproducible, and interpretable. Add ML as a ranking layer only after the baseline has been properly validated.

That gives you a project that can start as a research/backtesting tool and gradually become a daily decision-support system without having to rewrite everything later.
