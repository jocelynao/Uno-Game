'''
Jocelyn Ao and Sam Testa
Professor Williams
Lab Section B57 
Final Project
'''

from pygame import *
import sys
from classCard import *
from classPlayer import *
from classGame import *

'''
This class is a GUI interface that sets up a screen and simulates an
uno game. Each of the player's cards are displayed and so is the discard
pile. The person has to click on the card they want to play and that
card, if valid, will be taken out of the person's hand and placed into
the discard pile. The goal of the game is to get rid all of cards. The
class makes use of the Game, Card, and Player class. This Uno class
can start an Uno game, move a player's card into the discard pile, and
draw a card if there's no play available.
'''

class Uno:

#Class Variables ----------------------------------------------------   

    FIVE_HUNDRED = 500

 # Card Measurements
    PIC_LENGTH = 40
    PIC_HEIGHT = 70
    
 # Starting Card Position
    START_CARD_X = 300
    START_CARD_Y = 200
    
 # Spacing between each of the card
    THE_SPACING = 50

 # Measurements of the boxes that cover the player's hand
    COVER_LENGTH = 1000
    COVER_ONE_HEIGHT = 100
    COVER_TWO_HEIGHT = 200
    COVER_Y = 400

 # Measurement of the window
    WINDOW_X = 800
    WINDOW_Y = 500

 # Player's two hand position
    PLAYER_TWO_CARD_POSITION = 400

 # The positions of the texts that will appear in the game
    FONT_TITLE_PLACE = 300
    FONT_PLACE_X = 500
    FONT_PLACE_Y_ONE = 150
    FONT_PLACE_Y_TWO = 300
    WIN_FONT_PLACE = 100

 # Text size
    WIN_FONT_SIZE = 100
    FONT_SIZE = 20

 # Color RGB Model
    GREEN = ((0, 204, 0))
    DARK_GREEN = (0, 102, 0)
    BLACK = (0 , 0, 0)

#Constructor -------------------------------------------------------
    
 # Begins the game by creating the players and an Uno game.
    def __init__(self):
        
        pygame.init()        
   # Creates the players
        self.__playerOne = Player("Player 1", 0)
        self.__playerTwo = Player("Player 2", Uno.PLAYER_TWO_CARD_POSITION )
   # Creates the game
        self.__unoGame = Game(self.__playerOne, self.__playerTwo)
   # Creates the window and fills it with color
        self.__window = display.set_mode((Uno.WINDOW_X, Uno.WINDOW_Y))
        self.__window.fill(Uno.GREEN)
   # Creates the fonts
        self.__winFont = pygame.font.SysFont("Arial", Uno.WIN_FONT_SIZE)
        self.__theFont = pygame.font.SysFont("Arial", Uno.FONT_SIZE)
   # Sets up the beginning screen
        self.__window.blit(self.__theFont.render("Welcome to Uno! It's Player\
1's Turn. Click the card to start!", True, (Uno.BLACK)),\
                           (Uno.FONT_TITLE_PLACE, Uno.FONT_TITLE_PLACE))
        pygame.draw.rect(self.__window, Uno.DARK_GREEN, (0, 0, \
                                                         Uno.COVER_LENGTH,\
                                                         Uno.COVER_ONE_HEIGHT))
        pygame.draw.rect(self.__window, Uno.DARK_GREEN, (0, Uno.COVER_Y, \
                                                         Uno.COVER_LENGTH,\
                                                         Uno.COVER_TWO_HEIGHT))
   # Loads the music
        mixer.music.load("Tetris_theme_with_download_.ogg")
        mixer.music.play(-1)
   # Begins the game
        self.beginGame()
        running = True
# Runs the game -------------------------------------------------------------  
        while running:
            # Quits if the person presses the X button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                # Does something if the person clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Displays the ending screen if a person wins
                    # Invokes displayEnd()
                    if self.gameOver():
                        self.__displayEnd()
                    else:
                        # This is initialized to none because from
                        #  the start, there has not been an invalid card played
                        wrongPlay = None
                        thePlayer = self.__unoGame.getTurnStatus()
                        # Allows a person to play a turn if they can
                        # If a person clicks on the card, that card will be
                        #  removed from the person's hand and placed into
                        #  the discard pile if the card is a valid play.
                        #  The program sees if a person has clicked on the
                        #  card by obtaining the mouse positions and the
                        #  card's rectangle position and seeing if the two
                        #  collide
                        # Invokes getStartPos(), getCardPos(), get_pos(), \
                        #  collidepoint(), playCard(), getDiscardPile(), pop()
                        if self.__unoGame.canPlay(thePlayer):
                            aDict = thePlayer.getCardPos()
                            # This is initialized to none because for now
                            #  the card the person plays does not match
                            #  the card that is in the discard pile
                            hitCard = None
                            mousePos = pygame.mouse.get_pos()
                            for (aCard, aPos) in aDict.items():
                                if aPos.collidepoint(mousePos):
                                    self.__unoGame.playCard(thePlayer, aCard)
                                    discardPile = self.__unoGame.getDiscardPile()
                                    discardCard = discardPile[-1]
                                    if discardCard == aCard:
                                        hitCard = discardCard
                                    cardNum = aCard.getNumber()
                                    cardColor = aCard.getColor()
                                    if not self.__unoGame.validPlay(cardColor, cardNum):
                                        wrongPlay = aCard
                            aDict.pop(hitCard, None)
                        # Draws a card for the user if a person has no
                        #  playable cards
                        # Invokes getTurnStatus(), drawCard(), displayGame()
                        else:
                            thePlayer = self.__unoGame.getTurnStatus()
                            self.__unoGame.drawCard(thePlayer)
                        self.__displayGame(thePlayer)
                        # Prints out whether a card is a valid play or not
                        if wrongPlay != None:
                            self.__window.blit(self.__theFont.render("Not a \
valid play!", True, (Uno.BLACK)), (100, 200))
##                        if not self.__unoGame.validPlay(aCard.getColor(), aCard.getNumber()):
##                            self.__window.blit(self.__theFont.render("Not a valid play!", True,\
##                                               (Uno.BLACK)), (300, 300))

                pygame.display.flip()
        mainloop()

