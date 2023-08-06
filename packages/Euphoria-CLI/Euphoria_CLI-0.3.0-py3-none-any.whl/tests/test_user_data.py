import unittest
import json
import jsonschema
from src.store.userData import get_user_balance


class TestUserData(unittest.TestCase):
    def test_get_user_balance_active_address(self):
        res = get_user_balance("0x18bdAD1211eed7808Dbca6Beb6a387F5F9c77Efd")
        schema = {
            "wagmi": "number",
            "swagmi": "number",
        }
        self.assertIsNone(jsonschema.validate(json.dumps(res), schema=schema))

    def test_get_user_balance_inactive_address(self):
        res = get_user_balance("0x0000000000000000000000000000000000000000")
        schema = {
            "wagmi": 0,
            "swagmi": 0,
        }
        self.assertEqual(res, schema)

    @unittest.expectedFailure
    def test_get_user_balance_no_address(self):
        res = get_user_balance("")
