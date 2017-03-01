

#-----------------------------------------------------------------------------
#Class

class Player:

  #---------------------------------------------------------------------------
  #Constructor
    
    def __init__(self, name, num):
        self.__name = name
        self.__hand = []
        self.__cardPos = {}
        self.__startPos = num
        self.__windowPos = ()

  #---------------------------------------------------------------------------
  #Accessors
        
    def getName(self):
        return str(self.__name)

    def getHand(self):
        return self.__hand

    #returns the cooridnate position of the card
    def getCardPos(self):
        return self.__cardPos

    #returns the starting posiiton of the card
    def getStartPos(self):
        return self.__startPos

    #param1: aCard (key) - number of the card in play
    #has the player 'receive' a card by having it append to the hand list
    def receiveCard(self, aCard):
        self.__hand.append(aCard)


