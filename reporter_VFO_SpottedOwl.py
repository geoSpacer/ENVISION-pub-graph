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
    yLabelText = 'Hectares'

    repList = list(set(pd.io.parsers.read_csv(outDir + r'VFO_Spotted_Owl_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_VFO_SpottedOwl.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot total area
        totalArea = pd.io.parsers.read_csv(outDir + r'VFO_Spotted_Owl_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        varList = list(totalArea.columns.values)
        varList.remove('Scenario')
        varList.remove(' Run')
        varList.remove(' Year')
        varList.remove(' Version')
        varList.remove(' Timestamp')

        reporterFunc.plotReporter('VFO Spotted Owl', pdfFile, totalArea, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'VFO_Spotted_Owl_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            reporterFunc.plotReporter('VFO Spotted Owl - ' + owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

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
