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
    varList = [' Small Tree Saw Timber Total',' Medium Tree Saw Timber Total',' Large Tree Saw Timber Total',' Giant Tree Saw Timber Total']
    yLabelText = ''
    figTextList = ['Small trees','Medium trees','Large trees','Giant trees']

    # list of ownerships to graphs
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']
    reporterName = r'StandingVol_bySize_by_OWNER_pivot.csv'
    ownerLabelField = ' OWNER_label'

    if ownership == 'All':
        pdfFile = PdfPages(outDir + chartTitle + '_syu_StandingVol_bySize_landscape.pdf')
    elif ownership in ownersToGraph:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_syu_StandingVol_bySize_' + ownersToGraph[0] + '.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_syu_StandingVol_bySize_' + ownersToGraph[0] + '.pdf')
        ownerLabelField = ' OWNER_DETL_label'
        reporterName = r'StandingVol_bySize_by_OWNER_DETL_pivot.csv'

    fig = pl.figure(1, figsize=(11,8.5))
    for varStruct in varList:
        # setup plot for all scenarios
        ax = fig.add_subplot(2,2,varList.index(varStruct) + 1)
        print ('Running ' + varStruct)

        for scenario in runList:
            inDir = outDir + scenario + "\\"

            if os.path.isdir(inDir):
                totalArea = pd.io.parsers.read_csv(inDir + reporterName)
                yearList = list(set(totalArea[' Year']))
                repList = list(set(totalArea[' Run']))

                # get stats from multiple reps
                statsList = []
                statsList2 = []
                for year in range(1,max(yearList) + 1):
                    yearArea = totalArea[totalArea[' Year'] == year]

                    dataList = []
                    dataList2 = []
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

                        dataList.append(ownerArea[varStruct + ' (m3)'].iloc[0])
                        dataList2.append(ownerArea[varStruct + ' SYU (m3)'].iloc[0])

                    # convert to numpy array
                    numpyList = np.array(dataList)
                    numpyList2 = np.array(dataList2)

                    # add year data to dictionary
                    dataDict = {'timeStep': year, 'mean': np.mean(numpyList, axis=0)}
                    dataDict2 = {'timeStep': year, 'mean': np.mean(numpyList2, axis=0)}

                    # convert to list for DataFrame
                    statsList.append(dataDict)
                    statsList2.append(dataDict2)

                # convert to DataFrame
                dataTable = pd.DataFrame(statsList)
                dataTable2 = pd.DataFrame(statsList2)

                if (varList.index(varStruct)) < (len(varList) / 2):
                    labelXtick = False
                else:
                    labelXtick = True

                labelYtick = True
                yLabelText = ''

                labelYtick = True
                plotLegend = (0.99,0.99)
                xLabelText = ''
                dataTable['mean'] = dataTable['mean'] / 1000000
                dataTable2['mean'] = dataTable2['mean'] / 1000000

                mnAxis, mxAxis = reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean'], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, figTextList[varList.index(varStruct)])
                mnAxis, mxAxis = reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable2, ['mean'], xLabelText, yLabelText, scenario + '_SYU_', labelXtick, labelYtick, plotLegend, figTextList[varList.index(varStruct)])

    reporterFunc.plotFigureText(fig, 'Simulation Year', 'Standing saw timber volume ( $\mathregular{1x10^6}$ $\mathregular{m^3}$)')

#    pl.savefig(outDir + 'report4_ForestStructure2_landscape.png', bbox_inches='tight', dpi=300)
    pdfFile.savefig()
    pl.close()
    pdfFile.close()
    print "Done with standing volume."

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
