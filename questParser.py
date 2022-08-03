from ast import pattern
from sre_parse import FLAGS
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from GameConcepts.skills import skills

quests = {}

def GetSoup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #needed user agent to prevent 403 from wiki
    page = urlopen(req)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, 'html.parser')

def ExtractQuestsFromTableList(quests, tbody):
    for tr in tbody.findAll('tr'):
        index = 0
        quest = {}
        for td in tr.findAll('td'):
            match index:
                case 0:
                    quest["number"] = td.text.strip()
                case 1:
                    quest["name"] = td.text.strip()
                    quest["href"] = td.next.attrs["href"]
                case 2:
                    quest["difficulty"] = td.text.strip()
                case 3:
                    quest["length"] = td.text.strip()
                case 4:
                    quest["questPoints"] = int(td.text.strip())
                case 5:
                    quest["series"] = td.text.strip()
                case 6:
                    quest["releaseDate"] = td.text.strip()
            index += 1
        quest["levelRequirements"] = {}
        quest["experienceGranted"] = {}
        quest["prerequisiteQuests"] = []
        if ("href" in quest):
            quests[quest["href"]] = quest

def GetXpRewardsForSkill(skillName, soup):
    el = soup.find(id=skill)
    tbody = el.find_next("tbody")
    for tr in tbody.findAll('tr'):
        index = 0
        quest = None
        for td in tr.findAll('td'):
            match index:
                case 0:
                    a = td.find_next("a")
                    href = a.attrs["href"]
                    if (href == "/w/Recipe_for_Disaster"):
                        a = a.find_next("a")
                        href = a.attrs["href"]
                    if href not in quests:
                        print("Cannot find Quest: " + href)
                        break
                    quest = quests[href]
                case 1:
                    quest["experienceGranted"][skillName] = float((td.next).replace(",",""))
                    break
            index += 1

def GetQuestPreRequisites(href, soup:BeautifulSoup):
    el = soup.find("th", {"class":"questdetails-header", "text":"Requirements"})
    li = soup.find("li", string="Completion of the following quests:")

def GetQuestFromName(name):
    for href in quests:
        if (quests[href]["name"] == name):
            return quests[href]
    print("Could not find quest : " + name)
    return None

soup = GetSoup("https://oldschool.runescape.wiki/w/Quests/List")

# Get free to play quests first
el = soup.find("td", {"data-sort-value":"Cook's Assistant"})
firstRow = el.parent
tbody = firstRow.parent
ExtractQuestsFromTableList(quests, tbody)

# Get Members quests
el = soup.find("td", {"data-sort-value":"Druidic Ritual"})
firstRow = el.parent
tbody = firstRow.parent
ExtractQuestsFromTableList(quests, tbody)

soup = GetSoup("https://oldschool.runescape.wiki/w/Quests/Skill_requirements")

for skill in skills:
    el = soup.find(id=skill)
    header = el.parent
    ul = header.find_next("ul")
    for li in ul.findAll("li"):
        text = li.text
        split = text.split('-')
        level = split[0].strip()
        a = li.find_next("a")
        href = a.attrs["href"]
        if (href.endswith("_(quest)")):
            href = href[0:len(href) - len("_(quest)")]
        quests[href]["levelRequirements"][skill] = int(level)

soup = GetSoup("https://oldschool.runescape.wiki/w/Quest_experience_rewards")

for skill in skills:
    GetXpRewardsForSkill(skill, soup)
GetXpRewardsForSkill("Skill_choice", soup)

import requests

result = requests.get('https://oldschool.runescape.wiki/api.php', params={
    'action': 'ask',
    'query': '[[Quest Requirements::+]]|?Quest Requirements|limit=500',
    'format': 'json'
}).json()

import re

for page in result['query']['results']:
    reqs = result['query']['results'][page]['printouts']['Quest Requirements'][0]
    quest = GetQuestFromName(page)
    if (quest == None):
        continue
    rePattern = "\[\[.+?\]\]"
    matches = re.findall(rePattern, reqs)
    for match in matches:
        match = match.strip("[]")
        req = GetQuestFromName(match)
        if (req == None):
            continue
        quest["prerequisiteQuests"].append(match)


import json
questsJSON = json.dumps(quests, indent=4, separators=(',', ': '))

import io
with io.open('./Data/quests.json', 'wt') as f:
    f.write(questsJSON)
