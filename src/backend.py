### THIS IS WHERE THE INNER WORKINGS OF THE ACTUAL BANK PART OF THE PROJECT WILL BE ###

from src.external_imports import *

@dataclass
class Money:
    ...

@dataclass
class Money:
    amount_kr: int
    # amount_ore: int # optional

    def __add__(self, amount: Money) -> Money:
        return Money(int(self.amount_kr + amount.amount_kr))

    def __sub__(self, amount: Money) -> Money:
        return Money(int(self.amount_kr - amount.amount_kr))

    def __mul__(self, amount: Money) -> Money:
        return Money(int(self.amount_kr * amount.amount_kr))

    def __lt__(self, amount: Money) -> Money:
        return self.amount_kr < amount.amount_kr

    def __gt__(self, amount: Money) -> Money:
        return self.amount_kr > amount.amount_kr

class AccountType(IntEnum):
    SAVINGS = 0
    DEBIT = 1
    STOCK_FOND = 2

class AccountError(Enum):
    PANIC = 0
    WRONG_PASSWORD = 1
    WRONG_NAME = 2
    NOT_LOGGED_IN = 3
    NOT_ENOUGH_MONEY = 4
    
@dataclass
class Account:
    acc_type: AccountType
    name: str
    password_salt_hash: str
    acc_id: int
    money: Money
    interest: float

@dataclass
class BankState:
    all_accounts: Dict[int, Account] # key = account_id
    bank_state_save_file_location: str
    salt_str: str
    next_account_id: int
    account_type_to_interest: Dict[AccountType, float]
    logged_in_account_id: int # -1 if not logged into any account

def init_bank() -> BankState:
    # NOTE(TeYo): currently just for testing
    account_type_to_interest = {
        AccountType.SAVINGS : 0.012,
        AccountType.DEBIT : 0.004,
        AccountType.STOCK_FOND : 0.0
    }
    bank = BankState(
        all_accounts=dict(), 
        bank_state_save_file_location="bank.save.txt",
        salt_str="123abc",
        next_account_id=0,
        account_type_to_interest=account_type_to_interest,
        logged_in_account_id=-1)
    return bank

### GLOBAL STATE ###
# NOTE(TeYo): Just for simplicity (might change later if it becomes a problem)

bank = init_bank()

def login(name: str, password: str) -> Account | AccountError:
    global bank
    password_hash = hashlib.sha256((bank.salt_str+password).encode()).hexdigest()
    for id, account in bank.all_accounts.items():
        if name != account.name:
            continue
        if password_hash != account.password_salt_hash:
            return AccountError.WRONG_PASSWORD

        bank.logged_in_account_id = id
        return account
    return AccountError.WRONG_NAME

def logout():
    global bank
    bank.logged_in_account_id = -1

def create_account(name: str, password: str, acc_type: AccountType) -> Account | AccountError:
    global bank
    # TODO(TeYo): add error checking and name and password restrictions / requirements
    acc_id = bank.next_account_id
    bank.next_account_id += 1
    account = Account(
        acc_type=acc_type,
        name=name,
        password_salt_hash=hashlib.sha256((bank.salt_str+password).encode()).hexdigest(),
        acc_id=acc_id,
        money=Money(0),
        interest=bank.account_type_to_interest[acc_type])
    bank.all_accounts[acc_id] = account
    return account

def input_money(account: Account, amount: Money) -> None | AccountError:
    global bank
    if bank.logged_in_account_id != account.acc_id:
        return AccountError.NOT_LOGGED_IN
    account.money += amount

def withdraw_money(account: Account, amount: Money) -> None | AccountError:
    global bank
    if bank.logged_in_account_id != account.acc_id:
        return AccountError.NOT_LOGGED_IN
    if account.money < amount:
        return AccountError.NOT_ENOUGH_MONEY
    account.money -= amount

def transfer_money(src_account: Account, dest_account: Account, amount: Money) -> None | AccountError:
    global bank
    if bank.logged_in_account_id != src_account.acc_id:
        return AccountError.NOT_LOGGED_IN
    if src_account.money < amount:
        return AccountError.NOT_ENOUGH_MONEY
    src_account.money -= amount
    dest_account.money += amount

def get_current_account() -> Account | AccountError:
    global bank
    if bank.logged_in_account_id == -1:
        return AccountError.NOT_LOGGED_IN
    return bank.all_accounts[bank.logged_in_account_id]

def get_account_from_name(account_name: str) -> Account | AccountError:
    global bank
    for id, account in bank.all_accounts.items():
        if account_name != account.name:
            continue
        return account
    return AccountError.WRONG_NAME

# NOTE(TeYo): could replace with __repr__, but I generally don't like that way of doing things
def account_to_save_str(account: Account) -> str:
    type_str = str(int(account.acc_type))
    return f"#{type_str}|{account.name}|{account.password_salt_hash}|{account.acc_id}|{account.money.amount_kr}|{account.interest};"

def save_str_to_account(save_str: str) -> Account:
    # TODO(TeYo): perhaps add some error handling where you return the error
    element_strs = save_str[1:len(save_str)-1].split("|")
    if len(element_strs) != 6:
        print("FIX THIS!")
        exit(1)
    return Account(acc_type=AccountType(int(element_strs[0])),
                   name=element_strs[1],
                   password_salt_hash=element_strs[2],
                   acc_id=int(element_strs[3]),
                   money=Money(int(element_strs[4])),
                   interest=float(element_strs[5]))

# TODO(TeYo): add error handling here too
def load_bank():
    global bank
    account_strs = None
    account_count = 0
    try:
        with open(bank.bank_state_save_file_location, "r+") as file:
            account_strs = file.read()
    except FileNotFoundError as error:
        return
    account_index_ranges = []
    search_idx = 0
    while True:
        try:
            start_idx = account_strs.index("#", search_idx, len(account_strs))
            end_idx = account_strs.index(";", start_idx, len(account_strs))
            account_index_ranges.append((start_idx, end_idx))
            search_idx = start_idx+1
        except ValueError as error:
            break
    for start_idx, end_idx in account_index_ranges:
        save_str = account_strs[start_idx:end_idx+1]
        account = save_str_to_account(save_str)
        bank.all_accounts[account.acc_id] = account

# TODO(TeYo): errors need handling
def save_bank():
    global bank
    account_strs = ""
    for account in bank.all_accounts.values():
        account_strs += account_to_save_str(account)
    with open(bank.bank_state_save_file_location, "w+") as file:
        file.write(account_strs)


