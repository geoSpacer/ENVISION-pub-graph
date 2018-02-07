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
    varList = [' Stand Replacing FirePMG1', ' Stand Replacing FirePMG2', ' Stand Replacing FirePMG3', ' Stand Replacing FirePMG4', ' Stand Replacing FirePMG5']

    # list of ownerships to graphs
##    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
    # remove Tribal from owners to graph
    ownersToGraph = ['Federal']

    reporterName = r'FireOccurance_by_OWNER_pivot.csv'
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

                    dataDict = {'rep_num': rep, 'year_num': year, 'HS_ha': ownerArea[' Stand Replacing FirePMG1'].iloc[0] + ownerArea[' Stand Replacing FirePMG2'].iloc[0] + ownerArea[' Stand Replacing FirePMG3'].iloc[0] + ownerArea[' Stand Replacing FirePMG4'].iloc[0] + ownerArea[' Stand Replacing FirePMG5'].iloc[0]}

                    # convert to list for DataFrame
                    statsList.append(dataDict)

            # convert to DataFrame
            dataTable = pd.DataFrame(statsList)

            extremeList = []
            if scenario == runList[0]:
                dataTable = dataTable.sort('HS_ha', ascending=False)
                indexTable = dataTable.head(n=38)
                indexTable.to_csv(outDir + scenario + ".csv", mode='w', header=True)

            for event in range(len(indexTable)):
                try:
                    extremeList.append(dataTable[(dataTable.rep_num == indexTable['rep_num'].iloc[event]) & (dataTable.year_num == indexTable['year_num'].iloc[event])]['HS_ha'].iloc[0])
                except:
                    print('Error!! Missing ' + 'Year ' + str(plotYear) + ' rep ' + str(plotRep))

            # make dataFrame to append to output dataFrame
            appendFrame = pd.DataFrame(data=[{'Policy': scenario, 'VarGroup': 'Fed For', 'Variable': 'HSFireExreme_For_ha', 'Value': sum(extremeList)}])
            outTable = outTable.append(appendFrame, ignore_index = True)

            numpyList = np.array(extremeList)
            appendFrame = pd.DataFrame(data=[{'Policy': scenario, 'VarGroup': 'Fed For', 'Variable': 'HSFireExreme_For_mean_ha', 'Value': np.mean(numpyList, axis=0)}])
            outTable = outTable.append(appendFrame, ignore_index = True)

            appendFrame = pd.DataFrame(data=[{'Policy': scenario, 'VarGroup': 'Fed For', 'Variable': 'HSFireExreme_For_median_ha', 'Value': np.median(numpyList, axis=0)}])
            outTable = outTable.append(appendFrame, ignore_index = True)

            appendFrame = pd.DataFrame(data=[{'Policy': scenario, 'VarGroup': 'Fed For', 'Variable': 'HSFireExreme_For_percent', 'Value': sum(extremeList) / sum(dataTable['HS_ha']) * 100}])
            outTable = outTable.append(appendFrame, ignore_index = True)

    outTable.to_csv(outDir + statsFile, mode='w', header=True)
    print "Done with PMG in HS fire extreme."

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
