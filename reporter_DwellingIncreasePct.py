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
import reporterFunc

def main(subArea, runName, chartTitle):
    outDir = "C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_test\\" + runName + "\\"
    pdfFile = PdfPages(outDir + '50_DwellingIncreasePct.pdf')
    varList = [' NumberDwellings']

    # plot total area
    totalArea = pd.io.parsers.read_csv(outDir + r'FireWise_pivot.csv')
    reporterFunc.plotReporter('', pdfFile, totalArea, varList, subArea, chartTitle, yLabeltext)

    fig = pl.figure(1, figsize=(11,8.5))
    ax = fig.add_subplot(1,1,1)

#    for varName in [' NumberDwellingsFirewise', ' NumberDwellings']:
    ax.plot(totalArea[' Year'], totalArea[' NumberDwellings'])

    # build legend
    #fontP = FontProperties()
    #fontP.set_size('10')
    #ax.legend(prop = fontP, bbox_to_anchor=(1.07,1.07))

    pl.xlabel('Simulation Year')
    pl.ylabel('Total Number of Dwellings (' + str(int((totalArea[' NumberDwellings'][50] - totalArea[' NumberDwellings'][0])/50)) + ') increase per year')
    pl.tick_params(axis='both', which='major', labelsize=10)
    #ax.text(0.02,0.92,'% Area where HCI >33', fontsize=8, transform=ax.transAxes)

    pl.ylim([0,None])
    pl.xlim([0,None])

    pctIncrease = (totalArea[' NumberDwellings'][50] - totalArea[' NumberDwellings'][0]) / totalArea[' NumberDwellings'][0] * 100
    fig.suptitle('FPF North -  18 March 2015 - ' + str(pctIncrease) + ' pct increase', fontsize=14, fontweight='bold')
    # pl.figtext(0.5,0.03,time.strftime("%d %B %Y"), fontsize=8)
    pdfFile.savefig()
    pl.close()

    pdfFile.close()
    print "Done."

if __name__ == '__main__':
    main()
