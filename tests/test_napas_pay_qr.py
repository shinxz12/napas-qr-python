#!/usr/bin/env python

import pytest

from qr_pay import QRPay, calculate_checksum, decode, parse, verify_checksum
from qr_pay.cli import main as cli_main
from qr_pay.decode import QRDecodeError, TLVObject, parse_tlv
from qr_pay.fields import Field


def test_qr_code_generate():
    qr_pay = QRPay('970436', '1031933430', purpose_of_transaction="Hello VietNam", transaction_amount=2000000)
    code = qr_pay.code
    assert (
        code
        == "00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA5303704540720000005802VN62170813Hello VietNam6304B872"
    )


def test_verify_checksum():
    code = (
        "00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA"
        "5303704540720000005802VN62170813Hello VietNam6304B872"
    )
    assert verify_checksum(code) is True
    assert verify_checksum(code[:-1] + "0") is False


def test_decode_extracts_fields():
    code = (
        "00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA"
        "5303704540720000005802VN62170813Hello VietNam6304B872"
    )
    data = decode(code)
    assert data["bin_id"] == "970436"
    assert data["consumer_id"] == "1031933430"
    assert data["service_code"] == "QRIBFTTA"
    assert data["transaction_amount"] == "2000000"
    assert data["transaction_currency"] == "704"
    assert data["country_code"] == "VN"
    assert data["purpose_of_transaction"] == "Hello VietNam"
    assert data["glocal_uuid"] == "A000000727"


def test_decode_round_trip():
    original = QRPay('970436', '1031933430', purpose_of_transaction="Hello VietNam", transaction_amount=2000000)
    rebuilt = QRPay.decode(original.code)
    assert rebuilt.code == original.code


def test_decode_rejects_bad_crc():
    code = (
        "00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA"
        "5303704540720000005802VN62170813Hello VietNam63040000"
    )
    with pytest.raises(QRDecodeError):
        decode(code)


def test_full_field_encode_decode_round_trip():
    original = QRPay(
        '970403',
        '0011012345678',
        service_code='ACCOUNT',
        point_of_initiation_method='DYNAMIC',
        transaction_amount=180000,
        merchant_category_code='5812',
        tip_or_convenience_indicator='03',
        convenience_fee_percentage='2.5',
        merchant_name='CONG TY ABC',
        merchant_city='HANOI',
        postal_code='100000',
        bill_number='NPS6869',
        reference_label='REF01',
        purpose_of_transaction='thanh toan',
        language_preference='vi',
        merchant_name_alt='Cong ty ABC',
        merchant_city_alt='Ha Noi',
    )
    code = original.code
    assert verify_checksum(code) is True

    data = decode(code)
    assert data["merchant_category_code"] == "5812"
    assert data["tip_or_convenience_indicator"] == "03"
    assert data["convenience_fee_percentage"] == "2.5"
    assert data["merchant_name"] == "CONG TY ABC"
    assert data["merchant_city"] == "HANOI"
    assert data["postal_code"] == "100000"
    assert data["reference_label"] == "REF01"
    assert data["language_preference"] == "vi"
    assert data["merchant_name_alt"] == "Cong ty ABC"
    assert data["merchant_city_alt"] == "Ha Noi"

    assert QRPay.decode(code).code == code


def test_decode_official_spec_example_dynamic_account():
    # §6.1.3 QR động đến tài khoản (well-formed reference example)
    code = (
        "00020101021238570010A00000072701270006970403011300110123456780208QRIBFTTA"
        "530370454061800005802VN62340107NPS68690819thanh toan don hang63042E2E"
    )
    data = decode(code)
    assert data["bin_id"] == "970403"
    assert data["consumer_id"] == "0011012345678"
    assert data["service_code"] == "QRIBFTTA"
    assert data["point_of_initiation_method"] == "12"  # 12 = dynamic per spec §5.2.2
    assert data["transaction_amount"] == "180000"
    assert data["bill_number"] == "NPS6869"
    assert data["purpose_of_transaction"] == "thanh toan don hang"


def test_decode_tolerates_malformed_nested_template():
    # §6.1.1 static example has an off-by-one inner sub-length; decode must not crash.
    code = "00020101021138570010A00000072701270006970403011200110123456780208QRIBFTTA53037045802VN6304F4E5"
    data = decode(code)
    assert data["point_of_initiation_method"] == "11"  # 11 = static per spec §5.2.2
    assert data["glocal_uuid"] == "A000000727"
    assert data["service_code"] == "QRIBFTTA"


