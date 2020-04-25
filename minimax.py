import abc 

class State(ABC):
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
    def terminal_test(self):
        '''
        Returns:
        bool - true iff game over at this state.
        '''
        pass


