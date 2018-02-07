#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Keith Olsen
#
# Created:     01/12/2014
# updated: 21 January 2018
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import numpy as np
import pandas as pd
import pylab as pl
from matplotlib.font_manager import FontProperties
import time

def plotReporter(strata, pdfFile, plotData, totalHa, varList, subArea, chartTitle, yLabelText):
    fig = pl.figure(1, figsize=(11,8.5))
    ax = fig.add_subplot(1,1,1)

    for varName in varList:
        if varName[:1] == ' ':
            labelName = varName[1:]
        else:
            labelName = varName

        lineWidthVal = 1.0
        if 'Giant' in varName or 'Woodpecker' in varName or 'Partial' in varName:
            lineWidthVal = 2.0

        if 'LargeGiantOpen' in varName or varName == ' Partial Harvest (ha)':
            pl.gca().set_color_cycle(None)

        if totalHa > 0:
            if 'Fire' in varName or 'fire' in varName:
                ax.plot(plotData[' Year'], plotData[varName] / totalHa * 100, label=labelName, c=getColor(varName), lw=lineWidthVal)
            else:
                ax.plot(plotData[' Year'], plotData[varName] / totalHa * 100, label=labelName, lw=lineWidthVal)
        else:
            if 'Fire' in varName or 'fire' in varName:
                ax.plot(plotData[' Year'], plotData[varName], label=labelName, c=getColor(varName), lw=lineWidthVal)
            else:
                ax.plot(plotData[' Year'], plotData[varName], label=labelName, lw=lineWidthVal)


    # build legend
    fontP = FontProperties()
    fontP.set_size('10')
    ax.legend(prop = fontP, bbox_to_anchor=(1.07,1.07))

    pl.xlabel('Simulation Year')
    pl.ylabel(yLabelText)
    pl.tick_params(axis='both', which='major', labelsize=10)
    #ax.text(0.02,0.92,'% Area where HCI >33', fontsize=8, transform=ax.transAxes)

    # pl.ylim([0,None])
    # pl.xlim([0,None])

    if strata == '':
        fig.suptitle('FPF ' + subArea + ' - ' + plotData['Scenario'].iloc[0] + ' - ' + chartTitle, fontsize=14, fontweight='bold')
    else:
        fig.suptitle('FPF ' + subArea + ' - ' + plotData['Scenario'].iloc[0] + ' - ' + chartTitle + ' - ' + strata, fontsize=14, fontweight='bold')

    # pl.figtext(0.5,0.03,time.strftime("%d %B %Y"), fontsize=8)
    pdfFile.savefig()
    pl.close()

def plotReporter_partial(fig, ax, strata, plotData, totalHa, varList, subArea, chartTitle, yLabelText):
    for varName in varList:
        if varName[:1] == ' ':
            labelName = varName[1:]
        else:
            labelName = varName

        lineWidthVal = 1.0
        if 'Giant' in varName or 'Woodpecker' in varName or 'Partial' in varName:
            lineWidthVal = 2.0

        if 'LargeGiantOpen' in varName or varName == ' Partial Harvest (ha)':
            pl.gca().set_color_cycle(None)

        if totalHa > 0:
            if 'Fire' in varName or 'fire' in varName:
                ax.plot(plotData[' Year'], plotData[varName] / totalHa * 100, label=labelName, c=getColor(varName), lw=lineWidthVal)
            else:
                ax.plot(plotData[' Year'], plotData[varName] / totalHa * 100, label=labelName, lw=lineWidthVal)
        else:
            if 'Fire' in varName or 'fire' in varName:
                ax.plot(plotData[' Year'], plotData[varName], label=labelName, c=getColor(varName), lw=lineWidthVal)
            else:
                ax.plot(plotData[' Year'], plotData[varName], label=labelName, lw=lineWidthVal)


    # build legend
    fontP = FontProperties()
    fontP.set_size('10')
    ax.legend(prop = fontP, bbox_to_anchor=(1.07,1.07))

    pl.xlabel('Simulation Year')
    pl.ylabel(yLabelText)
    pl.tick_params(axis='both', which='major', labelsize=10)
    #ax.text(0.02,0.92,'% Area where HCI >33', fontsize=8, transform=ax.transAxes)

    # pl.ylim([0,None])
    # pl.xlim([0,None])

    if strata == '':
        fig.suptitle('FPF ' + subArea + ' - ' + plotData['Scenario'].iloc[0] + ' - ' + chartTitle, fontsize=14, fontweight='bold')
    else:
        fig.suptitle('FPF ' + subArea + ' - ' + plotData['Scenario'].iloc[0] + ' - ' + chartTitle + ' - ' + strata, fontsize=14, fontweight='bold')

    # pl.figtext(0.5,0.03,time.strftime("%d %B %Y"), fontsize=8)

