from bugshot import BugShotGameBuilder, BugShotGameConfig
from bugshot.enums import BugShotPlayer, BugShotAction, BugShotItem
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
        num_trials=100,
        dispatcher=dispatcher,
        imagine=CombinationBugShotImagine(max_chambers=100),
        explorer=RandomBugShotStateExplorer(dispatcher=dispatcher),
    )

    while game.get_winner() is None:
        observation = game.observe()
        print_observation(observation)
        turn = game.get_turn()
        if turn == BugShotPlayer.PLAYER1:
            action = input_action(dispatcher.get_available_actions(game.state))
            game.do_action(action)
        else:
            action = monte_agent.act(observation=observation)
            print(f'Opponent action: {action.value}')
            game.do_action(action)
    
    print(f'{game.get_winner().value} wins!')

def print_observation(observation: list[int]):
    indent = 2

    num_live_shells = observation[0]
    num_blank_shells = observation[1]
    init_life = observation[2]
    life_player1 = observation[3]
    life_player2 = observation[4]
    items_player1 = observation[5:5+len(BugShotItem)]
    items_player2 = observation[5+len(BugShotItem):5+2*len(BugShotItem)]
    is_opponent_handcuffed = observation[5+2*len(BugShotItem)]
    is_magnified_live = observation[5+2*len(BugShotItem)+1]
    is_magnified_blank = observation[5+2*len(BugShotItem)+2]
    is_shotgun_sawed = observation[5+2*len(BugShotItem)+3]
    
    print(f'--------------- Observation ---------------')
    print(f'{"Live shells":<{indent}}: {num_live_shells}')
    print(f'{"Blank shells":<{indent}}: {num_blank_shells}')
    print(f'{"Initial life":<{indent}}: {init_life}')
    print(f'{"Life player1":<{indent}}: {life_player1}')
    print(f'{"Life player2":<{indent}}: {life_player2}')
    print(f'{"Items player1":<{indent}}: {describe_item_board_observation(items_player1)}')
    print(f'{"Items player2":<{indent}}: {describe_item_board_observation(items_player2)}')
    print(f'{"Opponent handcuffed":<{indent}}: {is_opponent_handcuffed}')
    print(f'{"Magnified live":<{indent}}: {is_magnified_live}')
    print(f'{"Magnified blank":<{indent}}: {is_magnified_blank}')
    print(f'{"Shotgun sawed":<{indent}}: {is_shotgun_sawed}')

def describe_item_board_observation(observation: list[int]):
    return '[' + ', '.join([f'{item.value}: {observation[i]}' for i, item in enumerate(BugShotItem)]) + ']'

def input_action(valid_actions: list[BugShotAction]):
    valid_actions = [x.value for x in valid_actions]
    while True:
        print(f'Available actions: {valid_actions}')
        action = input('Enter action: ')
        try:
            action = BugShotAction(action)
            return action
        except:
            pass

if __name__ == '__main__':
    main()
