from datetime import datetime, timedelta
from .utils.paymentsAPI import PaymentsAPI

__all__ = ['PaymentsProcessor']


class PaymentsProcessor:
    def __init__(self, paymentsAPI=None):
        """
        :param paymentsAPI: PaymentsAPI | None - If None, a new PaymentsAPI will be created, else inherit from caller
        """
        self.paymentsAPI = paymentsAPI or PaymentsAPI()

    @staticmethod
    def get_frequency_delta(frequency):
        if frequency == 'WEEKLY':
            return 7
        if frequency == 'BI_WEEKLY':
            return 14
        if frequency == 'MONTHLY':
            return 30
        raise Exception('Invalid frequency')

    @staticmethod
    def get_greater_date(first_date, second_date):
        if first_date is None:
            return second_date
        if second_date is None:
            return first_date

        return max([first_date, second_date])

    @staticmethod
    def get_next_payment_due_date(debt_id, plans_by_debt_id):
        plan = plans_by_debt_id.get(debt_id)
        if not plan:
            return None
        frequency = PaymentsProcessor.get_frequency_delta(plan['installment_frequency'])
        comparison_date = datetime.strptime(plan['start_date'], '%Y-%m-%d')
        last_payment_date = plan.get('last_payment_date')
        if last_payment_date:
            last_payment_date = datetime.strptime(last_payment_date, '%Y-%m-%d')
            comparison_date = PaymentsProcessor.get_greater_date(comparison_date, last_payment_date)
        next_payment_due_date = comparison_date + timedelta(frequency)
        return next_payment_due_date.strftime('%Y-%m-%d')

    @staticmethod
    def add_data_to_payment_plans(payments, plans_by_debt_id):
        for payment in payments:
            plan = plans_by_debt_id.get(payment['payment_plan_id'])
            if plan:
                if not plan.get('amount_paid'):
                    plan['amount_paid'] = 0
                plan['amount_paid'] += payment['amount']

                if not plan.get('last_payment_date'):
                    plan['last_payment_date'] = payment['date']
                else:
                    plan['last_payment_date'] = PaymentsProcessor.get_greater_date(
                        datetime.strptime(plan['last_payment_date'], '%Y-%m-%d'),
                        datetime.strptime(payment['date'], '%Y-%m-%d')
                    ).strftime('%Y-%m-%d')

    def add_plan_and_payment_data_to_debts(self, debts, plans_by_debt_id):
        for debt in debts:
            if debt['id'] in plans_by_debt_id:
                debt['is_in_payment_plan'] = True
                amount_to_pay = plans_by_debt_id[debt['id']]['amount_to_pay']
                amount_paid = plans_by_debt_id[debt['id']].get('amount_paid', 0)
                debt['remaining_amount'] = amount_to_pay - amount_paid
            else:
                debt['is_in_payment_plan'] = False
                debt['remaining_amount'] = debt['amount']

            if debt['remaining_amount'] <= 0:
                debt['next_payment_due_date'] = None
            else:
                debt['next_payment_due_date'] = self.get_next_payment_due_date(debt['id'], plans_by_debt_id)

    def get_debts(self):
        debts = self.paymentsAPI.get_debts()
        plans = self.paymentsAPI.get_payment_plans()
        payments = self.paymentsAPI.get_payments()

        plans_by_debt_id = {plan['debt_id']: plan for plan in plans}
        self.add_data_to_payment_plans(payments, plans_by_debt_id)
        self.add_plan_and_payment_data_to_debts(debts, plans_by_debt_id)

        return debts
