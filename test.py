from bugshot import BugShotGameBuilder, BugShotGameConfig, BugShotPlayer
from agent import BugShotGameAgent, RandomBugShotGameAgent

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
        min_shell=2,
        max_shell=6,
        initial_life=3,
    )
    game_builder = BugShotGameBuilder()

    agent1 = RandomBugShotGameAgent()
    agent2 = RandomBugShotGameAgent()
    
    tester = BugShotGameTester(
        config=config,
        game_builder=game_builder,
        agent1=agent1,
        agent2=agent2,
        max_steps=1000,
    )

    winner = tester.test(verbose=True)
    print(f'Winner: {winner.value}')

if __name__ == '__main__':
    main()
