


This class represents a named card, each having its own name,\
color, file name, card image for its loaded picture, and location\
if the card ever gets played into a user’s hand. 
'''

#-----------------------------------------------------------------------------
#Imports
import pygame

#-----------------------------------------------------------------------------
#Class
class Card:

  #---------------------------------------------------------------------------
  #Constructor
    def __init__(self, color, number, fileName):
        self.__color = color
        self.__number = number
        self.__fileName = fileName
        self.__cardImage = pygame.image.load(self.__fileName)
        self.__imageLoc = {}

  #---------------------------------------------------------------------------
  #Accessors
        
    def getColor(self):
        return self.__color

    #returns the location of the image
    def getImageLoc(self):
        return self.__imageLoc

    def getNumber(self):
        return self.__number

    def getFileName(self):
        return self.__fileName

    def getCardImage(self):
        return self.__cardImage

    #sets the location of the image
    def setImageLoc(self, card, location):
        self.__imageLoc[card] = location

#-----------------------------------------------------------------------------
#Tester
    
##def main():
##    window = pygame.display.set_mode((500, 500))
##    pygame.init()
##    while True:
##        r = Card("red", 1, "red1.png")
##        for event in pygame.event.get():
##            if event.type == pygame.QUIT: sys.exit()
##
##
##        window.blit(r.getCardImage(), (0,0))
##        pygame.display.flip()
