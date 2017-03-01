

#-----------------------------------------------------------------------------
#Imports

from classPlayer import *
from classCard import *
import random

#-----------------------------------------------------------------------------
#Constants

#assigns colors to a global constant 
RED = "red"
BLUE = "blue"
GREEN = "green"
YELLOW = "yellow"
#wild cards are assigned to black color 
BLACK = "black"
#all action cards are assigned to numbers 
SKIP = 10
DRAW_TWO = 11
WILD = 12
DRAW_FOUR_WILD = 13

#-----------------------------------------------------------------------------
#Class

class Game:
    
  #---------------------------------------------------------------------------
  #Constructor
    
    def __init__(self, playerOne, playerTwo):
        self.__playerOne = (playerOne)
        self.__playerTwo = (playerTwo)
        self.__turnStatus = playerOne
        self.__deck = []
        self.__discardPile = []
        self.__colorStatus = None
        self.__numberStatus = None
        self.__discardCard = None


  #---------------------------------------------------------------------------
  #Accessors
        
    def getPlayerOne(self):
        return self.__playerOne

    def getPlayerTwo(self):
        return self.__playerTwo

    def getDeck(self):
        return self.__deck

    def getNumberStatus(self):
        return self.__numberStatus

    def getTurnStatus(self):
        return self.__turnStatus

    def getDiscardPile(self):
        return self.__discardPile

    def getColorStatus(self):
        return self.__colorStatus
  #---------------------------------------------------------------------------
  #Mutators
    
        #create 108 instances of Card class
        #25 of each color
        #2 of each rank: red, green, blue, yellow, 1-9, skip, draw two
            #one zero each color
            #leave out reverse for now
            #10 = skip
            #11 = draw two
        #4 wilds, 4 wild draw four --> black color \
        # (so we don't have to make a whole new class)
    def fillDeck(self):
        try:
            for i in range(1, 12):
                r = Card(RED, i, "red"+str(i)+".png")
                b = Card(BLUE, i, "blue" + str(i) + ".png")
                g = Card(GREEN, i, "green" + str(i) + ".png")
                y = Card(YELLOW, i, "yellow" + str(i) + ".png")
                self.__deck.append(r)
                self.__deck.append(b)
                self.__deck.append(g)
                self.__deck.append(y)
    #            return r.getCardImage()
            for card in range(4):
                w = Card("black", 12, "black12.png")
                fw = Card("black", 13, "black13.png")
                self.__deck.append(w)
                self.__deck.append(fw)
        except FileNotFoundError as err:  # outer exception\
            #handler for infile open
            print("\nFile not found:  deleted or in wrong folder?\
\n" + str(err) + '\n')
        except IOError as err: # outer exception handler for infile open
            print("\nException raised during open of input file, \
try a different file: \n" + str(err) + '\n')
        except Exception as err: # outer exception handler for infile open
            print("\nData cannot be read:  \n" + str(err) + '\n')


    #begins the game by randomly picking a starting card which sets the
            #game's beginning color and number status
            #this starts the discard pile for the game
    #deals seven cards to both players 
    def startGame(self):
        startingCard = (random.choice(self.__deck))
        while startingCard.getNumber() > 9:
            startingCard = (random.choice(self.__deck))
        self.__deck.remove(startingCard)
        self.__discardPile.append(startingCard)
        self.__colorStatus = startingCard.getColor()
        self.__numberStatus = startingCard.getNumber()
        self.__discardCard = startingCard
        for aCard in range(7): 
            theCard = random.choice(self.__deck)
            self.__playerOne.receiveCard(theCard)
            self.__deck.remove(theCard)
        for aCard in range(7): 
            theCard = random.choice(self.__deck)
            self.__playerTwo.receiveCard(theCard)
            self.__deck.remove(theCard)

    #param1: player (str) - the player whose turn it is
    #this method checks to see if the player has any available plays
            #if so, then they must play that card
    def canPlay(self, player):
        playersHand = player.getHand()
        for card in playersHand:
            cardNum = card.getNumber()
            cardColor = card.getColor()
            if (self.validPlay(cardColor, cardNum)):
                return self.validPlay(cardColor, cardNum)
            

    #param1: player (str) - the player whose turn it is
    #param2: card (str) - the card in play
    #when clicked, the card is placed at the top of the discard pile after
            #validPlay() is called and returns True
            #if the card's number if greater than 9 i.e. a special card
                #specialCard() is called 
    def playCard(self, player, card):
        cardColor = card.getColor()
        cardNumber = card.getNumber()
        if not self.validPlay(cardColor, cardNumber):
            self.sameTurn()
        else:
            if cardNumber > 9:
                self.specialCard(player, card)
            else:
                self.__colorStatus = cardColor
                self.__numberStatus = card.getNumber()
                self.nextTurn()
            self.__discardPile.append(card)
            playerHand = player.getHand()
            if card in playerHand:
                playerHand.remove(card)

    #param1: player (str) - the player whose turn it currently is
    #param2: card (str) - the card in play 
    #called if the card number in play is greater than nine     
    def specialCard(self, player, card):
        cardNum = card.getNumber()
        cardColor = card.getColor()
        if cardNum == SKIP:
            self.sameTurn()
            self.__colorStatus = cardColor
            self.__numberStatus = cardNum 
        elif cardNum == DRAW_TWO:
            self.drawTwo(player)
            self.sameTurn()
            self.__colorStatus = cardColor
            self.__numberStatus = cardNum
        elif cardNum == WILD:
            self.wildCard()
            self.nextTurn()
            self.__numberStatus = cardNum
        else:
            self.wildFourCard(player)
            self.sameTurn()
            self.__numberStatus = cardNum
            
    #this method is called whenever the action card: Draw Two is played
    #when the cards are removed from the deck this method also checks
            #to see if the deck is empty or not, if it is it adds a new
            #deck to refill it 
    def drawTwo(self, player):
        if player == self.__playerOne:
            playerGetCard = self.__playerTwo
        else:
            playerGetCard = self.__playerOne
        for i in range(2):
            newCard = random.choice(self.__deck)
            self.__deck.remove(newCard)
            if self.__deck == []:
                self.fillDeck()
            playerGetCard.receiveCard(newCard)


    #this method is called whenever the action card: wild is played
            #it takes in a user input asking for an update to the color status
            #it then proceeds to validate that input with colorValidated()
    def wildCard(self):
        newColor = input("What color would you like to choose?")
        newColor = newColor.strip()
        while not self.colorValidated(newColor):
            print("Try again")
            newColor = input("What color would you like to choose?")
            newColor = newColor.strip()
        self.__colorStatus = newColor 


    #param1: player (str) - the player whose turn the game is currently on
    #this method is called whenever the action card: wild four is played
    #it calls the wildCard method
    #it adds four random cards to the opponent's hand
            #after each card it checks the main deck to see if it needs to be
            #refilled 
    def wildFourCard(self, player):
        self.wildCard()
        if player == self.__playerOne:
            playerGetCard = self.__playerTwo
        else:
            playerGetCard = self.__playerOne
        for i in range(4):
            newCard = random.choice(self.__deck)
            self.__deck.remove(newCard)
            if self.__deck == []:
                self.fillDeck()
                print("reshuffling")
            playerGetCard.receiveCard(newCard)

    #param1: player (str) - the player whose turn the game is currently one
    #draws a card if there is no valid play and checks the deck to see if it
            #needs to be refilled after drawing
    def drawCard(self, player):
        newCard = random.choice(self.__deck)
        self.__deck.remove(newCard)
        if self.__deck == []:
            self.fillDeck()
            print("reshuffling")
        player.receiveCard(newCard)
        self.nextTurn()

    #called if the turn is remaining the same
            #this occurs after a skip,a draw two, and a wild draw four
    def sameTurn(self):
        if self.__turnStatus == self.__playerOne:
            self.__turnStatus = self.__playerOne
        else:
            self.__turnStatus = self.__playerTwo

    #called after a valid play of card numbers one through nine and a wild 
    def nextTurn(self):
        if self.__turnStatus == self.__playerOne:
            self.__turnStatus = self.__playerTwo
        else:
            self.__turnStatus = self.__playerOne


    #param1: color (str) - color of the card in play
    #param2: number (str) - number of the card in play
    #compares the color and number of the card to the current color and
        #number status of the game
    def validPlay(self, color, number):
        return color == self.__colorStatus or number == \
               self.__numberStatus or number > 11

    #param1: color (str) - the color the user chooses after a wild
    #checks to see if the user chose a valid color for the new color status
    def colorValidated(self, color):
        return color.lower() == RED or color.lower() == BLUE or color.lower() \
               == GREEN or color.lower() == YELLOW