def plotReporter_compare(strata, pdfFile, plotData, plotData2, totalHa, varList, subArea, chartTitle, yLabelText):
    fig = pl.figure(1, figsize=(11,8.5))
    ax = fig.add_subplot(1,1,1)

    # plot default run
    for varName in varList:
        if varName[:1] == ' ':
            labelName = varName[1:]
        else:
            labelName = varName

        lineWidthVal = 1.0
        if 'Giant' in varName or 'Woodpecker' in varName or 'Partial' in varName:
            lineWidthVal = 2.0

        if 'LargeGiantOpen' in varName or varName == ' Partial Harvest (ha)':
            pl.gca().set_color_cycle(None)

        if totalHa > 0:
            if 'Fire' in varName or 'fire' in varName:
                ax.plot(plotData[' Year'], plotData[varName] / totalHa * 100, label=labelName, c=getColor(varName), lw=lineWidthVal)
            else:
                ax.plot(plotData[' Year'], plotData[varName] / totalHa * 100, label=labelName, lw=lineWidthVal)
        else:
            if 'Fire' in varName or 'fire' in varName:
                ax.plot(plotData[' Year'], plotData[varName], label=labelName, c=getColor(varName), lw=lineWidthVal)
            else:
                ax.plot(plotData[' Year'], plotData[varName], label=labelName, lw=lineWidthVal)

    # plot run to compare
    for varName in varList:
        if varName[:1] == ' ':
            labelName = varName[1:] + ' 0923'
        else:
            labelName = varName + ' 0923'

        lineWidthVal = 1.0
        if 'Giant' in varName or 'Woodpecker' in varName or 'Partial' in varName:
            lineWidthVal = 2.0

        if 'LargeGiantOpen' in varName or varName == ' Partial Harvest (ha)':
            pl.gca().set_color_cycle(None)

        if totalHa > 0:
            if 'Fire' in varName or 'fire' in varName:
                ax.plot(plotData[' Year'], plotData2[varName] / totalHa * 100, label=labelName, c=getColor(varName), lw=lineWidthVal)
            else:
                ax.plot(plotData[' Year'], plotData2[varName] / totalHa * 100, label=labelName, lw=lineWidthVal)
        else:
            if 'Fire' in varName or 'fire' in varName:
                ax.plot(plotData[' Year'], plotData2[varName], label=labelName, c=getColor(varName), lw=lineWidthVal)
            else:
                ax.plot(plotData[' Year'], plotData2[varName], label=labelName, lw=lineWidthVal)

    # build legend
    fontP = FontProperties()
    fontP.set_size('10')
    ax.legend(prop = fontP, bbox_to_anchor=(1.07,1.07))

    pl.xlabel('Simulation Year')
    pl.ylabel(yLabelText)
    pl.tick_params(axis='both', which='major', labelsize=10)
    #ax.text(0.02,0.92,'% Area where HCI >33', fontsize=8, transform=ax.transAxes)

    # pl.ylim([0,None])
    # pl.xlim([0,None])

    if strata == '':
        fig.suptitle('FPF ' + subArea + ' - ' + plotData['Scenario'].iloc[0] + ' - ' + chartTitle, fontsize=14, fontweight='bold')
    else:
        fig.suptitle('FPF ' + subArea + ' - ' + plotData['Scenario'].iloc[0] + ' - ' + chartTitle + ' - ' + strata, fontsize=14, fontweight='bold')

    # pl.figtext(0.5,0.03,time.strftime("%d %B %Y"), fontsize=8)
    pdfFile.savefig()
    pl.close()

def plotReporter2(fig, ax, strata, pdfFile, plotData, varList, subArea, chartTitle, yLabelText, scenario):
    if scenario == 'CurrentPolicy':
        colorVal = 'k'
        labelName = 'Current Policy'
    elif scenario == 'NoFedTreat':
        colorVal = 'r'
        labelName = 'No Federal Treatment'
    elif scenario == 'Restoration':
        colorVal = 'c'
        labelName = 'Restoration'
    elif scenario == 'NoFireNoMgmt':
        colorVal = 'm'
        labelName = 'No Fire No Treatment'

    for varName in varList:
        lineWidthVal = 2.0
        lineStyleVal = '-'

        if varName == 'lower' or varName == 'upper':
            lineStyleVal = '--'
            lineWidthVal = 1.0
            labelName = ''

        ax.plot(plotData['timeStep'], plotData[varName], label=labelName, lw=lineWidthVal, linestyle=lineStyleVal, c=colorVal)

    # build legend
    fontP = FontProperties()
    fontP.set_size('10')

    if 'Carbon' in yLabelText or 'Owl' in yLabelText or 'Forest Structure' in yLabelText:
        ax.legend(prop = fontP, bbox_to_anchor=(0.26,0.99))
    else:
        ax.legend(prop = fontP, bbox_to_anchor=(0.99,0.99))

    pl.xlabel('Simulation Year')
    pl.ylabel(yLabelText)
    pl.tick_params(axis='both', which='major', labelsize=10)
    #ax.text(0.02,0.92,'% Area where HCI >33', fontsize=8, transform=ax.transAxes)

    # pl.ylim([0,None])
    # pl.xlim([0,None])

    if strata == '':
        fig.suptitle('FPF ' + subArea + ' - ' + chartTitle, fontsize=14, fontweight='bold')
    elif scenario == 'CurrentPolicy':
        fig.suptitle('FPF ' + subArea + ' - ' + chartTitle + ' - ' + strata, fontsize=14, fontweight='bold')


