from __future__ import print_function, division
from random import shuffle
import copy

##To Do List
#Check if new card is valid in dealersCard.
#in findWinner return 2 if a pontoon gets double pay.

def newDeck():
    # Create a deck with numbers 1-9 four times and 10 sixteen times.
    deck = range(1,10)*4 + [10]*16
    shuffle(deck)
    return deck

def dealCard(deck):
    # Take a deck of remaining cards and deal one.
    # Shuffle and take the last card.
    numberCards = len(deck)
    if numberCards == 0:
        return False
    else:
        shuffle(deck)
        newCard = deck.pop()
        return newCard

def removeFromDeck(newCard, deck):
    # Remove a new card from the deck.
    # Return False if card is not found.
    if newCard in deck:
        cardIndex = deck.index(newCard)
        # Merge together all cards before and after new card.
        deck = deck[:cardIndex] + deck[cardIndex+1:]
        return deck
    else:
        return False

def dealersCard(deck):
    # Take dealer's card out of the deck.
    validCard = False
    while not validCard:
        message = "Enter the dealer's shown card\n"
        newCardString = raw_input(message)
        newCard = int(newCardString)
        validCard = True

    # Check if new deck started.
    deck = removeFromDeck(newCard, deck)
    if deck is False:
        deck = newDeck()

def myCards(deck):
    # Take my two cards out of the deck and save them.
    myCards = []
    for i in range(2):
        validCard = False
        while not validCard:
            message = "Enter my card\n"
            newCardString = raw_input(message)
            newCard = int(newCardString)
            validCard = True
        # Check if new deck started.
        deck = removeFromDeck(newCard, deck)
        if deck is False:
            deck = newDeck()
        myCards.append(newCard)
    
def tableCards(deck):
    # Take all table cards out of the deck.
    dealingFinished = False
    while not dealingFinished:
        validCard = False
        while not validCard:
            message = "Enter cards of all other players\n"
            newCardString = raw_input(message)
            newCard = int(newCardString)
            # If entered card is "0" then stop asking for cards.
            if newCardString == "0":
                dealingFinished = True
                break
            validCard = True
        # Check if new deck started.
        if not dealingFinished:
            deck = removeFromDeck(newCard, deck)
            if deck is False:
                deck = newDeck()
    
def cardsTotal(cards):
    # Check the total of all cards a player has.
    # Use Ace=11 if possible.
    naiveSum = sum(cards)
    # Check for aces.
    if 1 in cards:
        if naiveSum < 12:
            return naiveSum+10
        else:
            return naiveSum
    else:
        return naiveSum

def dealerDecision(dealerCards, deck):
    # Choose to hit or stand on current cards.
    dealerMax = 17
    handValue = cardsTotal(dealerCards)
    if handValue > 21:
        return "bust"
    elif handValue < dealerMax:
        return "hit"
    else:
        return "stand"

def dealerPlay(dealerCards, deck):
    # Play as the dealer until deciding to stand.
    decision = "hit"
    while decision == "hit":
        #print("ln 115")
        # Keep playing until decision is not hit.
        decision = dealerDecision(dealerCards, deck)
        #print("ln 118")
        if decision == "hit":
            #print("ln 120")
            newCard = dealCard(deck)
            if(newCard == False):
                print("deck", deck)
                print("dealerCards", dealerCards)
                print("decision", decision)
                temp = raw_input("Error deck is empty")
            dealerCards.append(newCard)

def handValue(hand):
    # Find the value of this hand.
    # Return 0 if bust and 22 if pontoon.
    total = cardsTotal(hand)
    if total > 21:
        return 0
    elif total == 21:
        # Check for a pontoon.
        twoCards = (len(hand) == 2)
        acePresent = 1 in hand
        tenPresent = 10 in hand
        if twoCards and acePresent and tenPresent:
            return 22
        else:
            return 21
    else:
        return total

def findWinner(myCards, dealerCards):
    # Compare my cards and the dealer's cards to see who wins.
    # Return 1 for win or 0 for loss.
    myValue = handValue(myCards)
    dealerValue = handValue(dealerCards)
    if myValue > dealerValue:
        return 1
    else:
        return 0

