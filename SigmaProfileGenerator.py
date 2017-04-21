#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - October 2016
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

SigmaProgenVersion = '1.2.0'
# Version Changelog
# - SmartPurge implementation. Needs Firmware v01-1.2.3
# - Cura 2 integration (under experimental features)
# - Raft improvements

import time, math, os, platform, sys, json, string, shutil, zipfile, uuid, ctypes, glob

def createSimplify3DProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, dataLog, createFile):
    fff = []
    fff.append(r'<?xml version="1.0" encoding="utf-8"?>'+'\n')
    for q in profilesData['quality']:
        if q['id'] == 'Standard':
            defaultPrintQualityBase = 'Standard'
            break
        else:
            defaultPrintQualityBase = profilesData['quality'][0]['id']
    if hotendLeft['id'] == 'None':
        if hotendRight['id'] == 'None':
            return
        else:            
            fileName = "BCN3D Sigma - Right Extruder "+str(hotendRight['nozzleSize'])+" Only ("+filamentRight['id']+")"
            defaultPrintQuality = 'Right Extruder - '+defaultPrintQualityBase
            extruderPrintOptions = ['Right Extruder']
            filamentLeft = dict([('id', '')])
    elif hotendRight['id'] == 'None':
        fileName = "BCN3D Sigma - Left Extruder "+str(hotendLeft['nozzleSize'])+" Only ("+filamentLeft['id']+")"
        defaultPrintQuality = 'Left Extruder - '+defaultPrintQualityBase
        extruderPrintOptions = ['Left Extruder']
        filamentRight = dict([('id', '')])
    else:
        fileName = "BCN3D Sigma - "+str(hotendLeft['nozzleSize'])+" Left ("+filamentLeft['id']+"), "+str(hotendRight['nozzleSize'])+" Right ("+filamentRight['id']+")"
        defaultPrintQuality = 'Left Extruder - '+defaultPrintQualityBase
        extruderPrintOptions = ['Left Extruder', 'Right Extruder', 'Both Extruders']
    fff.append(r'<profile name="'+fileName+r'" version="'+time.strftime("%Y-%m-%d")+" "+time.strftime("%H:%M:%S")+r'" app="S3D-Software 3.1.1">'+'\n')
    fff.append('  <baseProfile></baseProfile>\n')
    fff.append('  <printMaterial></printMaterial>\n')
    fff.append('  <printQuality>'+defaultPrintQuality+'</printQuality>\n') #+extruder+secondaryExtruderAction+str(quality['id'])+
    if hotendLeft['id'] != 'None':
        fff.append('  <printExtruders>Left Extruder Only</printExtruders>\n')
    else:
        fff.append('  <printExtruders>Right Extruder Only</printExtruders>\n')        
    if hotendLeft['id'] != 'None':
        fff.append(r'  <extruder name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">'+'\n')
        fff.append('    <toolheadNumber>0</toolheadNumber>\n')
        fff.append('    <diameter>'+str(hotendLeft['nozzleSize'])+'</diameter>\n')
        fff.append('    <autoWidth>0</autoWidth>\n')
        fff.append('    <width>'+str(hotendLeft['nozzleSize'] * 0.875)+'</width>\n')
        fff.append('    <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+'</extrusionMultiplier>\n')
        fff.append('    <useRetract>1</useRetract>\n')
        fff.append('    <retractionDistance>'+str(filamentLeft['retractionDistance'])+'</retractionDistance>\n')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>\n')
        fff.append('    <retractionZLift>0.05</retractionZLift>\n')
        fff.append('    <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+'</retractionSpeed>\n')
        fff.append('    <useCoasting>0</useCoasting>\n')
        fff.append('    <coastingDistance>0.2</coastingDistance>\n')
        fff.append('    <useWipe>0</useWipe>\n')
        fff.append('    <wipeDistance>5</wipeDistance>\n')
        fff.append('  </extruder>\n')
    else:
        fff.append(r'  <extruder name="">'+'\n')
        fff.append('    <toolheadNumber>0</toolheadNumber>\n')
        fff.append('    <diameter>0</diameter>\n')
        fff.append('    <autoWidth>0</autoWidth>\n')
        fff.append('    <width>0</width>\n')
        fff.append('    <extrusionMultiplier>0</extrusionMultiplier>\n')
        fff.append('    <useRetract>0</useRetract>\n')
        fff.append('    <retractionDistance>0</retractionDistance>\n')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>\n')
        fff.append('    <retractionZLift>0</retractionZLift>\n')
        fff.append('    <retractionSpeed>0</retractionSpeed>\n')
        fff.append('    <useCoasting>0</useCoasting>\n')
        fff.append('    <coastingDistance>0</coastingDistance>\n')
        fff.append('    <useWipe>0</useWipe>\n')
        fff.append('    <wipeDistance>0</wipeDistance>\n')
        fff.append('  </extruder>\n')
    if hotendRight['id'] != 'None':
        fff.append(r'  <extruder name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">'+'\n')
        fff.append('    <toolheadNumber>1</toolheadNumber>\n')
        fff.append('    <diameter>'+str(hotendRight['nozzleSize'])+'</diameter>\n')
        fff.append('    <autoWidth>0</autoWidth>\n')
        fff.append('    <width>'+str(hotendRight['nozzleSize'] * 0.875)+'</width>\n')
        fff.append('    <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+'</extrusionMultiplier>\n')
        fff.append('    <useRetract>1</useRetract>\n')
        fff.append('    <retractionDistance>'+str(filamentRight['retractionDistance'])+'</retractionDistance>\n')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>\n')
        fff.append('    <retractionZLift>0.05</retractionZLift>\n')
        fff.append('    <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+'</retractionSpeed>\n')
        fff.append('    <useCoasting>0</useCoasting>\n')
        fff.append('    <coastingDistance>0.2</coastingDistance>\n')
        fff.append('    <useWipe>0</useWipe>\n')
        fff.append('    <wipeDistance>5</wipeDistance>\n')
        fff.append('  </extruder>\n')
    fff.append('  <primaryExtruder>0</primaryExtruder>\n')
    fff.append('  <layerHeight>0.2</layerHeight>\n')
    fff.append('  <topSolidLayers>4</topSolidLayers>\n')
    fff.append('  <bottomSolidLayers>4</bottomSolidLayers>\n')
    fff.append('  <perimeterOutlines>3</perimeterOutlines>\n')
    fff.append('  <printPerimetersInsideOut>1</printPerimetersInsideOut>\n')
    fff.append('  <startPointOption>3</startPointOption>\n')
    fff.append('  <startPointOriginX>105</startPointOriginX>\n')
    fff.append('  <startPointOriginY>300</startPointOriginY>\n')
    fff.append('  <startPointOriginZ>300</startPointOriginZ>\n')
    fff.append('  <sequentialIslands>0</sequentialIslands>\n')
    fff.append('  <spiralVaseMode>0</spiralVaseMode>\n')
    fff.append('  <firstLayerHeightPercentage>125</firstLayerHeightPercentage>\n')
    fff.append('  <firstLayerWidthPercentage>100</firstLayerWidthPercentage>\n')
    fff.append('  <firstLayerUnderspeed>0.85</firstLayerUnderspeed>\n')
    fff.append('  <useRaft>0</useRaft>\n')
    fff.append('  <raftExtruder>0</raftExtruder>\n')
    fff.append('  <raftLayers>2</raftLayers>\n')
    fff.append('  <raftOffset>3</raftOffset>\n')
    fff.append('  <raftSeparationDistance>0.2</raftSeparationDistance>\n')
    fff.append('  <raftInfill>85</raftInfill>\n')
    fff.append('  <disableRaftBaseLayers>0</disableRaftBaseLayers>\n')
    fff.append('  <useSkirt>1</useSkirt>\n')
    fff.append('  <skirtExtruder>999</skirtExtruder>\n')
    fff.append('  <skirtLayers>1</skirtLayers>\n')
    fff.append('  <skirtOutlines>2</skirtOutlines>\n')
    fff.append('  <skirtOffset>4</skirtOffset>\n')
    fff.append('  <usePrimePillar>0</usePrimePillar>\n')
    fff.append('  <primePillarExtruder>999</primePillarExtruder>\n')
    fff.append('  <primePillarWidth>15</primePillarWidth>\n')
    fff.append('  <primePillarLocation>7</primePillarLocation>\n')
    fff.append('  <primePillarSpeedMultiplier>1</primePillarSpeedMultiplier>\n')
    fff.append('  <useOozeShield>0</useOozeShield>\n')
    fff.append('  <oozeShieldExtruder>999</oozeShieldExtruder>\n')
    fff.append('  <oozeShieldOffset>2</oozeShieldOffset>\n')
    fff.append('  <oozeShieldOutlines>1</oozeShieldOutlines>\n')
    fff.append('  <oozeShieldSidewallShape>1</oozeShieldSidewallShape>\n')
    fff.append('  <oozeShieldSidewallAngle>30</oozeShieldSidewallAngle>\n')
    fff.append('  <oozeShieldSpeedMultiplier>1</oozeShieldSpeedMultiplier>\n')
    fff.append('  <infillExtruder>1</infillExtruder>\n')
    fff.append('  <internalInfillPattern>Grid</internalInfillPattern>\n')
    fff.append('  <externalInfillPattern>Rectilinear</externalInfillPattern>\n')
    fff.append('  <infillPercentage>20</infillPercentage>\n')
    fff.append('  <outlineOverlapPercentage>25</outlineOverlapPercentage>\n')
    fff.append('  <infillExtrusionWidthPercentage>100</infillExtrusionWidthPercentage>\n')
    fff.append('  <minInfillLength>3</minInfillLength>\n')
    fff.append('  <infillLayerInterval>1</infillLayerInterval>\n')
    fff.append('  <infillAngles>45,-45</infillAngles>\n')
    fff.append('  <overlapInfillAngles>1</overlapInfillAngles>\n')
    fff.append('  <generateSupport>0</generateSupport>\n')
    fff.append('  <supportExtruder>0</supportExtruder>\n')
    fff.append('  <supportInfillPercentage>25</supportInfillPercentage>\n')
    fff.append('  <supportExtraInflation>1</supportExtraInflation>\n')
    fff.append('  <denseSupportLayers>5</denseSupportLayers>\n')
    fff.append('  <denseSupportInfillPercentage>75</denseSupportInfillPercentage>\n')
    fff.append('  <supportLayerInterval>1</supportLayerInterval>\n')

    fff.append('  <supportHorizontalPartOffset>0.7</supportHorizontalPartOffset>\n')
    fff.append('  <supportUpperSeparationLayers>1</supportUpperSeparationLayers>\n')
    fff.append('  <supportLowerSeparationLayers>1</supportLowerSeparationLayers>\n')

    fff.append('  <supportType>0</supportType>\n')
    fff.append('  <supportGridSpacing>1</supportGridSpacing>\n')
    fff.append('  <maxOverhangAngle>60</maxOverhangAngle>\n')
    fff.append('  <supportAngles>90</supportAngles>\n')
    if hotendLeft['id'] != 'None':
        fff.append(r'  <temperatureController name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">'+'\n')
        fff.append('    <temperatureNumber>0</temperatureNumber>\n')
        fff.append('    <isHeatedBed>0</isHeatedBed>\n')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>\n')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>\n')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>\n')
        fff.append(r'    <setpoint layer="1" temperature="150"/>'+'\n')
        fff.append('  </temperatureController>\n')
    if hotendRight['id'] != 'None':
        fff.append(r'  <temperatureController name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">'+'\n')
        fff.append('    <temperatureNumber>1</temperatureNumber>\n')
        fff.append('    <isHeatedBed>0</isHeatedBed>\n')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>\n')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>\n')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>\n')
        fff.append(r'    <setpoint layer="1" temperature="150"/>'+'\n')
        fff.append('  </temperatureController>\n')
    if (hotendLeft['id'] != 'None' and filamentLeft['bedTemperature'] > 0) or (hotendRight['id'] != 'None' and filamentRight['bedTemperature'] > 0):
        fff.append('  <temperatureController name="Heated Bed">\n')
        fff.append('    <temperatureNumber>0</temperatureNumber>\n')
        fff.append('    <isHeatedBed>1</isHeatedBed>\n')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>\n')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>\n')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>\n')
        fff.append(r'    <setpoint layer="1" temperature="50"/>'+'\n')
        fff.append('  </temperatureController>\n')
    fff.append('  <fanSpeed>\n')
    fff.append(r'    <setpoint layer="1" speed="0" />'+'\n')
    fff.append(r'    <setpoint layer="2" speed="100"/>'+'\n')
    fff.append('  </fanSpeed>\n')
    fff.append('  <blipFanToFullPower>0</blipFanToFullPower>\n')
    fff.append('  <adjustSpeedForCooling>1</adjustSpeedForCooling>\n')
    fff.append('  <minSpeedLayerTime>5</minSpeedLayerTime>\n')
    fff.append('  <minCoolingSpeedSlowdown>75</minCoolingSpeedSlowdown>\n')
    fff.append('  <increaseFanForCooling>1</increaseFanForCooling>\n')
    fff.append('  <minFanLayerTime>5</minFanLayerTime>\n')
    fff.append('  <maxCoolingFanSpeed>100</maxCoolingFanSpeed>\n')
    fff.append('  <increaseFanForBridging>1</increaseFanForBridging>\n')
    fff.append('  <bridgingFanSpeed>100</bridgingFanSpeed>\n')
    fff.append('  <use5D>1</use5D>\n')
    fff.append('  <relativeEdistances>0</relativeEdistances>\n')
    fff.append('  <allowEaxisZeroing>1</allowEaxisZeroing>\n')
    fff.append('  <independentExtruderAxes>0</independentExtruderAxes>\n')
    fff.append('  <includeM10123>0</includeM10123>\n')
    fff.append('  <stickySupport>1</stickySupport>\n')
    fff.append('  <applyToolheadOffsets>0</applyToolheadOffsets>\n')
    fff.append('  <gcodeXoffset>0</gcodeXoffset>\n')
    fff.append('  <gcodeYoffset>0</gcodeYoffset>\n')
    fff.append('  <gcodeZoffset>0</gcodeZoffset>\n')
    fff.append('  <overrideMachineDefinition>1</overrideMachineDefinition>\n')
    fff.append('  <machineTypeOverride>0</machineTypeOverride>\n')
    fff.append('  <strokeXoverride>210</strokeXoverride>\n')
    fff.append('  <strokeYoverride>297</strokeYoverride>\n')
    fff.append('  <strokeZoverride>210</strokeZoverride>\n')
    fff.append('  <originOffsetXoverride>0</originOffsetXoverride>\n')
    fff.append('  <originOffsetYoverride>0</originOffsetYoverride>\n')
    fff.append('  <originOffsetZoverride>0</originOffsetZoverride>\n')
    fff.append('  <homeXdirOverride>-1</homeXdirOverride>\n')
    fff.append('  <homeYdirOverride>-1</homeYdirOverride>\n')
    fff.append('  <homeZdirOverride>-1</homeZdirOverride>\n')
    fff.append('  <flipXoverride>1</flipXoverride>\n')
    fff.append('  <flipYoverride>-1</flipYoverride>\n')
    fff.append('  <flipZoverride>1</flipZoverride>\n')
    fff.append('  <toolheadOffsets>0,0|0,0|0,0|0,0|0,0|0,0</toolheadOffsets>\n')
    fff.append('  <overrideFirmwareConfiguration>1</overrideFirmwareConfiguration>\n')
    fff.append('  <firmwareTypeOverride>RepRap (Marlin/Repetier/Sprinter)</firmwareTypeOverride>\n')
    fff.append('  <GPXconfigOverride>r2</GPXconfigOverride>\n')
    fff.append('  <baudRateOverride>250000</baudRateOverride>\n')
    fff.append('  <overridePrinterModels>0</overridePrinterModels>\n')
    fff.append('  <printerModelsOverride></printerModelsOverride>\n')
    fff.append('  <startingGcode></startingGcode>\n')
    fff.append('  <layerChangeGcode></layerChangeGcode>\n')
    fff.append('  <retractionGcode></retractionGcode>\n')
    fff.append('  <toolChangeGcode></toolChangeGcode>\n')
    fff.append('  <endingGcode>M104 S0 T0,M104 S0 T1,M140 S0\t\t;heated bed heater off,G91\t\t;relative positioning,G1 Z+0.5 E-5 Y+10 F[travel_speed]\t;move Z up a bit and retract filament,G28 X0 Y0\t\t;move X/Y to min endstops so the head is out of the way,M84\t\t;steppers off,G90\t\t;absolute positioning,</endingGcode>\n')
    fff.append('  <exportFileFormat>gcode</exportFileFormat>\n')
    fff.append('  <celebration>0</celebration>\n')
    fff.append('  <celebrationSong></celebrationSong>\n')
    fff.append('  <postProcessing></postProcessing>\n')
    fff.append('  <defaultSpeed>2400</defaultSpeed>\n')
    fff.append('  <outlineUnderspeed>0.85</outlineUnderspeed>\n')
    fff.append('  <solidInfillUnderspeed>0.85</solidInfillUnderspeed>\n')
    fff.append('  <supportUnderspeed>0.9</supportUnderspeed>\n')
    fff.append('  <rapidXYspeed>12000</rapidXYspeed>\n')
    fff.append('  <rapidZspeed>1002</rapidZspeed>\n') # If this value changes, Simplify3D bug correction post script should be adapted
    fff.append('  <minBridgingArea>10</minBridgingArea>\n')
    fff.append('  <bridgingExtraInflation>0</bridgingExtraInflation>\n')
    fff.append('  <bridgingExtrusionMultiplier>1</bridgingExtrusionMultiplier>\n')
    fff.append('  <bridgingSpeedMultiplier>1.5</bridgingSpeedMultiplier>\n')
    fff.append('  <filamentDiameter>2.85</filamentDiameter>\n')
    fff.append('  <filamentPricePerKg>19.95</filamentPricePerKg>\n')
    fff.append('  <filamentDensity>1.25</filamentDensity>\n')
    fff.append('  <useMinPrintHeight>0</useMinPrintHeight>\n')
    fff.append('  <minPrintHeight>0</minPrintHeight>\n')
    fff.append('  <useMaxPrintHeight>0</useMaxPrintHeight>\n')
    fff.append('  <maxPrintHeight>0</maxPrintHeight>\n')
    fff.append('  <useDiaphragm>0</useDiaphragm>\n')
    fff.append('  <diaphragmLayerInterval>5</diaphragmLayerInterval>\n')
    fff.append('  <robustSlicing>1</robustSlicing>\n')
    fff.append('  <mergeAllIntoSolid>0</mergeAllIntoSolid>\n')
    fff.append('  <onlyRetractWhenCrossingOutline>0</onlyRetractWhenCrossingOutline>\n')
    fff.append('  <retractBetweenLayers>1</retractBetweenLayers>\n')
    fff.append('  <useRetractionMinTravel>1</useRetractionMinTravel>\n')
    fff.append('  <retractionMinTravel>1.5</retractionMinTravel>\n')
    fff.append('  <retractWhileWiping>1</retractWhileWiping>\n')
    fff.append('  <onlyWipeOutlines>1</onlyWipeOutlines>\n')
    fff.append('  <avoidCrossingOutline>1</avoidCrossingOutline>\n')
    fff.append('  <maxMovementDetourFactor>3</maxMovementDetourFactor>\n')
    fff.append('  <toolChangeRetractionDistance>8</toolChangeRetractionDistance>\n')
    fff.append('  <toolChangeExtraRestartDistance>0</toolChangeExtraRestartDistance>\n')
    fff.append('  <toolChangeRetractionSpeed>2400</toolChangeRetractionSpeed>\n')
    fff.append('  <allowThinWallGapFill>1</allowThinWallGapFill>\n')
    fff.append('  <thinWallAllowedOverlapPercentage>10</thinWallAllowedOverlapPercentage>\n')
    fff.append('  <horizontalSizeCompensation>-0.1</horizontalSizeCompensation>\n')
    # fff.append('  <overridePrinterModels>1</overridePrinterModels>\n')
    # fff.append('  <printerModelsOverride>BCN3DSigma.stl</printerModelsOverride>\n')
    # fff.append('  <autoConfigureMaterial name="'+str(filamentLeft)+" Left, "+str(filamentRight)+" Right"+r'">\n')
    for extruder in extruderPrintOptions:
        for quality in sorted(profilesData['quality'], key=lambda k: k['index']):
            currentInfillPercentage = quality['infillPercentage']
            currentInfillLayerInterval = 1
            currentOverlapInfillAngles = 1
            currentGenerateSupport = 0
            currentSupportHorizontalPartOffset = 0.7
            currentSupportUpperSeparationLayers = 1
            currentSupportLowerSeparationLayers = 1
            currentSupportAngles = '90'
            currentSupportInfillPercentage = 25
            currentDenseSupportInfillPercentage = 75
            currentAvoidCrossingOutline = 1
            fanActionOnToolChange1 = ''
            fanActionOnToolChange2 = ''
            if extruder in ['Left Extruder', 'Right Extruder']:
                # MEX
                if extruder == 'Left Extruder':
                    # MEX Left
                    currentPrimaryExtruder = 0
                    currentFilament = filamentLeft
                    currentHotend = hotendLeft
                    currentLayerHeight = layerHeight(hotendLeft, quality)
                    currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'MEX Left')
                    hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, currentDefaultSpeed)
                    purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight)
                    if 'Both Extruders' in extruderPrintOptions:
                        currentLayerHeightTemp = layerHeight(hotendRight, quality)
                        currentDefaultSpeedTemp, currentFirstLayerUnderspeedTempTemp, currentOutlineUnderspeedTemp, currentSupportUnderspeedTemp = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeightTemp, currentInfillLayerInterval, quality, 'MEX Right')
                        hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeightTemp, currentDefaultSpeedTemp)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeedTemp, currentLayerHeightTemp)
                    else:
                        hotendRightTemperature = hotendLeftTemperature
                        purgeValuesT1 = purgeValuesT0
                else:
                    # MEX Right
                    currentPrimaryExtruder = 1
                    currentFilament = filamentRight
                    currentHotend = hotendRight
                    currentLayerHeight = layerHeight(hotendRight, quality)
                    currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'MEX Right')
                    hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeight, currentDefaultSpeed)
                    purgeValuesT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight)
                    if 'Both Extruders' in extruderPrintOptions:
                        currentLayerHeightTemp = layerHeight(hotendLeft, quality)
                        currentDefaultSpeedTemp, currentFirstLayerUnderspeedTempTemp, currentOutlineUnderspeedTemp, currentSupportUnderspeedTemp = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeightTemp, currentInfillLayerInterval, quality, 'MEX Left')
                        hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeightTemp, currentDefaultSpeedTemp)
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeedTemp, currentLayerHeightTemp)
                    else:
                        hotendLeftTemperature = hotendRightTemperature
                        purgeValuesT0 = purgeValuesT1
                currentInfillExtruder = currentPrimaryExtruder
                currentSupportExtruder = currentPrimaryExtruder
                currentBedTemperature = currentFilament['bedTemperature']
                secondaryExtruderAction = ' - '
            else:
                # IDEX                
                if filamentLeft['isSupportMaterial'] != filamentRight['isSupportMaterial']:
                    # IDEX, Support Material
                    currentGenerateSupport = 1
                    currentSupportHorizontalPartOffset = 0.1
                    currentSupportUpperSeparationLayers = 0
                    currentSupportLowerSeparationLayers = 0
                    currentSupportAngles = '90,0'
                    currentSupportInfillPercentage = 25
                    currentDenseSupportInfillPercentage = 100
                    if filamentLeft['isSupportMaterial']:
                        # IDEX, Support Material in Left Hotend
                        currentPrimaryExtruder = 1
                        currentFilament = filamentRight
                        currentHotend = hotendRight
                        currentLayerHeight = min(layerHeight(hotendRight, quality), hotendLeft['nozzleSize']*0.5)
                        supportFilament = filamentLeft
                        supportHotend = hotendLeft
                        secondaryExtruderAction = ' (Left Ext. for supports) - '
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'IDEX, Supports with Left')
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed * currentSupportUnderspeed, currentLayerHeight)
                        purgeValuesT1 = purgeValuesT0
                        hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, currentDefaultSpeed*currentSupportUnderspeed)
                        hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeight, currentDefaultSpeed)
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M107'+"\t\t"+r';disable fan for support material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M106 S'+str(fanSpeed(currentFilament, hotendRightTemperature, currentLayerHeight))+"\t\t"+r';enable fan for part material,'
                    else:
                        # IDEX, Support Material in Right Hotend
                        currentPrimaryExtruder = 0
                        currentFilament = filamentLeft
                        currentHotend = hotendLeft
                        currentLayerHeight = min(layerHeight(hotendLeft, quality), hotendRight['nozzleSize']*0.5)
                        supportFilament = filamentRight
                        supportHotend = hotendRight
                        secondaryExtruderAction = ' (Right Ext. for supports) - '
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'IDEX, Supports with Right')
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed * currentSupportUnderspeed, currentLayerHeight)
                        hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, currentDefaultSpeed)
                        hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeight, currentDefaultSpeed*currentSupportUnderspeed)
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M106 S'+str(fanSpeed(currentFilament, hotendLeftTemperature, currentLayerHeight))+"\t\t"+r';enable fan for part material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M107'+"\t\t"+r';disable fan for support material,' 
                    currentInfillExtruder = currentPrimaryExtruder
                    currentSupportExtruder = abs(currentPrimaryExtruder-1)
                else:
                    # IDEX, Combined Infill
                    currentAvoidCrossingOutline = 0
                    if hotendLeft['nozzleSize'] <= hotendRight['nozzleSize']:
                        # IDEX, Combined Infill (Right Hotend has thicker or equal nozzle)
                        currentPrimaryExtruder = 0
                        currentFilament = filamentLeft
                        currentHotend = hotendLeft
                        currentLayerHeight = min(layerHeight(currentHotend, quality), hotendRight['nozzleSize']*0.5)
                        currentInfillLayerInterval = int(str((hotendRight['nozzleSize']*0.5)/currentLayerHeight).split('.')[0])
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'IDEX, Infill with Right')
                        hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, max(currentDefaultSpeed,currentDefaultSpeed*currentOutlineUnderspeed))
                        hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeight*currentInfillLayerInterval, currentDefaultSpeed)
                        secondaryExtruderAction = ' (Right Ext. for infill) - '
                        if currentFilament['fanPercentage'][1] != 0:
                            fanActionOnToolChange1 = '' # '{IF NEWTOOL=0} M106 S'+str(fanSpeed(currentFilament, hotendLeftTemperature, currentLayerHeight))+"\t\t"+r';enable fan for perimeters,'
                            fanActionOnToolChange2 = '' # '{IF NEWTOOL=1} M107'+"\t\t"+r';disable fan for infill,'
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight * currentInfillLayerInterval)
                    else:
                        # IDEX, Combined Infill (Left Hotend has thicker nozzle)
                        currentPrimaryExtruder = 1
                        currentFilament = filamentRight
                        currentHotend = hotendRight
                        currentLayerHeight = min(layerHeight(currentHotend, quality), hotendLeft['nozzleSize']*0.5)
                        currentInfillLayerInterval = int(str((hotendLeft['nozzleSize']*0.5)/currentLayerHeight).split('.')[0])
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'IDEX, Infill with Left')
                        hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight*currentInfillLayerInterval, currentDefaultSpeed)
                        hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeight, max(currentDefaultSpeed,currentDefaultSpeed*currentOutlineUnderspeed))
                        secondaryExtruderAction = ' (Left Ext. for infill) - '
                        if currentFilament['fanPercentage'][1] != 0:
                            fanActionOnToolChange1 = '' # '{IF NEWTOOL=0} M107'+"\t\t"+r';disable fan for infill,'
                            fanActionOnToolChange2 = '' # '{IF NEWTOOL=1} M106 S'+str(fanSpeed(currentFilament, hotendRightTemperature, currentLayerHeight))+"\t\t"+r';enable fan for perimeters,'
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight * currentInfillLayerInterval)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight)
                    currentInfillExtruder = abs(currentPrimaryExtruder-1)
                    currentSupportExtruder = currentPrimaryExtruder
                currentBedTemperature = max(filamentLeft['bedTemperature'], filamentRight['bedTemperature'])
            currentFirstLayerHeightPercentage = int(min(125, (currentHotend['nozzleSize']/2)/currentLayerHeight*100, maxFlowValue(currentHotend, currentFilament, currentLayerHeight)*100/(currentHotend['nozzleSize']*currentLayerHeight*(currentDefaultSpeed/60)*float(currentFirstLayerUnderspeed))))
            
            # First layer height correction to stay always between 0.1 - 0.2 mm
            firstLayerHeight = min(max(0.1, (currentLayerHeight * currentFirstLayerHeightPercentage/100.)), 0.2)
            currentFirstLayerHeightPercentage = int(firstLayerHeight * 100 / float(currentLayerHeight))
            currentFirstLayerUnderspeed = min(quality['firstLayerUnderspeed'], round(100 / float(currentFirstLayerHeightPercentage), 2))

            currentPerimeterOutlines = max(2, int(round(quality['wallWidth'] / currentHotend['nozzleSize']))) # 2 minimum Perimeters needed
            currentTopSolidLayers = max(4, int(round(quality['topBottomWidth'] / currentLayerHeight)))        # 4 minimum layers needed
            currentBottomSolidLayers = currentTopSolidLayers
            currentRaftExtruder = currentPrimaryExtruder
            currentSkirtExtruder = currentPrimaryExtruder
            useCoasting, useWipe, onlyRetractWhenCrossingOutline, retractBetweenLayers, useRetractionMinTravel, retractWhileWiping, onlyWipeOutlines = retractValues(currentFilament)
            currentStartPurgeLengthT0, currentToolChangePurgeLengthT0, currentPurgeSpeedT0, currentSParameterT0, currentEParameterT0, currentPParameterT0 = purgeValuesT0
            currentStartPurgeLengthT1, currentToolChangePurgeLengthT1, currentPurgeSpeedT1, currentSParameterT1, currentEParameterT1, currentPParameterT1 = purgeValuesT1
            fff.append(r'  <autoConfigureQuality name="'+extruder+secondaryExtruderAction+str(quality['id'])+r'">'+'\n')
            fff.append('    <globalExtrusionMultiplier>1</globalExtrusionMultiplier>\n')
            fff.append('    <fanSpeed>\n')
            fff.append(r'      <setpoint layer="1" speed="0" />'+'\n')
            if currentPrimaryExtruder == 0:
                fff.append(r'      <setpoint layer="2" speed="'+str(fanSpeed(currentFilament, hotendLeftTemperature, currentLayerHeight))+r'" />'+'\n')
            else:
                fff.append(r'      <setpoint layer="2" speed="'+str(fanSpeed(currentFilament, hotendRightTemperature, currentLayerHeight))+r'" />'+'\n')
            fff.append('    </fanSpeed>\n')
            fff.append('    <filamentDiameter>'+str(currentFilament['filamentDiameter'])+'</filamentDiameter>\n')
            fff.append('    <filamentPricePerKg>'+str(currentFilament['filamentPricePerKg'])+'</filamentPricePerKg>\n')
            fff.append('    <filamentDensity>'+str(currentFilament['filamentDensity'])+'</filamentDensity>\n')
            if hotendLeft['id'] != 'None':
                fff.append(r'    <extruder name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">'+'\n')
                fff.append('      <toolheadNumber>0</toolheadNumber>\n')
                fff.append('      <diameter>'+str(hotendLeft['nozzleSize'])+'</diameter>\n')
                fff.append('      <autoWidth>0</autoWidth>\n')
                fff.append('      <width>'+str(hotendLeft['nozzleSize'] * 0.875)+'</width>\n')
                fff.append('      <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+'</extrusionMultiplier>\n')
                fff.append('      <useRetract>1</useRetract>\n')
                fff.append('      <retractionDistance>'+str(filamentLeft['retractionDistance'])+'</retractionDistance>\n')
                fff.append('      <extraRestartDistance>0</extraRestartDistance>\n')
                fff.append('      <retractionZLift>'+("%.2f" % (currentLayerHeight/2.))+'</retractionZLift>\n')
                fff.append('      <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+'</retractionSpeed>\n')
                fff.append('      <useCoasting>'+str(retractValues(filamentLeft)[0])+'</useCoasting>\n')
                fff.append('      <coastingDistance>'+str(coastValue(hotendLeft, filamentLeft))+'</coastingDistance>\n')
                fff.append('      <useWipe>'+str(retractValues(filamentLeft)[1])+'</useWipe>\n')
                fff.append('      <wipeDistance>'+str(hotendLeft['nozzleSize']*12.5)+'</wipeDistance>\n')
                fff.append('    </extruder>\n')
            if hotendRight['id'] != 'None':
                fff.append(r'    <extruder name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">\n')
                fff.append('      <toolheadNumber>1</toolheadNumber>\n')
                fff.append('      <diameter>'+str(hotendRight['nozzleSize'])+'</diameter>\n')
                fff.append('      <autoWidth>0</autoWidth>\n')
                fff.append('      <width>'+str(hotendRight['nozzleSize'] * 0.875)+'</width>\n')
                fff.append('      <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+'</extrusionMultiplier>\n')
                fff.append('      <useRetract>1</useRetract>\n')
                fff.append('      <retractionDistance>'+str(filamentRight['retractionDistance'])+'</retractionDistance>\n')
                fff.append('      <extraRestartDistance>0</extraRestartDistance>\n')
                fff.append('      <retractionZLift>'+str(currentLayerHeight/2)+'</retractionZLift>\n')
                fff.append('      <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+'</retractionSpeed>\n')
                fff.append('      <useCoasting>'+str(retractValues(filamentRight)[0])+'</useCoasting>\n')
                fff.append('      <coastingDistance>'+str(coastValue(hotendRight, filamentRight))+'</coastingDistance>\n')
                fff.append('      <useWipe>'+str(retractValues(filamentRight)[1])+'</useWipe>\n')
                fff.append('      <wipeDistance>'+str(hotendRight['nozzleSize']*12.5)+'</wipeDistance>\n')
                fff.append('    </extruder>\n')
            fff.append('    <primaryExtruder>'+str(currentPrimaryExtruder)+'</primaryExtruder>\n')
            fff.append('    <raftExtruder>'+str(currentRaftExtruder)+'</raftExtruder>\n')
            fff.append('    <skirtExtruder>'+str(currentSkirtExtruder)+'</skirtExtruder>\n')
            fff.append('    <infillExtruder>'+str(currentInfillExtruder)+'</infillExtruder>\n')
            fff.append('    <supportExtruder>'+str(currentSupportExtruder)+'</supportExtruder>\n')
            fff.append('    <generateSupport>'+str(currentGenerateSupport)+'</generateSupport>\n')
            fff.append('    <layerHeight>'+str(currentLayerHeight)+'</layerHeight>\n')
            fff.append('    <firstLayerHeightPercentage>'+str(currentFirstLayerHeightPercentage)+'</firstLayerHeightPercentage>\n')
            fff.append('    <topSolidLayers>'+str(currentTopSolidLayers)+'</topSolidLayers>\n')
            fff.append('    <bottomSolidLayers>'+str(currentBottomSolidLayers)+'</bottomSolidLayers>\n')
            fff.append('    <perimeterOutlines>'+str(currentPerimeterOutlines)+'</perimeterOutlines>\n')
            fff.append('    <infillPercentage>'+str(currentInfillPercentage)+'</infillPercentage>\n')
            fff.append('    <infillLayerInterval>'+str(currentInfillLayerInterval)+'</infillLayerInterval>\n')
            fff.append('    <defaultSpeed>'+str(currentDefaultSpeed)+'</defaultSpeed>\n')
            fff.append('    <firstLayerUnderspeed>'+str(currentFirstLayerUnderspeed)+'</firstLayerUnderspeed>\n')
            fff.append('    <outlineUnderspeed>'+str(currentOutlineUnderspeed)+'</outlineUnderspeed>\n')
            fff.append('    <supportUnderspeed>'+str(currentSupportUnderspeed)+'</supportUnderspeed>\n')
            fff.append('    <supportInfillPercentage>'+str(currentSupportInfillPercentage)+'</supportInfillPercentage>\n')
            fff.append('    <denseSupportInfillPercentage>'+str(currentDenseSupportInfillPercentage)+'</denseSupportInfillPercentage>\n')
            fff.append('    <avoidCrossingOutline>'+str(currentAvoidCrossingOutline)+'</avoidCrossingOutline>\n')
            fff.append('    <overlapInfillAngles>'+str(currentOverlapInfillAngles)+'</overlapInfillAngles>\n')
            fff.append('    <supportHorizontalPartOffset>'+str(currentSupportHorizontalPartOffset)+'</supportHorizontalPartOffset>\n')
            fff.append('    <supportUpperSeparationLayers>'+str(currentSupportUpperSeparationLayers)+'</supportUpperSeparationLayers>\n')
            fff.append('    <supportLowerSeparationLayers>'+str(currentSupportLowerSeparationLayers)+'</supportLowerSeparationLayers>\n')
            fff.append('    <supportAngles>'+str(currentSupportAngles)+'</supportAngles>\n')
            fff.append('    <onlyRetractWhenCrossingOutline>'+str(onlyRetractWhenCrossingOutline)+'</onlyRetractWhenCrossingOutline>\n')
            fff.append('    <retractBetweenLayers>'+str(retractBetweenLayers)+'</retractBetweenLayers>\n')
            fff.append('    <useRetractionMinTravel>'+str(useRetractionMinTravel)+'</useRetractionMinTravel>\n')
            fff.append('    <retractWhileWiping>'+str(retractWhileWiping)+'</retractWhileWiping>\n')
            fff.append('    <onlyWipeOutlines>'+str(onlyWipeOutlines)+'</onlyWipeOutlines>\n')
            fff.append('    <minBridgingArea>10</minBridgingArea>\n')
            fff.append('    <bridgingExtraInflation>0</bridgingExtraInflation>\n')
            if currentGenerateSupport == 0:
                bridgingSpeedMultiplier = 1.5
            else:
                bridgingSpeedMultiplier = 1
            fff.append('    <bridgingExtrusionMultiplier>'+str(round(currentFilament['extrusionMultiplier']*(1/bridgingSpeedMultiplier), 2))+'</bridgingExtrusionMultiplier>\n')
            fff.append('    <bridgingSpeedMultiplier>'+str(bridgingSpeedMultiplier)+'</bridgingSpeedMultiplier>\n')
            if hotendLeft['id'] != 'None':
                fff.append(r'    <temperatureController name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">'+'\n')
                fff.append('      <temperatureNumber>0</temperatureNumber>\n')
                fff.append('      <isHeatedBed>0</isHeatedBed>\n')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>\n')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>\n')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>\n')
                fff.append(r'      <setpoint layer="1" temperature="'+str(hotendLeftTemperature)+r'"/>'+'\n')
                fff.append('    </temperatureController>\n')
            if hotendRight['id'] != 'None':
                fff.append(r'    <temperatureController name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">'+'\n')
                fff.append('      <temperatureNumber>1</temperatureNumber>\n')
                fff.append('      <isHeatedBed>0</isHeatedBed>\n')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>\n')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>\n')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>\n')
                fff.append(r'      <setpoint layer="1" temperature="'+str(hotendRightTemperature)+r'"/>'+'\n')
                fff.append('    </temperatureController>\n')
            if (hotendLeft['id'] != 'None' and filamentLeft['bedTemperature'] > 0) or (hotendRight['id'] != 'None' and filamentRight['bedTemperature'] > 0):
                fff.append(r'    <temperatureController name="Heated Bed">'+'\n')
                fff.append('      <temperatureNumber>0</temperatureNumber>\n')
                fff.append('      <isHeatedBed>1</isHeatedBed>\n')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>\n')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>\n')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>\n')
                fff.append(r'      <setpoint layer="1" temperature="'+str(currentBedTemperature)+r'"/>'+'\n')
                fff.append('    </temperatureController>\n')
            if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':                    
                fff.append('    <toolChangeGcode>{IF NEWTOOL=0} T0\t\t\t;Start tool switch 0,{IF NEWTOOL=0} G1 F2400 E0,{IF NEWTOOL=0} M800 F'+str(currentPurgeSpeedT0)+' S'+str(currentSParameterT0)+' E'+str(currentEParameterT0)+' P'+str(currentPParameterT0)+'\t;SmartPurge - Needs Firmware v01-1.2.3,;{IF NEWTOOL=0} G1 F'+str(currentPurgeSpeedT0)+' E'+str(currentToolChangePurgeLengthT0)+'\t\t;Default purge value,'+fanActionOnToolChange1+',{IF NEWTOOL=1} T1\t\t\t;Start tool switch 1,{IF NEWTOOL=1} G1 F2400 E0,{IF NEWTOOL=1} M800 F'+str(currentPurgeSpeedT1)+' S'+str(currentSParameterT1)+' E'+str(currentEParameterT1)+' P'+str(currentPParameterT1)+'\t;SmartPurge - Needs Firmware v01-1.2.3,;{IF NEWTOOL=1} G1 F'+str(currentPurgeSpeedT1)+' E'+str(currentToolChangePurgeLengthT1)+'\t\t;Default purge,'+fanActionOnToolChange2+",G4 P2000\t\t\t\t;Stabilize Hotend's pressure,G92 E0\t\t\t\t;Zero extruder,G1 F3000 E-4.5\t\t\t\t;Retract,G1 F[travel_speed]\t\t\t;End tool switch,G91,G1 F[travel_speed] Z2,G90</toolChangeGcode>\n")
            else:
                fff.append('    <toolChangeGcode/>\n')
            if currentFilament['isFlexibleMaterial']:
                reducedAccelerationForPerimeters = 2000
            else:
                reducedAccelerationForPerimeters = accelerationForPerimeters(currentHotend['nozzleSize'], currentLayerHeight, int(currentDefaultSpeed/60. * currentOutlineUnderspeed))
            fff.append(r'    <postProcessing>{REPLACE "; outer perimeter" "; outer perimeter\nM204 S'+str(reducedAccelerationForPerimeters)+r'"},{REPLACE "; inner perimeter" "; inner perimeter\nM204 S2000"},{REPLACE "; solid layer" "; solid layer\nM204 S2000"},{REPLACE "; infill" "; infill\nM204 S2000",{REPLACE "; support" "; support\nM204 S2000"},{REPLACE "; layer end" "; layer end\nM204 S2000"},{REPLACE "F12000\nG1 Z'+str(round(currentLayerHeight*currentFirstLayerHeightPercentage/100., 3))+r' F1002\nG92 E0" "F12000\nG1 Z'+str(round(currentLayerHeight*currentFirstLayerHeightPercentage/100., 3))+r' F1002\nG1 E0.0000 F720\nG92 E0"}</postProcessing>\n')
            fff.append('  </autoConfigureQuality>\n')

            if dataLog != 'noData' :
                # Store flows, speeds, temperatures and other data
                writeData(extruder, currentDefaultSpeed, currentInfillLayerInterval, currentLayerHeight, hotendLeft, hotendRight, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder, filamentLeft, filamentRight, quality, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed, currentFirstLayerHeightPercentage, hotendLeftTemperature, hotendRightTemperature, currentBedTemperature, dataLog)                        

    # fff.append('  </autoConfigureMaterial>\n')

    # Start gcode must be defined in autoConfigureExtruders. Otherwise you have problems with the first heat sequence in Dual Color prints.
    if hotendLeft['id'] != 'None':
        fff.append(r'  <autoConfigureExtruders name="Left Extruder Only"  allowedToolheads="1">'+'\n')
        fff.append('    <startingGcode>;Sigma ProGen: '+str(SigmaProgenVersion)+',,'+firstHeatSequence(hotendLeftTemperature, 0, currentBedTemperature, 'Simplify3D')+',G21\t\t;metric values,G90\t\t;absolute positioning,M82\t\t;set extruder to absolute mode,M107\t\t;start with the fan off,G28 X0 Y0\t\t;move X/Y to min endstops,G28 Z0\t\t;move Z to min endstops,T0\t\t;change to active toolhead,G92 E0\t\t;zero the extruded length,G1 Z5 F200\t\t;Safety Z axis movement,G1 F'+str(currentPurgeSpeedT0)+' E'+str(currentStartPurgeLengthT0)+'\t;extrude '+str(currentStartPurgeLengthT0)+'mm of feed stock,G92 E0\t\t;zero the extruded length again</startingGcode>\n')
        fff.append('    <layerChangeGcode>M104 S0 T1</layerChangeGcode>\n')
        fff.append('  </autoConfigureExtruders>\n')
    if hotendRight['id'] != 'None':
        fff.append(r'  <autoConfigureExtruders name="Right Extruder Only"  allowedToolheads="1">'+'\n')
        fff.append('    <startingGcode>;Sigma ProGen: '+str(SigmaProgenVersion)+',,'+firstHeatSequence(0, hotendRightTemperature, currentBedTemperature, 'Simplify3D')+',G21\t\t;metric values,G90\t\t;absolute positioning,M82\t\t;set extruder to absolute mode,M107\t\t;start with the fan off,G28 X0 Y0\t\t;move X/Y to min endstops,G28 Z0\t\t;move Z to min endstops,T1\t\t;change to active toolhead,G92 E0\t\t;zero the extruded length,G1 Z5 F200\t\t;Safety Z axis movement,G1 F'+str(currentPurgeSpeedT0)+' E'+str(currentStartPurgeLengthT0)+'\t;extrude '+str(currentStartPurgeLengthT0)+'mm of feed stock,G92 E0\t\t;zero the extruded length again</startingGcode>\n')
        fff.append('    <layerChangeGcode>M104 S0 T0</layerChangeGcode>\n')
        fff.append('  </autoConfigureExtruders>\n')
    if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':
        fff.append(r'  <autoConfigureExtruders name="Both Extruders"  allowedToolheads="2">'+'\n')
        fff.append('    <startingGcode>;Sigma ProGen: '+str(SigmaProgenVersion)+',,'+firstHeatSequence(hotendLeftTemperature, hotendRightTemperature, currentBedTemperature, 'Simplify3D')+',G21\t\t;metric values,G90\t\t;absolute positioning,M107\t\t;start with the fan off,G28 X0 Y0\t\t;move X/Y to min endstops,G28 Z0\t\t;move Z to min endstops,T1\t\t;switch to the 2nd extruder,G92 E0\t\t;zero the extruded length,G1 F'+str(currentPurgeSpeedT1)+' E'+str(currentStartPurgeLengthT1)+'\t;extrude '+str(currentStartPurgeLengthT1)+'mm of feed stock,G92 E0\t\t;zero the extruded length again,G1 F200 E-9,T0\t\t;switch to the 1st extruder,G92 E0\t\t;zero the extruded length,G1 F'+str(currentPurgeSpeedT0)+' E'+str(currentStartPurgeLengthT0)+'\t;extrude '+str(currentStartPurgeLengthT0)+'mm of feed stock,G92 E0\t\t;zero the extruded length again</startingGcode>\n')
        fff.append('    <layerChangeGcode></layerChangeGcode>\n')
        fff.append('  </autoConfigureExtruders>\n')

    fff.append('</profile>\n')
    if createFile == 'createFile':
        f = open(fileName+".fff", "w")
        f.writelines(fff)
        f.close()
    if createFile == '--no-file':
        print string.join(fff, '')
    if createFile == '--only-filename':
        print fileName+'.fff'
    return fileName+'.fff'

def createCuraProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, dataLog, createFile):
    
    #  Attention: hotendLeft and hotendRight must be the same, or "None".

    makeSupports = 'None'
    supportType = 'Lines'
    supportDualExtrusion = 'First extruder'
    supportXYDistance = 1

    if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None' and hotendLeft['id'] != hotendRight['id']:
        return
    if hotendLeft['id'] == 'None':
        if hotendRight['id'] == 'None':
            return
        else:            
            # MEX Right
            hotend, extruder, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder = hotendRight, "Right Extruder", 1, 1, 1, 
            currentLayerHeight = layerHeight(hotend, quality)
            supportZdistance = currentLayerHeight
            fileName = "BCN3D Sigma - Right Extruder "+str(hotendRight['nozzleSize'])+" Only ("+filamentRight['id']+") - "+quality['id']
            extruderPrintOptions = ["Right Extruder"]
            filamentLeft = dict([('id', '')])
            currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, 1, quality, 'MEX Right')
            printTemperature1 = 0
            printTemperature2 = temperatureValue(filamentRight, hotendRight, currentLayerHeight, currentDefaultSpeed)
            bedTemperature = filamentRight['bedTemperature']
            filamentDiameter1 = filamentRight['filamentDiameter']
            filamentDiameter2 = 0
            filamentFlow = filamentRight['extrusionMultiplier']*100
            retractionSpeed = filamentRight['retractionSpeed']
            retractionAmount = filamentRight['retractionDistance']
            currentFirstLayerHeightPercentage = int(min(125, (hotend['nozzleSize']/2)/currentLayerHeight*100, maxFlowValue(hotendRight, filamentRight, currentLayerHeight)*100/(hotend['nozzleSize']*currentLayerHeight*(currentDefaultSpeed/60.)*float(currentFirstLayerUnderspeed))))
            if filamentRight['fanPercentage'][1] > 0:
                fanEnabled = 'True'
            else:
                fanEnabled = 'False'
            fanPercentage = fanSpeed(filamentRight, printTemperature2, currentLayerHeight)            
            hotendLeftTemperature, hotendRightTemperature = 0, printTemperature2
            purgeValuesGeneral = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight)       
            purgeValuesT0 = purgeValuesGeneral
            purgeValuesT1 = purgeValuesGeneral
    elif hotendRight['id'] == 'None':
        # MEX Left
        hotend, extruder, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder = hotendLeft, "Left Extruder", 0, 0, 0
        currentLayerHeight = layerHeight(hotend, quality)
        supportZdistance = currentLayerHeight
        fileName = "BCN3D Sigma - Left Extruder "+str(hotendLeft['nozzleSize'])+" Only ("+filamentLeft['id']+") - "+quality['id']
        extruderPrintOptions = ["Left Extruder"]
        filamentRight = dict([('id', '')])
        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, 1, quality, 'MEX Left')
        printTemperature1 = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, currentDefaultSpeed)
        printTemperature2 = 0
        bedTemperature = filamentLeft['bedTemperature']
        filamentDiameter1 = filamentLeft['filamentDiameter']
        filamentDiameter2 = 0
        filamentFlow = filamentLeft['extrusionMultiplier']*100
        retractionSpeed = filamentLeft['retractionSpeed']
        retractionAmount = filamentLeft['retractionDistance']
        currentFirstLayerHeightPercentage = int(min(125, (hotend['nozzleSize']/2)/currentLayerHeight*100, maxFlowValue(hotendLeft, filamentLeft, currentLayerHeight)*100/(hotend['nozzleSize']*currentLayerHeight*(currentDefaultSpeed/60.)*float(currentFirstLayerUnderspeed))))
        if filamentLeft['fanPercentage'][1] > 0:
            fanEnabled = 'True'
        else:
            fanEnabled = 'False'
        fanPercentage = fanSpeed(filamentLeft, printTemperature1, currentLayerHeight)
        hotendLeftTemperature, hotendRightTemperature = printTemperature1, 0
        purgeValuesGeneral = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight)       
        purgeValuesT0 = purgeValuesGeneral
        purgeValuesT1 = purgeValuesGeneral
    else:
        # IDEX
        hotend, extruder, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder = hotendLeft, "Both Extruders", 0, 0, 0
        currentLayerHeight = layerHeight(hotend, quality)
        supportZdistance = currentLayerHeight
        fileName = "BCN3D Sigma - "+str(hotendLeft['nozzleSize'])+" Left ("+filamentLeft['id']+"), "+str(hotendRight['nozzleSize'])+" Right ("+filamentRight['id']+") - "+quality['id']
        extruderPrintOptions = ["Both Extruders"] 
        if filamentLeft['isSupportMaterial'] != filamentRight['isSupportMaterial']:
            # IDEX, Support Material
            makeSupports = 'Everywhere'
            supportDualExtrusion = 'Second extruder'
            supportXYDistance = 1
            supportZdistance = 0
            supportType = 'Grid'
            if filamentLeft['isSupportMaterial']:
                # IDEX, Support Material in Left Hotend. For Cura it's not a correct combination
                return
            else:
                # IDEX, Support Material in Right Hotend
                currentSupportExtruder = 1
                currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, 1, quality, 'IDEX, Supports with Right')
                printTemperature1 = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, currentDefaultSpeed)
                printTemperature2 = temperatureValue(filamentRight, hotendRight, currentLayerHeight, currentDefaultSpeed*currentSupportUnderspeed)
        else:
            # IDEX, Dual Color / Material
            makeSupports = 'None'
            supportDualExtrusion = 'Both'
            currentDefaultSpeedL, currentFirstLayerUnderspeedL, currentOutlineUnderspeedL, currentSupportUnderspeedL = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, 1, quality, 'MEX Left')
            currentDefaultSpeedR, currentFirstLayerUnderspeedR, currentOutlineUnderspeedR, currentSupportUnderspeedR = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, 1, quality, 'MEX Right')
            currentDefaultSpeed = min(currentDefaultSpeedL, currentDefaultSpeedR)
            currentFirstLayerUnderspeed = min(currentFirstLayerUnderspeedL, currentFirstLayerUnderspeedR)
            currentOutlineUnderspeed = min(currentOutlineUnderspeedL, currentOutlineUnderspeedR)
            currentSupportUnderspeed  = min(currentSupportUnderspeedL, currentSupportUnderspeedR)
            printTemperature1 = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, currentDefaultSpeed)
            printTemperature2 = temperatureValue(filamentRight, hotendRight, currentLayerHeight, currentDefaultSpeed)
        bedTemperature = max(filamentLeft['bedTemperature'], filamentRight['bedTemperature'])
        filamentDiameter1 = filamentLeft['filamentDiameter']
        filamentDiameter2 = filamentRight['filamentDiameter']
        filamentFlow = max(filamentLeft['extrusionMultiplier'], filamentRight['extrusionMultiplier'])*100
        retractionSpeed = max(filamentLeft['retractionSpeed'], filamentRight['retractionSpeed'])
        retractionAmount = max(filamentLeft['retractionDistance'], filamentRight['retractionDistance'])
        currentFirstLayerHeightPercentage = int(min(125, (hotend['nozzleSize']/2)/currentLayerHeight*100, min(maxFlowValue(hotendLeft, filamentLeft, currentLayerHeight),maxFlowValue(hotendRight, filamentRight, currentLayerHeight))*100/(hotend['nozzleSize']*currentLayerHeight*(currentDefaultSpeed/60)*float(currentFirstLayerUnderspeed))))
        if filamentLeft['fanPercentage'][1] == 0 or filamentRight['fanPercentage'][1] == 0:
            fanEnabled = 'False'
        else:
            fanEnabled = 'True'
        fanPercentage = max(fanSpeed(filamentLeft, printTemperature1, currentLayerHeight), fanSpeed(filamentRight, printTemperature2, currentLayerHeight))
        hotendLeftTemperature, hotendRightTemperature = printTemperature1, printTemperature2
        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight)
        purgeValuesT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight)

    # First layer height correction to stay always between 0.1 - 0.2 mm
    firstLayerHeight = "%.2f" % min(max(0.1, (currentLayerHeight * currentFirstLayerHeightPercentage/100.)), 0.2)
    currentFirstLayerHeightPercentage = int(float(firstLayerHeight) * 100 / float(currentLayerHeight))
    currentFirstLayerUnderspeed = min(quality['firstLayerUnderspeed'], round(100 / float(currentFirstLayerHeightPercentage), 2))

    currentStartPurgeLengthT0, currentToolChangePurgeLengthT0, currentPurgeSpeedT0, currentSParameterT0, currentEParameterT0, currentPParameterT0 = purgeValuesT0
    currentStartPurgeLengthT1, currentToolChangePurgeLengthT1, currentPurgeSpeedT1, currentSParameterT1, currentEParameterT1, currentPParameterT1 = purgeValuesT1
    purgeValuesGeneral = max(currentStartPurgeLengthT0, currentStartPurgeLengthT1), max(currentToolChangePurgeLengthT0, currentToolChangePurgeLengthT1), min(currentPurgeSpeedT0, currentPurgeSpeedT1), max(currentSParameterT0, currentSParameterT1), max(currentEParameterT0, currentEParameterT1), max(currentPParameterT0, currentPParameterT1)
    currentStartPurgeLength, currentToolChangePurgeLength, currentPurgeSpeed, currentSParameter, currentEParameter, currentPParameter = purgeValuesGeneral
    perimeters = 0
    while perimeters*hotend['nozzleSize'] < quality['wallWidth']:
        perimeters += 1
    currentWallThickness = perimeters * hotend['nozzleSize']
    bottomLayerSpeed = int(currentFirstLayerUnderspeed * currentDefaultSpeed/60.)
    outerShellSpeed = int(currentOutlineUnderspeed * currentDefaultSpeed/60.)
    innerShellSpeed = int(outerShellSpeed + (currentDefaultSpeed/60.-outerShellSpeed)/2.)

    ini = []
    ini.append('[profile]\n')
    ini.append('layer_height = '+str(currentLayerHeight)+'\n')
    ini.append('wall_thickness = '+str(currentWallThickness)+'\n')
    ini.append('retraction_enable = True\n')
    ini.append('solid_layer_thickness = '+str(quality['topBottomWidth'])+'\n')
    ini.append('fill_density = '+str(quality['infillPercentage'])+'\n')
    ini.append('nozzle_size = '+str(hotend['nozzleSize'])+'\n')
    ini.append('print_speed = '+str(currentDefaultSpeed/60)+'\n')
    ini.append('print_temperature = '+str(printTemperature1)+'\n')
    ini.append('print_temperature2 = '+str(printTemperature2)+'\n')
    ini.append('print_temperature3 = 0\n')
    ini.append('print_temperature4 = 0\n')
    ini.append('print_temperature5 = 0\n')
    ini.append('print_bed_temperature = '+str(bedTemperature)+'\n')
    ini.append('support = '+makeSupports+'\n')
    ini.append('platform_adhesion = None\n')
    ini.append('support_dual_extrusion = '+supportDualExtrusion+'\n')
    ini.append('wipe_tower = False\n')
    ini.append('wipe_tower_volume = 50\n')
    ini.append('ooze_shield = False\n')
    ini.append('filament_diameter = '+str(filamentDiameter1)+'\n')
    ini.append('filament_diameter2 = '+str(filamentDiameter2)+'\n')
    ini.append('filament_diameter3 = 0\n')
    ini.append('filament_diameter4 = 0\n')
    ini.append('filament_diameter5 = 0\n')
    ini.append('filament_flow = '+str(filamentFlow)+'\n')
    ini.append('retraction_speed = '+str(retractionSpeed)+'\n')
    ini.append('retraction_amount = '+str(retractionAmount)+'\n')
    ini.append('retraction_dual_amount = 8\n')
    ini.append('retraction_min_travel = 1.5\n')
    if filamentLeft['id'] != '' and filamentLeft['isFlexibleMaterial'] or filamentRight['id'] != '' and filamentRight['isFlexibleMaterial']:
        ini.append('retraction_combing = All\n')
    else:
        ini.append('retraction_combing = No Skin\n')
    ini.append('retraction_minimal_extrusion = 0\n')
    ini.append('retraction_hop = '+("%.2f" % (currentLayerHeight/2.))+'\n')
    ini.append('bottom_thickness = '+str(firstLayerHeight)+'\n')
    ini.append('layer0_width_factor = 100\n')
    ini.append('object_sink = 0\n')
    ini.append('overlap_dual = 0.15\n')
    ini.append('travel_speed = 200\n')
    ini.append('bottom_layer_speed = '+str(bottomLayerSpeed)+'\n')
    ini.append('infill_speed = '+str(currentDefaultSpeed/60)+'\n')
    ini.append('solidarea_speed = '+str(outerShellSpeed)+'\n')
    ini.append('inset0_speed = '+str(outerShellSpeed)+'\n')
    ini.append('insetx_speed = '+str(innerShellSpeed)+'\n')
    ini.append('cool_min_layer_time = 5\n')
    ini.append('fan_enabled = '+str(fanEnabled)+'\n')
    ini.append('skirt_line_count = 2\n')
    ini.append('skirt_gap = 2\n')
    ini.append('skirt_minimal_length = 150.0\n')
    ini.append('fan_full_height = 0.5\n')
    ini.append('fan_speed = '+str(fanPercentage)+'\n')
    ini.append('fan_speed_max = 100\n')
    ini.append('cool_min_feedrate = 10\n')
    ini.append('cool_head_lift = False\n')
    ini.append('solid_top = True\n')
    ini.append('solid_bottom = True\n')
    ini.append('fill_overlap = 15\n')
    ini.append('perimeter_before_infill = True\n')
    ini.append('support_type = '+str(supportType)+'\n')
    ini.append('support_angle = 60\n')
    ini.append('support_fill_rate = 40\n')
    ini.append('support_xy_distance = '+str(supportXYDistance)+'\n')
    ini.append('support_z_distance = '+str(supportZdistance)+'\n')
    ini.append('spiralize = False\n')
    ini.append('simple_mode = False\n')
    ini.append('brim_line_count = 5\n')
    ini.append('raft_margin = 3.0\n')                                        # default 5.0
    ini.append('raft_line_spacing = 2.0\n')                                  # default 3.0
    ini.append('raft_base_thickness = '+str(currentLayerHeight)+'\n')        # default 0.3
    ini.append('raft_base_linewidth = '+str(hotend['nozzleSize']*5)+'\n')    # default 1.0
    ini.append('raft_interface_thickness = '+str(currentLayerHeight)+'\n')   # default 0.27
    ini.append('raft_interface_linewidth = '+str(hotend['nozzleSize'])+'\n') # default 0.4
    ini.append('raft_airgap_all = 0.0\n')                                    # default 0.0
    ini.append('raft_airgap = 0.2\n')                                        # default 0.22
    ini.append('raft_surface_layers = 2\n')                                  # default 2
    ini.append('raft_surface_thickness = '+str(currentLayerHeight)+'\n')     # default 0.27
    ini.append('raft_surface_linewidth = '+str(hotend['nozzleSize'])+'\n')   # default 0.4
    ini.append('fix_horrible_union_all_type_a = True\n')
    ini.append('fix_horrible_union_all_type_b = False\n')
    ini.append('fix_horrible_use_open_bits = False\n')
    ini.append('fix_horrible_extensive_stitching = False\n')
    ini.append('plugin_config = (lp1\n')
    if filamentLeft['id'] != '' and filamentLeft['isFlexibleMaterial'] or filamentRight['id'] != '' and filamentRight['isFlexibleMaterial']:
        ini.append('\t.\n')
    else:
        ini.append('\t(dp2\n')
        ini.append("\tS'params'\n")
        ini.append('\tp3\n')
        ini.append('\t(dp4\n')
        ini.append("\tsS'filename'\n")
        ini.append('\tp5\n')
        ini.append("\tS'RingingRemover.py'\n")
        ini.append('\tp6\n')
        ini.append('\tsa.\n')
    ini.append('object_center_x = -1\n')
    ini.append('object_center_y = -1\n')
    ini.append('\n')
    ini.append('[alterations]\n')
    ini.append('start.gcode = ;Sliced at: {day} {date} {time}\n')
    ini.append('\t;Profile: '+str(fileName)+'\n')
    ini.append('\t;Sigma ProGen: '+str(SigmaProgenVersion)+'\n')
    ini.append('\t;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}\n')
    ini.append('\t;Print time: {print_time}\n')
    ini.append('\t;Filament used: {filament_amount}m {filament_weight}g\n')
    ini.append('\t;Filament cost: {filament_cost}\n')
    if hotendLeft['id'] != 'None':
        ini.append(firstHeatSequence(printTemperature1, 0, bedTemperature, 'Cura'))
    else:
        ini.append(firstHeatSequence(0, printTemperature2, bedTemperature, 'Cura'))
    ini.append('\tG21                               ;metric values\n')
    ini.append('\tG90                               ;absolute positioning\n')
    ini.append('\tM82                               ;set extruder to absolute mode\n')
    ini.append('\tM107                              ;start with the fan off\n')
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops\n')
    ini.append('\tG28 Z0                            ;move Z to min endstops\n')
    ini.append('\tT'+str(currentPrimaryExtruder)+'  ;change to active toolhead\n')
    ini.append('\tG92 E0                            ;zero the extruded length\n')
    ini.append('\tG1 Z5 F1200                       ;Safety Z axis movement\n')
    ini.append('\tG1 F'+str(currentPurgeSpeed)+' E'+str(currentStartPurgeLength)+' ;extrude '+str(currentStartPurgeLength)+'mm of feed stock\n')
    ini.append('\tG92 E0                            ;zero the extruded length again\n')
    ini.append('\tG1 F2400 E-4\n')
    ini.append('\tG91\n')
    ini.append('\tG1 F{travel_speed} Z5\n')
    ini.append('\tG90\n')
    ini.append('end.gcode = M104 S0\n')
    ini.append('\tM140 S0                           ;heated bed heater off\n')
    ini.append('\tG91                               ;relative positioning\n')
    ini.append('\tG1 Z+0.5 E-5 Y+10 F{travel_speed} ;move Z up a bit and retract filament\n')
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops, so the head is out of the way\n')
    ini.append('\tM84                               ;steppers off\n')
    ini.append('\tG90                               ;absolute positioning\n')
    ini.append('\t;{profile_string}\n')
    ini.append('start2.gcode = ;Sliced at: {day} {date} {time}\n')
    ini.append('\t;Profile: '+str(fileName)+'\n')
    ini.append('\t;Sigma ProGen: '+str(SigmaProgenVersion)+'\n')
    ini.append('\t;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}\n')
    ini.append('\t;Print time: {print_time}\n')
    ini.append('\t;Filament used: {filament_amount}m {filament_weight}g\n')
    ini.append('\t;Filament cost: {filament_cost}\n')
    ini.append(firstHeatSequence(printTemperature1, printTemperature2, bedTemperature, 'Cura'))
    ini.append('\tG21                               ;metric values\n')
    ini.append('\tG90                               ;absolute positioning\n')
    ini.append('\tM107                              ;start with the fan off\n')
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops\n')
    ini.append('\tG28 Z0                            ;move Z to min endstops\n')
    ini.append('\tT1                                ;switch to the 2nd extruder\n')
    ini.append('\tG92 E0                            ;zero the extruded length\n')
    ini.append('\tG1 F'+str(currentPurgeSpeedT1)+' E'+str(currentStartPurgeLengthT1)+' ;extrude '+str(currentStartPurgeLengthT1)+'mm of feed stock\n')
    ini.append('\tG92 E0                            ;zero the extruded length again\n')
    ini.append('\tG1 F2400 E-{retraction_dual_amount}\n')
    ini.append('\tT0                                ;switch to the 1st extruder\n')
    ini.append('\tG92 E0                            ;zero the extruded length\n')
    ini.append('\tG1 F'+str(currentPurgeSpeedT0)+' E'+str(currentStartPurgeLengthT0)+' ;extrude '+str(currentStartPurgeLengthT0)+'mm of feed stock\n')
    ini.append('\tG92 E0                            ;zero the extruded length again\n')
    ini.append('\tG1 F2400 E-4\n')
    ini.append('\tG91\n')
    ini.append('\tG1 F{travel_speed} Z5\n')
    ini.append('\tG90\n')
    ini.append('end2.gcode = M104 T0 S0\n')
    ini.append('\tM104 T1 S0                        ;extruder heater off\n')
    ini.append('\tM140 S0                           ;heated bed heater off\n')
    ini.append('\tG91                               ;relative positioning\n')
    ini.append('\tG1 Z+0.5 E-5 Y+10 F{travel_speed} ;move Z up a bit and retract filament\n')
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops, so the head is out of the way\n')
    ini.append('\tM84                               ;steppers off\n')
    ini.append('\tG90                               ;absolute positioning\n')
    ini.append('\t;{profile_string}\n')
    ini.append('support_start.gcode = \n')
    ini.append('support_end.gcode = \n')
    ini.append('cool_start.gcode = \n')
    ini.append('cool_end.gcode = \n')
    ini.append('replace.csv = \n')
    ini.append('preswitchextruder.gcode =          ;Switch between the current extruder and the next extruder, when printing with multiple extruders.\n')
    ini.append('\t;This code is added before the T(n)\n')
    ini.append('postswitchextruder.gcode =         ;Switch between the current extruder and the next extruder, when printing with multiple extruders.\n')
    ini.append('\t;This code is added after the T(n)\n')
    ini.append('\tG1 F2400 E0\n')
    ini.append('\tM800 F'+str(currentPurgeSpeed)+' S'+str(currentSParameter)+' E'+str(currentEParameter)+' P'+str(currentPParameter)+' ;SmartPurge - Needs Firmware v01-1.2.3\n')
    ini.append('\t;G1 F'+str(currentPurgeSpeed)+' E'+str(currentToolChangePurgeLength)+' ;Default purge\n')
    ini.append("\tG4 P2000 ;Stabilize Hotend's pressure\n")
    ini.append('\tG92 E0 ;Zero extruder\n')
    ini.append('\tG1 F2400 E-4 ;Retract\n')
    ini.append('\tG1 F{travel_speed}\n')
    ini.append('\tG91\n')
    ini.append('\tG1 F{travel_speed} Z2\n')
    ini.append('\tG90\n')

    if dataLog != 'noData' :
        # Store flows, speeds, temperatures and other data
        writeData(extruder, currentDefaultSpeed, 1, currentLayerHeight, hotendLeft, hotendRight, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder, filamentLeft, filamentRight, quality, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed, currentFirstLayerHeightPercentage, hotendLeftTemperature, hotendRightTemperature, bedTemperature, dataLog)

    if createFile == 'createFile':
        f = open(fileName+".ini", "w")
        f.writelines(ini)
        f.close()
    if createFile == '--no-file':
        print string.join(ini, '')
    if createFile == '--only-filename':
        print fileName+'.ini'
    return fileName+'.ini'

