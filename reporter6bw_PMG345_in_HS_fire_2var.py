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
import os.path

def main(outDir, subArea, runList, chartTitlePre, ownership):
    varList = [' Stand Replacing FirePMG3', ' Stand Replacing FirePMG4', ' Stand Replacing FirePMG5']
    chartTitle = chartTitlePre
    PMG345Ha = reporterFunc.getPMG345Ha(subArea)

    # list of ownerships to graphs
    if ownership == 'All':
        ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
        pdfFile = PdfPages(outDir + 'report6bw_PMG345_in_HS_Fire_All.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + 'report6bw_PMG345_in_HS_Fire_' + ownersToGraph[0] + '.pdf')

    # Current Policy run required!
    for scenario in ['Restoration','CurrentPolicy']:
        inDir = outDir + scenario + "\\"

        if scenario == 'Restoration':
            yearList = list(set(pd.io.parsers.read_csv(inDir + r'FireOccurance_by_OWNER_pivot.csv')[' Year']))
            repList = list(set(pd.io.parsers.read_csv(inDir + r'FireOccurance_by_OWNER_pivot.csv')[' Run']))

        totalArea = pd.io.parsers.read_csv(inDir + r'FireOccurance_by_OWNER_pivot.csv')
        dataTable = pd.DataFrame(totalArea[totalArea[' Year'] > 0])
        dataTable['key'] = dataTable[' OWNER_label'] + '_' + dataTable[' Run'].astype(str) + '_' + dataTable[' Year'].astype(str)

        if scenario == 'Restoration':
            scenarioTable = dataTable
        else:
            scenarioTable = pd.merge(scenarioTable, dataTable, how='left', on='key')

    # sum over owners
    scenarioTable.index = scenarioTable['key']
    fireProneArea = PMG345Ha[ownersToGraph[0]]
    if ownership == 'All':
        for rep in range(len(repList)):
            for year in range(1, len(yearList)):
                for owner in ownersToGraph:
                    key = owner + '_' + str(rep) + '_' + str(year)
                    print(key)
                    if owner != ownersToGraph[0]:
                        for varName in varList:
                            scenarioTable.loc[ownersToGraph[0] + '_' + str(rep) + '_' + str(year),varName + '_x'] += scenarioTable.loc[key,varName + '_x']
                            scenarioTable.loc[ownersToGraph[0] + '_' + str(rep) + '_' + str(year),varName + '_y'] += scenarioTable.loc[key,varName + '_y']

        for owner in ownersToGraph:
            fireProneArea += PMG345Ha[owner]

    ownerArea = pd.DataFrame(scenarioTable[scenarioTable[' OWNER_label_y'] == ownersToGraph[0]])

    # calculate percent of PMG345 area for each row
    ownerArea['CP_HS_pct'] = (ownerArea[varList[0] + '_y'] + ownerArea[varList[1] + '_y'] + ownerArea[varList[2] + '_y']) / fireProneArea * 100
    ownerArea['Res_HS_pct'] = (ownerArea[varList[0] + '_x'] + ownerArea[varList[1] + '_x'] + ownerArea[varList[2] + '_x']) / fireProneArea * 100

    #Sort dataTable on percent PMG345 in HS fire
    dataTable = ownerArea.sort('CP_HS_pct', ascending=False)

    for splot in [1, 2]:
        # setup plot for all scenarios
        fig = pl.figure(1, figsize=(4,4))
        ax = fig.add_subplot(1,1,1)

        # label plots and set percent of top values
        if splot == 1:
            yLabelText = 'Area of high severity fire in fire-frequent landscape (%)'
            labelXaxis = True
            figText = 'a'
            topPercent = 1.0
        elif splot == 2:
            yLabelText = 'Area of top 10% stand-replacing fires in fire-frequent landscape (%)'
            labelXaxis = True
            figText = 'b'
            topPercent = 0.1

        statsList1 = []
        statsList3 = []

        valueSet = []
        maxValueSet = []

        for i in range(int(round(len(dataTable) * topPercent))):
            statsList1.append(dataTable['CP_HS_pct'].iloc[i])
            statsList3.append(dataTable['Res_HS_pct'].iloc[i])

        valueSet.append(statsList1)
        valueSet.append(statsList3)

        maxValueSet.append(max(statsList1))
        maxValueSet.append(max(statsList3))

        labelList = ['Current\nManagement','Accelerated\nRestoration']
        print yLabelText
        print 'median for Current Management ' + str(np.median(valueSet[0]))
        print 'median for Restoration ' + str(np.median(valueSet[1]))
        print

        reporterFunc.plotReporter4bw(fig, ax, ownership, pdfFile, valueSet, labelList, subArea, chartTitle, yLabelText, maxValueSet, labelXaxis, figText)


##    yLabelText = 'Area of high-severity fire (%)'
##    reporterFunc.plotFigureText(fig, '', yLabelText)
##
   ## pl.savefig(outDir + 'report4bw_PMG345_in_HS_Fire_All.png', bbox_inches='tight', dpi=300)
        pdfFile.savefig()
        pl.close()
    pdfFile.close()
    print "Done."

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 6:
        print "Usage: reporter_.py <outDir> <subArea> <runList> <chartTitle> <ownership>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    except Exception, e:
        print "\n\n" + sys.argv[1] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
