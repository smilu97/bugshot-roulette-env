import random

from abc import ABCMeta, abstractmethod

from bugshot.enums import BugShotAction
from bugshot.dispatcher import BugShotStateDispatcher
from evaluator import BugShotStateEvaluator
from imagine import BugShotImagine, RandomBugShotImagine

class BugShotGameAgent(metaclass=ABCMeta):
    
    @abstractmethod
    def act(self, observation: list[int]) -> BugShotAction:
        raise NotImplementedError()

class LoopDetectingBugShotGameAgent(BugShotGameAgent):
    '''
    An agent that detects loops in its actions and avoids them.
    '''

    __last_observation_hash: int
    __last_action: BugShotAction
    __loop_actions: set[(int, BugShotAction)]

    def __init__(self):
        self.__last_observation_hash = None
        self.__last_action = None
        self.__loop_actions = set()

    def act(self, observation: list[int]) -> BugShotAction:
        observation_hash = self.__hash_observation(observation)
        if observation_hash == self.__last_observation_hash:
            self.__loop_actions.add((observation_hash, self.__last_action))
        
        while True:
            action = self.act0(observation)
            if (observation_hash, action) not in self.__loop_actions:
                self.__last_observation_hash = observation_hash
                self.__last_action = action
                return action
    
    @abstractmethod
    def act0(self, observation: list[int]) -> BugShotAction:
        raise NotImplementedError()

    def __hash_observation(self, observation: list[int]) -> int:
        return hash(tuple(observation))

class RandomBugShotGameAgent(BugShotGameAgent):
    
    dispatcher: BugShotStateDispatcher
    imagine: BugShotImagine

    def __init__(self, dispatcher: BugShotStateDispatcher):
        self.dispatcher = dispatcher
        self.imagine = RandomBugShotImagine()

    def act(self, observation: list[int]) -> BugShotAction:
        state = self.imagine.imagine(observation)[0]
        return random.choice(self.dispatcher.get_available_actions(state))

class MonteCarloBugShotGameAgent(BugShotGameAgent):
    
    dispatcher: BugShotStateDispatcher
    imagine: BugShotImagine
    evaluator: BugShotStateEvaluator

    def __init__(self, dispatcher: BugShotStateDispatcher, imagine: BugShotImagine, evaluator: BugShotStateEvaluator):
        super().__init__()
        self.dispatcher = dispatcher
        self.imagine = imagine
        self.evaluator = evaluator

    def act(self, observation: list[int]) -> BugShotAction:
        states = self.imagine.imagine(observation)

        best_action = None
        best_score = -9999
        for action in list(BugShotAction):
            score = sum((self.evaluator.evaluate(self.dispatcher.dispatch(state, action)) for state in states))
            if score > best_score:
                best_action = action
                best_score = score
        return best_action
