def valid_email(email):
    return bool(email and '@' in email and '.' in email.split('@')[-1])

def valid_price(value):
    try:
        return float(value) >= 0
    except (ValueError, TypeError):
        return False
