import streamlit as st
import numpy as np
import pandas as pd
import os

champions = pd.read_csv(os.getcwd() + "\\data\\champion_info_scrape.csv")

champions_inventory = pd.read_csv(os.getcwd() + "\\cache\\champ_list.csv")
store = pd.read_csv(os.getcwd() + "\\cache\\store.csv")

with open(os.getcwd() + "\\cache\\gold.csv") as gold_file:
    file_val = gold_file.read()
    if file_val == "":
        gold = 0
    else:
        gold = int(file_val)

clear = st.button("Clear data")
if clear:
    champions_inventory = pd.DataFrame(columns = ["name"])
    store = pd.DataFrame(columns = ["name", "cost"])
    gold = 0

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
    select = st.sidebar.button("{}_{} ({}gp)".format(name, str(index), int(cost)))
    if select:
        champions_inventory = champions_inventory.append(champions[champions["name"].str.match(name)])
        store = store.drop(store[store["name"] == name].index[0])

# TODO you will probably have to add rows to your dataframe for items and current level and such
def sell_inventory_button(name):
    global champions_inventory
    global gold
    select = st.sidebar.button("{}_{} ({}gp)".format(name, str(champions_inventory[champions_inventory["name"] == name].index[0]), int(champions_inventory[champions_inventory["name"] == name]["cost"].iloc[0])))
    if select:
        champions_inventory = champions_inventory.drop(champions_inventory[champions_inventory["name"] == name].index[0])


if list_all:
    for name in champions["name"]:
        champion_button(name)
else:
    search = st.text_input("Champion Name")
    if search != "":
        for name in champions[champions["name"].str.contains(search, case=False)]["name"]:
            champion_button(name)

st.write("Gold: {}".format(gold))

# add_gold = st.number_input("Add gold: ", format="%i", step=1, value=0)
reset_gold = st.number_input("Reset gold to this amount: ", format="%i", step=1, value=gold)

if reset_gold != gold:
    gold = reset_gold
# if add_gold != 0:
#     gold += add_gold
#     st.write("New gold: {}".format(gold))
 

st.markdown("# Inventory")
st.write(champions_inventory["name"])
st.markdown("# Store")
st.write(store)

st.sidebar.markdown("## Sell")
# I know this is a faux pas, but there will only ever be 5 rows so its fine
for i, row in champions_inventory.iterrows():
    sell_inventory_button(row["name"])

st.sidebar.markdown("## Purchase")
# I know this is a faux pas, but there will only ever be 5 rows so its fine
for i, row in store.iterrows():
    store_button(row["name"], i, row["cost"])

# Caching stuff
champions_inventory.to_csv(os.getcwd() + "\\cache\\champ_list.csv", index=False)
store.to_csv(os.getcwd() + "\\cache\\store.csv", index=False)
with open(os.getcwd() + "\\cache\\gold.csv", mode="w") as gold_file:
    gold_file.write(str(gold))