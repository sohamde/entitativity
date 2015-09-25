## class to play a two player game
## authors: soham de, patrick roos
## emails: (sohamde, roos) at cs umd edu

from utils import mean, transpose


class TwoPlayerGame:
	"""
	Class to play a two player game
	"""
	 
	def __init__(self, player1, player2, player1Neighs, player2Neighs, payoffmat):
		"""
		Initializing the two players
		"""
		
		self.players = [ player1, player2 ]
		self.payoffmat = payoffmat
		self.opponents = {player1:player2, player2:player1}

		self.player1Neighs = player1Neighs
		self.player2Neighs = player2Neighs

		# history will be a list of moves for each iteration ((p1_move, p2_move), (p1move, p2_move), ...)
		self.history = list() 
		
		
	def run(self, fullEnt = False, game_iter=1):
		"""
		Recording both players' moves
		"""
		
		player1, player2 = self.players

		# each iteration, get new moves and append these to history
		for iteration in range(game_iter):
			if fullEnt:
				newmoves = player1.move(self, self.player1Neighs), player2.move(self, self.player2Neighs)
			else:
				newmoves = player1.move(self, []), player2.move(self, [])
			self.history.append(newmoves)
			
		# prompt players to record the game played (i.e., 'self')
		player1.record(self); player2.record(self)
		
	def get_payoffs(self):
		"""
		Return payoff received for both players
		"""

		player1, player2 = self.players     # unpack the two players

		# generate a payoff pair for each game iteration in history
		payoffs = (self.payoffmat[m1][m2] for (m1,m2) in self.history)
		pay1, pay2 = transpose(payoffs)     # transpose to get a payoff sequence for each player

		return { player1:mean(pay1), player2:mean(pay2) }       # return a mapping of each player to its mean payoff

	def get_last_move(self, player):
		"""
		if history not empty, return prior move of `player`
		"""

		if self.history:
			player_idx = self.players.index(player)
			last_move = self.history[-1][player_idx]
		else:
			last_move = None
		return last_move
	
	def get_coops_defects(self, player):
		"""
		return number of cooperations and defections for a player
		"""

		defects = 0
		coops = 0
		playerIndex = self.players.index(player)
		for moves in self.history:	
			if moves[playerIndex] == 0:
				coops+=1
			else:	
				defects +=1
		
		return (coops, defects)

