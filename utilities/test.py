import access
import pandas as pd

database_inst = database()
power_average = pd.read_sql("SELECT * FROM aurora.power_average", database_inst.engine)
