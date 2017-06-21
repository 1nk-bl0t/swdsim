"""
Game engine for SWD simulation.
"""

### DICE:
# SIDES 1-6:
#   VALUE
#   SYMBOL/TYPE (MELEE, RANGED, SHIELD, RESOURCE, DISRUPT, DISCARD, FOCUS, SPECIAL, BLANK, ANY)
#   (COST)
#   MODIFIER?
# READY?

SAMPLE_DIE_A1 = [[1, 'Ranged', 0, False],
                 [2, 'Ranged', 0, False],
                 [1, 'Focus', 0, False],
                 [1, 'Discard', 0, False],
                 [1, 'Resource', 0, False],
                 [0, 'Blank', 0, False]
                ]

class Dice(object):
    """Create Dice objects."""

    def __init__(self, die_values):
        self.sides = []
        for i in range(0, 6):
            self.sides.append(die_values[i])

    def __repr__(self):
        return_string = '('
        for i in range(0, 6):
            if self.sides[i][1] not in ['Blank', 'Special']:
                if self.sides[i][3]:
                    return_string += '+'
                return_string += str(self.sides[i][0]) + ' '
            return_string += str(self.sides[i][1])
            if self.sides[i][2]:
                return_string += ' Cost ' + str(self.sides[i][2])
            if i < 5:
                return_string += ', '
        return return_string + ')'

### CARDS:
# ID (SET/NUMBER)
# RARITY
# TITLE
# (SUBTITLE)
# UNIQUE?
# AFFILIATION (HERO, VILLAIN, NEUTRAL)
# COLOUR (RED, BLUE, YELLOW, GREY)
# TYPE (BATTLEFIELD, CHARACTER, EVENT, UPGRADE, SUPPORT)
# (SUBTYPE (WEAPON, EQUIPMENT, ABILITY, VEHICLE, DROID, NONE))
# (HEALTH)
# COST(S)
# (FLAVOUR TEXT)
# (EFFECT(S))
# (ACTION(S))
# IMAGE
# DIE?
# READY?

SAMPLE_CARD_A1 = {'id':['Awakenings', 1],
                  'rarity':'Legendary',
                  'title':'Captain Phasma',
                  'subtitle':'Elite Trooper',
                  'unique':True,
                  'affiliation':'Villain',
                  'colour':'Red',
                  'type':'Character',
                  'health':11,
                  'cost':[12, 15],
                  'text':"Your non-unique characters have the Guardian \
                          keyword.",
                  'die':SAMPLE_DIE_A1
                 }
SAMPLE_CARD_A2 = {'id':['Awakenings', 2],
                  'rarity':'Starter',
                  'title':'First Order Storm Trooper',
                  'unique':False,
                  'affiliation':'Villain',
                  'colour':'Red',
                  'type':'Character',
                  'health':7,
                  'cost':[7],
                  'text':"Members of this new generation of stormtroopers are \
                          trained from birth and fed a steady diet of First \
                          Order propaganda to ensure absolute loyalty.",
                  'die':[[1, 'Ranged', 0, False],
                         [2, 'Ranged', 0, False],
                         [2, 'Ranged', 1, False],
                         [1, 'Resource', 0, False],
                         [0, 'Blank', 0, False],
                         [0, 'Blank', 0, False]
                        ]
                 }
SAMPLE_CARD_A70 = {'id':['Awakenings', 70],
                   'rarity':'Uncommon',
                   'title':'Endless Ranks',
                   'unique':False,
                   'affiliation':'Villain',
                   'colour':'Red',
                   'type':'Event',
                   'cost':[5],
                   'text':"Return one of your defeated non-unique Red \
                           characters to the game with no damage on it.",
                  }
SAMPLE_CARD_A72 = {'id':['Awakenings', 72],
                   'rarity':'Common',
                   'title':'Probe',
                   'unique':False,
                   'affiliation':'Villain',
                   'colour':'Red',
                   'type':'Event',
                   'cost':[0],
                   'text':"Look at 2 random cards in an opponent's hand and \
                           discard any of those cards that are events.",
                  }

class Card(object):
    """Create Card objects."""

    def __init__(self, card_data):
        self.set_name = card_data['id'][0]
        self.card_num = card_data['id'][1]
        self.rarity = card_data['rarity']
        self.title = card_data['title']
        if 'subtitle' in card_data:
            self.subtitle = card_data['subtitle']
        else:
            self.subtitle = ''
        self.unique = card_data['unique']
        self.affiliation = card_data['affiliation']
        self.colour = card_data['colour']
        self.type = card_data['type']
        if self.type is 'Character':
            self.health = card_data['health']
        if 'subtype' in card_data:
            self.subtype = card_data['subtype']
        else:
            self.subtype = ''
        self.cost = card_data['cost']
        if 'effects' in card_data:
            # TODO
            # PROCESS EFFECTS
            pass
        else:
            self.effects = None
        if 'actions' in card_data:
            # TODO
            # PROCESS ACTIONS
            pass
        else:
            self.actions = None
        self.text = card_data['text']
        if 'die' in card_data:
            self.die = Dice(card_data['die'])
        else:
            self.die = None

    def __repr__(self):
        return_string = self.set_name + ', ' + str(self.card_num) + ', ' + self.title
        if self.die != None:
            return_string += ', ' + str(self.die)
        return return_string
    
    def get_card_set(self):
        return self.set_name
    
    def get_card_num(self):
        return self.card_num
    
    def get_card_title(self):
        return_string = self.title
        if self.subtitle != '':
            return_string += ' - ' + self.subtitle
        return return_string
    
