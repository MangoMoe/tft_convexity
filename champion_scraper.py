# %%
import httplib2
from bs4 import BeautifulSoup
import pandas as pd
import os
from tqdm.auto import tqdm

# %%
http = httplib2.Http()
status, response = http.request("https://app.mobalytics.gg/tft/set3/champions")

soup = BeautifulSoup(response)

# %%

frame = pd.DataFrame({})

def extract_champion_data(uri):
    global frame
    base_url = "https://app.mobalytics.gg"
    url = base_url + uri
    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response)

    h1 = soup.find('h1', {"class": "tft-champion-cardstyles__Name-sc-1ne6d17-10"})
    name = h1.text

    div = soup.find('div', {"class": "tft-champion-cardstyles__Cost-sc-1ne6d17-7"})
    cost = int(div.text)

    # This is actually special ability damage
    # div = soup.find('div', {"class": "markupstyles__SpreadBetweenLayout-bs8lb6-0"})
    # damages = div.find_all("p")[1].text.split(" / ")
    # damages = [int(x) for x in damages]
    # print(damages)

    # typography__Text14x700-sc-1ossu1y-12 iKInKs
    divs = soup.find_all('div', {"class": "champion-stat-with-titlestyles__Wrapper-sc-18rahlm-0 rOzjO champion-statsstyles__LongStat-sc-1kfvrng-1 ggiZGv"})

    healths = divs[0].find_all("p")[1].text.split(" / ")
    healths = [int(x) for x in healths]

    damages = divs[1].find_all("p")[1].text.split(" / ")
    damages = [int(x) for x in damages]

    dps = divs[2].find_all("p")[1].text.split(" / ")
    dps = [int(x) for x in dps]

    divs = soup.find_all('div', {"class":"champion-stat-with-titlestyles__Wrapper-sc-18rahlm-0 rOzjO champion-statsstyles__ShortStats-sc-1kfvrng-2 fEQSwV"})

    armor = int(divs[0].find_all("p")[1].text)

    mr = int(divs[1].find_all("p")[1].text)

    speed = float(divs[2].find_all("p")[1].text)

    rng = int(divs[3].find("svg")["value"])

    divs = soup.find_all('div', {"class": "champion-stat-with-titlestyles__Wrapper-sc-18rahlm-0 rOzjO champion-statsstyles__AutoStats-sc-1kfvrng-3 bBdKGz"})

    mana = divs[0].find_all("p")[1].text.split(" / ")
    for i in range(len(mana)):
        if mana[i] == "-":
            mana[i] = "0"
    mana = [int(x) for x in mana]
    mana_start = mana[0]
    mana_max = mana[1]

    # synergies
    spans = soup.find_all('span', {"class": "synergy-description-blockstyles__NameValue-sc-17poswj-2 kixkDF"})
    synergies = [span.text for span in spans]

    # TODO figure out how you want to handle the lists
    row = {
        "name":name,

        "cost":cost, 

        "t1_health":healths[0], 
        "t2_health":healths[1], 
        "t3_health":healths[2], 

        "t1_damage":damages[0], 
        "t2_damage":damages[1], 
        "t3_damage":damages[2], 

        "t1_dps":dps[0], 
        "t2_dps":dps[1], 
        "t3_dps":dps[2], 

        "armor":armor,
        "mr":mr,
        "speed":speed,
        "range":rng,
        "mana_start":mana_start,
        "mana_max":mana_max,
        # TODO figure out how to handle list of synergies
        "synergies":synergies
    }

    frame = frame.append(row, ignore_index=True)

for link in tqdm(soup.find_all('a', href=True)):
    if "set3/champions/" in link['href']:
        extract_champion_data(link['href'])

print(frame.head())
# print(os.getcwd() + "\\data\\champion_info_scrape.csv")
frame.to_csv(os.getcwd() + "\\data\\champion_info_scrape.csv")

# %%
