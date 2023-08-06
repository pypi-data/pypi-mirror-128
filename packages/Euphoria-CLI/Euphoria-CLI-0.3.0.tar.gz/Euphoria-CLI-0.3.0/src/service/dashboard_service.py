try:
    from store import euphoriaData
except ImportError:
    from ..store import euphoriaData


def getData():
    data = {}

    data["WAGMI Price"] = f"${euphoriaData.wagmi_price:,.2f}"
    data["Market Cap"] = f"${euphoriaData.market_cap:,.4f}"
    data["TVL"] = f"${euphoriaData.staking_TVL:,.2f}"
    data["APY"] = f"{euphoriaData.staking_APY:,.2%}"
    data["Current Index"] = f"{euphoriaData.currentIndex / 1000000000 :.2f}"
    data["Treasury balance"] = 0  # to be calculated
    data["Backing per $WAGMI"] = 0  # to be calculated
    data["Runway"] = 0  # to be calculated

    return data
