import abc

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
    '''
    Agent that plays user-inputted actions.
    '''

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
            try:
                response_eval = eval(response) 
                for i in range(len(poss_actions)):
                    if response == str(i) or response == str(poss_actions[i]) or response_eval == poss_actions[i]:
                        action = poss_actions[i]
                        successful_input = True 
                        break
            except:
                pass
            if not successful_input:
                print("Invalid input.")
        return action

class Minimax(Agent):
    '''
    Agent that uses Minimax to calculate the best-posible move to make.
    '''

    def predicted_utilities(self, state):
        '''
        Determine the utility of State state for player, assuming optimal stategy for every player.
        '''
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
        best_utilities, best_action, *_ = self.predicted_utilities(state)
        print("Minimax worst-case utilities prediction: ", best_utilities)
        return best_action


