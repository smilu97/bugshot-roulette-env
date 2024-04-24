import random

from collections import Counter
from abc import ABCMeta, abstractmethod

from bugshot import BugShotAction, BugShotStateDispatcher
from explorer import BugShotStateExplorer
from decoder import BugShotStateDecoder, RandomBugShotStateDecoder

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
    decoder: BugShotStateDecoder

    def __init__(self, dispatcher: BugShotStateDispatcher):
        self.dispatcher = dispatcher
        self.decoder = RandomBugShotStateDecoder()

    def act(self, observation: list[int]) -> BugShotAction:
        state = self.decoder.decode(observation)[0]
        return random.choice(self.dispatcher.get_available_actions(state))

class MonteCarloBugShotGameAgent(BugShotGameAgent):
    
    num_trials: int
    dispatcher: BugShotStateDispatcher
    decoder: BugShotStateDecoder
    explorer: BugShotStateExplorer

    def __init__(self, num_trials: int, dispatcher: BugShotStateDispatcher, decoder: BugShotStateDecoder, explorer: BugShotStateExplorer):
        super().__init__()
        self.num_trials = num_trials
        self.dispatcher = dispatcher
        self.decoder = decoder
        self.explorer = explorer

    def act(self, observation: list[int]) -> BugShotAction:
        root_states = self.decoder.decode(observation)

        count_win = Counter()
        count_lose = Counter()

        for _ in range(self.num_trials):
            root_state = random.choice(root_states)
            is_win, actions = self.explorer.explore(root_state)
        
            if len(actions) == 0:
                continue
            action = actions[0]

            if is_win:
                count_win[action] += 1
            else:
                count_lose[action] += 1

        win_ratios = dict()
        
        for action in BugShotAction:
            count_total = count_win[action] + count_lose[action]
            if count_total != 0:
                win_ratios[action] = count_win[action] / count_total
        
        return max(win_ratios, key=win_ratios.get)
