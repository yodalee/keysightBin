import sys
import numpy as np
import struct
from collections import namedtuple


def readfile(binFile, arg):
    """read binFile and return data as numpy array
    :binFile: path to bin file
    :arg: an int, indicate the nth waveform to read
    """
    selWav = 0
    headerFmt = "5if3d2i16s16s24s16sdI"
    headerSiz = struct.calcsize(headerFmt) 
    waveformHeader = namedtuple("waveformHeader",
        "headerSize waveformType nWaveformBuffers nPoints \
        count xDisplayRange xDisplayOrigin xIncrement \
        xOrigin xUnits yUnits dateString timeString \
        frameString waveformString timeTag segmentIndex")
    bufHeaderFmt = "ihhi"
    bufHeaderSiz = struct.calcsize(bufHeaderFmt)
    bufHeader = namedtuple("bufHeader",
        "headerSize bufferType bytesPerPoint bufferSize")

    data = None
    time = None

    try:
        fd = open(binFile, 'rb')
        magic, fileVer, fileSize, nWav = struct.unpack(
            '2s2sii', fd.read(12))

        if magic.decode('ascii') != "AG":
            sys.stderr.write("Unrecognized file format\n")
            return None, None

        if arg and arg <= nWav:
            selWav = arg

        for idx in range(nWav):
            # read waveform header
            header = waveformHeader._make(
                    struct.unpack(headerFmt, fd.read(headerSiz)))
            # skip remaining data in the header
            fd.seek(header.headerSize - headerSiz, 1)

            if idx == selWav:
                stop = header.xIncrement * header.nPoints + header.xOrigin
                time = np.linspace(header.xOrigin, stop, header.nPoints)

            for bufIdx in range(header.nWaveformBuffers):
                bufferHeader = bufHeader._make(
                        struct.unpack(bufHeaderFmt, fd.read(bufHeaderSiz)))
                if idx == selWav:
                    if bufferHeader.bufferType in [1, 2, 3]:
                        fmt = "%df" % (header.nPoints)
                    elif bufferHeader.bufferType == 4:
                        fmt = "%di" % (header.nPoints)
                    elif bufferHeader.bufferType == 5:
                        fmt = "%dB" % (header.nPoints)
                    else:
                        fmt = "%dB" % (header.bufferSize)
                    data = np.asarray(struct.unpack(
                        fmt, fd.read(struct.calcsize(fmt))))
                else:
                    # skip waveform
                    fd.seek(bufferHeader.bufferSize, 1)

        return time, data
    except IOError:
        sys.stderr.write("%s open error\n" & (binFile))
        return None, None
    finally:
        fd.close()
