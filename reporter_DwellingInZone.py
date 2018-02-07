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

def main(outDir, subArea, chartTitlePre):
    varList = [' Dwellings in Rural Residential', ' Dwellings in Resort District', ' Dwellings in Urban Reserve', ' Dwellings in Forest Use 1', ' Dwellings in EFU']
    yLabelText = 'Average Dwellings per Hectare'
    zoneHa = reporterFunc.getZoneHa(subArea)

    repList = list(set(pd.io.parsers.read_csv(outDir + r'DwellingsInZone_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_DwellingsInZone.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot landscape
        totalArea = pd.io.parsers.read_csv(outDir + r'DwellingsInZone_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        for varName in varList:
            totalArea[varName] = totalArea[varName] / zoneHa[varName]

        reporterFunc.plotReporter('', pdfFile, totalArea, 0, varList, subArea, chartTitle, yLabelText)

        # plot landscape in absolute numbers of dwellings
        totalArea = pd.io.parsers.read_csv(outDir + r'DwellingsInZone_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]
        yLabelText = 'Number of Dwellings'

        reporterFunc.plotReporter('', pdfFile, totalArea, 0, varList, subArea, chartTitle, yLabelText)

        pdfFile.close()
        print "Done."

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 4:
        print "Usage: reporter_.py <outDir> <subArea> <chartTitle>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

    except Exception, e:
        print "\n\n" + sys.argv[1] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