def createCura2Files():

    '''
        Values hierarchy:
            
            quality->material->variant->definition

            We first ask if the top (user) has the setting value. If not, we continue down. So if the quality sets a value (say fan speed) and material sets it as well, the one set by the quality is used.
    '''

    cura2id = 'bcn3dsigma'
    cura2Name = 'Sigma'
    cura2Manufacturer = 'BCN3D Technologies'
    cura2Category = 'BCN3D Technologies'
    cura2Author = 'Guillem'

    for hotend in sorted(profilesData['hotend'], key=lambda k: k['id']):
        cura2PreferredVariant = hotend['id'].replace(' ', '_')
        if '0.4mm - Brass' in hotend['id']:
            cura2PreferredVariant = hotend['id'].replace(' ', '_')
            break

    for quality in sorted(profilesData['quality'], key=lambda k: k['index']):
        cura2PreferredQuality = quality['id'].replace(' ', '_')
        if 'Standard' in quality['id']:
            cura2PreferredQuality = quality['id'].replace(' ', '_')
            break

    for filament in sorted(profilesData['filament'], key=lambda k: k['id']):
        cura2PreferredMaterial = filament['id'].replace(' ', '_')
        if 'Colorfila PLA' in filament['id']:
            cura2PreferredMaterial = filament['id'].replace(' ', '_')
            break

    if "resources" in os.listdir('.'):
        shutil.rmtree("resources")
    os.mkdir('resources')
    os.mkdir('resources/definitions')
    with open('resources/definitions/'+cura2id+'.def.json', 'w') as f:
        lines = []
        lines.append(r'{'+'\n')
        lines.append(r'    "id": "'+cura2id+r'",'+'\n')
        lines.append(r'    "version": 2,'+'\n')
        lines.append(r'    "name": "'+cura2Name+r'",'+'\n')
        lines.append(r'    "inherits": "fdmprinter",'+'\n')
        lines.append(r'    "metadata": {'+'\n')
        lines.append(r'        "author": "'+cura2Author+r'",'+'\n')
        lines.append(r'        "category": "'+cura2Category+r'",'+'\n')
        lines.append(r'        "manufacturer": "'+cura2Manufacturer+r'",'+'\n')
        lines.append(r'        "file_formats": "text/x-gcode",'+'\n')
        lines.append(r'        "platform": "'+cura2id+r'_bed.obj",'+'\n')
        # lines.append(r'        "platform_texture": "'+cura2id+r'backplate.png",'+'\n')
        lines.append(r'        "platform_offset": [0, 0, 0],'+'\n')
        lines.append(r'        "has_machine_quality": true,'+'\n')
        lines.append(r'        "visible": true,'+'\n')
        lines.append(r'        "has_materials": true,'+'\n')
        lines.append(r'        "has_machine_materials": true,'+'\n')
        lines.append(r'        "has_variant_materials": true,'+'\n')
        lines.append(r'        "has_variants": true,'+'\n')
        lines.append(r'        "preferred_material": "*'+cura2PreferredMaterial+r'*",'+'\n')
        lines.append(r'        "preferred_variant": "*'+cura2PreferredVariant+r'*",'+'\n')
        lines.append(r'        "preferred_quality": "*'+cura2PreferredQuality+r'*",'+'\n')
        lines.append(r'        "variants_name": "Hotend",'+'\n')
        lines.append(r'        "machine_extruder_trains":'+'\n')
        lines.append(r'        {'+'\n')
        lines.append(r'            "0": "'+cura2id+r'_extruder_left",'+'\n')
        lines.append(r'            "1": "'+cura2id+r'_extruder_right"'+'\n')
        lines.append(r'        },'+'\n')
        lines.append(r'        "supported_actions": [ "MachineSettingsAction" ]'+'\n')
        lines.append(r'    },'+'\n')
        lines.append(r'    "overrides": {'+'\n')
        lines.append(r'        "machine_name": { "default_value": "'+cura2Name+r'" },'+'\n')
        lines.append(r'        "machine_width": { "default_value": 210 },'+'\n')
        lines.append(r'        "machine_depth": { "default_value": 297 },'+'\n')
        lines.append(r'        "machine_height": { "default_value": 210 },'+'\n')
        lines.append(r'        "machine_heated_bed": { "default_value": true },'+'\n')
        lines.append(r'        "machine_extruder_count": { "default_value": 2 },'+'\n')
        lines.append(r'        "machine_center_is_zero": { "default_value": false },'+'\n')
        lines.append(r'        "machine_gcode_flavor": { "default_value": "RepRap (Marlin/Sprinter)" },'+'\n')
        lines.append(r'        "machine_head_with_fans_polygon":'+'\n')
        lines.append(r'        {'+'\n')
        lines.append(r'            "default_value":'+'\n')
        lines.append(r'            ['+'\n')
        lines.append(r'                [ -27.8, 39.6 ],'+'\n')
        lines.append(r'                [ -27.8, -58.8 ],'+'\n')
        lines.append(r'                [ 26.2, 39.6 ],'+'\n')
        lines.append(r'                [ 26.2, -58.8 ]'+'\n')
        lines.append(r'            ]'+'\n')
        lines.append(r'        },'+'\n')
        lines.append(r'        "gantry_height": { "default_value": 210 },'+'\n')
        lines.append(r'        "extruder_prime_pos_z": { "default_value": 2.0 },'+'\n') # The Z coordinate of the position where the nozzle primes at the start of printing.
        lines.append(r'        "extruder_prime_pos_abs": { "default_value": false },'+'\n') # Make the extruder prime position absolute rather than relative to the last-known location of the head.
        lines.append(r'        "machine_max_feedrate_x": { "default_value": 200 },'+'\n')
        lines.append(r'        "machine_max_feedrate_y": { "default_value": 200 },'+'\n')
        lines.append(r'        "machine_max_feedrate_z": { "default_value": 15 },'+'\n')
        lines.append(r'        "machine_acceleration": { "default_value": 2000 },'+'\n')
        lines.append(r'        "layer_height_0": { "value": "max(0.1, min(0.2, round(layer_height * 1.25, 2)))" }'+'\n')
        # lines.append(r'        "support_enable":'+'\n')
        # lines.append(r'        {'+'\n')
        # lines.append(r'            "default_value": false,'+'\n')
        # lines.append(r'            "resolve": "'+"'True' if 'True' in extruderValues('support_enable') else 'False'"+r'"'+'\n') # Not working
        # lines.append(r'        }'+'\n')

        # lines.append(r'        "machine_start_gcode": { "default_value": "\n;Sigma ProGen: '+str(SigmaProgenVersion)+r'\n\nG21\t\t;metric values\nG90\t\t;absolute positioning\nM82\t\t;set extruder to absolute mode\nM107\t\t;start with the fan off\nG28 X0 Y0\t\t;move X/Y to min endstops\nG28 Z0\t\t;move Z to min endstops\nG1 Z5 F200\t\t;Safety Z axis movement\n;{extruder_left_start_code}\n;{extruder_right_start_code}\n" },'+'\n')
        # lines.append(r'        "machine_end_gcode": { "default_value": "\nM104 S0 T0\nM104 S0 T1\nM140 S0\t\t;heated bed heater off\nG91\t\t;relative positioning\nG1 Z+0.5 E-5 Y+10 F12000\t;move Z up a bit and retract filament\nG28 X0 Y0\t\t;move X/Y to min endstops so the head is out of the way\nM84\t\t;steppers off\nG90\t\t;absolute positioning\n" },'+'\n')

        # lines.append(r'        "prime_tower_position_x": { "default_value": 105 },'+'\n')
        # lines.append(r'        "prime_tower_position_y": { "default_value": 250 },'+'\n')
        # lines.append(r'        "prime_tower_wipe_enabled": { "default_value": false },'+'\n')

        # lines.append(r'        "material_bed_temp_wait": { "value": "True" },'+'\n')
        # lines.append(r'        "material_print_temp_wait": { "value": "True" },'+'\n')
        # lines.append(r'        "material_bed_temp_prepend": { "value": "True" },'+'\n') # Cura 2.5 ignores it
        # lines.append(r'        "material_print_temp_prepend": { "value": "True" },'+'\n') # Cura 2.5 ignores it
        # lines.append(r'        "multiple_mesh_overlap": { "value": "0" },'+'\n')
        # lines.append(r'        "raft_airgap": { "value": "0" },'+'\n')
        # lines.append(r'        "raft_base_thickness": { "value": "0.3" },'+'\n')
        # lines.append(r'        "raft_interface_line_spacing": { "value": "0.5" },'+'\n')
        # lines.append(r'        "raft_interface_line_width": { "value": "0.5" },'+'\n')
        # lines.append(r'        "raft_interface_thickness": { "value": "0.2" },'+'\n')
        # lines.append(r'        "raft_jerk": { "value": "jerk_layer_0" },'+'\n')
        # lines.append(r'        "raft_margin": { "value": "10" },'+'\n')
        # lines.append(r'        "raft_surface_layers": { "value": "1" },'+'\n')
        # lines.append(r'        "support_angle": { "value": "45" },'+'\n')
        # lines.append(r'        "support_pattern": { "value": "'+"'triangles'"+r'" },'+'\n')
        # lines.append(r'        "support_use_towers": { "value": "False" },'+'\n')
        # lines.append(r'        "support_xy_distance": { "value": "wall_line_width_0 * 2.5" },'+'\n')
        # lines.append(r'        "support_xy_distance_overhang": { "value": "wall_line_width_0" },'+'\n')
        # lines.append(r'        "wall_0_inset": { "value": "0" },'+'\n')
        lines.append(r'    }'+'\n')
        lines.append(r'}'+'\n')
        f.writelines(lines)

    os.mkdir('resources/extruders')
    with open('resources/extruders/'+cura2id+'_extruder_left.def.json', 'w') as f:
        lines = []
        lines.append(r'{'+'\n')
        lines.append(r'    "id": "'+cura2id+r'_extruder_left",'+'\n')
        lines.append(r'    "version": 2,'+'\n')
        lines.append(r'    "name": "Extruder Left",'+'\n')
        lines.append(r'    "inherits": "fdmextruder",'+'\n')
        lines.append(r'    "metadata": {'+'\n')
        lines.append(r'        "machine": "'+cura2id+r'",'+'\n')
        lines.append(r'        "position": "0"'+'\n')
        lines.append(r'    },'+'\n')
        lines.append(r''+'\n')
        lines.append(r'    "overrides": {'+'\n')
        lines.append(r'        "extruder_nr": {'+'\n')
        lines.append(r'            "default_value": 0,'+'\n')
        lines.append(r'            "maximum_value": "1"'+'\n')
        lines.append(r'        },'+'\n')
        lines.append(r'        "machine_nozzle_offset_x": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "machine_nozzle_offset_y": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "machine_extruder_start_code": { "default_value": "\n;{extruder_left_change_code}\nG91\nG1 F12000 Z2\nG90\n" },'+'\n') # Should be set as a quality parameter, but Cura 2.5 doesn't allow it
        lines.append(r'        "machine_extruder_start_pos_abs": { "default_value": false },'+'\n')
        lines.append(r'        "machine_extruder_start_pos_x": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "machine_extruder_start_pos_y": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "machine_extruder_end_code": { "default_value": "" },'+'\n')
        lines.append(r'        "machine_extruder_end_pos_abs": { "default_value": false },'+'\n')
        lines.append(r'        "machine_extruder_end_pos_x": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "machine_extruder_end_pos_y": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "extruder_prime_pos_x": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "extruder_prime_pos_y": { "default_value": 0.0 }'+'\n')
        lines.append(r'    }'+'\n')
        lines.append(r'}'+'\n')
        f.writelines(lines)
    with open('resources/extruders/'+cura2id+'_extruder_right.def.json', 'w') as f:
        lines = []
        lines.append(r'{'+'\n')
        lines.append(r'    "id": "'+cura2id+r'_extruder_right",'+'\n')
        lines.append(r'    "version": 2,'+'\n')
        lines.append(r'    "name": "Extruder Right",'+'\n')
        lines.append(r'    "inherits": "fdmextruder",'+'\n')
        lines.append(r'    "metadata": {'+'\n')
        lines.append(r'        "machine": "'+cura2id+r'",'+'\n')
        lines.append(r'        "position": "1"'+'\n')
        lines.append(r'    },'+'\n')
        lines.append(r''+'\n')
        lines.append(r'    "overrides": {'+'\n')
        lines.append(r'        "extruder_nr": {'+'\n')
        lines.append(r'            "default_value": 1,'+'\n')
        lines.append(r'            "maximum_value": "1"'+'\n')
        lines.append(r'        },'+'\n')
        lines.append(r'        "machine_nozzle_offset_x": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "machine_nozzle_offset_y": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "machine_extruder_start_code": { "default_value": "\n;{extruder_right_change_code}\nG91\nG1 F12000 Z2\nG90\n" },'+'\n') # Should be set as a quality parameter, but Cura 2.5 doesn't allow it
        lines.append(r'        "machine_extruder_start_pos_abs": { "default_value": false },'+'\n')
        lines.append(r'        "machine_extruder_start_pos_x": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "machine_extruder_start_pos_y": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "machine_extruder_end_code": { "default_value": "" },'+'\n')
        lines.append(r'        "machine_extruder_end_pos_abs": { "default_value": false },'+'\n')
        lines.append(r'        "machine_extruder_end_pos_x": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "machine_extruder_end_pos_y": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "extruder_prime_pos_x": { "default_value": 0.0 },'+'\n')
        lines.append(r'        "extruder_prime_pos_y": { "default_value": 0.0 }'+'\n')
        lines.append(r'    }'+'\n')
        lines.append(r'}'+'\n')
        f.writelines(lines)

    os.mkdir('resources/materials')
    os.mkdir('resources/materials/'+cura2id)
    for filament in sorted(profilesData['filament'], key=lambda k: k['id']):
        with open('resources/materials/'+cura2id+'/'+filament['brand'].replace(' ', '_')+'_'+filament['material'].replace(' ', '_')+'.xml.fdm_material', 'w') as f:
            lines = []
            lines.append(r'<?xml version="1.0" encoding="UTF-8"?>'+'\n')
            lines.append(r'<fdmmaterial xmlns="http://www.ultimaker.com/material">'+'\n')
            lines.append(r'    <metadata>'+'\n')
            lines.append(r'        <name>'+'\n')
            lines.append(r'            <brand>'+filament['brand']+'</brand>'+'\n')
            lines.append(r'            <material>'+filament['material']+'</material>'+'\n')
            lines.append(r'            <color>'+filament['color']+'</color>'+'\n')
            lines.append(r'        </name>'+'\n')
            lines.append(r'        <GUID>'+str(uuid.uuid1())+'</GUID>'+'\n')
            lines.append(r'        <version>1</version>'+'\n')
            lines.append(r'        <color_code>'+filament['colorCode']+'</color_code>'+'\n')
            if filament['brand'] == 'Colorfila':
                lines.append(r'        <instructions>http://bcn3dtechnologies.com/en/3d-printer-filaments</instructions>'+'\n')
                lines.append(r'        <author>'+'\n')
                lines.append(r'            <organization>BCN3D Technologies</organization>'+'\n')
                lines.append(r'            <contact>BCN3D Support</contact>'+'\n')
                lines.append(r'            <email>info@bcn3dtechnologies.com</email>'+'\n')
                lines.append(r'            <phone>+34 934 137 088</phone>'+'\n')
                lines.append(r'            <address>'+'\n')
                lines.append(r'                <street>Esteve Terradas 1</street>'+'\n')
                lines.append(r'                <city>Castelldefels</city>'+'\n')
                lines.append(r'                <region>Barcelona</region>'+'\n')
                lines.append(r'                <zip>08860</zip>'+'\n')
                lines.append(r'                <country>Spain</country>'+'\n')
                lines.append(r'            </address>'+'\n')
                lines.append(r'        </author>'+'\n')
                lines.append(r'        <supplier>'+'\n')
                lines.append(r'            <organization>BCN3D Technologies</organization>'+'\n')
                lines.append(r'            <contact>BCN3D Support</contact>'+'\n')
                lines.append(r'            <email>info@bcn3dtechnologies.com</email>'+'\n')
                lines.append(r'            <phone>+34 934 137 088</phone>'+'\n')
                lines.append(r'            <address>'+'\n')
                lines.append(r'                <street>Esteve Terradas 1</street>'+'\n')
                lines.append(r'                <city>Castelldefels</city>'+'\n')
                lines.append(r'                <region>Barcelona</region>'+'\n')
                lines.append(r'                <zip>08860</zip>'+'\n')
                lines.append(r'                <country>Spain</country>'+'\n')
                lines.append(r'            </address>'+'\n')
                lines.append(r'        </supplier>'+'\n')
                # lines.append(r'        <EAN>11 22222 33333 4</EAN>'+'\n')
                # lines.append(r'        <MSDS>http://...</MSDS>'+'\n')
                # lines.append(r'        <TDS>http://...</TDS>'+'\n')
            lines.append(r'    </metadata>'+'\n')
            lines.append(r'    <properties>'+'\n')
            lines.append(r'        <density>'+str(filament['filamentDensity'])+'</density>'+'\n')
            lines.append(r'        <diameter>'+str(filament['filamentDiameter'])+'</diameter>'+'\n')
            lines.append(r'    </properties>'+'\n')
            lines.append(r'    <settings>'+'\n')
            lines.append(r''+'\n')
            lines.append(r'        <machine>'+'\n')
            lines.append(r'           <machine_identifier manufacturer="'+cura2Manufacturer+r'" product="'+cura2id+r'" />'+'\n')
            for hotend in sorted(profilesData['hotend'], key=lambda k: k['id']):
                if hotend['id'] != 'None':
                    lines.append(r'           <hotend id="'+hotend['id']+r'">'+'\n')
                    if filament['isAbrasiveMaterial'] and hotend['material'] == "Brass":
                        lines.append(r'                <setting key="hardware compatible">no</setting>'+'\n')
                    else:
                        lines.append(r'                <setting key="hardware compatible">yes</setting>'+'\n')
                    lines.append(r'            </hotend>'+'\n')

            lines.append(r'       </machine>'+'\n')
            lines.append(r''+'\n')
            lines.append(r'    </settings>'+'\n')
            lines.append(r'</fdmmaterial>'+'\n')
            f.writelines(lines)

    os.mkdir('resources/meshes')
    shutil.copyfile('Profiles Data/bcn3dsigma_bed.obj', 'resources/meshes/'+cura2id+'_bed.obj')

    os.mkdir('resources/quality')
    os.mkdir('resources/quality/'+cura2id)
    for hotend in sorted(profilesData['hotend'], key=lambda k: k['id']):
        if hotend['id'] != 'None':
            for filament in sorted(profilesData['filament'], key=lambda k: k['id']):
                for quality in sorted(profilesData['quality'], key=lambda k: k['index']):

                    # Create a new global quality for the new layer height
                    if cura2id+'_global_Layer_'+("%.2f" % layerHeight(hotend, quality))+'_mm_Quality.inst.cfg' not in os.listdir('resources/quality/'+cura2id):
                        with open('resources/quality/'+cura2id+'/'+cura2id+'_global_Layer_'+("%.2f" % layerHeight(hotend, quality))+'_mm_Quality.inst.cfg', 'w') as f:
                            lines = []
                            lines.append(r'[general]'+'\n')
                            lines.append(r'version = 2'+'\n')
                            lines.append(r'name = Global Layer '+("%.2f" % layerHeight(hotend, quality))+' mm'+'\n')
                            lines.append(r'definition = '+cura2id+'\n')
                            lines.append(r''+'\n')
                            lines.append(r'[metadata]'+'\n')
                            lines.append(r'type = quality'+'\n')
                            lines.append(r'quality_type = layer'+("%.2f" % layerHeight(hotend, quality))+'mm'+'\n')
                            lines.append(r'global_quality = True'+'\n')
                            lines.append(r'weight = '+str(len(glob.glob('resources/quality/'+cura2id+'/'+cura2id+'_global_Layer_*')))+'\n')
                            lines.append(r''+'\n')
                            lines.append(r'[values]'+'\n')
                            lines.append(r'layer_height = '+("%.2f" % layerHeight(hotend, quality))+'\n')
                            f.writelines(lines)

                    with open('resources/quality/'+cura2id+'/'+cura2id+'_'+hotend['id'].replace(' ', '_')+'_'+filament['brand'].replace(' ', '_')+'_'+filament['material'].replace(' ', '_')+'_'+quality['id'].replace(' ', '_')+'_Quality.inst.cfg', 'w') as f:

                        # keep all default keywords commented to make Cura faster

                        lines = []
                        lines.append(r'[general]'+'\n')
                        lines.append(r'version = 2'+'\n')
                        lines.append(r'name = '+quality['id']+' Quality'+'\n')
                        lines.append(r'definition = '+cura2id+'\n')
                        lines.append(r''+'\n')
                        lines.append(r'[metadata]'+'\n')
                        lines.append(r'type = quality'+'\n')
                        lines.append(r'quality_type = layer'+("%.2f" % layerHeight(hotend, quality))+'mm'+'\n')
                        lines.append(r'material = '+filament['brand'].replace(' ', '_')+'_'+filament['material'].replace(' ', '_')+'_'+cura2id+'_'+hotend['id'].replace(' ', '_')+'\n')
                        lines.append(r'weight = '+str(-(quality['index']-3))+'\n')
                        lines.append(r''+'\n')
                        lines.append(r'[values]'+'\n')

                        currentLayerHeight = layerHeight(hotend, quality)
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotend, hotend, filament, filament, currentLayerHeight, 1, quality, 'MEX Left')
                        hotendLeftTemperature = temperatureValue(filament, hotend, currentLayerHeight, currentDefaultSpeed)
                        currentStartPurgeLength, currentToolChangePurgeLength, currentPurgeSpeed, currentSParameter, currentEParameter, currentPParameter = purgeValues(hotend, filament, currentDefaultSpeed, currentLayerHeight)
                        
                        lines.append(r'machine_extruder_start_code = ="\nM800 F'+str(currentPurgeSpeed)+' S'+str(currentSParameter)+' E'+str(currentEParameter)+' P'+str(currentPParameter)+r'\t;SmartPurge - Needs Firmware v01-1.2.3\nG4 P2000\t\t\t\t;Stabilize Hotend'+"'"+r's pressure\nG92 E0\t\t\t\t;Zero extruder\nG1 F3000 E-4.5\t\t\t\t;Retract\nG1 F12000\t\t\t;End tool switch\nG91\nG1 F12000 Z2\nG90\n"'+'\n') # Keyword NOT WORKING on Cura 2.5

                        # resolution
                        lines.append(r'layer_height = '+("%.2f" % layerHeight(hotend, quality))+'\n')
                        lines.append(r'line_width = =machine_nozzle_size * 0.875'+'\n')
                        # lines.append(r'wall_line_width = =line_width'+'\n')
                        # lines.append(r'wall_line_width_0 = =wall_line_width'+'\n')
                        lines.append(r'wall_line_width_x = =machine_nozzle_size * 0.85'+'\n')
                        # lines.append(r'skin_line_width = =line_width'+'\n')
                        lines.append(r'infill_line_width = =machine_nozzle_size * 1.4'+'\n')
                        # lines.append(r'skirt_brim_line_width = =line_width'+'\n')
                        lines.append(r'support_line_width = =infill_line_width'+'\n')
                        # lines.append(r'support_interface_line_width = =line_width'+'\n')
                        # lines.append(r'prime_tower_line_width = =line_width'+'\n')

                        #shell
                        lines.append(r'wall_thickness = '+("%.2f" % quality['wallWidth'])+'\n') 
                        # lines.append(r'wall_0_wipe_dist = =machine_nozzle_size / 2'+'\n')
                        lines.append(r'top_bottom_thickness = '+("%.2f" % quality['topBottomWidth'])+'\n') 
                        if filament['isFlexibleMaterial']:
                            lines.append(r'travel_compensate_overlapping_walls_enabled = False'+'\n')
                        else: 
                            lines.append(r'travel_compensate_overlapping_walls_enabled = True'+'\n') 
                        # lines.append(r'fill_perimeter_gaps = everywhere'+'\n') 
                        lines.append(r'xy_offset = -0.1'+'\n') 
                        lines.append(r'z_seam_type = back'+'\n') 
                        lines.append(r'z_seam_x = 105'+'\n') 
                        lines.append(r'z_seam_y = 297'+'\n') 

                        # infill
                        lines.append(r'infill_sparse_density = ='+("%.2f" % min(100, quality['infillPercentage'] * 1.25))+' if infill_pattern == '+"'"+'cubicsubdiv'+"'"+r' else '+("%.2f" % quality['infillPercentage'])+'\n') # 'if' is not working...
                        lines.append(r'infill_pattern = cubicsubdiv'+'\n')
                        # lines.append(r'sub_div_rad_mult = 100'+'\n')
                        # lines.append(r'sub_div_rad_add = =wall_line_width_x'+'\n')
                        # lines.append(r'infill_overlap = =10 if infill_sparse_density < 95 and infill_pattern != '+"'"+'concentric'+"'"+r' else 0'+'\n')
                        lines.append(r'infill_before_walls = False'+'\n')
                        # lines.append(r'min_infill_area = 0'+'\n')
                        # lines.append(r'max_skin_angle_for_expansion = 20'+'\n')

                        # material -> it's defined here as material's <setting key> uses different keys. This allows to avoid the translation dictionary.
                        lines.append(r'material_flow_dependent_temperature = True'+'\n')
                        lines.append(r'default_material_print_temperature = '+str(round((filament['printTemperature'][1]-filament['printTemperature'][0])/2.+filament['printTemperature'][0]))+'\n')
                        # lines.append(r'material_initial_print_temperature = =max(-273.15, material_print_temperature - 10)'+'\n')
                        # lines.append(r'material_final_print_temperature = =max(-273.15, material_print_temperature - 15)'+'\n')
                        lines.append(r'material_flow_temp_graph = [[1.0,'+str(filament['printTemperature'][0])+'], ['+str(maxFlowValue(hotend, filament, layerHeight(hotend, quality)))+','+str(filament['printTemperature'][1])+']]'+'\n')
                        # lines.append(r'material_extrusion_cool_down_speed = 0.7'+'\n') # this value depends on extruded flow (not material_flow)
                        lines.append(r'material_bed_temperature = '+("%.2f" % filament['bedTemperature'])+'\n')
                        lines.append(r'material_diameter = '+("%.2f" % filament['filamentDiameter'])+'\n')
                        lines.append(r'material_flow = '+("%.2f" % (filament['extrusionMultiplier'] * 100))+'\n')
                        # lines.append(r'retraction_enable = True'+'\n')
                        # lines.append(r'retract_at_layer_change = False'+'\n')
                        lines.append(r'retraction_amount = '+("%.2f" % filament['retractionDistance'])+'\n')
                        lines.append(r'retraction_speed = '+("%.2f" % filament['retractionSpeed'])+'\n')
                        # lines.append(r'retraction_retract_speed = =retraction_speed'+'\n')
                        # lines.append(r'retraction_prime_speed = =retraction_speed'+'\n')
                        # lines.append(r'retraction_extra_prime_amount = 0'+'\n') # Adjust for flex materials
                        # lines.append(r'retraction_min_travel = =line_width * 2'+'\n') # if this value works better, update Cura & S3D
                        # lines.append(r'retraction_count_max = 90'+'\n')
                        # lines.append(r'retraction_extrusion_window = =retraction_amount'+'\n')
                        # lines.append(r'material_standby_temperature = 150'+'\n')
                        # lines.append(r'switch_extruder_retraction_amount = =machine_heat_zone_length'+'\n')
                        lines.append(r'switch_extruder_retraction_speed = =retraction_speed'+'\n')
                        # # lines.append(r'switch_extruder_extra_prime_amount = '+("%.2f" % filament['retractionSpeed'])+'\n') # Parameter that should be there to purge on toolchage
                        lines.append(r'switch_extruder_prime_speed = =retraction_speed'+'\n')

                        # # speed
                        lines.append(r'speed_print = '+("%.2f" % (currentDefaultSpeed/60.))+'\n')
                        # lines.append(r'speed_infill = =speed_print'+'\n')
                        lines.append(r'speed_wall = =round(speed_print - (speed_print - speed_print * '+("%.2f" % currentOutlineUnderspeed)+') / 2, 1)'+'\n')
                        lines.append(r'speed_wall_0 = =round(speed_print * '+("%.2f" % currentOutlineUnderspeed)+', 1)'+'\n')
                        lines.append(r'speed_wall_x = =speed_wall'+'\n')
                        lines.append(r'speed_topbottom = =speed_wall_0'+'\n')
                        lines.append(r'speed_support = =round(speed_print * '+("%.2f" % currentSupportUnderspeed)+', 1)'+'\n')
                        # lines.append(r'speed_support_infill = =speed_support'+'\n')
                        lines.append(r'speed_support_interface = =speed_wall'+'\n')
                        lines.append(r'speed_travel = =round(speed_print if magic_spiralize else 200)'+'\n')
                        lines.append(r'speed_layer_0 = =round(speed_print * '+("%.2f" % currentFirstLayerUnderspeed)+', 1)'+'\n')
                        # lines.append(r'speed_print_layer_0 = =speed_layer_0'+'\n')
                        lines.append(r'speed_travel_layer_0 = =round(speed_travel / 3, 1)'+'\n')
                        # lines.append(r'skirt_brim_speed = =speed_layer_0'+'\n')
                        # lines.append(r'speed_slowdown_layers = 2'+'\n')
                        lines.append(r'speed_equalize_flow_enabled = True'+'\n')
                        lines.append(r'speed_equalize_flow_max = 100'+'\n')

                        lines.append(r'acceleration_enabled = True'+'\n')
                        lines.append(r'acceleration_print = 2000'+'\n')
                        # lines.append(r'acceleration_infill = =acceleration_print'+'\n')
                        lines.append(r'acceleration_wall = =round(acceleration_print - (acceleration_print - acceleration_wall_0)/ 2)'+'\n')
                        lines.append(r'acceleration_wall_0 = '+str(int(accelerationForPerimeters(hotend['nozzleSize'], currentLayerHeight, int(currentDefaultSpeed/60. * currentOutlineUnderspeed))))+'\n')
                        # lines.append(r'acceleration_wall_x = =acceleration_wall'+'\n')
                        lines.append(r'acceleration_topbottom = =acceleration_wall_0'+'\n')
                        lines.append(r'acceleration_support = =acceleration_wall'+'\n')
                        # lines.append(r'acceleration_support_infill = =acceleration_support'+'\n')
                        lines.append(r'acceleration_support_interface = =acceleration_topbottom'+'\n')
                        lines.append(r'acceleration_travel = =acceleration_print if magic_spiralize else 2250'+'\n')
                        lines.append(r'acceleration_layer_0 = =acceleration_topbottom'+'\n')
                        # lines.append(r'acceleration_print_layer_0 = =acceleration_layer_0'+'\n')
                        # lines.append(r'acceleration_travel_layer_0 = =acceleration_layer_0 * acceleration_travel / acceleration_print'+'\n')
                        # lines.append(r'acceleration_skirt_brim = =acceleration_layer_0'+'\n')

                        lines.append(r'jerk_enabled = True'+'\n')
                        lines.append(r'jerk_print = =15'+'\n') # Adjust all jerk
                        # lines.append(r'jerk_infill = =jerk_print'+'\n')
                        lines.append(r'jerk_wall = =jerk_print * 0.75'+'\n')
                        lines.append(r'jerk_wall_0 = =jerk_wall * 0.5'+'\n')
                        # lines.append(r'jerk_wall_x = =jerk_wall'+'\n')
                        lines.append(r'jerk_topbottom = =jerk_print * 0.5'+'\n')
                        lines.append(r'jerk_support = =jerk_print * 0.75'+'\n')
                        # lines.append(r'jerk_support_infill = =jerk_support'+'\n')
                        lines.append(r'jerk_support_interface = =jerk_topbottom'+'\n')
                        lines.append(r'jerk_prime_tower = =jerk_print * 0.75'+'\n')
                        lines.append(r'jerk_travel = =jerk_print if magic_spiralize else 15'+'\n')
                        lines.append(r'jerk_layer_0 = =jerk_topbottom'+'\n')
                        # lines.append(r'jerk_print_layer_0 = =jerk_layer_0'+'\n')
                        # lines.append(r'jerk_travel_layer_0 = =jerk_layer_0 * jerk_travel / jerk_print'+'\n')
                        # lines.append(r'jerk_skirt_brim = =jerk_layer_0'+'\n')

                        # travel
                        lines.append(r'retraction_combing = noskin'+'\n')
                        # lines.append(r'travel_retract_before_outer_wall = False'+'\n')
                        # lines.append(r'travel_avoid_other_parts = True'+'\n')
                        # lines.append(r'travel_avoid_distance = =machine_nozzle_tip_outer_diameter / 2 * 1.25'+'\n')
                        # lines.append(r'start_layers_at_same_position = False'+'\n') # different than z_seam
                        lines.append(r'layer_start_x = 105'+'\n') # different than z_seam
                        lines.append(r'layer_start_y = 297'+'\n') # different than z_seam
                        lines.append(r'retraction_hop_enabled = True'+'\n')
                        lines.append(r'retraction_hop_only_when_collides = True'+'\n')
                        # lines.append(r'retraction_hop = =0.75 * machine_nozzle_size'+'\n')
                        # lines.append(r'retraction_hop_after_extruder_switch = True'+'\n')

                        # cooling
                        if filament['fanPercentage'][1] > 0:
                            lines.append(r'cool_fan_enabled = True'+'\n')
                        else:
                            lines.append(r'cool_fan_enabled = False'+'\n')
                        lines.append(r'cool_fan_speed = '+str(int(filament['fanPercentage'][1]))+'\n')
                        lines.append(r'cool_fan_speed_min = '+str(int(filament['fanPercentage'][0]))+'\n')
                        # lines.append(r'cool_fan_speed_max = =cool_fan_speed'+'\n')
                        # lines.append(r'cool_min_layer_time_fan_speed_max = 10'+'\n')
                        # lines.append(r'cool_fan_speed_0 = 0'+'\n')
                        lines.append("cool_fan_full_at_height = =0 if resolveOrValue('adhesion_type') == 'raft' else resolveOrValue('layer_height_0 + 4 * layer_height')"+'\n') # after 6 layers
                        # lines.append(r'cool_min_layer_time = 5'+'\n')
                        # lines.append(r'cool_min_speed = 10'+'\n')
                        # lines.append(r'cool_lift_head = False'+'\n')

                        # support
                        if filament['isSupportMaterial']:
                            lines.append(r'support_enable = True'+'\n') # Not working
                            lines.append(r'support_infill_rate = 25'+'\n')
                            lines.append(r'support_xy_distance = 0.5'+'\n')
                            lines.append(r'support_z_distance = 0'+'\n')
                        else:
                            lines.append(r'support_enable = False'+'\n')
                            lines.append(r'support_infill_rate = 15'+'\n')
                            lines.append(r'support_xy_distance = 0.7'+'\n')
                            lines.append(r'support_z_distance = =layer_height'+'\n')

                        # lines.append(r'support_type = everywhere'+'\n')
                        # lines.append(r'support_pattern = =zigzag'+'\n')
                        # lines.append(r'support_connect_zigzags = True'+'\n')
                        # lines.append(r'support_top_distance = =extruderValue(support_extruder_nr, 'support_z_distance')'+'\n')
                        # lines.append(r'support_bottom_distance = =extruderValue(support_extruder_nr, 'support_z_distance') if resolveOrValue('support_type') == 'everywhere' else 0'+'\n')
                        # lines.append(r'support_xy_overrides_z = z_overrides_xy'+'\n')
                        # lines.append(r'support_xy_distance_overhang = =machine_nozzle_size / 2'+'\n')
                        # lines.append(r'support_bottom_stair_step_height = 0.3'+'\n')
                        lines.append(r'support_join_distance = 10'+'\n')

                        #line 3039

                        # lines.append(r'cool_lift_head = False'+'\n')
                        # lines.append(r'cool_lift_head = False'+'\n')
                        # lines.append(r'cool_lift_head = False'+'\n')


                        # adjust skirt lenght to make the start purge

                        # lines.append('adhesion_type = 0'+'\n')
                        # lines.append('brim_line_count = 0'+'\n')
                        # lines.append('brim_width = 0'+'\n')
                        # lines.append('coasting_enable = 0'+'\n')
                        # lines.append('coasting_min_volume = 0'+'\n')
                        # lines.append('coasting_speed = 0'+'\n')
                        # lines.append('coasting_volume = 0'+'\n')
                        # lines.append('gradual_infill_step_height = 0'+'\n')
                        # lines.append('gradual_infill_steps = 0'+'\n')
                        # lines.append('infill_before_walls = 0'+'\n')
                        # lines.append('material_flow = 0'+'\n')
                        # lines.append('multiple_mesh_overlap = 0'+'\n')
                        # lines.append('ooze_shield_angle = 0'+'\n')
                        # lines.append('prime_tower_enable = 0'+'\n')
                        # lines.append('prime_tower_size = 0'+'\n')
                        # lines.append('raft_acceleration = 0'+'\n')
                        # lines.append('raft_airgap = 0'+'\n')
                        # lines.append('raft_base_line_spacing = 0'+'\n')
                        # lines.append('raft_base_line_width = 0'+'\n')
                        # lines.append('raft_base_speed = 0'+'\n')
                        # lines.append('raft_base_thickness = 0'+'\n')
                        # lines.append('raft_interface_line_spacing = 0'+'\n')
                        # lines.append('raft_interface_line_width = 0'+'\n')
                        # lines.append('raft_interface_speed = 0'+'\n')
                        # lines.append('raft_interface_thickness = 0'+'\n')
                        # lines.append('raft_jerk = 0'+'\n')
                        # lines.append('raft_margin = 0'+'\n')
                        # lines.append('raft_speed = 0'+'\n')
                        # lines.append('raft_surface_layers = 0'+'\n')
                        # lines.append('raft_surface_line_width = 0'+'\n')
                        # lines.append('raft_surface_thickness = 0'+'\n')
                        # lines.append('skirt_brim_minimal_length = 0'+'\n')
                        # lines.append('skirt_gap = 0'+'\n')
                        # lines.append('support_angle = 0'+'\n')
                        # lines.append('support_bottom_distance = 0'+'\n')
                        # lines.append('support_bottom_height = 0'+'\n')
                        # lines.append('support_bottom_stair_step_height = 0'+'\n')
                        # lines.append('support_enable = 0'+'\n')
                        # lines.append('support_infill_rate = 0'+'\n')
                        # lines.append('support_interface_enable = 0'+'\n')
                        # lines.append('support_interface_height = 0'+'\n')
                        # lines.append('support_interface_line_distance = 0'+'\n')
                        # lines.append('support_interface_pattern = 0'+'\n')
                        # lines.append('support_join_distance = 0'+'\n')
                        # lines.append('support_line_distance = 0'+'\n')
                        # lines.append('support_offset = 0'+'\n')
                        # lines.append('support_pattern = 0'+'\n')
                        # lines.append('support_top_distance = 0'+'\n')
                        # lines.append('support_use_towers = 0'+'\n')
                        # lines.append('support_xy_distance = 0'+'\n')
                        # lines.append('support_xy_distance_overhang = 0'+'\n')
                        # lines.append('support_z_distance = 0'+'\n')
                        # lines.append('wall_0_inset = 0'+'\n')
                        # lines.append('support_infill_extruder_nr = 0'+'\n')
                        # lines.append('adhesion_extruder_nr = 0'+'\n')
                        # lines.append('support_extruder_nr = 0'+'\n')
                        # lines.append('support_interface_extruder_nr = 0'+'\n')

                        # lines.append(r'        "material_print_temperature_layer_0": { "value": "material_print_temperature + 5" },'+'\n')
                        # lines.append(r'        "support_z_distance": { "value": "0" },'+'\n')

                        # lines.append(r'        <setting key="print temperature">'+str(filament['printTemperature'][0])+'</setting>'+'\n')
                        # lines.append(r'        <setting key="heated bed temperature">'+str(filament['bedTemperature'])+'</setting>'+'\n')
                        # lines.append(r'        <setting key="standby temperature">'+str(filament['printTemperature'][0]-25)+'</setting>'+'\n')
                        # lines.append(r'           <setting key="print temperature">'+str(filament['printTemperature'][0])+'</setting>'+'\n')
                        # lines.append(r'           <setting key="heated bed temperature">'+str(filament['bedTemperature'])+'</setting>'+'\n')
                        # lines.append(r'           <setting key="standby temperature">'+str(filament['printTemperature'][0]-25)+'</setting>'+'\n')
                        # lines.append(r'           <setting key="print cooling">40.0</setting>'+'\n')

                        # lines.append(''+'\n')
                        # lines.append('support_z_distance = 0'+'\n')
                        # lines.append('support_interface_enable = True'+'\n')
                        # lines.append(''+'\n')
                        # lines.append(''+'\n')
                        # lines.append('adhesion_type = skirt'+'\n')
                        # lines.append('skirt_gap = 0.5'+'\n')
                        # lines.append('skirt_brim_minimal_length = 50'+'\n')
                        # lines.append(''+'\n')
                        # lines.append('coasting_enable = True'+'\n')
                        # lines.append('coasting_volume = 0.1'+'\n')
                        # lines.append('coasting_min_volume = 0.17'+'\n')
                        # lines.append('coasting_speed = 90'+'\n')
                        # lines.append(''+'\n')

                        f.writelines(lines)
   
    os.mkdir('resources/variants')
    for hotend in sorted(profilesData['hotend'], key=lambda k: k['id']):
        if hotend['id'] != 'None':
            with open('resources/variants/'+cura2id+'_'+hotend['id'].replace(' ', '_')+'.inst.cfg', 'w') as f:
                lines = []
                lines.append('[general]'+'\n')
                lines.append('name = '+hotend['id']+'\n')
                lines.append('version = 2'+'\n')
                lines.append('definition = '+cura2id+'\n')
                lines.append(''+'\n')
                lines.append('[metadata]'+'\n')
                lines.append('author = '+cura2Author+'\n')
                lines.append('type = variant'+'\n')
                lines.append(''+'\n')
                lines.append('[values]'+'\n')

                # machine settings
                lines.append('machine_nozzle_size = '+str(hotend['nozzleSize'])+'\n')
                lines.append('machine_nozzle_tip_outer_diameter = '+str(hotend['nozzleTipOuterDiameter'])+'\n')
                lines.append('machine_nozzle_head_distance = '+str(hotend['nozzleHeadDistance'])+'\n')
                lines.append('machine_nozzle_expansion_angle = '+str(hotend['nozzleExpansionAngle'])+'\n')
                lines.append('machine_heat_zone_length = 8'+'\n')
                lines.append('machine_nozzle_temp_enabled = True'+'\n')
                lines.append('machine_nozzle_heat_up_speed = '+str(hotend['heatUpSpeed'])+'\n')
                lines.append('machine_nozzle_cool_down_speed = '+str(hotend['coolDownSpeed'])+'\n')
                lines.append('machine_min_cool_heat_time_window = '+str(hotend['minimumCoolHeatTimeWindow'])+'\n')

                f.writelines(lines)

