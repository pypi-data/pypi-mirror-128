try:
    from store import euphoriaData, userData
except ImportError:
    from ..store import euphoriaData, userData


def get_basic_info():
    data = {}

    data["APY"] = f"{euphoriaData.staking_APY:,.2%}"
    data["TVL"] = f"${euphoriaData.staking_TVL:,.2f}"
    data["Current Index"] = f"{euphoriaData.currentIndex / 1000000000 :.2f}"

    return data


def get_user_data(addr):
    data = {}

    user_data = userData.get_user_balance(addr)

    data["Your Balance"] = f"{user_data['wagmi'] / 1e9 :.6f} WAGMI"
    data["Your Staked Balance"] = f"{user_data['swagmi'] / 1e9 :.8f} sWAGMI"
    data[
        "Next Reward Amount"
    ] = f"{((euphoriaData.staking_rebase / 100) * user_data['swagmi'] / 1e7) :.8f} sWAGMI"
    data["Next Reward Yield"] = f"{euphoriaData.staking_rebase:.4%}"
    data["ROI (5-Day Rate)"] = f"{euphoriaData.five_day_rate :.4%}"

    return data


def getData(addr):
    if addr:
        d1 = get_basic_info()
        d2 = get_user_data(addr)
        return {**d1, **d2}
    else:
        return get_basic_info()