def plotReporter3(fig, ax, strata, pdfFile, plotData, varList, subArea, chartTitle, yLabelText, scenario, maxValueList):
    if scenario == 'CurrentPolicy':
        colorVal = 'k'
        labelName = 'Current Policy'
    elif scenario == 'NoFedTreat':
        colorVal = 'r'
        labelName = 'No Federal Treatment'
    elif scenario == 'Restoration':
        colorVal = 'c'
        labelName = 'Restoration'
    elif scenario == 'NoFireNoMgmt':
        colorVal = 'g'
        labelName = 'No Fire No Treatment'

    ax.boxplot(plotData, whis=100.0)
    ax.set_xticklabels(varList)

    # build legend
##    fontP = FontProperties()
##    fontP.set_size('10')
##    ax.legend(prop = fontP, bbox_to_anchor=(1.07,1.07))

##    pl.xlabel('Simulation Year')
    pl.ylabel(yLabelText)
##    pl.tick_params(axis='both', which='major', labelsize=10)

##    ax.text(0.8, 0.45,'{:.2f}'.format(maxValueList[0]), fontsize=8)
##    ax.text(1.8, 0.45,'{:.2f}'.format(maxValueList[1]), fontsize=8)
##    ax.text(2.8, 0.45,'{:.2f}'.format(maxValueList[2]), fontsize=8)

    #pl.ylim([0,None])
    # pl.xlim([0,None])

    if strata == '':
        fig.suptitle('FPF ' + subArea + ' - ' + chartTitle, fontsize=14, fontweight='bold')
    elif scenario == 'CurrentPolicy':
        fig.suptitle('FPF ' + subArea + ' - ' + chartTitle + ' - ' + strata, fontsize=14, fontweight='bold')


def plotReporter4(fig, ax, strata, pdfFile, plotData, varList, xLabelText, yLabelText, scenario, labelXtick, labelYtick, plotLegend, figText):
    # lookup scenario color and labels
    scenarioLabelList = getScenarioLabels(scenario)
    colorVal = scenarioLabelList[0]
    labelName = scenarioLabelList[1]
    labelNameShort = scenarioLabelList[2]

    if 'HarvVol' in scenario:
        scenarioLabelList = getScenarioLabels(figText)
        figText = scenarioLabelList[1]

    figTextList = ['Northern Spotted Owl\n(nest)','Pacific Marten','Black-backed WP','White-headed WP','Northern Goshawk\n(nest)','Western Bluebird','Pileated WP','Mule Deer','Cheatgrass']

    for varName in varList:
        lineWidthVal = 1.5
        lineStyleVal = '-'

        if varName == 'lower' or varName == 'upper':
            lineStyleVal = '--'
            lineWidthVal = 0.5
            labelName = labelNameShort = ''

        if figText in figTextList: labelName = labelNameShort
        ax.plot(plotData['timeStep'], plotData[varName], label=labelName, lw=lineWidthVal, linestyle=lineStyleVal, c=colorVal)

    # for wildlife data
    if figText in figTextList:
        pl.subplots_adjust(hspace=0.08,wspace=0.25)
        legendSize = '5.5'
    else:
        pl.subplots_adjust(hspace=0.05,wspace=0.15)
        legendSize = '7'

    if plotLegend != (-99,-99):
        # build legend
        fontP = FontProperties()
        fontP.set_size(legendSize)
        lg = ax.legend(prop = fontP, bbox_to_anchor=plotLegend)
        lg.draw_frame(False)

    pl.xlabel(xLabelText,fontsize=10)
    pl.ylabel(yLabelText,fontsize=10)

    if labelXtick:
        pl.tick_params(axis='x', which='major', labelsize=8)
    else:
        ax.set_xticklabels([])

    if labelYtick:
        pl.tick_params(axis='y', which='major', labelsize=8)
    else:
        pl.subplots_adjust(hspace=0.05,wspace=0.07)
        ax.set_yticklabels([])

    if len(figText) > 1:
        if figText == 'Northern Goshawk\n(nest)':
            ax.text(0.05,0.9, figText, fontsize=8, transform=ax.transAxes)
        elif figText == 'Northern Spotted Owl\n(nest)':
            ax.text(0.5,0.9, figText, fontsize=8, transform=ax.transAxes)
        else:
            ax.text(0.05,0.92, figText, fontsize=8, transform=ax.transAxes)

    else:
        ax.text(0.03,0.91, figText, fontsize=14, transform=ax.transAxes)

    #ax.text(0.02,0.92,'% Area where HCI >33', fontsize=8, transform=ax.transAxes)

    if figText in ['Early successional']:
        pl.ylim([0,50])
    elif figText in ['Pole and small']:
        pl.ylim([0,50])
    elif figText in ['Medium']:
        pl.ylim([0,50])
    elif figText in ['Large and giant']:
        pl.ylim([0,50])
    elif figText in ['Open canopy','Closed canopy']:
        pl.ylim([0,50])
    elif figText in ['High resilience','Low resilience']:
        pl.ylim([0,50])

    # set chart title
    pl.figtext(0.25,0.92,'DRAFT Research Scenarios - Oregon State University - ' + time.strftime("%d %B %Y"), fontsize=5)

    # pl.xlim([0,None])
    return(ax.get_ylim())


