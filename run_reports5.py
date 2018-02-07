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

import reporter5_PMG_in_HS_fire_byOwner
import reporter5_PMG12345_in_HS_fire_byOwner
import reporter5_PMG345_in_Hazard_byOwner
import reporter5_PMG345_in_Hazard_byOwner_NoTreatment
import reporter5_PMG12345_in_Hazard_byOwner
import reporter5_Volume_byOwner
import reporter5_Volume_byOwner_noFire
import reporter5_ForestStructure2_byOwner
import reporter5bw_HS_fire_byOwner
import reporter5bar_ForestStructure2_byOwner

def main():
    subArea = 'Southwest'
    runName = 'Southwest_20151026'
    chartTitle = '26 October 2015'

##    reporter5_ForestStructure2_byOwner.main(subArea,runName,chartTitle)
##    reporter5_PMG_in_HS_fire_byOwner.main(subArea,runName,chartTitle)
##    reporter5_PMG12345_in_HS_fire_byOwner.main(subArea,runName,chartTitle)

##    reporter5_PMG345_in_Hazard_byOwner_NoTreatment.main(subArea,runName,chartTitle)
##    reporter5_PMG345_in_Hazard_byOwner.main(subArea,runName,chartTitle)
    reporter5_PMG12345_in_Hazard_byOwner.main(subArea,runName,chartTitle)

##    reporter5_Volume_byOwner.main(subArea,runName,chartTitle)
##    reporter5_Volume_byOwner_noFire.main(subArea,runName,chartTitle)

##    reporter5bw_HS_fire_byOwner.main(subArea,runName,chartTitle)

##    reporter5bar_ForestStructure2_byOwner.main(subArea,runName,chartTitle)

if __name__ == '__main__':
    main()
