# Changelog

## 0.1.0 (2024-03-15)

* First release on PyPI.


## 0.1.1 (2024-04-08)

* Increase max length of Purpose of Transaction


## 0.1.2 (2024-10-19)

* Fix the CRC issue


## 0.2.0 (2026-07-20)

* Support the full NAPAS247 field set in both encode and decode: MCC (52), tip/convenience indicator (55) and fees (56, 57), merchant name/city/postal (59, 60, 61), and the Merchant Information Language template (64: language preference, alternate name/city).
* Add VietQR decoder: `decode()`, `QRPay.decode()`, `QRPay.parse()`, with CRC verification (`verify_checksum`).
* Add `napas_qr` CLI with `encode` / `decode` subcommands.
* Emit root data objects in spec ID order (`38` before `53`, matching spec §6.1 examples). 
* Fix inverted Point of Initiation Method. 