def plotReporter4bw(fig, ax, strata, pdfFile, plotData, varList, subArea, chartTitle, yLabelText, maxValueList, labelXaxis, figText):

    yLimMax = 0
    widthsList = []
    for scenario in plotData:
        yLimMax = max(yLimMax, np.percentile(scenario, 75))
        widthsList.append(0.65)
    yLimMax *= 1.2

    if yLimMax == 0:
        yLimMax = max(maxValueList) * 1.2

    ax.boxplot(plotData, whis=100.0, widths=widthsList)
    pl.subplots_adjust(hspace=0.05)

    if labelXaxis:
        ax.set_xticklabels(varList,fontsize=8)
    else:
        ax.set_xticklabels([])

    # build legend
##    fontP = FontProperties()
##    fontP.set_size('10')
##    ax.legend(prop = fontP, bbox_to_anchor=(1.07,1.07))

##    pl.xlabel('Simulation Year')
    pl.ylabel(yLabelText,fontsize=8)
    pl.tick_params(axis='y', which='major', labelsize=8)
    pl.ylim([0,yLimMax])

    if figText == 'a' or figText == 'A':
        # print max value text at top of box and whiskar plot
        for i in range(len(varList)):
            if maxValueList[i] > 1000:
                ax.text(i + 0.73, yLimMax - (yLimMax * 0.06),'Max = {:.0f}'.format(maxValueList[i]), fontsize=8)
            else:
                ax.text(i + 0.73, yLimMax - (yLimMax * 0.06),'Max = {:.2f}'.format(maxValueList[i]), fontsize=8)

    ax.text(0.03,0.91, figText, fontsize=14, transform=ax.transAxes)


def plotReporter5(fig, ax, strata, pdfFile, plotData, varList, xLabelText, yLabelText, owner, labelXtick, labelYtick, plotLegend, figText):
    if owner == 'USFS' or 'Chemult' in owner or 'JWTR' in owner or 'Sun' in owner:
        colorVal = 'k'
    elif owner == 'State' or 'Chiloquin' in owner or 'Jeld' in owner or 'Gil' in owner:
        colorVal = 'r'
    elif owner == 'Corporate Forest' or 'Klamath' in owner or 'Spear' in owner:
        colorVal = 'deepskyblue'
    else:
        colorVal = 'mediumpurple'

    if '(Fremont-Winema NF)' in owner:
        labelName = owner[:-24]
##    elif 'Cascade Timberlands' in owner:
##        labelName = owner[21:-1]
    elif 'JWTR' in owner:
        labelName = 'PC1'
    elif 'Mazama' in owner:
        labelName = 'PC2'
    elif 'Jeld' in owner:
        labelName = 'PC3'
    elif 'Spear' in owner:
        labelName = 'PC4'
    elif 'Collins' in owner:
        labelName = 'PC5'
    else:
        labelName = owner

    for varName in varList:
        lineWidthVal = 1.5
        lineStyleVal = '-'

        if varName == 'lower' or varName == 'upper':
            lineStyleVal = '--'
            lineWidthVal = 0.5
            labelName = ''

        ax.plot(plotData['timeStep'], plotData[varName], label=labelName, lw=lineWidthVal, linestyle=lineStyleVal, c=colorVal)

    if plotLegend != (-99,-99):
        # build legend
        fontP = FontProperties()
        fontP.set_size('8')
        lg = ax.legend(prop = fontP, bbox_to_anchor=plotLegend)
        lg.draw_frame(False)

    pl.xlabel(xLabelText,fontsize=10)
    pl.ylabel(yLabelText,fontsize=10)

    # for wildlife data
    figTextList = ['Northern Spotted Owl\n(nest)','Pacific Marten','Black-backed WP','White-headed WP','Northern Goshawk\n(nest)','Western Bluebird','Pileated WP','Mule Deer','Cheatgrass']
    if figText in figTextList:
        pl.subplots_adjust(hspace=0.08,wspace=0.25)
    else:
        pl.subplots_adjust(hspace=0.05,wspace=0.15)


    if labelXtick:
        pl.tick_params(axis='x', which='major', labelsize=8)
    else:
        ax.set_xticklabels([])

    if labelYtick:
        pl.tick_params(axis='y', which='major', labelsize=8)
    else:
        pl.subplots_adjust(hspace=0.05,wspace=0.07)
        ax.set_yticklabels([])

    if len(figText) > 1:
        if figText == 'Pole and small':
            ax.text(0.05,0.72, figText, fontsize=10, transform=ax.transAxes)
        elif figText == 'Northern Spotted Owl\n(nest)' or figText == 'Northern Goshawk\n(nest)':
            ax.text(0.05,0.85, figText, fontsize=8, transform=ax.transAxes)
        else:
            ax.text(0.05,0.92, figText, fontsize=8, transform=ax.transAxes)

    else:
        ax.text(0.03,0.91, figText, fontsize=14, transform=ax.transAxes)


    # pl.ylim([0,None])
    # pl.xlim([0,None])

