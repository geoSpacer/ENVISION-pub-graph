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
#    varList = [' Total Merch Harvest (m3)', ' Total Carbon (live+dead) (Mg)']
    varList = [' Total Carbon (live+dead) (Mg)']

    # list of ownerships to graphs
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']
    reporterNameWood = r'WoodProducts_by_OWNER_pivot.csv'
    reporterNameVol = r'Carbon_by_OWNER_pivot.csv'
    ownerLabelField = ' OWNER_label'

    if ownership == 'All':
        pdfFile = PdfPages(outDir + chartTitle + '_Carbon_landscape.pdf')
    elif ownership in ownersToGraph:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_Carbon_' + ownersToGraph[0] + '.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_Carbon_' + ownersToGraph[0] + '.pdf')
        ownerLabelField = ' OWNER_DETL_label'
        reporterNameWood = r'WoodProducts_by_OWNER_DETL_pivot.csv'
        reporterNameVol = r'Carbon_by_OWNER_DETL_pivot.csv'

    fig = pl.figure(1, figsize=(4,4))
    for varStruct in varList:
        # setup plot for all scenarios
        ax = fig.add_subplot(1,1,varList.index(varStruct) + 1)

        for scenario in runList:
            inDir = outDir + scenario + "\\"

            if os.path.isdir(inDir):
                if varStruct == ' Total Merch Harvest (m3)':
                    totalArea = pd.io.parsers.read_csv(inDir + reporterNameWood)
                    figText = 'A'
                elif varStruct == ' Total Carbon (live+dead) (Mg)':
                    totalArea = pd.io.parsers.read_csv(inDir + reporterNameVol)
                    figText = ''

                yearList = list(set(totalArea[' Year']))
                repList = list(set(totalArea[' Run']))

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
                            else:
                                tempArea = repArea[repArea[ownerLabelField] == ownerToGraph]
#                                for varName in varList:
        #                            totalArea.loc[list(ownerArea.index)[0],varName] += tempArea[varName].iloc[0]
                                ownerArea[varStruct].iloc[0] += tempArea[varStruct].iloc[0]

                                ownerToGraph = 'All'

                        dataList.append(ownerArea[varStruct].iloc[0])

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

                labelYtick = True
                if varStruct == ' Total Merch Harvest (m3)':
                    yLabelText = 'Merchantable volume ( $\mathregular{1x10^3}$ $\mathregular{m^3}$)'
                    dataTable['mean'] = dataTable['mean'] / 1000
                    dataTable['lower'] = dataTable['lower'] / 1000
                    dataTable['upper'] = dataTable['upper'] / 1000
                    labelXtick = False
                    xLabelText = ''
                    plotLegend = (0.5,0.99)
                elif varStruct == ' Total Carbon (live+dead) (Mg)':
                    yLabelText = 'Aboveground carbon ( $\mathregular{1x10^6}$ Mg )'
                    dataTable['mean'] = dataTable['mean'] / 1000000
                    dataTable['lower'] = dataTable['lower'] / 1000000
                    dataTable['upper'] = dataTable['upper'] / 1000000
                    labelXtick = True
                    xLabelText = 'Simulation Year'
                    plotLegend = (0.5,0.99)

                mnAxis, mxAxis = reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean','lower','upper'], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, figText)


#    pl.savefig(outDir + 'report4_Vol_Carbon_landscape.png', bbox_inches='tight', dpi=300)
    pdfFile.savefig()
    pl.close()
    pdfFile.close()
    print "Done with Total Carbon."

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
