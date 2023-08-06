from cloud_validol.loader.lib import pg
from cloud_validol.loader.reports import prices


def main():
    engine = pg.get_engine()

    prices.update(engine)