def installCura2Files():
    
    allowAutoInstall = False

    if platform.system() == 'Darwin' and 'Cura.app' in os.listdir('/Applications'):
        allowAutoInstall = True
        root_src_dir = 'resources'
        root_dst_dir = '/Applications/Cura.app/Contents/Resources/resources'
    
    elif platform.system() == 'Windows':

        installedCuras = []
        
        for folder in os.listdir('C:\Program Files'): # add [::-1] to list folders in reverse order
            if 'Cura 2' in folder and 'Cura.exe' in os.listdir('C:\\Program Files\\'+folder):
                    installedCuras.append(folder)

        if len(installedCuras) >= 1:

            # check permissions for Windows 10
            if platform.release() == '10':
                if is_admin():
                    allowAutoInstall = True
                else:
                    pass
            else:
                allowAutoInstall = True
            
            if allowAutoInstall:
                if len(installedCuras) > 1:
                    print "\n\t\tYou have more than one Cura 2 installed! Select where you want to add the BCN3D Sigma:"
                    answer0 = ''
                    folderOptions = []
                    for c in range(len(installedCuras)):
                        folderOptions.append(str(c+1))
                        print '\t\t'+str(c+1)+'. '+installedCuras[c]
                    while answer0 not in folderOptions:
                        answer0 = raw_input('\t\t')            
                    allowAutoInstall = True
                    root_src_dir = 'resources'
                    root_dst_dir = 'C:\\Program Files\\'+installedCuras[int(answer0)-1]+'\\resources'
                else:
                    allowAutoInstall = True
                    root_src_dir = 'resources'
                    root_dst_dir = 'C:\\Program Files\\'+installedCuras[0]+'\\resources'

    if allowAutoInstall:
        for src_dir, dirs, files in os.walk(root_src_dir):
            dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.move(src_file, dst_dir)
        if "resources" in os.listdir('.'):
            shutil.rmtree("resources")
        print '\n\t\tThe BCN3D Sigma has been successfully added to Cura 2. Enjoy!\n'
    else:
        print "\n\t\tUnable to install files automatically.\n"
        print "\t\tA new folder called 'resources' has been created in your working directory."
        print "\t\tCOMBINE it with the one inside your Cura 2 installation folder. Be careful to NOT replace it!\n"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def createSimplify3DProfilesBundle(dataLog, profilesCreatedCount):    
    y = 'y'
    if getSimplify3DBundleSize()/1024/1024 >= 150: # define Size limit to notice (in MB)
        print '\t\tEstimated space needed during the process: '+str(int(getSimplify3DBundleSize()*1.075/1024/1024))+' MB.'
        print '\t\tEstimated final bundle size: '+str(int(getSimplify3DBundleSize()*0.075/1024/1024))+' MB.'
        print '\t\tDo you want to continue? (Y/n)'
        while y not in ['Y', 'n']:
            y = raw_input('\t\t')
        print
    else:
        y = 'Y'
    if y == 'Y':
        totalSmaProfiles = (len(profilesData['hotend'])-1) *  len(profilesData['filament']) * 2
        totalBigProfiles = (len(profilesData['hotend'])-1)**2 * len(profilesData['filament'])**2
        totalProfilesAvailable = totalSmaProfiles + totalBigProfiles
        if ".BCN3D Sigma - Simplify3D Profiles temp" in os.listdir('.'):
            shutil.rmtree(".BCN3D Sigma - Simplify3D Profiles temp")
        os.mkdir(".BCN3D Sigma - Simplify3D Profiles temp")
        os.chdir(".BCN3D Sigma - Simplify3D Profiles temp")
        for hotendLeft in sorted(profilesData['hotend'], key=lambda k: k['id']):
            if hotendLeft['id'] != 'None':
                os.mkdir("Left Hotend "+hotendLeft['id'])
                os.chdir("Left Hotend "+hotendLeft['id'])
            else:
                os.mkdir("No Left Hotend")
                os.chdir("No Left Hotend")
            for hotendRight in sorted(profilesData['hotend'], key=lambda k: k['id']):
                if hotendRight['id'] != 'None':
                    os.mkdir("Right Hotend "+hotendRight['id'])
                    os.chdir("Right Hotend "+hotendRight['id'])
                else:                
                    os.mkdir("No Right Hotend")
                    os.chdir("No Right Hotend")
                for filamentLeft in sorted(profilesData['filament'], key=lambda k: k['id']):
                    for filamentRight in sorted(profilesData['filament'], key=lambda k: k['id']):
                        if hotendRight['id'] == 'None' and hotendLeft['id'] == 'None':
                            break
                        profilesCreatedCount += 1
                        createSimplify3DProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, dataLog, 'createFile')
                        sys.stdout.write("\r\t\tProgress: %d%%" % int(float(profilesCreatedCount)/totalProfilesAvailable*100))
                        sys.stdout.flush()
                        if hotendRight['id'] == 'None':
                            break
                    if hotendLeft['id'] == 'None':
                        break
                os.chdir('..')
            os.chdir('..')
        csv = open("BCN3D Sigma - Simplify3D Profiles.csv", "w")
        csv.writelines(dataLog)
        csv.close()
        os.chdir('..')
        sys.stdout.write("\r\t\tProgress: Creating the zip file...")
        sys.stdout.flush()
        shutil.make_archive('BCN3D Sigma - Simplify3D Profiles', 'zip', '.BCN3D Sigma - Simplify3D Profiles temp')
        shutil.rmtree(".BCN3D Sigma - Simplify3D Profiles temp")
        print("\r\t\tYour bundle 'BCN3D Sigma - Simplify3D Profiles.zip' is ready. Enjoy!\n")+'\t',
        return profilesCreatedCount
    else:
        return 0

