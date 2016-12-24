import sys 
import os
import numpy as np

class Board(object):
	def __init__(self, size):
		self.size = size
		self.grid = {}
	def move(self, color, x ,y):
		self.set(color, x, y)
		for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			nx = x + dx
			ny = y + dy
			cell = self.get(nx, ny)
			if cell and cell != color:
				group, liberties = self.group(nx, ny)
				if liberties == 0:
					self.remove_group(group)
	def get(self, x ,y):
		return self.grid.get((x, y))
	def set(self, color, x , y):
		self.grid[(x, y)] = color
	def remove_group(self, group):
		for x, y in group:
			self.grid.pop((x ,y))
	def group(self, x ,y):
		color = self.get(x, y)
		if not color:
			return []
		result = set()
		perimeter = {}
		self._group(x, y, color, result, perimeter)
		liberties = list(perimeter.values()).count(None)
		return sorted(result), liberties
	def _group(self, x, y, color, result, perimeter):
		if x < 0 or y < 0 or x >=self.size or y >= self.size:
			return
		if (x, y) in result:
			return
		cell = self.get(x, y)
		if cell !=color:
			perimeter[(x, y)] = cell
			return
		result.add((x, y))
		self._group(x - 1, y, color, result, perimeter)
		self._group(x + 1, y, color, result, perimeter)
		self._group(x, y - 1, color, result, perimeter)
		self._group(x, y + 1, color, result, perimeter)
	def __str__(self):
		rows = []
		for y in range(self.size):
			row = []
			for x in range(self.size):
				row.append(self.get(x, y) or '.')
			rows.append(' '.join(row))
		return '\n'.join(rows)
	def calculateLiberty(self, color, x, y):
		group, liberties = self.group(x, y)
		return liberties
	
def parse(filename):
	result = []
	with open(filename) as fp:
		for line in fp:
			if line.startswith(';B[') or line.startswith(';W['):
				tmp = line.split(';');
				for item in tmp:
					if item.startswith('B') or item.startswith('W'):
						if not item.startswith('B[]') and not item.startswith('W[]'):
							color = item[0]
							x = ord(item[2]) - ord('a')
							y = ord(item[3]) - ord('a')
							result.append((color, x ,y))
	return result
	
def loadData(path):
	files = os.listdir(path)
	for filename in files:
		if not os.path.isdir(filename):
			filepath = path + "/" + filename
			yield filepath

def main():
	totalStates = 4096
	totalCnt = 1
	path = "/home/alex/下载/KGS-2010-19-17536-/kgs-19-2010"
	pathx = "/home/alex/桌面/KGS2010/datax"
	pathy = "/home/alex/桌面/KGS2010/datay"
	print ("Initializing...")
	dx = np.zeros((totalStates,7,19,19))
	dy = np.zeros((totalStates,361))
	numStates = -1
	parsedFiles = 0
	print ("Parsing...")
	for filepath in loadData(path):
		moves = parse(filepath)
		board = Board(19)
		for i, (color, x, y) in enumerate(moves):
			numStates = numStates + 1
			if numStates >= totalStates:
				break
			board.move(color, x ,y)
			black = [k for k, v in board.grid.items() if v == 'B']
			white = [k for k, v in board.grid.items() if v == 'W']
			if i!=0:
				dy[numStates-1,x+y*19]=1;
			if i!=len(moves)-1:
				for px in range(19):
					for py in range(19):
						dx[numStates, 0, px, py] = 1
				for px, py in black:
					dx[numStates, 0, px, py] = 0
					lty = board.calculateLiberty('B', px, py)
					if lty == 1:
						dx[numStates, 1, px, py] = 1
					if lty == 2:
						dx[numStates, 2, px, py] = 1
					if lty >= 3:
						dx[numStates, 3, px, py] = 1		
				for px, py in white:
					dx[numStates, 0, px, py] = 0
					lty = board.calculateLiberty('W', px, py)
					if lty == 1:
						dx[numStates, 4, px, py] = 1
					if lty == 2:
						dx[numStates, 5, px, py] = 1
					if lty >= 3:
						dx[numStates, 6, px, py] = 1		
		if numStates >= totalStates:
			print ("ParsedFiles: ", parsedFiles)
			print ("Saving...")
			np.savez_compressed(pathx + "/" + str(totalCnt) + ".npz", dx=dx)
			np.savez_compressed(pathy + "/" + str(totalCnt) + ".npz", dy=dy)
			print ("Done!")
			print ("Initializing...")
			totalCnt += 1
			dx = np.zeros((totalStates,7,19,19))
			dy = np.zeros((totalStates,361))
			numStates = -1
			parsedFiles = 0
			print ("Parsing...")
		else:
			parsedFiles += 1
	print("Finish!")
	
if __name__ == '__main__':
	main()
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
