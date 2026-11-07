# Settlement timing and intraday price pressure: Vietnam's T+2 afternoon selling rule

Data and code for

> Tran, M.H. and Tran, M.N. (2026). *Settlement timing and intraday price pressure: Evidence from Vietnam's T+2 afternoon selling rule.* Working paper, Banking Academy of Vietnam.

Since 29 August 2022 (Decision 109/QĐ-VSD), shares bought on day T on the Ho Chi Minh Stock Exchange can be sold in the
afternoon session of day T+2, but not in its morning session; before that date they could first be sold on day T+3.
The paper shows that, after the change, the index falls when trading resumes after the lunch break on about 88% of days,
that the decline is predicted by trading value two days earlier (not one or three days earlier) and that it reverses within 30 minutes.

## Contents

| Path | Description |
|---|---|
| `data/VNINDEX_1min.csv.gz`, `data/VN30_1min.csv.gz` | One-minute index records, 2022-2026, provided by FiinGroup (see `data/README.md`) |
| `ana/load.py` | Reads the data files and caches them as pickles |
| `ana/buildB.py` | Samples the continuous sessions (9:15-11:30, 13:00-14:30) on a regular one-minute grid |
| `ana/t2_data.py` | Daily return components (overnight, morning, lunch, afternoon, closing auction) and abnormal trading value |
| `ana/t2_tables.py` | All regressions and tests; writes `results/results.json` |
| `ana/t2_figs.py` | Figure 1 (intraday return path) and Figure 2 (lunch return by quintile of lagged trading value) |
| `run_all.sh` | Runs everything in order |

## Reproducing the results

```bash
git clone https://github.com/manhhab/vn-settlement-intraday-pressure.git
cd vn-settlement-intraday-pressure
pip install -r requirements.txt
./run_all.sh
```

The full run takes less than a minute on a laptop. `results/results.json` contains every number reported in the tables
(keys `T1`-`T5`, `T3p` for the other return components and `Q` for Figure 2), separately for the VNINDEX and the VN30.

## Definitions

* Return components (log returns, %): `ON` = previous close to the first morning price (incl. opening auction);
  `AM` = morning session; `LUNCH` = last morning price (11:30) to first afternoon price (13:00);
  `PM` = afternoon session; `ATC` = closing auction. They sum to the close-to-close return `CC`.
* Abnormal trading value `AV(t)` = log of matched trading value on day t over its average on the previous 10 days.
* Standard errors are Newey-West with five lags.

## Licence and citation

Code: MIT licence (see `LICENSE`). Data: provided by FiinGroup and shared free of charge for research and replication;
please cite the paper and acknowledge FiinGroup as the data source.
