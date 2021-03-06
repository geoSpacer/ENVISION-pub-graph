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
    varList = [' Prescribed Fire (ha)', ' Mowing and Grinding (ha)', ' Thinning (ha)', ' Partial Harvest (ha)']
##    forestedHa = reporterFunc.getOwnerForestedHa(subArea)
##    ownerAllHa = reporterFunc.getOwnerHa(subArea)
    figTextList = ['Federal','Tribal','Corporate Forest','Family Forest']

    # list of ownerships to graphs
#    ownersToGraph = ['Federal','Tribal','Private Industrial','Private Non-Industrial']
    ownersToGraph = ['Federal']

    if ownership == 'SYU':
        pdfFile = PdfPages(outDir + chartTitle + '_syu_Management_area_2x2.pdf')
        varList = [' Prescribed Fire (ha) SYU', ' Mowing and Grinding (ha) SYU', ' Thinning (ha) SYU', ' Partial Harvest (ha) SYU']
    else:
        pdfFile = PdfPages(outDir + chartTitle + '_Management_area_2x2.pdf')

    fig = pl.figure(1, figsize=(11,8.5))
    for varStruct in varList:
        for owner in ownersToGraph:
            # setup plot for all scenarios
            ax = fig.add_subplot(2,2,varList.index(varStruct)+1)
            yLabelText = 'Area of' + varStruct[:-3] + "1000 ha)"

            for scenario in runList:
                inDir = outDir + scenario + "\\"

                if os.path.isdir(inDir):
                    # load area stats by owner
                    areaStats = pd.io.parsers.read_csv(inDir + "AreaStats_by_OWNER_pivot.csv")
                    areaStats = areaStats[areaStats[' Year'] == 1]

                    totalArea = pd.io.parsers.read_csv(inDir + r'ManagementDisturb_by_OWNER_pivot.csv')
                    yearList = list(set(totalArea[' Year']))
                    repList = list(set(totalArea[' Run']))

                    # get stats from multiple reps
                    statsList = []
                    for year in range(1,max(yearList) + 1):
                        yearArea = totalArea[totalArea[' Year'] == year]

                        dataList = []
                        for rep in repList:
                            repArea = yearArea[yearArea[' Run'] == rep]

                            ownerArea = pd.DataFrame(repArea[repArea[' OWNER_label'] == owner])
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

                    if (varList.index(varStruct)) < (len(varList) / 2):
                        labelXtick = False
                    else:
                        labelXtick = True

                    labelYtick = True
                    plotLegend = (0.99,0.99)
                    xLabelText = ''
                    dataTable['mean'] = dataTable['mean'] / 1000
                    dataTable['lower'] = dataTable['lower'] / 1000
                    dataTable['upper'] = dataTable['upper'] / 1000

                    if owner == 'Tribal':
                        plotLegend = (0.84,0.33)

                    mnAxis, mxAxis = reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean','lower','upper'], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, figTextList[ownersToGraph.index(owner)])

            if mxAxis > 7:
                mxAxis += 1
                ax.set_ylim(mnAxis,mxAxis)

    reporterFunc.plotFigureText(fig, 'Simulation Year', '')
    pdfFile.savefig()
    pl.close()



    ## pl.savefig(outDir + 'report4_Vol_Owners.png', bbox_inches='tight', dpi=300)
    pdfFile.close()
    print "Done with Management area."

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
