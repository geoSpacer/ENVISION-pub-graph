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
    varList = [' NumberDwellingsFirewise', ' NumberDwellings']
    yLabelText = 'Firewised dwellings (%)'
    chartTitle = chartTitlePre

    # list of ownerships to graphs
    reporterName = r'FireWiseWUI_pivot.csv'
    pdfFile = PdfPages(outDir + 'report4_Firewise_landscape.pdf')

    fig = pl.figure(1, figsize=(8.5,11))
    # setup plot for all scenarios
    ax = fig.add_subplot(2,1,1)

    for scenario in ['CurrentPolicy','No_Treatment_Fed','Restoration','noFireNoTreatFed']:
        inDir = outDir + runName + "_" + scenario + "\\"

        if os.path.isdir(inDir):
            yearList = list(set(pd.io.parsers.read_csv(inDir + reporterName)[' Year']))
            repList = list(set(pd.io.parsers.read_csv(inDir + reporterName)[' Run']))
            totalArea = pd.io.parsers.read_csv(inDir + reporterName)

            # get stats from multiple reps
            statsList = []
            for year in range(1,max(yearList) + 1):
                yearArea = totalArea[totalArea[' Year'] == year]

                dataList = []
                for rep in repList:
                    repArea = yearArea[yearArea[' Run'] == rep]

                    if repArea[' NumberDwellings'].iloc[0] > 0:
                        dataList.append(repArea[' NumberDwellingsFirewise'].iloc[0] / repArea[' NumberDwellings'].iloc[0] * 100)
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

            plotLegend = (0.3,0.99)
            labelXtick = labelYtick = True

            reporterFunc.plotReporter4(fig, ax, '', pdfFile, dataTable, ['mean','lower','upper'], 'Simulation Year', yLabelText, scenario, labelXtick, labelYtick, plotLegend, '')


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
