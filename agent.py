import random

from abc import ABCMeta, abstractmethod

from bugshot.enums import BugShotAction

class BugShotGameAgent(metaclass=ABCMeta):
    
    @abstractmethod
    def act(self, observation: list[int]) -> BugShotAction:
        raise NotImplementedError()

class LoopDetectingBugShotGameAgent(BugShotGameAgent):

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

class RandomBugShotGameAgent(LoopDetectingBugShotGameAgent):
    
    def act0(self, observation: list[int]) -> BugShotAction:
        return random.choice(list(BugShotAction))
