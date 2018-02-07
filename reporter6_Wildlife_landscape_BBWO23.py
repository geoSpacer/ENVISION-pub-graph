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
    varList = [' High Suitability', ' American Marten Good (ha)', ' Black-backed Woodpecker Good (ha)', ' White-headed Woodpecker Good (ha)', ' Northern Goshawk Good (ha)', ' Western Bluebird Good (ha)', ' Pileated Woodpecker Good (ha)', 'MD High Suitability', ' DownyBrome0.66-1 (ha)']
    figTextList = ['Northern Spotted Owl\n(nest)','Pacific Marten','Black-backed WP','White-headed WP','Northern Goshawk\n(nest)','Western Bluebird','Pileated WP','Mule Deer','Cheatgrass']
    yLabelText = 'Area (%)'
    ownerLabelField = ' OWNER_label'

    # list of ownerships to graphs
    if ownership == 'All':
        ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']
        pdfFile = PdfPages(outDir + chartTitle + '_Wildlife_landscape_BBWO23.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_Wildlife_' + ownersToGraph[0] + '_BBWO23.pdf')

    # load area stats by owner
    areaStats = pd.io.parsers.read_csv(outDir + runList[0] + "\\AreaStats_by_OWNER_pivot.csv")
    areaStats = areaStats[areaStats[' Year'] == 1]

    # sum total areas over selected ownerships
    for ownerToGraph in ownersToGraph:
        ownerStats = areaStats[areaStats[ownerLabelField] == ownerToGraph]
        if ownerToGraph == ownersToGraph[0]:
            analysisModeledArea = ownerStats[' Forested (ha)'].iloc[0] + ownerStats[' Arid (ha)'].iloc[0]
            analysisForestedArea = ownerStats[' Forested (ha)'].iloc[0]
        else:
            analysisModeledArea += ownerStats[' Forested (ha)'].iloc[0] + ownerStats[' Arid (ha)'].iloc[0]
            analysisForestedArea += ownerStats[' Forested (ha)'].iloc[0]

    for varStruct in varList:
        # setup plot for all scenarios
        fig = pl.figure(1, figsize=(4,4))
        ax = fig.add_subplot(1,1,1)

        if varStruct == ' High Suitability':
            yLabelTextStruct = yLabelText + ' VFO Northern Spotted Owl High Suitability'
            modelGroup = 'vfoNSO'
        elif varStruct == 'MD High Suitability':
            yLabelTextStruct = yLabelText + ' Mule Deer High Suitability'
            varStruct = ' High Suitability'
            modelGroup = 'muleDeer'
        elif varStruct == ' DownyBrome0.66-1 (ha)':
            yLabelTextStruct = yLabelText + ' Downy Brome High Suitability'
            modelGroup = 'downyBrome'
        else:
            yLabelTextStruct = yLabelText + varStruct
            yLabelTextStruct = yLabelTextStruct.replace(" (ha)", "")
            modelGroup = 'iLAP'

        for scenario in runList:
            print 'Wildlife Running scenario ' + scenario + ' and variable ' + varStruct
            inDir = outDir + scenario + "\\"

            if os.path.isdir(inDir):
                if modelGroup == 'vfoNSO':
                    totalArea = pd.io.parsers.read_csv(inDir + r'VFO_Spotted_Owl_by_OWNER_pivot.csv')
                elif modelGroup == 'muleDeer':
                    totalArea = pd.io.parsers.read_csv(inDir + r'Mule_Deer_by_OWNER_pivot.csv')
                elif modelGroup == 'downyBrome':
                    totalArea = pd.io.parsers.read_csv(inDir + r'Downy_Brome_by_OWNER_pivot.csv')
                else:
                    totalArea = pd.io.parsers.read_csv(inDir + r'ILAP_wildlife_models_by_OWNER_pivot.csv')

                    # if species is Black-backed wookpecker do fair + good
                    if varStruct == ' Black-backed Woodpecker Good (ha)':
                        totalArea[' Black-backed Woodpecker Good (ha)'] = totalArea[' Black-backed Woodpecker Good (ha)'] + totalArea[' Black-backed Woodpecker Fair (ha)']

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
#                                for varName in varList:
        #                            totalArea.loc[list(ownerArea.index)[0],varName] += tempArea[varName].iloc[0]
                                ownerArea[varStruct].iloc[0] += tempArea[varStruct].iloc[0]

                                ownerToGraph = 'All'

                        dataList.append(ownerArea[varStruct].iloc[0])

##                        if varStruct == ' DownyBrome0.66-1 (ha)' or varStruct == ' DownyBrome0.33-0.66 (ha)':
##                            if analysisTotalArea > 0:
##                                dataList.append(ownerArea[varStruct].iloc[0] / analysisTotalArea * 100)
##                            else:
##                                dataList.append(0.0)
##                        else:
##                            if analysisForestedArea > 0:
##                                dataList.append(ownerArea[varStruct].iloc[0] / analysisForestedArea * 100)
##                            else:
##                                dataList.append(0.0)


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
                dataTable['mean'] = dataTable['mean'] / 1000 * 2.471
                dataTable['lower'] = dataTable['lower'] / 1000 * 2.471
                dataTable['upper'] = dataTable['upper'] / 1000 * 2.471

                figText = figTextList[varList.index(varStruct)]
                if modelGroup == 'muleDeer':
                    figText = 'Mule Deer'

                labelXtick = True
                labelYtick = True
                yLabelText = 'Area (1000 ac)'
                xLabelText = 'Simulation Year'

                if figText == 'Western Bluebird':
                    plotLegend = (0.99,0.5)
                elif figText == 'Northern Goshawk\n(nest)':
                    plotLegend = (0.99,0.6)
                elif figText == 'Pacific Marten' or figText == 'Black-backed WP' or figText == 'White-headed WP' or figText == 'Mule Deer' or figText == 'Pileated WP':
                    plotLegend = (0.35,0.3)
                elif figText == 'Northern Spotted Owl\n(nest)':
                    plotLegend = (0.35,0.99)
                else:
                    plotLegend = (0.99,0.99)

                mnAxis, mxAxis = reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean'], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, figText)

        # repeat y axis on right with percent
        ax.set_ylim(mnAxis,mxAxis)
        print "Max y axis value found: " + str(mxAxis) + " and min y axis value: " + str(mnAxis)
        yLabelText = 'Area (%)'
        if varStruct == ' DownyBrome0.66-1 (ha)' or varStruct == ' DownyBrome0.33-0.66 (ha)':
            mnAxis = mnAxis / analysisModeledArea * 100000 / 2.471
            mxAxis = mxAxis / analysisModeledArea * 100000 / 2.471
        else:
            mnAxis = mnAxis / analysisForestedArea * 100000 / 2.471
            mxAxis = mxAxis / analysisForestedArea * 100000 / 2.471

        reporterFunc.plotSecondYAxis(ax.twinx(), yLabelText, mnAxis, mxAxis)
        if mxAxis - mnAxis <= 4.5:
            pl.subplots_adjust(right=0.87)
        elif (mxAxis * analysisForestedArea / 100000 * 2.471) > 1000:
            pl.subplots_adjust(left=0.14)

        pdfFile.savefig()
        pl.close()

    pdfFile.close()
    print "Done with wildlife BBWO23."

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
