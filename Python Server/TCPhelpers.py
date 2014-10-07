import os
import hashlib

# string = 'yousonofabitch,networks is getting so hard. -_-;;; and bruce is just watching me code in python.'
# print 'Testing md5 with string: ', string
# k = hashlib.md5()
# k.update(string)
# print 'Digest is: ', k.hexdigest()

def generateMetaData(inputfile, blockSize):
	size = os.path.getsize(inputfile)
	print "Size of the file is: ", size
	numBlocks = size / blockSize 
	if size % blockSize != 0:
		numBlocks += 1
	print "Block size is: ", blockSize
	print "Number of blocks: ", numBlocks
	totalCheckSum = md5_for_file(inputfile, 512)
	print "Total checksum for the file: ", totalCheckSum


def md5_for_file(filename, block_size):
	f = open(filename, 'r')
	md5 = hashlib.md5()
	data = f.read(block_size)
	while data:
		md5.update(data)
		data = f.read(block_size)
	f.close()
	return md5.hexdigest()


filename = raw_input("File name: ")
generateMetaData(filename, 512)
