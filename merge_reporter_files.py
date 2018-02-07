#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      olsenk
#
# Created:     01/12/2014
# Copyright:   (c) olsenk 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import pandas as pd
import sys
import numpy as np
import os.path
import glob

def main():
    outDir = "C:\\Envision\\StudyAreas\\CentralOregon\\North\\North_20170621_NoMgmt\\"

    reporterFiles = [os.path.basename(x) for x in glob.glob(outDir + "part1\\*.csv")]

    for reporterFileName in reporterFiles:
        part1df = pd.io.parsers.read_csv(outDir + "part1\\" + reporterFileName)
        part2df = pd.io.parsers.read_csv(outDir + "part2\\" + reporterFileName)
        part2df[' Run'] = part2df[' Run'] + 10

        part1df = part1df.append(part2df, ignore_index = True)

        part1df.to_csv(outDir + reporterFileName, mode='w', header=True, index=False)

    print "Done with merge reporter files."

if __name__ == '__main__':
        # Test for correct number of arguments

    try:
        main()

    except Exception, e:
        print "\n\n" + e.args[0]

    except:
        print "unhandled Error!!"
