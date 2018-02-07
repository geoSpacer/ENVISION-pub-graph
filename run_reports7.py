#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      olsenk
#
# Created:     23/03/2015
# updated: 21 February 2018
#-------------------------------------------------------------------------------

import reporter7_PMG_in_HS_fire_cumulative
import reporter7_PMG_in_Potential_HS_fire
import reporter7_smoke
import reporter7_Homes_Exposed_HS_fire_cumulative
import reporter7_PMG_in_HS_fire_extreme
import reporter7_PMG_in_HS_fire_extreme_fed_stats
import reporter7_ForestStructure2_landscape
import reporter7_Vol_Federal
import reporter7_Vol_Large_Federal
import reporter7_Vol_Large_D3_Federal
import reporter7_Carbon_landscape
import reporter7_Wildlife_landscape_BBWO23

import reporter6_PMG_in_HS_fire_extreme_avg
import reporter6_PMG_in_HS_fire_extreme_NumDwellings1km


def main():
    subArea = 'North'
    chartTitle = 'North_20171117'

    statsFile = 'North_20171116_PMG12345_HS_fire_extreme_fed_stats.csv'
    outDir = "C:\\Envision\\StudyAreas\\CentralOregon\\North\\"
    runList = ['North_20170621_NoMgmt','North_20170606_CurrentPolicy','North_20170611_Goodfires50','North_20170605_FuelBreak300','North_20170615_Timber','North_20170617_HRV','North_20170617_WildfireMgmt','North_20170619_Wildlife']

##    reporter7_PMG_in_HS_fire_cumulative.main(outDir, runList, statsFile)
##    reporter7_PMG_in_Potential_HS_fire.main(outDir, runList, statsFile)
##    reporter7_smoke.main(outDir, runList, statsFile)
##    reporter7_Homes_Exposed_HS_fire_cumulative.main(outDir, runList, statsFile)
##    reporter7_PMG_in_HS_fire_extreme.main(outDir, runList, statsFile)
##    reporter7_ForestStructure2_landscape.main(outDir, runList, statsFile)
##    reporter7_Vol_Federal.main(outDir, runList, statsFile)
##    reporter7_Vol_Large_Federal.main(outDir, runList, statsFile)
##    reporter7_Vol_Large_D3_Federal.main(outDir, runList, statsFile)
##    reporter7_Carbon_landscape.main(outDir, runList, statsFile)
##    reporter7_Wildlife_landscape_BBWO23.main(outDir, runList, statsFile)

##    reporter7_PMG_in_HS_fire_extreme_fed_stats.main(outDir, runList, statsFile)
    reporter6_PMG_in_HS_fire_extreme_avg.main(outDir, subArea, runList, chartTitle, 'Federal')
##    reporter6_PMG_in_HS_fire_extreme_NumDwellings1km.main(outDir, subArea, runList, chartTitle, 'Federal')

##    reporter6_Management_area.main(outDir, subArea, runList, chartTitle, '')
##    reporter6_Management_area_2x2.main(outDir, subArea, runList, chartTitle, '')
##    reporter6_Total_Volume_landscape.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_ForestStructure3_landscape.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_PMG_in_HS_fire_extreme_avg.main(outDir, subArea, runList, chartTitle, 'All')
##    reporter6_PMG_in_HS_fire_proportion.main(outDir, subArea, runList, chartTitle, 'All')



if __name__ == '__main__':
    main()
