from random import shuffle

burst_boader = 21   #バーストのボーダーライン
ACE_BONUS = 11  #Aを11として運用するボーダーライン
ELEVEN_ACE = 10 #Aを11にする変数
number_of_cards_remaining = 10  #山札を切りなおすボーダーライン

def decks_shuffle():
    suits = ["♠", "♥", "♦", "♣"]
    ranks = [str(i) for i in range(2, 11)] + ['A', 'J', 'Q', 'K']
    decks = [f"{suit}{rank}" for suit in suits for rank in ranks]
    shuffle(decks)
    return decks

def get_hand_sum(card):
    rank = card[1:]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 1
    else:
        return int(rank)

def ACE_check(hands, total, A):
    if any(card[1:] == 'A' for card in hands) and total <= ACE_BONUS:
        total += ELEVEN_ACE
        A = True
    elif total > burst_boader and A:
        total -= ELEVEN_ACE
        A = False
    return total, A

def calculation(hands, A):
    total = sum(get_hand_sum(card) for card in hands)
    return ACE_check(hands, total, A)


def put(hands, A, deck):
    card = deck.pop(0)
    hands.append(card)
    total, A = calculation(hands, A)
    return hands, total, A, deck

def win_or_lose(player_total, dealer_total):
    if player_total == dealer_total:
        print("Draw")
        return 0
    elif (player_total > dealer_total and (player_total <= burst_boader and dealer_total <= burst_boader)) or (player_total <= burst_boader and dealer_total > burst_boader):
        print("You win!!")
        return 1
    else:
        print("You lose...")
        return -1

def check_chip(win_or_lose, bet):
    if win_or_lose == 1:
        return bet * 2
    elif win_or_lose == 0:
        return bet
    else:
        return 0

chips = 5000
deck = []

discribute = 2  #カードを配る回数
blackjack = 21
dealer_stop = 20    #ディーラーがプレイする手札合計の上限(公式ルールは17らしい。どんでん返しがあるほうがおもろいやん？)

player_total = dealer_total = 0
while chips >= 0:
    print()
    #山札シャッフル
    if len(deck) <= number_of_cards_remaining:
        deck = decks_shuffle()
        print("Shuffle completed")

    player_hands, dealer_hands = [], []
    player_A = dealer_A = False

    #カード配り
    for _ in range(discribute):
        player_hands.append(deck.pop(0))
        dealer_hands.append(deck.pop(0))

    print("Your chips:", chips)
    bet = int(input("How many chips do you bet?\n 0: end\n"))
    bet = abs(bet)
    if bet == 0:
        break
    chips -= bet

    #手札の合計算出。Aは11として運用し、あることをマーク。
    print("------------------------")
    player_total, player_A = calculation(player_hands, player_A)
    dealer_total, dealer_A = calculation(dealer_hands, dealer_A)
    print(f"your hand is {', '.join(player_hands)}\n total: {player_total}")
    print(f"dealer's hand is {dealer_hands[0]}, ?")
    print("------------------------")

    #ブラックジャック判定
    Blackjack = False
    if player_total == blackjack or dealer_total == blackjack:
        Blackjack = True

    #プレイヤーのターン
    while player_total < burst_boader and not Blackjack:

        command = input("put(1) or stand(0)?: ")
        if command == "put" or command == '1':
            player_hands, player_total, player_A, deck = put(player_hands, False, deck)
            print("Now, your hands:", ', '.join(player_hands))
            print("Your total:", player_total)
        elif command == "stand" or command == '0':
            break
        else:
            print(f"This command is not supported: {command}")
    
    #ディーラーのターン
    player_burst = player_total > burst_boader
    while dealer_total < player_total and dealer_total < burst_boader and not player_burst and not Blackjack:
        dealer_hands, dealer_total, dealer_A, deck = put(dealer_hands, False, deck)
    
    #集計
    print("-----------------------------")
    chips += check_chip(win_or_lose(player_total, dealer_total), bet)

    print("\nplayer")
    if player_total == blackjack and Blackjack:
        print(f"{', '.join(player_hands)}, total: {player_total}, Blackjack!!")
    elif player_burst:
        print(f"{', '.join(player_hands)}, total: {player_total}, Burst!!")
    else:
        print(f"{', '.join(player_hands)}, total: {player_total}")
    print("dealer")
    if dealer_total == blackjack and Blackjack:
        print(f"{', '.join(dealer_hands)}, total: {dealer_total}, Blackjack!!")
    elif dealer_total > burst_boader:
        print(f"{', '.join(dealer_hands)}, total: {dealer_total}, Burst!!")
    else:
        print(f"{', '.join(dealer_hands)}, total: {dealer_total}")
    print("-----------------------------")

if chips < 0:
    print("Game over")
    print("You have no chips.")
else:
    print("Final result:")
    print(f"chips: {chips}")