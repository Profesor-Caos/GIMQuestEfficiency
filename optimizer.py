from functools import cmp_to_key
import json
import re
from GameConcepts.player import Player
import GameConcepts.levels as levels

quests = None
player = Player()

questDifficulties = ["Novice", "Intermediate", "Special", "Experienced", "Master", "Grandmaster"]
questLengths = ["Very Short", "Short", "Medium", "Long", "Very Long"]

wikiOptimalIronmanQuestOrder = [
	"Cook's Assistant",
	"Sheep Shearer",
	"Misthalin Mystery",
	"The Restless Ghost",
	"X Marks the Spot",
	"Witch's Potion",
	"Imp Catcher",
	"Client of Kourend",
	"Romeo & Juliet",
	"Gertrude's Cat",
	"Rune Mysteries",
	"Tree Gnome Village",
	"Monk's Friend",
	"Hazeel Cult",
	"Plague City",
	"Biohazard",
	"Fight Arena",
	"Clock Tower",
	"Sheep Herder",
	"Dwarf Cannon",
	"Waterfall Quest",
	"Murder Mystery",
	"Merlin's Crystal",
	"Holy Grail",
	"Druidic Ritual",
	"Witch's House",
	"Below Ice Mountain",
	"Black Knights' Fortress",
	"Recruitment Drive",
	"Observatory Quest",
	"Priest in Peril",
	"Rag and Bone Man I",
	"Nature Spirit",
	"Scorpion Catcher",
	"Jungle Potion",
	"Vampyre Slayer",
	"A Porcine of Interest",
	"Death Plateau",
	"Goblin Diplomacy",
	"The Queen of Thieves",
	"The Depths of Despair",
	"Mountain Daughter",
	"The Grand Tree",
	"Tribal Totem",
	"The Dig Site",
	"The Golem",
	"The Knight's Sword",
	"Sleeping Giants",
	"Elemental Workshop I",
	"Recipe for Disaster: Another Cook's quest",
	"Recipe for Disaster: Goblin generals",
	"Demon Slayer",
	"Shadow of the Storm",
	"Elemental Workshop II",
	"Lost City",
	"Fairytale I - Growing Pains",
	"Shield of Arrav",
	"Creature of Fenkenstrain",
	"A Soul's Bane",
	"The Lost Tribe",
	"Death to the Dorgeshuun",
	"The Giant Dwarf",
	"Another Slice of H.A.M.",
	"Making History",
	"In Search of the Myreque",
	"Shades of Mort'ton",
	"In Aid of the Myreque",
	"Bone Voyage",
	"Wanted!",
	"The Feud",
	"Troll Stronghold",
	"Troll Romance",
	"Dragon Slayer I",
	"Horror from the Deep",
	"Ernest the Chicken",
	"Animal Magnetism",
	"Shilo Village",
	"Doric's Quest",
	"Spirits of the Elid",
	"Icthlarin's Little Helper",
	"Ratcatchers",
	"Darkness of Hallowvale",
	"Tower of Life",
	"Fishing Contest",
	"Recipe for Disaster: Dwarf",
	"Ghosts Ahoy",
	"Forgettable Tale...",
	"Garden of Tranquillity",
	"Enlightened Journey",
	"Recipe for Disaster: Evil Dave",
	"Big Chompy Bird Hunting",
	"Zogre Flesh Eaters",
	"Recipe for Disaster: Pirate Pete",
	"Tai Bwo Wannai Trio",
	"The Tourist Trap",
	"Eadgar's Ruse",
	"My Arm's Big Adventure",
	"The Fremennik Trials",
	"The Fremennik Isles",
	"Getting Ahead",
	"Recipe for Disaster: Lumbridge Guide",
	"Recipe for Disaster: Skrach Uglogwee",
	"Haunted Mine",
	"Watchtower",
	"Prince Ali Rescue",
	"Contact!",
	"The Eyes of Glouphrie",
	"Temple of the Eye",
	"Sea Slug",
	"Olaf's Quest",
	"Tears of Guthix",
	"Temple of Ikov",
	"One Small Favour",
	"A Tail of Two Cats",
	"The Slug Menace",
	"Between a Rock...",
	"Monkey Madness I",
	"Cold War",
	"The Ascent of Arceuus",
	"Eagles' Peak",
	"Underground Pass",
	"Rag and Bone Man II",
	"Rum Deal",
	"Pirate's Treasure",
	"Cabin Fever",
	"The Great Brain Robbery",
	"The Hand in the Sand",
	"Enakhra's Lament",
	"Heroes' Quest",
	"Throne of Miscellania",
	"Royal Trouble",
	"Desert Treasure",
	"A Taste of Hope",
	"Family Crest",
	"Legends' Quest",
	"Recipe for Disaster: Sir Amik Varze",
	"Land of the Goblins",
	"Fairytale II - Cure a Queen",
	"Tale of the Righteous",
	"The Forsaken Tower",
	"A Kingdom Divided",
	"Recipe for Disaster: Awowogei",
	"Regicide",
	"Roving Elves",
	"Mourning's End Part I",
	"Mourning's End Part II",
	"Lunar Diplomacy",
	"What Lies Below",
	"King's Ransom",
	"Swan Song",
	"Grim Tales",
	"Dream Mentor",
	"Devious Minds",
	"The Fremennik Exiles",
	"Sins of the Father",
	"Beneath Cursed Sands",
	"Making Friends with My Arm",
	"Monkey Madness II",
	"A Night at the Theatre",
	"Dragon Slayer II",
	"Song of the Elves",
	"The Corsair Curse",
]

