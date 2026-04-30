# Mock customer data for testing
CUSTOMERS = [
    {"email": "donaldgarcia@example.net", "pin": "7912"},
    {"email": "michellejames@example.com", "pin": "1520"},
    {"email": "laurahenderson@example.org", "pin": "1488"},
    {"email": "spenceamanda@example.org", "pin": "2535"},
    {"email": "glee@example.net", "pin": "4582"},
    {"email": "williamsthomas@example.net", "pin": "4811"},
    {"email": "justin78@example.net", "pin": "9279"},
    {"email": "jason31@example.com", "pin": "1434"},
    {"email": "samuel81@example.com", "pin": "4257"},
    {"email": "williamleon@example.net", "pin": "9928"},
]

def get_customer_by_email(email: str):
    for customer in CUSTOMERS:
        if customer["email"] == email:
            return customer
    return None
