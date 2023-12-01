'''This module contains the logic to seed the development databases
for the `Cat's Rare Treasures` FastAPI app.'''
from seed import seed_db
from subprocess import run


def main() -> None:
    '''This function runs the `setup_dbs` SQL script
    and the `seed_db` function'''
    # Create test and dev databases
    run('psql -f db/setup_dbs.sql', shell=True)
    seed_db()


if __name__ == "__main__":
    main()
