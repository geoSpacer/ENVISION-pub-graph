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
    varList = [' Total Merch Harvest (m3)']
    yLabelText = 'Merchantable Volume Harvested (m3)'
    chartTitle = chartTitlePre
    PMG345Ha = reporterFunc.getPMG345Ha(subArea)

    # list of ownerships to graphs
    if ownership == 'All':
        ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
        pdfFile = PdfPages(outDir + 'report2_Merch_Volume_All.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + 'report2_Merch_Volume_' + ownersToGraph[0] + '.pdf')

    # setup plot for all scenarios
    fig = pl.figure(1, figsize=(11,8.5))
    ax = fig.add_subplot(1,1,1)

    for scenario in ['CurrentPolicy','NoFedTreat','Restoration','NoFireNoMgmt']:
        inDir = outDir + runName + "_" + scenario + "\\"

        if os.path.isdir(inDir):
            yearList = list(set(pd.io.parsers.read_csv(inDir + r'WoodProducts_by_OWNER_pivot.csv')[' Year']))
            repList = list(set(pd.io.parsers.read_csv(inDir + r'WoodProducts_by_OWNER_pivot.csv')[' Run']))
            totalArea = pd.io.parsers.read_csv(inDir + r'WoodProducts_by_OWNER_pivot.csv')

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
                        else:
                            tempArea = repArea[repArea[' OWNER_label'] == ownerToGraph]
                            for varName in varList:
    #                            totalArea.loc[list(ownerArea.index)[0],varName] += tempArea[varName].iloc[0]
                                ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                            fireProneArea += PMG345Ha[ownerToGraph]
                            ownerToGraph = 'All'

                    dataList.append(ownerArea[varList[0]].iloc[0])

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

            reporterFunc.plotReporter2(fig, ax, ownerToGraph + ' - ' + str(len(repList)) + ' reps', pdfFile, dataTable, ['mean','lower','upper'], subArea, chartTitle, yLabelText, scenario)


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