### PLAYER:
# CHARACTERS
# HAND
# DECK
# DISCARD_PILE
# BATTLEFIELD
# DICE POOL
# RESOURCES
# LIMBO

SAMPLE_PLAYER1 = ['Player1',
                  [('Captain Phasma - Elite Trooper', 2),
                   ('First Order Storm Trooper', 1),
                   ('First Order Storm Trooper', 1)
                  ],
                  'Starship Graveyard - Jakku',
                  [('Endless Ranks', 2),
                   ('Probe', 1)
                  ]
                 ]

class Player(object):
    """Create Player objects."""

    def __init__(self, player_num, player_details):
        self.player_num = player_num
        self.player_name = player_details[0]
        self.characters = []
        #for character in player_details[1]:
        #for i in range(0, character[1]):
        self.battlefield = player_details[2]
        self.deck = player_details[3]
        self.hand = []
        self.actions = []
        self.discards = []
        self.removed_cards = []
        self.limbo = []
        self.resources = 0
        self.dice_pool = []
        self.dice_bag = []

SAMPLE_GAME = []

class Game(object):
    """Create Game objects."""

    def __init__(self, num_players=2):
        self.num_players = num_players
        self.players = []
        for i in range(0, self.num_players):
            #READ IN PLAYER DATA
            player_details = SAMPLE_PLAYER1
            self.players[i] = Player(i + 1, player_details)


CARDS_PER_SET = {'Awakenings': 174, 'Spirit of Rebellion': 160}
CARDS = []
PLAYERS = []
#for card_set in CARDS_PER_SET:
#    for card_number in range(0, CARDS_PER_SET[card_set]):
#        #READ IN CARD DATA
#        new_card = Card(card_set, card_number + 1)
#        CARDS.append(new_card)
CARDS.append(Card(SAMPLE_CARD_A1))
CARDS.append(Card(SAMPLE_CARD_A2))
CARDS.append(Card(SAMPLE_CARD_A70))
CARDS.append(Card(SAMPLE_CARD_A72))
PLAYERS.append(Player(1, SAMPLE_PLAYER1))
for card in CARDS:
    print(card)

def find_card(card_list, card_name):
    """Search for a specific card"""
    for single_card in card_list:
        if single_card.get_card_title == card_name:
            return single_card

### INITIALIZATION
# INITIALIZE GAME:
#   INITIALIZE PLAY AREA
#   INITIALIZE PLAYERS:
#       INITIALIZE CHARACTERS
#       INITIALIZE BATTLEFIELD
#       INITIALIZE DECK

### GAME SETUP
# EACH PLAYER:
#   SHUFFLE DECK
#   DRAW 5 CARDS
#   MULLIGAN
#   GET 2 RESOURCES
#   ROLL CHARACTER DICE
# WINNING ROLL SELECTS BATTLEFIELD
# ASSERT BATTLEFIELD OWNERSHIP
# DEPLOY 2 SHIELDS

### PLAY GAME
# LOOP ROUNDS:
#   LOOP ACTION PHASE:
#       EACH PLAYER:
#           TAKE ONE ACTION (OR MORE)
#   UPKEEP PHASE:
#       READY EXHAUSTED CARDS
#       RETURN DICE IN POOL TO CARDS
#       GAIN 2 RESOURCES
#       DISCARD ANY NUMBER OF CARDS FROM HAND
#       IF POSSIBLE, DRAW HAND BACK UP TO MAX_HAND_SIZE

### POSSIBLE ACTIONS:
# PLAY A CARD FROM HAND:
#   PLAY AN EVENT
#   PLAY AN UPGRADE
#   PLAY A SUPPORT
# ACTIVATE A CHARACTER:
#   ROLL ALL CHARACTER/UPGRADE DICE
#   EXHAUST CHARACTER
# ACTIVATE A SUPPORT:
#   ROLL SUPPORT DIE
#   EXHAUST SUPPORT
# RESOLVE DICE:
#   SELECT SYMBOL TO RESOLVE
#   LOOP RESOLVE A DIE:
#       ADD ANY MODIFIER DICE?
# USE A CARD ACTION
# DISCARD TO REROLL:
#   SELECT CARD TO DISCARD
#   SELECT DICE TO REROLL
# CLAIM THE BATTLEFIELD:
#   TAKE CONTROL OF BATTLEFIELD
#   RESOLVE BATTLEFIELD ABILITY
# PASS

### WIN CONDITIONS:
# ALL CHARACTERS ARE DEFEATED
# NO CARDS IN HAND OR DECK AFTER UPKEEP PHASE
#   IF MILL TIE, BATTLEFIELD CONTROLLER WINS
