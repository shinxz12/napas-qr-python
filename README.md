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
* Using [segno](https://segno.readthedocs.io/en/latest/) for QR generator.

# Parameters
| Field                     | Mandatory | Default Value | Description                                    |
|---------------------------|-----------|---------------|------------------------------------------------|
| bin_id                    | Yes       | None          | BIN ID                                         |
| consumer_id               | Yes       | None          | Card/Account ID                                |
| service_code              | Yes       | "ACCOUNT"     | "PAYMENT", "CASH_WITHDRAWL", "CARD", "ACCOUNT" |
| transaction_amount        | No        | None          | Amount                                         |
| purpose_of_transaction.   | No        | None          | Message                                        |
| point_of_initiation_method| Yes       | "DYNAMIC"     | "DYNAMIC" OR "STATIC"                          |
| transaction_currency      | Yes       | 704(VND)      | currency                                       |
| bill_number               | No        | None          | Bill number                                    |
| mobile_number             | No        | None          | Mobile Number                                  |
| store_label               | No        | None          | Store Label                                    |
| reference_label           | No        | None          | Reference Label                                |
| customer_label            | No        | None          | Customer Label                                 |

Please read more in the VietQR docs.

## Example

* Generate code with base informations and an account service:
```
from qr_pay import QRPay

qr_pay = QRPay('970436', '1031933430', purpose_of_transaction="Thanh toan hoa don")
code = qr_pay.code
# 00020101021153037045802VN38540010A00000072701240006970436011010319334300208QRIBFTTA62220818Thanh toan hoa don6304FCE9
# Generate QR code
qr_pay.generate_qr_pay()
```

<p align="center">
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAAxAQAAAABb53yxAAABN0lEQVR42mP4DwYNDLjoD/L3Gt+wNzB8v56/TfZ7A8OXOP9tseJAOiDz0lQQHeeunisOkv9r8xco/0E0NDQEqP7/zyvb/UH6XQ2rhdY3MPzYLdX6tryB4VMz77SJ7xsY/hqamx0H8r9MO3pxOj9Qf2aubhaQ/zf66b5qoPyHZB+95/kNDH/uLswS6geKb4g7CtL/NfzplWB/oDmpMdNPAuX/uuRemCbfwPBx61F9LZB5YtXXLgHFv5h8FbsPpP/HbcwG618kdXAtUP7z1O6AeyB9vxW3RoLcw3q8cB7Q/k9LM/rLQPr7n367DzT/y3f/LeFA939jX1g1AWj+/w9xLenlIP+9vXdUH+jeW/5by0Hqg3MLBID6v4Qfa0sChU9AddjceqD8hW9954H2fBDbmJotjzt8oTQALM/W5aEFuuoAAAAASUVORK5CYII=">
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
# 0002010102115303704540720000005802VN38630010A00000072701330006970436011997043686255816010180208QRIBFTTC63045FCF
qr_pay.generate_qr_pay()
```

<p align="center">
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACkAAAApAQAAAACAGz1bAAAA4UlEQVR42mP4DwINDFipD1KRU9gbGL7f3Lv3ewPDl4DYUHEgFbvbFkTFicYCqe+3tLYC5T6IhoYAVf7/bLUfqO8j6/3A+w0Mn8oW7VrfwPCb+2yZewPDT32O4/oNDH/kZaWvNzB8S/qyoh+oXSLTHsj7v6h5FlDlF+ErLseB+h6t+g3WdyekHCi4b9IqIO9X7L4QoMpfO36tym9g+Bpz1GU6UMmqlEXngaaIVQaEA035ZGEOtOGD4FVXe6DgNZntIHcGfbnADnJ1zurtIN7zUKAp3692ay8HqbwSGo7D7xAKAFDunMTKMVUkAAAAAElFTkSuQmCC">
</p>

* Generate QR code with custom styles following segno:
```
qr_pay = QRPay('970436', '1031933430')
# Code: 0002010102115303704540720000005802VN38630010A00000072701330006970436011997043686255816010180208QRIBFTTC63045FCF
styles = { "scale": 2, "dark": "darkblue"}
dist = "qr_code_style.png"
qr_pay.generate_qr_pay(dist=dist, styles=styles)
```

<p align="center">
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFIAAABSAQMAAAD94hHYAAAABlBMVEUAAIv///+fga7nAAAA60lEQVR42rWTMWoGMAiFpa6BXEVwDXj1QFbBqwRcA9YupY1Zf6fw+CIv+gLxWxM+cgZUXotA5hf8qRBf5uZx68TAzoxVd7PuD/0gc9XFtalx6Q9JM1c/Eb2r/Xj+r2PaCUa/9SZDm6neuoFtl0F3/9UC5pZ28xsDHc1vfowWpHPevOAcq0fhQ9vsq/oh7E5E++bbaQnby79vJilztrPyRuE193KYih+1GYmPm2fe2Z7WzecoB2nb9b1DVmai7qv12es8AdGZuJc+PnCbPPKTc3aAR97GVrMHfyQDV/PG0zIQ8vBDmbjq/5P/7hvmnXQlddv3uQAAAABJRU5ErkJggg==">
</p>
