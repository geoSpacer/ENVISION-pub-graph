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
    varList = [' Seedling-Sapling', ' Pole',' Small tree',' Medium tree',' Large tree',' Giant tree',' Open Canopy',' Moderate Canopy',' Closed Canopy',' Single-story',' Multi-story']

    # list of ownerships to graphs
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']
    reporterNameVol = r'ForestStructure3_by_OWNER_pivot.csv'
    ownerLabelField = ' OWNER_label'

    if ownership == 'All':
        pdfFile = PdfPages(outDir + chartTitle + '_ForestStructure3_landscape.pdf')
    elif ownership in ownersToGraph:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_ForestStructure3_' + ownersToGraph[0] + '.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_ForestStructure3_' + ownersToGraph[0] + '.pdf')
        ownerLabelField = ' OWNER_DETL_label'

    # load area stats by owner
    areaStats = pd.io.parsers.read_csv(outDir + runList[0] + "\\AreaStats_by_OWNER_pivot.csv")
    areaStats = areaStats[areaStats[' Year'] == 1]

    # sum total areas over selected ownerships
    for ownerToGraph in ownersToGraph:
        ownerStats = areaStats[areaStats[ownerLabelField] == ownerToGraph]
        if ownerToGraph == ownersToGraph[0]:
            PMG345Area = ownerStats[' PVT MNG GR 3 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 4 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 5 (ha)'].iloc[0]
            analysisModeledArea = ownerStats[' Forested (ha)'].iloc[0] + ownerStats[' Arid (ha)'].iloc[0]
            analysisForestedArea = ownerStats[' Forested (ha)'].iloc[0]
        else:
            PMG345Area += ownerStats[' PVT MNG GR 3 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 4 (ha)'].iloc[0] + ownerStats[' PVT MNG GR 5 (ha)'].iloc[0]
            analysisModeledArea += ownerStats[' Forested (ha)'].iloc[0] + ownerStats[' Arid (ha)'].iloc[0]
            analysisForestedArea += ownerStats[' Forested (ha)'].iloc[0]

    for landscape in [' (ha) PMG345',' (ha) Forest']:
        for varStruct in varList:
            print 'Forest structure 3 - ' + varStruct + landscape
            fig = pl.figure(1, figsize=(4,4))
            # setup plot for all scenarios
            ax = fig.add_subplot(1,1,1)

            varStruct += landscape
            if landscape == ' (ha) PMG345':
                yLabelText = 'Area of FF landscape in ' + varStruct[1:-12] + ' (1000 ha)'
                analysisArea = PMG345Area
            elif landscape == ' (ha) Forest':
                yLabelText = 'Area of ' + varStruct[1:-12] + ' (1000 ha)'
                analysisArea = analysisForestedArea
            else:
                yLabelText = 'Error!! Missing landscape'
                analysisArea = 1

            for scenario in runList:
                inDir = outDir + scenario + "\\"

                if os.path.isdir(inDir):
                    totalArea = pd.io.parsers.read_csv(inDir + reporterNameVol)
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
                                    ownerArea[varStruct].iloc[0] += repArea[repArea[ownerLabelField] == ownerToGraph][varStruct].iloc[0]

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
    #                unitText = ' ( $\mathregular{1x10^6}$ $\mathregular{m^3}$ )'
                    dataTable['mean'] = dataTable['mean'] / 1000
                    dataTable['lower'] = dataTable['lower'] / 1000
                    dataTable['upper'] = dataTable['upper'] / 1000
                    labelXtick = True
                    xLabelText = 'Simulation Year'
                    plotLegend = (0.5,0.99)
                    figText = ''

                    mnAxis, mxAxis = reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean'], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, figText)

            # repeat y axis on right with percent
            ax.set_ylim(mnAxis,mxAxis)
            print "Max y axis value found: " + str(mxAxis) + " and min y axis value: " + str(mnAxis)
            yLabelText = yLabelText[:-8] + '%)'
            mnAxis = mnAxis / analysisArea * 100000
            mxAxis = mxAxis / analysisArea * 100000

            reporterFunc.plotSecondYAxis(ax.twinx(), yLabelText, mnAxis, mxAxis)
            if mxAxis - mnAxis <= 4.5:
                pl.subplots_adjust(right=0.87)
            elif (mxAxis * analysisArea / 100000) > 1000:
                pl.subplots_adjust(left=0.14)

            pdfFile.savefig()
            pl.close()
    pdfFile.close()
    print "Done with ForestStructure3."

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
