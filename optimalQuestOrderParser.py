from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import json

quests = None
with open("./Data/quests.json") as f:
    quests = json.load(f)

def GetSoup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #needed user agent to prevent 403 from wiki
    page = urlopen(req)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, 'html.parser')

output = "wikiOptimalIronmanQuestOrder = [\n"

soup = GetSoup("https://oldschool.runescape.wiki/w/Optimal_quest_guide/Ironman")
el = soup.find("caption", text="Old School RuneScape Quest Guide\n")
tbody = el.find_next("tbody")
for tr in tbody.findAll('tr'):
    td = tr.findNext("td")
    if (td == None):
        continue
    name = td.text.strip()
    if hasattr(td.next, "attrs"):
        href = td.next.attrs["href"]
        if href in quests:
            output += f"\t\"{name}\"\n"
            quests.pop(href, None) #prevents multiple entries for quests that occupy multiple rows

output += "]"

import io
with io.open('./Data/optimalQuests.txt', 'wt') as f:
    f.write(output)