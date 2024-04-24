from tqdm import tqdm
import sys

from bugshot import BugShotGameBuilder, BugShotGameConfig, BugShotPlayer
from agent import BugShotGameAgent, RandomBugShotGameAgent, MonteCarloBugShotGameAgent
from imagine import CombinationBugShotImagine
from explorer import RandomBugShotStateExplorer

class BugShotGameTester:

    config: BugShotGameConfig
    game_builder: BugShotGameBuilder
    agent1: BugShotGameAgent
    agent2: BugShotGameAgent
    max_steps: int

    def __init__(
            self,
            config: BugShotGameConfig,
            game_builder: BugShotGameBuilder,
            agent1: BugShotGameAgent,
            agent2: BugShotGameAgent,
            max_steps: int = 1000,
        ):

        self.config = config
        self.game_builder = game_builder
        self.agent1 = agent1
        self.agent2 = agent2
        self.max_steps = max_steps
    
    def test(self, verbose=False) -> BugShotPlayer:
        game = self.game_builder.build(config=self.config)

        if verbose:        
            indent = 4
            game.state.print(indent=indent)

        for _ in range(self.max_steps):
            winner = game.get_winner()
            if winner is not None:
                return winner

            turn = game.get_turn()
            agent = self.agent1 if turn == BugShotPlayer.PLAYER1 else self.agent2
            observation = game.observe()
            action = agent.act(observation)
            
            if game.do_action(action) and verbose:
                print(f'{turn.value} -> {action.value}')
                game.state.print(indent=indent)

        return None

def evaluate_agent(tester: BugShotGameTester, num_trials: int = 1000) -> float:
    num_wins = 0
    for _ in tqdm(range(num_trials)):
        winner = tester.test(verbose=False)
        if winner == BugShotPlayer.PLAYER1:
            num_wins += 1
    
    return num_wins / num_trials

def main():
    config = BugShotGameConfig(
        min_items_per_init=2,
        max_items_per_init=4,
        max_items_per_board=8,
        min_shell=3,
        max_shell=8,
        min_initial_life=2,
        max_initial_life=3,
    )
    game_builder = BugShotGameBuilder()

    dispatcher = game_builder.build(config=config).dispatcher
    monte_agent = MonteCarloBugShotGameAgent(
        num_trials=100,
        dispatcher=dispatcher,
        imagine=CombinationBugShotImagine(max_chambers=100),
        explorer=RandomBugShotStateExplorer(dispatcher=dispatcher),
    )
    random_agent = RandomBugShotGameAgent(dispatcher=dispatcher)
    
    tester = BugShotGameTester(
        config=config,
        game_builder=game_builder,
        agent1=monte_agent,
        agent2=random_agent,
        max_steps=1000,
    )

    num_trials = 1000 if len(sys.argv) < 2 else int(sys.argv[1])
    
    if num_trials == 1:
        winner = tester.test(verbose=True)
        print(f'Winner: {winner}')
    else:
        win_rate = evaluate_agent(tester, num_trials=1000)
        print(f'Win rate: {win_rate}')

if __name__ == '__main__':
    main()
