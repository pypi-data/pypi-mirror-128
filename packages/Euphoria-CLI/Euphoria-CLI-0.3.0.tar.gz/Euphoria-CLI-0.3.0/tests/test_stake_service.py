import unittest
import jsonschema
import json

from src.service.stake_service import get_basic_info, get_user_data
from utils.schema.stake import schema_basic_info, schema_user_data


class TestStakeService(unittest.TestCase):
    def test_basic_info(self):
        res = get_basic_info()
        self.assertIsNone(
            jsonschema.validate(json.dumps(res), schema=schema_basic_info)
        )

    def test_user_info(self):
        res = get_user_data("0x0000000000000000000000000000000000000000")
        self.assertIsNone(jsonschema.validate(json.dumps(res), schema=schema_user_data))
