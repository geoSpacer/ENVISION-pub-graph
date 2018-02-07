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
    yLabelText = 'Carbon (Mg C)'

    repList = list(set(pd.io.parsers.read_csv(outDir + r'Carbon_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_Carbon_compare.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot landscape
        totalArea = pd.io.parsers.read_csv(outDir + r'Carbon_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]
        totalArea2 = pd.io.parsers.read_csv("C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_production\\North_20150923_CurrentPolicy\\" + r'Carbon_pivot.csv')
        totalArea2 = totalArea2[totalArea2[' Run'] == repNum]

        varList = list(totalArea.columns.values)
        varList.remove('Scenario')
        varList.remove(' Run')
        varList.remove(' Year')
        varList.remove(' Version')
        varList.remove(' Timestamp')
    #    varList.remove(' OWNER_value')
    #    varList.remove(' OWNER_label')

        reporterFunc.plotReporter_compare('', pdfFile, totalArea, totalArea2, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'Carbon_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]
        totalArea2 = pd.io.parsers.read_csv("C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_production\\North_20150923_CurrentPolicy\\" + r'Carbon_by_OWNER_pivot.csv')
        totalArea2 = totalArea2[totalArea2[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            byOwner2 = totalArea2[totalArea2[' OWNER_label'] == owner]

            varList = list(byOwner.columns.values)
            varList.remove('Scenario')
            varList.remove(' Run')
            varList.remove(' Year')
            varList.remove(' Version')
            varList.remove(' Timestamp')
            varList.remove(' OWNER_value')
            varList.remove(' OWNER_label')

            reporterFunc.plotReporter_compare(owner, pdfFile, byOwner, byOwner2, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner detl
        totalArea = pd.io.parsers.read_csv(outDir + r'carbon_by_OWNER_DETL_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]
        totalArea2 = pd.io.parsers.read_csv("C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_production\\North_20150923_CurrentPolicy\\" + r'carbon_by_OWNER_DETL_pivot.csv')
        totalArea2 = totalArea2[totalArea2[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_DETL_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_DETL_label'] == owner]
            byOwner2 = totalArea2[totalArea2[' OWNER_DETL_label'] == owner]

            varList = list(byOwner.columns.values)
            varList.remove('Scenario')
            varList.remove(' Run')
            varList.remove(' Year')
            varList.remove(' Version')
            varList.remove(' Timestamp')
            varList.remove(' OWNER_DETL_value')
            varList.remove(' OWNER_DETL_label')

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
