#!/usr/bin/env python
# coding: utf-8

# <h1><center>Języki Programowania w Analize Danych</center></h1>
# <h3><center><ul style="list-style: none;">
#     <li>Mateusz Gałasiński 234054</li>
#     <li>Jakub Kurek 234078</li>
#     </ul></center></h3> 
# <h2><center>Zadanie 1 - Analiza statystyczna dla wybranego zbioru danych</center></h2>

# ### Additional setup

# In[1]:


# install additional packages
get_ipython().system('pip install k3d > /dev/null')
get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


from pathlib import Path
import numpy as np
from matplotlib import pyplot as pypl
from pandas import read_csv
import json


# ## Configuration

# In[3]:


class Config(object):
    def __init__(self, dataSourceUrl, quantitativeColumns, qualitativeColumns):
        self.dataSourceUrl = dataSourceUrl
        self.quantitativeColumns = quantitativeColumns
        self.qualitativeColumns = qualitativeColumns
def as_config(dct):
    return Config(
        dct['dataSourceUrl'],
        dct['quantitativeColumns'],
        dct['qualitativeColumns'],)
json_config ="""
{
    "dataSourceUrl": "/home/jovyan/host-note/fertility_Diagnosis.data",
    "quantitativeColumns": [
        "season",
        "childish_disease", 
        "accident_trauma", 
        "surgical_treatmnent",
        "fevers", 
        "alcohol_consumption", 
        "smoking_habit", 
        "output_diagnosis"
    ],
    "qualitativeColumns": [
        "age", 
        "hours_sitting"
    ]
}"""
config = json.loads(json_config, object_hook = as_config)


# ## Data description

# In[4]:


for line in [line for line in Path('/home/jovyan/host-note/fertility_Diagnosis.names').read_text().splitlines() if line]:
    print(line)


# ## Divide into qualitative and quantitative

# In[5]:


dataset = read_csv(config.dataSourceUrl, header=0)
qualitativeDataset = dataset[config.qualitativeColumns]
quantitativeDataset = dataset[config.quantitativeColumns]
dataset.shape


# ## 1. Describe
# *Dla poszczególnych atrybutów wyznaczyć medianę, minimum i maximum dla cech ilościowych i dominantę dla cech jakościowych.*

# In[6]:


qualitativeDataset.describe()


# ### Modes

# In[7]:


qualitativeDataset.mode()


# ## 2. Correlation matrix
# *Narysować histogramy dla dwóch cech ilościowych najbardziej ze sobą skorelowanych*

# In[8]:


qualitativeDataset.corr()


# ### Histogram for attributes with highest correlation
# 

# In[9]:


corr = qualitativeDataset.corr()
max = -2
c, r = "", ""
for column in corr:
    for row in corr:
        if row != column and np.absolute(corr[column][row]) > max:
            max = np.absolute(corr[column][row])
            c = column
            r = row
hist = qualitativeDataset.hist(column=[c, r])


# # Births

# *Dla danych Births zbadać hipotezę, że dzienna średnia liczba urodzeń dzieci wynosi: 10000  
# (poziom istotności statystycznej 5%)*

# In[10]:


from calendar import isleap
from scipy.stats import t
hypothesis_z = 1000_0
alpha = 0.05
column_name = "births"
data = read_csv("/home/jovyan/host-note/births.csv", header=0)
num_of_days = data['year'].unique().size * 365 + np.sum(np.array(list(map(lambda y: isleap(y), data['year'].unique()))))
mean_b = data[column_name].sum() / num_of_days
print(f"Średnia ilość urodzeń w ciagu dnia to: {mean_b}")
std_b = data[column_name].std()
print(f"Odchylenie standardowe ilości urodzeń w ciagu dnia to: {std_b}")
tperc_b = t.ppf(1 - alpha/2, data['births'].count()-1)
print(f"Wartość krytyczna: {tperc_b}")
b_max = mean_b + tperc_b*std_b/(np.sqrt(data[column_name].count()))
b_min = mean_b - tperc_b*std_b/(np.sqrt(data[column_name].count()))
print(f"{b_min} – {b_max}")

if not (hypothesis_z > b_min and hypothesis_z < b_max):
    print(f"Hypothesis that mean {column_name} is {hypothesis_z} with confidence: {1 - alpha}% is false!")
else:
    print("Hyopthesis is correct !")

fig = pypl.figure()
ax = fig.add_subplot(1,1,1)
ax.set_title("Births h")
data.hist(column=[column_name], ax=ax)
pypl.axvline(x=b_min, linestyle='--', color='red')
pypl.axvline(x=b_max, linestyle='--', color='red')
lin = pypl.axvline(x=hypothesis_z, linestyle='--', color='purple')

