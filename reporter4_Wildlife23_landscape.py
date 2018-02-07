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

def main(subArea, runName, chartTitlePre, ownership):
    outDir = "C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_production\\"
    varList = [' Moderate Suitability', ' American Marten', ' Black-backed Woodpecker', ' White-headed Woodpecker', ' Northern Goshawk', ' Western Bluebird', ' Pileated Woodpecker', 'MD Moderate Suitability', ' DownyBrome0.33-0.66 (ha)']
    yLabelText = 'Percent of Landscape in'
    chartTitle = chartTitlePre
    forestedHa = reporterFunc.getOwnerForestedHa(subArea)
    ownerAllHa = reporterFunc.getOwnerHa(subArea)

    # list of ownerships to graphs
    if ownership == 'All':
        ownersToGraph = ['Federal','State','Private Non-Industrial','Private Industrial','Tribal','Homeowner']
        pdfFile = PdfPages(outDir + 'report4_Wildlife23_landscape.pdf')
    else:
        ownersToGraph = [ownership]
        pdfFile = PdfPages(outDir + 'report4_Wildlife23_' + ownersToGraph[0] + '.pdf')

    fig = pl.figure(1, figsize=(8.5,11))
    for varStruct in varList:
        # setup plot for all scenarios
        ax = fig.add_subplot(3,3,varList.index(varStruct) + 1)

        if varStruct == ' Moderate Suitability':
            varStructAdd = ' High Suitability'
            yLabelTextStruct = yLabelText + ' VFO Northern Spotted Owl Mod+High'
            modelGroup = 'vfoNSO'
        elif varStruct == 'MD Moderate Suitability':
            varStructAdd = ' High Suitability'
            yLabelTextStruct = yLabelText + ' Mule Deer Mod+High'
            varStruct = ' Moderate Suitability'
            modelGroup = 'muleDeer'
        elif varStruct == ' DownyBrome0.33-0.66 (ha)':
            varStructAdd = ' DownyBrome0.66-1 (ha)'
            yLabelTextStruct = yLabelText + ' Downy Brome Mod+High'
            modelGroup = 'downyBrome'
        else:
            yLabelTextStruct = yLabelText + varStruct + ' Fair+Good'
            varStructAdd = varStruct + ' Good (ha)'
            varStruct = varStruct + ' Fair (ha)'
            modelGroup = 'iLAP'

        for scenario in ['CurrentPolicy','NoTreatment','NoFedTreat','Restoration','NoFireNoMgmt']:
            inDir = outDir + runName + "_" + scenario + "\\"

            if os.path.isdir(inDir):
                if modelGroup == 'vfoNSO':
                    yearList = list(set(pd.io.parsers.read_csv(inDir + r'VFO_Spotted_Owl_by_OWNER_pivot.csv')[' Year']))
                    repList = list(set(pd.io.parsers.read_csv(inDir + r'VFO_Spotted_Owl_by_OWNER_pivot.csv')[' Run']))
                    totalArea = pd.io.parsers.read_csv(inDir + r'VFO_Spotted_Owl_by_OWNER_pivot.csv')
                elif modelGroup == 'muleDeer':
                    yearList = list(set(pd.io.parsers.read_csv(inDir + r'Mule_Deer_by_OWNER_pivot.csv')[' Year']))
                    repList = list(set(pd.io.parsers.read_csv(inDir + r'Mule_Deer_by_OWNER_pivot.csv')[' Run']))
                    totalArea = pd.io.parsers.read_csv(inDir + r'Mule_Deer_by_OWNER_pivot.csv')
                elif modelGroup == 'downyBrome':
                    yearList = list(set(pd.io.parsers.read_csv(inDir + r'Downy_Brome_by_OWNER_pivot.csv')[' Year']))
                    repList = list(set(pd.io.parsers.read_csv(inDir + r'Downy_Brome_by_OWNER_pivot.csv')[' Run']))
                    totalArea = pd.io.parsers.read_csv(inDir + r'Downy_Brome_by_OWNER_pivot.csv')
                else:
                    yearList = list(set(pd.io.parsers.read_csv(inDir + r'ILAP_wildlife_models_by_OWNER_pivot.csv')[' Year']))
                    repList = list(set(pd.io.parsers.read_csv(inDir + r'ILAP_wildlife_models_by_OWNER_pivot.csv')[' Run']))
                    totalArea = pd.io.parsers.read_csv(inDir + r'ILAP_wildlife_models_by_OWNER_pivot.csv')

                # sum fair and good habitat into fair column
                totalArea[varStruct] = totalArea[varStruct] + totalArea[varStructAdd]

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
                                ownerArea = pd.DataFrame(repArea[repArea[' OWNER_label'] == ownerToGraph])
                                analysisTotalArea = ownerAllHa[ownerToGraph]
                                analysisForestedArea = forestedHa[ownerToGraph]
                            else:
                                tempArea = repArea[repArea[' OWNER_label'] == ownerToGraph]
#                                for varName in varList:
        #                            totalArea.loc[list(ownerArea.index)[0],varName] += tempArea[varName].iloc[0]
                                ownerArea[varStruct].iloc[0] += tempArea[varStruct].iloc[0]

                                analysisTotalArea += ownerAllHa[ownerToGraph]
                                analysisForestedArea += forestedHa[ownerToGraph]
                                ownerToGraph = 'All'

                        if varStruct == ' DownyBrome0.66-1 (ha)' or varStruct == ' DownyBrome0.33-0.66 (ha)':
                            if analysisTotalArea > 0:
                                dataList.append(ownerArea[varStruct].iloc[0] / analysisTotalArea * 100)
                            else:
                                dataList.append(0.0)
                        else:
                            if analysisForestedArea > 0:
                                dataList.append(ownerArea[varStruct].iloc[0] / analysisForestedArea * 100)
                            else:
                                dataList.append(0.0)



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


                if yLabelTextStruct == (yLabelText + ' Pileated Woodpecker Fair+Good') or yLabelTextStruct == (yLabelText + ' Mule Deer Mod+High') or yLabelTextStruct == (yLabelText + ' Downy Brome Mod+High'):
                    labelXaxis = True
                else:
                    labelXaxis = False

                plotLegend = False
##                if varList.index(varStruct) + 1 == 8:
##                    plotLegend = True

                reporterFunc.plotReporter4(fig, ax, ownerToGraph + ' - ' + str(len(repList)) + ' reps', pdfFile, dataTable, ['mean','lower','upper'], yLabelTextStruct, scenario, labelXaxis, plotLegend)


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
