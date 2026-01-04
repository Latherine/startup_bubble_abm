# Startup Bubble — Agent-Based Model (ABM)

A compact agent-based model that simulates formation, growth, and collapse dynamics in startup investment markets.  
This README reflects the actual scripts and files currently in the repository and gives exact usage, dependencies, data requirements, and example outputs.

Repository: https://github.com/Latherine/startup_bubble_abm

---

## Contents (actual project files)

- `.gitignore`
- `data/` (present, empty — place input CSVs or outputs here)
- `docs/` (empty; add docs here)
- `src/`
  - `bubble_market_abm_final.py` — main ABM implementation (Investor, Market, data loader, and market factory).
  - `calibrated_and_run_final` — executable script that loads project data, calibrates model sensitivity over a grid, runs a calibrated simulation, and runs a scenario with higher behavioral investor share.

---

## Quick setup

1. Clone repository
   ```bash
   git clone https://github.com/Latherine/startup_bubble_abm.git
   cd startup_bubble_abm
   ```

2. Create & activate virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate    # macOS / Linux
   .venv\Scripts\activate       # Windows (PowerShell)
   ```

3. Install required packages
   ```bash
   pip install numpy pandas matplotlib
   ```

   (The code imports: numpy, pandas, matplotlib, random. No other third‑party packages are required.)

---

## Data required

The runner script expects two CSV files present when it runs (place them in the repository root or `data/` and run the script from the same working directory):

1. funding_rounds.csv  
   Required columns used by the loader:
   - `object_id` (startup identifier)
   - `funded_at` (date of funding; used to sort valuations)
   - `post_money_valuation_usd` (valuation in USD; zeros are replaced with NaN and dropped)

2. acquisitions.csv  
   Required columns used by the loader:
   - `acquired_object_id` (matched against `object_id` in funding file)
   - `price_amount` (used as the "fundamental" value in the model)

Behavior of the loader:
- The loader (`load_data()` in `bubble_market_abm_final.py`) scans acquisitions, finds a target with at least 3 non‑zero historical valuations in `funding_rounds.csv`, returns (price_series, fundamental).
- If no suitable company is found the loader raises `ValueError("No startup with usable valuation history found.")`.

---

## How to run (exact commands)

Main entrypoint (script with __main__): `src/calibrated_and_run_final` — run with Python:

```bash
python src/calibrated_and_run_final
```

Notes:
- The file `src/calibrated_and_run_final` imports `create_market` and `load_data` from `src/bubble_market_abm_final.py`.
- There are no command-line arguments implemented in these scripts. The script reads the CSV files directly via `load_data()` and uses internal parameter values (see "Default parameters" below).
- Running `python src/bubble_market_abm_final.py` will only define classes/functions; no __main__ entrypoint is provided in that file.

---

## Default parameters used by the runner

In `src/calibrated_and_run_final`:

- Calibration:
  - sensitivity_grid = np.linspace(0.01, 0.2, 20)
  - n_agents = 100 (default used by create_market in calibration)
  - frac_behavioral = 0.6
  - Calibration objective: match the peak price of the historical `price_series` by minimizing absolute difference between simulated peak and target peak.

- After calibration:
  - Calibrated run: n_agents=100, frac_behavioral=0.6, sensitivity=best_sensitivity
  - Scenario run: n_agents=100, frac_behavioral=0.8 (higher behavioral share), sensitivity=best_sensitivity

In `src/bubble_market_abm_final.py`:
- Investor types: "rational" and "behavioral".
- Decision rules:
  - Rational: buy if price < 0.98 * fundamental; sell if price > 1.02 * fundamental; else hold.
  - Behavioral: buy if sentiment >= 0.6, sell if sentiment <= 0.4, else hold.
- Sentiment update for behavioral agents: +/- 0.1 per positive/negative price change (bounded [0,1]).
- Market price update: price *= (1 + sensitivity * net_pressure), where net_pressure = (buys - sells)/n_agents.

---

## Expected outputs (what the script prints and shows)

When you run `python src/calibrated_and_run_final` (with valid CSV inputs), typical script behavior:

- Console print of calibrated sensitivity, for example:
  ```
  Calibrated sensitivity: 0.05368421052631579
  ```
  (this value is illustrative — actual number depends on the data and calibration run)

- Visualizations displayed via matplotlib (`plt.show()`), produced twice per run:
  1. Price path plot:
     - X axis: time step index (0..T)
     - Y axis: market price
     - A dashed horizontal red line shows the fundamental value passed from data
     - Title example: "Bubble and Crash Simulation (Calibrated Run)"
  2. Buy/Sell pressure plot:
     - Plots of buy pressure and sell pressure across time
     - Title: "Market Pressure Over Time"

The script will produce these two plots for the calibrated run and again for the scenario run (so 4 plots total, shown sequentially).

---

## Running on a headless server (no display)

The scripts call `plt.show()`. To save plots instead of showing them, edit `bubble_market_abm_final.py` in the `visualize` method:

Replace:
```python
plt.show()
```
with:
```python
plt.savefig(f"results/price_path{title_suffix}.png", dpi=150)
plt.close()
```
and likewise for the buy/sell pressure figure (use a different filename). Create a `results/` directory first.

---

## Example minimal reproducible workflow

1. Put `funding_rounds.csv` and `acquisitions.csv` in the repository root (or run script from the folder containing them).
2. Install dependencies: `pip install numpy pandas matplotlib`
3. Run:
   ```bash
   python src/calibrated_and_run_final
   ```
4. Expect a printed "Calibrated sensitivity: <value>" and 4 plotted figures (2 for calibrated run, 2 for the high-sentiment scenario).

---

## Development notes & suggestions

- The repository currently lacks CLI parsing — consider adding argparse flags (input paths, grid ranges, n_agents, frac_behavioral, output directory) to `calibrated_and_run_final`.
- Consider adding file-saving behavior for reproducible runs and CI-friendly outputs.
- Add `requirements.txt` and a `LICENSE` file if you want to publish.

- Inspect the exact contents of `src/bubble_market_abm_final.py` and `src/calibrated_and_run_final` and update this README to include exact command-line arguments, required packages, and sample outputs; or

If you want, I can:
- Update the `visualize` method to save figures to `results/` and commit the change.
- Add a thin CLI wrapper around `calibrated_and_run_final` with flags for input file paths and output directory, and commit `requirements.txt`.

---

## Contact

Maintainer: Latherine  
Repo: https://github.com/Latherine/startup_bubble_abm

```