osirisQuestingOrder = [
	"X Marks the Spot",
	"Monk's Friend",
	"Sheep Herder",
	"Sea Slug",
	"Plague City",
	"Gertrude's Cat",
	"Witch's House",
	"Druidic Ritual",
	"Witch's Potion",
	"The Knight's Sword",
	"The Tourist Trap",
	"Fight Arena",
	"Tree Gnome Village",
	"Hazeel Cult",
	"Tribal Totem",
	"Dwarf Cannon",
	"Waterfall Quest",
	"Cook's Assistant",
	"Recipe for Disaster/Another Cook's Quest",
	"Sheep Shearer",
	"Imp Catcher",
	"Rune Mysteries",
	"Demon Slayer",
	"Romeo & Juliet",
	"The Grand Tree",
	"Murder Mystery",
	"Fishing Contest",
	"Doric's Quest",
	"Goblin Diplomacy",
	"Pirate's Treasure",
	"Black Knights' Fortress",
	"Recruitment Drive",
	"Observatory Quest",
	"The Restless Ghost",
	"The Dig Site",
	"Biohazard",
	"Jungle Potion",
	"Shilo Village",
	"Merlin's Crystal",
	"Elemental Workshop I",
	"The Lost Tribe",
	"The Feud",
	"The Golem",
	"Shadow of the Storm",
	"Priest in Peril",
	"Nature Spirit",
	"Creature of Fenkenstrain",
	"Elemental Workshop II",
	"Ernest the Chicken",
	"Vampyre Slayer",
	"Lost City",
	"Fairytale I - Growing Pains",
	"Prince Ali Rescue",
	"Dragon Slayer I",
	"Recipe for Disaster/Freeing Evil Dave",
	"Death to the Dorgeshuun",
	"Holy Grail",
	"Horror from the Deep",
	"Animal Magnetism",
	"Spirits of the Elid",
	"Underground Pass",
	"Ghosts Ahoy",
	"Monkey Madness I",
	"Wanted!",
	"Shades of Mort'ton",
	"Heroes' Quest",
	"The Fremennik Trials",
	"Throne of Miscellania",
	"Royal Trouble",
	"Bone Voyage",
	"Tears of Guthix",
	"The Giant Dwarf",
	"Forgettable Tale...",
	"Garden of Tranquillity",
	"The Eyes of Glouphrie",
	"Tower of Life",
	"Temple of Ikov",
	"Enlightened Journey",
	"Big Chompy Bird Hunting",
	"Rag and Bone Man I",
	"Family Crest",
	"Legends' Quest",
	"Death Plateau",
	"Troll Stronghold",
	"Regicide",
	"The Hand in the Sand",
	"Recipe for Disaster/Freeing the Mountain Dwarf",
	"Recipe for Disaster/Freeing the Goblin generals",
	"Recipe for Disaster/Freeing Pirate Pete",
	"Recipe for Disaster/Freeing the Lumbridge Guide",
	"Recipe for Disaster/Freeing Sir Amik Varze",
	"Recipe for Disaster/Freeing Skrach Uglogwee",
	"Recipe for Disaster/Freeing King Awowogei",
	"Lunar Diplomacy",
	"The Fremennik Isles",
	"Dream Mentor",
	"Song of the Elves",
]

