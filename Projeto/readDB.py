import h5py

f = h5py.File('ex_table_09.h5', 'r')

g = f['table1']

for i in g:
	print i