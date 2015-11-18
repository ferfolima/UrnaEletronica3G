filein = open('string.txt', 'r')
string = filein.readline()
filein.close()

print string

fileout = open('string.txt', 'aw')
fileout.write('\n\n\n\n\nIsso eh um teste')
fileout.close()