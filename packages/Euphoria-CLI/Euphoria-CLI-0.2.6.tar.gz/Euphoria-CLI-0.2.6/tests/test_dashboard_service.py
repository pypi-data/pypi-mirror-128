import unittest
import jsonschema
import json

from src.service.dashboard_service import getData
from utils.schema.dashboard import schema


class TestStakeService(unittest.TestCase):
    def test_data(self):
        res = getData()
        self.assertIsNone(jsonschema.validate(json.dumps(res), schema=schema))
