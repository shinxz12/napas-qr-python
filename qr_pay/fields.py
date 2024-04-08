from typing import Any, Optional, Tuple


class Field:
    WHITE_LIST_VALUES: Optional[Tuple[str, ...]] = None
    id: Optional[str] = None
    length: Optional[str] = None
    value: Any = None
    max_length: Optional[int] = None
    is_alias: bool = False

    def __init__(self, value=None):
        if value:
            if self.is_alias and isinstance(value, str) and getattr(self, value, None):
                value = getattr(self, value)
            value = str(value)
            if self.WHITE_LIST_VALUES and value not in self.WHITE_LIST_VALUES:
                raise ValueError(f"{self.__class__.__name__} value is invalid")
            self.value = value
        if self.value:
            self.length = str(len(str(self.value)))

        if self.length is None:
            return
        if self.max_length and self.max_length < int(self.length):
            raise ValueError(f"Length of {self.__class__.__name__} must be less than or equal to {self.max_length}")
        if len(self.length) == 1:
            self.length = "0" + self.length

    @property
    def code(self) -> str:
        if self.id is None:
            return ""
        if self.value is None and self.length is not None:
            return self.id + self.length
        if self.value is None:
            return ""
        return self.id + str(self.length) + str(self.value)


class PayloadFormatIndicator(Field):
    id = "00"
    value = "01"
    max_length = 2


class PointOfInitiationMethod(Field):
    DYNAMIC = "11"
    STATIC = "12"
    WHITE_LIST_VALUES = (DYNAMIC, STATIC)
    id = "01"
    value = DYNAMIC
    max_length = 2
    is_alias = True


class GlobalUuid(Field):
    id = "00"
    value = "A000000727"
    max_length = 32


class PaymentNetworkSpecific(Field):
    id = "01"


class BinId(Field):
    id = "00"
    value = "970403"
    max_length = 6


class ConsumerId(Field):
    id = "01"
    max_length = 19


class ServiceCode(Field):
    PAYMENT = "QRPUSH"
    CASH_WITHDRAWL = "QRCASH"
    CARD = "QRIBFTTC"
    ACCOUNT = "QRIBFTTA"
    WHITE_LIST_VALUES = (PAYMENT, CASH_WITHDRAWL, CARD, ACCOUNT)
    id = "02"
    value = ACCOUNT
    max_length = 10
    is_alias = True


class ConsumerAccountInformation(Field):
    id = "38"
    max_length = 99


class TransactionCurrency(Field):
    id = "53"
    value = "704"
    max_length = 3


class TransactionAmount(Field):
    id = "54"
    max_length = 13


class CountryCode(Field):
    id = "58"
    value = "VN"


class AdditionalDataFieldTemplates(Field):
    id = "62"
    max_length = 99


class BillNumber(Field):
    id = "01"
    max_length = 25


class MobileNumber(Field):
    id = "02"
    max_length = 25


class StoreLabel(Field):
    id = "03"
    max_length = 25


class LoyaltyNumber(Field):
    id = "04"
    max_length = 25


class ReferenceLabel(Field):
    id = "05"
    max_length = 25


class CustomerLabel(Field):
    id = "06"
    max_length = 25


class TerminalLabel(Field):
    id = "07"
    max_length = 25


class PurposeOfTransaction(Field):
    id = "08"
    # max_length = 25
    # Increasing the max length because some banks support more than the document max length
    max_length = 90


class AdditionalConsumerDataRequest(Field):
    id = "09"
    max_length = 25


class Crc(Field):
    id = "63"
    length = "04"