def getSimplify3DBundleSize(oneLineCsvSize = float(10494984)/78480): # experimental value
    if ".BCN3D Sigma - Simplify3D Profiles temp" in os.listdir('.'):
        shutil.rmtree(".BCN3D Sigma - Simplify3D Profiles temp")
    os.mkdir(".BCN3D Sigma - Simplify3D Profiles temp")
    os.chdir(".BCN3D Sigma - Simplify3D Profiles temp")
    
    totalSmaProfiles = (len(profilesData['hotend'])-1) *  len(profilesData['filament']) * 2
    totalBigProfiles = (len(profilesData['hotend'])-1)**2 * len(profilesData['filament'])**2

    fileNameBig = createSimplify3DProfile(profilesData['hotend'][0], profilesData['hotend'][0], profilesData['filament'][0], profilesData['filament'][0], 'noData', 'createFile')
    fileNameSmall = createSimplify3DProfile(profilesData['hotend'][0], profilesData['hotend'][-1], profilesData['filament'][0], profilesData['filament'][0], 'noData', 'createFile')
    
    csvSize = oneLineCsvSize * (totalSmaProfiles*len(profilesData['quality']) + totalBigProfiles*len(profilesData['quality'])*3)
    bundleSize = totalSmaProfiles*os.path.getsize(fileNameSmall)+totalBigProfiles*os.path.getsize(fileNameBig) + csvSize

    os.chdir('..')
    shutil.rmtree(".BCN3D Sigma - Simplify3D Profiles temp")
    return bundleSize*1.05

