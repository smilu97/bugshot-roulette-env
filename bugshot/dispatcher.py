import random

from abc import ABCMeta, abstractmethod

from .state import BugShotState, BugShotItemBoard
from .enums import BugShotAction, BugShotShell, BugShotItem, BugShotPlayer
from .initializer import BugShotChamberInitializer, BugShotItemBoardInitializer

class BugShotStateDispatcher(metaclass=ABCMeta):
    
    @abstractmethod
    def dispatch(
        self,
        state: BugShotState,
        action: BugShotAction,
    ) -> BugShotState:
        raise NotImplementedError()

    @abstractmethod
    def get_winner(self, state: BugShotState) -> BugShotPlayer:
        raise NotImplementedError()
    
    @abstractmethod
    def get_available_actions(self, state: BugShotState) -> list[BugShotAction]:
        raise NotImplementedError()

class DefaultBugShotStateDispatcher(BugShotStateDispatcher):
    
    chamber_initializer: BugShotChamberInitializer
    item_board_initializer: BugShotItemBoardInitializer
    max_num_items_per_board: int

    def __init__(
            self,
            chamber_initializer: BugShotChamberInitializer,
            item_board_initializer: BugShotItemBoardInitializer,
            max_num_items_per_board: int = 8,
        ):

        self.chamber_initializer = chamber_initializer
        self.item_board_initializer = item_board_initializer
        self.max_num_items_per_board = max_num_items_per_board

    def dispatch(
        self,
        state: BugShotState,
        action: BugShotAction,
    ) -> BugShotState:
        
        winner = self.get_winner(state)
        if winner is not None:
            return state

        return self.__dispatch_common(self.__dispatch_action(state, action))
        
    def get_available_actions(self, state: BugShotState) -> list[BugShotAction]:
        actions = list()
        item_board = state.item_boards[state.turn]
        if item_board.remains[BugShotItem.HANDCUFFS] > 0 and not state.is_opponent_handcuffed:
            actions.append(BugShotAction.USE_HANDCUFFS)
        if item_board.remains[BugShotItem.BEER] > 0:
            actions.append(BugShotAction.USE_BEER)
        if item_board.remains[BugShotItem.MAGNIFYING_GLASS] > 0 and not state.is_magnified_shell:
            actions.append(BugShotAction.USE_MAGNIYING_GLASS)
        if item_board.remains[BugShotItem.CIGARATTES] > 0:
            actions.append(BugShotAction.USE_CIGARATTES)
        if item_board.remains[BugShotItem.HAND_SAW] > 0 and not state.is_shotgun_sawed:
            actions.append(BugShotAction.USE_HAND_SAW)

        return [
            BugShotAction.USE_SHOTGUN_SELF,
            BugShotAction.USE_SHOTGUN_OPPONENT,
        ] + actions
    
    def __dispatch_action(
            self,
            state: BugShotState,
            action: BugShotAction,
    ) -> BugShotState:
        
        if action == BugShotAction.USE_SHOTGUN_SELF:
            return self._use_shotgun_self(state)
        if action == BugShotAction.USE_SHOTGUN_OPPONENT:
            return self._use_shotgun_opponent(state)
        if action == BugShotAction.USE_HANDCUFFS:
            return self._use_handcuffs(state)
        if action == BugShotAction.USE_BEER:
            return self._use_beer(state)
        if action == BugShotAction.USE_MAGNIYING_GLASS:
            return self._use_magnifying_glass(state)
        if action == BugShotAction.USE_CIGARATTES:
            return self._use_cigarattes(state)
        if action == BugShotAction.USE_HAND_SAW:
            return self._use_hand_saw(state)
        
        raise ValueError(f'Unknown action: {action}')
    
    def __dispatch_common(self, state: BugShotState) -> BugShotState:
        winner = self.get_winner(state)
        if winner is not None:
            return state
        
        if len(state.chamber) == 0:
            new_chamber = self.chamber_initializer.initialize()
            item_boards = self.__add_items(state.item_boards)
            state = state.set_chamber(new_chamber).set_item_boards(item_boards)
        
        return state

    def get_winner(self, state: BugShotState) -> BugShotPlayer:
        if state.life_dict[BugShotPlayer.PLAYER1] <= 0:
            return BugShotPlayer.PLAYER2
        if state.life_dict[BugShotPlayer.PLAYER2] <= 0:
            return BugShotPlayer.PLAYER1
        return None
    
    def _use_shotgun_self(self, state: BugShotState) -> BugShotState:
        return self.__use_shotgun(state, state.turn)

    def _use_shotgun_opponent(self, state: BugShotState) -> BugShotState:
        return self.__use_shotgun(state, state.turn.opponent())

    def __use_shotgun(self, state: BugShotState, to_player: BugShotPlayer) -> BugShotState:
        damage = DefaultBugShotStateDispatcher.get_damage(state)
        state = state \
            .pop_chamber() \
            .add_life(to_player, -damage) \
            .magnify_shell(revert=True) \
            .saw_shotgun(revert=True)
        
        if self.__should_pass_turn(state, to_player, damage):
            if state.is_opponent_handcuffed:
                return state.handcuff_opponent(revert=True)
            else:
                return state.pass_turn()
        
        return state
    
    def __should_pass_turn(self, state: BugShotState, to_player: BugShotPlayer, damage: int) -> bool:
        return to_player != state.turn or damage > 0
    
    def _use_handcuffs(self, state: BugShotState) -> BugShotState:
        num_remains = state.get_item_remains(BugShotItem.HANDCUFFS)
        if num_remains == 0:
            return state
        return state.decrease_item_remains(BugShotItem.HANDCUFFS).handcuff_opponent()
    
    def _use_beer(self, state: BugShotState) -> BugShotState:
        num_remains = state.get_item_remains(BugShotItem.BEER)
        if num_remains == 0:
            return state
        return state.decrease_item_remains(BugShotItem.BEER).pop_chamber()
    
    def _use_magnifying_glass(self, state: BugShotState) -> BugShotState:
        num_remains = state.get_item_remains(BugShotItem.MAGNIFYING_GLASS)
        if num_remains == 0:
            return state
        return state.decrease_item_remains(BugShotItem.MAGNIFYING_GLASS).magnify_shell()
    
    def _use_cigarattes(self, state: BugShotState) -> BugShotState:
        num_remains = state.get_item_remains(BugShotItem.CIGARATTES)
        if num_remains == 0:
            return state
        state = state.decrease_item_remains(BugShotItem.CIGARATTES)
        if state.life_dict[state.turn] < state.init_life:
            return state.add_life(state.turn, 1)
        return state
    
    def _use_hand_saw(self, state: BugShotState) -> BugShotState:
        num_remains = state.get_item_remains(BugShotItem.HAND_SAW)
        if num_remains == 0:
            return state
        return state.decrease_item_remains(BugShotItem.HAND_SAW).saw_shotgun()
    
    @staticmethod
    def get_damage(state: BugShotState) -> int:
        current_shell = state.chamber[-1]
        damage = 1 if current_shell == BugShotShell.LIVE else 0
        damage = 2 * damage if state.is_shotgun_sawed else damage
        return damage

    def __add_items(self, item_boards: dict[BugShotPlayer, BugShotItemBoard]) -> dict[BugShotPlayer, BugShotItemBoard]:
        item_boards2 = self.item_board_initializer.initialize()
        return {
            player: self.__add_items_to_board(item_boards[player], item_boards2[player])
            for player in BugShotPlayer
        }

    def __add_items_to_board(self, board: BugShotItemBoard, board2: BugShotItemBoard) -> BugShotItemBoard:
        max_new_items = self.max_num_items_per_board - board.get_num_items()
        if max_new_items <= 0:
            return board

        new_items = self.__serialize_items(board2)
        random.shuffle(new_items)

        for item in new_items[:max_new_items]:
            board = board.add_item(item, 1)
        return board

    def __serialize_items(self, item_board: BugShotItemBoard) -> list[BugShotItem]:
        return [
            item
            for item, num in item_board.remains.items()
            for _ in range(num)
        ]
