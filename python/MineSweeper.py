from random import randint

class MineSweeper():

	class Square():
		def __init__(self, content):
			self.shown = content
			self.hidden = ''
			self.colour = '\033[0m'

		def __str__(self):
			str = self.colour + self.shown #+ '\033[0m'
			return str

	DIRS = [(-1, -1), (-1, 0), (-1, 1),
		(0, -1), (0, 1),
		(1, -1), (1, 0), (1, 1)]

	MODES = {1: ("EASY", 9, 9, 10),
		2: ("MEDIUM", 16, 16, 40),
		3: ("HARD", 16, 30, 99),
		4: ("CUSTOM", '?', '?', '?'),
		}

	COLOUR = {'0': "\033[0;47m",
		'1': "\033[30;47m",
		'2': "\033[31;47m",
		'3': "\033[32;47m",
		'4': "\033[33;47m",
		'5': "\033[34;47m",
		'6': "\033[35;47m",
		'7': "\033[36;47m",
		'8': "\033[90;47m",
		'X': "\033[0;31m",
		'X#': "\033[30;41m",
		'F': "\033[91;47m",
		'F+': "\033[92;107m",
		'F-': "\033[91;107m",
		'*': "\033[97;100m",
		' ': "\033[0m",
		}	

	def __init__(self):
		self.colourGrid = [[' ']]
		self.greyGrid = [[' ']]
		self.mineLocs = []
		self.falseFlags = []
		self.rows = 0
		self.cols = 0
		self.mines = 0
		self.flags = 0
		self.gameOver = False
		self.gameLost = None
		self.safeSquares = 0
		self.squaresUncovered = 0
		self.colour = False

	def printBoard(self):
		if self.colour:
			for row in self.colourGrid:
				print(*row, end='')
				print("\033[0m")
		else:
			for row in self.greyGrid:
				print(*row)

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
		if self.cols < 10:
			self.colourGrid[0].extend([(' ' + str(i)) for i in range(1, self.cols + 1)])
			self.greyGrid[0].extend([(' ' + str(i)) for i in range(1, self.cols + 1)])
		else:
			self.colourGrid[0].extend([(' ' + str(i)) for i in range(1, 10)])
			self.colourGrid[0].extend([i for i in range(10, self.cols + 1)])
			self.greyGrid[0].extend([(' ' + str(i)) for i in range(1, 10)])
			self.greyGrid[0].extend([i for i in range(10, self.cols + 1)])
		for i in range(1, self.rows + 1):
			if i < 10:
				self.colourGrid.append([(' ' + str(i))])
				self.greyGrid.append([(' ' + str(i))])
			else:
				self.colourGrid.append([i])
				self.greyGrid.append([i])
			if self.cols < 10:
				self.colourGrid[i].extend([self.Square('* ') for _ in range(self.cols)])
				self.greyGrid[i].extend(['* ' for _ in range(self.cols)])
			else:
				self.colourGrid[i].extend([self.Square('* ') for _ in range(9)])
				self.colourGrid[i].extend([self.Square('*')])
				self.colourGrid[i].extend([self.Square(' *') for _ in range(10, self.cols)])
				self.greyGrid[i].extend(['* ' for _ in range(9)])
				self.greyGrid[i].extend(['*'])
				self.greyGrid[i].extend([' *' for _ in range(10, self.cols)])


		for _ in range(self.mines):
			while True:
				r, c = randint(1, self.rows), randint(1, self.cols)
				if not self.colourGrid[r][c].hidden == 'X':
					self.colourGrid[r][c].hidden = 'X'
					self.mineLocs.append((r, c))
					break

		for row in range(1, self.rows + 1):
			for col in range(1, self.cols + 1):
				self.colourGrid[row][col].colour = self.COLOUR[self.colourGrid[row][col].shown.strip()]
				if self.colourGrid[row][col].hidden == 'X':
					continue
				count = 0
				for r, c in self.adjList(row, col):
					if self.colourGrid[r][c].hidden == 'X':
						count += 1
				self.colourGrid[row][col].hidden = str(count)

	def setUp(self):
		for key, spec in self.MODES.items():
			print(f"{key}:{spec[0]} Size:{spec[1]}x{spec[2]} Mines:{spec[3]}")
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
		print("COLOUR: Switch between colour and greyscale")
		print("QUIT: Quit the game.")
		print("HELP: Display this page.\n")

	def rules(self):
		print("\nI feel like you should know these already. I'll fill them in later maybe.\n")

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
			if self.colourGrid[nr][nc].hidden == '0' and self.colourGrid[nr][nc].shown.strip()  == '*':
				self.colourGrid[nr][nc].shown = self.swapChar(self.colourGrid[nr][nc].shown, 0)
				self.greyGrid[nr][nc] = self.colourGrid[nr][nc].shown
				self.colourGrid[nr][nc].colour = self.COLOUR[self.colourGrid[nr][nc].shown.strip()]
				self.squaresUncovered += 1
				stack.extend(self.adjList(nr, nc))
			elif self.colourGrid[nr][nc].shown.strip() == '*' and not self.colourGrid[nr][nc].hidden == 'X':
				self.colourGrid[nr][nc].shown = self.swapChar(self.colourGrid[nr][nc].shown, self.colourGrid[nr][nc].hidden)
				self.greyGrid[nr][nc] = self.colourGrid[nr][nc].shown
				self.colourGrid[nr][nc].colour = self.COLOUR[self.colourGrid[nr][nc].shown.strip()]
				self.squaresUncovered += 1
				

	def playTurn(self):
		self.printBoard()
		print(f"Mines Remaining: {self.mines - self.flags}")
		action = input("What would you like to do? ").split()
		match action[0].upper():
			case "DIG":
				try:
					r, c = int(action[1]), int(action[2])
				except IndexError:
					self.help()
					return
				if self.colourGrid[r][c].shown.strip() == 'F':
					check = input("Are you sure you want to dig a flagged location? Y/N: ").upper()
					if check == 'N':
						return
				if self.colourGrid[r][c].hidden == 'X':
					self.colourGrid[r][c].shown = self.swapChar(self.colourGrid[r][c].shown, 'X')
					self.gameOver = True
					self.gameLost = True
				else:
					self.uncover(r, c)
			case "FLAG":
				try:
					r, c = int(action[1]), int(action[2])
				except IndexError:
					self.help()
					return
				if self.colourGrid[r][c].shown.strip() == '*':
					self.flags += 1
					self.colourGrid[r][c].shown = self.swapChar(self.colourGrid[r][c].shown, 'F')
					self.greyGrid[r][c] = self.colourGrid[r][c].shown
					if self.colourGrid[r][c].hidden == 'X':
						self.falseFlags.append((r, c))
				elif self.colourGrid[r][c].strip() == 'F':
					self.flags -= 1
					self.colourGrid[r][c] = self.swapChar(self.colourGrid[r][c], '*')
					self.greyGrid[r][c] = self.colourGrid[r][c].shown
			case "EXPAND":
				try:
					r, c = int(action[1]), int(action[2])
				except IndexError:
					self.help()
					return
				self.expandSquare(r, c)
			case "END":
				self.quickEnd()
			case "RULES":
				self.rules()
			case "COLOUR":
				self.colour = not self.colour
			case "QUIT":
				self.gameOver = True
			case default:
				self.help()

	def expandSquare(self, r, c):
		adj = self.adjList(r, c)
		for ar, ac in adj:
			if self.colourGrid[ar][ac].hidden == 'X' and not self.colourGrid[ar][ac].shown.strip() == 'F':
				self.colourGrid[ar][ac].shown = self.swapChar(self.colourGrid[ar][ac], 'X')
				self.gameOver = True
				self.gameLost = True
			else:
				self.uncover(ar, ac)

	def quickEnd(self):
		self.gameOver = True
		self.gameLost = False
		for mr, mc in self.mineLocs:
			if self.colourGrid[mr][mc].shown.strip() == '*':
				self.colourGrid[mr][mc].shown = self.swapChar(self.colourGrid[mr][mc].shown, 'X')
				self.gameLost = True
				

	def gameLoop(self):
		while not self.gameOver:
			self.playTurn()
			if self.squaresUncovered == self.safeSquares:
				self.gameOver = True
				self.gameLost = False

	def showMines(self):
		for mr, mc in self.mineLocs:
			match self.colourGrid[mr][mc].shown.strip():
				case '*':
					self.colourGrid[mr][mc].shown = self.swapChar(self.colourGrid[mr][mc].shown, 'X')
					self.greyGrid[mr][mc] = self.colourGrid[mr][mc].shown
					self.colourGrid[mr][mc].colour = self.COLOUR['X']
				case 'X':
					self.greyGrid[mr][mc] = self.colourGrid[mr][mc].shown
					self.colourGrid[mr][mc].colour = self.COLOUR['X#']
				case 'F':
					self.colourGrid[mr][mc].colour = self.COLOUR['F+']
		for fr, fc in self.falseFlags:
			if self.colourGrid[fr][fc].shown.strip() == 'F':
				self.colourGrid[fr][fc].colour = self.COLOUR['F-']
				self.greyGrid[fr][fc] = self.swapChar(self.greyGrid[fr][fc], 'f')
		self.printBoard()

	def gameEnd(self):
		if self.gameLost == None:
			return
		elif not self.gameLost:
			print("Congratulations, you won!")
			self.printBoard()
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
	
		
