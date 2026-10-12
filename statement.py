from datetime import datetime
from utils import normalize

class Statement:
    def __init__(self, id_:str, date:str, description: str, debit: str, credit: str, balance: str):
        self.id = id_
        self.date = datetime.strptime(date, '%Y-%m-%d').date()
        self.description = description
        self.debit = float(debit) if debit else None
        self.credit = float(credit) if credit else None
        self.balance = float(balance)

        self.amount = self.debit if self.debit is not None else self.credit
        self.direction = 'out' if self.debit is not None else 'in'
        self.merchant_key = normalize(description)