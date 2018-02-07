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

import os
import reporter4_ForestStructure2_landscape
import reporter4_Resilience_landscape
# import reporter4_ForestStructure_LG_landscape
import reporter4_Wildlife_landscape
import reporter4_Wildlife_landscape_BBWO23
import reporter4_Wildlife23_landscape
import reporter4_Vol_Carbon_landscape
import reporter4_Vol_Owners
import reporter4_Vol_Owners_Detl
import reporter4_PMG_in_HS_fire
import reporter4_PMG_in_Potential_HS_fire
import reporter4bw_PMG345_in_HS_fire
import reporter4bw_PMG345_in_HS_fire_2var
import reporter4bw_Homes_Exposed_to_HS_fire
import reporter4_Firewise_landscape

def main():
    subArea = 'North'
    runName = 'North_20151023'
    chartTitle = '23 October 2015'
    rootDir = "M:\\Envision_output_summaries\\North_2015\\"

    if os.path.isdir(rootDir + runName):
        raw_input("Run directory exists... press a key")
    else:
        os.mkdir(rootDir + runName)

####    for owner in ['All','Federal','Tribal','Private Industrial','Private Non-Industrial']:
####    for owner in ['All','Federal','Tribal','Private Industrial','Private Non-Industrial','BLM Lands','Chemult Ranger District (Fremont-Winema NF)','Chiloquin Ranger District (Fremont-Winema NF)','Klamath Ranger District (Fremont-Winema NF)','ODF Sun Pass','JWTR Timber Holdings','Cascade Timberlands (Mazama Forest)','Jeld-Wen Inc','J-Spear Ranch']:
##    reporter4_ForestStructure2_landscape.main(subArea, runName, chartTitle, 'All')
##    reporter4_Wildlife_landscape.main(subArea, runName, chartTitle, 'All')
##    reporter4_Wildlife_landscape_BBWO23.main(subArea, runName, chartTitle, 'All')
####        reporter4_Wildlife23_landscape.main(subArea, runName, chartTitle, owner)
#    reporter4_Vol_Carbon_landscape.main(rootDir, subArea, runName, chartTitle, 'All')
    reporter4_Vol_Owners.main(rootDir, subArea, runName, chartTitle, 'All')
######    reporter4_Vol_Owners_Detl.main(subArea, runName, chartTitle, 'All')
##    reporter4_PMG_in_HS_fire.main(subArea, runName, chartTitle, 'All')
##    reporter4_PMG_in_Potential_HS_fire.main(subArea, runName, chartTitle, 'All')
##    reporter4_Resilience_landscape.main(subArea,runName, chartTitle, 'All')
##    reporter4_Firewise_landscape.main(subArea,runName,chartTitle, 'All')

#    reporter4bw_PMG345_in_HS_fire.main(rootDir, subArea, runName, chartTitle, 'All')
##    reporter4bw_PMG345_in_HS_fire_2var.main(subArea, runName, chartTitle, 'All')
#    reporter4bw_Homes_Exposed_to_HS_fire.main(rootDir, subArea, runName, chartTitle, 'All')


if __name__ == '__main__':
    main()
