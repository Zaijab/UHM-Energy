"""
Here we use SQLAlchemy to define an astraction layer to SQL.
This design choice was motivated by the need to perform complex calculations on the data output by the SQL queries in Python.
PostgreSQL could not train neural networks, perform cross validation to determin optimal knots in a spline, or integration with other libraries like web portals or SSH Tunneling.
I can then input queries (Selectable objects) directly using Pandas.read_sql() and output using Pandas.to_sql().
If one really wants to know the raw SQL to run, use query.compile().

SQLAlchemy has a number of ways to define a database.
In this module I use the Object Relational Mapper (ORM) method.
This treats tables and schemas like Python classes.

Here is the organizing structure for the database.
Meters belong to buildings which belong to building groups.
Sub meters belong to main meters.

Hence, we can construct a Directed Acyclic Graph (DAG) to model the relations between our data.
We then use the PostgreSQL extension LTree to model the relations. This extension allows us to efficiently answer queries like:

- What are all the buildings belonging to a group?
- What are all the meters belonging to a building?
- If a building has non-null data for all its meters, then return the sum, otherwise return NULL.
"""

from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class Base(DeclarativeBase):
    pass

# Meters has a heirarchical system of main vs sub meters
# LTree is an extension to PostgreSQL which represents tree-like structures

# Define the nodes of the tree
class Meters(Base):
    __tablename__ = "meters"
    id: Mapped[int] = mapped_column(primary_key=True)
    building: Mapped[int]
    name: Mapped[str] = mapped_column(String(255))

# Define the paths in the tree
class Meter_Types(Base):
    __tablename__ = "meter_types"
    sub_id: Mapped[int]
    main_id: Mapped[int]

# Similarly, for buildings
# Define the nodes (each building)
class Buildings(Base):
    pass

# Define the meters belonging to a building
class Meters_Buildings(Base):
    pass

class Buildings_Complexes(Base):
    pass

