# GIMQuestEfficiency

A little project I made for a Group Ironman Quest Point Rush competition.

The idea is to basically use a greedy algorithm to figure out what quest would be easiest to do next at any point.

I scraped all the information of quest difficulty, length, quest points, level requirements, experience granted, and prerequisite quests from the OSRS wiki.

Using that and an idea of experience rates that are obtainable at certain levels, I plan to go through all the quests, figuring out what ones can be done, and update the player's experience totals with the quest rewards.
With the updated levels, you repeat that figuring out what quests you can do now, until you can't complete any quests.
At this point, you figure out how much experience you need to meet the requirements for each remaining quest, and using approximate experience/hour rates of training, get an estimate of how long it would take before you could do each quest. You then select whatever one is lowest as the next quest to do.

I'm not sure how good the final results will be, so I may end up changing the algorithm from the description above. 