def createCuraProfilesBundle(dataLog, profilesCreatedCount):  
    y = 'y'
    if getCuraBundleSize()/1024/1024 >= 150: # define Size limit to notice (in MB)
        print '\t\tEstimated space needed during the process: '+str(int(getSimplify3DBundleSize()*1.075/1024/1024))+' MB.'
        print '\t\tEstimated final bundle size: '+str(int(getSimplify3DBundleSize()*0.075/1024/1024))+' MB.'
        print '\t\tDo you want to continue? (Y/n)'
        while y not in ['Y', 'n']:
            y = raw_input('\t\t')
        print
    else:
        y = 'Y'
    if y == 'Y':
        nozzleSizes = []
        for hotend in sorted(profilesData['hotend'], key=lambda k: k['id'])[:-1]:
            nozzleSizes.append(hotend['nozzleSize'])
        curaGroupedSizes = {x:nozzleSizes.count(x) for x in nozzleSizes}
        curaIDEXHotendsCombinations = 0
        for size in curaGroupedSizes:
            curaIDEXHotendsCombinations += curaGroupedSizes[size]**2
        totalProfilesAvailable = ((len(profilesData['hotend'])-1) *  len(profilesData['filament']) * 2 + curaIDEXHotendsCombinations * len(profilesData['filament'])**2) * len(profilesData['quality'])
        if ".BCN3D Sigma - Cura Profiles temp" in os.listdir('.'):
            shutil.rmtree(".BCN3D Sigma - Cura Profiles temp")
        os.mkdir(".BCN3D Sigma - Cura Profiles temp")
        os.chdir(".BCN3D Sigma - Cura Profiles temp")

        for hotendLeft in sorted(profilesData['hotend'], key=lambda k: k['id']):
            if hotendLeft['id'] != 'None':
                os.mkdir("Left Hotend "+hotendLeft['id'])
                os.chdir("Left Hotend "+hotendLeft['id'])
            else:
                os.mkdir("No Left Hotend")
                os.chdir("No Left Hotend")
            for hotendRight in sorted(profilesData['hotend'], key=lambda k: k['id']):
                if hotendRight['id'] != 'None':
                    os.mkdir("Right Hotend "+hotendRight['id'])
                    os.chdir("Right Hotend "+hotendRight['id'])
                else:                
                    os.mkdir("No Right Hotend")
                    os.chdir("No Right Hotend")
                for quality in sorted(profilesData['quality'], key=lambda k: k['index']):
                    os.mkdir(quality['id'])
                    os.chdir(quality['id'])
                    for filamentLeft in sorted(profilesData['filament'], key=lambda k: k['id']):
                        for filamentRight in sorted(profilesData['filament'], key=lambda k: k['id']):
                            if hotendRight['id'] == 'None' and hotendLeft['id'] == 'None':
                                break
                            if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':
                                if hotendLeft['nozzleSize'] != hotendRight['nozzleSize']:
                                    break
                            profilesCreatedCount += 1
                            createCuraProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, dataLog, 'createFile')
                            sys.stdout.write("\r\t\tProgress: %d%%" % int(float(profilesCreatedCount)/totalProfilesAvailable*100))
                            sys.stdout.flush()
                            if hotendRight['id'] == 'None':
                                break
                        if hotendLeft['id'] == 'None':
                            break
                    os.chdir('..')
                os.chdir('..')
            os.chdir('..')
        csv = open("BCN3D Sigma - Cura Profiles.csv", "w")
        csv.writelines(dataLog)
        csv.close()
        os.chdir('..')
        sys.stdout.write("\r\t\tProgress: Creating the zip file...")
        sys.stdout.flush()
        shutil.make_archive('BCN3D Sigma - Cura Profiles', 'zip', '.BCN3D Sigma - Cura Profiles temp')
        shutil.rmtree(".BCN3D Sigma - Cura Profiles temp")
        print("\r\t\tYour bundle 'BCN3D Sigma - Cura Profiles.zip' is ready. Enjoy!\n")+'\t',
        return profilesCreatedCount
    else:
        return 0

