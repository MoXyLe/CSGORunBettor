f = open("csgorun\data.txt", "r")

#allData = {}

gettingAt = 1.2
crash = 1.2

row = 0
maxRow = 0
maxRowID = 0

bank = 12.0
currentBets = 0.0
previousBets = 0.0
maxBets = 0.0
minimalBet = 0.25
lost = False
potentialWin = minimalBet * (gettingAt - 1.0)
streak = 2
amountOfWins = 0
amountOfLosses = 0

below = 0
above = 0

divided = 43

betting = False

for i in f:
    if bank / divided > minimalBet:
        minimalBet = round((bank / divided) - 0.005, 2)
    if float(i.split(" ")[1]) >= crash:
        above += 1
        row += 1
        if row == streak + 1 or betting:
            currentBets = 0.0
            bank += round(minimalBet * (gettingAt - 1), 2)
            amountOfWins += 1
            betting = False
            #print(i.split(" ")[0])

    else:
        if row == streak or betting:
            currentBets += (currentBets / (gettingAt - 1)) + minimalBet
            if currentBets >= bank:
                amountOfLosses += 1
                print("Balance was " + str(bank))
                bank = 12.0
                minimalBet = 0.25
            else:
                betting = True
        below += 1
        row = 0

    #allData[int(i.split(" ")[0])] = float(i.split(" ")[1])

print("Amount of wins is " + str(amountOfWins))
print("Amount of losses is " + str(amountOfLosses))
print("Max row is " + str(maxRow))
print("Max bet is " + str(maxBets))
print("Total bank is " + str(bank))
if lost:
    print("You lost!")
else:
    print("You won!")

print("Below crash " + str(below))
print("Above crash " + str(above))

f.close()

"""
elif float(i.split(" ")[1]) < gettingAt and row > streak:
    row += 1
    currentBets += currentBets * (1 / (gettingAt - 1)) + minimalBet
    if currentBets > maxBets:
        maxBets = currentBets
"""
