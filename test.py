from tqdm import tqdm

from bugshot import BugShotGameBuilder, BugShotGameConfig, BugShotPlayer
from agent import BugShotGameAgent, RandomBugShotGameAgent, MonteCarloBugShotGameAgent
from imagine import CombinationBugShotImagine
from evaluator import MonteCarloBugShotStateEvaluator

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
        dispatcher=dispatcher,
        imagine=CombinationBugShotImagine(max_chambers=100),
        evaluator=MonteCarloBugShotStateEvaluator(
            dispatcher=dispatcher,
            num_trials=100,
        ),
    )
    random_agent = RandomBugShotGameAgent(dispatcher=dispatcher)
    
    tester = BugShotGameTester(
        config=config,
        game_builder=game_builder,
        agent1=monte_agent,
        agent2=random_agent,
        max_steps=1000,
    )

    num_trials = 100
    num_wins = 0
    for _ in tqdm(range(num_trials)):
        winner = tester.test(verbose=False)
        if winner == BugShotPlayer.PLAYER1:
            num_wins += 1
    
    print(f'Win rate: {num_wins / num_trials}')

if __name__ == '__main__':
    main()
