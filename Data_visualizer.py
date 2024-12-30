import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from Cortellis_data_processor import status_to_number
from Cortellis_data_processor import number_to_status
from Cortellis_data_processor import status_mapper

data_path = 'drug_vs_indication_clinical.csv'
data = pd.read_csv(data_path)

def digitalize_data(values):
    shape = values.shape
    values_unrolled = values.ravel()
    digitalized_values_unrolled = np.array(status_to_number(values_unrolled, status_mapper))
    digitalized_values = digitalized_values_unrolled.reshape(shape)
    return digitalized_values
