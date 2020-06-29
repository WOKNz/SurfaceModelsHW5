import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from plotVTK import plot as vtkPlot
from grid_db import Grid


#IMporting data
dem = np.genfromtxt('data/dem_50.asc',skip_header=6)
params = pd.read_csv('data/dem_50.asc',nrows=6,delim_whitespace=True,header=None)
params.columns = ['Key','Value']
params = pd.Series(params.Value.values,index=params.Key).to_dict()

# Testing input
# plt.imshow(dem)
# plt.show()

# Min max elevation
dem_max = np.max(dem)
dem_min = np.min(dem)

# Creating arrays for X and Y
demX = np.zeros(dem.shape)
demY = np.zeros(dem.shape)

# Flipping data on X axis for easier manipulation on demx/demY
dem = np.flip(dem, axis=0)

# Filling demX/demY
for row in range(0,dem.shape[0]):
	for column in range(0,dem.shape[1]):
		demX[row,column] = params['cellsize']*column+params['xllcorner']
		demY[row,column] = params['cellsize']*row+params['yllcorner']

# Creating points
points = np.vstack((demX.flatten(),demY.flatten(),dem.flatten()))
points = (points.T).tolist()

# Creating triangles
triangles = []
for row in range(0,dem.shape[0]-1):
	for column in range(0,dem.shape[1]-1):
		p1 = row*dem.shape[1]+column
		p2 = row*dem.shape[1]+column+1
		p3 = (row+1)*dem.shape[1]+column
		p4 = (row+1)*dem.shape[1]+column+1
		triangles.append([p1,p2,p3])
		triangles.append([p2,p4,p3])
dem_flat = dem.flatten()

# Creating Colors
colors = []
for row in range(0,dem.shape[0]):
	for column in range(0,dem.shape[1]):
		color = ((dem[row,column]-dem_min)/dem_max)*255
		colors.append([color])

# VTK plot result
colors_np = np.ones((len(points),3))*200
points_np = np.array(points)
triangles_np = np.array(triangles)
vtkPlot(points_np,triangles_np,colors_np,0)
vtkPlot(points_np,triangles_np,colors_np,1)

colors_np = np.array(colors).astype(int)
colors_np = np.hstack((colors_np,colors_np,colors_np))
vtkPlot(points_np,triangles_np,colors_np,5)


#Creating grid of cells
i_grid = Grid(demX,demY,dem,params)


f = open("export.asc","w+")
f.write("ncols %d\n" % i_grid.ncols)
f.write("nrows %d\n" % i_grid.nrows)
f.write("xllcorner %d\n" % i_grid.xllcorner)
f.write("yllcorner %d\n" % i_grid.yllcorner)
f.write("cellsize %d\n" % i_grid.cellsize)
f.write("NODATA_value %d\n" % -9999)
f.close()

f = open("export.asc", 'a')

a = np.array([1.2, 2.3, 4.5])
b = np.array([6.7, 8.9, 10.11])
c = np.array([12.13, 14.15, 16.17])
for i in range(0,dem.shape[0]):
	np.savetxt(f, dem[-(i+1),:], fmt='%1.4f', newline=" ")
	f.write("\n")
f.close()

print('pause')
