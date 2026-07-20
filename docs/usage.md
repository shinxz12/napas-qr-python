# Usage

`napas-qr-python` encodes and decodes VietQR payloads for the NAPAS247 fast
transfer service (EMVCo Merchant-Presented Mode QR).

## Encode

Build a payload from fields and read it off the `.code` property:

```python
from qr_pay import QRPay

qr_pay = QRPay(
    bin_id="970436",              # beneficiary bank BIN
    consumer_id="1031933430",     # account (or card) number
    service_code="ACCOUNT",       # ACCOUNT | CARD | PAYMENT | CASH_WITHDRAWL
    transaction_amount=50000,     # optional; omit for a reusable static QR
    purpose_of_transaction="Thanh toan don hang",
)
print(qr_pay.code)
```

### Static vs dynamic

`point_of_initiation_method` follows spec §5.2.2: `"STATIC"` (emitted as `11`,
reusable / multi-use) or `"DYNAMIC"` (emitted as `12`, single transaction,
typically with a fixed amount). Default is `"DYNAMIC"`.

```python
QRPay("970436", "1031933430", point_of_initiation_method="STATIC")
```

### All fields

Every root and template object from the spec is supported — MCC (52),
tip/convenience indicator and fees (55–57), merchant name/city/postal (59–61),
additional data (62.01–09), and the alternate-language template (64). See the
parameter table on the [Home](index.md) page.

```python
qr_pay = QRPay(
    bin_id="970403",
    consumer_id="0011012345678",
    transaction_amount=189000,
    merchant_category_code="5812",
    merchant_name="CUA HANG ABC",
    merchant_city="HA NOI",
    bill_number="HD2026001",
    reference_label="REF99",
    language_preference="vi",
    merchant_name_alt="Cửa hàng ABC",
)
```

### Generate a QR image

Rendering uses [segno](https://segno.readthedocs.io/); `styles` are passed
straight through to `segno`'s `save()`:

```python
qr_pay.generate_qr_pay(dist="qr.png", styles={"scale": 8, "border": 3, "dark": "darkblue"})
```

## Decode

Parse a raw payload back into fields. The CRC is verified by default and a
`qr_pay.decode.QRDecodeError` is raised on a mismatch or malformed input.

```python
from qr_pay import QRPay, decode

code = "00020101021238570010A00000072701270006970403011300110123456780208QRIBFTTA530370454061800005802VN62340107NPS68690819thanh toan don hang63042E2E"

data = decode(code)                     # dict of fields
qr_pay = QRPay.decode(code)             # re-encodable QRPay instance
assert QRPay.decode(code).code == code  # round-trips

data = decode(code, verify_crc=False)   # skip CRC check

root = QRPay.parse(code)                # nested EMVCo TLV objects
root["38"].children["01"].get("00")     # -> '970403' (BIN)
```

## Verify a checksum

```python
from qr_pay import verify_checksum, calculate_checksum

verify_checksum(code)          # True / False over a full payload
calculate_checksum(code[:-4])  # recompute the 4-char CRC (CRC-CCITT / 0x1021)
```

## Command line

```console
$ napas_qr encode --bin 970436 --consumer 1031933430 --amount 50000 --purpose "Thanh toan"
$ napas_qr encode --bin 970436 --consumer 1031933430 --qr qr.png
$ napas_qr decode "<payload>"
$ napas_qr decode "<payload>" --no-verify
```
