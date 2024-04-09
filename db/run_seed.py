'''This module contains the logic to seed the development databases
for the `Cat's Rare Treasures` FastAPI app.'''
from seed import seed_db


def main() -> None:
    '''This function runs the `seed_db` function'''
    seed_db()


if __name__ == "__main__":
    main()
