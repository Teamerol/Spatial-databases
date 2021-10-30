from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric
from geoalchemy2 import Geometry
from sqlalchemy.sql.elements import and_

#Подключение к базе данных
# !!! Обязательно заменить password на пароль пользователя postgres !!!
parameters = "postgresql://postgres:password@localhost/postgres"
connection = create_engine(parameters)

#Создание сессии
Session = sessionmaker(bind=connection)
session = Session()

#Декларативное объявление таблиц
Base = declarative_base()

class Points(Base):
    __tablename__ = "Extracted_points"
    id = Column("id", Integer, primary_key=True)
    geom = Column("geom", Geometry("POINT", srid=32639))
    pid = Column("pid", Integer)
    family = Column("family", String)
    genus = Column("genus", String)
    species = Column("species", String)
    day = Column("day", Integer)
    month = Column("month", Integer)
    year = Column("year", Integer)
    region = Column("region", String)
    latitude = Column("latitude", Numeric)
    longitude = Column("longitude", Numeric)
    herbary = Column("herbary", String)

class Borders(Base):
    __tablename__ = "Komi_district_borders"
    id = Column("id", Integer, primary_key=True)
    geom = Column("geom", Geometry("POLYGON", srid=32639))
    osm_id = Column("osm_id", Numeric)
    name = Column("name", String)
    admin_lvl = Column("admin_lvl", String)


#Запрос
results = session.query(Points.family).\
    filter(Borders.name == 'Койгородский район').\
        filter(Points.geom.St_Within(Borders.geom)).\
            order_by(Points.family).\
                distinct(Points.family)

for result in results:
    print(result.family)
