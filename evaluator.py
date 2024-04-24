import random

from abc import ABCMeta, abstractmethod

from bugshot.state import BugShotState
from bugshot.dispatcher import BugShotStateDispatcher
from bugshot.enums import BugShotAction, BugShotPlayer, BugShotItem

class BugShotStateEvaluator(metaclass=ABCMeta):
    
    @abstractmethod
    def evaluate(self, state: BugShotState) -> float:
        raise NotImplementedError()

class MonteCarloBugShotStateEvaluator(BugShotStateEvaluator):
    
    dispatcher: BugShotStateDispatcher
    num_trials: int

    def __init__(self, dispatcher: BugShotStateDispatcher, num_trials: int):
        self.dispatcher = dispatcher
        self.num_trials = num_trials

    def evaluate(self, state: BugShotState) -> float:
        num_wins = 0
        for _ in range(self.num_trials):
            if self.evaluate_once(state):
                num_wins += 1
        return num_wins / self.num_trials

    def evaluate_once(self, state: BugShotState) -> bool:
        while self.dispatcher.get_winner(state) is None:
            action = self.__get_random_action(state)
            state = self.dispatcher.dispatch(state, action)
        return self.dispatcher.get_winner(state) == BugShotPlayer.PLAYER1
    
    def __get_random_action(self, state: BugShotState) -> BugShotAction:
        return random.choice(self.dispatcher.get_available_actions(state))
