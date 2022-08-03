import GameConcepts.levels as levels
import Testing.test as test

testCases = [
    { "input": 0, "expected": 0 },
    { "input": 1, "expected": 0 },
    { "input": 2, "expected": 83 },
    { "input": 50, "expected": 101333 },
    { "input": 99, "expected": 13034431 },
]

for case in testCases:
    test.Test('Testing exp from level', levels.GetExpForLevel, case["input"], case["expected"])

testCases = [
    { "input": 0, "expected": 1 },
    { "input": 1, "expected": 1 },
    { "input": 100, "expected": 2 },
    { "input": 100000, "expected": 49 },
    { "input": 1000000, "expected": 73 },
    { "input": 100000000, "expected": 99 },
]

for case in testCases:
    test.Test('Testing level from exp', levels.GetLevelFromExp, case["input"], case["expected"])