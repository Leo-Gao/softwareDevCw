import itertools, random
import time

class Player(object):
    
    def __init__(self, name, health=30, handsize=5, deck=[], hand=[], discard=[], active=[], money=0, attack=0):
        self.name = name
        self.health = health
        self.handsize = handsize
        self.deck = deck
        self.hand = hand
        self.discard = discard
        self.active = active
        self.money = money
        self.attack = attack
   
    def deck2hand(self):
    
        for x in range(0, self.handsize):
            if (len(self.deck) == 0):
                random.shuffle(self.discard)
                self.deck = self.discard
                self.discard = []
            card = self.deck.pop()
            self.hand.append(card)  
            
    def showHandCards(self):
        print "\n ===== Your Hand  ====="
        index = 0
        for card in self.hand:
            print "[%s] %s" % (index, card)
            index = index + 1
            
    def showActiveCards(self):
        print "\n ===== Your Active Cards ====="
        for card in self.active:
            print card
    
    def showAttributes(self):
        print "\n ===== Your Values in Your Active Cards ===== "
        print "Money %s, Attack %s,  %s Cards left in hand" % (self.money, self.attack,len(self.hand))    
        
    def calAttributes(self):
               
        for card in self.active:
            self.money = self.money + card.get_money()
            self.attack = self.attack + card.get_attack()      
    
    def endTurn(self):
        self.money = 0
        self.attack = 0
        
        if (len(self.hand) >0 ):
            for x in range(0, len(self.hand)):
                self.discard.append(self.hand.pop())


        if (len(self.active) >0 ):
            for x in range(0, len(self.active)):
                self.discard.append(self.active.pop())
                
        for x in range(0, self.handsize):
            if len(self.deck) == 0:
                random.shuffle(self.discard)
                self.deck = self.discard
                self.discard = []
            card = self.deck.pop()
            self.hand.append(card)
        
        print self.name, 'turn ending'
            
class PlayerOne(Player):
    
    def __init__(self, name, health=30, handsize=5, deck=[], hand=[], discard=[], active=[], money=0, attack=0):
        Player.__init__(self, name, health=30, handsize=5, deck=[], hand=[], discard=[], active=[], money=0, attack=0)
         
    def buyCards(self,central):
        
        while self.money > 0:
            print '\nMoney you have:::::',self.money
            print "\nAvailable Cards:"
            ind = 0
            for card in central.active:
                print "[%s] %s" % (ind,card)
                ind = ind + 1
            print "\nChoose a card to buy [0-n], S for supplement, E to end buying"
            bv = raw_input("Choose option: ")
            if bv.lower() == 's':
                if len(central.supplement) > 0:
                    card = central.supplement[0]
                    if self.money >= card.cost:
                        self.money = self.money - card.cost
                        self.discard.append(central.supplement.pop())
                        print "***** Supplement Bought: Card is %s costing %s, with money %s , attack %s " % (card.name, card.cost, card.get_money(),card.get_attack())
                    else:
                        print "***** insufficient money to buy"
                else:
                    print "***** no supplements left"
            elif bv.lower() == 'e':
                break;
            elif bv.isdigit():
                if int(bv) < len(central.active):
                    if self.money >= central.active[int(bv)].cost:
                        card = central.active[int(bv)]
                        self.money = self.money - card.cost
                        self.discard.append(central.active.pop(int(bv)))
                        if( len(central.deck) > 0):
                            card = central.deck.pop()
                            central.active.append(card)
                        else:
                            central.activeSize = central.activeSize - 1
                        print "***** Card bought: Card is %s costing %s, with money %s , attack %s " % (card.name, card.cost, card.get_money(),card.get_attack())
                    else:
                        print "***** insufficient money to buy"
                else:
                    print "***** enter a valid index number"
            else:
                print "***** Enter a valid option"
                
        print '\nMoney Left:::::',self.money
        
    def attackOppo(self,pC):
       
        showHealth(self, pC)                    
        print "\nyou values attack %s, money %s" % (self.attack, self.money)
        print "attacking with strength %s" % self.attack
        pC.health = pC.health - self.attack
        self.attack = 0

