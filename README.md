# napas-qr

Generate VietQR for python following VietQR [Vi Version](https://vietqr.net/portal-service/download/documents/QR_Format_T&C_v1.0_VN_092021.pdf)
and [En Version](https://vietqr.net/portal-service/download/documents/QR_Format_T&C_v1.5.2_EN_102022.pdf)

## Features

* VietQR code encoder.
* Using [segno](https://segno.readthedocs.io/en/latest/) for QR generator.

# Parameters
| field           | mandatory | default value | description|
|-----------------|---------|---------|--------------------|
| bin_id          | Yes     | None    | BIN ID             |
| consumer_id     | Yes     | None    | Card/Account ID|
| service_code    | Yes     | "ACCOUNT"|"PAYMENT", "CASH_WITHDRAWL", "CARD", "ACCOUNT"|
| transaction_amount        | No      | None  | Amount|
| purpose_of_transaction.   | No      |  None | Message|
| point_of_initiation_method| Yes     |  "DYNAMIC"   | "DYNAMIC" OR "STATIC"|
| transaction_currency      | Yes     |   704(VND) |    currency|
| bill_number               | No      |   None |    Country code|
| mobile_number             | No      |   None |    Country code|
| store_label               | No      |   None   |    Country code|
| reference_label           | No      |   None   |    Country code|
| customer_label            | No      |   None   |    Country code|

Read more in the VietQR docs.

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
    <img src="./resources/images/qr_code_base.png">
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
    <img src="./resources/images/qr_code_card.png">
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
    <img src="./resources/images/qr_code_style.png">
</p>
