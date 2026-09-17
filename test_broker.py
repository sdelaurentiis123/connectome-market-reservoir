import numpy as np
from backtest import run_long_flat
from broker import PaperBroker

def test_broker_round_trip_tracks_pnl():
    broker = PaperBroker(cash=1000, fee_bps=0, slippage_bps=0)
    broker.market_order(1, 100, "buy")
    broker.market_order(-1, 110, "sell")
    assert broker.portfolio.position == 0
    assert broker.portfolio.cash == 1010
    assert broker.portfolio.realized_pnl == 10

def test_backtest_reports_drawdown_and_turnover():
    result = run_long_flat(np.array([100., 110., 90.]), np.array([1, 1, 0]), fee_bps=0, slippage_bps=0)
    assert len(result.equity) == 3
    assert result.turnover == 190
    assert result.max_drawdown < 0
