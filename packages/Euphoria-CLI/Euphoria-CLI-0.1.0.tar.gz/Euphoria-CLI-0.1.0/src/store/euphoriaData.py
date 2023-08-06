import math

try:
    from abi import staking, WAGMI, sWAGMI
    from helpers.token_price import loadTokenPrices
    from helpers.web3Helper import buildContract
    from helpers.spinner_helper import spinner
except ImportError:
    from ..abi import staking, WAGMI, sWAGMI
    from ..helpers.token_price import loadTokenPrices
    from ..helpers.web3Helper import buildContract
    from ..helpers.spinner_helper import spinner

with spinner:
    wagmi_price = loadTokenPrices(
        "WAGMI"
    )  # TODO: find a way to calculate wagmi price than fetch
    one_price = loadTokenPrices("ONE")

    staking_contract = buildContract(staking.address, staking.ABI)
    WAGMI_contract = buildContract(WAGMI.address, WAGMI.ABI)
    sWAGMI_contract = buildContract(sWAGMI.address, sWAGMI.ABI)

    # market_price =

    total_supply = WAGMI_contract.functions.totalSupply().call() / math.pow(10, 9)
    circulating_supply = (
        sWAGMI_contract.functions.circulatingSupply().call() / math.pow(10, 9)
    )

    staking_TVL = circulating_supply * wagmi_price
    market_cap = total_supply * wagmi_price

    # TODO: import all bonds

    epoch = staking_contract.functions.epoch().call()
    staking_reward = epoch[1]
    circ = sWAGMI_contract.functions.circulatingSupply().call()
    staking_rebase = staking_reward / circ
    five_day_rate = math.pow(1 + staking_rebase, 5 * 3) - 1
    staking_APY = math.pow(1 + staking_rebase, 365 * 3) - 1

    currentIndex = staking_contract.functions.index().call()
    next_rebase = epoch[3]

    # TODO: calculate runway after calculating bonds and treasury balance
