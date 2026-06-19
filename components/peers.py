import streamlit as st
import pandas as pd
from data.stock_data import load_peer_history
from utils.indicators import get_return
from utils.peers import get_peer_list


def build_peer_dataframe(ticker, one_month_return):
    peers = get_peer_list(ticker)
    rows = [{
        "Ticker": ticker,
        "1M Return (%)": round(one_month_return, 2) if one_month_return is not None else None,
        "Type": "Selected Stock",
    }]

    for peer in peers:
        peer_history = load_peer_history(peer)
        if not peer_history.empty:
            peer_return = get_return(peer_history, 22)
            rows.append({
                "Ticker": peer,
                "1M Return (%)": round(peer_return, 2) if peer_return is not None else None,
                "Type": "Peer / Benchmark",
            })

    return pd.DataFrame(rows)


def get_peer_difference(peer_df, ticker, one_month_return):
    if len(peer_df) <= 1 or one_month_return is None:
        return None

    peer_avg = peer_df[peer_df["Ticker"] != ticker]["1M Return (%)"].mean()
    return one_month_return - peer_avg
