from abc import ABCMeta, abstractmethod

from .state import BugShotState, BugShotItemBoard
from .enums import BugShotShell, BugShotPlayer, BugShotItem

class BugShotStateSelector(metaclass=ABCMeta):
    
    @abstractmethod
    def select(self, state: BugShotState) -> list[int]:
        raise NotImplementedError()

class DefaultBugShotStateSelector(BugShotStateSelector):

    player: BugShotPlayer

    def __init__(self, player: BugShotPlayer):
        self.player = player
    
    def select(self, state: BugShotState) -> list[int]:
        num_live_shells = len([shell for shell in state.chamber if shell == BugShotShell.LIVE])
        num_blank_shells = len([shell for shell in state.chamber if shell == BugShotShell.BLANK])
        init_life = state.init_life
        life_player1 = state.life_dict[BugShotPlayer.PLAYER1]
        life_player2 = state.life_dict[BugShotPlayer.PLAYER2]
        items_player1 = self.__serialize_items(state.item_boards[BugShotPlayer.PLAYER1])
        items_player2 = self.__serialize_items(state.item_boards[BugShotPlayer.PLAYER2])
        is_opponent_handcuffed = int(state.is_opponent_handcuffed)
        is_magnified_live = state.is_magnified_shell and state.chamber[-1] == BugShotShell.LIVE
        is_magnified_blank = state.is_magnified_shell and state.chamber[-1] == BugShotShell.BLANK
        is_shotgun_sawed = int(state.is_shotgun_sawed)

        if self.player is BugShotPlayer.PLAYER2:
            life_player1, life_player2 = life_player2, life_player1
            items_player1, items_player2 = items_player2, items_player1
        
        return [
            num_live_shells,
            num_blank_shells,
            init_life,
            life_player1,
            life_player2,
            *items_player1,
            *items_player2,
            is_opponent_handcuffed,
            is_magnified_live,
            is_magnified_blank,
            is_shotgun_sawed,
        ]
    
    def __serialize_items(self, item_board: BugShotItemBoard) -> list[int]:
        return [item_board.remains[item] for item in BugShotItem]
