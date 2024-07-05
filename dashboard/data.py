import pandas as pd
from pymongo import MongoClient
import numpy as np

def get_data_from_mongodb():
    client = MongoClient('mongodb://mongo:27017')
    db = client['Database_Etudiant']
    collection = db['lycee']
    data = list(collection.find({}))
    # Convert the data to a pandas DataFrame
    dataframe = pd.DataFrame(data)
    dataframe.replace('', np.nan, inplace=True)
    return dataframe