def getCuraBundleSize(oneLineCsvSize = float(10494984)/78480): # experimental value
    if ".BCN3D Sigma - Cura Profiles temp" in os.listdir('.'):
        shutil.rmtree(".BCN3D Sigma - Cura Profiles temp")
    os.mkdir(".BCN3D Sigma - Cura Profiles temp")
    os.chdir(".BCN3D Sigma - Cura Profiles temp")

    nozzleSizes = []
    for hotend in sorted(profilesData['hotend'], key=lambda k: k['id'])[:-1]:
        nozzleSizes.append(hotend['nozzleSize'])
    curaGroupedSizes = {x:nozzleSizes.count(x) for x in nozzleSizes}
    curaIDEXHotendsCombinations = 0
    for size in curaGroupedSizes:
        curaIDEXHotendsCombinations += curaGroupedSizes[size]**2

    totalProfiles = ((len(profilesData['hotend'])-1) *  len(profilesData['filament']) * 2 + curaIDEXHotendsCombinations * len(profilesData['filament'])**2) * len(profilesData['quality'])

    fileName = createCuraProfile(profilesData['hotend'][0], profilesData['hotend'][0], profilesData['filament'][0], profilesData['filament'][0], profilesData['quality'][0], 'noData', 'createFile')
    
    csvSize = oneLineCsvSize * totalProfiles
    bundleSize = totalProfiles*os.path.getsize(fileName) + csvSize

    os.chdir('..')
    shutil.rmtree(".BCN3D Sigma - Cura Profiles temp")
    return bundleSize*1.05

def layerHeight(hotend, quality):
    rawLayerHeight = hotend['nozzleSize'] * quality['layerHeightMultiplier']
    if rawLayerHeight > 0.1:
        if rawLayerHeight > 0.2:
            base = 0.1
        else:
            base = 0.05
    else:
        base = 0.025
    return round(rawLayerHeight / base) * base

def speedMultiplier(hotend, filament):
    if filament['isFlexibleMaterial']:
        return float(filament['defaultPrintSpeed'])/24*hotend['nozzleSize']
        # 24*hotend['nozzleSize'] -> experimental value that works better with flexibles
    else:
        return float(filament['defaultPrintSpeed'])/60
        # 60 -> speed for base material (PLA) at base quality (Standard)

def purgeValues(hotend, filament, speed, layerHeight, minPurgeLength = 20): # purge at least 20mm so the filament weight is enough to stay inside the purge container
    
    '''
    SmartPurge Command:
    M800 F-- S-- E-- P--
        F - Speed
        S - Slope (according to NSize, Flow, Purge@5min)
        E - Maximum distance to purge (according to NSize, Flow)
        P - Minimum distance to purge
    '''

    # nozzleSizeBehavior
    maxPurgeLenghtAtHotendTip = 2.25 * filament['purgeLength'] * filament['extrusionMultiplier']
    minPurgeLenghtAtHotendTip = 0.5  * filament['purgeLength'] * filament['extrusionMultiplier']
    curveGrowth = 1 # Here we assume the growth curve is constant for all materials. Change this value if it's not
    hotendPurgeMultiplier = (maxPurgeLenghtAtHotendTip - (maxPurgeLenghtAtHotendTip-minPurgeLenghtAtHotendTip)*math.exp(-hotend['nozzleSize']/float(curveGrowth)))/float(filament['purgeLength'])

    baseStartLength04 = 7
    startPurgeLength = float("%.2f" % max(10, (hotendPurgeMultiplier * baseStartLength04)))
    
    # this length is a FIXED value. It is not used on SmartPurge, we do not recommend to work with fixed purge lengths
    baseToolChangeLength04 = 1.5 # experimental value that works well for most of the prints
    toolChangePurgeLength = float("%.2f" % (hotendPurgeMultiplier * baseToolChangeLength04))

    # F - Extrusion Speed -> adjusted to improve surplus material storage (maximum purge speed for the hotend's temperature):
    maxPrintSpeed = (max(1, temperatureValue(filament, hotend, layerHeight, speed) - filament['printTemperature'][0])/float(max(1, filament['printTemperature'][1]-filament['printTemperature'][0]))) * maxFlowValue(hotend, filament, layerHeight) / (hotend['nozzleSize']*layerHeight/60.)
    F = float("%.2f" % (maxPrintSpeed * hotend['nozzleSize'] * layerHeight / (math.pi * (filament['filamentDiameter']/2.)**2)))

    # S - Slope of the SmartPurge function (according to NSize, Flow, PurgeLength)
    distanceAtNozzleTip = hotendPurgeMultiplier * filament['purgeLength'] * filament['extrusionMultiplier']
    slopeCorrection = 0.005 # experimental value
    S = float("%.4f" % ((distanceAtNozzleTip * (hotend['nozzleSize']/2.)**2) / ((filament['filamentDiameter']/2.)**2) * slopeCorrection))

    # E - Maximum distance to purge (according to NSize, Flow)
    if hotend['nozzleSize'] >= 0.8:
        maxPurgeLength = (6 + 16)/2. # max length to purge (highFlow)
    else:
        maxPurgeLength = (6 + 12)/2. # max length to purge (standard)
    E = float("%.2f" % (maxPurgeLength * filament['extrusionMultiplier']))
    
    # P - Minimum distance to purge 
    P = float("%.4f" % ((minPurgeLength*filament['extrusionMultiplier']*(hotend['nozzleSize']/2.)**2) / ((filament['filamentDiameter']/2.)**2)))
    
    # P (testing value)
    P = 0

    return (startPurgeLength, toolChangePurgeLength, F, S, E, P)

