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

import reporter3_PMG345_in_HS_fire
import reporter3_PMG345_in_HS_fire_top10pct
import reporter3_PMG345_in_LgGtOp
import reporter3_NSO_VFO
import reporter3_BBWO_iLAP
import reporter3_WHWO_iLAP
import reporter3_Carbon
import reporter3_Merch_Volume


def main():
    subArea = 'North'
    runName = 'North_20150804'
    chartTitle = '4 August 2015'

    reporter3_PMG345_in_HS_fire.main(subArea, runName, chartTitle, 'All')
    reporter3_PMG345_in_HS_fire.main(subArea, runName, chartTitle, 'Federal')
    reporter3_PMG345_in_HS_fire_top10pct.main(subArea, runName, chartTitle, 'All')
    reporter3_PMG345_in_HS_fire_top10pct.main(subArea, runName, chartTitle, 'Federal')
    reporter3_PMG345_in_LgGtOp.main(subArea, runName, chartTitle, 'All')
    reporter3_PMG345_in_LgGtOp.main(subArea, runName, chartTitle, 'Federal')
    reporter3_NSO_VFO.main(subArea, runName, chartTitle, 'All')
    reporter3_BBWO_iLAP.main(subArea, runName, chartTitle, 'All')
    reporter3_WHWO_iLAP.main(subArea, runName, chartTitle, 'All')
    reporter3_Carbon.main(subArea, runName, chartTitle, 'All')
    reporter3_Carbon.main(subArea, runName, chartTitle, 'Federal')
    reporter3_Merch_Volume.main(subArea, runName, chartTitle, 'All')
    reporter3_Merch_Volume.main(subArea, runName, chartTitle, 'Federal')


if __name__ == '__main__':
    main()
