#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      olsenk
#
# Created:     23/03/2015
# Copyright:   (c) olsenk 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import reporter6_syu_ForestStructure2_landscape
import reporter6_syu_StandingVol_by_Size_landscape
import reporter6_ForestStructure3_landscape
import reporter6_PMG_in_HS_fire_cumulative
import reporter6_PMG_in_HS_fire
import reporter6_PMG_in_HS_fire_extreme
import reporter6_PMG_in_HS_fire_extreme_avg
import reporter6_PMG_in_Potential_HS_fire
import reporter6_Vol_Carbon_landscape
import reporter6_Vol_Owners
import reporter6_Vol_LgTree_Owners
import reporter6_Total_Volume_landscape
import reporter6_Wildlife_landscape_BBWO23
import reporter6bw_PMG345_in_HS_fire_2var
import reporter6_Management_area
import reporter6_Management_area_2x2
import reporter6_Homes_Exposed_HS_fire_cumulative
import reporter6_smoke
import reporter6_PMG_in_HS_fire_proportion

def main():
    subArea = 'Southeast'
    chartTitle = 'Southeast_20170821'
    outDir = "C:\\Envision\\StudyAreas\\CentralOregon\\Southeast\\"
#    runList = ['North_20170621_NoMgmt','North_20170606_CurrentPolicy','North_20170611_Goodfires50','North_20170605_FuelBreak300','North_20170615_Timber','North_20170617_HRV','North_20170617_WildfireMgmt','North_20170619_Wildlife']
    runList = ['Southeast_20170821_CurrentPolicy']

##    reporter6_Management_area.main(outDir, subArea, runList, chartTitle, '')
##    reporter6_Management_area_2x2.main(outDir, subArea, runList, chartTitle, '')
##    reporter6_Total_Volume_landscape.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_Vol_Carbon_landscape.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_PMG_in_HS_fire.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_PMG_in_Potential_HS_fire.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_Vol_Owners.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_Vol_LgTree_Owners.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_Wildlife_landscape_BBWO23.main(outDir, subArea, runList, chartTitle, 'All')
#####    reporter6bw_PMG345_in_HS_fire_2var.main(outDir, subArea, "['Restoration','CurrentPolicy']", chartTitle, 'All')
#    reporter6_syu_ForestStructure2_landscape.main(outDir, subArea, runList, chartTitle, 'Federal')
    reporter6_syu_StandingVol_by_Size_landscape.main(outDir, subArea, runList, chartTitle, 'Federal')
##    reporter6_ForestStructure3_landscape.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_Homes_Exposed_HS_fire_cumulative.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_smoke.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_PMG_in_HS_fire_extreme.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_PMG_in_HS_fire_extreme_avg.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_PMG_in_HS_fire_proportion.main(outDir, subArea, runList, chartTitle, 'All')

####    for owner in ['All','Federal','Tribal','Private Industrial','Private Non-Industrial']:
####    for owner in ['All','Federal','Tribal','Private Industrial','Private Non-Industrial','BLM Lands','Chemult Ranger District (Fremont-Winema NF)','Chiloquin Ranger District (Fremont-Winema NF)','Klamath Ranger District (Fremont-Winema NF)','ODF Sun Pass','JWTR Timber Holdings','Cascade Timberlands (Mazama Forest)','Jeld-Wen Inc','J-Spear Ranch']:
##    reporter4_Wildlife_landscape.main(subArea, runName, chartTitle, 'All')
##    reporter4_Wildlife_landscape_BBWO23.main(subArea, runName, chartTitle, 'All')
####        reporter4_Wildlife23_landscape.main(subArea, runName, chartTitle, owner)
######    reporter4_Vol_Owners_Detl.main(subArea, runName, chartTitle, 'All')
##    reporter4_Resilience_landscape.main(subArea,runName, chartTitle, 'All')
##    reporter4_Firewise_landscape.main(subArea,runName,chartTitle, 'All')

##    reporter4bw_PMG345_in_HS_fire.main(subArea, runName, chartTitle, 'All')
##    reporter4bw_Homes_Exposed_to_HS_fire.main(subArea, runName, chartTitle, 'All')


if __name__ == '__main__':
    main()
