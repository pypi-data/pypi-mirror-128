import unittest
import dg_sdk
from tests.conftest import *


class TestMerchant(unittest.TestCase):

    def setUp(self):
        dg_sdk.DGClient.mer_config = dg_sdk.MerConfig(private_key, public_key, sys_id, product_id, huifu_id)

        print("setup")

    def tearDown(self):
        print("tearDown")

    def test_query_merch_info(self):
        result = dg_sdk.Merchant.query_merch_info()
        assert result["sub_resp_code"] == "00000000"

    def test_query_split_config(self):
        result = dg_sdk.Merchant.query_split_config()
        assert result["sub_resp_code"] == "00000000"

    def test_modify(self):
        result = dg_sdk.Merchant.modify(upper_huifu_id=upper_huifu_id, settle_agree_pic="./test1.zip")

        assert result["sub_resp_code"] == "00000000"
