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

def main(subArea, runName, chartTitlePre):
    outDir = "C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_production\\"
    varList = [' Total Merch Harvest (m3)']
    chartTitle = chartTitlePre
#    PMG345Ha = reporterFunc.getPMG345Ha(subArea)
    PMG12345Ha = reporterFunc.getPMG12345Ha(subArea)

    # list of ownerships to graphs
    reporterName = r'WoodProducts_by_OWNER_DETL_pivot.csv'
    ownerLabelField = ' OWNER_DETL_label'

    pdfFile = PdfPages(outDir + 'report5_Volume_byOwner_noFire.pdf')

    for plotPage in [1,2]:
        # setup plot for all scenarios
        fig = pl.figure(1, figsize=(8.5,11))

        for splot in [1, 2]:
            ax = fig.add_subplot(2,1,splot)
            inDir = outDir + runName + "_noFireCP\\"

            if plotPage == 1:
                if splot == 1:
                    ownersToGraph = ['USFS','State','Corporate Forest']
                elif splot == 2:
                    ownersToGraph = ['Chemult Ranger District (Fremont-Winema NF)','Chiloquin Ranger District (Fremont-Winema NF)','Klamath Ranger District (Fremont-Winema NF)']
            elif plotPage == 2:
                if splot == 1:
                    ownersToGraph = ['ODF Sun Pass','ODF Gilchrist']
                elif splot == 2:
                    ownersToGraph = ['JWTR Timber Holdings','Cascade Timberlands (Mazama Forest)','Jeld-Wen Inc','J-Spear Ranch']

            if os.path.isdir(inDir):
                yearList = list(set(pd.io.parsers.read_csv(inDir + reporterName)[' Year']))
                repList = list(set(pd.io.parsers.read_csv(inDir + reporterName)[' Run']))
                totalArea = pd.io.parsers.read_csv(inDir + reporterName)

                # sum output over selected ownerships
                for ownership in ownersToGraph:
                    print ownership

                    # get stats from multiple reps
                    statsList = []
                    for year in range(1,max(yearList) + 1):
                        yearArea = totalArea[totalArea[' Year'] == year]

                        dataList = []
                        for rep in repList:
                            repArea = yearArea[yearArea[' Run'] == rep]

                            if ownership == 'USFS':
                                ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == 'Chemult Ranger District (Fremont-Winema NF)'])
                                fireProneArea = PMG12345Ha['Chemult Ranger District (Fremont-Winema NF)']

                                for subOwner in ['Chiloquin Ranger District (Fremont-Winema NF)','Klamath Ranger District (Fremont-Winema NF)']:
                                    tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                    fireProneArea += PMG12345Ha[subOwner]
                                    for varName in varList:
                                        ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                            elif ownership == 'State':
                                ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == 'ODF Sun Pass'])
                                fireProneArea = PMG12345Ha['ODF Sun Pass']

                                for subOwner in ['ODF Gilchrist']:
                                    tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                    fireProneArea += PMG12345Ha[subOwner]
                                    for varName in varList:
                                        ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                            elif ownership == 'Corporate Forest':
                                ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == 'JWTR Timber Holdings'])
                                fireProneArea = PMG12345Ha['JWTR Timber Holdings']

                                for subOwner in ['Cascade Timberlands (Mazama Forest)','Jeld-Wen Inc','J-Spear Ranch']:
                                    tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                    fireProneArea += PMG12345Ha[subOwner]
                                    for varName in varList:
                                        ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                            else:
                                ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == ownership])
                                fireProneArea = PMG12345Ha[ownership]

                            if fireProneArea > 0:
                                dataList.append(ownerArea[' Total Merch Harvest (m3)'].iloc[0])
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

                    if splot == 1:
                        labelXaxis = False
                        plotLegend = True
                        yLabelText = 'Total Merchantable Harvest (m3) - No Fire'
                    elif splot == 2:
                        labelXaxis = True
                        plotLegend = True
                        yLabelText = 'Total Merchantable Harvest (m3) - No Fire'

                    reporterFunc.plotReporter5(fig, ax, '', pdfFile, dataTable, ['mean','lower','upper'], yLabelText, ownership, labelXaxis, plotLegend)


        pdfFile.savefig()
        pl.close()
    pdfFile.close()
    print "Done."

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 4:
        print "Usage: reporter_.py <subArea> <runName> <chartTitle>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

    except Exception, e:
        print "\n\n" + sys.argv[2] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
