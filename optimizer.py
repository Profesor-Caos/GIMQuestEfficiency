from functools import cmp_to_key
import json
import re
from GameConcepts.player import Player
import GameConcepts.levels as levels

quests = None
player = Player()

questDifficulties = ["Novice", "Intermediate", "Experienced", "Master", "Grandmaster"]
questLengths = ["Very Short", "Short", "Medium", "Long", "Very Long"]

startingQuestOrder = ["Cook's Assistant", ]
osirisQuestingOrder = ["X Marks the Spot", "Monk's Friend", "Sheep Herder", "Sea Slug", "Plague City", "Gertrude's Cat", "Witch's House", "Druidic Ritual", "Witch's Potion", 
"The Knight's Sword", "The Tourist Trap", "Fight Arena", "Tree Gnome Village", "Hazeel Cult", "Tribal Totem", "Dwarf Cannon", "Waterfall Quest", "Cook's Assistant", 
"Recipe for Disaster/Another Cook's Quest", "Sheep Shearer","Imp Catcher", "Rune Mysteries", "Demon Slayer", "Romeo and Juliet", "The Grand Tree", "Murder Mystery", "Fishing Contest", 
"Doric's Quest", "Goblin Diplomacy", "Pirate's Treasure", "Black Knights' Fortress", "Recruitment Drive", "Observatory Quest", "The Restless Ghost", "The Dig Site", "Biohazard", 
"Jungle Potion", "Shilo Village", "Merlin's Crystal", "Elemental Workshop I", "The Lost Tribe", "The Feud", "The Golem", "Shadow of the Storm", "Priest in Peril", "Nature Spirit", 
"Creature of Fenkenstrain", "Elemental Workshop 2", "Ernest the Chicken," "Vampyre Slayer", "Lost City", "Fairytale I - Growing Pains", "Dragon Slayer I", 
"Recipe for Disaster/Freeing Evil Dave", "Death to the Dorgeshuun", "Holy Grail", "Horror from the Deep", "Animal Magnetism", "Spirits of the Elid", "Underground Pass", 
"Ghosts Ahoy", "Monkey Madness", "Wanted!", "Shades of Mort'ton", "Heroes' Quest", "Fremennik Trials", "Throne of Miscellania", "Royal Trouble", "Bone Voyage", "Tears of Guthix", 
"The Giant Dwarf", "Forgettable Tale...", "Garden of Tranquility", "Eyes of Glouphrie", "Tower of Life", "Temple of Ikov", "Enlightened Journey", "Big Chompy Bird Hunt", 
"Rag and Bone Man", "Family Crest", "Legends' Quest", "Death Plateau", "Troll Stronghold", "Regicide", "Hand in the Sand", "Recipe for Disaster/Freeing the Mountain Dwarf",
"Recipe for Disaster/Freeing the Goblin generals", "Recipe for Disaster/Freeing Pirate Pete", "Recipe for Disaster/Freeing the Lumbridge Guide",
"Recipe for Disaster/Freeing Sir Amik Varze", "Recipe for Disaster/Freeing Skrach Uglogwee", "Recipe for Disaster/Freeing King Awowogei", "Lunar Diplomacy",
"The Fremennik Isles", "Dream Mentor", "Song of the Elves"]

modifiedOsirisOrder = ["X Marks the Spot", "Monk's Friend", "Sheep Herder", "Sea Slug", "Plague City", "Gertrude's Cat", "Witch's House", "Druidic Ritual", "Witch's Potion", 
"The Knight's Sword", "The Tourist Trap", "Fight Arena", "Tree Gnome Village", "Hazeel Cult", "Tribal Totem", "Dwarf Cannon", "Waterfall Quest", "Cook's Assistant", 
"Recipe for Disaster/Another Cook's Quest", "Sheep Shearer","Imp Catcher", "Rune Mysteries", "Demon Slayer", "Romeo and Juliet", "The Grand Tree", "Murder Mystery", "Fishing Contest", 
"Doric's Quest", "Goblin Diplomacy", "Pirate's Treasure", "Black Knights' Fortress", "Recruitment Drive", "Observatory Quest", "The Restless Ghost", "The Dig Site", "Biohazard", 
"Jungle Potion", "Shilo Village", "Merlin's Crystal", "Elemental Workshop I", "The Lost Tribe", "The Feud", "The Golem", "Shadow of the Storm", "Priest in Peril", "Nature Spirit", 
"Creature of Fenkenstrain", "Elemental Workshop 2", "Ernest the Chicken," "Vampyre Slayer", "Lost City", "Fairytale I - Growing Pains", "Dragon Slayer I", 
"Recipe for Disaster/Freeing Evil Dave", "Death to the Dorgeshuun", "Holy Grail", "Horror from the Deep", "Animal Magnetism", "Spirits of the Elid", "Underground Pass", 
"Ghosts Ahoy", "Monkey Madness", "Wanted!", "Shades of Mort'ton", "Heroes' Quest", "Fremennik Trials", "Throne of Miscellania", "Royal Trouble", "Bone Voyage", "Tears of Guthix", 
"The Giant Dwarf", "Forgettable Tale...", "Garden of Tranquility", "Eyes of Glouphrie", "Tower of Life", "Temple of Ikov", "Enlightened Journey", "Big Chompy Bird Hunt", 
"Rag and Bone Man", "Family Crest", "Legends' Quest", "Death Plateau", "Troll Stronghold", "Regicide", "Hand in the Sand", "Recipe for Disaster/Freeing the Mountain Dwarf",
"Recipe for Disaster/Freeing the Goblin generals", "Recipe for Disaster/Freeing Pirate Pete", "Recipe for Disaster/Freeing the Lumbridge Guide",
"Recipe for Disaster/Freeing Sir Amik Varze", "Recipe for Disaster/Freeing Skrach Uglogwee", "Recipe for Disaster/Freeing King Awowogei", "Lunar Diplomacy",
"The Fremennik Isles", "Dream Mentor"]

def QuestSortComparison(questID1, questID2):
    quest1 = quests[questID1]
    quest2 = quests[questID2]

    # Highest preference for easiest quest
    if (questDifficulties.index(quest1["difficulty"]) > questDifficulties.index(quest2["difficulty"])):
        return 1
    if (questDifficulties.index(quest1["difficulty"]) < questDifficulties.index(quest2["difficulty"])):
        return -1
    
    # Next preference is quest length
    if (questLengths.index(quest1["length"]) > questLengths.index(quest2["length"])):
        return 1
    if (questLengths.index(quest1["length"]) < questLengths.index(quest2["length"])):
        return -1

    # Last preference is quest points
    return quest2["questPoints"] - quest1["questPoints"] # More quest points is preferred

with open("./Data/quests.json") as f:
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

sortedQuestsToComplete = sorted(questsToComplete, key=cmp_to_key(QuestSortComparison))

print("Immediately Completable Quests:")
print(questsToComplete)

for questID in sortedQuestsToComplete:
    CompleteQuest(questID)

print("Completed Quests:")
print(completedQuests)
