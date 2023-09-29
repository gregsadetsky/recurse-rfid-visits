# value from rfid reader - integer followed by enter key
read_value_str = "0007747995"
read_value_value = int(read_value_str, 10)

facility_id = (read_value_value >> 16) & 0xFF
print("facility_id", facility_id)
card_id = read_value_value & 0xFFFF
print("card_id", card_id)

assert card_id == 14747
