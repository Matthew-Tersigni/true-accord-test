import requests

__all__ = ['PaymentsAPI']


class PaymentsAPI:
    def __init__(self, url=None):
        self.url = url or 'https://my-json-server.typicode.com/druska/trueaccord-mock-payments-api'

    def get_debts(self):
        r = requests.get(self.url + '/debts')
        return r.json()

    def get_payments(self):
        r = requests.get(self.url + '/payments')
        return r.json()

    def get_payment_plans(self):
        r = requests.get(self.url + '/payment_plans')
        return r.json()
