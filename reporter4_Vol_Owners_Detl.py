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
    varStruct = ' Total Merch Harvest (m3)'
#    yLabelText = 'Percent of Landscape in'
    chartTitle = chartTitlePre
    forestedHa = reporterFunc.getOwnerForestedHa(subArea)
    ownerAllHa = reporterFunc.getOwnerHa(subArea)

    # list of ownerships to graphs
    ownersToGraph = ['BLM Lands','Chemult Ranger District (Fremont-Winema NF)','Chiloquin Ranger District (Fremont-Winema NF)','Klamath Ranger District (Fremont-Winema NF)','ODF Sun Pass','JWTR Timber Holdings','Cascade Timberlands (Mazama Forest)','Jeld-Wen Inc','J-Spear Ranch']
    pdfFile = PdfPages(outDir + 'report4_Vol_Owners_Detl.pdf')

    fig = pl.figure(1, figsize=(8.5,11))
    subPlotNum = 0
    for owner in ownersToGraph:
        # setup plot for all scenarios
        subPlotNum += 1
        if subPlotNum == 5:
            subPlotNum = 1
            pdfFile.savefig()
            pl.close()
            fig = pl.figure(1, figsize=(8.5,11))

        ax = fig.add_subplot(2,2,subPlotNum)

        for scenario in ['CurrentPolicy','NoTreatment','NoFedTreat','Restoration','NoFireNoMgmt']:
            inDir = outDir + runName + "_" + scenario + "\\"

            if os.path.isdir(inDir):
                yearList = list(set(pd.io.parsers.read_csv(inDir + r'WoodProducts_by_OWNER_DETL_pivot.csv')[' Year']))
                repList = list(set(pd.io.parsers.read_csv(inDir + r'WoodProducts_by_OWNER_DETL_pivot.csv')[' Run']))
                totalArea = pd.io.parsers.read_csv(inDir + r'WoodProducts_by_OWNER_DETL_pivot.csv')
                yLabelText = 'Merchantable Volume Harvested (m3)'

                # get stats from multiple reps
                statsList = []
                for year in range(1,max(yearList) + 1):
                    yearArea = totalArea[totalArea[' Year'] == year]

                    dataList = []
                    for rep in repList:
                        repArea = yearArea[yearArea[' Run'] == rep]

                        ownerArea = pd.DataFrame(repArea[repArea[' OWNER_DETL_label'] == owner])
                        dataList.append(ownerArea[varStruct].iloc[0])

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

                plotLegend = False
                if subPlotNum == 3 or subPlotNum == 4:
                    labelXaxis = True
                else:
                    labelXaxis = False

                yLabelTextOwner = owner + ' ' + yLabelText
                reporterFunc.plotReporter4(fig, ax, owner + ' - ' + str(len(repList)) + ' reps', pdfFile, dataTable, ['mean','lower','upper'], yLabelTextOwner, scenario, labelXaxis, plotLegend)


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
