# Connectome Market Reservoir

Research scaffold for testing a fixed *Drosophila* connectome subgraph as a recurrent reservoir for market regime and volatility prediction.

This is a research project, **not a trading system or financial advice**. The honest question is whether evolved graph topology offers useful memory or nonlinear separation relative to matched random reservoirs. It is not "a fly brain that trades."

## Targets

Prefer targets with a defensible signal-to-noise ratio:

- future realized-volatility bucket
- volatility-spike probability
- market/regime classification
- liquidity or spread stress

Raw next-tick price direction is not the primary target.

## Method

1. Query a tractable MaleCNS subgraph from `male-cns:v1.0`.
2. Feed standardized returns, realized volatility, volume, spread, and order-book imbalance into fixed input nodes.
3. Propagate state using explicit leaky nonlinear dynamics.
4. Train only a regularized linear/logistic readout.
5. Compare against degree-preserving rewires, Erdős-Rényi graphs, matched echo-state networks, logistic regression, gradient boosting, and a small recurrent baseline.

## Guardrails

- strict chronological walk-forward evaluation
- purge/embargo samples whose labels overlap the training window
- fit scalers and hyperparameters on training data only
- freeze graph, edge-sign assumptions, and hyperparameters before final test
- include fees, spread, slippage, latency, turnover, and capacity in any strategy simulation
- report calibration, AUROC/AUPRC, drawdown, turnover, and stability across regimes
- never infer an edge from one favorable backtest

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
python -m connectome_market.demo
```

Set `NEUPRINT_TOKEN` only when querying neuPrint. Market data is not bundled; loaders require an explicit local file or adapter.

## Status

Cold-start scaffold. The included demo is synthetic and runnable. It proves plumbing only, not market efficacy.

## Data credit

Male CNS data: FlyEM at HHMI Janelia, Cambridge Connectomics Group, Google Research, and collaborators. See https://male-cns.janelia.org/ and follow dataset citation/license terms.

## License

MIT for repository code. External datasets retain their own terms.

## Backtesting and paper execution

Backtesting is core, not a demo afterthought. The intended harness must support:

- event-driven, timestamp-ordered simulation without look-ahead
- walk-forward retraining and purged/embargoed validation
- configurable spread, fees, slippage, latency, partial fills, and position limits
- position, cash, equity, realized/unrealized PnL, turnover, drawdown, and exposure logs
- graph/null-model sweeps with frozen final-test configuration
- reproducible run manifests and seeds

`PaperBroker` provides a runnable long/flat simulated execution loop. An Alpaca paper adapter is a documented future path; no live-money adapter belongs here until the model has repeated out-of-sample evidence and a separately reviewed risk layer.

### Prediction markets

The same reservoir can ingest Polymarket or Kalshi contract series: implied probability, bid/ask spread, depth, volume, time-to-expiry, and correlated-contract features. Targets can be probability calibration, regime shifts, or bounded paper-trading policies on binary event contracts. Historical snapshots must be timestamp-aligned and evaluated without using resolution information before it became public.

## Non-negotiable design constraints

1. **Independent N means whole market experiments.** Replication and final validation use held-out market periods, instruments, or event cohorts, not overlapping windows from one trajectory. Purge and embargo all label overlap.
2. **No pseudo-replication.** Re-running deterministic code does not create seeds. State the independent unit and vary genuinely stochastic graph draws, initializations, instruments/events, and market periods.
3. **Keep physical/economic variables physical.** Features use causal timestamps and strategies transact at executable bid/ask prices with fees, slippage, latency, and position limits. Midprice hindsight is not a fill.
4. **Prove state sufficiency before architecture search.** Show that the causal feature history contains predictive information for the target before tuning reservoir topology.
5. **Null models are the experiment.** Persistence, linear/logistic models, matched echo-state networks, degree-preserving rewires, and matched random graphs receive the same tuning budget, costs, and evaluation.
6. **Fail closed numerically.** NaNs, infinities, singular fits, and undefined metrics invalidate the run. Never zero-fill or clip them and keep a headline metric.
7. **Tests test the math.** Tests check causality, split isolation, reservoir updates, fills, accounting, invariants, and failure modes, not only file existence or schema shape.
8. **One canonical definition per result.** Each target, split, fill, PnL field, and headline metric has one implementation and one recorded provenance.
9. **Launchers are immutable and non-destructive.** Runs write versioned outputs and fail safely. No broad or unconditional `rm -f`; raw data and prior results stay immutable.
10. **A clean clone must reproduce the run.** `requirements-lock.txt` records the exact tested environment. Dependency changes require a new lock and clean-environment test.
11. **Code stays proportional to evidence.** Add infrastructure only when an experiment needs it; do not bury an untested idea under production-shaped code.
12. **Claims track evidence.** Until repeated held-out evidence exists, call this a scaffold or a paper-trading experiment, not an advantage, alpha, or validated biological mechanism.