def retractValues(filament):
    if filament['isFlexibleMaterial']:
        useCoasting = 0
        useWipe = 0
        onlyRetractWhenCrossingOutline = 1
        retractBetweenLayers = 0
        useRetractionMinTravel = 1
        retractWhileWiping = 1
        onlyWipeOutlines = 1
    else:
        useCoasting = 0
        useWipe = 0
        onlyRetractWhenCrossingOutline = 0
        retractBetweenLayers = 0
        useRetractionMinTravel = 1
        retractWhileWiping = 1
        onlyWipeOutlines = 1
    return useCoasting, useWipe, onlyRetractWhenCrossingOutline, retractBetweenLayers, useRetractionMinTravel, retractWhileWiping, onlyWipeOutlines

def coastValue(hotend, filament):
    return float("%.2f" % ((hotend['nozzleSize']/0.4)**2*filament['purgeLength']))

def maxFlowValue(hotend, filament, layerHeight):
    if hotend['nozzleSize'] <= 0.6:
        if filament['maxFlow'] == 'None':
            return hotend['nozzleSize']*layerHeight*filament['advisedMaxPrintSpeed']
        else:
            return filament['maxFlow']
    else:
        if filament['maxFlowForHighFlowHotend'] == 'None':
            if filament['maxFlow'] == 'None':
                return hotend['nozzleSize']*layerHeight*filament['advisedMaxPrintSpeed']
            else:
                return filament['maxFlow']
        else:
            return filament['maxFlowForHighFlowHotend']

def temperatureValue(filament, hotend, layerHeight, speed, base = 5):
    # adaptative temperature according to flow values. Rounded to base
    flow = hotend['nozzleSize']*layerHeight*float(speed)/60

    # Warning if something is not working properly
    if int(flow) > int(maxFlowValue(hotend, filament, layerHeight)):
        print "warning! you're trying to print at higher flow than allowed:", filament['id']+':', str(int(flow)), str(int(maxFlowValue(hotend, filament, layerHeight)))

    temperature = int(base * round((filament['printTemperature'][0] + flow/maxFlowValue(hotend, filament, layerHeight) * float(filament['printTemperature'][1]-filament['printTemperature'][0]))/float(base)))
    return temperature

def fanSpeed(filament, temperature, layerHeight, base = 5):
    # adaptative fan speed according to temperature values. Rounded to base
    if filament['printTemperature'][1] - filament['printTemperature'][0] == 0 or filament['fanPercentage'][1] == 0:
        fanSpeed = filament['fanPercentage'][0]
    else:
        fanSpeedForTemperature = int(base * round((filament['fanPercentage'][0] + (temperature-filament['printTemperature'][0])/float(filament['printTemperature'][1]-filament['printTemperature'][0])*float(filament['fanPercentage'][1]-filament['fanPercentage'][0]))/float(base)))
        LayerHeightAtMaxFanSpeed = 0.025
        LayerHeightAtMinFanSpeed = 0.2
        fanSpeedForLayerHeight = int(base * round((filament['fanPercentage'][0] + (layerHeight - LayerHeightAtMaxFanSpeed)/float(LayerHeightAtMinFanSpeed-LayerHeightAtMaxFanSpeed)*float(filament['fanPercentage'][1]-filament['fanPercentage'][0]))/float(base)))
        fanSpeed = max(fanSpeedForTemperature, fanSpeedForLayerHeight)
    return min(fanSpeed, 100) # Repassar. Aquest 100 no hauria de ser necessari

def timeVsTemperature(value, element, action, command):
    hotendParameter1 = 80
    hotendParameter2 = 310
    hotendParameter3 = 25
    bedParameterA1 = 51
    bedParameterA2 = 61
    bedParameterA3 = 19
    bedParameterB1 = 1000
    bedParameterB2 = 90
    bedParameterB3 = 47
    bedParameterB4 = 10

    # return needed time (sec) to reach Temperature (ºC)
    if command == 'getTime':
        temperature = value
        if action == 'heating':
            if element == 'M104 ':
                time = hotendParameter1 * math.log(-(hotendParameter2-hotendParameter3)/(float(temperature)-hotendParameter2))
            elif element == 'M140 ':
                if temperature <= 60:
                    time = bedParameterA1 * math.log(-(bedParameterA2-bedParameterA3)/(float(temperature)-bedParameterA2))
                else:
                    time = bedParameterB1 * math.log(-bedParameterB2/(float(temperature)-bedParameterB2-bedParameterB3))+bedParameterB4
        elif action == 'cooling':
            time = 0
        return max(0, time)

    # return temperature (ºC) reached after heating during given time (sec)
    elif command == 'getTemperature':
        time = value
        if action == 'heating':
            if element == 'M104 ':
                temperature = hotendParameter2 - (hotendParameter2 - hotendParameter3) * math.exp(-time/hotendParameter1)
            elif element == 'M140 ':
                if time <= 180:
                    temperature = bedParameterA2 - (bedParameterA2 - bedParameterA3) * math.exp(-time/bedParameterA1)
                else:
                    temperature = bedParameterB2 + bedParameterB3 - bedParameterB2 * math.exp(-(time - bedParameterB4)/bedParameterB1)
        elif action == 'cooling':
            temperature = 0
        return max(0, temperature)

