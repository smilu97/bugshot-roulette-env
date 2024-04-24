#!/usr/bin/env python

from bugshot import (
    BugShotGameBuilder,
    BugShotGameConfig,
    BugShotState,
    BugShotPlayer,
    BugShotAction,
    BugShotShell,
)
from agent import MonteCarloBugShotGameAgent
from imagine import CombinationBugShotImagine
from explorer import RandomBugShotStateExplorer

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
    game = game_builder.build(config=config)

    dispatcher = game_builder.build(config=config).dispatcher
    monte_agent = MonteCarloBugShotGameAgent(
        num_trials=1000,
        dispatcher=dispatcher,
        imagine=CombinationBugShotImagine(max_chambers=100),
        explorer=RandomBugShotStateExplorer(dispatcher=dispatcher),
    )

    while game.get_winner() is None:
        print_state(game.state)
        if game.get_turn() == BugShotPlayer.PLAYER1:
            action = input_action(dispatcher.get_available_actions(game.state))
            print(f'Player action: {action.value}')
        else:
            action = monte_agent.act(observation=game.observe())
            print(f'Opponent action: {action.value}')
        game.do_action(action)
    
    print(f'{game.get_winner().value} wins!')

def print_state(state: BugShotState):
    indent = 2

    num_live_shells = state.chamber.count(BugShotShell.LIVE)
    num_blank_shells = state.chamber.count(BugShotShell.BLANK)
    life_player1 = state.life_dict[BugShotPlayer.PLAYER1]
    life_player2 = state.life_dict[BugShotPlayer.PLAYER2]
    items_player1 = state.item_boards[BugShotPlayer.PLAYER1].describe()
    items_player2 = state.item_boards[BugShotPlayer.PLAYER2].describe()
    is_opponent_handcuffed = state.is_opponent_handcuffed
    is_magnified_live = state.is_magnified_shell and state.chamber[-1] == BugShotShell.LIVE
    is_magnified_blank = state.is_magnified_shell and state.chamber[-1] == BugShotShell.BLANK
    magnifier_result = 'live' if is_magnified_live else 'blank' if is_magnified_blank else 'none'
    is_shotgun_sawed = state.is_shotgun_sawed
    
    print(f'--------------- Observation ---------------')
    print(f'{"Live shells":<{indent}}: {num_live_shells}')
    print(f'{"Blank shells":<{indent}}: {num_blank_shells}')
    print(f'{"Lifes":<{indent}}: {life_player1} vs {life_player2}')
    print(f'{"Items player1":<{indent}}: {items_player1}')
    print(f'{"Items player2":<{indent}}: {items_player2}')
    if is_opponent_handcuffed:
        print(f'{"Opponent handcuffed":<{indent}}: True')
    if magnifier_result != 'none':
        print(f'{"Magnified":<{indent}}: {magnifier_result}')
    if is_shotgun_sawed:
        print(f'{"Shotgun sawed":<{indent}}: True')

def input_action(valid_actions: list[BugShotAction]):
    valid_action_values = [x.value for x in valid_actions]
    print(f'Available actions: {valid_action_values}')
    while True:
        try:
            action = input(f'Enter action (1-{len(valid_actions)}): ')
            action = int(action)
            if action < 1 or action > len(valid_actions):
                continue
            return valid_actions[action - 1]
        except KeyboardInterrupt as e:
            raise e
        except:
            continue

if __name__ == '__main__':
    main()
