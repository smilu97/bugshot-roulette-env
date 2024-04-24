from .enums import BugShotItem, BugShotPlayer, BugShotShell

class BugShotItemBoard:

    remains: dict[BugShotItem, int]

    def __init__(self, remains: dict[BugShotItem, int]):
        for _, v in remains.items():
            if v < 0:
                raise ValueError('Remains of an item should be non-negative.')

        self.remains = remains
    
    def add_item(self, item: BugShotItem, value: int) -> 'BugShotItemBoard':
        return BugShotItemBoard(
            remains={
                **self.remains,
                item: self.remains[item] + value,
            },
        )
    
    def get_num_items(self) -> int:
        return sum(self.remains.values())

class BugShotState:

    __slots__ = [
        'turn',
        'chamber',
        'init_life',
        'life_dict',
        'item_boards',
        'is_opponent_handcuffed',
        'is_magnified_shell',
        'is_shotgun_sawed',
    ]

    turn: BugShotPlayer
    chamber: list[BugShotShell]
    init_life: int
    life_dict: dict[BugShotPlayer, int]
    item_boards: dict[BugShotPlayer, BugShotItemBoard]

    is_opponent_handcuffed: bool
    is_magnified_shell: bool
    is_shotgun_sawed: bool

    def __init__(
            self, 
            turn: BugShotPlayer,
            chamber: list[BugShotShell],
            init_life: int,
            life_dict: dict[BugShotPlayer, int],
            item_boards: dict[BugShotPlayer, BugShotItemBoard],
            is_opponent_handcuffed: bool = False,
            is_magnified_shell: bool = False,
            is_shotgun_sawed: bool = False,
        ):
        
        self.turn = turn
        self.chamber = chamber
        self.init_life = init_life
        self.life_dict = life_dict
        self.item_boards = item_boards
        
        self.is_opponent_handcuffed = is_opponent_handcuffed
        self.is_magnified_shell = is_magnified_shell
        self.is_shotgun_sawed = is_shotgun_sawed
    
    def print(self, indent: int = 0):
        indent_str = ' ' * indent
        print(f'{indent_str}Turn: {self.turn.value}')
        print(f'{indent_str}Chamber: {[x.value for x in self.chamber]}')
        print(f'{indent_str}Initial Life: {self.init_life}')
        print(f'{indent_str}Life1: {self.life_dict[BugShotPlayer.PLAYER1]}')
        print(f'{indent_str}Life2: {self.life_dict[BugShotPlayer.PLAYER2]}')
        print(f'{indent_str}Item Boards:')
        for player, item_board in self.item_boards.items():
            remains = [v for _, v in item_board.remains.items()]
            print(f'{indent_str}  {player.value}: {remains}')
        print(f'{indent_str}Opponent Handcuffed: {self.is_opponent_handcuffed}')
        print(f'{indent_str}Magnified Shell: {self.is_magnified_shell}')
        print(f'{indent_str}Shotgun Sawed: {self.is_shotgun_sawed}')

    def pass_turn(self) -> 'BugShotState':
        return BugShotState(
            turn=self.turn.opponent(),
            chamber=self.chamber,
            init_life=self.init_life,
            life_dict=self.life_dict,
            item_boards=self.item_boards,
            is_opponent_handcuffed=self.is_opponent_handcuffed,
            is_magnified_shell=self.is_magnified_shell,
            is_shotgun_sawed=self.is_shotgun_sawed,
        )
    
    def pop_chamber(self) -> 'BugShotState':
        return BugShotState(
            turn=self.turn,
            chamber=self.chamber[:-1],
            init_life=self.init_life,
            life_dict=self.life_dict,
            item_boards=self.item_boards,
            is_opponent_handcuffed=self.is_opponent_handcuffed,
            is_magnified_shell=self.is_magnified_shell,
            is_shotgun_sawed=self.is_shotgun_sawed,
        )

    def set_chamber(self, chamber: list[BugShotShell]) -> 'BugShotState':
        return BugShotState(
            turn=self.turn,
            chamber=chamber,
            init_life=self.init_life,
            life_dict=self.life_dict,
            item_boards=self.item_boards,
            is_opponent_handcuffed=self.is_opponent_handcuffed,
            is_magnified_shell=self.is_magnified_shell,
            is_shotgun_sawed=self.is_shotgun_sawed,
        )
    
    def get_item_remains(self, item: BugShotItem) -> int:
        return self.item_boards[self.turn].remains[item]

    def decrease_item_remains(self, item: BugShotItem) -> 'BugShotState':
        return BugShotState(
            turn=self.turn,
            chamber=self.chamber,
            init_life=self.init_life,
            life_dict=self.life_dict,
            item_boards={
                **self.item_boards,
                self.turn: self.item_boards[self.turn].add_item(item, -1),
            },
            is_opponent_handcuffed=self.is_opponent_handcuffed,
            is_magnified_shell=self.is_magnified_shell,
            is_shotgun_sawed=self.is_shotgun_sawed,
        )
    
    def set_item_boards(self, item_boards: dict[BugShotPlayer, BugShotItemBoard]) -> 'BugShotState':
        return BugShotState(
            turn=self.turn,
            chamber=self.chamber,
            init_life=self.init_life,
            life_dict=self.life_dict,
            item_boards=item_boards,
            is_opponent_handcuffed=self.is_opponent_handcuffed,
            is_magnified_shell=self.is_magnified_shell,
            is_shotgun_sawed=self.is_shotgun_sawed,
        )
    
    def add_life(self, player: BugShotPlayer, diff: int) -> 'BugShotState':
        return BugShotState(
            turn=self.turn,
            chamber=self.chamber,
            init_life=self.init_life,
            life_dict={
                **self.life_dict,
                player: self.life_dict[player] + diff,
            },
            item_boards=self.item_boards,
            is_opponent_handcuffed=self.is_opponent_handcuffed,
            is_magnified_shell=self.is_magnified_shell,
            is_shotgun_sawed=self.is_shotgun_sawed,
        )
    
    def handcuff_opponent(self, revert=False) -> 'BugShotState':
        return BugShotState(
            turn=self.turn,
            chamber=self.chamber,
            init_life=self.init_life,
            life_dict=self.life_dict,
            item_boards=self.item_boards,
            is_opponent_handcuffed=not revert,
            is_magnified_shell=self.is_magnified_shell,
            is_shotgun_sawed=self.is_shotgun_sawed,
        )
    
    def magnify_shell(self, revert=False) -> 'BugShotState':
        return BugShotState(
            turn=self.turn,
            chamber=self.chamber,
            init_life=self.init_life,
            life_dict=self.life_dict,
            item_boards=self.item_boards,
            is_opponent_handcuffed=self.is_opponent_handcuffed,
            is_magnified_shell=not revert,
            is_shotgun_sawed=self.is_shotgun_sawed,
        )
    
    def saw_shotgun(self, revert=False) -> 'BugShotState':
        return BugShotState(
            turn=self.turn,
            chamber=self.chamber,
            init_life=self.init_life,
            life_dict=self.life_dict,
            item_boards=self.item_boards,
            is_opponent_handcuffed=self.is_opponent_handcuffed,
            is_magnified_shell=self.is_magnified_shell,
            is_shotgun_sawed=not revert,
        )
    