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

    # remove Tribal from owners to graph
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']

    reporterName = r'PotentialDisturbance_by_OWNER_pivot.csv'
    ownerLabelField = ' OWNER_label'

    # reset list of owners to graph
    if ownership == 'All':
        pdfFile = PdfPages(outDir + chartTitle + '_Potential_HS_Fire_landscape.pdf')
    elif ownership in ownersToGraph:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_Potential_HS_Fire_' + ownersToGraph[0] + '.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_Potential_HS_Fire_' + ownersToGraph[0] + '.pdf')
        ownerLabelField = ' OWNER_DETL_label'
        reporterName = r'PotentialDisturbance_by_OWNER_DETL_pivot.csv'

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

    for splot in [1,3,5,7]:
        # setup plot for all scenarios
        fig = pl.figure(1, figsize=(4,4))
        ax = fig.add_subplot(1,1,1)

        for scenario in runList:
            print "Potential HS Fire Running scenario " + scenario
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
                                ownerArea = pd.DataFrame(repArea[repArea[' OWNER_label'] == ownerToGraph])
                            else:
                                tempArea = repArea[repArea[' OWNER_label'] == ownerToGraph]
                                for varName in varList:
        #                            totalArea.loc[list(ownerArea.index)[0],varName] += tempArea[varName].iloc[0]
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                                ownerToGraph = 'All'

                        if splot == 1 or splot == 2:
                            dataList.append(ownerArea[' Potential HighSev Fire (ha) PMG1'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG2'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG3'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG4'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG5'].iloc[0])
                        elif splot == 3 or splot == 4:
                            dataList.append(ownerArea[' Potential HighSev Fire (ha) PMG3'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG4'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG5'].iloc[0])
                        elif splot == 5 or splot == 6:
                            dataList.append(ownerArea[' Potential HighSev Fire (ha) PMG2'].iloc[0])
                        elif splot == 7 or splot == 8:
                            dataList.append(ownerArea[' Potential HighSev Fire (ha) PMG1'].iloc[0])

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
                plotLegend = (0.5,0.99)
                xLabelText = 'Simulation Year'

                dataTable['mean'] = dataTable['mean'] / 1000
                dataTable['lower'] = dataTable['lower'] / 1000
                dataTable['upper'] = dataTable['upper'] / 1000
                if splot == 1:
                    yLabelText = 'Area of high-severity fire hazard (1000 ha)'
                elif splot == 2:
                    yLabelText = 'Area of high-severity fire hazard (1000 ac)'
                    dataTable['mean'] = dataTable['mean'] * 2.471
                    dataTable['lower'] = dataTable['lower'] * 2.471
                    dataTable['upper'] = dataTable['upper'] * 2.471
                elif splot == 3:
                    yLabelText = 'Area of fire frequent landscape in HS hazard (1000 ha)'
                elif splot == 4:
                    yLabelText = 'Area of fire frequent landscape in HS hazard (1000 ac)'
                    dataTable['mean'] = dataTable['mean'] * 2.471
                    dataTable['lower'] = dataTable['lower'] * 2.471
                    dataTable['upper'] = dataTable['upper'] * 2.471
                elif splot == 5:
                    yLabelText = 'Area of lodgepole landscape in HS hazard (1000 ha)'
                elif splot == 7:
                    yLabelText = 'Area of high elevation landscape in HS hazard (1000 ha)'

                mnAxis, mxAxis = reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean','lower','upper'], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, '')

        # repeat y axis on right with percent
        ax.set_ylim(mnAxis,mxAxis)
        print "Max y axis value found: " + str(mxAxis) + " and min y axis value: " + str(mnAxis)
        if splot == 1:
            yLabelText = 'Area of high-severity fire hazard (%)'
            mnAxis = mnAxis / PMG12345Area * 100000
            mxAxis = mxAxis / PMG12345Area * 100000
        elif splot == 2:
            yLabelText = 'Area of high-severity fire hazard (%)'
            mnAxis = mnAxis / PMG12345Area * 100000 / 2.471
            mxAxis = mxAxis / PMG12345Area * 100000 / 2.471
        elif splot == 3:
            yLabelText = 'Area of fire frequent landscape in HS hazard (%)'
            mnAxis = mnAxis / PMG345Area * 100000
            mxAxis = mxAxis / PMG345Area * 100000
        elif splot == 4:
            yLabelText = 'Area of fire frequent landscape in HS hazard (%)'
            mnAxis = mnAxis / PMG345Area * 100000 / 2.471
            mxAxis = mxAxis / PMG345Area * 100000 / 2.471
        elif splot == 5:
            yLabelText = 'Area of lodgepole landscape in HS hazard (%)'
            mnAxis = mnAxis / PMG2Area * 100000
            mxAxis = mxAxis / PMG2Area * 100000
        elif splot == 7:
            yLabelText = 'Area of high elevation landscape in HS hazard (%)'
            mnAxis = mnAxis / PMG1Area * 100000
            mxAxis = mxAxis / PMG1Area * 100000

        reporterFunc.plotSecondYAxis(ax.twinx(), yLabelText, mnAxis, mxAxis)
        pl.subplots_adjust(right=0.89)

        pdfFile.savefig()
        pl.close()

    pdfFile.close()
    print "Done with HS hazard."

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
