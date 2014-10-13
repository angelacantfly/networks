import sys

def convertIndexToStr( index, bytes ):
    indexStr = str(index)
    numDigit = len(indexStr)
    if numDigit > bytes:
        return '-1'
    else:
        filler = '0' *  (bytes - numDigit)
        return filler + indexStr

# print 'convertIndexToStr( 500, 8) : ', convertIndexToStr( 500, 8)
# print 'convertIndexToStr( 10, 1) : ', convertIndexToStr( 10, 1)


