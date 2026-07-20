# Napas QR Python

[![pypi](https://img.shields.io/pypi/v/napas-qr-python.svg)](https://pypi.org/project/napas-qr-python/)
[![python](https://img.shields.io/pypi/pyversions/napas-qr-python.svg)](https://pypi.org/project/napas-qr-python/)
[![Build Status](https://github.com/shinxz12/napas-qr-python/actions/workflows/dev.yml/badge.svg)](https://github.com/shinxz12/napas-qr-python/actions/workflows/dev.yml)


Generate VietQR for python following VietQR [Vi Version](https://vietqr.net/portal-service/download/documents/QR_Format_T&C_v1.0_VN_092021.pdf)
and [En Version](https://vietqr.net/portal-service/download/documents/QR_Format_T&C_v1.5.2_EN_102022.pdf)

* Documentation: <https://shinxz12.github.io/napas-qr-python>
* GitHub: <https://github.com/shinxz12/napas-qr-python>
* PyPI: <https://pypi.org/project/napas-qr-python/>
* Free software: MIT

## Features

* VietQR code encoder.
* VietQR code decoder with CRC verification.
* Using [segno](https://segno.readthedocs.io/en/latest/) for QR generator.

# Parameters

All root and template fields from the NAPAS247 spec are supported.

| Field                          | ID    | Mandatory | Default     | Description                                    |
|--------------------------------|-------|-----------|-------------|------------------------------------------------|
| bin_id                         | 38.01.00 | Yes    | None        | Beneficiary BIN / bank code                    |
| consumer_id                    | 38.01.01 | Yes    | None        | Card / account ID                              |
| service_code                   | 38.02 | Yes       | "ACCOUNT"   | "PAYMENT", "CASH_WITHDRAWL", "CARD", "ACCOUNT" |
| glocal_uuid                    | 38.00 | No        | "A000000727"| NAPAS AID (GUID)                               |
| payload_format_indicator       | 00    | No        | "01"        | Payload format version                         |
| point_of_initiation_method     | 01    | Yes       | "DYNAMIC"   | "STATIC" (11) or "DYNAMIC" (12)                |
| merchant_category_code         | 52    | No        | None        | MCC (ISO 18245)                                |
| transaction_currency           | 53    | Yes       | "704" (VND) | Currency (ISO 4217)                            |
| transaction_amount             | 54    | No        | None        | Amount                                         |
| tip_or_convenience_indicator   | 55    | No        | None        | "01", "02" or "03"                             |
| convenience_fee_fixed          | 56    | No        | None        | Fixed fee (when indicator = 02)                |
| convenience_fee_percentage     | 57    | No        | None        | Percentage fee (when indicator = 03)           |
| country_code                   | 58    | Yes       | "VN"        | Country (ISO 3166-1 alpha-2)                   |
| merchant_name                  | 59    | No        | None        | Merchant name                                  |
| merchant_city                  | 60    | No        | None        | Merchant city                                  |
| postal_code                    | 61    | No        | None        | Postal code                                    |
| bill_number                    | 62.01 | No        | None        | Bill number                                    |
| mobile_number                  | 62.02 | No        | None        | Mobile number                                  |
| store_label                    | 62.03 | No        | None        | Store label                                    |
| loyalty_number                 | 62.04 | No        | None        | Loyalty number                                 |
| reference_label                | 62.05 | No        | None        | Reference label                                |
| customer_label                 | 62.06 | No        | None        | Customer label                                 |
| terminal_label                 | 62.07 | No        | None        | Terminal label                                 |
| purpose_of_transaction         | 62.08 | No        | None        | Purpose / message                              |
| additional_consumer_data_request| 62.09| No        | None        | "A", "M", "E" combination                      |
| language_preference            | 64.00 | No        | None        | Alternate language (ISO 639)                   |
| merchant_name_alt              | 64.01 | No        | None        | Merchant name (alternate language)             |
| merchant_city_alt              | 64.02 | No        | None        | Merchant city (alternate language)             |

Please read more in the VietQR docs.

## Example

* Generate code with base informations and an account service:
```
from qr_pay import QRPay

qr_pay = QRPay('970436', '1031933430', purpose_of_transaction="Thanh toan hoa don")
code = qr_pay.code
# 00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA53037045802VN62220818Thanh toan hoa don6304E8A4
# Generate QR code
qr_pay.generate_qr_pay()
```

<p align="center">
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGIAAABiAQAAAACD3jujAAABRElEQVR42r1UMYpFMQiUtQ3kKgFbwasHbANeRbAV3Pytdon12j2GyTg6PqhfteEfvgCDcmM6yP6CP1USk8MYo15s0fE6RYEdNlNjKLVYLWHhjiexJOxEpwdIP7WaPqtSRIU/jh7eggliOM6LobHmpgx530RaW5C18uV5gt253DYbDIcTgY79YjGV/QTHfPV4ySHaZOPlSd49gDvzi23UgXyk0+NpkU4eDQ+IOGiF0ovpyEV62+z0Ajni+tOGN9VpFHfzJNiid2YGzZuWJZMTGz2DM5ENOn+jVI/jCel4tWdAjAabw6baav3da3AR0NP447rL3SXU+LtpyM/MTpMXsatka62mF9JaKAcBq8m1xCef0vDuPTAFO81GL5xyet07627z7gdavYv52CynvXeWkBGEnd4K3unW5QxXfPanrb///Nd9AyIx88qkxwgJAAAAAElFTkSuQmCC">
</p>

* Generate code with a card service and amount:
```
data = {
    "bin_id": "970436",
    "consumer_id": "9704368625581601018",
    "service_code": "CARD",
    "transaction_amount": 2000000
}
qr_pay = QRPay(**data)
code = qr_pay.code
# 00020101021238630010A00000072701330006970436011997043686255816010180208QRIBFTTC5303704540720000005802VN6304A2DC
qr_pay.generate_qr_pay()
```

<p align="center">
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFIAAABSAQAAAADvV742AAAA60lEQVR42rWTMYqEMQiFZW2FXEWw/cGrC2kFrxKwDbjZZpiN045VeLyYL/EF6lUGX1kDhggvUPuBtyrNyRRZt86CipnYddsRn/SckoK9f1BMaf0B5RQ3nqpB5H/M/3UEWad93vrQx6c53fqWiJnCjXMXbHa//cIle3I2f50NHnb7Jz547tv8O8iCOk8uezi58UQ8biMaz4DF4xG9/RTu2zv/xCG5RG6/e1Cx79uvB76szysIKczX7eejLQHt8wIH1nZfQGRN0XZusuvS0fMjJ4RAXXdCX30uwuc5NXveMMDdPuRtm8zs/N/8d79J+XYm3YJ18AAAAABJRU5ErkJggg==">
</p>

* Generate QR code with custom styles following segno:
```
qr_pay = QRPay('970436', '1031933430')
# Code: 00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA53037045802VN630424AB
styles = { "scale": 2, "dark": "darkblue"}
dist = "qr_code_style.png"
qr_pay.generate_qr_pay(dist=dist, styles=styles)
```

<p align="center">
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFIAAABSAQMAAAD94hHYAAAABlBMVEUAAIv///+fga7nAAAA7UlEQVR42rWTsYoGMQiE5WyFvIpgK/jqAduArxKwDXj7N8cRt/2twjCZ/TLJQv3NhK+sAUWNNtj8gX9TllPFsm6dBXOk4ItOvt501amJPX8HHWn5D88z3HiqElw/zJc/2Tij5TsJFqrc/iEwXHPdfjoeEKG33xHHQ9lykAhDt985mHseiXP7ZZ3S0XmEQ1x341nHijY1npSczxdaD6uOm0q0Pmd5Sj8XxtMoqt964diJ/d7XINwYcPsZ56c5azmla6iNfr/B6sL9PfjYZtzyZVUwvOiDnk3Q3xsrLm49W4oiZ+MEpEFi0Pm/+d/9Avuabi7z3CkuAAAAAElFTkSuQmCC">
</p>

## Decode

Parse a raw VietQR payload back into fields. The CRC is verified by default
(raises `qr_pay.decode.QRDecodeError` on mismatch or malformed input).

```python
from qr_pay import QRPay, decode

code = "00020101021238570010A00000072701270006970403011300110123456780208QRIBFTTA530370454061800005802VN62340107NPS68690819thanh toan don hang63042E2E"

# As a dict of fields
data = decode(code)
# {'bin_id': '970403', 'consumer_id': '0011012345678', 'service_code': 'QRIBFTTA',
#  'transaction_amount': '180000', 'point_of_initiation_method': '12',
#  'purpose_of_transaction': 'thanh toan don hang', ...}

# As a QRPay instance (re-encodable)
qr_pay = QRPay.decode(code)
assert qr_pay.bin_id == "970403"

# Skip CRC verification for non-standard payloads
data = decode(code, verify_crc=False)

# Low-level nested EMVCo TLV objects
root = QRPay.parse(code)
root["38"].children["01"].get("00")  # -> '970403' (BIN)
```

## Command line

Installing the package exposes a `napas_qr` command with `encode` and `decode`
subcommands.

```console
# Encode fields into a payload (and optionally write a QR image)
$ napas_qr encode --bin 970436 --consumer 1031933430 --amount 50000 --purpose "Thanh toan"
00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA53037045405500005802VN62140810Thanh toan630438A6

$ napas_qr encode --bin 970436 --consumer 1031933430 --qr qr.png

# Decode a payload into JSON (CRC verified by default)
$ napas_qr decode "00020101021238570010A00000072701270006970403011300110123456780208QRIBFTTA530370454061800005802VN62340107NPS68690819thanh toan don hang63042E2E"
{
  "point_of_initiation_method": "12",
  "bin_id": "970403",
  "consumer_id": "0011012345678",
  "transaction_amount": "180000",
  "purpose_of_transaction": "thanh toan don hang",
  ...
}

# Decode without CRC verification
$ napas_qr decode "<payload>" --no-verify
```

Full option list: `napas_qr encode --help` / `napas_qr decode --help`.
