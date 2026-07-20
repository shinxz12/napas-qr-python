"""Command-line interface for napas-qr-python.

Usage::

    napas_qr decode <code>
    napas_qr encode --bin 970436 --consumer 1031933430 [--amount 2000000] ...
"""
import argparse
import json
import sys
from typing import List, Optional

from .decode import QRDecodeError
from .decode import decode as decode_payload
from .qr_pay import QRPay


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="napas_qr", description="Encode/decode VietQR (NAPAS247) payloads.")
    sub = parser.add_subparsers(dest="command", required=True)

    dec = sub.add_parser("decode", help="Decode a raw VietQR payload into fields.")
    dec.add_argument("code", help="Raw VietQR payload string.")
    dec.add_argument("--no-verify", action="store_true", help="Skip CRC verification.")

    enc = sub.add_parser("encode", help="Encode fields into a VietQR payload.")
    enc.add_argument("--bin", dest="bin_id", required=True, help="Beneficiary BIN / bank code.")
    enc.add_argument("--consumer", dest="consumer_id", required=True, help="Card or account number.")
    enc.add_argument("--amount", dest="transaction_amount", type=int, help="Transaction amount.")
    enc.add_argument("--purpose", dest="purpose_of_transaction", help="Purpose / message.")
    enc.add_argument(
        "--service",
        dest="service_code",
        default="ACCOUNT",
        choices=["PAYMENT", "CASH_WITHDRAWL", "CARD", "ACCOUNT"],
        help="Service code (default: ACCOUNT).",
    )
    enc.add_argument(
        "--method",
        dest="point_of_initiation_method",
        default="DYNAMIC",
        choices=["STATIC", "DYNAMIC"],
        help="Point of initiation method (default: DYNAMIC).",
    )
    enc.add_argument("--qr", metavar="PATH", help="Also write a QR image to PATH.")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "decode":
        try:
            data = decode_payload(args.code, verify_crc=not args.no_verify)
        except QRDecodeError as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        print(json.dumps({k: v for k, v in data.items() if v is not None}, ensure_ascii=False, indent=2))
        return 0

    # encode
    kwargs = {
        "bin_id": args.bin_id,
        "consumer_id": args.consumer_id,
        "service_code": args.service_code,
        "point_of_initiation_method": args.point_of_initiation_method,
        "transaction_amount": args.transaction_amount,
        "purpose_of_transaction": args.purpose_of_transaction,
    }
    qr_pay = QRPay(**{k: v for k, v in kwargs.items() if v is not None})
    print(qr_pay.code)
    if args.qr:
        qr_pay.generate_qr_pay(dist=args.qr)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
