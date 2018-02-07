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
    varStruct = ' Total Merch Harvest (m3)'

    # create new empty dataFrame for output
    outTable = pd.DataFrame()
    for scenario in runList:
        inDir = outDir + scenario + "\\"

        if os.path.isdir(inDir):
            totalArea = pd.io.parsers.read_csv(inDir + r'WoodProducts_by_OWNER_pivot.csv')
            yearList = list(set(totalArea[' Year']))
            repList = list(set(totalArea[' Run']))

            # get stats from multiple reps
            statsList = []
            for year in range(1,max(yearList) + 1):
                yearArea = totalArea[totalArea[' Year'] == year]

                dataList = []
                for rep in repList:
                    repArea = yearArea[yearArea[' Run'] == rep]

                    ownerArea = pd.DataFrame(repArea[repArea[' OWNER_label'] == 'Federal'])
                    dataList.append(ownerArea[varStruct].iloc[0])

                # convert to numpy array
                numpyList = np.array(dataList)

                # add year data to dictionary
                dataDict = {'timeStep': year, 'mean': np.mean(numpyList, axis=0)}

                # convert to list for DataFrame
                statsList.append(dataDict)

            # convert to DataFrame
            dataTable = pd.DataFrame(statsList)
            dataTable['cum_mean'] = dataTable['mean'].cumsum()

            # make dataFrame to append to output dataFrame
            appendFrame = pd.DataFrame(data=[{'Policy': scenario, 'VarGroup': 'EcoServices', 'Variable': 'CumulativeTotalMerchHarv_m3', 'Year1': dataTable[dataTable['timeStep'] == 1]['cum_mean'].iloc[0], 'Year25': dataTable[dataTable['timeStep'] == 25]['cum_mean'].iloc[0], 'Year49': dataTable[dataTable['timeStep'] == 49]['cum_mean'].iloc[0]}])
            outTable = outTable.append(appendFrame, ignore_index = True)

    outTable.to_csv(outDir + statsFile, mode='a', header=False)
    print "Done with harvest vol by owner."

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