##    if strata == '':
##        fig.suptitle('FPF ' + subArea + ' - ' + chartTitle, fontsize=14, fontweight='bold')
##    elif scenario == 'CurrentPolicy':
##        fig.suptitle('FPF ' + subArea + ' - ' + chartTitle + ' - ' + strata, fontsize=14, fontweight='bold')
##    pl.figtext(0.5,0.03,yLabelText, fontsize=8)


def plotReporter5bw(fig, ax, strata, pdfFile, plotData, varList, subArea, chartTitle, yLabelText, maxValueList, labelXaxis, figText):

    yLimMax = 0
    widthsList = []
    for scenario in plotData:
        yLimMax = max(yLimMax, np.percentile(scenario, 75))
        widthsList.append(0.65)
    yLimMax *= 1.5

    if yLimMax == 0:
        yLimMax = max(maxValueList) * 1.2

    yLimMax = 10

    ax.boxplot(plotData, whis=100.0, widths=widthsList)
    pl.subplots_adjust(hspace=0.13, wspace=0.05)

    if labelXaxis:
        ax.set_xticklabels(varList,fontsize=8)
    else:
        ax.set_xticklabels([])

    # build legend
##    fontP = FontProperties()
##    fontP.set_size('10')
##    ax.legend(prop = fontP, bbox_to_anchor=(1.07,1.07))

##    pl.xlabel('Simulation Year')
    pl.ylabel(yLabelText,fontsize=8)

    if figText == 'a' or figText == 'c':
        pl.tick_params(axis='y', which='major', labelsize=8)
    else:
        ax.set_yticklabels([])

    pl.ylim([0,yLimMax])

#    if figText == 'a':
        # print max value text at top of box and whiskar plot
    for i in range(len(varList)):
        if maxValueList[i] > 1000:
            ax.text(i + 0.73, yLimMax - (yLimMax * 0.06),'Max\n{:.0f}'.format(maxValueList[i]), fontsize=6.5)
        else:
            ax.text(i + 1.04, yLimMax - (yLimMax * 0.1),'Max\n{:.2f}'.format(maxValueList[i]), fontsize=6.5)

    ax.text(0.03,0.91, figText, fontsize=14, transform=ax.transAxes)


def plotReporter5bar(fig, ax, strata, pdfFile, plotDataFrame, varList, yLabelText, ownership, labelYaxis):

    plotData = list(plotDataFrame[0])

    if 'Fremont-Winema NF' in ownership:
        ownership = ownership[:-35]
    elif 'JWTR' in ownership:
        ownership = 'PC1'
    elif 'Mazama' in ownership:
        ownership = 'PC2'
    elif 'Jeld' in ownership:
        ownership = 'PC3'
    elif 'Spear' in ownership:
        ownership = 'PC4'
    elif 'Collins' in ownership:
        ownership = 'PC5'
    elif 'Corporate' in ownership:
        ownership = 'Corporate'

    ind = np.arange(len(plotData))
    width = 0.35

    # reverse order of items to plot
##    plotData.reverse()
##    varListReverse = varList[::-1]

    ax.barh(ind, plotData, color=plotDataFrame.positives.map({True: 'b', False: 'r'}))

    pl.subplots_adjust(wspace = 0.25, hspace = 0.10, left = 0.2)
    pl.tick_params(axis='x', which='major', labelsize=7.5)
    pl.tick_params(axis='y', which='major', labelsize=9)
    pl.locator_params(axis='x', nbins=5)

    # remove the last label on the x axis
##    labels = [item.get_text() for item in ax.get_xticklabels()]
##    labels[-1] = ''
##    ax.set_xticklabels(labels)

    if labelYaxis:
        ax.set(yticks=np.arange(len(plotData)+1) + width, yticklabels=varList + [''], ylim=[2*width - 1, len(plotData)+1])
    else:
        ax.set(yticks=np.arange(len(plotData)+1) + width, yticklabels=[], ylim=[2*width - 1, len(plotData)+1])

    ax.text(0.5,0.92, ownership, horizontalalignment='center', transform=ax.transAxes, fontsize=9)

def plotReporter6_points(fig, ax, strata, pdfFile, plotList, runList, yLabelText):

    xLabelList = ['']
    for scenario in runList:
        # lookup scenario color and labels
        scenarioLabelList = getScenarioLabels(scenario)
        colorVal = scenarioLabelList[0]
        labelName = scenarioLabelList[1]
        labelNameShort = scenarioLabelList[2]
        if (runList.index(scenario) % 2) == 0:
            xLabelList.append(labelNameShort)
        else:
            xLabelList.append("\n" + labelNameShort)

    ax.plot(plotList, 'ks')
    ax.set_xlim(-1,len(plotList))
    mnAxis, mxAxis = ax.get_ylim()
    ax.set_ylim(mnAxis-1, mxAxis+1)

#    pl.xlabel(xLabelText,fontsize=10)
    pl.ylabel(yLabelText,fontsize=10)

    ax.set_xticklabels(xLabelList)
    pl.tick_params(axis='x', which='major', labelsize=6)
    pl.tick_params(axis='y', which='major', labelsize=8)

