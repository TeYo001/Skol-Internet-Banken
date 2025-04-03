# the bank

from src.backend import *
from src.menu import *
from src.render import *


# TODO(TeYo)
# Skapa konton
# Ränta (konstant på spar)
# Avkastning (slump ränta) på aktiefond

def main():
    menu = menu_init()
    menu_run(menu)

if __name__ == "__main__":
    main()
