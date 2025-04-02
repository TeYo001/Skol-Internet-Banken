# the bank

from src.backend import *
from src.menu import *
from src.render import *


# TODO(TeYo)
# Skapa konton
# Ränta (konstant på spar)
# Avkastning (slump ränta) på aktiefond

def main():
    # Note(TeYo): Just for testing
    money = Money(100)
    print(f"money: {money.amount_kr}")

if __name__ == "__main__":
    main()
