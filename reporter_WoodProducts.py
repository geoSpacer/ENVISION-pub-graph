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
import pylab as pl

def main(outDir, subArea, chartTitlePre):
    varList = [' Harvest Total (m3)', ' Total Merch Harvest (m3)', ' Salvage Harvest (m3)', ' Merch Harvest Live(m3)']
    varList2 = [' Harvest Total SYU (m3)', ' Total Merch Harvest SYU (m3)', ' Salvage Harvest SYU (m3)', ' Merch Harvest Live SYU (m3)']
    yLabelText = 'Cubic Meters'

    # plot harvest volume by owner. Create additional graph for SYU only volume.
    repList = list(set(pd.io.parsers.read_csv(outDir + r'WoodProducts_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_VolumeHarvest.pdf')
        pdfFile2 = PdfPages(outDir + 'R' + str(repNum) + '_VolumeHarvest_SYU.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot total area
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        reporterFunc.plotReporter('', pdfFile, totalArea, 0, varList, subArea, chartTitle, yLabelText)
        reporterFunc.plotReporter('', pdfFile2, totalArea, 0, varList2, subArea, chartTitle, yLabelText)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter(owner, pdfFile2, byOwner, 0, varList2, subArea, chartTitle, yLabelText)

        # plot by owner detl
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_by_OWNER_DETL_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_DETL_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_DETL_label'] == owner]
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter(owner, pdfFile2, byOwner, 0, varList2, subArea, chartTitle, yLabelText)

        pdfFile.close()
        pdfFile2.close()

    # plot harvest volume by owner for Ponerosa Pine (cover type 750 - 770). Create additional graph for PP SYU only volume.
    repList = list(set(pd.io.parsers.read_csv(outDir + r'WoodProducts_pivot.csv')[' Run']))
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_VolumeHarvest_PP.pdf')
        pdfFile2 = PdfPages(outDir + 'R' + str(repNum) + '_VolumeHarvest_PP_SYU.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_PP_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]
        totalArea2 = pd.io.parsers.read_csv(outDir + r'WoodProducts_by_OWNER_pivot.csv')
        totalArea2 = totalArea2[totalArea2[' Run'] == repNum]
        totalArea3 = pd.io.parsers.read_csv(outDir + r'WoodProducts_MC_by_OWNER_pivot.csv')
        totalArea3 = totalArea3[totalArea3[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            byOwner2 = totalArea2[totalArea2[' OWNER_label'] == owner]
            byOwner3 = totalArea3[totalArea3[' OWNER_label'] == owner]

            fig = pl.figure(1, figsize=(11,8.5))
            ax = fig.add_subplot(1,1,1)

            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner2, 0, [' Total Merch Harvest (m3)'], subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner, 0, [' PP Total Merch Harvest (m3)'], subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner3, 0, [' MC Total Merch Harvest (m3)'], subArea, chartTitle, yLabelText)

            pdfFile.savefig()
            pl.close()
            fig = pl.figure(1, figsize=(11,8.5))
            ax = fig.add_subplot(1,1,1)

            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner2, 0, [' Total Merch Harvest SYU (m3)'], subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner, 0, [' PP Total Merch Harvest SYU (m3)'], subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner3, 0, [' MC Total Merch Harvest SYU (m3)'], subArea, chartTitle, yLabelText)

            pdfFile2.savefig()
            pl.close()

        pdfFile.close()
        pdfFile2.close()

    # plot volume of large trees salvage harvest
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_VolumeHarvest_LgTree_SalHarvest.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        totalArea2 = pd.io.parsers.read_csv(outDir + r'LgTreeVol_SalHarvest_by_OWNER_pivot.csv')
        totalArea2 = totalArea2[totalArea2[' Run'] == repNum]
        totalArea2['Large Tree Salvage Harv (m3)'] = totalArea2[' LgTreeVol SalHarvest Giant (m3)'] + totalArea2[' LgTreeVol SalHarvest Large (m3)'] + totalArea2[' LgTreeVol SalHarvest Medium (m3)']

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            byOwner2 = totalArea2[totalArea2[' OWNER_label'] == owner]

            fig = pl.figure(1, figsize=(11,8.5))
            ax = fig.add_subplot(1,1,1)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner, 0, [' Salvage Harvest (m3)'], subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner2, 0, ['Large Tree Salvage Harv (m3)'], subArea, chartTitle, yLabelText)

            pdfFile.savefig()
            pl.close()

        # plot by owner detl
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_by_OWNER_DETL_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        totalArea2 = pd.io.parsers.read_csv(outDir + r'LgTreeVol_SalHarvest_by_OWNER_DETL_pivot.csv')
        totalArea2 = totalArea2[totalArea2[' Run'] == repNum]
        totalArea2['Large Tree Salvage Harv (m3)'] = totalArea2[' LgTreeVol SalHarvest Giant (m3)'] + totalArea2[' LgTreeVol SalHarvest Large (m3)'] + totalArea2[' LgTreeVol SalHarvest Medium (m3)']

        ownerNames = list(set(totalArea[' OWNER_DETL_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_DETL_label'] == owner]
            byOwner2 = totalArea2[totalArea2[' OWNER_DETL_label'] == owner]

            fig = pl.figure(1, figsize=(11,8.5))
            ax = fig.add_subplot(1,1,1)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner, 0, [' Salvage Harvest (m3)'], subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner2, 0, ['Large Tree Salvage Harv (m3)'], subArea, chartTitle, yLabelText)

            pdfFile.savefig()
            pl.close()

        pdfFile.close()

    # plot volume of large trees merch harv live
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_VolumeHarvest_LgTree_MerchHarvLive.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        totalArea2 = pd.io.parsers.read_csv(outDir + r'LgTreeVol_MerchHarvLive_D3_D55_by_OWNER_pivot.csv')
        totalArea2 = totalArea2[totalArea2[' Run'] == repNum]
        totalArea2['Lg Tree MerchHarvLive D55 (m3)'] = totalArea2[' LgTreeVol MerchHarvLive D55_1 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D55_2 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D55_3 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D55_4 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D55_5 (m3)']
        totalArea2['Lg Tree MerchHarvLive D3 (m3)'] = totalArea2[' LgTreeVol MerchHarvLive D3_1 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D3_2 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D3_3 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D3_4 (m3)']

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            byOwner2 = totalArea2[totalArea2[' OWNER_label'] == owner]

            fig = pl.figure(1, figsize=(11,8.5))
            ax = fig.add_subplot(1,1,1)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner, 0, [' Merch Harvest Live(m3)'], subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner2, 0, ['Lg Tree MerchHarvLive D55 (m3)'], subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner2, 0, ['Lg Tree MerchHarvLive D3 (m3)'], subArea, chartTitle, yLabelText)

            pdfFile.savefig()
            pl.close()

        # plot by owner detl
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_by_OWNER_DETL_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        totalArea2 = pd.io.parsers.read_csv(outDir + r'LgTreeVol_MerchHarvLive_D3_D55_by_OWNER_DETL_pivot.csv')
        totalArea2 = totalArea2[totalArea2[' Run'] == repNum]
        totalArea2['Lg Tree MerchHarvLive D55 (m3)'] = totalArea2[' LgTreeVol MerchHarvLive D55_1 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D55_2 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D55_3 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D55_4 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D55_5 (m3)']
        totalArea2['Lg Tree MerchHarvLive D3 (m3)'] = totalArea2[' LgTreeVol MerchHarvLive D3_1 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D3_2 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D3_3 (m3)'] + totalArea2[' LgTreeVol MerchHarvLive D3_4 (m3)']

        ownerNames = list(set(totalArea[' OWNER_DETL_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_DETL_label'] == owner]
            byOwner2 = totalArea2[totalArea2[' OWNER_DETL_label'] == owner]

            fig = pl.figure(1, figsize=(11,8.5))
            ax = fig.add_subplot(1,1,1)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner, 0, [' Merch Harvest Live(m3)'], subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner2, 0, ['Lg Tree MerchHarvLive D55 (m3)'], subArea, chartTitle, yLabelText)
            reporterFunc.plotReporter_partial(fig, ax, owner, byOwner2, 0, ['Lg Tree MerchHarvLive D3 (m3)'], subArea, chartTitle, yLabelText)

            pdfFile.savefig()
            pl.close()

        pdfFile.close()

    varList = [' Saw Timber Total (m3)']
    for repNum in repList:
        pdfFile = PdfPages(outDir + 'R' + str(repNum) + '_VolumeStanding.pdf')
        chartTitle = chartTitlePre + ' - R' + str(repNum)

        # plot total area
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        reporterFunc.plotReporter('', pdfFile, totalArea, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_by_OWNER_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_label'] == owner]
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

        # plot by owner detl
        totalArea = pd.io.parsers.read_csv(outDir + r'WoodProducts_by_OWNER_DETL_pivot.csv')
        totalArea = totalArea[totalArea[' Run'] == repNum]

        ownerNames = list(set(totalArea[' OWNER_DETL_label']))
        ownerNames.sort()
        for owner in ownerNames:
            byOwner = totalArea[totalArea[' OWNER_DETL_label'] == owner]
            reporterFunc.plotReporter(owner, pdfFile, byOwner, 0, varList, subArea, chartTitle, yLabelText)

        pdfFile.close()

        print "Done."

if __name__ == '__main__':
        # Test for correct number of arguments
    if len(sys.argv) != 4:
        print "Usage: reporter_.py <outDir> <subArea> <chartTitle>"
        sys.exit(1)

    try:
        main(sys.argv[1], sys.argv[2], sys.argv[3])

    except Exception, e:
        print "\n\n" + sys.argv[1] + ": " + e.args[0]

    except:
        print "unhandled Error!!"
