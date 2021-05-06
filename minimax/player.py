import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Move():
    move = None
    cost = 0


class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    depth = None
    def __init__(self, symbol, depth): 
        super(MinimaxPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]



    def minimax(self,symbol,board,depth):
        legalMoves = game_rules.getLegalMoves(board, symbol)
        next_move = Move()
        if depth == 0 or len(legalMoves) == 0:
            next_move.cost = self.h1(board, symbol)
            return next_move

        if symbol == "x":
            new_symbol = "o"
        else:
            new_symbol = "x"

        if symbol == self.symbol:
            next_move.cost = NEG_INF
            for move in legalMoves:
                val = self.minimax(new_symbol,game_rules.makeMove(board,move),depth-1)
                if val.cost > next_move.cost:
                    next_move.cost = val.cost
                    next_move.move = move
            return next_move
        else: 
            next_move.cost = POS_INF
            for move in legalMoves:
                val = self.minimax(new_symbol,game_rules.makeMove(board,move),depth-1)
                if val.cost < next_move.cost:
                    next_move.cost = val.cost
                    next_move.move = move
            return next_move


    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return self.minimax(self.symbol,board,self.depth).move
        else: return None
        



# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    depth = None
    def __init__(self, symbol, depth): 
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth = depth

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def ab_pruning(self,symbol,board,alpha,beta,depth):
        legalMoves = game_rules.getLegalMoves(board, symbol)
        next_move = Move()
        if depth == 0 or len(legalMoves) == 0:
            next_move.cost = self.h1(board, symbol)
            return next_move

        if symbol == "x":
            new_symbol = "o"
        else:
            new_symbol = "x"

        if symbol == self.symbol:
            next_move.cost = NEG_INF
            for move in legalMoves:
                val = self.ab_pruning(new_symbol,game_rules.makeMove(board,move),alpha,beta,depth-1)
                if val.cost > next_move.cost:
                    next_move.cost = val.cost
                    next_move.move = move
                    
                alpha = max(alpha,val.cost)
                if beta<=alpha:
                    break
            return next_move
        else: 
            next_move.cost = POS_INF
            for move in legalMoves:
                val = self.ab_pruning(new_symbol,game_rules.makeMove(board,move),alpha,beta,depth-1)
                if val.cost < next_move.cost:
                    next_move.cost = val.cost
                    next_move.move = move
                beta = min(beta,val.cost)
                if beta<=alpha:
                    break
            return next_move

    # Edit this one here. :)
    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return self.ab_pruning(self.symbol,board,NEG_INF,POS_INF,self.depth).move
        else: return None


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)

