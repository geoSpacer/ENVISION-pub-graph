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
    yLabelText = 'Percent of PMG 3, 4, and 5 in Stand Replacing Fire (top 10%)'
    chartTitle = chartTitlePre
    PMG345Ha = reporterFunc.getPMG345Ha(subArea)

    # list of ownerships to graphs
    if ownership == 'All':
        ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
        pdfFile = PdfPages(outDir + 'report3_PMG345_in_HS_Fire_top10pct_All.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + 'report3_PMG345_in_HS_Fire_top10pct_' + ownersToGraph[0] + '.pdf')

    # setup plot for all scenarios
    fig = pl.figure(1, figsize=(11,8.5))
    ax = fig.add_subplot(1,1,1)

    for scenario in ['CurrentPolicy','NoFedTreat','Restoration']:
        inDir = outDir + runName + "_" + scenario + "\\"

        yearList = list(set(pd.io.parsers.read_csv(inDir + r'FireOccurance_by_OWNER_pivot.csv')[' Year']))
        repList = list(set(pd.io.parsers.read_csv(inDir + r'FireOccurance_by_OWNER_pivot.csv')[' Run']))
        totalArea = pd.io.parsers.read_csv(inDir + r'FireOccurance_by_OWNER_pivot.csv')
        dataTable = pd.DataFrame(totalArea[totalArea[' Year'] > 0])
        dataTable['key'] = dataTable[' OWNER_label'] + '_' + dataTable[' Run'].astype(str) + '_' + dataTable[' Year'].astype(str)

        if scenario == 'CurrentPolicy':
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
                            scenarioTable.loc[ownersToGraph[0] + '_' + str(rep) + '_' + str(year),varName] += scenarioTable.loc[key,varName]
                            scenarioTable.loc[ownersToGraph[0] + '_' + str(rep) + '_' + str(year),varName + '_x'] += scenarioTable.loc[key,varName + '_x']
                            scenarioTable.loc[ownersToGraph[0] + '_' + str(rep) + '_' + str(year),varName + '_y'] += scenarioTable.loc[key,varName + '_y']

        for owner in ownersToGraph:
            fireProneArea += PMG345Ha[owner]

    ownerArea = pd.DataFrame(scenarioTable[scenarioTable[' OWNER_label'] == ownersToGraph[0]])

    # calculate percent of PMG345 area for each row
    ownerArea['CP_HS_pct'] = (ownerArea[varList[0] + '_x'] + ownerArea[varList[1] + '_x'] + ownerArea[varList[2] + '_x']) / fireProneArea * 100
    ownerArea['NFT_HS_pct'] = (ownerArea[varList[0] + '_y'] + ownerArea[varList[1] + '_y'] + ownerArea[varList[2] + '_y']) / fireProneArea * 100
    ownerArea['Res_HS_pct'] = (ownerArea[varList[0]] + ownerArea[varList[1]] + ownerArea[varList[2]]) / fireProneArea * 100

    #Sort dataTable on percent PMG345 in HS fire
    dataTable = ownerArea.sort('NFT_HS_pct', ascending=False)

    statsList1 = []
    statsList2 = []
    statsList3 = []

    valueSet = []
    maxValueSet = []

    for i in range(int(round(len(dataTable) * 0.1))):
        statsList1.append(dataTable['CP_HS_pct'].iloc[i])
        statsList2.append(dataTable['NFT_HS_pct'].iloc[i])
        statsList3.append(dataTable['Res_HS_pct'].iloc[i])

    valueSet.append(statsList1)
    valueSet.append(statsList2)
    valueSet.append(statsList3)

    maxValueSet.append(max(statsList1))
    maxValueSet.append(max(statsList2))
    maxValueSet.append(max(statsList3))

    labelList = ['Current Policy','No Fed Treatment','Restoration']
    reporterFunc.plotReporter3(fig, ax, ownership + ' - ' + str(len(repList)) + ' reps', pdfFile, valueSet, labelList, subArea, chartTitle, yLabelText, scenario, maxValueSet)


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
