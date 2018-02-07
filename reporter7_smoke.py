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

def main(outDir, runList, statsFile):
    varList = [' Smoke_surfaceFire (Mg)', ' Smoke_mixSevFire (Mg)', ' Smoke_standRepFire (Mg)', ' Smoke_prescribedFire (Mg)']

    # list of ownerships to graphs
##    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
    # remove Tribal from owners to graph
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']

    reporterName = r'Smoke_by_OWNER_pivot.csv'
    ownerLabelField = ' OWNER_label'

    # create new empty dataFrame for output
    outTable = pd.DataFrame()
    for scenario in runList:
        print 'Running scenario ' + scenario
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

                    dataList.append(ownerArea[' Smoke_surfaceFire (Mg)'].iloc[0] + ownerArea[' Smoke_mixSevFire (Mg)'].iloc[0] + ownerArea[' Smoke_standRepFire (Mg)'].iloc[0] + ownerArea[' Smoke_prescribedFire (Mg)'].iloc[0])
                    dataList2.append(ownerArea[' Smoke_prescribedFire (Mg)'].iloc[0])

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
            dataTable['cum_mean'] = dataTable['mean'].cumsum()
            dataTable2 = pd.DataFrame(statsList2)
            dataTable2['cum_mean'] = dataTable2['mean'].cumsum()

            # make dataFrame to append to output dataFrame
            appendFrame = pd.DataFrame(data=[{'Policy': scenario, 'VarGroup': 'Fire', 'Variable': 'CumulativeSmokeAll_Mg', 'Year1': dataTable[dataTable['timeStep'] == 1]['cum_mean'].iloc[0], 'Year25': dataTable[dataTable['timeStep'] == 25]['cum_mean'].iloc[0], 'Year49': dataTable[dataTable['timeStep'] == 49]['cum_mean'].iloc[0]}])
            outTable = outTable.append(appendFrame, ignore_index = True)
            appendFrame2 = pd.DataFrame(data=[{'Policy': scenario, 'VarGroup': 'Fire', 'Variable': 'CumulativeSmokePrescribed_Mg', 'Year1': dataTable2[dataTable2['timeStep'] == 1]['cum_mean'].iloc[0], 'Year25': dataTable2[dataTable2['timeStep'] == 25]['cum_mean'].iloc[0], 'Year49': dataTable2[dataTable2['timeStep'] == 49]['cum_mean'].iloc[0]}])
            outTable = outTable.append(appendFrame2, ignore_index = True)

    outTable.to_csv(outDir + statsFile, mode='a', header=False)

    print "Done with smoke."

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 4:
        print "Usage: reporter_.py <outDir> <runList> <statsFile>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

    except Exception, e:
        print "\n\n" + sys.argv[1] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