def test_parse_returns_nested_tlv():
    code = (
        "00020101021238570010A00000072701270006970403011300110123456780208QRIBFTTA"
        "530370454061800005802VN62340107NPS68690819thanh toan don hang63042E2E"
    )
    root = QRPay.parse(code)
    merchant = root["38"]
    assert merchant.get("00") == "A000000727"
    assert merchant.children["01"].get("00") == "970403"


# --------------------------------------------------------------------------- #
# CRC
# --------------------------------------------------------------------------- #

def test_calculate_checksum_known_value():
    # §6.1.1 CRC input (without the final value) -> F4E5
    data = "00020101021138570010A00000072701270006970403011200110123456780208QRIBFTTA53037045802VN6304"
    assert calculate_checksum(data) == "F4E5"


def test_verify_checksum_rejects_short_or_wrong_tag():
    assert verify_checksum("") is False
    assert verify_checksum("630") is False  # shorter than 8 chars
    assert verify_checksum("123456780000") is False  # 12 chars but no "6304" before value
    assert verify_checksum("63040000") is False  # correct tag, wrong checksum


def test_verify_checksum_accepts_lowercase_crc_suffix():
    code = QRPay('970436', '1031933430').code
    # Only the 4-char CRC hex value may vary in case; the data bytes must not.
    assert verify_checksum(code[:-4] + code[-4:].lower()) is True
    assert verify_checksum(code[:-4] + code[-4:].upper()) is True


# --------------------------------------------------------------------------- #
# Field validation
# --------------------------------------------------------------------------- #

def test_invalid_point_of_initiation_method_raises():
    with pytest.raises(ValueError):
        QRPay('970436', '1031933430', point_of_initiation_method='99').code


def test_invalid_service_code_raises():
    with pytest.raises(ValueError):
        QRPay('970436', '1031933430', service_code='NOPE').code


def test_invalid_tip_indicator_raises():
    with pytest.raises(ValueError):
        QRPay('970436', '1031933430', tip_or_convenience_indicator='09').code


def test_transaction_amount_exceeding_max_length_raises():
    with pytest.raises(ValueError):
        QRPay('970436', '1031933430', transaction_amount='1' * 14).code


def test_consumer_id_exceeding_max_length_raises():
    with pytest.raises(ValueError):
        QRPay('970436', '0' * 20).code


@pytest.mark.parametrize(
    "method,expected",
    [("STATIC", "010211"), ("DYNAMIC", "010212")],
)
def test_point_of_initiation_alias_resolution(method, expected):
    code = QRPay('970436', '1031933430', point_of_initiation_method=method).code
    assert expected in code


@pytest.mark.parametrize(
    "service,expected",
    [("PAYMENT", "QRPUSH"), ("CASH_WITHDRAWL", "QRCASH"), ("CARD", "QRIBFTTC"), ("ACCOUNT", "QRIBFTTA")],
)
def test_service_code_alias_resolution(service, expected):
    code = QRPay('970436', '1031933430', service_code=service).code
    assert expected in code


def test_field_base_without_id_returns_empty_code():
    assert Field().code == ""
    assert Field("value").code == ""


def test_crc_field_has_id_and_length_only():
    from qr_pay.fields import Crc

    assert Crc().code == "6304"


# --------------------------------------------------------------------------- #
# Optional field omission
# --------------------------------------------------------------------------- #

def test_optional_fields_omitted_when_absent():
    code = QRPay('970436', '1031933430').code
    assert "5404" not in code  # no transaction amount object
    assert "62" != code[len("00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA53037045802VN")]
    # no additional-data (62) or language (64) template present
    assert "6217" not in code
    assert "6431" not in code


def test_static_qr_has_no_amount():
    code = QRPay('970436', '1031933430', point_of_initiation_method='STATIC').code
    assert verify_checksum(code) is True
    assert decode(code)["transaction_amount"] is None


# --------------------------------------------------------------------------- #
# Decode / parse error handling
# --------------------------------------------------------------------------- #

def test_decode_empty_payload_raises():
    with pytest.raises(QRDecodeError):
        decode("")


def test_parse_tlv_truncated_header_raises():
    with pytest.raises(QRDecodeError):
        parse_tlv("0002011")  # dangling < 4 chars for next header


def test_parse_tlv_non_numeric_raises():
    with pytest.raises(QRDecodeError):
        parse_tlv("ZZ02ab")


def test_parse_tlv_value_exceeds_length_raises():
    with pytest.raises(QRDecodeError):
        parse_tlv("0099short")  # declares length 99 but value is short


def test_decode_skips_crc_when_disabled():
    code = (
        "00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA"
        "5303704540720000005802VN62170813Hello VietNam63040000"  # deliberately wrong CRC
    )
    data = decode(code, verify_crc=False)
    assert data["bin_id"] == "970436"
    with pytest.raises(QRDecodeError):
        decode(code)  # default verifies -> fails


