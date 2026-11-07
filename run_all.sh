#!/usr/bin/env bash
# Reproduces all tables and figures in the paper. Run from the repository root.
# Uses data/VNINDEX_1min.csv.gz and data/VN30_1min.csv.gz (included).
set -e
mkdir -p results
python3 ana/load.py        # read the one-minute files and cache them as pickles
python3 ana/buildB.py      # regular 1-minute grid of the continuous sessions
python3 ana/t2_data.py     # daily return components and abnormal trading value
python3 ana/t2_tables.py   # all regressions; writes results/results.json
python3 ana/t2_figs.py     # Figures 1 and 2 (results/Figure1.tif, Figure2.tif)