class PlayerCom(Player):
    
    def __init__(self, name, health=30, handsize=5, deck=[], hand=[], discard=[], active=[], money=0, attack=0):
        Player.__init__(self, name, health=30, handsize=5, deck=[], hand=[], discard=[], active=[], money=0, attack=0)  
    
    def buyCards(self,central):
        print "Computer buying"
        if self.money > 0:
            cb = True
            templist = []
            print "Starting Money %s and cb %s " % (self.money, cb)
            while cb:
                templist = []
                if len(central.supplement) > 0:
                    if central.supplement[0].cost <= self.money:
                        templist.append(("S", central.supplement[0]))
                for intindex in range (0, central.activeSize):
                    if central.active[intindex].cost <= self.money:
                        templist.append((intindex, central.active[intindex]))
                if len(templist) >0:
                    highestIndex = 0
                    for intindex in range(0,len(templist)):
                        if templist[intindex][1].cost > templist[highestIndex][1].cost:
                            highestIndex = intindex
                        if templist[intindex][1].cost == templist[highestIndex][1].cost:
                            if aggressive:
                                if templist[intindex][1].get_attack() >templist[highestIndex][1].get_attack():
                                    highestIndex = intindex
                            else:
                                if templist[intindex][1].get_attack() >templist[highestIndex][1].get_money():
                                    highestIndex = intindex
                    source = templist[highestIndex][0]
                    if source in range(0,5):
                        if self.money >= central.active[int(source)].cost:
                            self.money = self.money - central.active[int(source)].cost
                            card = central.active.pop(int(source))
                            print "Card bought %s" % card
                            self.discard.append(card)
                            if( len(central.deck) > 0):
                                card = central.deck.pop()
                                central.active.append(card)
                            else:
                                central.activeSize = central.activeSize - 1
                        else:
                            print "Error Occurred"
                    else:
                        if self.money >= central.supplement[0].cost:
                            self.money = self.money - central.supplement[0].cost
                            card = central.supplement.pop()
                            self.discard.append(card)
                            print "Supplement Bought %s" % card
                        else:
                            print "Error Occurred"
                else:
                    cb = False
                if self.money == 0:
                    cb = False
        else:
            print "No Money to buy anything"
        
    def attackOppo(self,pO):
        for x in range(0, len(self.hand)):
                card = self.hand.pop()
                self.active.append(card)
                self.money = self.money + card.get_money()
                self.attack = self.attack + card.get_attack()

        print "\nComputer player values attack %s, money %s" % (self.attack, self.money)
        print "Computer attacking with strength %s" % self.attack
        pO.health = pO.health - self.attack
        self.attack = 0
        showHealth(pO, self)
        print "\nComputer player values attack %s, money %s" % (self.attack, pC.money)
                            
class CentralClass(object):
    def __init__(self,name, active=[], activeSize=5, supplement=[], deck=[]):
        self.name = name
        self.active = active
        self.activeSize = activeSize
        self.supplement = supplement
        self.deck = deck
        
#class playerOne(Player):
    
    
            
class Card(object):
    def __init__(self, name, values=(0, 0), cost=1, clan=None):
        self.name = name
        self.cost = cost
        self.values = values
        self.clan = clan
    def __str__(self):
                return 'Name %s costing %s with attack %s and money %s' % (self.name, self.cost, self.values[0], self.values[1])
    def get_attack(self):
        return self.values[0]
    def get_money(self):
            return self.values[1]


def initData():
    
    pO = PlayerOne('player one')
    pC = PlayerCom('player computer')
       
    # put card into central
    central = CentralClass('central')
    
    sdc = [4 * [Card('Archer', (3, 0), 2)], 4 * [Card('Baker', (0, 3), 2)], 3 * [Card('Swordsman', (4, 0), 3)], 2 * [Card('Knight', (6, 0), 5)],3 * [Card('Tailor', (0, 4), 3)],3 * [Card('Crossbowman', (4, 0), 3)],3 * [Card('Merchant', (0, 5), 4)],4 * [Card('Thug', (2, 0), 1)],4 * [Card('Thief', (1, 1), 1)],2 * [Card('Catapault', (7, 0), 6)], 2 * [Card('Caravan', (1, 5), 5)],2 * [Card('Assassin', (5, 0), 4)]]   
    supplement = 10 * [Card('Levy', (1, 2), 2)]
    deck = list(itertools.chain.from_iterable(sdc))
    random.shuffle(deck)
    central.deck = deck
    central.supplement = supplement
    central.active = []
    
    maxCount = central.activeSize
    count = 0
    while count < maxCount:
        card = central.deck.pop()
        central.active.append(card)
        count = count + 1
        
        
    # initialize palyers cards    
    pd = [8 * [Card('Serf', (0, 1), 0)], 2 * [Card('Squire', (1, 0), 0)]]
     
    pO.deck = list(itertools.chain.from_iterable(pd))
    
    pC.deck = list(itertools.chain.from_iterable(pd))
    
    # move card from deck to hand area
    pO.deck2hand()
    
    # move card from deck to hand area
    pC.deck2hand()
    
    return pO,pC,central

# the flag indicate the whether it is the first time playing game

