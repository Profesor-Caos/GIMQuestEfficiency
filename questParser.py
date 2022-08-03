from quest import Quest

import jsonpickle
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

skills = ["Attack", "Strength", "Defence", "Ranged", "Prayer", "Magic", "Runecraft", "Construction", 
"Hitpoints", "Agility", "Herblore", "Thieving", "Crafting","Fletching", "Slayer", "Hunter", "Mining", 
"Smithing", "Fishing", "Cooking","Firemaking", "Woodcutting", "Farming"]

quests = {}

def GetSoup(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'}) #needed user agent to prevent 403 from wiki
    page = urlopen(req)
    html = page.read().decode("utf-8")
    return BeautifulSoup(html, 'html.parser')

def ExtractQuestsFromTableList(quests, tbody):
    for tr in tbody.findAll('tr'):
        index = 0
        quest = Quest()
        for td in tr.findAll('td'):
            match index:
                case 0:
                    quest.number = td.text.strip()
                case 1:
                    quest.name = td.text.strip()
                    quest.href = td.next.attrs['href']
                case 2:
                    quest.difficulty = td.text.strip()
                case 3:
                    quest.length = td.text.strip()
                case 4:
                    quest.questPoints = td.text.strip()
                case 5:
                    quest.series = td.text.strip()
                case 6:
                    quest.releaseDate = td.text.strip()
            index += 1
        quest.levelRequirements = {}
        quest.experienceGranted = {}
        if (hasattr(quest, 'href')):
            quests[quest.href] = quest

def GetXpRewardsForSkill(skillName, soup):
    el = soup.find(id=skill)
    tbody = el.find_next("tbody")
    for tr in tbody.findAll('tr'):
        index = 0
        quest = ''
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
                    quest.experienceGranted[skillName] = td.next
                    break
            index += 1

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
        quests[href].levelRequirements[skill] = level

soup = GetSoup("https://oldschool.runescape.wiki/w/Quest_experience_rewards")

for skill in skills:
    GetXpRewardsForSkill(skill, soup)
GetXpRewardsForSkill("Skill_choice", soup)

questsJSON = jsonpickle.encode(quests)
print(questsJSON)
#print(quests)