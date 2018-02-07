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
    varList = [' Potential HighSev Fire (ha) PMG1', ' Potential HighSev Fire (ha) PMG2', ' Potential HighSev Fire (ha) PMG3', ' Potential HighSev Fire (ha) PMG4', ' Potential HighSev Fire (ha) PMG5']
    PMG345Ha = reporterFunc.getPMG345Ha(subArea)
    PMG12345Ha = reporterFunc.getPMG12345Ha(subArea)

    # list of ownerships to graphs
    if ownership == 'All':
        ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
        pdfFile = PdfPages(outDir + chartTitle + '_Potential_HS_Fire_Landscape_PMG345.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_Potential_HS_Fire_' + ownersToGraph[0] + '.pdf')

    # setup plot for all scenarios
    fig = pl.figure(1, figsize=(4,4))

    for splot in [2]:
        ax = fig.add_subplot(1,1,1)
        for scenario in runList:
            inDir = outDir + scenario + "\\"

            if os.path.isdir(inDir):
                yearList = list(set(pd.io.parsers.read_csv(inDir + r'PotentialDisturbance_by_OWNER_pivot.csv')[' Year']))
                repList = list(set(pd.io.parsers.read_csv(inDir + r'PotentialDisturbance_by_OWNER_pivot.csv')[' Run']))
                totalArea = pd.io.parsers.read_csv(inDir + r'PotentialDisturbance_by_OWNER_pivot.csv')

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
                                ownerArea = pd.DataFrame(repArea[repArea[' OWNER_label'] == ownerToGraph])
                                fireProneArea = PMG345Ha[ownerToGraph]
                                forestedArea = PMG12345Ha[ownerToGraph]
                            else:
                                tempArea = repArea[repArea[' OWNER_label'] == ownerToGraph]
                                for varName in varList:
        #                            totalArea.loc[list(ownerArea.index)[0],varName] += tempArea[varName].iloc[0]
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]


                                fireProneArea += PMG345Ha[ownerToGraph]
                                forestedArea += PMG12345Ha[ownerToGraph]
                                ownerToGraph = 'All'

                        if splot == 1:
                            if forestedArea > 0:
                                dataList.append((ownerArea[' Potential HighSev Fire (ha) PMG1'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG2'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG3'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG4'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG5'].iloc[0]) / forestedArea * 100)
                            else:
                                dataList.append(0.0)
                        elif splot == 2:
                            if fireProneArea > 0:
                                dataList.append((ownerArea[' Potential HighSev Fire (ha) PMG3'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG4'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG5'].iloc[0]) / fireProneArea * 100)
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

                labelXtick = True
                labelYtick = True
                plotLegend = (0.6,0.99)
                xLabelText = 'Simulation Year'

                if splot == 1:
                    yLabelText = 'Area of high-severity fire hazard (%)'
                elif splot == 2:
                    yLabelText = 'Area of fire prone landscape in high-severity hazard (%)'

                reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean','lower','upper'], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, '')


    pl.savefig(outDir + 'report4_Potential_HS_Fire_Landscape.png', bbox_inches='tight', dpi=300)
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
