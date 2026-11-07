# Data

One-minute index records for the **VNINDEX** and the **VN30** of the Ho Chi Minh Stock Exchange (HOSE),
provided by **FiinGroup** and shared here free of charge for research and replication.

| File | Index | Records | Period |
|---|---|---|---|
| `VNINDEX_1min.csv.gz` | VNINDEX | 255,838 | 15 Feb 2022 - 25 Sep 2026 (continuous coverage from 9 Jun 2022) |
| `VN30_1min.csv.gz` | VN30 | 248,991 | 9 Jun 2022 - 25 Sep 2026 |

One row per one-minute record, as delivered by the data provider. Columns:

| Column | Description |
|---|---|
| `RecordId` | Record identifier |
| `ComGroupCode` | Index code |
| `TradingDate` | Timestamp of the minute (local time, Asia/Ho_Chi_Minh) |
| `ReferenceIndex` | Reference index level (previous close) |
| `OpenIndex`, `HighestIndex`, `LowestIndex`, `CloseIndex` | Index levels within the minute |
| `IndexChange`, `PercentIndexChange` | Change relative to the reference level |
| `TotalMatchVolume`, `TotalMatchValue` | Cumulative order-matched volume and value |
| `TotalDealVolume`, `TotalDealValue` | Cumulative negotiated (put-through) volume and value |
| `TotalVolume`, `TotalValue` | Cumulative total volume and value |

Notes on the raw records:

* The files contain records outside continuous trading (before 9:15, during the closing call auction 14:30-14:45 and after 14:45).
  The analysis samples the continuous sessions 9:15-11:30 and 13:00-14:30 on a regular one-minute grid and takes the official
  close as the last record at or before 14:45. Daily trading value is the cumulative `TotalMatchValue` at the close.
* The recording format changes on 5 May 2025, when HOSE migrated to a new trading system: from that date each day has exactly
  227 records on a fixed grid, whereas earlier records are irregular.
* Records for April and May 2022 are missing for the VNINDEX.

If you use the data, please cite the paper and acknowledge FiinGroup as the data source.
Cached pickles produced by `run_all.sh` are written to this folder; tables and figures go to `results/`.
