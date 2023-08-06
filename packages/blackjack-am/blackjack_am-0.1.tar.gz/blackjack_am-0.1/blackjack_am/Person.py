from .Card import Card

class Person:

    def __init__(self, name):
        '''
        Generic parent class representing a game participant

        Attributes:
            name (string) - participant name
            cards (set) - set of cards the participant has been dealt
        '''
        self.name = name
        self.cards = set()
        
        
    def print_cards(self):
        '''Function to print to screen all participant's cards and their summed value
        '''
        print('{}\'s Cards:'.format(self.name))
        for card in self.cards:
            card.print_card()
        print('{}\'s Cards Value: {}\n'.format(self.name, self.sum_cards()))
    
    
    def sum_cards(self):
        '''Function to sum participant's cards value
            Args: None
            Return:
                value (int or list of [int, int])
        '''
        #Set zero value as list so that both possible ace [1, 11] values can be added to it
        value = [0, 0]
        
        #Separate any aces from the non-ace cards
        aces = [x for x in self.cards if x.card_no == 'ace']
        non_ace_cards  = [x for x in self.cards if x.card_no != 'ace']
        
        #Only add both ace values for the 1st occurance of an ace in the participant's hand
        #Any more +11s will only cause the hand to bust so is not a real option
        x=1
        for card in aces:
            if x == 1:
                value[0] += card.value[0]
                value[1] += card.value[1]
                x += 1
            else:
                value[0] += card.value[0]
                value[1] += card.value[0]
        
        #For non-ace cards add card values to both value list items
        for card in non_ace_cards:
            value[0] += card.value
            value[1] += card.value
        
        #If both summed elements are the same then no ace has been involved and just return 1 value
        if value[0] == value[1]:
            return value[0]
        else:
            if value[1] > 21: #If the larger element is over 21 then it's bust so just return 1st element
                return value[0]
            else:
                return value
    
    
    def max_card_value(self):
        '''Function to return the maximum value of the participant's cards, if there is a choice of 2
            Args: None
            Return:
                value (int)
        '''
        if isinstance(self.sum_cards(), list):
            value = self.sum_cards()[1]
        else:
            value = self.sum_cards()
        return value
    

class Dealer(Person):

    def __init__(self, name):
        '''
        Child class inheriting from Person, representing the dealer of the game

        Attributes:
            name (string) - dealer name
            cards (set) - set of cards the dealer has been dealt
        '''
        Person.__init__(self, name)
        
    
class Player(Person):
    
    def __init__(self, name):
        '''
        Child class inheriting from Person, representing the game player

        Attributes:
            name (string) - player name
            cards (set) - set of cards the player has been dealt
            score (int) - player score
        '''
        Person.__init__(self, name)
        self.score = 0
        
    
    def bust(self):
        '''Function to return True if the player's cards total over 21
            Args: None
            Return:
                Boolean
        '''
        if self.max_card_value() > 21:
            return True
        else:
            return False

