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
#    ownerHaForested = reporterFunc.getOwnerForestedHa(subArea)

    repList = list(set(pd.io.parsers.read_csv(outDir + r'PST_NSO_fire_severity_by_OWNER_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_PST_NSO_HSfire_Federal.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'PST_NSO_fire_severity_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ['Federal']:
            yLabelText = 'Hectares'
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]

            varList = list(byOwner.columns.values)
            varList.remove('Scenario')
            varList.remove(' Run')
            varList.remove(' Year')
            varList.remove(' Version')
            varList.remove(' Timestamp')
            varList.remove(' OWNER_value')
            varList.remove(' OWNER_label')

            varList1 = []
            varList2 = []
            for var in varList:
                if 'fire' in var:
                    varList1.append(var)
                else:
                    varList2.append(var)

            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList1, subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList2, subArea, chartTitle, yLabelText)

            # Repeat graph with percent area
#            yLabelText = 'Percent of Forested Area'
#            reporterFunc.plotReporter(owner, pdfFile, byOwner, ownerHaForested[owner], varList, subArea, chartTitle, yLabelText)

        # plot by owner_detl
        totalArea = pd.io.parsers.read_csv(outDir + r'nonPST_NSO_fire_severity_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ['Federal']:
            yLabelText = 'Hectares'
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]

            varList = list(byOwner.columns.values)
            varList.remove('Scenario')
            varList.remove(' Run')
            varList.remove(' Year')
            varList.remove(' Version')
            varList.remove(' Timestamp')
            varList.remove(' OWNER_value')
            varList.remove(' OWNER_label')

            varList1 = []
            varList2 = []
            for var in varList:
                if 'fire' in var:
                    varList1.append(var)
                else:
                    varList2.append(var)

            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList1, subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList2, subArea, chartTitle, yLabelText)

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
