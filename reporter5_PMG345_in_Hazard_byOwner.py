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
    varList = [' Potential HighSev Fire (ha) PMG3', ' Potential HighSev Fire (ha) PMG4', ' Potential HighSev Fire (ha) PMG5']
    chartTitle = chartTitlePre
    PMG345Ha = reporterFunc.getPMG345Ha(subArea)
#    PMG12345Ha = reporterFunc.getPMG12345Ha(subArea)

    # list of ownerships to graphs
    reporterName = r'PotentialDisturbance_by_OWNER_DETL_pivot.csv'
    ownerLabelField = ' OWNER_DETL_label'

    pdfFile = PdfPages(outDir + 'report5_PMG345_HS_Hazard_byOwner.pdf')

#    for plotPage in [1,2]:
    # setup plot for all scenarios
    fig = pl.figure(1, figsize=(6.5,6.5))

    for splot in [1, 2, 3, 4]:
        ax = fig.add_subplot(2,2,splot)
        inDir = outDir + runName + "_CurrentPolicy\\"

#        if plotPage == 1:
        if splot == 1:
            ownersToGraph = ['USFS','State','Corporate Forest']
        elif splot == 2:
            ownersToGraph = ['Chemult Ranger District (Fremont-Winema NF)','Chiloquin Ranger District (Fremont-Winema NF)','Klamath Ranger District (Fremont-Winema NF)']
#        elif plotPage == 2:
        if splot == 3:
            ownersToGraph = ['ODF Sun Pass','ODF Gilchrist']
        elif splot == 4:
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
                            fireProneArea = PMG345Ha['Chemult Ranger District (Fremont-Winema NF)']

                            for subOwner in ['Chiloquin Ranger District (Fremont-Winema NF)','Klamath Ranger District (Fremont-Winema NF)']:
                                tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                fireProneArea += PMG345Ha[subOwner]
                                for varName in varList:
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                        elif ownership == 'State':
                            ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == 'ODF Sun Pass'])
                            fireProneArea = PMG345Ha['ODF Sun Pass']

                            for subOwner in ['ODF Gilchrist','ODF Gilchrist (The Conservation Fund)']:
                                tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                fireProneArea += PMG345Ha[subOwner]
                                for varName in varList:
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                        elif ownership == 'ODF Gilchrist':
                            ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == 'ODF Gilchrist'])
                            fireProneArea = PMG345Ha['ODF Gilchrist']

                            for subOwner in ['ODF Gilchrist (The Conservation Fund)']:
                                tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                fireProneArea += PMG345Ha[subOwner]
                                for varName in varList:
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                        elif ownership == 'Corporate Forest':
                            ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == 'JWTR Timber Holdings'])
                            fireProneArea = PMG345Ha['JWTR Timber Holdings']

                            for subOwner in ['Cascade Timberlands (Mazama Forest)','Jeld-Wen Inc','J-Spear Ranch']:
                                tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                fireProneArea += PMG345Ha[subOwner]
                                for varName in varList:
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                        else:
                            ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == ownership])
                            fireProneArea = PMG345Ha[ownership]

                        if fireProneArea > 0:
                            dataList.append((ownerArea[' Potential HighSev Fire (ha) PMG3'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG4'].iloc[0] + ownerArea[' Potential HighSev Fire (ha) PMG5'].iloc[0]) / fireProneArea * 100)
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

                plotLegend = (0.99,0.99)
                labelYtick = True
                if splot == 1:
                    labelXtick = False
                    figText = 'a'
                    plotLegend = (0.99,0.65)
                elif splot == 2:
                    labelXtick = False
                    figText = 'b'
                elif splot == 3:
                    labelXtick = True
                    figText = 'c'
                elif splot == 4:
                    labelXtick = True
                    figText = 'd'
                    plotLegend = (0.99,0.65)

                xLabelText = yLabelText = ''
                reporterFunc.plotReporter5(fig, ax, '', pdfFile, dataTable, ['mean','lower','upper'], xLabelText, yLabelText, ownership, labelXtick, labelYtick, plotLegend, figText)

    reporterFunc.plotFigureText(fig, 'Simulation year', 'Fire prone landscape in high severity fire hazard (%)')

    pl.savefig(outDir + 'report5_PMG345_HS_Hazard_byOwner.png', bbox_inches='tight', dpi=300)
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
