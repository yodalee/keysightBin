import sys
import numpy as np
import struct


def readfile(binFile):
    """read binFile and return data as numpy array
    """
    try:
        fd = open(binFile, 'rb')
        fileCookie = struct.unpack('2c', fd.read(2))
        fileVersion = struct.unpack('2c', fd.read(2))
        fileSize = struct.unpack('i', fd.read(2))
        nWaveforms = struct.unpack('i', fd.read(1))

        if fileCookie != "AG":
            sys.stderr.write("Unrecognized file format\n")
            return None, None



    except IOError:
        sys.stderr.write("%s open error\n" & (binFile))
        return None, None
    finally:
        fd.close()
