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
			self.rows, self.cols, self.mines = 0, 0, 0
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
			if self.mines > (self.rows * self.cols):
				print("You have selected more mines than squares available.")
				continue
			print(f"You have chosen a {self.rows}x{self.cols} grid with {self.mines} mines.")
			conf = input("Are you sure this is the setup you would like to play? Y/N: ")
			if conf.upper() == 'Y':
				confirmed = True
	
	def adjList(self, r, c):
		adj = []
		for dr, dc in self.DIRS:
			nr, nc = r + dr, c + dc
			if nr >= 1 and nr <= self.rows and nc >= 1 and nc <= self.cols:
				adj.append((nr, nc))
			else: 
				continue
		return adj

	def createGrid(self):
		self.playGrid = []
		self.playGrid.append(['#'])
		if self.cols < 10:
			self.playGrid[0].extend([(' ' + str(i)) for i in range(1, self.cols + 1)])
		else:
			self.playGrid[0].extend([(' ' + str(i)) for i in range(1, 10)])
			self.playGrid[0].extend([i for i in range(10, self.cols + 1)])
		for i in range(1, self.rows + 1):
			if i < 10:
				self.playGrid.append([(' ' + str(i))])
			else:
				self.playGrid.append([i])
			if self.cols < 10:
				self.playGrid[i].extend(['* ' for _ in range(self.cols)])
			else:
				self.playGrid[i].extend(['* ' for _ in range(9)])
				self.playGrid[i].extend(['*'])
				self.playGrid[i].extend([' *' for _ in range(10, self.cols)])

		self.hiddenGrid = [['*' for _ in range(self.cols + 1)] for _ in range(self.rows + 1)]
		#self.hiddenGrid.append(['#'])
		#self.hiddenGrid[0].extend([i for i in range(1, self.cols + 1)])
		#for i in range(1, self.rows + 1):
			#self.hiddenGrid.append([i])
			#self.hiddenGrid[i].extend(['*' for _ in range(self.cols)])

		for _ in range(self.mines):
			while True:
				r, c = randint(1, self.rows), randint(1, self.cols)
				if self.hiddenGrid[r][c] == '*':
					self.hiddenGrid[r][c] = 'X'
					self.mineLocs.append((r, c))
					break

		for row in range(1, self.rows + 1):
			for col in range(1, self.cols + 1):
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
		print("\nDIG <row> <col>: Reveal the chosen square. If it's a mine, you lose the game.")
		print("FLAG <row> <col>: Flag the chosen square. You will not be able to DIG it without confirmation.")
		print("EXPAND <row> <col>: Reveal all unflagged squares around the chosen square. If any are mines, you lose the game.")
		print("END: Reveal all unflagged squares. If any are mines, you lose the game.")
		print("RULES: Display the rules of the game MineSweeper.")
		print("QUIT: Quit the game.")
		print("HELP: Display this page.\n")

	def rules(self):
		pass

	def swapChar(self, curr, new):
		new = str(new)
		match curr:
			case ' *':
				new = ' ' + new
			case '* ':
				new = new + ' '
			case ' F':
				new = ' ' + new
			case 'F ':
				new = new + ' '
		return new

	def uncover(self, r, c):
		stack = [(r, c)]
		while stack:
			nr, nc = stack.pop()
			if self.hiddenGrid[nr][nc] == 0 and self.playGrid[nr][nc].strip()  == '*':
				self.playGrid[nr][nc] = self.swapChar(self.playGrid[nr][nc], 0)
				self.squaresUncovered += 1
				stack.extend(self.adjList(nr, nc))
			elif self.playGrid[nr][nc].strip() == '*' and not self.hiddenGrid[nr][nc] == 'X':
				self.playGrid[nr][nc] = self.swapChar(self.playGrid[nr][nc], self.hiddenGrid[nr][nc])
				self.squaresUncovered += 1
				

	def playTurn(self):
		for row in self.playGrid:
			print(*row)
		action = input("What would you like to do? ").split()
		match action[0].upper():
			case "DIG":
				r, c = int(action[1]), int(action[2])
				if self.playGrid[r][c].strip() == 'F':
					check = input("Are you sure you want to dig a flagged location? Y/N: ").upper()
					if check == 'N':
						return
				if self.hiddenGrid[r][c] == 'X':
					self.gameOver = True
					self.gameLost = True
				else:
					self.uncover(r, c)
			case "FLAG":
				r, c = int(action[1]), int(action[2])
				if self.playGrid[r][c].strip() == '*':
					self.playGrid[r][c] = self.swapChar(self.playGrid[r][c], 'F')
				elif self.playGrid[r][c].strip() == 'F':
					self.playGrid[r][c] = self.swapChar(self.playGrid[r][c], '*')
			case "EXPAND":
				r, c = int(action[1]), int(action[2])
				self.expandSquare(r, c)
			case "END":
				self.quickEnd()
			case "RULES":
				self.rules()
			case "QUIT":
				self.gameOver = True
			case default:
				self.help()

	def expandSquare(self, r, c):
		adj = self.adjList(r, c)
		for ar, ac in adj:
			if self.hiddenGrid[ar][ac] == 'X' and not self.playGrid[ar][ac].strip() == 'F':
				self.gameOver = True
				self.gameLost = True
				break
			else:
				self.uncover(ar, ac)

	def quickEnd(self):
		self.gameOver = True
		self.gameLost = False
		for mr, mc in self.mineLocs:
			if self.playGrid[mr][mc].strip() == 'F':
				self.gameLost = True
				break

	def gameLoop(self):
		while not self.gameOver:
			self.playTurn()
			if self.squaresUncovered == self.safeSquares:
				self.gameOver = True
				self.gameLost = False

	def showMines(self):
		for mr, mc in self.mineLocs:
			if self.playGrid[mr][mc].strip() == '*':
				self.playGrid[mr][mc] = self.swapChar(self.playGrid[mr][mc], 'X')
		for row in self.playGrid:
			print(*row)

	def gameEnd(self):
		if self.gameLost == None:
			return
		elif not self.gameLost:
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
	
		