def checkInput(flag):
    
    cG = False
    aggressive = False
    
    if flag:
        str_prompt = '\n Welcome Deck Card Game!  \n\n Do you want to play a game? y/N (default y):'
    else:
        str_prompt = '\n Do you want to play another game? y/N (default:y):'     
    
    while(True):
        pG = raw_input(str_prompt)
        if(pG.lower()=='y' or pG==''):
            cG = True
            break
        elif(pG.lower()=='n'):
            cG = False
            break
        else:
            print 'your input is ',pG,' it is not recognized, please try again, just type y or n '
            continue
    
    if not cG:
        print '\n You have choose N, the game will quit ~~~ ^ ^ !'
        return cG,aggressive
    
    str_prompt = "\n Do you want an aggressive (A) opponent or an acquisitive (Q) opponent? A/Q (defalut:A): "
    while(True):
        oT = raw_input(str_prompt)
        if(oT.lower()=='a' or oT==''):
            aggressive = True
            break
        elif(oT.lower()=='q'):
            aggressive = False
            break
        else:
            print 'your input is ',oT,' it is not recognized, please try again, just type A or Q '
            continue
        
    str_oppo = 'aggressive' if aggressive else 'acquisitive'
    print '\n You have choose an ',str_oppo, ' opponent'
    time.sleep(2)
    return cG,aggressive

def showCentralCards(central):
    print "Available Cards"
    for card in central.active:
        print card

    print "Supplement"
    if len(central.supplement) > 0:
        print central.supplement[0]

def showHealth(pO,pC):
        print "\nPlayer Health:::::::: %s" % pO.health
        print "Computer Health:::::: %s" % pC.health

def checkWinner(pO,pC,central):
    cG = True
    if pO.health <= 0:
        cG = False
        print "Computer wins"
    elif pC.health <= 0:
        cG = False
        print 'Player One Wins'
    elif central.activeSize == 0:
        print "No more cards available"
        if pO.health > pC.health:
            print "Player One Wins on Health"
        elif pC.health > pO.health:
            print "Computer Wins"
        else:
            pHT = 0
            pCT = 0
            if pHT > pCT:
                print "Player One Wins on Card Strength"
            elif pCT > pHT:
                print "Computer Wins on Card Strength"
            else:
                print "Draw"
        cG = False
    
    showHealth(pO, pC)
    
    return cG
    
if __name__ == '__main__':
    
    '''
    define three game roles
        pO: the player one
        pC: the player computer
        central: the overall cards collection 
    '''
     

   
    # initialize the detail information of each role
    pO,pC,central = initData()
    
    #showCentralCards(central)
    
    cG,aggressive = checkInput(True)
    
    while cG:
        
        print '\n ********* player one turn Start *********'
        while True:

            #pO.showHandCards()
            #pO.showActiveCards()
            pO.showAttributes()
            
            print("\n ===== Choose Action ===== ")
            print "\n(P = play all, [0-n] = play that card, B = Buy Card, A = Attack, E = end turn, S = Show health, C = Show Cards (default P)):"
            act = raw_input("Enter Action: ")
            print act
            
            if act.lower() == 'p' or act=='':
                if(len(pO.hand)>0):
                    for x in range(0, len(pO.hand)):
                        card = pO.hand.pop()
                        pO.active.append(card)
                    pO.calAttributes()  
                          
                pO.showHandCards()
                pO.showActiveCards()
            elif act.isdigit():
                if( int(act) < len(pO.hand)):
                    pO.active.append(pO.hand.pop(int(act)))
                    pO.calAttributes()    
                             
                pO.showHandCards()
                pO.showActiveCards()
            elif (act.lower() == 'b'):

                pO.buyCards(central)

            elif act.lower() == 'a':
                pO.attackOppo(pC)
                showHealth(pO, pC)
            elif act.lower() == 'e':
                pO.endTurn()
                break
            elif act.lower() == 's':
                showHealth(pO, pC)
            elif act.lower() == 'c':
                pO.showHandCards()
                pO.showActiveCards()
            else:
                print 'sorry, wrong input %s, please retype ' % (act)
        print '\n ********* player one turn END *********'       
        
        cG = checkWinner(pO,pC,central)
        if not cG:
            
            cG,aggressive = checkInput(False)
           
            if cG:
                
                # initialize the detail information of each role
                pO,pC,central = initData()
                
                showCentralCards(central)
            
            continue    
        
        
        
        print '\n\n\n ********* player computer turn Start *********\n\n'
        
        showCentralCards(central)
        
        pC.attackOppo(pO)
        
        pC.buyCards(central)
      
        pC.endTurn()
        
        print '\n ********* player computer turn END  ********* \n\n'

        cG = checkWinner(pO,pC,central)        
        if not cG:
            
            cG,aggressive = checkInput(False)
           
            if cG:
                
                # initialize the detail information of each role
                pO,pC,central = initData()
                
                showCentralCards(central)
                
            continue
        
    exit()
