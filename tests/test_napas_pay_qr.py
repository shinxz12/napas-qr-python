#!/usr/bin/env python

from qr_pay import QRPay


def test_qr_code_generate():
    qr_pay = QRPay('970436', '1031933430', purpose_of_transaction="Hello VietNam", transaction_amount=2000000)
    code = qr_pay.code
    assert (
        code
        == "0002010102115303704540720000005802VN38540010A00000072701240006970436011010319334300208QRIBFTTA62170813Hello VietNam63044A57"
    )
