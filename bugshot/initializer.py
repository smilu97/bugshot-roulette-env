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
        self.min_shell = min_shell
        self.max_shell = max_shell

    def initialize(self):
        num_shell = random.randint(self.min_shell, self.max_shell)
        return [self.__random_shell() for _ in range(num_shell)]
    
    def __random_shell(self):
        return BugShotShell.LIVE if random.randint(0, 1) else BugShotShell.BLANK

class DefaultBugShotStateInitializer(BugShotStateInitializer):

    initial_life: int
    item_board_initializer: BugShotItemBoardInitializer
    chamber_initializer: BugShotChamberInitializer

    def __init__(
            self,
            initial_life: int,
            item_board_initializer: BugShotItemBoardInitializer,
            chamber_initializer: BugShotChamberInitializer,
        ):

        self.initial_life = initial_life
        self.item_board_initializer = item_board_initializer
        self.chamber_initializer = chamber_initializer

    def initialize(self):
        return BugShotState(
            turn=BugShotPlayer.PLAYER1,
            chamber=self.chamber_initializer.initialize(),
            init_life=self.initial_life,
            life_dict={
                BugShotPlayer.PLAYER1: self.initial_life,
                BugShotPlayer.PLAYER2: self.initial_life,
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
