from datetime import datetime
from utils import normalize

class Alert:
    def __init__(self, id_:str, source:str, received_at:str, account:str, direction:str, amount:str, merchant:str, ref: str):
        self.id = id_
        self.source = source
        self.received_at = datetime.strptime(received_at, '%Y-%m-%d %H:%M')
        self.account = account
        self.direction = direction
        self.amount = float(amount)
        self.merchant = merchant
        self.ref = ref if ref else None

        self.merchant_key = normalize(merchant)
