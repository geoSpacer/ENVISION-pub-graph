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

import reporter_Bioenergy
import reporter_Carbon
import reporter_Carbon_compare
import reporter_Dwellings_by_WUI
import reporter_DwellingInZone
import reporter_DownyBrome
import reporter_FireExperience
import reporter_FireHazardDwellings
import reporter_FireOccurrence
import reporter_FireOccurrence_byOwner
import reporter_FireWise
import reporter_FireWise_Vars
import reporter_ForestStructure_byOwner
import reporter_ILAP_wildlife_models
import reporter_ManagementDisturbOwner
import reporter_Mule_Deer
import reporter_PotentialDisturbance
import reporter_PotentialDisturbance_byOwner
import reporter_VFO_SpottedOwl
import reporter_VolumeAvailable
import reporter_WoodProducts
import reporter_WoodProducts_compare
import reporter_TotalVolume
import reporter_TotalVolume_compare
import reporter_Smoke
import reporter_PST_NSO_HSfire_byOwner


def main():
##    for policy in ['CurrentPolicy','No_Treatment']:
    subArea = 'Southeast'
    runName = 'Southeast_20171229_CurrentPolicy'
    chartTitle = 'Current Policy - 29 December 2017'
    outDir = "C:\\Envision\\StudyAreas\\CentralOregon\\Southeast\\" + runName + "\\"
##    outDir = "C:\\Envision\\StudyAreas\\" + runName + "\\"

##    reporter_PST_NSO_HSfire_byOwner.main(outDir, subArea, chartTitle)
    reporter_Bioenergy.main(outDir, subArea, chartTitle)
    reporter_Carbon.main(outDir, subArea, chartTitle)
    reporter_Dwellings_by_WUI.main(outDir, subArea, chartTitle)
    reporter_DwellingInZone.main(outDir, subArea, chartTitle)
    reporter_DownyBrome.main(outDir, subArea, chartTitle)
    reporter_FireExperience.main(outDir, subArea, chartTitle)
    reporter_FireHazardDwellings.main(outDir, subArea, chartTitle)
    reporter_FireOccurrence.main(outDir, subArea, chartTitle)
    reporter_FireOccurrence_byOwner.main(outDir, subArea, chartTitle)
    reporter_FireWise.main(outDir, subArea, chartTitle)
    reporter_FireWise_Vars.main(outDir, subArea, chartTitle)
    reporter_ForestStructure_byOwner.main(outDir, subArea, chartTitle)
    reporter_ILAP_wildlife_models.main(outDir, subArea, chartTitle)
    reporter_ManagementDisturbOwner.main(outDir, subArea, chartTitle)
    reporter_Mule_Deer.main(outDir, subArea, chartTitle)
    reporter_PotentialDisturbance.main(outDir, subArea, chartTitle)
    reporter_PotentialDisturbance_byOwner.main(outDir, subArea, chartTitle)
    reporter_VFO_SpottedOwl.main(outDir, subArea, chartTitle)
    reporter_VolumeAvailable.main(outDir, subArea, chartTitle)
    reporter_WoodProducts.main(outDir, subArea, chartTitle)
    reporter_TotalVolume.main(outDir, subArea, chartTitle)
    reporter_Smoke.main(outDir, subArea, chartTitle)
##
##    reporter_TotalVolume_compare.main(subArea,runName,chartTitle)
##    reporter_Carbon_compare.main(subArea,runName,chartTitle)
##    reporter_WoodProducts_compare.main(subArea,runName,chartTitle)

if __name__ == '__main__':
    main()
