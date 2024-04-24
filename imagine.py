import random
import itertools

from abc import ABCMeta, abstractmethod

from bugshot import (
    BugShotState,
    BugShotItemBoard,
    BugShotItem,
    BugShotPlayer,
    BugShotShell,
)

class BugShotImagine(metaclass=ABCMeta):
    
    @abstractmethod
    def imagine(self, observation: list[int]) -> list[BugShotState]:
        raise NotImplementedError()

class AbstractBugShotImagine(BugShotImagine):

    def imagine(self, observation: list[int]) -> list[BugShotState]:
        num_live_shells = observation[0]
        num_blank_shells = observation[1]
        init_life = observation[2]
        life_player1 = observation[3]
        life_player2 = observation[4]
        items_player1 = observation[5:5+len(BugShotItem)]
        items_player2 = observation[5+len(BugShotItem):5+2*len(BugShotItem)]
        is_opponent_handcuffed = observation[5+2*len(BugShotItem)]
        is_magnified_live = observation[5+2*len(BugShotItem)+1]
        is_magnified_blank = observation[5+2*len(BugShotItem)+2]
        is_shotgun_sawed = observation[5+2*len(BugShotItem)+3]

        chambers = self._build_chambers(num_live_shells, num_blank_shells, is_magnified_live, is_magnified_blank)

        base = BugShotState(
            turn=BugShotPlayer.PLAYER1,
            chamber=[],
            init_life=init_life,
            life_dict={
                BugShotPlayer.PLAYER1: life_player1,
                BugShotPlayer.PLAYER2: life_player2,
            },
            item_boards={
                BugShotPlayer.PLAYER1: self.__build_item_board(items_player1),
                BugShotPlayer.PLAYER2: self.__build_item_board(items_player2),
            },
            is_opponent_handcuffed=is_opponent_handcuffed,
            is_magnified_shell=is_magnified_live or is_magnified_blank,
            is_shotgun_sawed=is_shotgun_sawed,
        )

        return [base.set_chamber(chamber=chamber) for chamber in chambers]
    
    @abstractmethod
    def _build_chambers(self, num_live: int, num_blank: int, is_magnified_live: int, is_magnified_blank: int) -> list[list[BugShotShell]]:
        raise NotImplementedError()
    
    def __build_item_board(self, num_items: list[int]) -> BugShotItemBoard:
        remains = dict()
        for item, num in zip(BugShotItem, num_items):
            remains[item] = num
        return BugShotItemBoard(remains=remains)

class RandomBugShotImagine(AbstractBugShotImagine):
    
    num_imagine: int

    def __init__(self, num_imagine: int = 1):
        self.num_imagine = num_imagine
    
    def _build_chambers(self, num_live: int, num_blank: int, is_magnified_live: int, is_magnified_blank: int) -> list[list[BugShotShell]]:
        return [self.__build_chamber(num_live, num_blank, is_magnified_live, is_magnified_blank) for _ in range(self.num_imagine)]

    def __build_chamber(self, num_live: int, num_blank: int, is_magnified_live: int, is_magnified_blank: int) -> list[BugShotShell]:
        chamber = [BugShotShell.LIVE] * (num_live - is_magnified_live) + [BugShotShell.BLANK] * (num_blank - is_magnified_blank)
        random.shuffle(chamber)

        if is_magnified_live:
            chamber.append(BugShotShell.LIVE)
        if is_magnified_blank:
            chamber.append(BugShotShell.BLANK)
        
        return chamber

class CombinationBugShotImagine(AbstractBugShotImagine):

    max_chambers: int

    def __init__(self, max_chambers: int = 100):
        self.max_chambers = max_chambers

    def _build_chambers(self, num_live: int, num_blank: int, is_magnified_live: int, is_magnified_blank: int) -> list[list[BugShotShell]]:
        chamber = [BugShotShell.LIVE] * (num_live - is_magnified_live) + [BugShotShell.BLANK] * (num_blank - is_magnified_blank)
        chambers = list(set(itertools.permutations(chamber)))

        if is_magnified_live:
            chambers = [chamber + (BugShotShell.LIVE,) for chamber in chambers]
        if is_magnified_blank:
            chambers = [chamber + (BugShotShell.BLANK,) for chamber in chambers]
        
        return chambers[:self.max_chambers]
    