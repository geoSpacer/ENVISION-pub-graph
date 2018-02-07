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
    varList = [' Resilient (ha) PMG345',' Early Successional (ha) Forest',' Pole and Small (ha) Forest',' Medium (ha) Forest',' Large and Giant (ha) Forest',' Open Canopy (ha) Forest',' Moderate Canopy (ha) Forest',' Closed Canopy (ha) Forest']
    chartTitle = chartTitlePre
    PMG345Ha = reporterFunc.getPMG345Ha(subArea)
    forestedHa = reporterFunc.getOwnerForestedHa(subArea)

    # list of ownerships to graphs
    reporterName = r'ForestStructure2_by_OWNER_DETL_pivot.csv'
    ownerLabelField = ' OWNER_DETL_label'

    pdfFile = PdfPages(outDir + 'report5bar_ForestStructre2_byOwner.pdf')

    # setup plot for all owners
    fig = pl.figure(1, figsize=(11,8.5))

    inDir = outDir + runName + "_CurrentPolicy\\"
    ownersToGraph = ['USFS','State','Corporate Forest','Chemult Ranger District (Fremont-Winema NF)','Chiloquin Ranger District (Fremont-Winema NF)','Klamath Ranger District (Fremont-Winema NF)','ODF Sun Pass','ODF Gilchrist','JWTR Timber Holdings','Cascade Timberlands (Mazama Forest)','Jeld-Wen Inc','J-Spear Ranch']

    if os.path.isdir(inDir):
        yearList = list(set(pd.io.parsers.read_csv(inDir + reporterName)[' Year']))
        repList = list(set(pd.io.parsers.read_csv(inDir + reporterName)[' Run']))
        totalArea = pd.io.parsers.read_csv(inDir + reporterName)

        # sum output over selected ownerships
        for ownership in ownersToGraph:
            ax = fig.add_subplot(2,6,ownersToGraph.index(ownership) + 1)
            print ownership

            # get stats from multiple reps
            statsList = []
            for varStruct in varList:
                for year in [1,max(yearList)]:
                    yearArea = totalArea[totalArea[' Year'] == year]

                    dataList = []
                    for rep in repList:
                        repArea = yearArea[yearArea[' Run'] == rep]

                        if ownership == 'USFS':
                            ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == 'Chemult Ranger District (Fremont-Winema NF)'])
                            fireProneArea345 = PMG345Ha['Chemult Ranger District (Fremont-Winema NF)']
                            fireProneArea = forestedHa['Chemult Ranger District (Fremont-Winema NF)']

                            for subOwner in ['Chiloquin Ranger District (Fremont-Winema NF)','Klamath Ranger District (Fremont-Winema NF)']:
                                tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                fireProneArea345 += PMG345Ha[subOwner]
                                fireProneArea += forestedHa[subOwner]
                                for varName in varList:
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                        elif ownership == 'State':
                            ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == 'ODF Sun Pass'])
                            fireProneArea345 = PMG345Ha['ODF Sun Pass']
                            fireProneArea = forestedHa['ODF Sun Pass']

                            for subOwner in ['ODF Gilchrist','ODF Gilchrist (The Conservation Fund)']:
                                tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                fireProneArea345 += PMG345Ha[subOwner]
                                fireProneArea += forestedHa[subOwner]
                                for varName in varList:
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                        elif ownership == 'ODF Gilchrist':
                            ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == 'ODF Gilchrist'])
                            fireProneArea345 = PMG345Ha['ODF Gilchrist']
                            fireProneArea = forestedHa['ODF Gilchrist']

                            for subOwner in ['ODF Gilchrist (The Conservation Fund)']:
                                tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                fireProneArea345 += PMG345Ha[subOwner]
                                fireProneArea += forestedHa[subOwner]
                                for varName in varList:
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                        elif ownership == 'Corporate Forest':
                            ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == 'JWTR Timber Holdings'])
                            fireProneArea345 = PMG345Ha['JWTR Timber Holdings']
                            fireProneArea = forestedHa['JWTR Timber Holdings']

                            for subOwner in ['Cascade Timberlands (Mazama Forest)','Jeld-Wen Inc','J-Spear Ranch']:
                                tempArea = repArea[repArea[ownerLabelField] == subOwner]
                                fireProneArea345 += PMG345Ha[subOwner]
                                fireProneArea += forestedHa[subOwner]
                                for varName in varList:
                                    ownerArea[varName].iloc[0] += tempArea[varName].iloc[0]

                        else:
                            ownerArea = pd.DataFrame(repArea[repArea[ownerLabelField] == ownership])
                            fireProneArea345 = PMG345Ha[ownership]
                            fireProneArea = forestedHa[ownership]

                        if varStruct in [' Resilient (ha) PMG345', ' Semi-Resilient (ha) PMG345', ' Low Resilience (ha) PMG345']:
                            if fireProneArea345 > 0:
                                dataList.append((ownerArea[varStruct].iloc[0]))
                            else:
                                dataList.append(0.0)
                        else:
                            if fireProneArea > 0:
                                dataList.append((ownerArea[varStruct].iloc[0]))
                            else:
                                dataList.append(0.0)

                    # calculate percent change
                    numpyList = np.array(dataList)
                    if year == 1:
                        startYrMean = np.mean(numpyList, axis=0)
                    else:
                        endYrMean = np.mean(numpyList, axis=0)

                # convert to list for DataFrame
                statsList.append((endYrMean - startYrMean) / startYrMean * 100)

            if 'USFS' in ownership or 'Sun Pass' in ownership:
                labelYaxis = True
            else:
                labelYaxis = False

            yLabelText = 'Percent change'
            varList2 = []
            for varName in varList:
                if '(ha)' in varName:
                    varList2.append(varName[:-12])

            statsList.reverse()
            varList2.reverse()
            statsDF = pd.DataFrame(statsList)
            statsDF['positives'] = statsDF[0] > 0
            reporterFunc.plotReporter5bar(fig, ax, '', pdfFile, statsDF, varList2, yLabelText, ownership, labelYaxis)


    reporterFunc.plotFigureText(fig, 'Change in % of ownership', '')

    pl.savefig(outDir + 'report5bar_ForestStructre2_byOwner.png', bbox_inches='tight', dpi=300)
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