def plotReporter6_bw(fig, ax, strata, pdfFile, plotList, runList, yLabelText):

    xLabelList = []
    for scenario in runList:
        # lookup scenario color and labels
        scenarioLabelList = getScenarioLabels(scenario)
        colorVal = scenarioLabelList[0]
        labelName = scenarioLabelList[1]
        labelNameShort = scenarioLabelList[2]
        if (runList.index(scenario) % 2) == 0:
            xLabelList.append(labelNameShort)
        else:
            xLabelList.append("\n" + labelNameShort)

    ax.boxplot(plotList)
#    ax.set_xlim(-1,len(plotList))
#    mnAxis, mxAxis = ax.get_ylim()
#    ax.set_ylim(mnAxis-1, mxAxis+1)

#    pl.xlabel(xLabelText,fontsize=10)
    pl.ylabel(yLabelText,fontsize=10)

    ax.set_xticklabels(xLabelList)
    pl.tick_params(axis='x', which='major', labelsize=6)
    pl.tick_params(axis='y', which='major', labelsize=8)

def plotReporter6_bar(fig, ax, strata, pdfFile, plotList, runList, yLabelText):

    xLabelList = []
    for scenario in runList:
        # lookup scenario color and labels
        scenarioLabelList = getScenarioLabels(scenario)
        colorVal = scenarioLabelList[0]
        labelName = scenarioLabelList[1]
        labelNameShort = scenarioLabelList[2]
        if (runList.index(scenario) % 2) == 0:
            xLabelList.append(labelNameShort)
        else:
            xLabelList.append("\n" + labelNameShort)

    y_pos = np.arange(len(xLabelList))
    ax.bar(y_pos, plotList, align='center', alpha=0.5)
#    ax.set_xlim(-1,len(plotList))
#    mnAxis, mxAxis = ax.get_ylim()
#    ax.set_ylim(mnAxis-1, mxAxis+1)

#    pl.xlabel(xLabelText,fontsize=10)
    pl.ylabel(yLabelText,fontsize=10)

    ax.set_xticklabels([''] + xLabelList)
    pl.tick_params(axis='x', which='major', labelsize=6)
    pl.tick_params(axis='y', which='major', labelsize=8)

    mnAxis, mxAxis = ax.get_ylim()
    ax.set_ylim(mnAxis, mxAxis)

def plotSecondYAxis(ax2, yLabelText, mnAxis, mxAxis):
    ax2.set_ylim(mnAxis, mxAxis)
    ax2.set_ylabel(yLabelText,fontsize=10)
    ax2.tick_params(axis='y', which='major', labelsize=8)

def plotFigureText(fig, xLabelText, yLabelText):

    big_ax = fig.add_subplot(111)
    big_ax.set_axis_bgcolor('none')
    big_ax.tick_params(labelcolor='none', top='off', bottom='off', left='off', right='off')
    for pos in ['top', 'bottom', 'right', 'left']:
        big_ax.spines[pos].set_edgecolor('none')

    pl.xlabel(xLabelText, fontsize=10)
    pl.ylabel(yLabelText, fontsize=10)

def getColor(varName):
    if 'fire in NSO SS' in varName:
        return('k')
    elif 'Stand' in varName or 'stand' in varName:
        return('r')
    elif 'High' in varName:
        return('r')
    elif 'Mixed' in varName or 'mixSev' in varName:
        return('b')
    elif 'Surface' in varName or 'surface' in varName:
        return('c')
    else:
        return('k')

##def getOwnerHa(subArea):
##    if subArea == 'North':
##        return({'Federal' : 762299, 'State' : 30022, 'Private Non-Industrial' : 46356, 'Private Industrial' : 59036, 'Tribal' : 257943, 'Homeowner' : 93667})
##    elif subArea == 'Southwest':
##        return({'Federal' : 519482, 'State' : 18434, 'Private Non-Industrial' : 103286, 'Private Industrial' : 202550, 'Tribal' : 96, 'Homeowner' : 176962,
##                'BLM Lands' : 48081,'Chemult Ranger District (Fremont-Winema NF)' : 160302,'Chiloquin Ranger District (Fremont-Winema NF)' : 187158,
##                'Klamath Ranger District (Fremont-Winema NF)' : 75952,'ODF Sun Pass' : 8703,'ODF Gilchrist' : 2369,'ODF Gilchrist (The Conservation Fund)' : 2952,
##                'JWTR Timber Holdings' : 140054,'Cascade Timberlands (Mazama Forest)' : 36826,'Jeld-Wen Inc' : 18944,'J-Spear Ranch' : 3692})
##    elif subArea == 'Southeast':
##        return({'Federal' : 625626, 'State' : 6505, 'Private Non-Industrial' : 133739, 'Private Industrial' : 165072, 'Tribal' : 0, 'Homeowner' : 129381})
##
##def getOwnerForestedHa(subArea):
##    if subArea == 'North':
##        return({'Federal' : 620388, 'State' : 28762, 'Private Non-Industrial' : 30960, 'Private Industrial' : 57046, 'Tribal' : 147606, 'Homeowner' : 5390})
##    elif subArea == 'Bend30K':
##        return({'Federal' : 53158, 'State' : 67, 'Private Non-Industrial' : 8761, 'Private Industrial' : 13097, 'Tribal' : 0, 'Homeowner' : 747})
##    elif subArea == 'Southwest':
##        return({'Federal' : 477664, 'State' : 17400, 'Private Non-Industrial' : 54082, 'Private Industrial' : 188437, 'Tribal' : 0, 'Other' : 33540, 'Homeowner' : 7001,
##                'BLM Lands' : 30433,'Chemult Ranger District (Fremont-Winema NF)' : 155949,'Chiloquin Ranger District (Fremont-Winema NF)' : 175802,
##                'Klamath Ranger District (Fremont-Winema NF)' : 72005,'ODF Sun Pass' : 8213,'ODF Gilchrist' : 2353,'ODF Gilchrist (The Conservation Fund)' : 2952,
##                'JWTR Timber Holdings' : 133334,'Cascade Timberlands (Mazama Forest)' : 34139,'Jeld-Wen Inc' : 14725,'J-Spear Ranch' : 3641})
##    elif subArea == 'Southeast':
##        return({'Federal' : 464998, 'State' : 5540, 'Private Non-Industrial' : 57577, 'Private Industrial' : 152965, 'Tribal' : 0, 'Homeowner' : 3594})
##
def getPVTHa(subArea):
    if subArea == 'North':
        return([115980, 186616, 93516, 157296, 304383, 157491, 139271])
    elif subArea == 'Bend30K':
        return([2119, 15594, 2629, 8801, 16910, 33378, 11373])
    elif subArea == 'Southwest':
        return([8008, 118078, 81685, 135647, 337025, 108504, 88038])
    elif subArea == 'Southeast':
        return([35973, 19942, 19243, 35535, 407078, 203536, 250387])
    elif subArea == 'South':
        return([42844, 129457, 92847, 158195, 701917, 294820, 314068])

