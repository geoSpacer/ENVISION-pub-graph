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
import sys
import numpy as np
import os.path

def main(outDir, runList, statsFile):
    varList = [' Potential HighSev Fire (ha) PMG3', ' Potential HighSev Fire (ha) PMG4', ' Potential HighSev Fire (ha) PMG5']

    # remove Tribal from owners to graph
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']

    reporterName = r'PotentialDisturbance_by_OWNER_pivot.csv'
    ownerLabelField = ' OWNER_label'

    # create new empty dataFrame for output
    outTable = pd.DataFrame()
    for scenario in runList:
        print "Potential HS Fire Running scenario " + scenario
        inDir = outDir + scenario + "\\"

        if os.path.isdir(inDir):
            totalArea = pd.io.parsers.read_csv(inDir + reporterName)
            yearList = list(set(totalArea[' Year']))
            repList = list(set(totalArea[' Run']))

            # get stats from multiple reps
            statsList = []
            for year in [1,25,49]:
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

                    dataList.append(ownerArea[' Potential HighSev Fire (ha) PMG3'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG4'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG5'].iloc[0])

                # convert to numpy array
                numpyList = np.array(dataList)

                # add year data to dictionary
                dataDict = {'timeStep': year, 'mean': np.mean(numpyList, axis=0)}

                # convert to list for DataFrame
                statsList.append(dataDict)

            # convert to DataFrame
            dataTable = pd.DataFrame(statsList)

            # make dataFrame to append to output dataFrame
            appendFrame = pd.DataFrame(data=[{'Policy': scenario, 'VarGroup': 'Fire', 'Variable': 'HSFireHazard_FF_ha', 'Year1': dataTable[dataTable['timeStep'] == 1]['mean'].iloc[0], 'Year25': dataTable[dataTable['timeStep'] == 25]['mean'].iloc[0], 'Year49': dataTable[dataTable['timeStep'] == 49]['mean'].iloc[0]}])
            outTable = outTable.append(appendFrame, ignore_index = True)

    outTable.to_csv(outDir + statsFile, mode='a', header=False)
    print "Done with HS hazard."

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
