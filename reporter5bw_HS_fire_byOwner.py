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
    varList = [' Stand Replacing FirePMG1',' Stand Replacing FirePMG2',' Stand Replacing FirePMG3',' Stand Replacing FirePMG4',' Stand Replacing FirePMG5']
    chartTitle = chartTitlePre
    PMG345Ha = reporterFunc.getPMG345Ha(subArea)
    forestedHa = reporterFunc.getPMG12345Ha(subArea)

    # list of ownerships to graphs
    reporterName = r'FireOccurance_by_OWNER_DETL_pivot.csv'
    ownerLabelField = ' OWNER_DETL_label'

    pdfFile = PdfPages(outDir + 'report5bw_HS_Fire_byOwner.pdf')

#    for plotPage in [1,2,3,4,5,6,7,8]:
    # setup plot for all scenarios
    fig = pl.figure(1, figsize=(6.5,6.5))

    for splot in [1,2,3,4]:
        ax = fig.add_subplot(2,2,splot)
        inDir = outDir + runName + "_CurrentPolicy\\"

#        if plotPage % 2 == 1:
        if splot == 1:
            ownersToGraph = ['USFS','State','Corporate Forest']
            ownerLabel = ['USFS','State','Corporate']
        elif splot == 2:
            ownersToGraph = ['Chemult Ranger District (Fremont-Winema NF)','Chiloquin Ranger District (Fremont-Winema NF)','Klamath Ranger District (Fremont-Winema NF)']
            ownerLabel = ['Chemult RD','Chiloquin RD','Klamath RD']
#        else:
        elif splot == 3:
            ownersToGraph = ['ODF Sun Pass','ODF Gilchrist']
            ownerLabel = ownersToGraph
        elif splot == 4:
            ownersToGraph = ['JWTR Timber Holdings','Cascade Timberlands (Mazama Forest)','Jeld-Wen Inc','J-Spear Ranch']
            ownerLabel = ['PC1','PC2','PC3','PC4']

        if os.path.isdir(inDir):
            yearList = list(set(pd.io.parsers.read_csv(inDir + reporterName)[' Year']))
            repList = list(set(pd.io.parsers.read_csv(inDir + reporterName)[' Run']))
            totalArea = pd.io.parsers.read_csv(inDir + reporterName)

            # sum output over selected ownerships
            valueSet = []
            maxValueSet = []
            for ownership in ownersToGraph:
                print ownership

                # get stats from multiple reps
                dataList = []
                for year in range(1,max(yearList) + 1):
                    yearArea = totalArea[totalArea[' Year'] == year]

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
                            fireProneArea = forestedHa['ODF Gilchrist']

                            for subOwner in ['ODF Gilchrist (The Conservation Fund)']:
                                tempArea = repArea[repArea[ownerLabelField] == subOwner]
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

##                        if plotPage in [1,2,5,6]:
##                            if fireProneArea345 > 0:
##                                dataList.append((ownerArea[' Stand Replacing FirePMG3'].iloc[0] + ownerArea[' Stand Replacing FirePMG4'].iloc[0] + ownerArea[' Stand Replacing FirePMG5'].iloc[0]) / fireProneArea345 * 100)
##                            else:
##                                dataList.append(0.0)
##                        else:
                        if fireProneArea > 0:
                            dataList.append((ownerArea[' Stand Replacing FirePMG1'].iloc[0] + ownerArea[' Stand Replacing FirePMG2'].iloc[0] + ownerArea[' Stand Replacing FirePMG3'].iloc[0] + ownerArea[' Stand Replacing FirePMG4'].iloc[0] + ownerArea[' Stand Replacing FirePMG5'].iloc[0]) / fireProneArea * 100)
                        else:
                            dataList.append(0.0)

##                    if plotPage < 5:
##                        topPercent = 1.0
##                    else:
                topPercent = 0.1

                dataList.sort(reverse=True)
                subDataList = []
                for i in range(int(round(len(dataList) * topPercent))):
                    subDataList.append(dataList[i])

                valueSet.append(subDataList)
                maxValueSet.append(max(subDataList))

            if splot == 1:
                labelXaxis = True
                figText = 'a'
            elif splot == 2:
                labelXaxis = True
                figText = 'b'
            elif splot == 3:
                labelXaxis = True
                figText = 'c'
            elif splot == 4:
                labelXaxis = True
                figText = 'd'

##                if plotPage in [1,2]:
##                    yLabelText = 'Fire frequent area (%)'
##                elif plotPage in [3,4]:
##                    yLabelText = 'Forested area (%)'
##                elif plotPage in [5,6]:
##                    yLabelText = 'Top 10% Fire frequent area (%)'
##                elif plotPage in [7,8]:
##                    yLabelText = 'Top 10% Forested area (%)'

            #reporterFunc.plotReporter5bw(fig, ax, '', pdfFile, valueSet, ownersToGraph, subArea, chartTitle, yLabelText, maxValueSet)

            yLabelText = ''
            reporterFunc.plotReporter5bw(fig, ax, '', pdfFile, valueSet, ownerLabel, subArea, chartTitle, yLabelText, maxValueSet, labelXaxis, figText)


    yLabelText = 'Forested area burned (%)'
    reporterFunc.plotFigureText(fig, '', yLabelText)

    pl.savefig(outDir + 'report5bw_HS_Fire_byOwner.png', bbox_inches='tight', dpi=300)
    pdfFile.savefig()
    pl.close()
    pdfFile.close()
    print "Done."

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 5:
        print "Usage: reporter_.py <subArea> <runName> <chartTitle>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

    except Exception, e:
        print "\n\n" + sys.argv[2] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
