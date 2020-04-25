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
    def display(self):
        '''
        Prints state to screen in human-readable format.
        '''
        pass
    
class GrundyState(State):

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

    def display(self):
        for h in self.heaps:
            print(h, end=" ")
        print()

class TicTacToeState(State):
    '''
    State for the TicTacToe game.

    Attributes:
    board - the layout of the pieces on the board. (0 = none, 1 = 'X', 2 = 'O')
    player - the index of the player who has the move.
    '''
    
    num_rows = 3
    num_cols = 3
    num_players = 2

    def __init__(self, board=None):
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

    def display(self):
        print(" ", end='')
        for j in range(self.num_cols):
            print(" {}".format(j), end='')
        print()
        for i in range(self.num_rows):
            print("{} ".format(i), end='')
            for j in range(self.num_cols):
                print("{} ".format(self.player_char(self.board[i][j])), end='')
            print()

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
            #Check for diagonals
            if all([self.board[i][i] == p for i in range(self.num_rows)]):
                return p
        return -1

    def is_terminal(self):
        return self.winner() != -1

    def utilities(self):
        winner = self.winner()
        if winner ==  -1:
            return (0,0)
        elif winner == 0:
            return (1,-1)
        elif winner == 1:
            return (-1,1)

class Agent:
    '''
    A player of games.
    '''
    @abc.abstractmethod
    def choose_move(self, state):
        '''
        Returns:
        action - the action that the agent has chosen to take off of State state
        '''
        pass

class Human(Agent):

    def choose_action(self, state):
        '''
        Query the user for an action via input
        '''
        #Display possible moves
        state.display()
        poss_actions = state.actions()
        print("Possible Actions: {}".format(poss_actions))

        #Read action from user input
        successful_input = False
        while not successful_input:
            response = input("Where would you like to move?")
            for poss_action in poss_actions:
                if response == str(poss_action):
                    action = poss_action
                    successful_input = True 
                    break
            else:
                print("Invalid input. Type the action you wish to choose exactly.")
        return action

class Minimax(Agent):

    def predicted_utilities(self, state):
        '''
        Determine the utility of State state for player, assuming optimal stategy for every player.
        '''
#        state.display()
#        input()
        #Calculate the best resulting State off of state for the player who plays off state, and its utilities vector
        player = state.player()
        best_utilities = tuple(-float('inf') for i in range(state.num_players))
        best_result = None
        for poss_action in state.actions():
            #Resulting state of playing poss_action off of state
            result = state.result(poss_action)
            if result.is_terminal():
                utilities = result.utilities()
            else:
                utilities = self.predicted_utilities(result)
            if utilities[player] > best_utilities[player]:
                best_utilities = utilities
        return best_utilities 

    def choose_action(self, state):
        '''
        Use Minimax algorithm to choose an action.
        '''
        #Player index of this agent (assumed to be the active player for state)
        player = state.player()
        #Find action that maximizes predicted utility of result of action off state
        action = max([poss_action for poss_action in state.actions()], key=lambda a : self.predicted_utilities(state.result(a))[player])
        return action


def play_game(state, agents):
    '''
    Play a game between Agent agents starting with State state.
    '''
    while not state.is_terminal():
        current_agent = agents[state.player()]
        #Get an action from current agent
        action = current_agent.choose_action(state) 
        #Update game state
        state = state.result(action)

if __name__ == '__main__':
    #s = TicTacToeState()
    m = Minimax()
    for i in range(3, 10):
        s = GrundyState(i)
        a = m.choose_action(s)
        print("Grundy: # {}\tChosen Action {}\tUtilities {}".format(i, a, m.predicted_utilities(s)))

