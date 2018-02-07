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

def main(subArea, runName, chartTitlePre, ownership):
    outDir = "C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_production\\"
    varList = [' White-headed Woodpecker Good (ha)']
    yLabelText = 'White-headed Woodpecker Good Habitat (ha)'
    chartTitle = chartTitlePre
    PMG345Ha = {'Federal':422702, 'State':22622, 'Private Non-Industrial':23372, 'Private Industrial':51911, 'Tribal':101160, 'Homeowner':3176}

    # list of ownerships to graphs
    if ownership == 'All':
        ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
        pdfFile = PdfPages(outDir + 'report3_WHWO_iLAP_All.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + 'report3_WHWO_iLAP_' + ownersToGraph[0] + '.pdf')

    # setup plot for all scenarios
    fig = pl.figure(1, figsize=(11,8.5))
    ax = fig.add_subplot(1,1,1)

    for scenario in ['CurrentPolicy','NoFedTreat','Restoration']:
        inDir = outDir + runName + "_" + scenario + "\\"

        yearList = list(set(pd.io.parsers.read_csv(inDir + r'ILAP_wildlife_models_pivot.csv')[' Year']))
        repList = list(set(pd.io.parsers.read_csv(inDir + r'ILAP_wildlife_models_pivot.csv')[' Run']))
        totalArea = pd.io.parsers.read_csv(inDir + r'ILAP_wildlife_models_pivot.csv')
        dataTable = pd.DataFrame(totalArea[totalArea[' Year'] > 0])
        dataTable['key'] = 'key_' + dataTable[' Run'].astype(str) + '_' + dataTable[' Year'].astype(str)

        if scenario == 'CurrentPolicy':
            scenarioTable = dataTable
        else:
            scenarioTable = pd.merge(scenarioTable, dataTable, how='left', on='key')

    # subset table for specific year
    valueSet = []
    maxValueSet = []
    labelList = []
    for yearVal in [24,49]:
        yearTable = scenarioTable[scenarioTable[' Year'] == yearVal]

        statsList1 = []
        statsList2 = []
        statsList3 = []

        for i in range(int(round(len(yearTable)))):
            statsList1.append(yearTable[varList[0] + '_x'].iloc[i])
            statsList2.append(yearTable[varList[0] + '_y'].iloc[i])
            statsList3.append(yearTable[varList[0]].iloc[i])

        valueSet.append(statsList1)
        valueSet.append(statsList2)
        valueSet.append(statsList3)

        maxValueSet.append(max(statsList1))
        maxValueSet.append(max(statsList2))
        maxValueSet.append(max(statsList3))

        labelList += ['CP Year ' + str(yearVal),'NFT Year ' + str(yearVal),'Res Year ' + str(yearVal)]

    reporterFunc.plotReporter3(fig, ax, ownership + ' - ' + str(len(repList)) + ' reps', pdfFile, valueSet, labelList, subArea, chartTitle, yLabelText, 'CurrentPolicy', maxValueSet)


    pdfFile.savefig()
    pl.close()
    pdfFile.close()
    print "Done."

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 5:
        print "Usage: reporter_.py <subArea> <runName> <chartTitle> <ownership>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    except Exception, e:
        print "\n\n" + sys.argv[2] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