def firstHeatSequence(leftHotendTemp, rightHotendTemp, bedTemp, software):
    startSequenceString = '; Start Heating Sequence. If you changed temperatures manually all elements may not heat in sync,'
    if software == 'Simplify3D':
        if leftHotendTemp > 0 and rightHotendTemp > 0:
            # IDEX
            timeLeftHotend  = (timeVsTemperature(leftHotendTemp,  'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S[extruder0_temperature]', ' T0,')
            timeRightHotend = (timeVsTemperature(rightHotendTemp, 'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S[extruder1_temperature]', ' T1,')
            timeBed         = (timeVsTemperature(bedTemp,         'M140 ', 'heating', 'getTime'), 'M140 ', 'M190 ', 'S[bed0_temperature]',       ',')
            startTimes = sorted([timeLeftHotend, timeRightHotend, timeBed])
            startSequenceString += startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-2][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
            startSequenceString += startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
            startSequenceString += startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-3][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
            startSequenceString += startTimes[-3][-4]+startTimes[-3][-2]+startTimes[-3][-1]
            startSequenceString += startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
            startSequenceString += startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
            startSequenceString += startTimes[-3][-3]+startTimes[-3][-2]+startTimes[-3][-1]
        else:
            if leftHotendTemp > 0:
                # MEX Left
                timeLeftHotend  = (timeVsTemperature(leftHotendTemp,  'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S[extruder0_temperature]', ' T0,')
                timeBed         = (timeVsTemperature(bedTemp,         'M140 ', 'heating', 'getTime'), 'M140 ', 'M190 ', 'S[bed0_temperature]',       ',')
                startTimes = sorted([timeLeftHotend, timeBed])
                startSequenceString += startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-2][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
                startSequenceString += startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
                startSequenceString += startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
                startSequenceString += startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
            else:
                # MEX Right
                timeRightHotend = (timeVsTemperature(rightHotendTemp, 'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S[extruder1_temperature]', ' T1,')
                timeBed         = (timeVsTemperature(bedTemp,         'M140 ', 'heating', 'getTime'), 'M140 ', 'M190 ', 'S[bed0_temperature]',       ',')
                startTimes = sorted([timeRightHotend, timeBed])
                startSequenceString += startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-2][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
                startSequenceString += startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
                startSequenceString += startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
                startSequenceString += startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
    elif software == 'Cura':
        startSequenceString = '\t;' + startSequenceString[2:-1] + '\n'
        if leftHotendTemp > 0 and rightHotendTemp > 0:
            # IDEX
            timeLeftHotend  = (timeVsTemperature(leftHotendTemp,  'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S{print_temperature}',     ' T0\n')
            timeRightHotend = (timeVsTemperature(rightHotendTemp, 'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S{print_temperature2}',    ' T1\n')
            timeBed         = (timeVsTemperature(bedTemp,         'M140 ', 'heating', 'getTime'), 'M140 ', 'M190 ', 'S{print_bed_temperature}', '\n')
            startTimes = sorted([timeLeftHotend, timeRightHotend, timeBed])
            startSequenceString += '\t'+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-2][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
            startSequenceString += '\t'+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
            startSequenceString += '\t'+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-3][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
            startSequenceString += '\t'+startTimes[-3][-4]+startTimes[-3][-2]+startTimes[-3][-1]
            startSequenceString += '\t'+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
            startSequenceString += '\t'+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
            startSequenceString += '\t'+startTimes[-3][-3]+startTimes[-3][-2]+startTimes[-3][-1]
        else:
            if leftHotendTemp > 0:
                # MEX Left
                timeLeftHotend = (timeVsTemperature(leftHotendTemp, 'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S{print_temperature}',     ' T0\n')
                timeBed        = (timeVsTemperature(bedTemp,        'M140 ', 'heating', 'getTime'), 'M140 ', 'M190 ', 'S{print_bed_temperature}', '\n')
                startTimes = sorted([timeLeftHotend, timeBed])
                startSequenceString += '\t'+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-2][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
                startSequenceString += '\t'+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
                startSequenceString += '\t'+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
                startSequenceString += '\t'+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
            else:
                # MEX Right
                timeRightHotend = (timeVsTemperature(rightHotendTemp, 'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S{print_temperature2}', ' T1\n')
                timeBed         = (timeVsTemperature(bedTemp,         'M140 ', 'heating', 'getTime'), 'M140 ', 'M190 ', 'S{print_bed_temperature}',       '\n')
                startTimes = sorted([timeRightHotend, timeBed])
                startSequenceString += '\t'+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-2][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
                startSequenceString += '\t'+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
                startSequenceString += '\t'+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
                startSequenceString += '\t'+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
    elif software == 'Cura2':

        # Using Cura 2.5.0 the only labels we know to point to extruder being used are:
        #   adhesion_extruder_nr
        #   support_infill_extruder_nr
        #   support_extruder_nr
        #   support_interface_extruder_nr

        startSequenceString = r'\n;' + startSequenceString[2:-1] + r'\n'
        if leftHotendTemp > 0 and rightHotendTemp > 0:
            # IDEX
            timeLeftHotend  = (timeVsTemperature(leftHotendTemp,  'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S{material_print_temperature_layer_0}',     r' T0\n')
            timeRightHotend = (timeVsTemperature(rightHotendTemp, 'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S{material_print_temperature_layer_0}',    r' T1\n')
            timeBed         = (timeVsTemperature(bedTemp,         'M140 ', 'heating', 'getTime'), 'M140 ', 'M190 ', 'S{material_bed_temperature}', r'\n')
            startTimes = sorted([timeLeftHotend, timeRightHotend, timeBed])
            startSequenceString += startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-2][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
            startSequenceString += startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
            startSequenceString += startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-3][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
            startSequenceString += startTimes[-3][-4]+startTimes[-3][-2]+startTimes[-3][-1]
            startSequenceString += startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
            startSequenceString += startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
            startSequenceString += startTimes[-3][-3]+startTimes[-3][-2]+startTimes[-3][-1]
        else:
            if leftHotendTemp > 0:
                # MEX Left
                timeLeftHotend = (timeVsTemperature(leftHotendTemp, 'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S{material_print_temperature_layer_0}',     r' T{adhesion_extruder_nr}\n')
                timeBed        = (timeVsTemperature(bedTemp,        'M140 ', 'heating', 'getTime'), 'M140 ', 'M190 ', 'S{material_bed_temperature}', r'\n')
                startTimes = sorted([timeLeftHotend, timeBed])
                startSequenceString += startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-2][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
                startSequenceString += startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
                startSequenceString += startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
                startSequenceString += startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
            else:
                # MEX Right
                timeRightHotend = (timeVsTemperature(rightHotendTemp, 'M104 ', 'heating', 'getTime'), 'M104 ', 'M109 ', 'S{material_print_temperature_layer_0}', r' T{adhesion_extruder_nr}\n')
                timeBed         = (timeVsTemperature(bedTemp,         'M140 ', 'heating', 'getTime'), 'M140 ', 'M190 ', 'S{material_bed_temperature}',       r'\n')
                startTimes = sorted([timeRightHotend, timeBed])
                startSequenceString += startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][0]-startTimes[-2][0], startTimes[-1][-4], 'heating', 'getTemperature')))+startTimes[-1][-1]
                startSequenceString += startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
                startSequenceString += startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
                startSequenceString += startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
    return startSequenceString

def accelerationForPerimeters(nozzleSize, layerHeight, outerWallSpeed, base = 5, multiplier = 30000, defaultAcceleration = 2000):
    return min(defaultAcceleration, int(base * round((nozzleSize * layerHeight * multiplier * 1/(outerWallSpeed**(1/2.)))/float(base))))

def speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, action):
    if action == 'MEX Left' or action == 'IDEX, Infill with Right' or action == 'IDEX, Supports with Right':
        leftExtruderDefaultSpeed = quality['defaultSpeed']*speedMultiplier(hotendLeft, filamentLeft)
        leftExtruderMaxSpeedAtMaxFlow = maxFlowValue(hotendLeft, filamentLeft, currentLayerHeight)/(hotendLeft['nozzleSize']*currentLayerHeight)
        if action == 'IDEX, Infill with Right':
            rightExtruderMaxSpeedAtMaxFlow = maxFlowValue(hotendRight, filamentRight, currentInfillLayerInterval*currentLayerHeight)/(currentInfillLayerInterval*currentLayerHeight*hotendRight['nozzleSize'])
        else:
            rightExtruderMaxSpeedAtMaxFlow = leftExtruderMaxSpeedAtMaxFlow
        if action == 'MEX Left':
            currentDefaultSpeed = int(str(float(min(leftExtruderDefaultSpeed, leftExtruderMaxSpeedAtMaxFlow, rightExtruderMaxSpeedAtMaxFlow, filamentLeft['advisedMaxPrintSpeed'])*60)).split('.')[0])
        else:
            currentDefaultSpeed = int(str(float(min(leftExtruderDefaultSpeed, leftExtruderMaxSpeedAtMaxFlow, rightExtruderMaxSpeedAtMaxFlow, filamentLeft['advisedMaxPrintSpeed'], filamentRight['advisedMaxPrintSpeed'])*60)).split('.')[0])
        maxAllowedUnderspeed = maxFlowValue(hotendLeft, filamentLeft, currentLayerHeight)/(currentLayerHeight*hotendLeft['nozzleSize']*float(currentDefaultSpeed)/60)
        
        if filamentLeft['isFlexibleMaterial']:
            currentFirstLayerUnderspeed = 1.00
            currentOutlineUnderspeed = 1.00
        else:
            currentFirstLayerUnderspeed = float("%.2f" % min(maxAllowedUnderspeed, leftExtruderDefaultSpeed*60*quality['firstLayerUnderspeed'] /float(currentDefaultSpeed)))
            currentOutlineUnderspeed    = float("%.2f" % min(maxAllowedUnderspeed, leftExtruderDefaultSpeed*60*quality['outlineUnderspeed']    /float(currentDefaultSpeed)))

        if action == 'IDEX, Supports with Right':
            currentSupportUnderspeed    = float("%.2f" % min(maxAllowedUnderspeed, maxFlowValue(hotendRight, filamentRight, currentLayerHeight)/float(layerHeight(hotendLeft, quality)*hotendRight['nozzleSize']*currentDefaultSpeed/60.)))
        else:
            currentSupportUnderspeed    = float("%.2f" % min(maxAllowedUnderspeed, leftExtruderDefaultSpeed*60*0.9                             /float(currentDefaultSpeed)))

    elif action == 'MEX Right' or action == 'IDEX, Infill with Left' or action == 'IDEX, Supports with Left':
        rightExtruderDefaultSpeed = quality['defaultSpeed']*speedMultiplier(hotendRight, filamentRight)
        rightExtruderMaxSpeedAtMaxFlow = maxFlowValue(hotendRight, filamentRight, currentLayerHeight)/(hotendRight['nozzleSize']*currentLayerHeight)
        if action == 'IDEX, Infill with Left':
            leftExtruderMaxSpeedAtMaxFlow = maxFlowValue(hotendLeft, filamentLeft, currentInfillLayerInterval*currentLayerHeight)/(currentInfillLayerInterval*currentLayerHeight*hotendLeft['nozzleSize'])
        else:
            leftExtruderMaxSpeedAtMaxFlow = rightExtruderMaxSpeedAtMaxFlow
        if action == 'MEX Right':
            currentDefaultSpeed = int(str(float(min(rightExtruderDefaultSpeed, rightExtruderMaxSpeedAtMaxFlow, leftExtruderMaxSpeedAtMaxFlow, filamentRight['advisedMaxPrintSpeed'])*60)).split('.')[0])
        else:
            currentDefaultSpeed = int(str(float(min(rightExtruderDefaultSpeed, rightExtruderMaxSpeedAtMaxFlow, leftExtruderMaxSpeedAtMaxFlow, filamentLeft['advisedMaxPrintSpeed'], filamentRight['advisedMaxPrintSpeed'])*60)).split('.')[0])
        maxAllowedUnderspeed = maxFlowValue(hotendRight, filamentRight, currentLayerHeight)/(currentLayerHeight*hotendRight['nozzleSize']*float(currentDefaultSpeed)/60)

        if filamentRight['isFlexibleMaterial']:
            currentFirstLayerUnderspeed = 1.00
            currentOutlineUnderspeed = 1.00
        else:
            currentFirstLayerUnderspeed = float("%.2f" % min(maxAllowedUnderspeed, rightExtruderDefaultSpeed*60*quality['firstLayerUnderspeed']/float(currentDefaultSpeed)))
            currentOutlineUnderspeed    = float("%.2f" % min(maxAllowedUnderspeed, rightExtruderDefaultSpeed*60*quality['outlineUnderspeed']   /float(currentDefaultSpeed)))

        if action == 'IDEX, Supports with Left':
            currentSupportUnderspeed    = float("%.2f" % min(maxAllowedUnderspeed, maxFlowValue(hotendLeft, filamentLeft, currentLayerHeight)  /float(hotendRight['nozzleSize']*quality['layerHeightMultiplier']*hotendLeft['nozzleSize']*currentDefaultSpeed/60.)))
        else:
            currentSupportUnderspeed    = float("%.2f" % min(maxAllowedUnderspeed, rightExtruderDefaultSpeed*60*0.9                            /float(currentDefaultSpeed)))
    return currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed

def testAllCombinations():

    # Calculate All profiles available for each software
    totalSmaProfiles = (len(profilesData['hotend'])-1) *  len(profilesData['filament']) * 2
    totalBigProfiles = (len(profilesData['hotend'])-1)**2 * len(profilesData['filament'])**2
    realSimplify3DProfilesAvailable = totalSmaProfiles + totalBigProfiles

    nozzleSizes = []
    for hotend in sorted(profilesData['hotend'], key=lambda k: k['id'])[:-1]:
        nozzleSizes.append(hotend['nozzleSize'])
    curaGroupedSizes = {x:nozzleSizes.count(x) for x in nozzleSizes}
    curaIDEXHotendsCombinations = 0
    for size in curaGroupedSizes:
        curaIDEXHotendsCombinations += curaGroupedSizes[size]**2

    realCuraProfilesAvailable = (totalSmaProfiles + curaIDEXHotendsCombinations * len(profilesData['filament'])**2) * len(profilesData['quality'])

    # Start iteration
    combinationCount = 0
    totalSimplify3DProfilesAvailable = len(profilesData['hotend'])**2 * len(profilesData['filament'])**2
    for hotendLeft in sorted(profilesData['hotend'], key=lambda k: k['id']):
        for hotendRight in sorted(profilesData['hotend'], key=lambda k: k['id']):
            for filamentLeft in sorted(profilesData['filament'], key=lambda k: k['id']):
                for filamentRight in sorted(profilesData['filament'], key=lambda k: k['id']):
                    createSimplify3DProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, 'noData', 'nothing')
                    combinationCount += 1
                    sys.stdout.write("\r\t\tTesting Simplify3D Profiles: %d%%" % int(float(combinationCount)/totalSimplify3DProfilesAvailable*100))
                    sys.stdout.flush()
    print '\r\t\tTesting Simplify3D Profiles: OK. Profiles tested: '+str(realSimplify3DProfilesAvailable)
    combinationCount = 0
    totalProfilesAvailable = len(profilesData['hotend'])**2 * len(profilesData['filament'])**2 * len(profilesData['quality'])
    for hotendLeft in sorted(profilesData['hotend'], key=lambda k: k['id']):
        for hotendRight in sorted(profilesData['hotend'], key=lambda k: k['id']):
            for filamentLeft in sorted(profilesData['filament'], key=lambda k: k['id']):
                for filamentRight in sorted(profilesData['filament'], key=lambda k: k['id']):
                    for quality in sorted(profilesData['quality'], key=lambda k: k['index']):
                        createCuraProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, 'noData', 'nothing')
                        combinationCount += 1
                        sys.stdout.write("\r\t\tTesting Cura Profiles:       %d%%" % int(float(combinationCount)/totalProfilesAvailable*100))
                        sys.stdout.flush()
    print '\r\t\tTesting Cura Profiles:       OK. Profiles Tested: '+str(realCuraProfilesAvailable)

    print '\t\tAll '+str(realSimplify3DProfilesAvailable + realCuraProfilesAvailable)+' profiles can be generated!\n'

def selectHotendAndFilament(extruder, header):
    clearDisplay()
    print header
    print "\n\tSelect Sigma's "+extruder+" Hotend (1-"+str(len(profilesData['hotend']))+'):'
    answer0 = ''
    hotendOptions = []
    for c in range(len(profilesData['hotend'])):
        hotendOptions.append(str(c+1))
    materialOptions = []
    for c in range(len(profilesData['filament'])):
        materialOptions.append(str(c+1))
    for hotend in range(len(profilesData['hotend'])):
        print '\t'+str(hotend+1)+'. '+sorted(profilesData['hotend'], key=lambda k: k['id'])[hotend]['id']
    while answer0 not in hotendOptions:
        answer0 = raw_input('\t')
    print '\t'+extruder+' Hotend: '+sorted(profilesData['hotend'], key=lambda k: k['id'])[int(answer0)-1]['id']
    if answer0 != str(int(hotendOptions[-1])):
        clearDisplay()
        print header
        print "\n\tSelect Sigma's "+extruder+" Extruder Loaded Filament (1-"+str(len(profilesData['filament']))+'):'
        answer1 = ''
        for material in range(len(profilesData['filament'])):
            print '\t'+str(material+1)+'. '+sorted(profilesData['filament'], key=lambda k: k['id'])[material]['id']
        while answer1 not in materialOptions:
            answer1 = raw_input('\t')
        print '\t'+extruder+' Extruder Filament: '+sorted(profilesData['filament'], key=lambda k: k['id'])[int(answer1)-1]['id']+'.'
    else:
        answer1 = '1'
    return (int(answer0)-1, int(answer1)-1)

def selectQuality(header):
    clearDisplay()
    print header
    print "\n\tSelect Quality:"
    answer0 = ''
    qualityOptions = []
    for c in range(len(profilesData['quality'])):
        qualityOptions.append(str(c+1))
    for quality in range(len(profilesData['quality'])):
        print '\t'+str(quality+1)+'. '+sorted(profilesData['quality'], key=lambda k: k['index'])[quality]['id']
    while answer0 not in qualityOptions:
        answer0 = raw_input('\t')
    print '\tQuality: '+sorted(profilesData['quality'], key=lambda k: k['index'])[int(answer0)-1]['id']
    return int(answer0)-1   

def validArguments():
    if len(sys.argv) > 1:
        if sys.argv[-1] == '--cura' and (len(sys.argv) == 7 or len(sys.argv) == 8):
            leftHotend = sys.argv[1]+'.json' in os.listdir('./Profiles Data/Hotends') or sys.argv[1] == 'None'
            rightHontend = sys.argv[2]+'.json' in os.listdir('./Profiles Data/Hotends') or sys.argv[2] == 'None'
            leftFilament = sys.argv[3]+'.json' in os.listdir('./Profiles Data/Filaments') or (sys.argv[1] == 'None' and sys.argv[3] == 'None')
            rightFilament = sys.argv[4]+'.json' in os.listdir('./Profiles Data/Filaments') or (sys.argv[2] == 'None' and sys.argv[4] == 'None')
            quality = sys.argv[5]+'.json' in os.listdir('./Profiles Data/Quality Presets')
            if len(sys.argv) == 8:
                fileAction = sys.argv[6] == '--no-file' or sys.argv[6] == '--only-filename'
                return leftHotend and rightHontend and leftFilament and rightFilament and quality and fileAction
            else:
                return leftHotend and rightHontend and leftFilament and rightFilament and quality
        elif sys.argv[-1] == '--simplify3d' and (len(sys.argv) == 6 or len(sys.argv) == 7):
            leftHotend = sys.argv[1]+'.json' in os.listdir('./Profiles Data/Hotends') or sys.argv[1] == 'None'
            rightHontend = sys.argv[2]+'.json' in os.listdir('./Profiles Data/Hotends') or sys.argv[2] == 'None'
            leftFilament = sys.argv[3]+'.json' in os.listdir('./Profiles Data/Filaments') or (sys.argv[1] == 'None' and sys.argv[3] == 'None')
            rightFilament = sys.argv[4]+'.json' in os.listdir('./Profiles Data/Filaments') or (sys.argv[2] == 'None' and sys.argv[4] == 'None')       
            if len(sys.argv) == 7:
                fileAction = sys.argv[5] == '--no-file' or sys.argv[5] == '--only-filename'
                return leftHotend and rightHontend and leftFilament and rightFilament and fileAction
            else:
                return leftHotend and rightHontend and leftFilament and rightFilament           
        else:
            return False
    else:
        return False

def readProfilesData():
    global profilesData
    profilesData = dict([("hotend", []), ("filament", []), ("quality", [])])
    for hotend in os.listdir('./Profiles Data/Hotends'):
        if hotend[-5:] == '.json':
            with open('./Profiles Data/Hotends/'+hotend) as hotend_file:    
                hotendData = json.load(hotend_file)
                profilesData['hotend'].append(hotendData)
    profilesData['hotend'].append(dict([('id', 'None')]))
    for filament in os.listdir('./Profiles Data/Filaments'):
        if filament[-5:] == '.json':
            with open('./Profiles Data/Filaments/'+filament) as filament_file:    
                filamentData = json.load(filament_file)
                profilesData['filament'].append(filamentData)
    for quality in os.listdir('./Profiles Data/Quality Presets'):
        if quality[-5:] == '.json':
            with open('./Profiles Data/Quality Presets/'+quality) as quality_file:    
                qualityData = json.load(quality_file)
                profilesData['quality'].append(qualityData)

def writeData(extruder, currentDefaultSpeed, currentInfillLayerInterval, currentLayerHeight, hotendLeft, hotendRight, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder, filamentLeft, filamentRight, quality, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed, currentFirstLayerHeightPercentage, hotendLeftTemperature, hotendRightTemperature, currentBedTemperature, dataLog):
    if extruder == 'Left Extruder':
        printA = "%.2f" % (float(currentDefaultSpeed)/60*currentInfillLayerInterval*currentLayerHeight*hotendLeft['nozzleSize'])
        printB = ""
    elif extruder == 'Right Extruder':
        printA = ""
        printB = "%.2f" % (float(currentDefaultSpeed)/60*currentInfillLayerInterval*currentLayerHeight*hotendRight['nozzleSize'])
    else:
        # IDEX
        if filamentLeft['isSupportMaterial'] != filamentRight['isSupportMaterial']:
            if filamentLeft['isSupportMaterial']:
                supportMaterialLoadedLeft  = float(currentSupportUnderspeed)
                supportMaterialLoadedRight = 1
            else:
                supportMaterialLoadedLeft  = 1
                supportMaterialLoadedRight = float(currentSupportUnderspeed)
        else:
            supportMaterialLoadedLeft  = 1
            supportMaterialLoadedRight = 1
        if hotendLeft['nozzleSize'] != hotendRight['nozzleSize']:
            if currentPrimaryExtruder == 0: 
                printA = "%.2f" % (float(currentDefaultSpeed)/60*currentLayerHeight*hotendLeft['nozzleSize']*supportMaterialLoadedLeft)
                printB = "%.2f" % (float(currentDefaultSpeed)/60*currentInfillLayerInterval*currentLayerHeight*hotendRight['nozzleSize']*supportMaterialLoadedRight)
            else:
                printA = "%.2f" % (float(currentDefaultSpeed)/60*currentLayerHeight*currentInfillLayerInterval*hotendLeft['nozzleSize']*supportMaterialLoadedLeft)
                printB = "%.2f" % (float(currentDefaultSpeed)/60*currentLayerHeight*hotendRight['nozzleSize']*supportMaterialLoadedRight)
        else:
            printA = "%.2f" % (float(currentDefaultSpeed)/60*1*currentLayerHeight*hotendLeft['nozzleSize']*supportMaterialLoadedLeft)
            printB = "%.2f" % (float(currentDefaultSpeed)/60*currentInfillLayerInterval*currentLayerHeight*hotendRight['nozzleSize']*supportMaterialLoadedRight)

        if currentPrimaryExtruder == 0:
            printA = "%.2f" % max(float(printA), float(printA) * currentOutlineUnderspeed, float(printA) * currentFirstLayerHeightPercentage/100. * currentFirstLayerUnderspeed)
        else:
            printB = "%.2f" % max(float(printB), float(printB) * currentOutlineUnderspeed, float(printB) * currentFirstLayerHeightPercentage/100. * currentFirstLayerUnderspeed)


    dataLog.append(filamentLeft['id']+";"+filamentRight['id']+";"+extruder+";"+quality['id']+";"+hotendLeft['id']+";"+hotendRight['id']+";"+'T'+str(currentInfillExtruder)+";"+'T'+str(currentPrimaryExtruder)+";"+'T'+str(currentSupportExtruder)+";"+str(printA)+";"+str(printB)+";"+str(currentInfillLayerInterval)+";"+("%.2f" % (currentDefaultSpeed/60.))+";"+str(currentFirstLayerUnderspeed)+";"+str(currentOutlineUnderspeed)+";"+str(currentSupportUnderspeed)+";"+str(currentFirstLayerHeightPercentage)+";"+str(hotendLeftTemperature)+";"+str(hotendRightTemperature)+";"+str(currentBedTemperature)+";\n")

def clearDisplay():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def main():
    if platform.system() == 'Windows':
        # os.system('color f0')
        os.system('mode con: cols=154 lines=35')
    if validArguments():
        readProfilesData()
        for hotend in os.listdir('./Profiles Data/Hotends'):
            if hotend == sys.argv[1]+'.json':
                with open('./Profiles Data/Hotends/'+hotend) as hotend_file:    
                    leftHotend = json.load(hotend_file)
            if hotend == sys.argv[2]+'.json':
                with open('./Profiles Data/Hotends/'+hotend) as hotend_file:    
                    rightHotend = json.load(hotend_file)
        for filament in os.listdir('./Profiles Data/Filaments'):
            if filament == sys.argv[3]+'.json':
                with open('./Profiles Data/Filaments/'+filament) as filament_file:    
                    leftFilament = json.load(filament_file)
            if filament == sys.argv[4]+'.json':
                with open('./Profiles Data/Filaments/'+filament) as filament_file:    
                    rightFilament = json.load(filament_file)
        if sys.argv[1] == 'None':
            leftHotend = dict([('id', 'None')])
        if sys.argv[2] == "None":
            rightHotend = dict([('id', 'None')])
        if sys.argv[3] == 'None':
            leftFilament = profilesData['filament'][0]
        if sys.argv[4] == 'None':
            rightFilament = profilesData['filament'][0]
        if sys.argv[-1] == '--simplify3d':
            if len(sys.argv) == 7:
                if sys.argv[5] == '--no-file' or sys.argv[5] == '--only-filename':
                    createSimplify3DProfile(leftHotend, rightHotend, leftFilament, rightFilament, 'noData', sys.argv[5])
            else:
                createSimplify3DProfile(leftHotend, rightHotend, leftFilament, rightFilament, 'noData', 'createFile')
        elif sys.argv[-1] == '--cura':
            for quality in os.listdir('./Profiles Data/Quality Presets'):
                if quality == sys.argv[5]+'.json':
                    with open('./Profiles Data/Quality Presets/'+quality) as quality_file:    
                        qualityCura = json.load(quality_file)
            if len(sys.argv) == 8:
                if sys.argv[6] == '--no-file' or sys.argv[6] == '--only-filename':
                    createCuraProfile(leftHotend, rightHotend, leftFilament, rightFilament, qualityCura, 'noData', sys.argv[6])
            else:
                createCuraProfile(leftHotend, rightHotend, leftFilament, rightFilament, qualityCura, 'noData', 'createFile')
    else:
        if len(sys.argv) == 1:
            experimentalMenu = False
            while True:
                clearDisplay()
                print '\n Welcome to the BCN3D Sigma Profile Generator ('+str(SigmaProgenVersion)+') \n'
                print ' Choose one option (1-4):'
                print ' 1. Profile for Simplify3D'
                print ' 2. Profile for Cura'
                print ' 3. Experimental features'
                print ' 4. Exit'
                if experimentalMenu:
                    x = '3'
                else: 
                    x = 'x'
                y = 'y'
                while x not in ['1','2','3','4']:
                    x = raw_input(' ')
                dataLog = ["LFilament;RFilament;Extruder;Quality;LNozzle;RNozzle;InfillExt;PrimaryExt;SupportExt;LFlow;RFlow;Layers/Infill;DefaultSpeed;FirstLayerUnderspeed;OutLineUnderspeed;SupportUnderspeed;FirstLayerHeightPercentage;LTemp;RTemp;BTemp;\n"]
                profilesCreatedCount = 0
                readProfilesData()

                if x == '3':
                    clearDisplay()
                    print '\n Welcome to the BCN3D Sigma Profile Generator \n\n\n\n'
                    print '    Experimental features'
                    print '\n\tChoose one option (1-6):'
                    print '\t1. Generate a bundle of profiles - Simplify3D'
                    print '\t2. Generate a bundle of profiles - Cura'
                    print '\t3. Test all combinations'
                    print '\t4. MacOS Only - Slice a model (with Cura)'
                    print '\t5. Add the Sigma to Cura 2'
                    print '\t6. Back'
                    x2 = 'x'
                    while x2 not in ['1','2','3','4', '5', '6', '7']:
                        x2 = raw_input('\t')

                singleProfileSimplify3D, singleProfileCura, bundleProfilesSimplify3D, bundleProfilesCura, testComb, sliceModel, cura2Files = False, False, False, False, False, False, False

                if x == '1':
                    singleProfileSimplify3D = True
                    GUIHeader = '\n Welcome to the BCN3D Sigma Profile Generator \n\n\n    Profile for Simplify3D'
                elif x == '2':
                    singleProfileCura = True
                    GUIHeader = '\n Welcome to the BCN3D Sigma Profile Generator \n\n\n\n    Profile for Cura'
                elif x == '3':
                    experimentalMenu = True               
                    if x2 == '1':
                        bundleProfilesSimplify3D = True
                        GUIHeader = '\n Welcome to the BCN3D Sigma Profile Generator \n\n\n\n\n    Experimental features\n\n\n\t   Generate a bundle of profiles - Simplify3D\n'
                    elif x2 == '2':
                        bundleProfilesCura = True
                        GUIHeader = '\n Welcome to the BCN3D Sigma Profile Generator \n\n\n\n\n    Experimental features\n\n\n\n\t   Generate a bundle of profiles - Cura\n'
                    elif x2 == '3':
                        testComb = True
                        GUIHeader = '\n Welcome to the BCN3D Sigma Profile Generator \n\n\n\n\n    Experimental features\n\n\n\n\n\t   Test all combinations\n'
                    elif x2 == '4':
                        sliceModel = True
                        GUIHeader = '\n Welcome to the BCN3D Sigma Profile Generator \n\n\n\n\n    Experimental features\n\n\n\n\n\n\t   MacOS Only - Slice a model (with Cura)'
                    elif x2 == '5':
                        cura2Files = True
                        GUIHeader = '\n Welcome to the BCN3D Sigma Profile Generator \n\n\n\n\n    Experimental features\n\n\n\n\n\n\n\t   Add the Sigma to Cura 2'
                    elif x2 == '6':
                        experimentalMenu = False
                elif x == '4':
                    if platform.system() != 'Windows':
                        print '\n Until next time!\n'
                    break

                if bundleProfilesSimplify3D or bundleProfilesCura or singleProfileSimplify3D or singleProfileCura:
                    if bundleProfilesSimplify3D:
                        clearDisplay()
                        print GUIHeader
                        profilesCreatedCount = createSimplify3DProfilesBundle(dataLog, profilesCreatedCount)
                    elif bundleProfilesCura:
                        clearDisplay()
                        print GUIHeader
                        profilesCreatedCount = createCuraProfilesBundle(dataLog, profilesCreatedCount)
                    elif singleProfileSimplify3D or singleProfileCura:
                        a = selectHotendAndFilament('Left', GUIHeader)
                        b = selectHotendAndFilament('Right', GUIHeader)
                        clearDisplay()
                        print GUIHeader
                        if sorted(profilesData['hotend'], key=lambda k: k['id'])[a[0]]['id'] == 'None' and sorted(profilesData['hotend'], key=lambda k: k['id'])[b[0]]['id'] == 'None':
                            raw_input("\n\tSelect at least one hotend to create a profile. Press Enter to continue...")
                        else:
                            if singleProfileSimplify3D:
                                print "\n\tYour new Simplify3D profile '"+createSimplify3DProfile(sorted(profilesData['hotend'], key=lambda k: k['id'])[a[0]], sorted(profilesData['hotend'], key=lambda k: k['id'])[b[0]], sorted(profilesData['filament'], key=lambda k: k['id'])[a[1]], sorted(profilesData['filament'], key=lambda k: k['id'])[b[1]], dataLog, 'createFile')+"' has been created."
                                profilesCreatedCount = 1
                            elif singleProfileCura:
                                makeProfile = True
                                if sorted(profilesData['hotend'], key=lambda k: k['id'])[a[0]]['id'] != 'None' and sorted(profilesData['hotend'], key=lambda k: k['id'])[b[0]]['id'] != 'None':
                                    if sorted(profilesData['hotend'], key=lambda k: k['id'])[a[0]]['nozzleSize'] != sorted(profilesData['hotend'], key=lambda k: k['id'])[b[0]]['nozzleSize']:
                                        raw_input("\n\tSelect two hotends with the same nozzle size to create a Cura profile. Press Enter to continue...")
                                        makeProfile = False
                                    elif sorted(profilesData['filament'], key=lambda k: k['id'])[a[1]]['isSupportMaterial'] and not sorted(profilesData['filament'], key=lambda k: k['id'])[b[1]]['isSupportMaterial']:
                                        raw_input("\n\tTo make IDEX prints with Cura using support material, please load the support material to the Right Extruder. Press Enter to continue...")
                                        makeProfile = False
                                if makeProfile:
                                    c = selectQuality(GUIHeader)
                                    clearDisplay()
                                    print GUIHeader
                                    if singleProfileCura:
                                        print "\n\tYour new Cura profile '"+createCuraProfile(sorted(profilesData['hotend'], key=lambda k: k['id'])[a[0]], sorted(profilesData['hotend'], key=lambda k: k['id'])[b[0]], sorted(profilesData['filament'], key=lambda k: k['id'])[a[1]], sorted(profilesData['filament'], key=lambda k: k['id'])[b[1]], sorted(profilesData['quality'], key=lambda k: k['index'])[c], dataLog, 'createFile')+"' has been created.\n"
                                        print "\tNOTE: To reduce the Ringing effect use the RingingRemover plugin by BCN3D.\n"
                                        profilesCreatedCount = 1

                    if profilesCreatedCount > 0:
                        while y not in ['Y', 'n']:
                            y = raw_input('\tSee profile(s) data? (Y/n) ')
                    if y == 'Y':
                        for l in dataLog:
                            print '\t',
                            for d in string.split(l, ';'):
                                print string.rjust(str(d)[:6], 6),
                        print '\t'+str(profilesCreatedCount)+' profile(s) created with '+str(len(dataLog)-1)+' configurations.\n'
                        raw_input("\tPress Enter to continue...")
                    elif y == 'n':
                        print ''
                elif sliceModel:
                    clearDisplay()
                    print GUIHeader
                    if platform.system() == 'Windows':
                        raw_input("\n\t\tThis feature is not available yet on Windows.\n\t\tPress Enter to continue...")
                    else:
                        if platform.system() == 'Windows':
                            profileFile = raw_input('\n\t\tDrag & Drop your .ini profile to this window. Then press Enter.\n\t\t').replace('"', '')
                            stlFile = raw_input('\n\t\tDrag & Drop your .stl model file to this window. Then press Enter.\n\t\t').replace('"', '')
                        else:
                            profileFile = raw_input('\n\t\tDrag & Drop your .ini profile to this window. Then press Enter.\n\t\t')[:-1].replace('\\', '')
                            stlFile = raw_input('\n\t\tDrag & Drop your .stl model file to this window. Then press Enter.\n\t\t')[:-1].replace('\\', '')
                        os.chdir('..')
                        gcodeFile = stlFile[:-4]+'.gcode'
                        os.system(r'/Applications/Cura/Cura-BCN3D.app/Contents/MacOS/Cura-BCN3D -i "'+profileFile+r'" -s "'+stlFile+r'" -o "'+gcodeFile+r'"')
                        raw_input("\n\t\tYour gcode file '"+string.split(stlFile, '/')[-1][:-4]+'.gcode'+"' has been created! Find it in the same folder as the .stl file.\n\t\tPress Enter to continue...")
                elif testComb:
                    clearDisplay()
                    print GUIHeader              
                    testAllCombinations()
                    raw_input("\t\tPress Enter to continue...")
                elif cura2Files:
                    clearDisplay()
                    print GUIHeader
                    createCura2Files()
                    installCura2Files()

                    # #remove after debug
                    # if platform.system() == 'Darwin':
                    #     if "cura.log" in os.listdir('/Users/Guillem/Library/Application Support/cura'):             
                    #         os.remove('/Users/Guillem/Library/Application Support/cura/cura.log')
                    #     return
                    # #remove after debug
                    
                    raw_input("\t\tPress Enter to continue...")

if __name__ == '__main__':
    main() 