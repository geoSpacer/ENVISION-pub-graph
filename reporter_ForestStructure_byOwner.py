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

    repList = list(set(pd.io.parsers.read_csv(outDir + r'ForestStructure_by_OWNER_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_ForestStructure_byOwner.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot total area
        totalArea = pd.io.parsers.read_csv(outDir + r'ForestStructure_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            yLabelText = 'Hectares'
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]

            varList = list(byOwner.columns.values)
            varList.remove('Scenario')
            varList.remove(' Run')
            varList.remove(' Year')
            varList.remove(' Version')
            varList.remove(' Timestamp')
            varList.remove(' OWNER_value')

            subVarList = []
            for varName in varList:
                if 'All' in varName:
                    subVarList.append(varName)

            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, subVarList, subArea, chartTitle, yLabelText)

            # plot percent of forested area
            yLabelText = 'Percent of Forested Area'
            reporterFunc.plotReporter(owner, pdfFile, byOwner, areaStats[areaStats[' OWNER_label'] == owner][' Forested (ha)'].iloc[0], subVarList, subArea, chartTitle, yLabelText)

            # plot fire occurrence by PVT management group
            yLabelText = 'Hectares'
            for PVTgpNum in range(1,7):
                PVTgp = 'PMG' + str(PVTgpNum)

                varList = list(byOwner.columns.values)
                varList.remove('Scenario')
                varList.remove(' Run')
                varList.remove(' Year')
                varList.remove(' Version')
                varList.remove(' Timestamp')
                varList.remove(' OWNER_value')

                subVarList = []
                for varName in varList:
                    if PVTgp in varName:
                        subVarList.append(varName)

                reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, subVarList, subArea, chartTitle, yLabelText)

        pdfFile.close()

        # Print out forest structure 2 file
        varList = [' Early Successional (ha) Forest', ' Pole and Small (ha) Forest', ' Medium (ha) Forest', ' Large and Giant (ha) Forest',' Open Canopy (ha) Sm+ Forest',' Closed Canopy (ha) Sm+ Forest']
        yLabelText = 'Hectares'
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_ForestStructure2_byOwner.pdf')

        # plot total area
        totalArea = pd.io.parsers.read_csv(outDir + r'ForestStructure2_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        reporterFunc.plotReporter('', pdfFile, totalArea, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'ForestStructure2_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner detl
        totalArea = pd.io.parsers.read_csv(outDir + r'ForestStructure2_by_OWNER_DETL_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_DETL_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_DETL_label'] == owner]
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

        pdfFile.close()

        # Print out forest structure 3 file
        varList = [' Open Canopy (ha) Forest', ' Moderate Canopy (ha) Forest', ' Closed Canopy (ha) Forest', ' Post-disturb Canopy (ha) Forest',' No Layers (ha) Forest',' Single-story (ha) Forest', ' Multi-story (ha) Forest']
        yLabelText = 'Hectares'
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_ForestStructure3_byOwner.pdf')

        # plot total area
        totalArea = pd.io.parsers.read_csv(outDir + r'ForestStructure3_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        reporterFunc.plotReporter('', pdfFile, totalArea, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'ForestStructure3_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner detl
        totalArea = pd.io.parsers.read_csv(outDir + r'ForestStructure3_by_OWNER_DETL_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_DETL_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_DETL_label'] == owner]
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

        pdfFile.close()

        # Print out forest structure 3 PMG345 file
        varList = [' Open Canopy (ha) PMG345', ' Moderate Canopy (ha) PMG345', ' Closed Canopy (ha) PMG345', ' Post-disturb Canopy (ha) PMG345',' No Layers (ha) PMG345',' Single-story (ha) PMG345', ' Multi-story (ha) PMG345']
        yLabelText = 'Hectares'
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_ForestStructure3_PMG345_byOwner.pdf')

        # plot total area
        totalArea = pd.io.parsers.read_csv(outDir + r'ForestStructure3_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        reporterFunc.plotReporter('', pdfFile, totalArea, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'ForestStructure3_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner detl
        totalArea = pd.io.parsers.read_csv(outDir + r'ForestStructure3_by_OWNER_DETL_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_DETL_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_DETL_label'] == owner]
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

        pdfFile.close()

        print "Done with ForestStructure by Owner"

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
