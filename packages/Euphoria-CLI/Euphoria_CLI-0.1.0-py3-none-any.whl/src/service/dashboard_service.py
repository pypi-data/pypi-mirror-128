try:
    from store import euphoriaData
except ImportError:
    from ..store import euphoriaData


def getData():
    data = {}

    data["WAGMI Price"] = euphoriaData.wagmi_price
    data["Market Cap"] = euphoriaData.market_cap
    data["TVL"] = euphoriaData.staking_TVL
    data["APY"] = euphoriaData.staking_APY
    data["Current Index"] = euphoriaData.currentIndex
    data["Treasury balance"] = ""
    data["Backing per $WAGMI"] = ""
    data["Runway"] = ""

    return data
