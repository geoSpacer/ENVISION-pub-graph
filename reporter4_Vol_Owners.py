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

def main(outDir, subArea, runName, chartTitlePre, ownership):
    varStruct = ' Total Merch Harvest (m3)'
#    yLabelText = 'Percent of Landscape in'
    chartTitle = chartTitlePre
    forestedHa = reporterFunc.getOwnerForestedHa(subArea)
    ownerAllHa = reporterFunc.getOwnerHa(subArea)
    figTextList = ['A','B','C','D']

    # list of ownerships to graphs
    ownersToGraph = ['Federal','Tribal','Private Industrial','Private Non-Industrial']
    pdfFile = PdfPages(outDir + 'report4_Vol_Owners.pdf')

    fig = pl.figure(1, figsize=(6.5,6.5))
    for owner in ownersToGraph:
        # setup plot for all scenarios
        ax = fig.add_subplot(2,2,ownersToGraph.index(owner) + 1)

#        for scenario in ['CurrentPolicy','No_Treatment_Fed','Restoration','noFireNoTreatFed','noFireCurrentPolicy']:
        for scenario in ['CurrentPolicy','No_Treatment_Fed','Restoration','noFireNoTreatFed']:
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


                labelXtick = True
                labelYtick = True
                plotLegend = (-99,-99)
                xLabelText = 'Simulation Year'
                dataTable['mean'] = dataTable['mean'] / 1000
                dataTable['lower'] = dataTable['lower'] / 1000
                dataTable['upper'] = dataTable['upper'] / 1000

                if ownersToGraph.index(owner) < 2:
                    labelXtick = False
                    xLabelText = ''

                if ownersToGraph.index(owner) % 2 == 1:
                    yLabelText = ''

                if owner == 'Tribal':
                    plotLegend = (0.84,0.33)

                xLabelText = yLabelText = ''
                reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean','lower','upper'], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, figTextList[ownersToGraph.index(owner)])


    reporterFunc.plotFigureText(fig, 'Simulation Year', 'Merchantable volume ( $\mathregular{1x10^3}$ $\mathregular{m^3}$)')

    pl.savefig(outDir + 'report4_Vol_Owners.png', bbox_inches='tight', dpi=300)
    pdfFile.savefig()
    pl.close()
    pdfFile.close()
    print "Done."

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 6:
        print "Usage: reporter_.py <subArea> <runName> <chartTitle> <ownership>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    except Exception, e:
        print "\n\n" + sys.argv[3] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
