import games
import agents

class Match:

    def __init__(self, state, agents):
        self.state = state
        self.agents = agents

    def display(self):
        '''
        Display the current state of the game.
        '''
        state_str = str(self.state)
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
    m = agents.Minimax()
    h = agents.Human()
    s = games.GrundyState(11)
#    s = games.TicTacToeState()
    g = Match(s, [h, m])
    g.play()
#    for i in range(3, 10):
#        s = GrundyState(i)
#        a = m.choose_action(s)
#        print("Grundy: # {}\tChosen Action {}\tUtilities {}".format(i, a, m.predicted_utilities(s)))

