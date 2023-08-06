import web3

provider = web3.HTTPProvider("https://api.s0.t.hmny.io")
w3 = web3.Web3(provider)


def buildContract(addr, abi):
    return w3.eth.contract(address=addr, abi=abi)
