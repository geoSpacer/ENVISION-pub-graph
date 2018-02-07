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
    # load area stats by owner
    areaStats = pd.io.parsers.read_csv(outDir + "AreaStats_by_OWNER_pivot.csv")
    areaStats = areaStats[(areaStats[' Year'] == 1) | (areaStats[' Year'] == 2007)]

    repList = list(set(pd.io.parsers.read_csv(outDir + r'ManagementDisturb_by_OWNER_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_ManagementDisturb.pdf')
        pdfFile2 = PdfPages(outDir + 'R' + str(repNum) + '_ManagementDisturb_SYU.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'ManagementDisturb_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            yLabelText = 'Hectares Treated'
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]

            varList = list(byOwner.columns.values)
            varList.remove('Scenario')
            varList.remove(' Run')
            varList.remove(' Year')
            varList.remove(' Version')
            varList.remove(' Timestamp')
            varList.remove(' OWNER_value')
            varList.remove(' OWNER_label')

            # create varList for SYU
            varList2 = []
            for varName in varList:
                if " SYU" in varName:
                    varList2.append(varName)

            for varName in varList2:
                    varList.remove(varName)

            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter(owner, pdfFile2, byOwner, 0, varList2, subArea, chartTitle, yLabelText)

            # Repeat graph with percent area
            yLabelText = 'Percent of Forested Area'
            reporterFunc.plotReporter(owner, pdfFile, byOwner, areaStats[areaStats[' OWNER_label'] == owner][' Forested (ha)'].iloc[0], varList, subArea, chartTitle, yLabelText)

        # plot by owner_detl
        totalArea = pd.io.parsers.read_csv(outDir + r'ManagementDisturb_by_OWNER_DETL_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_DETL_label']))
        ownerNames.sort()
        for owner in ownerNames:
            yLabelText = 'Hectares Treated'
            byOwner = totalArea[totalArea[' OWNER_DETL_label'] == owner]

            varList = list(byOwner.columns.values)
            varList.remove('Scenario')
            varList.remove(' Run')
            varList.remove(' Year')
            varList.remove(' Version')
            varList.remove(' Timestamp')
            varList.remove(' OWNER_DETL_value')
            varList.remove(' OWNER_DETL_label')

            # create varList for SYU
            varList2 = []
            for varName in varList:
                if " SYU" in varName:
                    varList2.append(varName)

            for varName in varList2:
                    varList.remove(varName)

            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter(owner, pdfFile2, byOwner, 0, varList2, subArea, chartTitle, yLabelText)

        pdfFile.close()
        pdfFile2.close()
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
