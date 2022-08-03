import json
import re
from player import Player
import levels

quests = None
player = Player()

questDifficulties = ["Novice", "Intermediate", "Experienced", "Master", "Grandmaster"]
questLengths = ["very short", "short", "medium", "long", "very long"]

def QuestSortComparison(questID1, questID2):
    quest1 = quests[questID1]
    quest2 = quests[questID2]
    if (questDifficulties.index(quest1["difficulty"]) > questDifficulties.index(quest2["difficulty"])):
        return 1
    if (questDifficulties.index(quest1["difficulty"]) < questDifficulties.index(quest2["difficulty"])):
        return -1
    
    if (questLengths.index(quest1["length"]) > questLengths.index(quest2["length"])):
        return 1
    if (questLengths.index(quest1["length"]) < questLengths.index(quest2["length"])):
        return -1
    
    if (quest1["questPoints"] > quest2["questPoints"]):
        return -1
    if (quest1["questPoints"] < quest2["questPoints"]):
        return 1
    
    return 0

with open("quests.json") as f:
    quests = json.load(f)

completedQuests = set([])
questsToComplete = set([])

def CheckIfQuestCanBeCompleted(quest):
    levelRequirements = quest["levelRequirements"]
    for skill in levelRequirements:
        reqLevel = levelRequirements[skill]
        if player.getLevel(skill) >= reqLevel:
            continue
        else:
            expRequired = levels.GetExpForLevel(reqLevel) - player.getExp(skill)
            return False
            #todo: approximate time to get level
    prereqQuests = quest["prerequisiteQuests"]
    for prereq in prereqQuests:
        if prereq not in completedQuests:
            return False
    return True

def CompleteQuest(questID):
    completedQuests.add(questID)
    exp = quests[questID]["experienceGranted"]
    for skill in exp:
        player.addExp(skill, exp[skill])

for questID in quests:
    quest = quests[questID]
    if (CheckIfQuestCanBeCompleted(quest)):
        questsToComplete.add(questID)

sortedQuestsToComplete = [];
for questID in questsToComplete:
    sortedQuestsToComplete.append(quests[questID])
sortedQuestsToComplete.sort()

print("Immediately Completable Quests:")
print(questsToComplete)

for questID in questsToComplete:
    CompleteQuest(questID)

print("Completed Quests:")
print(completedQuests)
