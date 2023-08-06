import pandas as pd
from textattack.datasets import Dataset


def dataframe_to_NLPDset(df, input_col_name, label_col_name):
    '''
    Takes in a dataframe and makes a textattack dataset.
    '''
    dset = []
    inputs = df[input_col_name].tolist()
    labels = df[label_col_name].tolist()
    for idx in range(len(inputs)):
        dpoint = (inputs[idx], labels[idx])
        dset.append(dpoint)
    dataset = Dataset(dset)
    return dataset