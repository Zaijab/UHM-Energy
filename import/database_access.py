"""
Import data using SQL Commands.

Store queries in $XDG_CACHE_HOME/uhm_campus_energy/{query_name}.pkl
"""
import os
from sshtunnel import SSHTunnelForwarder
from sqlalchemy import create_engine
from sqlalchemy import Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

"""
The following line will be used to store user credentials into variables.
The credentials will then be used to log into the server housing the PostgreSQL database.

Our current database uses SSH to log onto the server then to login to the PostgreSQL from there.

Please store your username and passwords responsibly.
This script assumes the credentials are stored in the UNIX Passwordstore encrypted with the users GPG Key Pair.
"""
user, password, postgres_address, ssh_address = os.popen('pass show postgres').read().split()
server = SSHTunnelForwarder(
    (ssh_address.split(':')[0], int(ssh_address.split(':')[1])),
    ssh_username=user,
    ssh_password=password,
    remote_bind_address=('127.0.0.1', int(postgres_address.split(':')[1])))

# Login and execute
with server as tunnel:
    engine = create_engine(f'postgresql://{user}:{password}@127.0.0.1:{str(server.local_bind_port)}/zain')
