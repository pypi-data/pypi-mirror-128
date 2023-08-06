from .Person import Player, Dealer
from .Card import Card

class Game:
    
    def __init__(self, name):
        '''
        Class representing the game itself
        
        Args: name (string) - player name

        Attributes:
            deck (set of instances of Card) - set of cards, initially empty
            dealer (instance of Dealer) - create new dealer using 'Dealer' as name
            player (instance of Player) - create new player using args 'name'
        '''
        self.deck = set()
        self.dealer = Dealer('Dealer')
        self.player = Player(name)
        
        
    def new_deck(self):
        '''Function to update game.deck with a new deck of cards
            Args: None
            Return:
                new_deck (set of Cards)
        '''
        suits = {'hearts','diamonds','clubs','spades'}
        card_dict = {'ace': [1, 11], 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9,
                   'jack':10, 'queen':10, 'king':10} #card numbers and their values
        new_deck = set()
        for suit in suits:
            for no in card_dict:
                new_deck.add(Card(no, suit, card_dict[no]))
        return new_deck
        
        
    def deal_cards(self):
        '''Function to deal 2 cards each to player and dealer
        '''
        self.deck = self.new_deck() #Create new deck of cards
        self.player.cards = set()
        self.dealer.cards = set()
        for x in range(2):
            self.player.cards.add(self.deck.pop())
            self.dealer.cards.add(self.deck.pop())
        self.print_cards('deal') #Print dealt cards to screen and compare totals

        
    def hit(self):
        '''Function to deal the player 1 additional card, if has chosen to 'hit', then compare totals
        '''
        self.player.cards.add(self.deck.pop())
        if self.player.bust(): #If player has bust (cards total over 21) print results
            self.print_cards('hit')
        else:
            self.dealer_check() #Otherwise update dealer's cards
            self.print_cards('hit')

            
    def dealer_check(self):
        '''Function to add 1 card to the dealer's hand if current total < 17
        '''
        value = self.dealer.sum_cards()
        if isinstance(value, list):
            if value[1] < 17:
                self.dealer.cards.add(self.deck.pop())
        else:
            if value < 17:
                self.dealer.cards.add(self.deck.pop())
        
        
    def stick(self):
        '''If player chooses to 'stick', function to add to the dealer's cards until cards value = 17 or bust
        '''
        while self.dealer.max_card_value() < 17:
            self.dealer_check()
        self.print_cards('stick') #Print dealt cards to screen and compare totals
    
    
    def print_cards(self, hit_stick):
        '''Function to print players and dealer cards to screen and compare totals
        '''
        self.player.print_cards()
        self.dealer.print_cards()
        self.compare_card_values(hit_stick)
    
    def compare_card_values(self, hit_stick):
        '''Function to compare player and dealer card total values to determine player win or lose
        
            Args:
                hit_stick (string) - the name of the function calling for the comparison
                                    if is 'stick' then no further game play, so compare final totals
        '''
        p_value = self.player.max_card_value()
        d_value = self.dealer.max_card_value()
        
        #If player has 21 or dealer is bust then print win
        if (p_value == 21 and d_value != 21) or (p_value < 21 and d_value > 21):
            self.print_win_lose('win')
        
        #If player is bust or dealer has 21 then print lose
        elif (p_value > 21) or (p_value != 21 and d_value == 21) :
            self.print_win_lose('lose')

        #If player has chosen to stick then player wins if total is greater than dealer's
        elif hit_stick == 'stick':
            if p_value > d_value:
                self.print_win_lose('win')
            elif p_value == d_value:
                self.print_win_lose('draw')
            else:
                self.print_win_lose('lose')
                
                
    def print_win_lose(self, win_lose):
        '''Function to print win or lose results to screen and update player's score
        '''
        if win_lose == 'win':
            print('Congratulations! You win')
            self.player.score += 1
        elif win_lose == 'lose':
            print('Sorry. You lose')
            self.player.score -= 1
        else:
            print('Its a draw. Play again?')
        print('{}\'s Score: {}'.format(self.player.name, self.player.score))
        
