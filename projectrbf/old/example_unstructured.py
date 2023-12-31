#!/usr/bin/env python3
import atlas4py as atlas
import math
import numpy as np


atlas.initialize() # Required, will also initialize MPI

# constants
earth_radius = 6371229.
km = 1000.

xy = np.array([
    [180,0],
    [90,0],
    [-90,0],
    [0,90],
    [0,-90],
    [0,0],
    [18,0],
    [36,0],
    [54,0],
    [72,0],
    [108,0],
    [126,0],
    [144,0],
    [162,0],
    [-162,0],
    [-144,0],
    [-126,0],
    [-108,0],
    [-72,0],
    [-54,0],
    [-36,0],
    [-18,0],
    [0,18],
    [0,36],
    [0,54],
    [0,72],
    [180,72],
    [180,54],
    [180,36],
    [180,18],
    [180,-18],
    [180,-36],
    [180,-54],
    [180,-72],
    [0,-72],
    [0,-54],
    [0,-36],
    [0,-18],
    [90,18],
    [90,36],
    [90,54],
    [90,72],
    [-90,72],
    [-90,54],
    [-90,36],
    [-90,18],
    [-90,-18],
    [-90,-36],
    [-90,-54],
    [-90,-72],
    [90,-72],
    [90,-54],
    [90,-36],
    [90,-18],
    [123.974,-58.6741],
    [154.087,-16.9547],
    [154.212,-58.8675],
    [114.377,-41.9617],
    [125.567,-23.5133],
    [137.627,-40.8524],
    [106.162,-24.5874],
    [158.508,-38.55],
    [137.826,-72.8109],
    [142.103,-26.799],
    [138.256,-13.8871],
    [168.39,-24.3266],
    [168.954,-12.0094],
    [117.333,-12.35],
    [102.254,-11.1537],
    [120.307,59.7167],
    [107.196,26.0167],
    [144.768,28.3721],
    [150.891,60.0343],
    [164.566,25.5053],
    [116.851,14.0295],
    [124.84,28.3978],
    [157.901,42.042],
    [111.41,43.1056],
    [134.333,44.6677],
    [103.277,11.707],
    [135.358,73.2119],
    [135.349,14.2311],
    [153.48,13.386],
    [168.071,11.5344],
    [-162.99,26.3775],
    [-147.519,56.1313],
    [-122.579,27.4824],
    [-117.909,59.2376],
    [-104.052,27.3616],
    [-153.107,14.9717],
    [-110.833,41.7436],
    [-144.847,32.8534],
    [-161.546,42.1031],
    [-129.866,44.5201],
    [-133.883,72.4163],
    [-166.729,11.8907],
    [-135.755,15.2529],
    [-106.063,14.4869],
    [-119.452,11.7037],
    [-146.026,-58.6741],
    [-115.913,-16.9547],
    [-115.788,-58.8675],
    [-155.623,-41.9617],
    [-144.433,-23.5133],
    [-132.373,-40.8524],
    [-163.838,-24.5874],
    [-111.492,-38.55],
    [-132.174,-72.8109],
    [-127.897,-26.799],
    [-131.744,-13.8871],
    [-101.61,-24.3266],
    [-101.046,-12.0094],
    [-152.667,-12.35],
    [-167.746,-11.1537],
    [-14.0127,-27.2963],
    [-59.193,-57.0815],
    [-56.465,-19.5751],
    [-27.056,-59.3077],
    [-57.124,-35.9752],
    [-33.4636,-28.3914],
    [-74.8037,-46.8602],
    [-40.089,-45.1376],
    [-74.8149,-28.3136],
    [-21.3072,-42.2177],
    [-44.0778,-72.6353],
    [-19.6969,-12.8527],
    [-40.1318,-12.1601],
    [-72.691,-11.4129],
    [-56.0261,58.6741],
    [-25.9127,16.9547],
    [-25.7876,58.8675],
    [-65.6229,41.9617],
    [-54.4335,23.5133],
    [-42.373,40.8524],
    [-73.838,24.5874],
    [-21.4917,38.55],
    [-42.1744,72.8109],
    [-37.8974,26.799],
    [-41.7437,13.8871],
    [-11.6095,24.3266],
    [-11.0459,12.0094],
    [-62.667,12.35],
    [-77.7456,11.1537],
    [30.3071,59.7167],
    [17.1956,26.0167],
    [54.7676,28.3721],
    [60.8915,60.0343],
    [74.5657,25.5053],
    [26.8506,14.0295],
    [34.8398,28.3978],
    [67.9014,42.042],
    [21.41,43.1056],
    [44.3335,44.6677],
    [13.2772,11.707],
    [45.3579,73.2119],
    [45.3492,14.2311],
    [63.4799,13.386],
    [78.0714,11.5344],
    [17.01,-26.3775],
    [32.4806,-56.1313],
    [57.4213,-27.4824],
    [62.0912,-59.2376],
    [75.9483,-27.3616],
    [26.893,-14.9717],
    [69.1672,-41.7436],
    [35.1527,-32.8534],
    [18.4543,-42.1031],
    [50.1344,-44.5201],
    [46.1172,-72.4163],
    [13.2711,-11.8907],
    [44.2448,-15.2529],
    [73.9368,-14.4869],
    [60.5478,-11.7037]
], dtype=np.float64)