modifiedOsirisQuestingOrder = [
	"X Marks the Spot",
	"Monk's Friend",
	"Sheep Herder",
	"Sea Slug",
	"Plague City",
	"Gertrude's Cat",
	"Witch's House",
	"Druidic Ritual",
	"Witch's Potion",
	"The Knight's Sword",
	"The Tourist Trap",
	"Fight Arena",
	"Tree Gnome Village",
	"Hazeel Cult",
	"Tribal Totem",
	"Dwarf Cannon",
	"Waterfall Quest",
	"Cook's Assistant",
	"Recipe for Disaster/Another Cook's Quest",
	"Sheep Shearer",
	"Imp Catcher",
	"Rune Mysteries",
	"Demon Slayer",
	"Romeo & Juliet",
	"The Grand Tree",
	"Murder Mystery",
	"Fishing Contest",
	"Doric's Quest",
	"Goblin Diplomacy",
	"Pirate's Treasure",
	"Black Knights' Fortress",
	"Recruitment Drive",
	"Observatory Quest",
	"The Restless Ghost",
	"The Dig Site",
	"Biohazard",
	"Jungle Potion",
	"Shilo Village",
	"Merlin's Crystal",
	"Elemental Workshop I",
	"The Lost Tribe",
	"The Feud",
	"The Golem",
	"Shadow of the Storm",
	"Priest in Peril",
	"Nature Spirit",
	"Creature of Fenkenstrain",
	"Elemental Workshop II",
	"Ernest the Chicken",
	"Vampyre Slayer",
	"Lost City",
	"Fairytale I - Growing Pains",
	"Prince Ali Rescue",
	"Dragon Slayer I",
	"Recipe for Disaster/Freeing Evil Dave",
	"Death to the Dorgeshuun",
	"Holy Grail",
	"Horror from the Deep",
	"Animal Magnetism",
	"Spirits of the Elid",
	"Underground Pass",
	"Ghosts Ahoy",
	"Monkey Madness I",
	"Wanted!",
	"Shades of Mort'ton",
	"The Fremennik Trials",
	"Bone Voyage",
	"Tears of Guthix",
	"The Giant Dwarf",
	"Forgettable Tale...",
	"Garden of Tranquillity",
	"Tower of Life",
	"Enlightened Journey",
	"Big Chompy Bird Hunting",
	"Rag and Bone Man I",
	"Death Plateau",
	"Troll Stronghold",
	"Recipe for Disaster/Freeing the Mountain Dwarf",
	"Recipe for Disaster/Freeing the Goblin generals",
	"Recipe for Disaster/Freeing Pirate Pete",
	"Recipe for Disaster/Freeing the Lumbridge Guide",
	"Recipe for Disaster/Freeing Skrach Uglogwee",
]

def GetQuestWeighting(quest):
    questWeight = wikiOptimalIronmanQuestOrder.index(quest["name"])
    if (quest["name"] in modifiedOsirisQuestingOrder):
        questWeight += modifiedOsirisQuestingOrder.index(quest["name"])
    else:
        questWeight += 60
    
    questWeight += questDifficulties.index(quest["difficulty"]) * 3

    questWeight += questLengths.index(quest["length"]) * 2

    questWeight -= quest["questPoints"] ** quest["questPoints"]

    return questWeight

def QuestSortComparison(questID1, questID2):
    quest1 = quests[questID1]
    quest2 = quests[questID2]
    
    return GetQuestWeighting(quest1) - GetQuestWeighting(quest2)

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

# for questID in quests:
#     quest = quests[questID]
#     if (CheckIfQuestCanBeCompleted(quest)):
#         questsToComplete.add(questID)

# sortedQuestsToComplete = sorted(questsToComplete, key=cmp_to_key(QuestSortComparison))

# print("Immediately Completable Quests:")
# print(questsToComplete)

# for questID in sortedQuestsToComplete:
#     CompleteQuest(questID)

# print("Completed Quests:")
# print(completedQuests)

# for osirisQuest in osirisQuestingOrder:
#     matched = False
#     for questID in quests:
#         quest = quests[questID]
#         if (quest["name"] == osirisQuest):
#             CompleteQuest(questID)
#             quests.pop(questID, None)
#             matched = True
#             break

for questID in quests:
    questsToComplete.add(questID)

sortedQuestsToComplete = sorted(questsToComplete, key=cmp_to_key(QuestSortComparison))
print(sortedQuestsToComplete)