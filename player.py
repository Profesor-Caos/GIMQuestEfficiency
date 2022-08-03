from skills import skills
import levels

class Player:
    def __init__(self):
        self.skills = {}
        for skill in skills:
            self.skills[skill] = 0
    
    def getLevel(self, skill):
        xp = self.skills[skill]
        return levels.GetLevelFromExp(xp)

    def getExp(self, skill):
        return self.skills[skill]

    def addExp(self, skill, xp):
        self.skills[skill] += xp