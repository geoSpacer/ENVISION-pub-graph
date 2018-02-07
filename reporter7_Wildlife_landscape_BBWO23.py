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
    varList = [' High Suitability', ' Northern Goshawk Good (ha)', ' Western Bluebird Good (ha)', ' Black-backed Woodpecker Good (ha)', ' White-headed Woodpecker Good (ha)']
    ownerLabelField = ' OWNER_label'
    ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Homeowner']

    # create new empty dataFrame for output
    outTable = pd.DataFrame()
    for varStruct in varList:
        if varStruct == ' High Suitability':
            modelGroup = 'vfoNSO'
        elif varStruct == 'MD High Suitability':
            varStruct = ' High Suitability'
            modelGroup = 'muleDeer'
        elif varStruct == ' DownyBrome0.66-1 (ha)':
            modelGroup = 'downyBrome'
        else:
            modelGroup = 'iLAP'

        for scenario in runList:
            print 'Wildlife Running scenario ' + scenario + ' and variable ' + varStruct
            inDir = outDir + scenario + "\\"

            varLabel = varStruct[1:]
            if os.path.isdir(inDir):
                if modelGroup == 'vfoNSO':
                    totalArea = pd.io.parsers.read_csv(inDir + r'VFO_Spotted_Owl_by_OWNER_pivot.csv')
                    varLabel = 'VFO_SpottedOwl_ha'
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
                                ownerArea[varStruct].iloc[0] += tempArea[varStruct].iloc[0]

                        dataList.append(ownerArea[varStruct].iloc[0])

                    # convert to numpy array
                    numpyList = np.array(dataList)

                    # add year data to dictionary
                    dataDict = {'timeStep': year, 'mean': np.mean(numpyList, axis=0)}

                    # convert to list for DataFrame
                    statsList.append(dataDict)

                # convert to DataFrame
                dataTable = pd.DataFrame(statsList)

                # make dataFrame to append to output dataFrame
                appendFrame = pd.DataFrame(data=[{'Policy': scenario, 'VarGroup': 'Wildlife', 'Variable': varLabel, 'Year1': dataTable[dataTable['timeStep'] == 1]['mean'].iloc[0], 'Year25': dataTable[dataTable['timeStep'] == 25]['mean'].iloc[0], 'Year49': dataTable[dataTable['timeStep'] == 49]['mean'].iloc[0]}])
                outTable = outTable.append(appendFrame, ignore_index = True)

    outTable.to_csv(outDir + statsFile, mode='a', header=False)
    print "Done with wildlife BBWO23."

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
