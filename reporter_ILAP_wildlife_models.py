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
    speciesList = ['Goshawk', 'Pileated', 'Sapsucker', 'Owl', 'Bluebird', 'White-headed', 'Marten', 'Black-backed']

    repList = list(set(pd.io.parsers.read_csv(outDir + r'ILAP_wildlife_models_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_ILAP_wildlife_models.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot total area
        totalArea = pd.io.parsers.read_csv(outDir + r'ILAP_wildlife_models_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]
        varList = list(totalArea.columns.values)

        for species in speciesList:
            subVarList = []
            for varName in varList:
                if species in varName:
                    subVarList.append(varName)

            reporterFunc.plotReporter('iLAP ' + species, pdfFile, totalArea, 0, subVarList, subArea, chartTitle, yLabelText)

            # plot by owner
            totalAreaOwner = pd.io.parsers.read_csv(outDir + r'ILAP_wildlife_models_by_OWNER_pivot.csv')
            totalAreaOwner = totalAreaOwner[totalAreaOwner[' Run'] == repNum]

            ownerNames = list(set(totalAreaOwner[' OWNER_label']))
            ownerNames.sort()
            for owner in ownerNames:
                byOwner = totalAreaOwner[totalAreaOwner[' OWNER_label'] == owner]
                reporterFunc.plotReporter('iLAP - ' + species + ' - ' + owner, pdfFile, byOwner, 0, subVarList, subArea, chartTitle, yLabelText)

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
