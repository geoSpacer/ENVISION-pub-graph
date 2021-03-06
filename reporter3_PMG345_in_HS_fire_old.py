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
import numpy as np
import reporterFunc
import pylab as pl

def main(subArea, runName, chartTitlePre, ownership):
    outDir = "C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_production\\"
    varList = [' Stand Replacing FirePMG3', ' Stand Replacing FirePMG4', ' Stand Replacing FirePMG5']
    yLabelText = 'Percent of PMG 3, 4, and 5 in Stand Replacing Fire'
    chartTitle = chartTitlePre
    PMG345Ha = reporterFunc.getPMG345Ha(subArea)

    # list of ownerships to graphs
    if ownership == 'All':
        ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
        pdfFile = PdfPages(outDir + 'report3_PMG345_in_HS_Fire_All.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + 'report3_PMG345_in_HS_Fire_' + ownersToGraph[0] + '.pdf')

    # setup plot for all scenarios
    fig = pl.figure(1, figsize=(11,8.5))
    ax = fig.add_subplot(1,1,1)

    valueSet1 = []
    valueSet2 = []
    maxValueSet1 = []
    maxValueSet2 = []
    for scenario in ['CurrentPolicy','NoFedTreat','Restoration']:
        inDir = outDir + runName + "_" + scenario + "\\"

        yearList = list(set(pd.io.parsers.read_csv(inDir + r'FireOccurance_by_OWNER_pivot.csv')[' Year']))
        repList = list(set(pd.io.parsers.read_csv(inDir + r'FireOccurance_by_OWNER_pivot.csv')[' Run']))
        totalArea = pd.io.parsers.read_csv(inDir + r'FireOccurance_by_OWNER_pivot.csv')

        # get stats from multiple reps
        statsList1 = []
        statsList2 = []
        for year in range(1,max(yearList) + 1):
            yearArea = totalArea[totalArea[' Year'] == year]

            dataList = []
            for rep in repList:
                repArea = yearArea[yearArea[' Run'] == rep]

                # sum output over selected ownerships
                for ownerToGraph in ownersToGraph:
                    if ownerToGraph == ownersToGraph[0]:
                        ownerArea = pd.DataFrame(repArea[repArea[' OWNER_label'] == ownerToGraph])
                        fireProneArea = PMG345Ha[ownerToGraph]
                    else:
                        tempArea = repArea[repArea[' OWNER_label'] == ownerToGraph]
                        for varName in varList:
#                            totalArea.loc[list(ownerArea.index)[0],varName] += tempArea[varName].iloc[0]
                            ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]


                        fireProneArea += PMG345Ha[ownerToGraph]
                        ownerToGraph = 'All'

                if fireProneArea > 0:
                    dataList.append((ownerArea[varList[0]].iloc[0] + ownerArea[varList[1]].iloc[0] + ownerArea[varList[2]].iloc[0]) / fireProneArea * 100)
                else:
                    dataList.append(0.0)

            # add year data to dictionary
            if year < 25:
                statsList1 += dataList
            else:
                statsList2 += dataList

        valueSet1.append(statsList1)
        valueSet2.append(statsList2)
        maxValueSet1.append(max(statsList1))
        maxValueSet2.append(max(statsList2))

    labelList = ['CP 0-24', 'NFT 0-24', 'Res 0-24', 'CP 25-50', 'NFT 25-50', 'Res 25-50']
    reporterFunc.plotReporter3(fig, ax, ownerToGraph + ' - ' + str(len(repList)) + ' reps', pdfFile, valueSet1 + valueSet2, labelList, subArea, chartTitle, yLabelText, scenario, maxValueSet1 + maxValueSet2)


    pdfFile.savefig()
    pl.close()
    pdfFile.close()
    print "Done."

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 5:
        print "Usage: reporter_.py <subArea> <runName> <chartTitle> <ownership>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    except Exception, e:
        print "\n\n" + sys.argv[2] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
