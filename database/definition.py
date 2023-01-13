"""
Here we use SQLAlchemy to define an astraction layer to SQL.
This design choice was motivated by the need to perform complex calculations on the data output by the SQL queries in Python.
For example, PostgreSQL can not:
- Train neural networks
- Perform cross validation to determine optimal knots in a spline
- Integrate with other APIs for web portals or SSH Tunneling

SQLAlchemy allows easy access to important CRUD features, especially with Pandas
Using SQLAlchemy we may read data using Pandas.read_sql() and output using Pandas.to_sql().

If one really wants to know the raw SQL to run, use query.compile().

SQLAlchemy has a number of ways to define a database.
In this module I use the Object Relational Mapper (ORM) method.
This treats tables and schemas like Python classes.

The organizing structure for the database is as follows:

Site <- Building <- Meter

Hence, we can construct a Directed Acyclic Graph (DAG) to model the relations between our data.
We then use the PostgreSQL extension LTree to model the relations. This extension allows us to efficiently answer queries like:

- What are all the buildings belonging to a group?
- What are all the meters belonging to a building?
- If a building has non-null data for all its meters, then return the sum, otherwise return NULL.
"""
import os
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Optional
from sqlalchemy import Column, Integer, String, ForeignKey, Index, func
from sqlalchemy.orm import declarative_base, relationship, remote, foreign
from sqlalchemy_utils import LtreeType, Ltree

Base = declarative_base()


class Site(Base):
    """
    Sourced from Aurora at BluePillar.
    GET ../API/V1/filters -> Unique Sites
    """
    __tablename__ = 'site'

    site_name = Column(String(255), primary_key=True)
    site_id = Column(String(255))
    path = Column(LtreeType, nullable=False)
    parent = relationship(
        'Meter',
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref='children',
        viewonly=True,)
    __table_args__ = (Index('ix_nodes_path', path, postgresql_using='gist'),)

    def __str__(self):
        return self.meter_id

    def __repr__(self):
        return 'campus({})'.format(self.campus_id)

class Building(Base):
    """
    Sourced from Aurora at BluePillar.
    GET ../API/V1/filters -> Unique Buildings
    """
    __tablename__ = 'building_complex'

    building_complex_id = Column(String(255), primary_key=True)
    campus = Column(String(255), nullable=False)
    path = Column(LtreeType, nullable=False)
    parent = relationship(
        'Meter',
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref='children',
        viewonly=True,)
    __table_args__ = (Index('ix_nodes_path', path, postgresql_using='gist'),)

    def __str__(self):
        return self.building_complex_id

    def __repr__(self):
        return 'BuildingComplex({})'.format(self.building_complex_id)

class Meter(Base):
    """
    Obtained from Aurora.
    GET ../API/V1/filters -> Unique Meters
    """
    __tablename__ = 'meter'

    meter_id = Column(String(255), primary_key=True)
    building_id = Column(String(255), nullable=False)
    
    path = Column(LtreeType, nullable=False)
    parent = relationship(
        'Meter',
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref='children',
        viewonly=True,)
    __table_args__ = (Index('ix_nodes_path', path, postgresql_using='gist'),)

    def __str__(self):
        return self.meter_id

    def __repr__(self):
        return 'Meter({})'.format(self.meter_id)

class Kw(Base):
    """
    Obtained from Aurora.
    GET ../API/V1/filter/{filter_id}/historical
    """
    __tablename__ = 'kw'

    meter_id = Column(String(255), primary_key=True)
    building_id = Column(String(255), nullable=False)
    
    path = Column(LtreeType, nullable=False)
    parent = relationship(
        'Meter',
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref='children',
        viewonly=True,)
    __table_args__ = (Index('ix_nodes_path', path, postgresql_using='gist'),)

    def __str__(self):
        return self.meter_id

    def __repr__(self):
        return 'Meter({})'.format(self.meter_id)

class Kwh(Base):
    """
    Obtained from Aurora.
    GET ../API/V1/filter/{filter_id}/historical
    """
    __tablename__ = 'kwh'

    meter_id = Column(String(255), primary_key=True)
    building_id = Column(String(255), nullable=False)
    
    path = Column(LtreeType, nullable=False)
    parent = relationship(
        'Meter',
        primaryjoin=remote(path) == foreign(func.subpath(path, 0, -1)),
        backref='children',
        viewonly=True,)
    __table_args__ = (Index('ix_nodes_path', path, postgresql_using='gist'),)

    def __str__(self):
        return self.meter_id

    def __repr__(self):
        return 'Meter({})'.format(self.meter_id)
