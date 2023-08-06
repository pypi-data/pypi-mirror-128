import pandas as pd
import numpy as np
import csv
from importlib import resources
import os
 
def load_csv (data_name, as_frame = False):
    """
        Load 'data_name' from the local library
        
        Parameters 
        ----------
        data_name : str
            Name of csv file to be loaded :
            'data_pelias.csv'
            'data.csv'
            'data2.csv'
            'id29-clientes-mapeado_consolidado.csv'
            'out.csv'
            'Tabela_abreviações.csv'

        as_frame : bool
            Load the data as a DataFrame.
            Default : dict

        Returns: 
        --------
        data : dict or DataFrame
            A container with the data
    """
    
    data_path = "GeoAPI/Data/" + data_name
    file_ = open(data_path, 'r')
    data = csv.reader(file_)
    columns = next(data)
    values = []
    for row in data :
        values.append(row)
    data_frame = pd.DataFrame(values, columns=columns)

    if as_frame :
        return data_frame
    else:
        dict_ = data_frame.to_dict()
        return dict_


if __name__ == "__main__":
    
    df = load_csv('data.csv',as_frame=True)