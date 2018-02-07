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
    varList = [' NumberOfNewDwellings']
    yLabelText = 'Number of New Dwellings'

    repList = list(set(pd.io.parsers.read_csv(outDir + r'DwellingsInWUI_by_WUI_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_Dwellings.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot by wui
        totalArea = pd.io.parsers.read_csv(outDir + r'DwellingsInWUI_by_WUI_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        byWUITable = pd.DataFrame()
        for wui in set(totalArea[' WUI_label']):
            byWUI = totalArea[totalArea[' WUI_label'] == wui]
            byWUI = byWUI.drop(byWUI.index[:1])
            if len(byWUITable) == 0:
                byWUITable = byWUI
            else:
                byWUI = byWUI.set_index(' Year')
                byWUI = byWUI.drop('Scenario', 1)
                byWUI = byWUI.drop(' Run', 1)
                byWUI = byWUI.drop(' Version', 1)
                byWUI = byWUI.drop(' Timestamp', 1)
                byWUI = byWUI.drop(' WUI_value', 1)
                byWUI = byWUI.drop(' WUI_label', 1)
                byWUITable = byWUITable.join(byWUI, ' Year', 'left')

            byWUITable = byWUITable.rename(columns={varList[0] : wui})

        reporterFunc.plotReporter('', pdfFile, byWUITable, 0, set(totalArea[' WUI_label']), subArea, chartTitle, yLabelText)

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
