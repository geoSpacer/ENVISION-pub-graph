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

import numpy as np
import pandas as pd
import pylab as pl
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages
import time

def main():
    outDir = "C:\\Users\\olsenk\\Dropbox\\FPF\\Envision Runs\\keith_test\\Keith_18Mar2015_50yr\\"
    pdfFile = PdfPages(outDir + 'Dwellings.pdf')
    varName = ' NumberOfNewDwellings'

    # plot by wui
    totalArea = pd.io.parsers.read_csv(outDir + r'DwellingsInWUI_by_WUI_pivot.csv')

    fig = pl.figure(1, figsize=(11,8.5))
    ax = fig.add_subplot(1,1,1)

##        varList = list(byOwner.columns.values)
##        varList.remove('Scenario')
##        varList.remove(' Run')
##        varList.remove(' Year')
##        varList.remove(' Version')
##        varList.remove(' Timestamp')
##        varList.remove(' WUI_value')
##        varList.remove(' WUI_label')

    for wui in set(totalArea[' WUI_label']):
        byWUI = totalArea[totalArea[' WUI_label'] == wui]
        ax.plot(byWUI[' Year'], byWUI[varName], label=wui)

    # build legend
    fontP = FontProperties()
    fontP.set_size('10')
    ax.legend(prop = fontP, bbox_to_anchor=(1.07,1.07))

    pl.xlabel('Simulation Year')
    pl.ylabel('Number of New Dwellings')
    pl.tick_params(axis='both', which='major', labelsize=10)
    #ax.text(0.02,0.92,'% Area where HCI >33', fontsize=8, transform=ax.transAxes)

    pl.ylim([0,300])
    pl.xlim([0,None])

    fig.suptitle('FPF North - Current 18 March 2015' + ' - ' + varName, fontsize=14, fontweight='bold')
    # pl.figtext(0.5,0.03,time.strftime("%d %B %Y"), fontsize=8)
    pdfFile.savefig()
    pl.close()

    pdfFile.close()
    print "Done."

if __name__ == '__main__':
    main()
