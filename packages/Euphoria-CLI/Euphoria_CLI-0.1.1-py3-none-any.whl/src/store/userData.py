try:
    from abi import WAGMI, sWAGMI
    from helpers.web3Helper import buildContract
    from helpers.spinner_helper import spinner
except ImportError:
    from ..abi import WAGMI, sWAGMI
    from ..helpers.web3Helper import buildContract
    from ..helpers.spinner_helper import spinner

WAGMI_contract = buildContract(WAGMI.address, WAGMI.ABI)
sWAGMI_contract = buildContract(sWAGMI.address, sWAGMI.ABI)


@spinner
def get_user_balance(addr):
    wagmi_bal = WAGMI_contract.functions.balanceOf(addr).call()
    swagmi_bal = sWAGMI_contract.functions.balanceOf(addr).call()

    return {"wagmi": wagmi_bal, "swagmi": swagmi_bal}
