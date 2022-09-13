import json
from unittest import TestCase
from src.utils.paymentsAPI import PaymentsAPI
from src.paymentsProcessor import PaymentsProcessor

__all__ = ['TestPaymentsAPI', 'IntegrationTestCase']


class TestPaymentsAPI(TestCase):
    def setUp(self):
        self.paymentsAPI = PaymentsAPI()
        self.paymentsProcessor = PaymentsProcessor(self.paymentsAPI)

    def test_get_debts(self):
        data = self.paymentsAPI.get_debts()
        expected = [
            {
                "amount": 123.46,
                "id": 0
            },
            {
                "amount": 100,
                "id": 1
            },
            {
                "amount": 4920.34,
                "id": 2
            },
            {
                "amount": 12938,
                "id": 3
            },
            {
                "amount": 9238.02,
                "id": 4
            }
        ]
        self.assertEqual(data, expected)

    def test_get_payment_plans(self):
        data = self.paymentsAPI.get_payment_plans()
        expected = [
            {
                "amount_to_pay": 102.5,
                "debt_id": 0,
                "id": 0,
                "installment_amount": 51.25,
                "installment_frequency": "WEEKLY",
                "start_date": "2020-09-28"
            },
            {
                "amount_to_pay": 100,
                "debt_id": 1,
                "id": 1,
                "installment_amount": 25,
                "installment_frequency": "WEEKLY",
                "start_date": "2020-08-01"
            },
            {
                "amount_to_pay": 4920.34,
                "debt_id": 2,
                "id": 2,
                "installment_amount": 1230.085,
                "installment_frequency": "BI_WEEKLY",
                "start_date": "2020-01-01"
            },
            {
                "amount_to_pay": 4312.67,
                "debt_id": 3,
                "id": 3,
                "installment_amount": 1230.085,
                "installment_frequency": "WEEKLY",
                "start_date": "2020-08-01"
            }
        ]
        self.assertEqual(data, expected)

    def test_get_payments(self):
        data = self.paymentsAPI.get_payments()
        expected = [
            {
                "amount": 51.25,
                "date": "2020-09-29",
                "payment_plan_id": 0
            },
            {
                "amount": 51.25,
                "date": "2020-10-29",
                "payment_plan_id": 0
            },
            {
                "amount": 25,
                "date": "2020-08-08",
                "payment_plan_id": 1
            },
            {
                "amount": 25,
                "date": "2020-08-08",
                "payment_plan_id": 1
            },
            {
                "amount": 4312.67,
                "date": "2020-08-08",
                "payment_plan_id": 2
            },
            {
                "amount": 1230.085,
                "date": "2020-08-01",
                "payment_plan_id": 3
            },
            {
                "amount": 1230.085,
                "date": "2020-08-08",
                "payment_plan_id": 3
            },
            {
                "amount": 1230.085,
                "date": "2020-08-15",
                "payment_plan_id": 3
            }
        ]
        self.assertEqual(data, expected)

    def test_get_greater_date(self):
        date1 = '2020-09-28'
        date2 = '2020-09-29'
        data = self.paymentsProcessor.get_greater_date(date1, date2)
        expected = '2020-09-29'
        self.assertEqual(data, expected)

    def test_get_greater_date_empty_first(self):
        date1 = None
        date2 = '2020-09-29'
        data = self.paymentsProcessor.get_greater_date(date1, date2)
        expected = '2020-09-29'
        self.assertEqual(data, expected)

    def test_get_greater_date_empty_second(self):
        date2 = None
        date1 = '2020-09-29'
        data = self.paymentsProcessor.get_greater_date(date1, date2)
        expected = '2020-09-29'
        self.assertEqual(data, expected)

    def test_get_frequency_weekly(self):
        frequency = 'WEEKLY'
        data = self.paymentsProcessor.get_frequency_delta(frequency)
        expected = 7
        self.assertEqual(data, expected)

    def test_get_frequency_bi_weekly(self):
        frequency = 'BI_WEEKLY'
        data = self.paymentsProcessor.get_frequency_delta(frequency)
        expected = 14
        self.assertEqual(data, expected)

    def test_get_frequency_monthly(self):
        frequency = 'MONTHLY'
        data = self.paymentsProcessor.get_frequency_delta(frequency)
        expected = 30
        self.assertEqual(data, expected)

    def test_get_frequency_invalid(self):
        with self.assertRaises(Exception):
            frequency = 'INVALID'
            self.paymentsProcessor.get_frequency_delta(frequency)

    def test_add_data_to_payment_plans(self):
        payments = [
            {
                "amount": 25,
                "date": "2020-08-08",
                "payment_plan_id": 1
            },
            {
                "amount": 25,
                "date": "2020-08-08",
                "payment_plan_id": 1
            }
        ]
        debts = [
            {
                "amount": 150,
                "id": 1
            }
        ]
        payment_plans = {
            1: {
                "amount_to_pay": 100,
                "debt_id": 1,
                "id": 1,
                "installment_amount": 25,
                "installment_frequency": "WEEKLY",
                "start_date": "2020-08-01"
            }
        }
        self.paymentsProcessor.add_data_to_payment_plans(payments, payment_plans)
        expected = {
            1: {
                "amount_to_pay": 100,
                "debt_id": 1,
                "id": 1,
                "installment_amount": 25,
                "installment_frequency": "WEEKLY",
                "start_date": "2020-08-01",
                "amount_paid": 50,
                "last_payment_date": "2020-08-08"
            }
        }
        self.assertEqual(payment_plans, expected)
        self.paymentsProcessor.add_plan_and_payment_data_to_debts(debts, payment_plans)
        expected_2 = [
            {
                "amount": 150,
                "id": 1,
                "is_in_payment_plan": True,
                "remaining_amount": 50,
                "next_payment_due_date": "2020-08-15"
            }
        ]
        self.assertEqual(debts, expected_2)


class IntegrationTestCase(TestCase):
    def setUp(self):
        self.paymentsAPI = PaymentsAPI()
        self.paymentsProcessor = PaymentsProcessor(self.paymentsAPI)

    def test_integration(self):
        debts = self.paymentsProcessor.get_debts()
        expected = [
            {
                "amount": 123.46,
                "id": 0,
                "is_in_payment_plan": True,
                "remaining_amount": 0.0,
                "next_payment_due_date": None
            },
            {
                "amount": 100,
                "id": 1,
                "is_in_payment_plan": True,
                "remaining_amount": 50,
                "next_payment_due_date": "2020-08-15"
            },
            {
                "amount": 4920.34,
                "id": 2,
                "is_in_payment_plan": True,
                "remaining_amount": 607.6700000000001,
                "next_payment_due_date": "2020-08-22"
            },
            {
                "amount": 12938,
                "id": 3,
                "is_in_payment_plan": True,
                "remaining_amount": 622.415,
                "next_payment_due_date": "2020-08-22"
            },
            {
                "amount": 9238.02,
                "id": 4,
                "is_in_payment_plan": False,
                "remaining_amount": 9238.02,
                "next_payment_due_date": None
            }
        ]
        self.assertEqual(debts, expected)
        print(json.dumps(debts, indent=4))