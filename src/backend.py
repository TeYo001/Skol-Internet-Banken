### THIS IS WHERE THE INNER WORKINGS OF THE ACTUAL BANK PART OF THE PROJECT WILL BE ###

from src.external_imports import *

@dataclass
class Money:
    amount_kr: int
    # amount_ore: int # optional

class AccountType(Enum):
    SAVINGS = 0
    DEBIT = 1
    STOCK_FOND = 2

class AccountError(Enum):
    PANIC = 0
    

@dataclass
class Account:
    acc_type: AccountType
    name: str
    password_salt_hash: str
    acc_id: int
    money: Money
    interest: float

def login(name: str, password: str) -> Account | AccountError:
    ...

def logout():
    ...

def create_account(name: str, password: str) -> Account | AccountError:
    ...

def input_money(account: Account, amount: Money):
    ...

def withdraw_money(account: Account, amount: Money):
    ...

def transfer_money(src_account: Account, dest_account: Account, amount: Money):
    ...
