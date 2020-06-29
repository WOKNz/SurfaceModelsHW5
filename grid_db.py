import numpy as np

class CellQ:
	def __init__(self,p,id=None):
		self.p1 = [p[0],None] # to top
		self.p2 = [p[1],None] # to right
		self.p3 = [p[2],None] # to left
		self.p4 = [p[3],None] # to bottom
		self.surf_prm = None
		self.id = id

	def xy(self,variable):
		return [1, variable, variable ** 2, variable ** 3]

	def xy_t(self,variable):
		return [0, 1, 2 * variable, 3 * variable ** 2]

	def calcSurf(self):

		if self.p1[1] is None or self.p2[1] is None or self.p3[1] is None or self.p4[1] is None:
			A = np.array([[1,self.p1[0][0],self.p1[0][1],self.p1[0][0]*self.p1[0][1]],
			             [1,self.p2[0][0],self.p2[0][1],self.p2[0][0]*self.p2[0][1]],
			             [1,self.p3[0][0],self.p3[0][1],self.p3[0][0]*self.p3[0][1]],
			             [1,self.p4[0][0],self.p4[0][1],self.p4[0][0]*self.p4[0][1]]])
			l = np.array([[self.p1[0][2]],
			              [self.p2[0][2]],
			              [self.p3[0][2]],
			              [self.p4[0][2]],])
			self.surf_prm = np.dot(np.linalg.inv(A),l)

		else:

			#Bqubic
			q1 = self.p1[1].p3[1]
			q2 = self.p1[1].p2[1]
			q3 = self.p4[1].p3[1]
			q4 = self.p4[1].p2[1]
			H1 = np.array([[q1.p1[0][2],q1.p2[0][2]],[q1.p3[0][2],q1.p4[0][2]]])
			H2 = np.array([[q2.p1[0][2],q2.p2[0][2]],[q2.p3[0][2],q2.p4[0][2]]])
			H3 = np.array([[q3.p1[0][2],q3.p2[0][2]],[q3.p3[0][2],q3.p4[0][2]]])
			H4 = np.array([[q4.p1[0][2],q4.p2[0][2]],[q4.p3[0][2],q2.p4[0][2]]])
			H12 = np.hstack((H1,H2))
			H34 = np.hstack((H3,H4))
			H = np.vstack((H12,H34))
			x_a = np.array([self.xy(self.p1[0][0]),
			                self.xy_t(self.p1[0][0]),
		                    self.xy(self.p2[0][0]),
			                self.xy_t(self.p2[0][0])])
			y_a = np.array([self.xy(self.p3[0][1]),
			                self.xy_t(self.p3[0][1]),
			                self.xy(self.p1[0][1]),
			                self.xy_t(self.p1[0][1])])

			self.surf_prm = np.dot(np.linalg.inv(x_a),np.dot(H,np.linalg.inv(y_a.T)))

class Grid:
	def __init__(self,grid_x_np,grid_y_np,grid_z_np,params):
		self.grid = None
		self.ncols = grid_z_np.shape[1]
		self.nrows = grid_z_np.shape[0]
		self.xllcorner = grid_x_np[0,0] # the array is fliped
		self.yllcorner = grid_y_np[0,0] # the array is fliped
		self.cellsize = np.abs(grid_x_np[0,1]-grid_x_np[0,0])

		grid_t2 = []
		row_grid_temp = []
		for row in range(0, grid_z_np.shape[0] - 1):
			for column in range(0, grid_z_np.shape[1] - 1):
				p1 = [grid_x_np[row,column],grid_y_np[row,column],grid_z_np[row,column]]
				p2 = [grid_x_np[row,column+1],grid_y_np[row,column+1],grid_z_np[row,column+1]]
				p3 = [grid_x_np[row+1,column],grid_y_np[row+1,column],grid_z_np[row+1,column]]
				p4 = [grid_x_np[row+1,column+1],grid_y_np[row+1,column+1],grid_z_np[row+1,column+1]]
				row_grid_temp.append(CellQ([p1,p2,p3,p4],str(row)+'x'+str(column)))
			grid_t2.append(row_grid_temp)
			row_grid_temp = []
		self.grid = grid_t2

		# Updating relatives
		maxRow = len(self.grid)-1
		maxCol = len(self.grid[0])-1




		#Corners
		self.grid[0][ 0].p2[1] = self.grid[0][1]
		self.grid[0][ 0].p4[1] = self.grid[1][0]

		self.grid[0][ maxCol].p3[1] = self.grid[0][ maxCol - 1]
		self.grid[0][ maxCol].p4[1] = self.grid[1][ maxCol]

		self.grid[maxRow][ 0].p1[1] = self.grid[maxRow - 1][ 0]
		self.grid[maxRow][ 0].p2[1] = self.grid[maxRow][ 1]

		self.grid[maxRow][ maxCol].p1[1] = self.grid[maxRow - 1][ maxCol]
		self.grid[maxRow][ maxCol].p3[1] = self.grid[maxRow][ maxCol - 1]


		# Sides without Corners
		for row in range(1, maxRow):
			self.grid[row][0].p1[1] = self.grid[row-1][0]
			self.grid[row][0].p2[1] = self.grid[row][1]
			self.grid[row][0].p4[1] = self.grid[row+1][0]
		for row in range(1, maxRow):
			self.grid[row][maxCol].p1[1] = self.grid[row-1][maxCol]
			self.grid[row][maxCol].p3[1] = self.grid[row][maxCol-1]
			self.grid[row][maxCol].p4[1] = self.grid[row+1][maxCol]
		for column in range(1, maxCol):
			self.grid[0][column].p2[1] = self.grid[0][column+1]
			self.grid[0][column].p3[1] = self.grid[0][column-1]
			self.grid[0][column].p4[1] = self.grid[0+1][column]
		for column in range(1, maxCol):
			self.grid[maxRow][column].p1[1] = self.grid[maxRow-1][column]
			self.grid[maxRow][column].p2[1] = self.grid[maxRow][column+1]
			self.grid[maxRow][column].p3[1] = self.grid[maxRow][column-1]


		# Center part
		for row in range(1, maxRow):
			for column in range(1, maxCol):
				self.grid[row][column].p1[1] = self.grid[row-1][column]
				self.grid[row][column].p2[1] = self.grid[row][column+1]
				self.grid[row][column].p3[1] = self.grid[row][column-1]
				self.grid[row][column].p4[1] = self.grid[row+1][column]

		test = []
		for row in range(0, maxRow+1):
			t3 = []
			for column in range(0, maxCol+1):
				pass
			test.append(t3)
		result_test = np.array(test)

		# Calc surfaces params
		for row in range(0,len(self.grid)):
			for column in range(0,len(self.grid[0])):
				self.grid[row][column].calcSurf()