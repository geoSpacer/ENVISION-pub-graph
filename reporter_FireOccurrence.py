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
    yLabelText = 'Percent of Area'
    PVTmngGrpArea = reporterFunc.getPVTHa(subArea)

    repList = list(set(pd.io.parsers.read_csv(outDir + r'FireOccurance_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_FireOccurrence.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot total area
        totalArea = pd.io.parsers.read_csv(outDir + r'FireOccurance_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]
        varList = [' Wildfire(ha)', ' SurfaceWildfire(ha)', ' MixedSeverityFire(ha)', ' StandReplacingFire(ha)']
        reporterFunc.plotReporter('', pdfFile, totalArea, sum(PVTmngGrpArea), varList, subArea, chartTitle, yLabelText)

        # plot potential disturbance by PVT management group
        for PVTgpNum in range(0,7):
            PVTgp = 'PMG' + str(PVTgpNum)

            varList = list(totalArea.columns.values)
            varList.remove('Scenario')
            varList.remove(' Run')
            varList.remove(' Year')
            varList.remove(' Version')
            varList.remove(' Timestamp')

            subVarList = []
            for varName in varList:
                if PVTgp in varName:
                    subVarList.append(varName)

            reporterFunc.plotReporter(PVTgp, pdfFile, totalArea, PVTmngGrpArea[PVTgpNum], subVarList, subArea, chartTitle, yLabelText)

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
