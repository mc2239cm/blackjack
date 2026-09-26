from random import shuffle

burst_border = 21   #バーストのボーダーライン
ACE_BONUS = 11  #Aを11として運用するボーダーライン
ELEVEN_ACE = 10 #Aを11にする変数
number_of_cards_remaining = 10  #山札を切りなおすボーダーライン

class DeckManager:
    def __init__(self):
        self.cards = []
    
    def shuffle_if_needed(self):
        if len(self.cards) <= number_of_cards_remaining:
            suits = ["♠", "♥", "♦", "♣"]
            ranks = [str(i) for i in range(2, 11)] + ['A', 'J', 'Q', 'K']
            self.cards = [f"{suit}{rank}" for suit in suits for rank in ranks]
            shuffle(self.cards)
            print("Shuffle Compleated")
    
    def draw(self):
        return self.cards.pop(0)


class HandManager:
    def __init__(self):
        self.hands = []
        self.has_A = False
    
    def total(self):
        base_total = sum(self.get_card_value(card) for card in self.hands)

        self.has_A = any(card[1:] == 'A' for card in self.hands)
        if self.has_A and base_total <= ACE_BONUS:
            base_total += ELEVEN_ACE

        return base_total

    def get_card_value(self, card):
        rank = card[1:]
        if rank == 'A':
            return 1
        elif rank in ['J', 'Q', 'K']:
            return 10
        else:
            return int(rank)

    def add_cards(self, card):
        self.hands.append(card)


class PlayerManager:
    def __init__(self):
        self.chips = 5000
    
    def check_chip(self, win_or_lose, bet):
        if win_or_lose == 1:
            return bet * 2
        elif win_or_lose == 0:
            return bet
        else:
            return 0
    
    def win_or_lose(self, player_total, dealer_total):
        if player_total == dealer_total:
            print("Draw")
            return 0
        elif (player_total > dealer_total and (player_total <= burst_border and dealer_total <= burst_border)) or (player_total <= burst_border and dealer_total > burst_border):
            print("You win!!")
            return 1
        else:
            print("You lose...")
            return -1


Player = PlayerManager()
Deck = DeckManager()

discribute = 2  #カードを配る回数
blackjack = 21  #バーストのボーダーライン
dealer_stop = 20    #ディーラーがプレイする手札合計の上限(公式ルールは17)

while Player.chips > 0:
    Deck.shuffle_if_needed()

    player_hands = HandManager()
    dealer_hands = HandManager()

    for _ in range(discribute):
        player_hands.add_cards(Deck.draw())
        dealer_hands.add_cards(Deck.draw())

    print("Your chips:", Player.chips)
    bet = int(input("How many chips do you bet?\n 0: end\n"))
    bet = abs(bet)
    if bet == 0:
        break
    Player.chips -= bet

    print("------------------------")
    print(f"your hand is {', '.join(player_hands.hands)}\n total: {player_hands.total()}")
    print(f"dealer's hand is {dealer_hands.hands[0]}, ?")
    print("------------------------")

    isBlackjack = (player_hands.total() == blackjack or dealer_hands.total() == blackjack)

    #プレイヤーのターン
    while player_hands.total() < burst_border and not isBlackjack:
        command = input("put(1) or stand(0)?: ")
        if command in ["put", "1"]:
            player_hands.add_cards(Deck.draw())
            print("Now, your hands:", ', '.join(player_hands.hands))
            print("Your total:", player_hands.total())
        elif command in ["stand", "0"]:
            break
        else:
            print(f"This command is not supported: {command}")
    
    player_burst = player_hands.total() > burst_border
    while dealer_hands.total() < player_hands.total() and dealer_hands.total() < burst_border and not player_burst and not isBlackjack:
        dealer_hands.add_cards(Deck.draw())
    
    print("-----------------------------")
    Player.chips += Player.check_chip(Player.win_or_lose(player_hands.total(), dealer_hands.total()), bet)
    print("\nplayer")
    if player_hands.total() == blackjack and isBlackjack:
        print(f"{', '.join(player_hands.hands)}, total: {player_hands.total()}, Blackjack!!")
    elif player_burst:
        print(f"{', '.join(player_hands.hands)}, total: {player_hands.total()}, Burst!!")
    else:
        print(f"{', '.join(player_hands.hands)}, total: {player_hands.total()}")
    print("dealer")
    if dealer_hands.total() == blackjack and isBlackjack:
        print(f"{', '.join(dealer_hands.hands)}, total: {dealer_hands.total()}, Blackjack!!")
    elif dealer_hands.total() > burst_border:
        print(f"{', '.join(dealer_hands.hands)}, total: {dealer_hands.total()}, Burst!!")
    else:
        print(f"{', '.join(dealer_hands.hands)}, total: {dealer_hands.total()}")
    print("-----------------------------")

if Player.chips <= 0:
    print("Game over")
    print("You have no chips.")
else:
    print("Final result:")
    print(f"chips: {Player.chips}")
