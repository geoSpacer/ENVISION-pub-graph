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
    varList = [' Stand Replacing FirePMG1',' Stand Replacing FirePMG2',' Stand Replacing FirePMG3',' Stand Replacing FirePMG4',' Stand Replacing FirePMG5',' Surface FirePMG1',' Surface FirePMG2',' Surface FirePMG3',' Surface FirePMG4',' Surface FirePMG5',' Mixed Severity FirePMG1',' Mixed Severity FirePMG2',' Mixed Severity FirePMG3',' Mixed Severity FirePMG4',' Mixed Severity FirePMG5']

    # list of ownerships to graphs
##    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
    # remove Tribal from owners to graph
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']

    reporterName = r'FireOccurance_by_OWNER_pivot.csv'
    ownerLabelField = ' OWNER_label'

    # set list of owners to graph
    if ownership == 'All':
        pdfFile = PdfPages(outDir + chartTitle + '_HS_Fire_proportion.pdf')
    elif ownership in ownersToGraph:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_HS_Fire_prop_' + ownersToGraph[0] + '.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + chartTitle + '_HS_Fire_prop_' + ownersToGraph[0] + '.pdf')
        ownerLabelField = ' OWNER_DETL_label'
        reporterName = r'FireOccurance_by_OWNER_DETL_pivot.csv'

    for splot in [1,3,5,7]:
        # setup plot for all scenarios
        fig = pl.figure(1, figsize=(4,4))
        ax = fig.add_subplot(1,1,1)

        for scenario in runList:
            inDir = outDir + scenario + "\\"
            print ('Running scenario ' + scenario)

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
                            HSarea = ownerArea[' Stand Replacing FirePMG1'].iloc[0] + ownerArea[' Stand Replacing FirePMG2'].iloc[0] + ownerArea[' Stand Replacing FirePMG3'].iloc[0] + ownerArea[' Stand Replacing FirePMG4'].iloc[0] + ownerArea[' Stand Replacing FirePMG5'].iloc[0]
                            MSarea = ownerArea[' Mixed Severity FirePMG1'].iloc[0] + ownerArea[' Mixed Severity FirePMG2'].iloc[0] + ownerArea[' Mixed Severity FirePMG3'].iloc[0] + ownerArea[' Mixed Severity FirePMG4'].iloc[0] + ownerArea[' Mixed Severity FirePMG5'].iloc[0]
                            SUarea = ownerArea[' Surface FirePMG1'].iloc[0] + ownerArea[' Surface FirePMG2'].iloc[0] + ownerArea[' Surface FirePMG3'].iloc[0] + ownerArea[' Surface FirePMG4'].iloc[0] + ownerArea[' Surface FirePMG5'].iloc[0]
                        elif splot == 3 or splot == 4:
                            HSarea = ownerArea[' Stand Replacing FirePMG3'].iloc[0] + ownerArea[' Stand Replacing FirePMG4'].iloc[0] + ownerArea[' Stand Replacing FirePMG5'].iloc[0]
                            MSarea = ownerArea[' Mixed Severity FirePMG3'].iloc[0] + ownerArea[' Mixed Severity FirePMG4'].iloc[0] + ownerArea[' Mixed Severity FirePMG5'].iloc[0]
                            SUarea = ownerArea[' Surface FirePMG3'].iloc[0] + ownerArea[' Surface FirePMG4'].iloc[0] + ownerArea[' Surface FirePMG5'].iloc[0]
                        elif splot == 5 or splot == 6:
                            HSarea = ownerArea[' Stand Replacing FirePMG2'].iloc[0]
                            MSarea = ownerArea[' Mixed Severity FirePMG2'].iloc[0]
                            SUarea = ownerArea[' Surface FirePMG2'].iloc[0]
                        elif splot == 7 or splot == 8:
                            HSarea = ownerArea[' Stand Replacing FirePMG1'].iloc[0]
                            MSarea = ownerArea[' Mixed Severity FirePMG1'].iloc[0]
                            SUarea = ownerArea[' Surface FirePMG1'].iloc[0]

                        # if fire occured in that rep then add to dataList
                        if (HSarea + MSarea + SUarea) > 0:
                            dataList.append(HSarea / (HSarea + MSarea + SUarea) * 100)

                    # convert to numpy array
                    numpyList = np.array(dataList)
                    lower95th = np.mean(numpyList, axis=0) - ((1.96 * np.std(numpyList, axis=0)) / np.sqrt(len(repList)))
                    upper95th = np.mean(numpyList, axis=0) + ((1.96 * np.std(numpyList, axis=0)) / np.sqrt(len(repList)))

                    if lower95th < 0:
                        lower95th = 0.0

                    # add year data to dictionary
                    if len(numpyList) > 0:
                        dataDict = {'timeStep': year, 'mean': np.mean(numpyList, axis=0), 'std': np.std(numpyList, axis=0), 'lower': lower95th, 'upper': upper95th}
                    else:
                        dataDict = {'timeStep': year, 'mean': 0.0, 'std': 0.0, 'lower': 0.0, 'upper': 0.0}

                    # convert to list for DataFrame
                    statsList.append(dataDict)

                # convert to DataFrame
                dataTable = pd.DataFrame(statsList)

                labelXtick = True
                labelYtick = True
                plotLegend = (0.5,0.99)
                xLabelText = 'Simulation Year'

                if splot == 1:
                    yLabelText = 'Proportion of wildfire in HS (%)'
                elif splot == 3:
                    yLabelText = 'Proportion of wildfire in HS for FF landscape (%)'
                if splot == 5:
                    yLabelText = 'Proportion of wildfire in HS for lodgepole landscape (%)'
                if splot == 7:
                    yLabelText = 'Proportion of wildfire in HS for high elev landscape (%)'

                mnAxis, mxAxis = reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean'], xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, '')

        pdfFile.savefig()
        pl.close()
    pdfFile.close()
    print "Done with PMG in HS fire proportion."

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
