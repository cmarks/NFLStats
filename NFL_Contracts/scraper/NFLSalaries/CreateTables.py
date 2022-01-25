from sqlalchemy import create_engine  
from sqlalchemy import Table, Column, String, MetaData, Integer

db_string = "postgresql://postgres:postgres@localhost:5432/nfl"

db = create_engine(db_string)

meta = MetaData(db)  
contract_table = Table('contracts', meta,  
                       Column('player', String),
                       Column('team', String),
                       Column('age', String),
                       Column('total_value', Integer),
                       Column('avg_year', Integer),
                       Column('total_guaranteed', Integer),
                       Column('fully_guaranteed', Integer),
                       Column('free_agency_year', String),
                       Column('free_agency_type', String))

with db.connect() as conn:

    # Create
    contract_table.create()
    # insert_statement = film_table.insert().values(title="Doctor Strange", director="Scott Derrickson", year="2016")
    # conn.execute(insert_statement)

    # Read
    # select_statement = film_table.select()
    # result_set = conn.execute(select_statement)
    # for r in result_set:
    #     print(r)

    # Update
    # update_statement = film_table.update().where(film_table.c.year=="2016").values(title = "Some2016Film")
    # conn.execute(update_statement)

    # Delete
    # delete_statement = film_table.delete().where(film_table.c.year == "2016")
    # conn.execute(delete_statement)