def getWinChance(myCards, dealerCards, deck, sampleSize=2000):
    # If I stop hitting now what is the chance that I beat the dealer?
    # Sample size of 10000 gives 1% margin in 95% confidence interval.
    winCount = 0
    for i in range(sampleSize):
        deckCopy = copy.copy(deck)
        dealerCardsCopy = copy.copy(dealerCards)
        dealerPlay(dealerCardsCopy, deckCopy)
        winCount += findWinner(myCards, dealerCardsCopy)
    winChance = winCount/sampleSize
    return winChance

def decisionMethod(myCards, dealerCards, deck, sampleSize=200):
    # Use decision method to choose whether to hit or stand.
    # Find the chance that I win if I stop hitting now.
    winChanceNow = getWinChance(myCards, dealerCards, deck)
    
    # Find chance that I win if I hit once more.
    # Average the chances from many possible dealt cards.
    winChanceSum = 0
    for i in range(sampleSize):
        deckCopy = copy.copy(deck)
        myCardsCopy = copy.copy(myCards)
        newCard = dealCard(deckCopy)
        myCardsCopy.append(newCard)
        winChanceSum += getWinChance(myCardsCopy, dealerCards, deck)
    winChanceAfterOne = winChanceSum/sampleSize
    
    # Find chance that I win if I hit twice more.
    # Average the chances from many possible dealt cards.
    winChanceSum = 0
    for i in range(sampleSize):
        deckCopy = copy.copy(deck)
        myCardsCopy = copy.copy(myCards)
        newCard = dealCard(deckCopy)
        myCardsCopy.append(newCard)
        newCard = dealCard(deckCopy)
        myCardsCopy.append(newCard)
        winChanceSum += getWinChance(myCardsCopy, dealerCards, deck)
    winChanceAfterTwo = winChanceSum/sampleSize

    if (winChanceAfterOne+winChanceAfterTwo) > winChanceNow:
        decision = "hit"
    else:
        decision = "stand"
    return decision

def playMyHand(myCards, dealerCards, deck):
    # Play until deciding to stand.
    decision = "hit"
    while decision == "hit":
        # Keep playing until decision is not hit.
        decision = decisionMethod(myCards, dealerCards, deck)
        if decision == "hit":
            newCard = dealCard(deck)
            myCards.append(newCard)

def simulateGame(deck, numberOtherPlayers=0):
    # Play one game with myself and some other players.
    # Deal the dealer's cards
    dealerCards = []
    for i in range(0,2):
        dealerCards.append(dealCard(deck))
    # Show the first of the dealer's cards
    dealerShownCards = dealerCards[0:1]
    
    # Play all the other players' hands.
    for player in range(0, numberOtherPlayers):
        # Deal this player's two cards.
        playerCards = []
        for i in range(0,2):
            playerCards.append(dealCard(deck))
        # Play until they reach 17 or more.
        # Assume that the player plays like the dealer.
        dealerPlay(playerCards, deck)

    # Deal my cards.
    myCards = []
    for i in range(0,2):
        myCards.append(dealCard(deck))
    
    # Play my hand using decision method.
    playMyHand(myCards, dealerShownCards, deck)

    # Play dealer's hand.
    dealerPlay(dealerCards, deck)

    # Find profit.
    outcome = findWinner(myCards, dealerCards)
    if outcome == 0:
        profit = -1
    else:
        profit = 1
    return profit

def getAverageProfit(numberOtherPlayers=0, sampleSize=100):
    # Simulate many games to find expected profit.
    sumProfit = 0
    sumSqProfit = 0
    for game in range(sampleSize):
        print("game",game)
        deck = newDeck()
        profit = simulateGame(deck, numberOtherPlayers=numberOtherPlayers)
        sumProfit += profit
        sumSqProfit += profit**2
    averageProfit = sumProfit / sampleSize
    varianceProfit = (sumSqProfit/sampleSize) - (averageProfit**2)
    profitSignificance = averageProfit / ((varianceProfit/sampleSize)**0.5)
    print("number of other players is " + str(numberOtherPlayers))
    print("Average profit is " + str(averageProfit))
    print("Variance is " + str(varianceProfit))
    print("Significance of profit sign is " + str(profitSignificance))
    print("-------------------------")

for players in range(4,7):
    getAverageProfit(numberOtherPlayers=players)
