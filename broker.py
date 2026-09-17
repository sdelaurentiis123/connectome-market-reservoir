from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Portfolio:
    cash: float = 10_000.0
    position: float = 0.0
    average_price: float = 0.0
    realized_pnl: float = 0.0

    def equity(self, mark: float) -> float:
        return self.cash + self.position * mark

class PaperBroker:
    """Minimal long/flat simulator with explicit fees and adverse slippage."""
    def __init__(self, cash: float = 10_000.0, fee_bps: float = 1.0, slippage_bps: float = 2.0):
        self.portfolio = Portfolio(cash=cash)
        self.fee_rate = fee_bps / 10_000
        self.slippage_rate = slippage_bps / 10_000
        self.trades: list[dict] = []

    def market_order(self, quantity: float, mid_price: float, timestamp: object) -> dict:
        if quantity == 0:
            raise ValueError("quantity must be non-zero")
        side = 1.0 if quantity > 0 else -1.0
        fill = mid_price * (1.0 + side * self.slippage_rate)
        notional = quantity * fill
        fee = abs(notional) * self.fee_rate
        if quantity > 0 and notional + fee > self.portfolio.cash:
            raise ValueError("insufficient paper cash")
        old_position = self.portfolio.position
        new_position = old_position + quantity
        if new_position < -1e-12:
            raise ValueError("starter broker is long/flat only")
        if quantity > 0:
            total_cost = old_position * self.portfolio.average_price + quantity * fill
            self.portfolio.average_price = total_cost / new_position
        else:
            sell_quantity = -quantity
            if sell_quantity > old_position + 1e-12:
                raise ValueError("cannot sell more than the paper position")
            self.portfolio.realized_pnl += sell_quantity * (fill - self.portfolio.average_price) - fee
            if abs(new_position) < 1e-12:
                self.portfolio.average_price = 0.0
        self.portfolio.cash -= notional + fee
        self.portfolio.position = new_position
        trade = {"timestamp": timestamp, "quantity": quantity, "fill_price": fill, "fee": fee,
                 "cash": self.portfolio.cash, "position": new_position,
                 "equity": self.portfolio.equity(mid_price)}
        self.trades.append(trade)
        return trade
