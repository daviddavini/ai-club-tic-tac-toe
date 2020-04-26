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
        print(self)

    def __str__(self):
        string = ''
        for h in self.heaps:
            string += "{} ".format(h)
        return string[:-1]

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

    def __str__(self):
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
            #Check for diagonals
            if all([self.board[i][i] == p for i in range(self.num_rows)]):
                return p
            if all([self.board[i][2-i] == p for i in range(self.num_rows)]):
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

    def display(self):
        print(self)

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

def combine_multiline_strings(strings, sep='\t'):
    lines = []
    #The size of each line so far (used for new lines)
    emptyline = ''
    for string in strings:
        #Add seperation between this line and previous line
        for i in range(len(lines)):
            lines[i] += sep
        if len(lines) != 0:
            emptyline += sep
        #Add string to lines
        split = string.splitlines()
        maxlength = max(len(l) for l in split)
        for i in range(len(lines)):
            if len(split) != 0:
                l = split.pop(0)
            else:
                l = ''
            lines[i] += l + ' '*(maxlength - len(l)) 
        for l in split:
            line = emptyline + l
            lines.append(line)
        #Update linelength
        emptyline += ' '*maxlength
    return '\n'.join(lines)

class Human(Agent):

    def choose_action(self, state):
        '''
        Query the user for an action via input
        '''
        #Print the possible actions and results
        poss_actions = state.actions()
        print('Possible Actions: ') 
        actions_str = 'Actions:\t'
        for i in range(len(poss_actions)):
            actions_str += '{}. {}\t'.format(i, poss_actions[i])
        actions_str = actions_str.expandtabs(15)
        result_strings = ['Results:']
        for poss_action in poss_actions:
            result = state.result(poss_action)
            result_strings.append(str(result))
        results_str = combine_multiline_strings(result_strings)
        results_str = results_str.expandtabs(15)
        print(actions_str)
        print(results_str)

        #Read action from user input
        successful_input = False
        while not successful_input:
            response = input("Which action would you like to take (Enter # or action)? ")
            #WARNING: The following code is dangerous
            response_eval = eval(response) 
            for i in range(len(poss_actions)):
                if response == str(i) or response == str(poss_actions[i]) or response_eval == poss_actions[i]:
                    action = poss_actions[i]
                    successful_input = True 
                    break
            else:
                print("Invalid input.")
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
        best_action = None
        best_result = None
        for poss_action in state.actions():
            #Resulting state of playing poss_action off of state
            result = state.result(poss_action)
            if result.is_terminal():
                utilities = result.utilities()
            else:
                utilities, *_ = self.predicted_utilities(result)
            if utilities[player] > best_utilities[player]:
                best_utilities = utilities
                best_action = poss_action
                best_result = result
        return best_utilities, best_action, best_result 

    def choose_action(self, state):
        '''
        Use Minimax algorithm to choose an action.
        '''
        #Player index of this agent (assumed to be the active player for state)
        player = state.player()
        #Find action that maximizes predicted utility of result of action off state
#        best_utility = -float('inf')
#        best_action = None
#        for poss_action in state.actions():
#            result = state.result(poss_action)
#            utility = self.predicted_utilities(result)[player]
#            if utility > best_utility:
#                best_utility = utility
#                best_action = poss_action
        best_utilities, best_action, *_ = self.predicted_utilities(state)
        print("Minimax worst-case utilities prediction: ", best_utilities)
        return best_action

class Game:

    def __init__(self, state, agents):
        self.state = state
        self.agents = agents

    def display(self):
        '''
        Display the current state of the game.
        '''
        state_str = str(self.state)
#        width = state_str.find('\n')
#        border = '='*(width//2 - 9)
#        full_boarder = '='*width
#        print(border, 'Current Game State', border)
#        print(state_str)
#        print(full_boarder)
        print('===================')
        print('Current Game State:')
        print(state_str)
        print('===================')

    def play(self):
        '''
        Play a game between Agent agents starting with State state.
        '''
        self.display()
        while not self.state.is_terminal():
            player = self.state.player()
            current_agent = self.agents[player]
            #Get an action from current agent
            action = current_agent.choose_action(self.state) 
            #Update game state
            self.state = self.state.result(action)
            print('Player {} made an action.'.format(player))
            #Display the game
            self.display()
           
if __name__ == '__main__':
    m = Minimax()
    h = Human()
#    s = GrundyState(11)
    s = TicTacToeState()
    g = Game(s, [h, m])
    g.play()
#    for i in range(3, 10):
#        s = GrundyState(i)
#        a = m.choose_action(s)
#        print("Grundy: # {}\tChosen Action {}\tUtilities {}".format(i, a, m.predicted_utilities(s)))

