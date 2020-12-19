
import os
import sys
import random 

class BankruptStat:
    def __init__(self,turn, winner = None):
        self.turn = turn
        self.winner = winner

class Bankrupt:

    def __init__(self,houses):
        self.houses = houses
        self.players = []

    def add_player(self,player):
        self.players.append(player)

    def run(self):
        self.sort_player_order()
        return self.game_loop()

    def game_loop(self):

        for turn in range(1, 1001):
            self.update()
            winner = self.has_winner()
            
            if winner != None:
                return BankruptStat(turn, winner.tag)

        winner = self.players[0]

        for player in self.players:
            if player.coins > winner.coins:
                winner = player
        
        return BankruptStat(1000, winner.tag)
                

    def has_winner(self):
        players_in_game = [player for player in self.players if player.is_active()]
        if len(players_in_game) == 1:
            return players_in_game[0]
        
        return None

    def update(self):
        for player in self.players:
            #print(player.is_active())
            if player.is_active():
                self.action(player)

    def sort_player_order(self):
        random.shuffle(self.players)


    def buy_house(self,house, buyer):
        assert house.owner == None
        assert buyer.coins >= house.buy_price
        buyer.coins -= house.buy_price
        house.owner = buyer
    
    def rent_house(self,house, tenent):
        #assert house.owner != tenent
        #assert house.owner != None
        #print("hey")
        if house.rent_price > tenent.coins:
            house.owner.coins += tenent.coins
        else:
            house.owner.coins += house.rent_price

        tenent.coins -= house.rent_price
        #print( tenent.coins - house.rent_price)

    def remove_player(self,player):
        player.active = False

        for house in houses:
            if house.owner == player:
                house.owner = None

    def action(self,player):
        player.move(random.randint(1,6))
        house = self.houses[player.position-1]
        #print(house.owner)
        if house.owner != player:
            if house.owner == None:
                if player.should_buy_house(house):
                    self.buy_house(house, player)
            else:
                self.rent_house(house, player)
            
        if player.coins < 0:
            self.remove_player(player)


class House:
    def __init__(self,buy_price, rent_price):
        self.buy_price = buy_price
        self.rent_price = rent_price
        self.owner = None


class Player:
    def __init__(self,bankrupt, tag):
        self.coins = 300
        self.position = 1
        self.active = True
        self.tag = tag
        self.bankrupt = bankrupt

    def should_buy_house(self,house):
        return self.coins >= house.buy_price

    def move(self,steps):
        self.position += steps
        
        if self.position > 20:
            self.coins += 100
            self.position -= 20
        
    def is_active(self):
        return self.active


class PlayerImpulsive(Player):
    def __init__(self, bankrupt, tag):
        super().__init__(bankrupt, tag)
    
    def should_buy_house(self,house):
        return super().should_buy_house(house)

class PlayerPicky(Player):
    def __init__(self, bankrupt, tag):
        super().__init__(bankrupt, tag)
    
    def should_buy_house(self,house):
        return super().should_buy_house(house) and house.rent_price > 50

class PlayerCautious(Player):
    def __init__(self, bankrupt, tag):
        super().__init__(bankrupt, tag)
    
    def should_buy_house(self,house):
        return super().should_buy_house(house) and self.coins - house.buy_price >= 80

class PlayerRandom(Player):
    def __init__(self, bankrupt, tag):
        super().__init__(bankrupt, tag)
    
    def should_buy_house(self,house):
        return super().should_buy_house(house) and random.randint(0,100) >= 50


def readFile(fileName):
    with open(os.path.join(sys.path[0], fileName), "r") as fileObj:
        words = fileObj.read().splitlines() #puts the file into an array
        fileObj.close()

    lista = []
    for x in words:
        lista.append((str(x).split()))
    
    #lista = [map(int,i) for i in lista]
    return lista





#MAIN




lista = readFile("gameConfig.txt")
houses = []

for i in range(len(lista)):
    houses.append(House(int(lista[i][0]),int(lista[i][1])))


timeouts = 0
endturn = 0
cautiouswins = 0
impulsivewins = 0
pickywins = 0
randomwins = 0
for it in range(300):

    bankrupt = Bankrupt(houses)
    bankrupt.add_player(PlayerImpulsive(bankrupt, "Impulsive"))
    bankrupt.add_player(PlayerPicky(bankrupt, "Picky"))
    bankrupt.add_player(PlayerCautious(bankrupt, "Cautious"))
    bankrupt.add_player(PlayerRandom(bankrupt, "Random"))
    statistics = bankrupt.run()
   #print(statistics.turn,statistics.winner)

    endturn += statistics.turn

    if(statistics.turn == 1000):
        timeouts += 1

    if(statistics.winner == "Impulsive"):
        impulsivewins += 1
    elif(statistics.winner == "Picky"):
        pickywins += 1
    elif(statistics.winner == "Cautious"):
        cautiouswins += 1
    elif(statistics.winner == "Random"):
        randomwins += 1

print ("Partidas terminadas em timeout: ", timeouts)
print ("Tempo médio pro término de uma partida: ", endturn/300)
print ("Porcentagem de vitórias do jogador Impulsivo: ",impulsivewins/3, "%")
print ("Porcentagem de vitórias do jogador Exigente: ",pickywins/3, "%")
print ("Porcentagem de vitórias do jogador Cauteloso: ",cautiouswins/3, "%")
print ("Porcentagem de vitórias do jogador Aleatório: ",randomwins/3, "%")
