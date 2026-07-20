from typing import Any, Dict, List, Literal, Optional

import segno

from . import fields
from .crc import calculate_checksum
from .decode import decode as _decode_payload
from .decode import parse as _parse_payload


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
        merchant_category_code: Optional[str] = None,
        transaction_currency: Optional[str] = None,
        tip_or_convenience_indicator: Optional[str] = None,
        convenience_fee_fixed: Optional[str] = None,
        convenience_fee_percentage: Optional[str] = None,
        country_code: Optional[str] = None,
        merchant_name: Optional[str] = None,
        merchant_city: Optional[str] = None,
        postal_code: Optional[str] = None,
        bill_number: Optional[str] = None,
        mobile_number: Optional[str] = None,
        store_label: Optional[str] = None,
        loyalty_number: Optional[str] = None,
        reference_label: Optional[str] = None,
        customer_label: Optional[str] = None,
        terminal_label: Optional[str] = None,
        additional_consumer_data_request: Optional[str] = None,
        language_preference: Optional[str] = None,
        merchant_name_alt: Optional[str] = None,
        merchant_city_alt: Optional[str] = None,
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
        self.merchant_category_code = merchant_category_code
        self.transaction_currency = transaction_currency
        self.tip_or_convenience_indicator = tip_or_convenience_indicator
        self.convenience_fee_fixed = convenience_fee_fixed
        self.convenience_fee_percentage = convenience_fee_percentage
        self.country_code = country_code
        self.merchant_name = merchant_name
        self.merchant_city = merchant_city
        self.postal_code = postal_code
        self.bill_number = bill_number
        self.mobile_number = mobile_number
        self.store_label = store_label
        self.loyalty_number = loyalty_number
        self.reference_label = reference_label
        self.customer_label = customer_label
        self.terminal_label = terminal_label
        self.purpose_of_transaction = purpose_of_transaction
        self.language_preference = language_preference
        self.merchant_name_alt = merchant_name_alt
        self.merchant_city_alt = merchant_city_alt
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def decode(cls, code: str, verify_crc: bool = True) -> "QRPay":
        """Build a :class:`QRPay` from a raw VietQR payload string.

        Set ``verify_crc=False`` to skip CRC validation (e.g. when decoding
        a payload known to have a non-standard checksum). Raises
        ``qr_pay.decode.QRDecodeError`` on malformed input.
        """
        data: Dict[str, Any] = {k: v for k, v in _decode_payload(code, verify_crc=verify_crc).items() if v is not None}
        return cls(**data)

    @staticmethod
    def parse(code: str, verify_crc: bool = True):
        """Parse a raw payload into nested EMVCo TLV objects (no field mapping)."""
        return _parse_payload(code, verify_crc=verify_crc)

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

    def _merchant_account_information_code(self) -> str:
        payment_network_specific_value = self.get_value_by_list_key(["bin_id", "consumer_id"])
        payment_network_specific = self.get_code_by_key("payment_network_specific", payment_network_specific_value)
        glocal_uuid = self.get_code_by_key("global_uuid")
        service_code = self.get_code_by_key("service_code")
        account_information_value = glocal_uuid + payment_network_specific + service_code
        return self.get_code_by_key("consumer_account_information", account_information_value)

    def _additional_data_code(self) -> str:
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
        return self.get_code_by_key("additional_data_field_templates", additional_data_value)

    def _merchant_language_code(self) -> str:
        language_keys = ["language_preference", "merchant_name_alt", "merchant_city_alt"]
        language_value = self.get_value_by_list_key(language_keys)
        return self.get_code_by_key("merchant_information_language_template", language_value)

    @property
    def code(self) -> str:
        # Root data objects in ascending ID order (spec §6.1 examples), CRC (63) last.
        code_list = [
            self.get_code_by_key("payload_format_indicator"),  # 00
            self.get_code_by_key("point_of_initiation_method"),  # 01
            self._merchant_account_information_code(),  # 38
            self.get_code_by_key("merchant_category_code"),  # 52
            self.get_code_by_key("transaction_currency"),  # 53
            self.get_code_by_key("transaction_amount"),  # 54
            self.get_code_by_key("tip_or_convenience_indicator"),  # 55
            self.get_code_by_key("convenience_fee_fixed"),  # 56
            self.get_code_by_key("convenience_fee_percentage"),  # 57
            self.get_code_by_key("country_code"),  # 58
            self.get_code_by_key("merchant_name"),  # 59
            self.get_code_by_key("merchant_city"),  # 60
            self.get_code_by_key("postal_code"),  # 61
            self._additional_data_code(),  # 62
            self._merchant_language_code(),  # 64
            self.get_code_by_key("crc", ""),  # 63 (id + length, value excluded)
        ]

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
