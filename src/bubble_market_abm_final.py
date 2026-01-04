import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# =========================
# Investor Agent
# =========================
class Investor:
    def __init__(self, agent_id, agent_type, sentiment=0.5):
        self.id = agent_id
        self.type = agent_type  # "rational" or "behavioral"
        self.sentiment = sentiment

    def decide(self, price, fundamental):
        if self.type == "rational":
            if price < 0.98 * fundamental:
                return "buy"
            elif price > 1.02 * fundamental:
                return "sell"
            else:
                return "hold"
        else:
            if self.sentiment >= 0.6:
                return "buy"
            elif self.sentiment <= 0.4:
                return "sell"
            else:
                return "hold"

    def update_sentiment(self, price_change):
        if self.type == "behavioral":
            if price_change > 0:
                self.sentiment = min(1, self.sentiment + 0.1)
            elif price_change < 0:
                self.sentiment = max(0, self.sentiment - 0.1)


# =========================
# Market Environment
# =========================
class Market:
    def __init__(self, agents, initial_price, fundamental, sensitivity):
        self.agents = agents
        self.price = initial_price
        self.fundamental = fundamental
        self.sensitivity = sensitivity

        self.price_history = [initial_price]
        self.buy_pressure = []
        self.sell_pressure = []

    def step(self):
        buys, sells = 0, 0

        for agent in self.agents:
            action = agent.decide(self.price, self.fundamental)
            if action == "buy":
                buys += 1
            elif action == "sell":
                sells += 1

        net_pressure = (buys - sells) / len(self.agents)

        old_price = self.price
        self.price *= (1 + self.sensitivity * net_pressure)
        price_change = self.price - old_price

        for agent in self.agents:
            agent.update_sentiment(price_change)

        self.price_history.append(self.price)
        self.buy_pressure.append(buys)
        self.sell_pressure.append(sells)

    def run(self, T):
        for _ in range(T):
            self.step()

    def visualize(self, title_suffix=""):
        # Visualization 1: Price path
        plt.figure(figsize=(8, 5))
        plt.plot(self.price_history, label="Market Price")
        plt.axhline(self.fundamental, linestyle="--", color="red",
                    label="Fundamental Value")
        plt.title(f"Bubble and Crash Simulation {title_suffix}")
        plt.xlabel("Time")
        plt.ylabel("Price")
        plt.legend()
        plt.show()

        # Visualization 2: Buy/Sell pressure
        plt.figure(figsize=(8, 4))
        plt.plot(self.buy_pressure, label="Buy Pressure")
        plt.plot(self.sell_pressure, label="Sell Pressure")
        plt.legend()
        plt.title("Market Pressure Over Time")
        plt.show()


# =========================
# Project 3 Data Loader
# =========================
def load_data():
    funding = pd.read_csv("funding_rounds.csv")
    acquisitions = pd.read_csv("acquisitions.csv")

    for _, row in acquisitions.iterrows():
        target_id = row["acquired_object_id"]

        vals = funding[funding["object_id"] == target_id] \
            .sort_values("funded_at")["post_money_valuation_usd"] \
            .replace(0, np.nan) \
            .dropna()

        if len(vals) >= 3:
            price_series = vals.values
            fundamental = row["price_amount"]
            return price_series, fundamental

    raise ValueError("No startup with usable valuation history found.")




# =========================
# Market Factory
# =========================
def create_market(n_agents, frac_behavioral, sensitivity,
                  initial_price, fundamental):

    agents = []
    for i in range(n_agents):
        if random.random() < frac_behavioral:
            agents.append(Investor(i, "behavioral"))
        else:
            agents.append(Investor(i, "rational"))

    return Market(
        agents=agents,
        initial_price=initial_price,
        fundamental=fundamental,
        sensitivity=sensitivity
    )
