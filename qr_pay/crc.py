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
    return hex(checksum)[2:].upper()
