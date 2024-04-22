from random import randint
from enum import Enum

class BugShotPlayer(Enum):
    PLAYER1 = 'PLAYER1'
    PLAYER2 = 'PLAYER2'

    def opponent(self):
        return BugShotPlayer.PLAYER2 if self == BugShotPlayer.PLAYER1 else BugShotPlayer.PLAYER1

class BugShotShell(Enum):
    BLANK = 'BLANK'
    LIVE = 'LIVE'

class BugShotItem(Enum):
    '''
    <a href="https://namu.wiki/w/Buckshot%20Roulette#s-4">BugShot Items</a>
    '''

    SHOTGUN = 'SHOTGUN'
    HANDCUFFS = 'HANDCUFFS'
    BEER = 'BEER'
    MAGNIFYING_GLASS = 'MAGNIFYING_GLASS'
    CIGARATTES = 'CIGARATTES'
    HAND_SAW = 'HAND_SAW'

    # TODO: 'Double or Nothing' Expansion
    # BURNER_PHONE = 'BURNER_PHONE'
    # INVERTER = 'INVERTER'
    # ADRENALINE = 'ADRENALINE'
    # EXPIRED_MEDICINE = 'EXPIRED_MEDICINE'

    @staticmethod
    def random():
        rv = randint(0, len(BugShotItem) - 1)
        return list(BugShotItem)[rv]

class BugShotAction(Enum):
    USE_SHOTGUN_SELF = 'USE_SHOTGUN_SELF'
    USE_SHOTGUN_OPPONENT = 'USE_SHOTGUN_OPPONENT'
    USE_HANDCUFFS = 'USE_HANDCUFFS'
    USE_BEER = 'USE_BEER'
    USE_MAGNIYING_GLASS = 'USE_MAGNIYING_GLASS'
    USE_CIGARATTES = 'USE_CIGARATTES'
    USE_HAND_SAW = 'USE_HAND_SAW'

    # TODO: 'Double or Nothing' Expansion
    # USE_BURNER_PHONE = 'USE_BURNER_PHONE'
    # USE_INVERTER = 'USE_INVERTER'
    # USE_ADRENALINE = 'USE_ADRENALINE'
    # USE_EXPIRED_MEDICINE = 'USE_EXPIRED_MEDICINE'
