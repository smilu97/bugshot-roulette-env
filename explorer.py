import random

from abc import ABCMeta, abstractmethod

from bugshot import (
    BugShotState,
    BugShotStateDispatcher,
    BugShotAction,
    BugShotPlayer,
)

class BugShotStateExplorer(metaclass=ABCMeta):
    
    @abstractmethod
    def explore(self, state: BugShotState) -> tuple[bool, list[BugShotAction]]:
        raise NotImplementedError()

class RandomBugShotStateExplorer(BugShotStateExplorer):
    
    dispatcher: BugShotStateDispatcher

    def __init__(self, dispatcher: BugShotStateDispatcher):
        self.dispatcher = dispatcher

    def explore(self, state: BugShotState) -> tuple[bool, list[BugShotAction]]:
        actions = list()
        while self.dispatcher.get_winner(state) is None:
            action = self.__get_random_action(state)
            actions.append(action)
            state = self.dispatcher.dispatch(state, action)
        return self.dispatcher.get_winner(state) == BugShotPlayer.PLAYER1, actions
    
    def __get_random_action(self, state: BugShotState) -> BugShotAction:
        return random.choice(self.dispatcher.get_available_actions(state))
