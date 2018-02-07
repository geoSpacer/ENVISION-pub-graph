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

def main(outDir, subArea, runList, chartTitle, ownership):
    varList = [' Stand Replacing FirePMG1', ' Stand Replacing FirePMG2', ' Stand Replacing FirePMG3', ' Stand Replacing FirePMG4', ' Stand Replacing FirePMG5']

    # list of ownerships to graphs
##    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
    # remove Tribal from owners to graph
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']

    reporterName = r'FireOccurance_by_OWNER_pivot.csv'
    reporterName2 = r'FireExperience_pivot.csv'
    ownerLabelField = ' OWNER_label'

    # set list of owners to graph
    if ownership == 'All':
        pdfFile = PdfPages(outDir + chartTitle + '_HS_Fire_extreme38.pdf')
    elif ownership in ownersToGraph:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + 'PMG345_HS_Fire_extreme38_NumDwellings1km' + ownersToGraph[0] + '.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_HS_Fire_extreme38_' + ownersToGraph[0] + '.pdf')
        ownerLabelField = ' OWNER_DETL_label'
        reporterName = r'FireOccurance_by_OWNER_DETL_pivot.csv'

    # load area stats by owner
    areaStats = pd.io.parsers.read_csv(outDir + runList[0] + "\\AreaStats_by_OWNER_pivot.csv")
    areaStats = areaStats[areaStats[' Year'] == 1]

    # sum total areas over selected ownerships
    for ownerToGraph in ownersToGraph:
        ownerStats = areaStats[areaStats[ownerLabelField] == ownerToGraph]
        if ownerToGraph == ownersToGraph[0]:
            PMG345Area = ownerStats[' PVT MNG GR 3 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 4 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 5 (ha)'].iloc[0]
            PMG12345Area = ownerStats[' PVT MNG GR 1 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 2 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 3 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 4 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 5 (ha)'].iloc[0]
            PMG1Area = ownerStats[' PVT MNG GR 1 (ha)'].iloc[0]
            PMG2Area = ownerStats[' PVT MNG GR 2 (ha)'].iloc[0]
        else:
            PMG345Area += ownerStats[' PVT MNG GR 3 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 4 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 5 (ha)'].iloc[0]
            PMG12345Area += ownerStats[' PVT MNG GR 1 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 2 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 3 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 4 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 5 (ha)'].iloc[0]
            PMG1Area += ownerStats[' PVT MNG GR 1 (ha)'].iloc[0]
            PMG2Area += ownerStats[' PVT MNG GR 2 (ha)'].iloc[0]

    for splot in [3]:
        # setup plot for all scenarios
        fig = pl.figure(1, figsize=(4,4))
        ax = fig.add_subplot(1,1,1)

        plotList = []
        for scenario in runList:
            inDir = outDir + scenario + "\\"
            print('Running scenario ' + scenario)

            if os.path.isdir(inDir):
                # find extreme set of fire years and copy to indexTable
                if scenario == runList[0]:
                    totalArea = pd.io.parsers.read_csv(inDir + reporterName)
                    yearList = list(set(totalArea[' Year']))
                    repList = list(set(totalArea[' Run']))

                    # get stats from multiple reps
                    statsList = []
                    for year in range(1,max(yearList) + 1):
                        yearArea = totalArea[totalArea[' Year'] == year]

                        for rep in repList:
                            repArea = yearArea[yearArea[' Run'] == rep]

                            # sum output over selected ownerships
                            for ownerToGraph in ownersToGraph:
                                if ownerToGraph == ownersToGraph[0]:
                                    ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == ownerToGraph])
                                else:
                                    tempArea = repArea[repArea[ownerLabelField] == ownerToGraph]
                                    for varName in varList:
            #                            totalArea.loc[list(ownerArea.index)[0],varName] += tempArea[varName].iloc[0]
                                        ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                                    ownerToGraph = 'All'

                            if splot == 1 or splot == 2:
                                dataDict = {'rep_num': rep, 'year_num': year, 'HS_ha': ownerArea[' Stand Replacing FirePMG1'].iloc[0] + ownerArea[' Stand Replacing FirePMG2'].iloc[0] + ownerArea[' Stand Replacing FirePMG3'].iloc[0] + ownerArea[' Stand Replacing FirePMG4'].iloc[0] + ownerArea[' Stand Replacing FirePMG5'].iloc[0]}
                            elif splot == 3 or splot == 4:
                                dataDict = {'rep_num': rep, 'year_num': year, 'HS_ha': ownerArea[' Stand Replacing FirePMG3'].iloc[0] + ownerArea[' Stand Replacing FirePMG4'].iloc[0] + ownerArea[' Stand Replacing FirePMG5'].iloc[0]}

                            # convert to list for DataFrame
                            statsList.append(dataDict)

                    # convert to DataFrame
                    dataTable = pd.DataFrame(statsList)
                    dataTable = dataTable.sort('HS_ha', ascending=False)
                    indexTable = dataTable.head(n=38)
                    indexTable.to_csv(outDir + scenario + "_extreme38_FF.csv", mode='w', header=True)

                totalArea = pd.io.parsers.read_csv(inDir + reporterName2)
                yearList = list(set(totalArea[' Year']))
                repList = list(set(totalArea[' Run']))

                # get stats from multiple reps
                statsList = []
                for year in range(1,max(yearList) + 1):
                    yearArea = totalArea[totalArea[' Year'] == year]

                    for rep in repList:
                        repArea = yearArea[yearArea[' Run'] == rep]
                        dataDict = {'rep_num': rep, 'year_num': year, 'NumDwellings1kmHS': repArea[' NumberDwellings1kmFromStandRep'].iloc[0]}

                        # convert to list for DataFrame
                        statsList.append(dataDict)

                # convert to DataFrame
                dataTable = pd.DataFrame(statsList)

                extremeList = []
                for event in range(len(indexTable)):
                    try:
                        extremeList.append(dataTable[(dataTable.rep_num == indexTable['rep_num'].iloc[event]) & (dataTable.year_num == indexTable['year_num'].iloc[event])]['NumDwellings1kmHS'].iloc[0])
                    except:
                        print('Error!! Missing ' + 'Year ' + str(plotYear) + ' rep ' + str(plotRep))

                plotList.append(sum(extremeList) / len(extremeList))

        yLabelText = 'Avg dwellings 1km from HS Fire in 38 extreme FF yrs'
        reporterFunc.plotReporter6_bar(fig, ax, '', pdfFile, plotList, runList, yLabelText)

        pl.subplots_adjust(left=0.14)
        pdfFile.savefig()
        pl.close()

    pdfFile.close()
    print "Done with PMG in HS fire extreme 38 Num Dwellings."

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
