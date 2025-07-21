from random import randint

class MineSweeper():

	DIRS = [(-1, -1), (-1, 0), (-1, 1),
		(0, -1), (0, 1),
		(1, -1), (1, 0), (1, 1)]

	MODES = {1: ("EASY", 9, 9, 10),
		2: ("MEDIUM", 16, 16, 40),
		3: ("HARD", 16, 30, 99),
		4: ("CUSTOM", '?', '?', '?'),
		}

	def __init__(self):
		self.playGrid = []
		self.hiddenGrid = []
		self.mineLocs = []
		self.rows = 0
		self.cols = 0
		self.mines = 0
		self.gameOver = False
		self.gameLost = None
		self.safeSquares = 0
		self.squaresUncovered = 0

	def customGame(self):
		confirmed = False
		while not confirmed:
			self.rows = input("How many rows would you like?: ")
			if not self.rows.isdigit():
				print("Please enter a valid number.")
				continue
			self.rows = int(self.rows)
			self.cols = input("How many columns would you like?: ")
			if not self.cols.isdigit():
				print("Please enter a valid number.")
				continue
			self.cols = int(self.cols)
			self.mines = input("How many mines would you like?: ")
			if not self.mines.isdigit():
				print("Please enter a valid number.")
				continue
			self.mines = int(self.mines)
			print(f"You have chosen a {self.rows}x{self.cols} grid with {self.mines} mines.")
			conf = input("Are you sure this is the setup you would like to play? Y/N: ")
			if conf.upper() == 'Y':
				confirmed = True
	
	def adjList(self, r, c):
		adj = []
		for dr, dc in self.DIRS:
			nr, nc = r + dr, c + dc
			if nr >= 0 and nr < self.rows and nc >= 0 and nc < self.cols:
				adj.append((nr, nc))
			else: 
				continue
		return adj

	def createGrid(self):
		self.playGrid = [['*' for _ in range(self.cols)] for _ in range(self.rows)]
		self.hiddenGrid = [['*' for _ in range(self.cols)] for _ in range(self.rows)]
		for i in range(self.mines):
			while True:
				r, c = randint(0, self.rows - 1), randint(0, self.cols - 1)
				if self.hiddenGrid[r][c] == '*':
					self.hiddenGrid[r][c] = 'X'
					self.mineLocs.append((r, c))
					break
		for row in range(self.rows):
			for col in range(self.cols):
				if self.hiddenGrid[row][col] == 'X':
					continue
				count = 0
				for r, c in self.adjList(row, col):
					if self.hiddenGrid[r][c] == 'X':
						count += 1
				self.hiddenGrid[row][col] = count

	def setUp(self):
		for key, spec in self.MODES.items():
			print(f"{key}:{spec[0]}\tSize:{spec[1]}x{spec[2]}\tMines:{spec[3]}")
		difficulty = None
		while difficulty not in self.MODES.keys():
			difficulty = int(input("Please select a difficulty from the above list: "))
		if difficulty == 4:
			self.customGame()
			self.createGrid()
		else:
			_, self.rows, self.cols, self.mines = self.MODES[difficulty]
			self.createGrid()
		self.safeSquares = (self.rows * self.cols) - self.mines

	def help(self):
		print("DIG <row> <col>: Reveal the chosen square. If it's a mine, you lose the game.")
		print("FLAG <row> <col>: Flag the chosen square. You will not be able to DIG it without confirmation.")
		print("RULES: Display the rules of the game MineSweeper.")
		print("QUIT: Quit the game.")
		print("HELP: Display this page.")

	def rules(self):
		pass

	def uncover(self, r, c):
		stack = [(r, c)]
		while stack:
			nr, nc = stack.pop()
			if self.hiddenGrid[nr][nc] == 0 and self.playGrid[nr][nc]  == '*':
				print('passed check')
				self.playGrid[nr][nc] = 0
				print('set value')
				self.squaresUncovered += 1
				print('iter value')
				print(f"({nr}, {nc}) is adjacent to {self.adjList(nr, nc)}")
				stack.extend(self.adjList(nr, nc))
				print('added neighbours')
			elif self.playGrid[nr][nc] == '*' and not self.hiddenGrid[nr][nc] == 'X':
				print('else check')
				self.playGrid[nr][nc] = self.hiddenGrid[nr][nc]
				self.squaresUncovered += 1
				

	def playTurn(self):
		for row in self.playGrid:
			print(*row)
		action = input("What would you like to do? ").split()
		match action[0].upper():
			case "DIG":
				r, c = int(action[1]), int(action[2])
				if self.hiddenGrid[r][c] == 'F':
					check = input("Are you sure you want to dig a flagged location? Y/N: ")
					if check == 'N':
						pass
				if self.hiddenGrid[r][c] == 'X':
					self.gameOver = True
					self.gameLost = True
				else:
					self.uncover(r, c)
			case "FLAG":
				r, c = int(action[1]), int(action[2])
				if self.playGrid[r][c] == '*':
					self.playGrid[r][c] = 'F'
				elif self.playGrid == 'F':
					self.playGrid = '*'
			case "RULES":
				self.rules()
			case "QUIT":
				self.gameOver = True
			case default:
				self.help()

	def gameLoop(self):
		while not self.gameOver:
			self.playTurn()
			if self.squaresUncovered == self.safeSquares:
				self.gameOver = True
				self.gameLost = False

	def showMines(self):
		for mr, mc in self.mineLocs:
			if self.playGrid[mr][mc] == '*':
				self.playGrid[mr][mc] = 'X'
		for row in self.playGrid:
			print(*row)

	def gameEnd(self):
		if not self.gameLost:
			print("Congratulations, you won!")
		else:
			print("You hit a mine!")
			self.showMines()
			
			
def main():
	game = MineSweeper()
	game.setUp()
	game.help()
	game.gameLoop()
	game.gameEnd()		

if __name__ == "__main__":
    main()
	
		
