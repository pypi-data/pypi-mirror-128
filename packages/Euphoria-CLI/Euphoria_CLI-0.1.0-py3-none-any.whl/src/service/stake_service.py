try:
    from store import euphoriaData, userData
except ImportError:
    from ..store import euphoriaData, userData


def get_basic_info():
    data = {}

    data["APY"] = euphoriaData.staking_APY
    data["TVL"] = euphoriaData.staking_TVL
    data["Current Index"] = euphoriaData.currentIndex

    return data


def get_user_data(addr):
    data = {}

    user_data = userData.get_user_balance(addr)

    data["Your Balance"] = user_data["wagmi"]
    data["Your Staked Balance"] = user_data["swagmi"]
    data["Next Reward Amount"] = (euphoriaData.staking_rebase / 100) * user_data[
        "swagmi"
    ]
    data["Next Reward Yield"] = euphoriaData.staking_rebase
    data["ROI (5-Day Rate)"] = euphoriaData.five_day_rate

    return data


def getData(addr):
    if addr:
        d1 = get_basic_info()
        d2 = get_user_data(addr)
        return {**d1, **d2}
    else:
        return get_basic_info()
