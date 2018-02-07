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
    varList = [' Smoke_surfaceFire (Mg)', ' Smoke_mixSevFire (Mg)', ' Smoke_standRepFire (Mg)', ' Smoke_prescribedFire (Mg)']

    # list of ownerships to graphs
##    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
    # remove Tribal from owners to graph
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']

    reporterName = r'Smoke_by_OWNER_pivot.csv'
    ownerLabelField = ' OWNER_label'

    # set list of owners to graph
    if ownership == 'All':
        pdfFile = PdfPages(outDir + chartTitle + '_smoke_landscape.pdf')
    elif ownership in ownersToGraph:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_smoke_' + ownersToGraph[0] + '.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_smoke_' + ownersToGraph[0] + '.pdf')
        ownerLabelField = ' OWNER_DETL_label'
        reporterName = r'Smoke_by_OWNER_DETL_pivot.csv'

    for splot in [1,2,3,4]:
        # setup plot for all scenarios
        fig = pl.figure(1, figsize=(4,4))
        ax = fig.add_subplot(1,1,1)

        for scenario in runList:
            inDir = outDir + scenario + "\\"

            if os.path.isdir(inDir):
                totalArea = pd.io.parsers.read_csv(inDir + reporterName)
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
                                for varName in varList:
        #                            totalArea.loc[list(ownerArea.index)[0],varName] += tempArea[varName].iloc[0]
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                                ownerToGraph = 'All'

                        if splot == 1 or splot == 2:
                            dataList.append(ownerArea[' Smoke_surfaceFire (Mg)'].iloc[0] + ownerArea[' Smoke_mixSevFire (Mg)'].iloc[0] + ownerArea[' Smoke_standRepFire (Mg)'].iloc[0])
                        elif splot == 3 or splot == 4:
                            dataList.append(ownerArea[' Smoke_prescribedFire (Mg)'].iloc[0])

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
                plotLegend = (0.99,0.99)
                xLabelText = 'Simulation Year'
                outVar = 'mean'

                if splot == 1:
                    yLabelText = 'Smoke from wildfire (Mg)'
                elif splot == 2:
                    yLabelText = 'Cumulative smoke from wildfire (1000 Mg)'
                    dataTable['cum_mean'] = dataTable['mean'].cumsum()
                    dataTable['cum_mean'] = dataTable['cum_mean'] / 1000
                    outVar = 'cum_mean'
                    plotLegend = (0.5,0.99)
                elif splot == 3:
                    yLabelText = 'Smoke from prescribed fire (Mg)'
                elif splot == 4:
                    yLabelText = 'Cumulative smoke from prescribed fire (Mg)'
                    dataTable['cum_mean'] = dataTable['mean'].cumsum()
                    outVar = 'cum_mean'
                    plotLegend = (0.5,0.99)

                mnAxis, mxAxis = reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, [outVar], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, '')

        if mxAxis > 1000:
            pl.subplots_adjust(left=0.14)

        pdfFile.savefig()
        pl.close()
    pdfFile.close()
    print "Done with smoke."

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
