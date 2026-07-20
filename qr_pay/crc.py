def calculate_checksum(raw_data: str) -> str:
    data = raw_data.encode('ascii')
    polynomial = 0x1021  # Polynomial '1021' (hex)
    initial_value = 0xFFFF  # Initial value 'FFFF' (hex)

    crc = initial_value
    for byte in data:
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynomial
            else:
                crc <<= 1
    checksum = crc & 0xFFFF
    return "%04X" % checksum


def verify_checksum(code: str) -> bool:
    """Verify the trailing CRC of a full VietQR payload.

    The checksum (ISO/IEC 13239) is computed over every byte up to and
    including the CRC id + length ("6304"), but excluding the CRC value
    itself, i.e. everything except the final four hex characters.
    """
    if len(code) < 8 or code[-8:-4] != "6304":
        return False
    return calculate_checksum(code[:-4]).upper() == code[-4:].upper()
