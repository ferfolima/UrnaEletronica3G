import numpy as np
import numpy
import scipy as sp
from scipy import misc
import h5py as hdf
import matplotlib.pyplot as plt
	
# Save the data into a hdf5 file
filename = "data.h5"

# Create and open the file with the given name
infile = hdf.File(filename, 'r')

imagem1 = infile['img_candidatos/imagem1']

#misc.imsave('teste_123.png', imagem1)
plt.imshow(imagem1)
plt.show()
