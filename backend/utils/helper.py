
import re

def validate_phone(phone_number):
    # Regex for a standard 10-digit phone number
    pattern = re.compile(r'^\d{10}$')
    return bool(pattern.match(phone_number))

def validate_pincode(pincode):
    # Regex for a standard 6-digit Indian pincode (since you're in India, this fits perfectly!)
    pattern = re.compile(r'^[1-9][0-9]{5}$')
    return bool(pattern.match(pincode))