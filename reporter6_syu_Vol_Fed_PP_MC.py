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
    varStruct = ' Total Merch Harvest SYU (m3)'
    yLabelText = 'Merchantable volume ( $\mathregular{1x10^3}$ $\mathregular{m^3}$)'
    yLabelText2 = 'Cumulative Merchantable volume ( $\mathregular{1x10^6}$ $\mathregular{m^3}$)'
    figTextList = ['Federal','Tribal','Corporate Forest','Family Forest']

    # list of ownerships to graphs
    owner = 'Federal'
    pdfFile = PdfPages(outDir + chartTitle + '_syu_Vol_PP_MC_Fed.pdf')
    pdfFile2 = PdfPages(outDir + chartTitle + '_syu_Vol_PP_MC_Fed_cumulative.pdf')

    for scenario in runList:
        fig = pl.figure(1, figsize=(4,4))
        fig2 = pl.figure(2, figsize=(4,4))
        # setup plot for all scenarios
        ax = fig.add_subplot(1,1,1)
        ax2 = fig2.add_subplot(1,1,1)

        for volSpp in ['','_PP','_MC']:
            inDir = outDir + scenario + "\\"

            if os.path.isdir(inDir):
                totalArea = pd.io.parsers.read_csv(inDir + r'WoodProducts' + volSpp + '_by_OWNER_pivot.csv')
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
                        if volSpp == '_PP':
                            dataList.append(ownerArea[' PP' + varStruct].iloc[0])
                        elif volSpp == '_MC':
                            dataList.append(ownerArea[' MC' + varStruct].iloc[0])
                        else:
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
                plotLegend = (0.99,0.99)
                xLabelText = 'Simulation Year'
                dataTable['mean'] = dataTable['mean'] / 1000
                dataTable['lower'] = dataTable['lower'] / 1000
                dataTable['upper'] = dataTable['upper'] / 1000
                dataTable['cum_mean'] = dataTable['mean'].cumsum()
                dataTable['cum_mean'] = dataTable['cum_mean'] / 1000

                if owner == 'Tribal':
                    plotLegend = (0.84,0.33)

                pl.figure(1)
                mnAxis, mxAxis = reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean','lower','upper'], xLabelText, yLabelText, 'HarvVol' + volSpp + '_SYU', labelXtick, labelYtick, plotLegend, scenario)
                pl.figure(2)
                mnAxis, mxAxis = reporterFunc.plotReporter4(fig2, ax2, '', pdfFile2, dataTable, ['cum_mean'], xLabelText, yLabelText2, 'HarvVol' + volSpp + '_SYU', labelXtick, labelYtick, plotLegend, scenario)

        pdfFile.savefig(fig)
        pdfFile2.savefig(fig2)
        pl.close(fig)
        pl.close(fig2)

    ##reporterFunc.plotFigureText(fig, 'Simulation Year', 'Merchantable volume ( $\mathregular{1x10^3}$ $\mathregular{m^3}$)')

    ## pl.savefig(outDir + 'report4_Vol_Owners.png', bbox_inches='tight', dpi=300)
    pdfFile.close()
    pdfFile2.close()
    print "Done with harvest vol by owner."

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