##def getPMG1Ha(subArea):
##    if subArea == 'North':
##        return({'Federal':133700, 'State':0, 'Private Non-Industrial':801, 'Private Industrial':284, 'Tribal':51818, 'Homeowner':12})
##
##def getPMG2Ha(subArea):
##    if subArea == 'North':
##        return({'Federal':421425, 'State':22622, 'Private Non-Industrial':23307, 'Private Industrial':51867, 'Tribal':96620, 'Homeowner':3176})
##
##def getPMG345Ha(subArea):
##    if subArea == 'North':
##        return({'Federal':421425, 'State':22622, 'Private Non-Industrial':23307, 'Private Industrial':51867, 'Tribal':96620, 'Homeowner':3176})
##    elif subArea == 'Southwest':
##        return({'Federal':336675, 'State':15101, 'Private Non-Industrial':48366, 'Private Industrial':148056, 'Tribal':0, 'Homeowner':6412,
##                'BLM Lands' : 27353,'Chemult Ranger District (Fremont-Winema NF)' : 102681,'Chiloquin Ranger District (Fremont-Winema NF)' : 165141,
##                'Klamath Ranger District (Fremont-Winema NF)' : 25700,'ODF Sun Pass' : 7323,'ODF Gilchrist' : 1574,'ODF Gilchrist (The Conservation Fund)' : 2749,
##                'JWTR Timber Holdings' : 120491,'Cascade Timberlands (Mazama Forest)' : 9552,'Jeld-Wen Inc' : 14717,'J-Spear Ranch' : 3446})
##    elif subArea == 'Southeast':
##        return({'Federal':430957, 'State':5306, 'Private Non-Industrial':56826, 'Private Industrial':149347, 'Tribal':0, 'Homeowner':3500})
##
##def getPMG12345Ha(subArea):
##    if subArea == 'North':
##        return({'Federal':628529, 'State':28762, 'Private Non-Industrial':30960, 'Private Industrial':57046, 'Tribal':148438, 'Homeowner':5390})
##    elif subArea == 'Southwest':
##        return({'Federal':478371, 'State':17400, 'Private Non-Industrial':54082, 'Private Industrial':188442, 'Tribal':0, 'Homeowner':7001,
##                'BLM Lands' : 30435,'Chemult Ranger District (Fremont-Winema NF)' : 156246,'Chiloquin Ranger District (Fremont-Winema NF)' : 175814,
##                'Klamath Ranger District (Fremont-Winema NF)' : 72401,'ODF Sun Pass' : 8213,'ODF Gilchrist' : 2353,'ODF Gilchrist (The Conservation Fund)' : 2952,
##                'JWTR Timber Holdings' : 133338,'Cascade Timberlands (Mazama Forest)' : 34139,'Jeld-Wen Inc' : 14725,'J-Spear Ranch' : 3641})
##    elif subArea == 'Southeast':
##        return({'Federal':465335, 'State':5540, 'Private Non-Industrial':57644, 'Private Industrial':153001, 'Tribal':0, 'Homeowner':3600})
##

