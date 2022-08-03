import csv
import math
experience = 0
difference = 0
with open('levels.csv', 'w', newline='\n') as f:
    fieldnames = ['level', 'experience', 'difference']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'level' : 1, 'experience' : 0, 'difference' : 0})
    for level in range(2, 100):
        difference = math.floor(level - 1 + 300*2**((level-1)/7)) // 4
        experience += difference
        writer.writerow({'level' : level, 'experience' : experience, 'difference' : difference})