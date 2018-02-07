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

import reporter2_PMG345_in_HS_fire
import reporter2_PMG345_in_LgGtOp
import reporter2_Merch_Volume
import reporter2_NSO_VFO
import reporter2_BBWO_iLAP
import reporter2_WHWO_iLAP
import reporter2_Carbon
import reporter2_ForestStructure2


def main():
    subArea = 'North'
    runName = 'North_20150804'
    chartTitle = '04 August 2015'

    reporter2_PMG345_in_HS_fire.main(subArea, runName, chartTitle, 'All')
    reporter2_PMG345_in_HS_fire.main(subArea, runName, chartTitle, 'Federal')
    reporter2_PMG345_in_LgGtOp.main(subArea, runName, chartTitle, 'All')
    reporter2_PMG345_in_LgGtOp.main(subArea, runName, chartTitle, 'Federal')
    reporter2_Merch_Volume.main(subArea, runName, chartTitle, 'All')
    reporter2_Merch_Volume.main(subArea, runName, chartTitle, 'Federal')
    reporter2_Merch_Volume.main(subArea, runName, chartTitle, 'Tribal')
    reporter2_Merch_Volume.main(subArea, runName, chartTitle, 'Private Industrial')
    reporter2_NSO_VFO.main(subArea, runName, chartTitle, 'All')
    reporter2_BBWO_iLAP.main(subArea, runName, chartTitle, 'All')
    reporter2_WHWO_iLAP.main(subArea, runName, chartTitle, 'All')
    reporter2_Carbon.main(subArea, runName, chartTitle, 'All')
    reporter2_Carbon.main(subArea, runName, chartTitle, 'Federal')
    reporter2_ForestStructure2.main(subArea, runName, chartTitle, 'All')
    reporter2_ForestStructure2.main(subArea, runName, chartTitle, 'Federal')
    reporter2_ForestStructure2.main(subArea, runName, chartTitle, 'Tribal')
    reporter2_ForestStructure2.main(subArea, runName, chartTitle, 'Private Industrial')
    reporter2_ForestStructure2.main(subArea, runName, chartTitle, 'Private Non-Industrial')


if __name__ == '__main__':
    main()
