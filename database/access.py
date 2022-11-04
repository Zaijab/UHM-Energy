"""
A frontend to the UH PostgreSQL Server.

Defines the following:
- Boilerplate code to access the server
- Funcitons to populate the database
- Functions to extract data

This module assumes user credentials are stored in the UNIX Passwordstore encrypted with a GPG Key Pair.
Please store username and passwords responsibly.
"""
import os
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class database():
    """
    __init__ will use the UNIX Passwordstore to grab user credentials.
    The credentials will then be used to log into the server housing the PostgreSQL database.
    
    Our current database uses SSH to log onto the server then to login to the PostgreSQL from there.
    """
    def __init__(self):
        user, password, postgres_address, ssh_address = os.popen('pass show postgres').read().split()
        server = SSHTunnelForwarder(
            (ssh_address.split(':')[0], int(ssh_address.split(':')[1])),
            ssh_username=user,
            ssh_password=password,
            remote_bind_address=('127.0.0.1', int(postgres_address.split(':')[1])))
    
        """
        Using the Login information as before, tunnel into the server using SSH.
        Create the PostgreSQL engine, and construct a session.
        """
        with server as tunnel:    
            engine = create_engine(f'postgresql://{user}:{password}@127.0.0.1:{str(server.local_bind_port)}/zain')
            self.session = sessionmaker(bind=engine)()
        return None
    
    """
    Input: A query string or text file
    Output: A Pandas DataFrame
    
    This function is cached by default.
    Python will search for a {HASH_OF_QUERY_STRING}.pkl file to load from in the .cache directory.
    
    I do not use the @cache annotation as this type of caching is intended to persist.
    """
    def query(self, query, cache = True):
        return None
    
    """
    Define the database using the SQLAlchemy ORM using DBName.
    Define tables and schemas from `definition.py`.
    """
    def bootstrap(self):
        return None
    
    """
    Append data from Aurora at BluePillar API to existing tables in the database.
    
    Input: Pandas DataFrame, Path to CSV, or CSV file object
    Output: None
    """
    def append(self):
        return None
