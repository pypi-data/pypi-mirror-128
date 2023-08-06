class Card:
    
    def __init__(self, number, suit, value):
        '''
        Class representing an individual playing card

        Attributes:
            number (string or int) - card name or number
            suit (string) - card suit: hearts, diamonds, clubs or spades
            value (int or list of [int, int] ) - card value, or if the card is an ace, list of card values (1 or 11)
        '''
        self.card_no = number
        self.suit = suit
        self.value = value
        
        
    def print_card(self):
        '''Function to print to screen the card number and suit
        '''
        print('{} of {}'.format(self.card_no, self.suit))
