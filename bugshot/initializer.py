import random

from abc import ABCMeta, abstractmethod

from .state import (
    BugShotState,
    BugShotItemBoard,
)
from .enums import BugShotPlayer, BugShotItem, BugShotShell

class BugShotItemBoardInitializer(metaclass=ABCMeta):
    
    @abstractmethod
    def initialize(self) -> dict[BugShotPlayer, BugShotItemBoard]:
        raise NotImplementedError()

class BugShotStateInitializer(metaclass=ABCMeta):

    @abstractmethod
    def initialize(self) -> BugShotState:
        raise NotImplementedError()

class BugShotChamberInitializer(metaclass=ABCMeta):

    @abstractmethod
    def initialize(self) -> list[BugShotShell]:
        raise NotImplementedError()

class DefaultBugShotChamberInitializer(BugShotChamberInitializer):

    min_shell: int
    max_shell: int

    def __init__(self, min_shell: int = 3, max_shell: int = 6):
        if min_shell < 2:
            raise ValueError('min_shell must be greater than or equal to 2')
        self.min_shell = min_shell
        self.max_shell = max_shell

    def initialize(self):
        num_shell = random.randint(self.min_shell, self.max_shell)
        num_live = random.randint(1, num_shell - 1)
        lives = [BugShotShell.LIVE for _ in range(num_live)]
        blanks = [BugShotShell.BLANK for _ in range(num_shell - num_live)]
        shells = lives + blanks
        random.shuffle(shells)
        return shells

class FixedBugShotChamberInitializer(BugShotChamberInitializer):

    num_blanks: int
    num_lives: int

    def __init__(self, num_blanks: int, num_lives: int):
        self.num_blanks = num_blanks
        self.num_lives = num_lives
    
    def initialize(self):
        chamber = [
            BugShotShell.BLANK for _ in range(self.num_blanks)
        ] + [
            BugShotShell.LIVE for _ in range(self.num_lives)
        ]
        random.shuffle(chamber)
        return chamber

class DefaultBugShotStateInitializer(BugShotStateInitializer):

    min_initial_life: int
    max_initial_life: int
    item_board_initializer: BugShotItemBoardInitializer
    chamber_initializer: BugShotChamberInitializer

    def __init__(
            self,
            min_initial_life: int,
            max_initial_life: int,
            item_board_initializer: BugShotItemBoardInitializer,
            chamber_initializer: BugShotChamberInitializer,
        ):

        self.min_initial_life = min_initial_life
        self.max_initial_life = max_initial_life
        self.item_board_initializer = item_board_initializer
        self.chamber_initializer = chamber_initializer

    def initialize(self):
        init_life = random.randint(self.min_initial_life, self.max_initial_life)
        return BugShotState(
            turn=BugShotPlayer.PLAYER1,
            chamber=self.chamber_initializer.initialize(),
            init_life=init_life,
            life_dict={
                BugShotPlayer.PLAYER1: init_life,
                BugShotPlayer.PLAYER2: init_life,
            },
            item_boards=self.item_board_initializer.initialize(),
        )

class DefaultBugShotItemBoardInitializer(BugShotItemBoardInitializer):

    min_items: int
    max_items: int

    def __init__(self, min_items: int = 2, max_items: int = 4):
        self.min_items = min_items
        self.max_items = max_items

    def initialize(self) -> dict[BugShotPlayer, BugShotItemBoard]:
        num_items = random.randint(self.min_items, self.max_items)
        return {
            player: BugShotItemBoard(remains=self.__build_remains(num_items=num_items))
            for player in BugShotPlayer
        }

    def __build_remains(self, num_items: int):
        remains: dict[BugShotItem, int] = {
            item: 0 for item in BugShotItem
        }

        for _ in range(num_items):
            item = BugShotItem.random()
            remains[item] += 1
        
        return remains
