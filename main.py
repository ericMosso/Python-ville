import random
import sys

#creating a class
class Card:
    #constructor
    def __init__(self, card, suit, value):
        #card constructor
        self.card = card
        self.value = value
        self.suit = suit

    def setValue(self, newValue):
        #we need this for setting aces in blackjack. we need self to refer to the class object itself.
        self.value = newValue


def createDeck():
    #we need a way to initialize all the cards
    #i suggest doing a nested for loops
    newDeck = []

    cards = ["A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2"]
    suits = ["Clubs", "Spades", "Diamonds", "Hearts"]
    cardSets = {
        "A": 11,
        "K": 10,
        "Q": 10,
        "J": 10,
        "10": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2
    }

    #4 suits * 13 card types = 52 cards in a deck
    #we'll initialize the cards accordingly
    for card in cards:
        for suit in suits:
            cardObject = Card(card, suit, cardSets.get(card))
            newDeck.append(cardObject)

    random.shuffle(newDeck)

    return newDeck

def printDealer(hand, cardcount):
  print("Dealer: ")
  print("One card hidden")
  for x in range(cardcount):
    if x > 0:
      print(hand[x].card, hand[x].suit)
  
  print("")

def printPlayer(hand, cardcount):
  print("Player: ")
  for x in range(cardcount):
    print(hand[x].card, hand[x].suit)

  print("")

def sumHand(hand, cardcount):
    hValue = 0
    for x in range(cardcount):
       
        hValue += hand[x].value

    return hValue


def checkHand(hand, cardcount):
    hValue = int(0)
    hValue = sumHand(hand, cardcount)
    # this takes the initial total default value of hand and changes the value of one Ace card at a time based on that
    for x in range(cardcount):
        if (hand[x].card == "A" and hValue > 21):
            hand[x].value = int(1)
        # the new hand value is then updated to the variable for hand value to determine if further changes are necessary
        # this covers for the potential of more than one Ace in a single hand
        hValue = sumHand(hand, cardcount)

    return hValue


def checkWin(dhand, phand, cardCountD, cardCountP, hitme):
    dval = int(0)
    pval = int(0)

    pval = sumHand(phand, cardCountP )
    print(pval)
    dval = sumHand(dhand, cardCountD )
    print(dval, "\n")

    win = False

    if(dval == 0 and pval == 0):
      win = False 
    elif (dval == 21 or pval == 21):
      win == True
      if (dval == 21 and pval != 21):
        print("dEaLeR wInS\n")
      elif (dval == 21 and pval == 21):
        print("pUsH\n")
      else:
        print("pLaYeR wInS\n")
    elif (dval > 21 or pval > 21):
      win = True
      if (dval > 21 and pval <= 21):
        print("PlaYer WiNs")
      elif(dval <= 21 and pval > 21):
        print("dEaLeR wInS")
      elif(dval > 21 and pval > 21):
        if(dval < pval):
          print("dEaLeR wInS")
        elif(dval > pval):
          print("pLaYeR wInS")
        elif(dval == pval):
          print("puSh")
    elif (dval < 21 and pval < 21):
      if (pval > dval and hitme != "1"):
        print("PlaYeR wInS")
        win = True
      elif (pval < dval and hitme != "1"):
        print("dEaLeR wInS")
        win = True
      elif (dval == pval):
        win = True
        print("Push")

    return win


#function that is useful to check if black jacks happen (getting 21 on first two cards)
def checkBlackJack(dhand, phand, cardCountD, cardCountP, win):
  dval = int(0)
  pval = int(0)

  pval = sumHand(phand, cardCountP )
  print("P: " , pval)
  dval = sumHand(dhand, cardCountD )
  print("")

  win = False

  if(dval == 21 or pval == 21):
    win = True
    if(dval == 21 and pval != 21):
      print("Dealer has a Black Jack, Dealer Wins")
    elif(pval == 21 and dval != 21):
      print("Player has a Black Jack, Player Wins")
  
  return win

def appen(deck, hand, cardcount):

    hand.append(deck[0])
    deck.pop(0)
    checkHand( hand, cardcount )

    return hand, deck

###

def main():
  playerHand = []
  dealerHand = []
  deck = []
  pCount = 0
  dCount = 0
  win = False

# asks user if they want to play a game of blackjack
  letsPlay = input("LeT's PlAy? ")

  # creates and shuffles a fresh deck of cards if the user wants to play
  if(letsPlay == "1"):
    letsPlay = True
    print("")
    deck = createDeck()
    random.shuffle(deck)

  # if the user doesn't want to play, output leaves a closing message and program ends
  elif(letsPlay != "1"):
    exitMessage = print("\nnIcE pLaYiNg w/YoU")
    return exitMessage

  # deals the initial 2 cards for user and dealer, prints their hands
  for x in range(2):
    pCount += 1
    appen(deck, playerHand, pCount)
    printPlayer(playerHand, pCount)

    dCount += 1
    appen(deck, dealerHand, dCount)
    printDealer(dealerHand, dCount)

  win = checkBlackJack(dealerHand, playerHand, dCount, pCount, win)
  if(win == True):
    sys.exit()

  hitme = input("Hit? ")

  # asks a player if they want to hit
  if(hitme == "1"):

  # so if the player wants another card, we deal them another card 
    while(hitme == "1"):
      pCount += 1
      appen(deck, playerHand, pCount)
      printPlayer(playerHand, pCount)

    # if the sum of the dealer's cards are below 17, dealers have to hit again
      if(sumHand(dealerHand, dCount) < 17):
        dCount += 1
        appen(deck, dealerHand, dCount)
        printDealer(dealerHand, dCount)
      else:
        printDealer(dealerHand, dCount)

      # asks dealer to deal player another card or not
      hitme = input("Hit? ")
      print("")

      # if the dealer deals another card to the player, also check if dealer needs another card
      if (hitme == "1" and sumHand(playerHand, pCount) < 21):
        continue
        
      elif(hitme != "1"):
        
        # if the player is done hitting, the dealer still might need cards
        while(sumHand(dealerHand, dCount) < 17):
          dCount += 1
          appen(deck, dealerHand, dCount)
          printDealer(dealerHand, dCount)

  else:

    # still need to possibly add to dealer's hand if they are under 17 when player doesn't hit at all from the initial deal
    while(sumHand(dealerHand, dCount) < 17):
      dCount += 1
      appen(deck, dealerHand, dCount)
      printDealer(dealerHand, dCount)

# checks for a winning hand
  checkWin(dealerHand, playerHand, dCount, pCount, hitme)

if __name__ == "__main__":
    main()
