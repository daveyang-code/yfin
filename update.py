from datetime import date, timedelta
import networkx as nx
import pandas as pd
import pickle
import yfinance as yf
import time
import progressbar
from statsmodels.tsa.stattools import adfuller


def set_node_adf(G):
    for n in G.nodes:
        try:
            data = yf.download(n, date.today()- timedelta(days=365), date.today())["Adj Close"]
            adf = adfuller(data)
            if adf[1] > 0.05:
                nx.set_node_attributes(G, {n:{"stationary":False}})
            elif adf[0] < adf[4]['1%'] and adf[0] < adf[4]['5%'] and adf[0] < adf[4]['10%']:
                nx.set_node_attributes(G, {n:{"stationary":True}})
            else:
                nx.set_node_attributes(G, {n:{"stationary":False}})
        except:
            pass
    return G


def set_edge_correlation(G):
    for edge in G.edges:
        try:
            tickers = [edge[0], edge[1]]
            data = pd.DataFrame(columns=tickers)
            for ticker in tickers:
                data[ticker] = yf.download(
                    ticker, date.today() - timedelta(30), date.today()
                )["Adj Close"]
            correlation = data.corr(method="pearson")
            nx.set_edge_attributes(
                G,
                {
                    edge: {
                        "correlation": correlation.iloc[1.0],
                    }
                },
            )
        except:
            pass
    return G


def set_edge_value(G):
    for e in G.edges:
        try:
            nx.set_edge_attributes(G, {e: {"value": abs(G.edge[e]["correlation"])}})
        except:
            pass
    return G


def set_edge_title(G):
    for e in G.edges:
        try:
            nx.set_edge_attributes(
                G,
                {
                    e: {
                        "title": "Correlation: " + str(G.edge[e]["correlation"]),
                    }
                },
            )
        except:
            pass
    return G


def set_edges(G):
    G = set_edge_correlation(G)
    G = set_edge_value(G)
    G = set_edge_title(G)
    return G


def init_attributes(G):
    bar = progressbar.ProgressBar(len(G.nodes))
    for i, g in enumerate(G.nodes):
        bar.update(i)
        data = yf.Ticker(g).info
        try:
            name = data["longName"]
        except:
            name = "N/A"
        try:
            industry = data["industry"]
        except:
            industry = "N/A"
        try:
            sector = data["sector"]
        except:
            sector = "N/A"
        nx.set_node_attributes(
            G, {g: {"name": name, "industry": industry, "sector": sector}}
        )
    return G


def remove_attribute(G, attr):
    for n in G.nodes:
        G.nodes[n].pop(attr)
    return G


def update_fundamentals(G):
    metrics = [
        "previousClose",
        "open",
        "dayLow",
        "dayHigh",
        "trailingPE",
        "volume",
        "averageVolume10days",
        "marketCap",
        "fiftyTwoWeekLow",
        "fiftyTwoWeekHigh",
        "currentPrice",
        "trailingPegRatio",
        "trailingAnnualDividendRate",
        "trailingAnnualDividendYield",
        "dividendRate",
        "dividendYield",
        "payoutRatio",
        "beta",
        "profitMargins",
        "shortRatio",
        "shortPercentOfFloat",
        "bookValue",
        "priceToBook",
        "trailingEps",
        "pegRatio",
        "quickRatio",
        "currentRatio",
        "debtToEquity",
        "revenuePerShare",
        "returnOnAssets",
        "returnOnEquity",
        "freeCashflow",
        "operatingCashflow",
        "earningsGrowth",
        "revenueGrowth",
        "grossMargins",
        "ebitdaMargins",
        "operatingMargins",
    ]
    bar = progressbar.ProgressBar(len(G.nodes))
    for i, n in enumerate(G.nodes):
        bar.update(i)
        data = yf.Ticker(n).info
        for m in metrics:
            try:
                nx.set_node_attributes(G, {n: {m: data[m]}})
            except:
                pass
    return G


def update_change(G):
    for i, n in enumerate(G.nodes):
        try:
            change = (
                (G.nodes[n]["currentPrice"] - G.nodes[n]["previousClose"])
                / G.nodes[n]["previousClose"]
                * 100
            )
            nx.set_node_attributes(G, {n: {"change": change}})
        except:
            pass
    return G


def update_title(G):
    for n in G.nodes:
        nx.set_node_attributes(
            G, {n: {"title": n + "\n" + "%.2f" % (G.nodes[n]["change"]) + "%"}}
        )
    return G


def update_value(G):
    for n in G.nodes:
        nx.set_node_attributes(G, {n: {"value": abs(G.nodes[n]["change"])}})
    return G


def set_nodes(G):
    G = update_fundamentals(G)
    G = update_change(G)
    G = update_title(G)
    G = update_value(G)
    G = set_node_adf(G)
    return G


def compose_graph(G, H):
    return nx.compose(G, H)


def print_network(G):
    print(G.nodes(data=True))
    print(G.edges(data=True))


def main():

    with open("network.gpickle", "rb") as f:
        G = pickle.load(f)

    G = set_nodes(G)
    G = set_edges(G)

    with open("network.gpickle", "wb") as f:
        pickle.dump(G, f, pickle.HIGHEST_PROTOCOL)


if __name__ == "__main__":
    main()
