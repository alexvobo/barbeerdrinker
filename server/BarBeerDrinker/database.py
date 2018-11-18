
from sqlalchemy import create_engine
from sqlalchemy import sql
from BarBeerDrinker import config

engine = create_engine(config.database_uri)

def get_bars():
    with engine.connect() as con:
        rs = con.execute("SELECT Bar_Name, Bar_License, Bar_City, Bar_Phone_Number, Bar_Address FROM Bar;")
        return [dict(row) for row in rs]

def find_bar(name):
    with engine.connect() as con:
        query = sql.text(
            "SELECT Bar_Name, Bar_License, Bar_City, Bar_Phone, Bar_Address FROM Bar WHERE name = :name;"
        )

        rs = con.execute(query, name=name)
        result = rs.first()
        if result is None:
            return None
        return dict(result)

def filter_beers(max_price):
    with engine.connect() as con:
        query = sql.text(
            "SELECT * FROM Sells WHERE Price < :max_price;"
        )

        rs = con.execute(query, max_price=max_price)
        results = [dict(row) for row in rs]
        for r in results:
            r['Price'] = float(r['Price'])
        return results


def get_bar_menu(bar_name):
    with engine.connect() as con:
        query = sql.text(
            'SELECT a.Bar_Name, a.Beer_Name, a.Price, b.Beer_Origin, coalesce(c.like_count, 0) as Likes \
                FROM Sells as a \
                JOIN Beer AS b \
                ON a.Beer_Name = b.Beer_Name \
                LEFT OUTER JOIN (SELECT Beer_Name, count(*) as like_count FROM Likes GROUP BY Beer_Name) as c \
                ON a.Beer_Name = c.Beer_Name \
                WHERE a.Bar_Name = :bar; \
            ')
        rs = con.execute(query, bar=bar_name)
        results = [dict(row) for row in rs]
        for i, _ in enumerate(results):
            results[i]['Price'] = float(results[i]['Price'])
        return results


def get_bars_selling(beer):
    with engine.connect() as con:
        query = sql.text('SELECT a.Bar_Name, a.Price, b.customers \
                FROM sells AS a \
                JOIN (SELECT Bar_Name, count(*) AS customers FROM Frequents GROUP BY Bar_Name) as b \
                ON a.Bar_Name = b.Bar_Name \
                WHERE a.Beer_Name = :beer \
                ORDER BY a.Price; \
            ')
        rs = con.execute(query, beer=beer)
        results = [dict(row) for row in rs]
        for i, _ in enumerate(results):
            results[i]['Price'] = float(results[i]['Price'])
        return results


def get_bar_frequent_counts():
    with engine.connect() as con:
        query = sql.text('SELECT Bar_Name, count(*) as frequentCount \
                FROM Frequents \
                GROUP BY Bar_Name; \
            ')
        rs = con.execute(query)
        results = [dict(row) for row in rs]
        return results


def get_bar_cities():
    with engine.connect() as con:
        rs = con.execute('SELECT DISTINCT Bar_City FROM Bar;')
        return [row['Bar_City'] for row in rs]


def get_beers():
    """Gets a list of beer names from the beers table."""

    with engine.connect() as con:
        rs = con.execute('SELECT  Beer_Name, Beer_Origin FROM Beer;')
        return [dict(row) for row in rs]


def get_beer_manufacturers(beer):
    with engine.connect() as con:
        if beer is None:
            rs = con.execute('SELECT DISTINCT Beer_Origin FROM Beer;')
            return [row['Beer_Origin'] for row in rs]

        query = sql.text('SELECT Beer_Origin FROM Beer WHERE Beer_Name = :beer;')
        rs = con.execute(query, beer=beer)
        result = rs.first()
        if result is None:
            return None
        return result['Beer_Origin']


def get_drinkers():
    with engine.connect() as con:
        rs = con.execute('SELECT Drinker_Name, Drinker_City, Drinker_Phone_Number, Drinker_Address FROM Drinker;')
        return [dict(row) for row in rs]


def get_likes(drinker_name):
    """Gets a list of beers liked by the drinker provided."""

    with engine.connect() as con:
        query = sql.text('SELECT Beer_Name FROM Likes WHERE Drinker_Name = :name;')
        rs = con.execute(query, name=drinker_name)
        return [row['Beer_Name'] for row in rs]


def get_drinker_info(drinker_name):
    with engine.connect() as con:
        query = sql.text('SELECT * FROM Drinker WHERE Drinker_Name = :name;')
        rs = con.execute(query, name=drinker_name)
        result = rs.first()
        if result is None:
            return None
        return dict(result)