#Functions -----------------------------------------------------------------

    #Begins the game by filling the deck of cards, distributing the cards to
    #  the players, and displaying the initial starting card for the game
    #Invokes fillDeck(), startGame(), and displayPile()
    def beginGame(self):
        self.__unoGame.fillDeck()
        self.__unoGame.startGame()
        self.__displayPile()


    #Displays the ending screen when the game ends
    #Invokes getHand(), getPlayerOne(), getPlayerTwo(), getName()
    def __displayEnd(self):
        if self.__playerOne.getHand() == []:
            theWinner = self.__unoGame.getPlayerOne()
        else:
            theWinner = self.__unoGame.getPlayerTwo()
        self.__window.fill(Uno.GREEN)
        self.__window.blit(self.__winFont.render\
                           (theWinner.getName() + " won!",\
                            True, (Uno.BLACK)), \
                           (Uno.WIN_FONT_PLACE,\
                            Uno.WIN_FONT_PLACE))

    #Invokes the functions needed to display all the features of the
    #  game
    #Invokes getCardPos(), getStartPos(), displayPile(), displayHand(),
    #  render(), modifyWindow()
    def __displayGame(self, thePlayer):
        cardPosOne = self.__playerOne.getCardPos()
        cardPosTwo = self.__playerTwo.getCardPos()
        startPosOne = self.__playerOne.getStartPos()
        startPosTwo = self.__playerTwo.getStartPos()
        self.__window.fill(Uno.GREEN)
        self.__displayPile()
        self.__displayHand(self.__playerOne, startPosOne, cardPosOne)
        self.__displayHand(self.__playerTwo, startPosTwo, cardPosTwo)
        self.__window.blit(self.__theFont.render("Turn Status: " + \
                                    thePlayer.getName(), \
                                   True, (Uno.BLACK)), (Uno.FONT_PLACE_X,\
                                                    Uno.FONT_PLACE_Y_ONE))
        self.__window.blit(self.__theFont.render("Color Status: " + \
                                   self.__unoGame.getColorStatus(),\
                                   True, (Uno.BLACK)), (Uno.FONT_PLACE_X,\
                                                    Uno.FONT_PLACE_Y_TWO))
        self.__modifyWindow(thePlayer)

    #Displays the discard pile
    #Invokes getDiscardPile(), getCardImage(), scale(), blit()
    def __displayPile(self):
        thePile = self.__unoGame.getDiscardPile()
        startCard = thePile[-1]
        startImage = startCard.getCardImage()
        newImage = transform.scale(startImage, \
                                   (Uno.PIC_LENGTH, Uno.PIC_HEIGHT))
        self.__window.blit(newImage, (Uno.START_CARD_X, Uno.START_CARD_Y))

    #Displays each of the persons hand and places them in the correct spot.
    #  It saves all of the card and its positions into a dictionary that is
    #  related to the individual player
    #Invokes getHand(), getCardImage(), scale(), blit()
    def __displayHand(self, aPlayer, y, aDict):
        x = 0
        for card in aPlayer.getHand():
            theImage = card.getCardImage()
            newImage = transform.scale(theImage, (Uno.PIC_LENGTH, \
                                                  Uno.PIC_HEIGHT))
            imageLoc = self.__window.blit(newImage, (x, y))
            x = x + Uno.THE_SPACING
            aDict[card] = imageLoc
        return aDict

    #Covers the person's hand that's not currently playing
    #Invokes getPlayerOne(), rect(), getPlayerTwo()
    def __modifyWindow(self, thePlayer):
        playerOne = self.__unoGame.getPlayerOne()
        if playerOne != thePlayer:
            pygame.draw.rect(self.__window, Uno.DARK_GREEN, (0, 0, Uno.COVER_LENGTH,\
                                             Uno.COVER_ONE_HEIGHT))
        playerTwo = self.__unoGame.getPlayerTwo()
        if playerTwo != thePlayer:
            pygame.draw.rect(self.__window, Uno.DARK_GREEN, (0, Uno.COVER_Y, \
                                                             Uno.COVER_LENGTH, \
                                                             Uno.COVER_TWO_HEIGHT))

    #Predicate function
    #Returns true if one of the player's hand is empty (bool)
    #Invokes getHand()
    def gameOver(self):
        return self.__playerOne.getHand() == [] or \
               self.__playerTwo.getHand() == []
    ##    if player == game.getPlayer1():
    ##        print("HI")
                

Uno()
