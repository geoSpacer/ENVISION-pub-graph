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
from matplotlib.backends.backend_pdf import PdfPages
import sys
import reporterFunc

def main(subArea, runName, chartTitlePre):
    outDir = "C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_test\\" + runName + "\\"
    yLabelText = 'Tree Volume (m3)'
    varList = [' Volume of Live Trees (m3)', ' Volume of Dead Trees (m3)', ' Volume of Live and Dead (m3)']

    repList = list(set(pd.io.parsers.read_csv(outDir + r'VolumeAllTrees_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_TotalVolume_compare.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot total area
        totalArea = pd.io.parsers.read_csv(outDir + r'VolumeAllTrees_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]
        totalArea2 = pd.io.parsers.read_csv("C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_production\\North_20150923_CurrentPolicy\\" + r'VolumeAllTrees_pivot.csv')
        totalArea2 = totalArea2[totalArea2[' Run'] == repNum]

        reporterFunc.plotReporter_compare('', pdfFile, totalArea, totalArea2, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'VolumeAllTrees_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]
        totalArea2 = pd.io.parsers.read_csv("C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_production\\North_20150923_CurrentPolicy\\" + r'VolumeAllTrees_by_OWNER_pivot.csv')
        totalArea2 = totalArea2[totalArea2[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            byOwner2 = totalArea2[totalArea2[' OWNER_label'] == owner]
            reporterFunc.plotReporter_compare(owner, pdfFile, byOwner, byOwner2, 0, varList, subArea, chartTitle, yLabelText)

        pdfFile.close()
        print "Done."

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 4:
        print "Usage: reporter_.py <subArea> <runName> <chartTitle>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

    except Exception, e:
        print "\n\n" + sys.argv[2] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
