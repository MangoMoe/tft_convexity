# %%
import httplib2
from bs4 import BeautifulSoup


# %%
http = httplib2.Http()
status, response = http.request("https://app.mobalytics.gg/tft/set3/champions")

soup = BeautifulSoup(response)

# %%
def extract_champion_data(uri):
    # TODO make the pandas dataframe (outside of here)
    base_url = "https://app.mobalytics.gg"
    url = base_url + uri
    http = httplib2.Http()
    status, response = http.request(url)
    soup = BeautifulSoup(response)

    h1 = soup.find('h1', {"class": "tft-champion-cardstyles__Name-sc-1ne6d17-10"})
    name = h1.text
    print(name)
    # typography__Text16x700-sc-1ossu1y-9 tft-champion-cardstyles__Name-sc-1ne6d17-10 hpWIZv

    div = soup.find('div', {"class": "markupstyles__SpreadBetweenLayout-bs8lb6-0"})
    damages = div.find_all("p")[1].text.split(" / ")
    print(damages)

    div = soup.find('div', {"class": "champion-statsstyles__Wrapper-sc-1uyt2ip-0"})
    healths = div.find("p").text.split(" / ")
    print(healths)
    # champion-statsstyles__Wrapper-sc-1uyt2ip-0 kkswzM


for link in soup.find_all('a', href=True):
    if "set3/champions/" in link['href']:
        extract_champion_data(link['href'])
        break
        # print(link['href'])