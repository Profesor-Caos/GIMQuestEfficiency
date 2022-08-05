osirisQuestingOrder = ["X Marks the Spot", "Monk's Friend", "Sheep Herder", "Sea Slug", "Plague City", "Gertrude's Cat", "Witch's House", "Druidic Ritual", "Witch's Potion", 
"The Knight's Sword", "The Tourist Trap", "Fight Arena", "Tree Gnome Village", "Hazeel Cult", "Tribal Totem", "Dwarf Cannon", "Waterfall Quest", "Cook's Assistant", 
"Recipe for Disaster/Another Cook's Quest", "Sheep Shearer","Imp Catcher", "Rune Mysteries", "Demon Slayer", "Romeo & Juliet", "The Grand Tree", "Murder Mystery", "Fishing Contest", 
"Doric's Quest", "Goblin Diplomacy", "Pirate's Treasure", "Black Knights' Fortress", "Recruitment Drive", "Observatory Quest", "The Restless Ghost", "The Dig Site", "Biohazard", 
"Jungle Potion", "Shilo Village", "Merlin's Crystal", "Elemental Workshop I", "The Lost Tribe", "The Feud", "The Golem", "Shadow of the Storm", "Priest in Peril", "Nature Spirit", 
"Creature of Fenkenstrain", "Elemental Workshop II", "Ernest the Chicken", "Vampyre Slayer", "Lost City", "Fairytale I - Growing Pains", "Prince Ali Rescue", "Dragon Slayer I", 
"Recipe for Disaster/Freeing Evil Dave", "Death to the Dorgeshuun", "Holy Grail", "Horror from the Deep", "Animal Magnetism", "Spirits of the Elid", "Underground Pass", 
"Ghosts Ahoy", "Monkey Madness I", "Wanted!", "Shades of Mort'ton", "Heroes' Quest", "The Fremennik Trials", "Throne of Miscellania", "Royal Trouble", "Bone Voyage", "Tears of Guthix", 
"The Giant Dwarf", "Forgettable Tale...", "Garden of Tranquillity", "The Eyes of Glouphrie", "Tower of Life", "Temple of Ikov", "Enlightened Journey", "Big Chompy Bird Hunting", 
"Rag and Bone Man I", "Family Crest", "Legends' Quest", "Death Plateau", "Troll Stronghold", "Regicide", "The Hand in the Sand", "Recipe for Disaster/Freeing the Mountain Dwarf",
"Recipe for Disaster/Freeing the Goblin generals", "Recipe for Disaster/Freeing Pirate Pete", "Recipe for Disaster/Freeing the Lumbridge Guide",
"Recipe for Disaster/Freeing Sir Amik Varze", "Recipe for Disaster/Freeing Skrach Uglogwee", "Recipe for Disaster/Freeing King Awowogei", "Lunar Diplomacy",
"The Fremennik Isles", "Dream Mentor", "Song of the Elves"]

output = "osirisQuestingOrder = [\n"
for string in osirisQuestingOrder:
    output += f"\t\"{string}\",\n"
output += "]"

import io
with io.open('./Data/osirisQuests.txt', 'wt') as f:
    f.write(output)