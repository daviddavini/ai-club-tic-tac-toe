import abc 
import copy

class State(abc.ABC):
    '''Represents a possible configuration of the game after a certain amount of time.'''

    @abc.abstractmethod
    def player(self):
        '''
        Returns:   
        int - the index of the player who has the move in this state.
        '''
        pass

    @abc.abstractmethod
    def actions(self):
        '''
        Returns:
        list of Action - the valid actions the player who has the move can make off of this state.
        '''
        pass

    @abc.abstractmethod
    def result(self, a):
        '''
        Returns:
        State - the result of playing Action a off of this state.
        '''
        pass

    @abc.abstractmethod
    def is_terminal(self):
        '''
        Returns:
        bool - true iff game over at this state.
        '''
        pass

    @abc.abstractmethod
    def utilities(self):
        '''
        Returns:
        float - the utility vector of this state (zero vector if not terminal node)
        '''
        pass

    @abc.abstractmethod
    def display_string(self):
        '''
        Returns:
        str - A multi-line string representing the game state.
        '''
        pass
    
    def __str__(self):
        return self.display_string()

class GrundyState(State):
    '''
    State for Grundy's game.

    Attributes:
    heaps - a list of numbers representing the amount in each heap.
    player_index - the index of the player who has the move.
    '''
 
    num_players = 2

    def __init__(self, heaps = 11):
        if type(heaps) == int:
            self.heaps = [heaps]
        else:
            self.heaps = heaps
        self.player_index = 0

    def player(self):
        return self.player_index

    def actions(self):
        actions = []
        for i in range(len(self.heaps)):
            for x in range(1, (self.heaps[i]-1)//2 + 1):
                action = (i, x)
                actions.append(action)
        return actions

    def result(self, action):
        i, x = action
        y = self.heaps[i] - x
        result = copy.copy(self)
        result.heaps = result.heaps[:i] + [x, y] + result.heaps[i+1:]
        result.player_index = (result.player_index + 1) % 2
        return result

    def is_terminal(self):
        return len(self.actions()) == 0

    def utilities(self):
        if self.is_terminal():
            utilities = [-1 for i in range(self.num_players)]
            utilities[self.player_index - 1] = 1
            utilities = tuple(utilities)
        else:
            utilities = tuple(0 for i in range(self.num_players))
        return utilities

    def display_string(self):
        string = ''
        for h in self.heaps:
            string += "{} ".format(h)
        return string[:-1]

class TicTacToeState(State):
    '''
    State for a TicTacToe game.

    Attributes:
    board - the layout of the pieces on the board. (0 = none, 1 = 'X', 2 = 'O')
    player_index - the index of the player who has the move.
    '''
   
    num_players = 2

    def __init__(self, board=None, dims = (3,3)):
        num_rows, num_cols = dims
        self.num_rows = num_rows
        self.num_cols = num_cols
        if board:
            self.board = copy.deepcopy(board)
        else:
            self.board = [[-1 for i in range(self.num_rows)] for i in range(self.num_cols)]
        self.player_index = 0

    def player_char(self, player):
        if player == 0:
            return 'X'
        elif player == 1:
            return 'O'
        else: 
            return '.'

    def display_string(self):
        string = ' '
        for j in range(self.num_cols):
            string += " {}".format(j)
        string += '\n'
        for i in range(self.num_rows):
            string += "{} ".format(i)
            for j in range(self.num_cols):
                string += "{} ".format(self.player_char(self.board[i][j]))
            string += '\n'
        return string[:-1]

    def player(self):
        return self.player_index

    def actions(self):
        actions = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == -1:
                    actions.append((i,j))
        return actions

    def result(self, action):
        #Copy this state
        child = copy.deepcopy(self)
        #Add piece
        i, j = action
        child.board[i][j] = child.player_index
        #Increment player index
        child.player_index = (child.player_index + 1) % 2 
        return child

    def winner(self):
        for p in range(2):
            #Check for horizontal lines
            for i in range(self.num_rows):
                if all([self.board[i][j] == p for j in range(self.num_cols)]):
                    return p
            #Check for vertical lines
            for j in range(self.num_cols):
                if all([self.board[i][j] == p for i in range(self.num_rows)]):
                    return p
            #Check for diagonals (code only works with square boards)
            if self.num_rows == self.num_cols:
                if all([self.board[i][i] == p for i in range(self.num_rows)]):
                    return p
                if all([self.board[i][self.num_rows-i-1] == p for i in range(self.num_rows)]):
                    return p
        return -1

    def full_board(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.board[i][j] == -1:
                    return False
        return True

    def is_terminal(self):
        return self.full_board() or self.winner() != -1

    def utilities(self):
        winner = self.winner()
        if winner ==  -1:
            return (0,0)
        elif winner == 0:
            return (1,-1)
        elif winner == 1:
            return (-1,1)


