import unittest
import web3
import src.store.euphoriaData as ed


class TestEuphoriaData(unittest.TestCase):
    def test_contracts(self):
        self.assertIsInstance(ed.staking_contract, web3.contract.Contract)
        self.assertIsInstance(ed.WAGMI_contract, web3.contract.Contract)
        self.assertIsInstance(ed.sWAGMI_contract, web3.contract.Contract)

    def test_supply(self):
        self.assertIs(type(ed.total_supply), float)
        self.assertIs(type(ed.circulating_supply), float)

    def test_misc(self):
        self.assertIs(type(ed.epoch), list)
        self.assertIs(type(ed.staking_rebase), float)
