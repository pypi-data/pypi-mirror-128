from dg_sdk.module.request_tools import request_post
from dg_sdk.module.merchant.merchant_api_urls import *
from dg_sdk.dg_client import DGClient
from dg_sdk.module.merchant.merchant_info import MerchantInfo
from dg_sdk.module.merchant.legal_info import LegalInfo
from dg_sdk.module.merchant.bussiness_lic_info import BussinessLicInfo
from dg_sdk.module.merchant.settle_config_info import SettleConfigInfo
from dg_sdk.module.merchant.cash_config_info import CashConfigInfo
from dg_sdk.module.merchant.mer_card_info import MerCardInfo
from dg_sdk.module.merchant.corp_info import CorpInfo
from typing import List
import os


class Merchant(object):
    """
    商户进件相关类，包含以下接口
    企业类型商户进件
    个体户类型商户进件
    基本信息修改
    详细信息查询
    新增总部
    修改总部
    总部商户绑定&解除
    查询账户信息
    商户业务开通
    商户业务开通修改
    申请单状态查询
    商户图片资料上传
    商户分账配置
    商户分账配置查询
    商户分期配置
    商户分期配置详情查询
    活动报名，支持微信
    """

    @classmethod
    def create_enterprise(cls, upper_huifu_id,
                          merchant_info: MerchantInfo,
                          card_info: MerCardInfo,
                          lic_info: BussinessLicInfo,
                          legal_info: LegalInfo,
                          settle_info: SettleConfigInfo = None,
                          cash_config: List[CashConfigInfo] = None,
                          settle_agree_pic="",
                          **kwargs):
        """
        企业类型商户进件
        :param upper_huifu_id: 渠道商汇付Id
        :param merchant_info: 商户经营信息
        :param lic_info: 营业执照信息
        :param legal_info: 法人信息
        :param card_info: 卡信息
        :param settle_info: 结算配置
        :param cash_config:取现配置列表
        :param settle_agree_pic: D1结算协议图片文件路径
        :param kwargs: 额外参数
        :return:
        """

        required_params = {
            "upper_huifu_id": upper_huifu_id,
            "product_id": DGClient.mer_config.product_id
        }
        if merchant_info:
            required_params.update(merchant_info.obj_to_dict())
        if lic_info:
            required_params.update(lic_info.obj_to_dict())
        if legal_info:
            required_params.update(legal_info.obj_to_dict())
        if card_info:
            required_params["card_info"] = card_info.obj_to_dict()
        if settle_info:
            required_params["settle_config"] = settle_info.obj_to_dict()
        if cash_config:
            configs = []
            for config in cash_config:
                configs.append(config.obj_to_dict())
            required_params["cash_config"] = configs

        file = None
        if not settle_agree_pic:
            settle_agree_pic = kwargs.get('settle_agree_pic')
            if settle_agree_pic:
                kwargs.pop('settle_agree_pic')

        if settle_agree_pic:
            file = {'settle_agree_pic': (
                os.path.basename(settle_agree_pic), open(settle_agree_pic, 'rb'), 'application/octet-stream')}

        required_params.update(kwargs)
        return request_post(ent_mer_reg, required_params, file)

    @classmethod
    def create_individual(cls, upper_huifu_id,
                          merchant_info: MerchantInfo,
                          card_info: MerCardInfo,
                          settle_info: SettleConfigInfo = None,
                          cash_config: List[CashConfigInfo] = None,
                          settle_agree_pic="",
                          short_name="",
                          **kwargs):
        """
        个人类型商户进件
        :param upper_huifu_id: 渠道商汇付Id
        :param merchant_info: 商户经营信息
        :param card_info: 卡信息
        :param settle_info: 结算配置
        :param cash_config:取现配置列表
        :param settle_agree_pic: D1结算协议图片文件路径
        :param short_name: 商户简称
        :param kwargs: 额外参数
        :return:
        """

        required_params = {
            "upper_huifu_id": upper_huifu_id,
            "product_id": DGClient.mer_config.product_id,
            "short_name": short_name,
        }
        if merchant_info:
            required_params.update(merchant_info.obj_to_dict())
        if card_info:
            required_params["card_info"] = card_info.obj_to_dict()
        if settle_info:
            required_params["settle_config"] = settle_info.obj_to_dict()
        if cash_config:
            configs = []
            for config in cash_config:
                configs.append(config.obj_to_dict())
            required_params["cash_config"] = configs

        file = None
        if not settle_agree_pic:
            settle_agree_pic = kwargs.get('settle_agree_pic')
            if settle_agree_pic:
                kwargs.pop('settle_agree_pic')

        if settle_agree_pic:
            file = {'settle_agree_pic': (
                os.path.basename(settle_agree_pic), open(settle_agree_pic, 'rb'), 'application/octet-stream')}

        required_params.update(kwargs)
        return request_post(ent_mer_reg, required_params, file)

    @classmethod
    def modify(cls, upper_huifu_id,
               merchant_info: MerchantInfo = None,
               lic_info: BussinessLicInfo = None,
               legal_info: LegalInfo = None,
               card_info: MerCardInfo = None,
               settle_info: SettleConfigInfo = None,
               cash_config: List[CashConfigInfo] = None,
               settle_agree_pic="",
               **kwargs):
        """
        修改商户基本信息
        :param upper_huifu_id: 渠道商汇付Id
        :param merchant_info: 商户经营信息
        :param lic_info: 营业执照信息
        :param legal_info: 法人信息
        :param card_info: 卡信息
        :param settle_info: 结算配置
        :param cash_config:取现配置列表
        :param settle_agree_pic: D1结算协议图片文件路径
        :param kwargs: 额外参数
        :return:
        """

        required_params = {
            "upper_huifu_id": upper_huifu_id,
            "product_id": DGClient.mer_config.product_id
        }
        if merchant_info:
            required_params.update(merchant_info.obj_to_dict())
        if lic_info:
            required_params.update(lic_info.obj_to_dict())
        if legal_info:
            required_params.update(legal_info.obj_to_dict())
        if card_info:
            required_params["card_info"] = card_info.obj_to_dict()
        if settle_info:
            required_params["settle_config"] = settle_info.obj_to_dict()
        if cash_config:
            configs = []
            for config in cash_config:
                configs.append(config.obj_to_dict())
            required_params["cash_config"] = configs

        file = None
        if not settle_agree_pic:
            settle_agree_pic = kwargs.get('settle_agree_pic')
            if settle_agree_pic:
                kwargs.pop('settle_agree_pic')

        if settle_agree_pic:
            file = {'settle_agree_pic': (
                os.path.basename(settle_agree_pic), open(settle_agree_pic, 'rb'), 'application/octet-stream')}

        required_params.update(kwargs)
        return request_post(mer_modify, required_params, files=file)

    @classmethod
    def query_merch_info(cls, **kwargs):
        """
        查询商户详细信息
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id
        }
        required_params.update(kwargs)
        return request_post(query_merch_info, required_params)

    @classmethod
    def add_headquarters(cls,
                         name,
                         contact_name,
                         contact_mobile_no,
                         contact_cert_no,
                         login_name="",
                         login_mobile_no="",
                         add_corp_info: CorpInfo = None,
                         bd_login_user_id="",
                         mer_huifu_id="",
                         **kwargs):
        """
        新增总部
        :param name: 总部名称
        :param contact_name: 联系人姓名
        :param contact_mobile_no: 联系人手机号
        :param contact_cert_no:  联系人身份证号码
        :param login_name: 管理员账号，有值，必须全网唯一；为空，不生成管理员账号
        :param login_mobile_no: 管理员手机号
        :param add_corp_info: 企业信息
        :param bd_login_user_id: 业务经理userId
        :param mer_huifu_id: 商户汇付Id
        :param kwargs:
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "name": name,
            "contact_name": contact_name,
            "contact_mobile_no": contact_mobile_no,
            "contact_cert_no": contact_cert_no,
            "login_name": login_name,
            "login_mobile_no": login_mobile_no,
            "bd_login_user_id": bd_login_user_id,
            "mer_huifu_id": mer_huifu_id,
        }
        if add_corp_info:
            required_params["add_corp_info"] = add_corp_info.obj_to_dict()

        required_params.update(kwargs)
        return request_post(add_chains_corp_info, required_params)

    @classmethod
    def modify_headquarters(cls,
                            name="",
                            contact_name="",
                            contact_mobile_no="",
                            contact_cert_no="",
                            edit_corp_info: CorpInfo = None,
                            mer_huifu_id="",
                            **kwargs):
        """
        修改总部
        :param name: 总部名称
        :param contact_name: 联系人姓名
        :param contact_mobile_no: 联系人手机号
        :param contact_cert_no:  联系人身份证号码
        :param edit_corp_info: 企业信息
        :param mer_huifu_id: 商户汇付Id
        :param kwargs:
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "name": name,
            "contact_name": contact_name,
            "contact_mobile_no": contact_mobile_no,
            "contact_cert_no": contact_cert_no,
            "mer_huifu_id": mer_huifu_id,
        }
        if edit_corp_info:
            required_params["edit_corp_info"] = edit_corp_info.obj_to_dict()

        required_params.update(kwargs)
        return request_post(modify_chains_corp_info, required_params)

    @classmethod
    def bind_headquarters(cls, chains_id, state, mer_type, **kwargs):
        """
        总部商户绑定&解除
        :param chains_id: 连锁编号,每个总部下最多添加50个商户
        :param state: 状态，1绑定，0 解除
        :param mer_type: 商户类型，0 自营，1 加盟
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id,
            "chains_id": chains_id,
            "state": state,
            "mer_type": mer_type,
        }
        required_params.update(kwargs)
        return request_post(bind_chains_mer, required_params)

    @classmethod
    def query_acct_info(cls, **kwargs):

        #TODO
        required_params = {
            "product_id": DGClient.mer_config.product_id
        }
        required_params.update(kwargs)
        return request_post(query_mer_split_config, required_params)



    @classmethod
    def reg_busi_info(cls, **kwargs):
        """
        商户业务开通
        :param kwargs:
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id
        }
        required_params.update(kwargs)
        return request_post(query_mer_split_config, required_params)


    @classmethod
    def query_split_config(cls, **kwargs):
        """
        查询商户分账配置信息
        :return:
        """

        required_params = {
            "product_id": DGClient.mer_config.product_id
        }
        required_params.update(kwargs)
        return request_post(query_mer_split_config, required_params)
