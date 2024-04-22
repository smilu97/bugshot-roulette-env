from .initializer import (
    BugShotStateInitializer,
    DefaultBugShotStateInitializer,
    DefaultBugShotItemBoardInitializer,
    DefaultBugShotChamberInitializer,
)
from .dispatcher import BugShotStateDispatcher, DefaultBugShotStateDispatcher
from .selector import BugShotStateSelector, DefaultBugShotStateSelector
from .enums import BugShotPlayer, BugShotAction

class BugShotGame:

    state_initializer: BugShotStateInitializer
    dispatcher: BugShotStateDispatcher
    selector_player1: BugShotStateSelector
    selector_player2: BugShotStateSelector

    def __init__(
            self,
            state_initializer: BugShotStateInitializer,
            dispatcher: BugShotStateDispatcher,
            selector_player1: BugShotStateSelector,
            selector_player2: BugShotStateSelector,
        ):

        self.state = state_initializer.initialize()
        self.dispatcher = dispatcher
        self.selector_player1 = selector_player1
        self.selector_player2 = selector_player2

    def do_action(self, action: BugShotAction) -> bool:
        next_state = self.dispatcher.dispatch(self.state, action)
        if next_state is self.state:
            return False
        self.state = next_state
        return True

    def observe(self) -> list[int]:
        if self.state.turn == BugShotPlayer.PLAYER1:
            return self.selector_player1.select(self.state)
        else:
            return self.selector_player2.select(self.state)
    
    def get_turn(self) -> BugShotPlayer:
        return self.state.turn
    
    def get_winner(self) -> BugShotPlayer:
        return self.dispatcher.get_winner(self.state)

class BugShotGameConfig:

    min_items_per_init: int
    max_items_per_init: int
    max_items_per_board: int
    min_shell: int
    max_shell: int
    initial_life: int

    def __init__(
            self,
            min_items_per_init: int,
            max_items_per_init: int,
            max_items_per_board: int,
            min_shell: int,
            max_shell: int,
            initial_life: int,
        ):

        self.min_items_per_init = min_items_per_init
        self.max_items_per_init = max_items_per_init
        self.max_items_per_board = max_items_per_board
        self.min_shell = min_shell
        self.max_shell = max_shell
        self.initial_life = initial_life

class BugShotGameBuilder:

    def build(self, config: BugShotGameConfig) -> BugShotGame:
        min_items_per_init = config.min_items_per_init
        max_items_per_init = config.max_items_per_init
        max_items_per_board = config.max_items_per_board
        min_shell = config.min_shell
        max_shell = config.max_shell
        initial_life = config.initial_life

        item_board_initializer = DefaultBugShotItemBoardInitializer(
            min_items=min_items_per_init,
            max_items=max_items_per_init,
        )
        chamber_initializer = DefaultBugShotChamberInitializer(
            min_shell=min_shell,
            max_shell=max_shell,
        )
        state_initializer = DefaultBugShotStateInitializer(
            initial_life=initial_life,
            item_board_initializer=item_board_initializer,
            chamber_initializer=chamber_initializer,
        )
        dispatcher = DefaultBugShotStateDispatcher(
            chamber_initializer=chamber_initializer,
            item_board_initializer=item_board_initializer,
            max_num_items_per_board=max_items_per_board,
        )
        selector_player1 = DefaultBugShotStateSelector(BugShotPlayer.PLAYER1)
        selector_player2 = DefaultBugShotStateSelector(BugShotPlayer.PLAYER2)

        return BugShotGame(
            state_initializer=state_initializer,
            dispatcher=dispatcher,
            selector_player1=selector_player1,
            selector_player2=selector_player2,
        )
