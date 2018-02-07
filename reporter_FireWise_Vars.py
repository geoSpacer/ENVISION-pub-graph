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
    repList = list(set(pd.io.parsers.read_csv(outDir + r'FireWiseVars_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_FireWiseVars.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot percent firewise
        ylabelText = 'Number of Dwellings'
        varList = [' DwellingsWithFIRE_500M_5y', ' DwellingsWithFIRE_10KM_5y', ' DwellingsWithPSFIRE_10KM_5y', ' DwellingsWithPRFIRE_2KM_5y']
        totalArea = pd.io.parsers.read_csv(outDir + r'FireWiseVars_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        reporterFunc.plotReporter('', pdfFile, totalArea, 0, varList, subArea, chartTitle, ylabelText)

        # plot average flame length
        varList = [' AvgPotentialFL_1km']
        yLabelText = 'Average Potential flame length (m) within 1km of IDU'
        reporterFunc.plotReporter('', pdfFile, totalArea, 0, varList, subArea, chartTitle, yLabelText)

        # plot average flame length
        varList = [' AvgTPH_500m']
        yLabelText = 'Average Trees per Ha within 500m of IDU'
        reporterFunc.plotReporter('', pdfFile, totalArea, 0, varList, subArea, chartTitle, yLabelText)

        # plot firewise vars by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'FireWiseVars_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]

            ylabelText = 'Number of Dwellings'
            varList = [' DwellingsWithFIRE_500M_5y', ' DwellingsWithFIRE_10KM_5y', ' DwellingsWithPSFIRE_10KM_5y', ' DwellingsWithPRFIRE_2KM_5y']
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, ylabelText)

            # plot average flame length
            varList = [' AvgPotentialFL_1km']
            yLabelText = 'Average Potential flame length (m) within 1km of IDU'
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

            # plot average flame length
            varList = [' AvgTPH_500m']
            yLabelText = 'Average Trees per Ha within 500m of IDU'
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

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