# approximate ad hoc euclidian resolution in meters
# resolution = 2500 * km / earth_radius
# grid = atlas.UnstructuredGrid(xy)

### OR pass x,y individually
# grid = atlas.UnstructuredGrid(xy[:,0],xy[:,1])

###OR existing named grids

# approximate euclidian resolution in meters adimensionalized to unit sphere
resolution = 100 * km / earth_radius
grid = atlas.Grid("H128") # HEALPix grid #Which grid is being accessed?

# grid = atlas.Grid("O320") # HEALPix grid
# resolution = 60 * 1000    #ad hoc

# grid = atlas.Grid("O160") # HEALPix grid
# resolution = 120 * 1000   #ad hoc


###Create FunctionSpace

functionspace = atlas.functionspace.PointCloud(grid, halo_radius=resolution*2, geometry="UnitSphere")

###Access parallelisation information, typically nb_parts == mpi_size, part == mpi_rank
# print("size", functionspace.size)
# print("nb_parts", functionspace.nb_parts)
# print("part", functionspace.part)

###Access fields as numpy arrays, if needed
lonlat = atlas.make_view(functionspace.lonlat) # longitude latitude in degrees
ghost = atlas.make_view(functionspace.ghost) # ghost: 1 for ghost, 0 for owned
partition = atlas.make_view(functionspace.partition) #partition owning point (0-based)
remote_index = atlas.make_view(functionspace.remote_index) # local index on partition owning point (careful, 1-based when atlas_HAVE_FORTRAN)
global_index = atlas.make_view(functionspace.global_index) # global index across partitions (always 1-based)

# internal = [ i for i in range(functionspace.size) if ghost[i] == 0 ]
# ghosts   = [ i for i in range(functionspace.size) if ghost[i] == 1 ]

###Create field and initialize ### Can be modified to anything.
field = functionspace.create_field(name="myfield")
view = atlas.make_view(field)
for n in range(field.size):
  if not ghost[n]:
    lon = lonlat[n,0] * math.pi / 180.
    lat = lonlat[n,1] * math.pi / 180.
    view[n] = math.cos(4.*lat) * math.sin(8.*lon)
  else:
    view[n] = 0


###Halo exchange
field.halo_dirty = True  #if set to False, following halo_exchange will have no effect. Note it was already True upon create_field
field.halo_exchange() # comment to see halo with value 0, but validation below will fail
field.halo_exchange() # this will be ignored because field.halo_dirty was set to False during first call


###Validate halo exchange ### Can be deleted after testing
validation_passed = True
for n in range(field.size):
  if ghost[n]:
    lon = lonlat[n,0] * math.pi / 180.
    lat = lonlat[n,1] * math.pi / 180.
    if view[n] != math.cos(4.*lat) * math.sin(8.*lon):
      validation_passed = False

if functionspace.part == 0:
  if validation_passed:
    print("validation of halo exchange passed")
  else:
    print("validation of halo exchange failed")


###Extra: search functionality
class Search:
  def __init__(self, functionspace):
    self.functionspace = functionspace
    self.lonlat = atlas.make_view(self.functionspace.lonlat)
    self.kdtree = atlas.IndexKDTree(geometry="UnitSphere")
    self.kdtree.build(lonlat)

  def nearest_indices_within_radius(self, i, radius):
    # radius is in metres on Earth geometry
    closest_indices = self.kdtree.closest_indices_within_radius(lon=self.lonlat[i,0], lat=self.lonlat[i,1], radius=radius)
    return closest_indices[1:] #first point is "i" itself, so skip it


search = Search(functionspace)
radius = resolution
index = 0
nearest = search.nearest_indices_within_radius(index,radius)
if functionspace.part == 0:
  print("nearest global indices to local index",index," ( global index",global_index[index],"): ", [global_index[n] for n in nearest])



# if functionspace.part == 0: #choose partition to plot here
  # plot_partition(field)

# plot_global(field)

atlas.finalize()
