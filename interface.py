import streamlit as st
import numpy as np
import pandas as pd
import os

champions = pd.read_csv(os.getcwd() + "\\data\\champion_info_scrape.csv")
# st.write(champions[champions["name"].str.match("Gangplank")]["name"])

champions_inventory = pd.read_csv(os.getcwd() + "\\cache\\champ_list.csv")
store = pd.read_csv(os.getcwd() + "\\cache\\store.csv")

clear = st.button("Clear data")
if clear:
    champions_inventory = pd.DataFrame(columns = ["name"])
    store = pd.DataFrame(columns = ["name", "cost"])

# st.show(champions)

list_all = st.checkbox("Show all champions")

def champion_button(name):
    global store
    select = st.button(name)
    if select:
        row = {"name":name, "cost":champions[champions["name"].str.match(name)]["cost"].iloc[0]}
        store = store.append(row, ignore_index=True)

def store_button(name, index, cost):
    global champions_inventory
    global store
    select = st.button("{}_{} ({}gp)".format(name, str(index), int(cost)))
    if select:
        champions_inventory = champions_inventory.append(champions[champions["name"].str.match(name)])
        store = store.drop(store[store["name"] == name].index[0])

if list_all:
    for name in champions["name"]:
        champion_button(name)
else:
    search = st.text_input("Champion Name")
    if search != "":
        for name in champions[champions["name"].str.contains(search, case=False)]["name"]:
            champion_button(name)

"Inventory"
st.write(champions_inventory["name"])
"Store"
st.write(store)

# I know this is a faux pas, but there will only ever be 5 rows so its fine
for i, row in store.iterrows():
    store_button(row["name"], i, row["cost"])

# Caching stuff
champions_inventory.to_csv(os.getcwd() + "\\cache\\champ_list.csv", index=False)
store.to_csv(os.getcwd() + "\\cache\\store.csv", index=False)