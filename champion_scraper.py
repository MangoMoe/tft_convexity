# %%
import requests
from bs4 import BeautifulSoup

#%%
page = requests.get("https://app.mobalytics.gg/tft/set3/champions")
soup = BeautifulSoup(page.content, 'html.parser')

# %%
# print(soup.prettify())
# print(soup.prettify())
print(len(soup.find_all('a')))


# %%
import httplib2
from bs4 import BeautifulSoup, SoupStrainer

http = httplib2.Http()
status, response = http.request("https://app.mobalytics.gg/tft/set3/champions")

# count = 0
# for link in BeautifulSoup(response, parse_only=SoupStrainer('a')):
#     count += 1
#     # print(link)
#     if link.__class__.__name__ == "Doctype":
#         print("what the heck")
#         continue
#     if "href" in link.attrs:
#         print(link['href'])
# print(count)

soup = BeautifulSoup(response)

for link in soup.find_all('a', href=True):
    if "set3/champions/" in link['href']:
        print(link['href'])

# %%
from bs4 import BeautifulSoup
import urllib.request

# resp = urllib.request.urlopen("https://app.mobalytics.gg/tft/set3/champions")
resp = urllib.request.urlopen("https://app.mobalytics.gg/tft/set3/champions/ahri")
# status, resp = http.request('http://www.nytimes.com')
soup = BeautifulSoup(resp, from_encoding=resp.info().get_param('charset'))

for link in soup.find_all('a', href=True):
    print(link['href'])