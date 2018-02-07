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
    varList = [' NumberDwellings1kmFromStandRep']
    chartTitle = chartTitlePre
    PMG345Ha = reporterFunc.getPMG345Ha(subArea)

    # list of ownerships to graphs
#    if ownership == 'All':
#        ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
    pdfFile = PdfPages(outDir + 'report4bw_Homes_Exposed_to_HS_Fire_All.pdf')
#    else:
#        ownersToGraph = [ownership]
#        pdfFile = PdfPages(outDir + 'report4bw_Homes_Exposed_to_HS_Fire_' + ownersToGraph[0] + '.pdf')

    # setup plot for all scenarios
    fig = pl.figure(1, figsize=(4,6.5))

    # Current Policy run required!
    for scenario in ['No_Treatment_Fed','Restoration','CurrentPolicy']:
        inDir = outDir + runName + "_" + scenario + "\\"

        if scenario == 'No_Treatment_Fed':
            yearList = list(set(pd.io.parsers.read_csv(inDir + r'FireExperience_pivot.csv')[' Year']))
            repList = list(set(pd.io.parsers.read_csv(inDir + r'FireExperience_pivot.csv')[' Run']))

        totalArea = pd.io.parsers.read_csv(inDir + r'FireExperience_pivot.csv')
        dataTable = pd.DataFrame(totalArea[totalArea[' Year'] > 0])
        dataTable['key'] = 'run' + dataTable[' Run'].astype(str) + '_' + dataTable[' Year'].astype(str)

        if scenario == 'No_Treatment_Fed':
            scenarioTable = dataTable
        else:
            scenarioTable = pd.merge(scenarioTable, dataTable, how='left', on='key')

    # sum over owners
    scenarioTable.index = scenarioTable['key']

    #Sort dataTable on number of homes exposed to fire
    scenarioTable = scenarioTable.rename(columns={' NumberDwellings1kmFromStandRep': 'CP_Dwellings1kmHSFire',' NumberDwellings1kmFromStandRep_x': 'NFT_Dwellings1kmHSFire',' NumberDwellings1kmFromStandRep_y': 'Res_Dwellings1kmHSFire'})
    dataTable = scenarioTable.sort('NFT_Dwellings1kmHSFire', ascending=False)

    for splot in [1, 2]:
        ax = fig.add_subplot(2,1,splot)

        # label plots and set percent of top values
        if splot == 1:
            yLabelText = 'Number of dwellings 1km from stand-replacing fire'
            labelXaxis = False
            figText = 'A'
            topPercent = 1.0
        elif splot == 2:
            yLabelText = 'Number of dwellings 1km from top 10% of stand-replacing fires'
            labelXaxis = True
            figText = 'B'
            topPercent = 0.1

        statsList1 = []
        statsList2 = []
        statsList3 = []

        valueSet = []
        maxValueSet = []

        for i in range(int(round(len(dataTable) * topPercent))):
            statsList1.append(dataTable['CP_Dwellings1kmHSFire'].iloc[i])
            statsList2.append(dataTable['NFT_Dwellings1kmHSFire'].iloc[i])
            statsList3.append(dataTable['Res_Dwellings1kmHSFire'].iloc[i])

        valueSet.append(statsList1)
        valueSet.append(statsList2)
        valueSet.append(statsList3)

        maxValueSet.append(max(statsList1))
        maxValueSet.append(max(statsList2))
        maxValueSet.append(max(statsList3))

        yLabelText = ''
        labelList = ['Current\nManagement','No Federal\nTreatment','Accelerated\nRestoration']
        reporterFunc.plotReporter4bw(fig, ax, ownership, pdfFile, valueSet, labelList, subArea, chartTitle, yLabelText, maxValueSet, labelXaxis, figText)


    yLabelText = 'Number of dwellings 1km from high-severity fire'
    reporterFunc.plotFigureText(fig, '', yLabelText)

    pl.savefig(outDir + 'report4bw_Homes_Exposed_to_HS_Fire_All.png', bbox_inches='tight', dpi=300)
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
