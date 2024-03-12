from typing import List, Literal, Optional

import segno

from . import fields
from .crc import calculate_checksum


class QRPay:
    def __init__(
        self,
        bin_id: str,
        consumer_id: str,
        transaction_amount: Optional[int] = None,
        purpose_of_transaction: Optional[str] = None,
        payload_format_indicator: Optional[str] = None,
        point_of_initiation_method: Optional[Literal["STATIC", "DYNAMIC"]] = "DYNAMIC",
        glocal_uuid: Optional[str] = None,
        service_code: Optional[Literal["PAYMENT", "CASH_WITHDRAWL", "CARD", "ACCOUNT"]] = "ACCOUNT",
        transaction_currency: Optional[str] = None,
        country_code: Optional[str] = None,
        bill_number: Optional[str] = None,
        mobile_number: Optional[str] = None,
        store_label: Optional[str] = None,
        loyalty_number: Optional[str] = None,
        reference_label: Optional[str] = None,
        customer_label: Optional[str] = None,
        terminal_label: Optional[str] = None,
        additional_consumer_data_request: Optional[str] = None,
        *args,
        **kwargs,
    ):
        self.bin_id = bin_id
        self.consumer_id = consumer_id
        self.transaction_amount = transaction_amount
        self.additional_consumer_data_request = additional_consumer_data_request
        self.payload_format_indicator = payload_format_indicator
        self.point_of_initiation_method = point_of_initiation_method
        self.global_uuid = glocal_uuid
        self.service_code = service_code
        self.transaction_currency = transaction_currency
        self.country_code = country_code
        self.bill_number = bill_number
        self.mobile_number = mobile_number
        self.store_label = store_label
        self.loyalty_number = loyalty_number
        self.reference_label = reference_label
        self.customer_label = customer_label
        self.terminal_label = terminal_label
        self.purpose_of_transaction = purpose_of_transaction
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_class_name_by_key(self, key: str) -> str:
        words = key.split('_')
        class_name = ''.join(word.capitalize() for word in words)
        return class_name

    def get_code_by_key(self, key: str, value=None) -> str:
        class_name = self.get_class_name_by_key(key)
        if value is None:
            value = getattr(self, key)
        cls = getattr(fields, class_name)
        if value:
            return cls(value).code
        return cls().code

    def get_value_by_list_key(self, list_key: List[str]) -> str:
        return "".join(list(map(self.get_code_by_key, list_key)))

    @property
    def code(self) -> str:
        base_key_list = [
            "payload_format_indicator",
            "point_of_initiation_method",
            "transaction_currency",
            "transaction_amount",
            "country_code",
        ]
        code_list = [self.get_value_by_list_key(base_key_list)]

        payment_network_specific_value = self.get_value_by_list_key(
            [
                "bin_id",
                "consumer_id",
            ]
        )
        payment_network_specific = self.get_code_by_key("payment_network_specific", payment_network_specific_value)
        glocal_uuid = self.get_code_by_key("global_uuid")
        service_code = self.get_code_by_key("service_code")
        account_information_value = glocal_uuid + payment_network_specific + service_code
        consumer_account_information = self.get_code_by_key("consumer_account_information", account_information_value)
        code_list.append(consumer_account_information)

        additional_data_keys = [
            "bill_number",
            "mobile_number",
            "store_label",
            "loyalty_number",
            "reference_label",
            "customer_label",
            "terminal_label",
            "purpose_of_transaction",
            "additional_consumer_data_request",
        ]
        additional_data_value = self.get_value_by_list_key(additional_data_keys)
        additional_data_field_templates = self.get_code_by_key("additional_data_field_templates", additional_data_value)
        code_list.append(additional_data_field_templates)

        code_list.append(self.get_code_by_key("crc", ""))

        code = "".join(code_list)
        checksum = calculate_checksum(code)
        code += checksum
        return code

    def generate_qr_code_image(self, code: str, dist: Optional[str] = None, styles: Optional[dict] = {}):
        img = segno.make_qr(code)
        dist = dist or "qr_code.png"
        segno_style = styles or {}
        img.save(dist, **segno_style)
        return img

    def generate_qr_pay(self, dist: Optional[str] = None, styles: Optional[dict] = {}) -> None:
        self.generate_qr_code_image(self.code, dist, styles)
