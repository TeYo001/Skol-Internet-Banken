# Plannerings Rapport

## Uppiften
Programmera en internetbank i python. Internetbanken ska innehålla liknande funktioner som en riktig internetbank. 
Till exempel möjlighet att skapa bankkonton, uttag/överföringar, konstant ränta på sparkonton, slumpad ränta på aktiefond konton, visualisering av förändring i saldo med hjälp av graffunktioner, med mera.

## Strategi och utförande
Delat "repository" på hemsidan GitHub, där det enkelt går att se varandras koder samt göra ändringar. Skriver en större del av koden innan vi börjar skriva på rapporten. 

## Rollfördelning
Huvudprogrammerare Teo, Programmerare Tobias, Programmerare Boo. 

## Kommunikation
Whatsapp och Zoom.

## Källmaterial
Föreläsningar som givits under kursen. Eventuell dokumentation från användarbibliotek. 

## Tidplan 
Arbeta på projektet under eftermiddagarna 2-3 gånger i veckan. Eventuellt få feedback vid

## Pseudo Kod

### Backend
```python
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
```

### Menu

```python
class MenuStateType(Enum):
    IDLE = 0

@dataclass
class MenuState:
    ...

@dataclass
class MenuState:
    state_type: MenuStateType
    valid_state_transitions: list[MenuStateType]
    state_transition_array: list[Callable[[MenuState], bool]]
    

# state machine
class MenuStateMachine:
    def __init__(self):
        self.all_states = []
        self.current_state_type = MenuStateType.IDLE
        self.current_state_info = MenuState
        self.valid_state_change_array = []

    def add_state(self, state: MenuState) -> bool:
        ...

    def change_state(self, state: MenuStateType) -> bool:
        ...

# initializes the menu state machine
def menu_init() -> MenuStateMachine:
    ...

def menu_start():
    ...

def menu_input_money():
    ...

def menu_withdraw_money():
    ...

def menu_transfer_money():
    ...

def menu_login():
    ...

def menu_logout():
    ...

def menu_create_account():
    ...

# where the account is visualized and where you can choose what to do once logged in
def menu_view_account():
    ...
```
