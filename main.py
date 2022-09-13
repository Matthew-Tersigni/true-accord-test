import json
from src.paymentsProcessor import PaymentsProcessor


def main():
    data = PaymentsProcessor().get_debts()
    for part in data:
        print(json.dumps(part))


if __name__ == "__main__":
    main()
