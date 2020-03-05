# %% [markdown]
# ## Exploratory Analysis

# %%
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt # plotting
import numpy as np # linear algebra
import os # accessing directory structure
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# %% [markdown]
# There are 4 csv files in the current version of the dataset:
# 

# %%
for dirname, _, filenames in os.walk('data'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# %%
tier_1_champs = pd.read_csv("data/Tier-1.csv")
print(tier_1_champs.head())

# %% [markdown]
# Looking at some of the NaN values and comparing to tftactics.gg, it seems like there is information that is available but is missing from these files, I'll probably have to add it manually (building a scraper would probably take too much time)
#
# In other news set 3 champions are on tftactics.gg, so that is good, I should build two separate csvs for each thing probably
# Actually I'll just copy and modify the CSVs when the new set comes out
## Apparently there is the new champions here: https://app.mobalytics.gg/tft/set3/champions/annie
#
# TODO I might want to add crit rate at somepoint?

# %%
