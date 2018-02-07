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

def main(subArea, runName, chartTitlePre, ownership):
    outDir = "C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_production\\"
#    varList = [' Resilient (ha) PMG345', ' Semi-Resilient (ha) PMG345', ' Low Resilience (ha) PMG345']
    varList = [' Resilient (ha) PMG345', ' Low Resilience (ha) PMG345']
    yLabelText = 'Area (%)'
    chartTitle = chartTitlePre
    PMG345Ha = reporterFunc.getPMG345Ha(subArea)
    forestedHa = reporterFunc.getOwnerForestedHa(subArea)
#    figTextList = ['High resilience','Moderate resilience','Low resilience']
    figTextList = ['High resilience','Low resilience']

    # list of ownerships to graphs
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
    reporterName = r'ForestStructure2_by_OWNER_pivot.csv'
    ownerLabelField = ' OWNER_label'

    if ownership == 'All':
        pdfFile = PdfPages(outDir + 'report4_Resilience_landscape.pdf')
    elif ownership in ownersToGraph:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + 'report4_Resilience_' + ownersToGraph[0] + '.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + 'report4_Resilience_' + ownersToGraph[0] + '.pdf')
        ownerLabelField = ' OWNER_DETL_label'
        reporterName = r'ForestStructure2_by_OWNER_DETL_pivot.csv'

    fig = pl.figure(1, figsize=(6.5,4))
    for varStruct in varList:
        # setup plot for all scenarios
        ax = fig.add_subplot(1,2,varList.index(varStruct) + 1)

        for scenario in ['CurrentPolicy','No_Treatment_Fed','Restoration','noFireNoTreatFed']:
            inDir = outDir + runName + "_" + scenario + "\\"

            if os.path.isdir(inDir):
                yearList = list(set(pd.io.parsers.read_csv(inDir + reporterName)[' Year']))
                repList = list(set(pd.io.parsers.read_csv(inDir + reporterName)[' Run']))
                totalArea = pd.io.parsers.read_csv(inDir + reporterName)

                # get stats from multiple reps
                statsList = []
                for year in range(1,max(yearList) + 1):
                    yearArea = totalArea[totalArea[' Year'] == year]

                    dataList = []
                    for rep in repList:
                        repArea = yearArea[yearArea[' Run'] == rep]

                        # sum output over selected ownerships
                        for ownerToGraph in ownersToGraph:
                            if ownerToGraph == ownersToGraph[0]:
                                ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == ownerToGraph])
                                fireProneArea345 = PMG345Ha[ownerToGraph]
                                fireProneArea = forestedHa[ownerToGraph]
                            else:
                                tempArea = repArea[repArea[ownerLabelField] == ownerToGraph]
                                for varName in varList:
        #                            totalArea.loc[list(ownerArea.index)[0],varName] += tempArea[varName].iloc[0]
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                                fireProneArea345 += PMG345Ha[ownerToGraph]
                                fireProneArea += forestedHa[ownerToGraph]
                                ownerToGraph = 'All'

                        if varStruct in [' Resilient (ha) PMG345', ' Semi-Resilient (ha) PMG345', ' Low Resilience (ha) PMG345']:
                            if fireProneArea345 > 0:
                                dataList.append(ownerArea[varStruct].iloc[0] / fireProneArea345 * 100)
                            else:
                                dataList.append(0.0)
                        else:
                            if fireProneArea > 0:
                                dataList.append(ownerArea[varStruct].iloc[0] / fireProneArea * 100)
                            else:
                                dataList.append(0.0)


                    # convert to numpy array
                    numpyList = np.array(dataList)
                    lower95th = np.mean(numpyList, axis=0) - ((1.96 * np.std(numpyList, axis=0)) / np.sqrt(len(repList)))
                    upper95th = np.mean(numpyList, axis=0) + ((1.96 * np.std(numpyList, axis=0)) / np.sqrt(len(repList)))

                    if lower95th < 0:
                        lower95th = 0.0

                    # add year data to dictionary
                    dataDict = {'timeStep': year, 'mean': np.mean(numpyList, axis=0), 'std': np.std(numpyList, axis=0), 'lower': lower95th, 'upper': upper95th}

                    # convert to list for DataFrame
                    statsList.append(dataDict)

                # convert to DataFrame
                dataTable = pd.DataFrame(statsList)

                plotLegend = (-99,-99)
                if varStruct == ' Pole and Small (ha) Forest' or varStruct == ' Low Resilience (ha) PMG345':
                    plotLegend = (0.99,0.25)

                if varList.index(varStruct) >= (len(varList) - 3):
                    labelXtick = True
                else:
                    labelXtick = False

                if varList.index(varStruct) == 0:
                    labelYtick = True
                else:
                    labelYtick = False

                xLabelText = yLabelText = ''
                reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean','lower','upper'], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, figTextList[varList.index(varStruct)])

    reporterFunc.plotFigureText(fig, 'Simulation Year', 'Area (%)')

    pl.savefig(outDir + 'report4_Resilience_landscape.png', bbox_inches='tight', dpi=300)
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
