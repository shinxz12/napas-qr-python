"""VietQR (NAPAS247 / EMVCo Merchant-Presented) decoder.

Parses a raw QR payload string back into its EMVCo TLV objects and,
where possible, into the fields understood by :class:`qr_pay.QRPay`.

Reference: "Tài liệu quy định về định dạng mã VietQR", NAPAS, v1.0 (09/2021).
"""
from typing import Dict, List, Optional

from .crc import verify_checksum

# --- Root-level object ids (Bảng 1) ---
ID_PAYLOAD_FORMAT_INDICATOR = "00"
ID_POINT_OF_INITIATION_METHOD = "01"
ID_MERCHANT_ACCOUNT_INFORMATION = "38"
ID_MERCHANT_CATEGORY_CODE = "52"
ID_TRANSACTION_CURRENCY = "53"
ID_TRANSACTION_AMOUNT = "54"
ID_TIP_OR_CONVENIENCE_INDICATOR = "55"
ID_CONVENIENCE_FEE_FIXED = "56"
ID_CONVENIENCE_FEE_PERCENTAGE = "57"
ID_COUNTRY_CODE = "58"
ID_MERCHANT_NAME = "59"
ID_MERCHANT_CITY = "60"
ID_POSTAL_CODE = "61"
ID_ADDITIONAL_DATA = "62"
ID_CRC = "63"
ID_MERCHANT_LANGUAGE = "64"

# --- Merchant Account Information sub-ids (Bảng 4) ---
ID_GUID = "00"
ID_BENEFICIARY = "01"
ID_SERVICE_CODE = "02"

# --- Beneficiary (ID 01 within 38) sub-ids ---
ID_ACQUIRER = "00"  # BIN / bank code
ID_MERCHANT = "01"  # merchant / consumer id

# --- Merchant Information Language Template sub-ids (Bảng 9) ---
ID_LANGUAGE_PREFERENCE = "00"
ID_MERCHANT_NAME_ALT = "01"
ID_MERCHANT_CITY_ALT = "02"

# --- Additional Data Field Template sub-ids (Bảng 8) ---
ADDITIONAL_DATA_FIELDS = {
    "01": "bill_number",
    "02": "mobile_number",
    "03": "store_label",
    "04": "loyalty_number",
    "05": "reference_label",
    "06": "customer_label",
    "07": "terminal_label",
    "08": "purpose_of_transaction",
    "09": "additional_consumer_data_request",
}


class QRDecodeError(ValueError):
    """Raised when a QR payload cannot be parsed as valid EMVCo TLV."""


class TLVObject:
    """A single EMVCo ID / Length / Value data object.

    ``children`` is populated for templates (ids nesting further TLV data)
    once :func:`parse` is asked to descend into them.
    """

    def __init__(self, id: str, value: str, children: Optional[Dict[str, "TLVObject"]] = None):
        self.id = id
        self.value = value
        self.children = children or {}

    def get(self, id: str) -> Optional[str]:
        child = self.children.get(id)
        return child.value if child else None

    def __repr__(self) -> str:
        return f"TLVObject(id={self.id!r}, value={self.value!r})"


def parse_tlv(data: str) -> Dict[str, TLVObject]:
    """Parse a flat EMVCo TLV string into ``{id: TLVObject}``.

    Each object is ``id`` (2 digits) + ``length`` (2 digits) + ``value``.
    Raises :class:`QRDecodeError` on any malformed structure.
    """
    result: Dict[str, TLVObject] = {}
    index = 0
    total = len(data)
    while index < total:
        if index + 4 > total:
            raise QRDecodeError(f"Truncated ID/length header at position {index}")
        id = data[index : index + 2]
        length_str = data[index + 2 : index + 4]
        if not id.isdigit() or not length_str.isdigit():
            raise QRDecodeError(f"Non-numeric ID/length {id!r}/{length_str!r} at position {index}")
        length = int(length_str)
        start = index + 4
        end = start + length
        if end > total:
            raise QRDecodeError(f"Value for ID {id!r} exceeds payload length")
        result[id] = TLVObject(id, data[start:end])
        index = end
    return result


# Ids whose value is itself a TLV template that we descend into.
_NESTED_ROOT_IDS = (ID_MERCHANT_ACCOUNT_INFORMATION, ID_ADDITIONAL_DATA, ID_MERCHANT_LANGUAGE)