def getZoneHa(subArea):
    if subArea == 'North':
        return({' Dwellings in Residential - Med':8370, ' Dwellings in Rural Residential':22818, ' Dwellings in Resort District':1051, ' Dwellings in Urban Reserve':3126, ' Dwellings in Forest Use 1':763654, ' Dwellings in EFU':118467})
    elif subArea == 'Southwest':
        return({' Dwellings in Residential - Med':4654, ' Dwellings in Rural Residential':19917, ' Dwellings in Resort District':0, ' Dwellings in Urban Reserve':0, ' Dwellings in Forest Use 1':700727, ' Dwellings in EFU':166381})
    elif subArea == 'Southeast':
        return({' Dwellings in Residential - Med':13, ' Dwellings in Rural Residential':8540, ' Dwellings in Resort District':0, ' Dwellings in Urban Reserve':0, ' Dwellings in Forest Use 1':706494, ' Dwellings in EFU':112292})
    elif subArea == 'South':
        return({' Dwellings in Residential - Med':4667, ' Dwellings in Rural Residential':23147, ' Dwellings in Resort District':0, ' Dwellings in Urban Reserve':0, ' Dwellings in Forest Use 1':1318441, ' Dwellings in EFU':266111})

def getScenarioLabels(scenario):
    if 'CurrentPolicy' in scenario:
        colorVal = 'k'
        labelName = 'Current Management'
        labelNameShort = 'Current Mgmt'
        if '_SYU_' in scenario:
            colorVal = 'r'
            labelName = 'Current Mgmt SYU'
            labelNameShort = 'Current SYU'

    elif 'NoMgmtNoFire' in scenario:
        colorVal = 'lightcoral'
        labelName = 'No Management No Fire'
        labelNameShort = 'NoMgmtNoFre'
    elif 'NoMgmt' in scenario:
        colorVal = 'grey'
        labelName = 'No Management'
        labelNameShort = 'No Mgmt'
        if '_SYU_' in scenario:
            colorVal = 'lightcoral'
            labelName = 'No Mgmt SYU'
            labelNameShort = labelName

    elif 'Timber' in scenario:
        colorVal = 'yellowgreen'
        labelName = 'Timber'
        labelNameShort = labelName
        if '_SYU_' in scenario:
            colorVal = 'orange'
            labelName = 'Timber SYU'
            labelNameShort = 'Timber SYU'

    elif 'Goodfires25' in scenario:
        colorVal = 'deepskyblue'
        labelName = 'Managed Fire 25'
        labelNameShort = labelName
    elif 'Goodfires50' in scenario:
        colorVal = 'r'
        labelName = 'Managed Fire 50'
        labelNameShort = labelName
    elif 'Goodfire' in scenario:
        colorVal = 'deepskyblue'
        labelName = 'Managed Fire'
        labelNameShort = labelName
        if '_SYU_' in scenario:
            colorVal = 'tan'
            labelName = 'Managed Fire SYU'
            labelNameShort = 'Timber SYU'

    elif 'WildfireMgmt' in scenario:
        colorVal = 'mediumpurple'
        labelName = 'Wildfire Management'
        labelNameShort = 'Wildfire Mgnt'
    elif 'WFMNGT_2' in scenario:
        colorVal = 'orange'
        labelName = 'Wildfire Mngt 2'
        labelNameShort = 'Wildfire Mngt 2'
    elif 'HRV' in scenario:
        colorVal = 'orange'
        labelName = 'Historic Variability'
        labelNameShort = 'HRV'
    elif 'Wildlife' in scenario:
        colorVal = 'paleturquoise'
        labelName = 'Wildlife'
        labelNameShort = 'Wildlife'
    elif 'FuelBreak100' in scenario:
        colorVal = 'tan'
        labelName = 'Fuel Break 100m'
        labelNameShort = 'FuelBreak100'
    elif 'FuelBreak300' in scenario:
        colorVal = 'pink'
        labelName = 'Fuel Break 300m'
        labelNameShort = 'FuelBreak300'
    elif 'HarvVol_PP' in scenario:
        colorVal = 'orange'
        labelName = 'Ponderosa Pine Volume'
        if '_SYU' in scenario: labelName = 'Ponderosa Pine Vol SYU'
        labelNameShort = 'PIPO Volume'
    elif 'HarvVol_MC' in scenario:
        colorVal = 'b'
        labelName = 'Mixed Conifer Volume'
        if '_SYU' in scenario: labelName = 'Mixed Conifer Vol SYU'
        labelNameShort = 'MCon Volume'
    elif 'HarvVol' in scenario:
        colorVal = 'k'
        labelName = 'Total Volume'
        if '_SYU' in scenario: labelName = 'Total Volume SYU'
        labelNameShort = 'Total Volume'
    elif scenario == 'NoTreatment':
        colorVal = 'r'
        labelName = 'No Treatment'
        labelNameShort = 'No Treat'
    elif scenario == 'No_Treatment_Fed':
        colorVal = 'r'
        labelName = 'No Federal Treatment'
        labelNameShort = 'No Federal Trt'
    elif scenario == 'Restoration':
        colorVal = 'deepskyblue'
        labelName = 'Accelerated Restoration'
        labelNameShort = 'Accel Restoration'
    elif scenario == 'noFireNoTreatFed':
        colorVal = 'mediumpurple'
        labelName = 'No Fire, No Fed Treatment'
        labelNameShort = 'No Fire, No Fed Trt'
    elif scenario == 'noFireCurrentPolicy':
        colorVal = 'orange'
        labelName = 'No Fire, Current Mgmt.'
    else:
        colorVal = 'grey'
        labelName = 'Scenario not found'
        labelNameShort = 'Error'

    return ([colorVal,labelName,labelNameShort])
