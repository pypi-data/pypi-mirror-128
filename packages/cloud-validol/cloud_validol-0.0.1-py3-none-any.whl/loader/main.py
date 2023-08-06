from lib import pg
from reports import prices


def main():
    engine = pg.get_engine()

    prices.update(engine)