def parse(code: str, verify_crc: bool = True) -> Dict[str, TLVObject]:
    """Parse a full VietQR payload into nested :class:`TLVObject` templates.

    When ``verify_crc`` is True (default) the trailing CRC is validated and
    :class:`QRDecodeError` is raised on mismatch.
    """
    if not code:
        raise QRDecodeError("Empty QR payload")
    if verify_crc and not verify_checksum(code):
        raise QRDecodeError("CRC checksum mismatch — payload is corrupt or altered")

    root = parse_tlv(code)
    for id in _NESTED_ROOT_IDS:
        obj = root.get(id)
        if obj is not None:
            obj.children = _parse_nested(obj.value)
    # Beneficiary (ID 01) inside merchant account information nests one level deeper.
    merchant = root.get(ID_MERCHANT_ACCOUNT_INFORMATION)
    if merchant is not None:
        beneficiary = merchant.children.get(ID_BENEFICIARY)
        if beneficiary is not None:
            beneficiary.children = _parse_nested(beneficiary.value)
    return root


def _parse_nested(value: str) -> Dict[str, TLVObject]:
    """Best-effort sub-template parse.

    Nested templates whose declared inner lengths don't line up (some NAPAS
    reference examples have off-by-one sub-lengths) are left un-expanded
    rather than failing the whole decode. The raw ``value`` stays available.
    """
    try:
        return parse_tlv(value)
    except QRDecodeError:
        return {}


def decode(code: str, verify_crc: bool = True) -> Dict[str, Optional[str]]:
    """Decode a VietQR payload into a flat dict of :class:`QRPay` kwargs.

    Unknown / unmapped ids are ignored. The result can be passed straight
    back into ``QRPay(**decode(code))`` to round-trip a payload.
    """
    root = parse(code, verify_crc=verify_crc)

    result: Dict[str, Optional[str]] = {
        "payload_format_indicator": _get(root, ID_PAYLOAD_FORMAT_INDICATOR),
        "point_of_initiation_method": _get(root, ID_POINT_OF_INITIATION_METHOD),
        "merchant_category_code": _get(root, ID_MERCHANT_CATEGORY_CODE),
        "transaction_currency": _get(root, ID_TRANSACTION_CURRENCY),
        "transaction_amount": _get(root, ID_TRANSACTION_AMOUNT),
        "tip_or_convenience_indicator": _get(root, ID_TIP_OR_CONVENIENCE_INDICATOR),
        "convenience_fee_fixed": _get(root, ID_CONVENIENCE_FEE_FIXED),
        "convenience_fee_percentage": _get(root, ID_CONVENIENCE_FEE_PERCENTAGE),
        "country_code": _get(root, ID_COUNTRY_CODE),
        "merchant_name": _get(root, ID_MERCHANT_NAME),
        "merchant_city": _get(root, ID_MERCHANT_CITY),
        "postal_code": _get(root, ID_POSTAL_CODE),
        "crc": _get(root, ID_CRC),
    }

    merchant = root.get(ID_MERCHANT_ACCOUNT_INFORMATION)
    if merchant is not None:
        result["glocal_uuid"] = merchant.get(ID_GUID)
        result["service_code"] = merchant.get(ID_SERVICE_CODE)
        beneficiary = merchant.children.get(ID_BENEFICIARY)
        if beneficiary is not None:
            result["bin_id"] = beneficiary.get(ID_ACQUIRER)
            result["consumer_id"] = beneficiary.get(ID_MERCHANT)

    additional = root.get(ID_ADDITIONAL_DATA)
    if additional is not None:
        for sub_id, key in ADDITIONAL_DATA_FIELDS.items():
            value = additional.get(sub_id)
            if value is not None:
                result[key] = value

    language = root.get(ID_MERCHANT_LANGUAGE)
    if language is not None:
        result["language_preference"] = language.get(ID_LANGUAGE_PREFERENCE)
        result["merchant_name_alt"] = language.get(ID_MERCHANT_NAME_ALT)
        result["merchant_city_alt"] = language.get(ID_MERCHANT_CITY_ALT)

    return result


def _get(root: Dict[str, TLVObject], id: str) -> Optional[str]:
    obj = root.get(id)
    return obj.value if obj is not None else None