def test_parse_skips_crc_when_disabled():
    code = "00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA53037045802VN63040000"
    root = parse(code, verify_crc=False)
    assert root["38"].get("00") == "A000000727"


# --------------------------------------------------------------------------- #
# Official spec examples (§6.1)
# --------------------------------------------------------------------------- #

def test_decode_spec_static_to_card():
    # §6.1.2 QR tĩnh đến thẻ
    code = "00020101021138600010A00000072701300006970403011697040311012345670208QRIBFTTC53037045802VN63044F52"
    assert verify_checksum(code) is True
    data = decode(code)
    assert data["bin_id"] == "970403"
    assert data["consumer_id"] == "9704031101234567"
    assert data["service_code"] == "QRIBFTTC"
    assert data["point_of_initiation_method"] == "11"


def test_decode_spec_dynamic_to_card():
    # §6.1.4 QR động đến thẻ
    code = (
        "00020101021238600010A00000072701300006970403011697040311012345670208QRIBFTTC"
        "530370454061800005802VN62340107NPS68690819thanh toan don hang6304A203"
    )
    assert verify_checksum(code) is True
    data = decode(code)
    assert data["service_code"] == "QRIBFTTC"
    assert data["point_of_initiation_method"] == "12"
    assert data["transaction_amount"] == "180000"
    assert data["bill_number"] == "NPS6869"


# --------------------------------------------------------------------------- #
# TLVObject
# --------------------------------------------------------------------------- #

def test_tlvobject_get_and_repr():
    obj = TLVObject("38", "value", {"00": TLVObject("00", "A000000727")})
    assert obj.get("00") == "A000000727"
    assert obj.get("99") is None
    assert "38" in repr(obj)


# --------------------------------------------------------------------------- #
# QR image generation
# --------------------------------------------------------------------------- #

def test_generate_qr_pay_writes_file(tmp_path):
    dist = tmp_path / "out.png"
    QRPay('970436', '1031933430').generate_qr_pay(dist=str(dist))
    assert dist.exists() and dist.stat().st_size > 0


def test_generate_qr_code_image_with_styles(tmp_path):
    dist = tmp_path / "styled.png"
    qr = QRPay('970436', '1031933430')
    qr.generate_qr_code_image(qr.code, dist=str(dist), styles={"scale": 2, "dark": "darkblue"})
    assert dist.exists()


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #

def test_cli_encode(capsys):
    rc = cli_main(["encode", "--bin", "970436", "--consumer", "1031933430", "--amount", "2000000"])
    out = capsys.readouterr().out.strip()
    assert rc == 0
    assert verify_checksum(out) is True
    assert decode(out)["transaction_amount"] == "2000000"


def test_cli_encode_writes_qr(tmp_path, capsys):
    dist = tmp_path / "cli.png"
    rc = cli_main(["encode", "--bin", "970436", "--consumer", "1031933430", "--qr", str(dist)])
    assert rc == 0
    assert dist.exists()


def test_cli_decode(capsys):
    code = QRPay('970436', '1031933430', transaction_amount=2000000).code
    rc = cli_main(["decode", code])
    out = capsys.readouterr().out
    assert rc == 0
    assert '"bin_id": "970436"' in out


def test_cli_decode_bad_crc_returns_error(capsys):
    rc = cli_main(["decode", "00020101021163040000"])
    err = capsys.readouterr().err
    assert rc == 1
    assert "error" in err.lower()


def test_cli_decode_no_verify(capsys):
    code = (
        "00020101021238540010A00000072701240006970436011010319334300208QRIBFTTA"
        "53037045802VN63040000"  # wrong CRC
    )
    rc = cli_main(["decode", code, "--no-verify"])
    out = capsys.readouterr().out
    assert rc == 0
    assert '"bin_id": "970436"' in out


# --------------------------------------------------------------------------- #
# Bank lookup (utils)
# --------------------------------------------------------------------------- #

def test_bank_update_reads_and_looks_up(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "resources").mkdir()

    class FakeResp:
        def raise_for_status(self):
            return None

        def json(self):
            return {"data": [{"code": "VCB", "name": "Vietcombank"}]}

    monkeypatch.setattr("qr_pay.utils.requests.get", lambda url: FakeResp())

    from qr_pay.utils import Bank

    bank = Bank()  # no file -> update_banks (mocked network) -> writes file
    assert bank.get_bank_by_code("vcb")["name"] == "Vietcombank"

    bank2 = Bank()  # file now exists -> get_banks reads it
    assert bank2.get_bank_by_code("VCB") is not None
    assert bank2.get_bank_by_code("does-not-exist") is None
