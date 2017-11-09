#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - May 2017
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

import math
import uuid

import ProgenSettings as PS
import Logger

def simplify3DProfile(hotendLeft, hotendRight, filamentLeft, filamentRight):
    fff = []
    fff.append('<?xml version="1.0" encoding="utf-8"?>')
    for q in PS.profilesData['quality']:
        if q['id'] == 'Standard':
            defaultPrintQualityBase = 'Standard'
            break
        else:
            defaultPrintQualityBase = PS.profilesData['quality'][0]['id']
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
    fff.append('<profile name="'+fileName+'" version="ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+')" app="S3D-Software 3.1.1">')
    fff.append('  <baseProfile></baseProfile>')
    fff.append('  <printMaterial></printMaterial>')
    fff.append('  <printQuality>'+defaultPrintQuality+'</printQuality>') #+extruder+secondaryExtruderAction+str(quality['id'])+
    if hotendLeft['id'] != 'None':
        fff.append('  <printExtruders>Left Extruder Only</printExtruders>')
    else:
        fff.append('  <printExtruders>Right Extruder Only</printExtruders>')        
    if hotendLeft['id'] != 'None':
        fff.append('  <extruder name="Left Extruder '+str(hotendLeft['nozzleSize'])+'">')
        fff.append('    <toolheadNumber>0</toolheadNumber>')
        fff.append('    <diameter>'+str(hotendLeft['nozzleSize'])+'</diameter>')
        fff.append('    <autoWidth>0</autoWidth>')
        fff.append('    <width>'+str(hotendLeft['nozzleSize'])+'</width>')
        fff.append('    <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+'</extrusionMultiplier>')
        fff.append('    <useRetract>1</useRetract>')
        fff.append('    <retractionDistance>'+str(filamentLeft['retractionDistance'])+'</retractionDistance>')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>')
        fff.append('    <retractionZLift>0.05</retractionZLift>')
        fff.append('    <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+'</retractionSpeed>')
        fff.append('    <useCoasting>0</useCoasting>')
        fff.append('    <coastingDistance>0.2</coastingDistance>')
        fff.append('    <useWipe>1</useWipe>')
        fff.append('    <wipeDistance>5</wipeDistance>')
        fff.append('  </extruder>')
    else:
        fff.append('  <extruder name="">')
        fff.append('    <toolheadNumber>0</toolheadNumber>')
        fff.append('    <diameter>0</diameter>')
        fff.append('    <autoWidth>0</autoWidth>')
        fff.append('    <width>0</width>')
        fff.append('    <extrusionMultiplier>0</extrusionMultiplier>')
        fff.append('    <useRetract>0</useRetract>')
        fff.append('    <retractionDistance>0</retractionDistance>')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>')
        fff.append('    <retractionZLift>0</retractionZLift>')
        fff.append('    <retractionSpeed>0</retractionSpeed>')
        fff.append('    <useCoasting>0</useCoasting>')
        fff.append('    <coastingDistance>0</coastingDistance>')
        fff.append('    <useWipe>1</useWipe>')
        fff.append('    <wipeDistance>0</wipeDistance>')
        fff.append('  </extruder>')
    if hotendRight['id'] != 'None':
        fff.append('  <extruder name="Right Extruder '+str(hotendRight['nozzleSize'])+'">')
        fff.append('    <toolheadNumber>1</toolheadNumber>')
        fff.append('    <diameter>'+str(hotendRight['nozzleSize'])+'</diameter>')
        fff.append('    <autoWidth>0</autoWidth>')
        fff.append('    <width>'+str(hotendRight['nozzleSize'])+'</width>')
        fff.append('    <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+'</extrusionMultiplier>')
        fff.append('    <useRetract>1</useRetract>')
        fff.append('    <retractionDistance>'+str(filamentRight['retractionDistance'])+'</retractionDistance>')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>')
        fff.append('    <retractionZLift>0.05</retractionZLift>')
        fff.append('    <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+'</retractionSpeed>')
        fff.append('    <useCoasting>0</useCoasting>')
        fff.append('    <coastingDistance>0.2</coastingDistance>')
        fff.append('    <useWipe>1</useWipe>')
        fff.append('    <wipeDistance>5</wipeDistance>')
        fff.append('  </extruder>')
    fff.append('  <primaryExtruder>0</primaryExtruder>')
    fff.append('  <layerHeight>0.2</layerHeight>')
    fff.append('  <topSolidLayers>4</topSolidLayers>')
    fff.append('  <bottomSolidLayers>4</bottomSolidLayers>')
    fff.append('  <perimeterOutlines>3</perimeterOutlines>')
    fff.append('  <printPerimetersInsideOut>1</printPerimetersInsideOut>')
    fff.append('  <startPointOption>3</startPointOption>')
    fff.append('  <startPointOriginX>105</startPointOriginX>')
    fff.append('  <startPointOriginY>300</startPointOriginY>')
    fff.append('  <sequentialIslands>0</sequentialIslands>')
    fff.append('  <spiralVaseMode>0</spiralVaseMode>')
    fff.append('  <firstLayerHeightPercentage>125</firstLayerHeightPercentage>')
    fff.append('  <firstLayerWidthPercentage>100</firstLayerWidthPercentage>')
    fff.append('  <firstLayerUnderspeed>0.85</firstLayerUnderspeed>')
    fff.append('  <useRaft>0</useRaft>')
    fff.append('  <raftExtruder>0</raftExtruder>')
    fff.append('  <raftTopLayers>2</raftTopLayers>')
    fff.append('  <raftBaseLayers>2</raftBaseLayers>')
    fff.append('  <raftOffset>3</raftOffset>')
    fff.append('  <raftSeparationDistance>0.2</raftSeparationDistance>')
    fff.append('  <raftTopInfill>85</raftTopInfill>')    
    fff.append('  <aboveRaftSpeedMultiplier>0.3</aboveRaftSpeedMultiplier>')
    fff.append('  <useSkirt>1</useSkirt>')
    fff.append('  <skirtExtruder>999</skirtExtruder>')
    fff.append('  <skirtLayers>1</skirtLayers>')
    fff.append('  <skirtOutlines>2</skirtOutlines>')
    fff.append('  <skirtOffset>4</skirtOffset>')
    fff.append('  <usePrimePillar>0</usePrimePillar>')
    fff.append('  <primePillarExtruder>999</primePillarExtruder>')
    fff.append('  <primePillarWidth>15</primePillarWidth>')
    fff.append('  <primePillarLocation>7</primePillarLocation>')
    fff.append('  <primePillarSpeedMultiplier>1</primePillarSpeedMultiplier>')
    fff.append('  <useOozeShield>0</useOozeShield>')
    fff.append('  <oozeShieldExtruder>999</oozeShieldExtruder>')
    fff.append('  <oozeShieldOffset>2</oozeShieldOffset>')
    fff.append('  <oozeShieldOutlines>1</oozeShieldOutlines>')
    fff.append('  <oozeShieldSidewallShape>1</oozeShieldSidewallShape>')
    fff.append('  <oozeShieldSidewallAngle>30</oozeShieldSidewallAngle>')
    fff.append('  <oozeShieldSpeedMultiplier>1</oozeShieldSpeedMultiplier>')
    fff.append('  <infillExtruder>1</infillExtruder>')
    fff.append('  <internalInfillPattern>Grid</internalInfillPattern>')
    fff.append('  <externalInfillPattern>Rectilinear</externalInfillPattern>')
    fff.append('  <infillPercentage>20</infillPercentage>')
    fff.append('  <outlineOverlapPercentage>25</outlineOverlapPercentage>')
    fff.append('  <infillExtrusionWidthPercentage>100</infillExtrusionWidthPercentage>')
    fff.append('  <minInfillLength>3</minInfillLength>')
    fff.append('  <infillLayerInterval>1</infillLayerInterval>')
    fff.append('  <internalInfillAngles>45,-45</internalInfillAngles>')
    fff.append('  <overlapInternalInfillAngles>1</overlapInternalInfillAngles>')
    fff.append('  <externalInfillAngles>45,-45</externalInfillAngles>')
    fff.append('  <generateSupport>0</generateSupport>')
    fff.append('  <supportExtruder>0</supportExtruder>')
    fff.append('  <supportInfillPercentage>25</supportInfillPercentage>')
    fff.append('  <supportExtraInflation>1</supportExtraInflation>')
    fff.append('  <supportBaseLayers>0</supportBaseLayers>')
    fff.append('  <denseSupportExtruder>0</denseSupportExtruder>')
    fff.append('  <denseSupportLayers>5</denseSupportLayers>')
    fff.append('  <denseSupportInfillPercentage>75</denseSupportInfillPercentage>')
    fff.append('  <supportLayerInterval>1</supportLayerInterval>')

    fff.append('  <supportHorizontalPartOffset>0.7</supportHorizontalPartOffset>')
    fff.append('  <supportUpperSeparationLayers>1</supportUpperSeparationLayers>')
    fff.append('  <supportLowerSeparationLayers>1</supportLowerSeparationLayers>')

    fff.append('  <supportType>0</supportType>')
    fff.append('  <supportGridSpacing>1</supportGridSpacing>')
    fff.append('  <maxOverhangAngle>60</maxOverhangAngle>')
    fff.append('  <supportAngles>90</supportAngles>')
    if hotendLeft['id'] != 'None':
        fff.append('  <temperatureController name="Left Extruder '+str(hotendLeft['nozzleSize'])+'">')
        fff.append('    <temperatureNumber>0</temperatureNumber>')
        fff.append('    <isHeatedBed>0</isHeatedBed>')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>')
        fff.append('    <setpoint layer="1" temperature="150"/>')
        fff.append('  </temperatureController>')
    if hotendRight['id'] != 'None':
        fff.append('  <temperatureController name="Right Extruder '+str(hotendRight['nozzleSize'])+'">')
        fff.append('    <temperatureNumber>1</temperatureNumber>')
        fff.append('    <isHeatedBed>0</isHeatedBed>')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>')
        fff.append('    <setpoint layer="1" temperature="150"/>')
        fff.append('  </temperatureController>')
    if (hotendLeft['id'] != 'None' and filamentLeft['bedTemperature'] > 0) or (hotendRight['id'] != 'None' and filamentRight['bedTemperature'] > 0):
        fff.append('  <temperatureController name="Heated Bed">')
        fff.append('    <temperatureNumber>0</temperatureNumber>')
        fff.append('    <isHeatedBed>1</isHeatedBed>')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>')
        fff.append('    <setpoint layer="1" temperature="50"/>')
        fff.append('  </temperatureController>')
    fff.append('  <fanSpeed>')
    fff.append('    <setpoint layer="1" speed="0" />')
    fff.append('    <setpoint layer="2" speed="100"/>')
    fff.append('  </fanSpeed>')
    fff.append('  <blipFanToFullPower>0</blipFanToFullPower>')
    fff.append('  <adjustSpeedForCooling>1</adjustSpeedForCooling>')
    fff.append('  <minSpeedLayerTime>5</minSpeedLayerTime>')
    fff.append('  <minCoolingSpeedSlowdown>75</minCoolingSpeedSlowdown>')
    fff.append('  <increaseFanForCooling>1</increaseFanForCooling>')
    fff.append('  <minFanLayerTime>5</minFanLayerTime>')
    fff.append('  <maxCoolingFanSpeed>100</maxCoolingFanSpeed>')
    fff.append('  <increaseFanForBridging>1</increaseFanForBridging>')
    fff.append('  <bridgingFanSpeed>100</bridgingFanSpeed>')
    fff.append('  <use5D>1</use5D>')
    fff.append('  <relativeEdistances>0</relativeEdistances>')
    fff.append('  <allowEaxisZeroing>1</allowEaxisZeroing>')
    fff.append('  <independentExtruderAxes>0</independentExtruderAxes>')
    fff.append('  <includeM10123>0</includeM10123>')
    fff.append('  <stickySupport>1</stickySupport>')
    fff.append('  <applyToolheadOffsets>0</applyToolheadOffsets>')
    fff.append('  <gcodeXoffset>0</gcodeXoffset>')
    fff.append('  <gcodeYoffset>0</gcodeYoffset>')
    fff.append('  <gcodeZoffset>0</gcodeZoffset>')
    fff.append('  <overrideMachineDefinition>1</overrideMachineDefinition>')
    fff.append('  <machineTypeOverride>0</machineTypeOverride>')
    fff.append('  <strokeXoverride>210</strokeXoverride>')
    fff.append('  <strokeYoverride>297</strokeYoverride>')
    fff.append('  <strokeZoverride>210</strokeZoverride>')
    fff.append('  <originOffsetXoverride>0</originOffsetXoverride>')
    fff.append('  <originOffsetYoverride>0</originOffsetYoverride>')
    fff.append('  <originOffsetZoverride>0</originOffsetZoverride>')
    fff.append('  <homeXdirOverride>-1</homeXdirOverride>')
    fff.append('  <homeYdirOverride>-1</homeYdirOverride>')
    fff.append('  <homeZdirOverride>-1</homeZdirOverride>')
    fff.append('  <flipXoverride>1</flipXoverride>')
    fff.append('  <flipYoverride>-1</flipYoverride>')
    fff.append('  <flipZoverride>1</flipZoverride>')
    fff.append('  <toolheadOffsets>0,0|0,0|0,0|0,0|0,0|0,0</toolheadOffsets>')
    fff.append('  <overrideFirmwareConfiguration>1</overrideFirmwareConfiguration>')
    fff.append('  <firmwareTypeOverride>RepRap (Marlin/Repetier/Sprinter)</firmwareTypeOverride>')
    fff.append('  <GPXconfigOverride>r2</GPXconfigOverride>')
    fff.append('  <baudRateOverride>250000</baudRateOverride>')
    fff.append('  <overridePrinterModels>0</overridePrinterModels>')
    fff.append('  <printerModelsOverride></printerModelsOverride>')
    fff.append('  <startingGcode></startingGcode>')
    fff.append('  <layerChangeGcode></layerChangeGcode>')
    fff.append('  <retractionGcode></retractionGcode>')
    fff.append('  <toolChangeGcode></toolChangeGcode>')
    fff.append('  <endingGcode>\
M104 S0 T0\t\t\t;left extruder heater off,\
M104 S0 T1\t\t\t;right extruder heater off,\
M140 S0\t\t\t;heated bed heater off,\
G91\t\t\t;relative positioning,\
G1 Z+0.5 E-5 Y+10 F[travel_speed]\t;move Z up a bit and retract filament,\
G28 X0 Y0\t\t\t;move X/Y to min endstops so the head is out of the way,\
M84\t\t\t;steppers off,\
G90\t\t\t;absolute positioning,</endingGcode>')
    fff.append('  <exportFileFormat>gcode</exportFileFormat>')
    fff.append('  <celebration>0</celebration>')
    fff.append('  <celebrationSong>Random Song</celebrationSong>')
    fff.append('  <postProcessing></postProcessing>')
    fff.append('  <defaultSpeed>2400</defaultSpeed>')
    fff.append('  <outlineUnderspeed>0.85</outlineUnderspeed>')
    fff.append('  <solidInfillUnderspeed>0.85</solidInfillUnderspeed>')
    fff.append('  <supportUnderspeed>0.9</supportUnderspeed>')
    fff.append('  <rapidXYspeed>12000</rapidXYspeed>')
    fff.append('  <rapidZspeed>1002</rapidZspeed>') # If this value changes, Simplify3D bug correction post script should be adapted
    fff.append('  <minBridgingArea>10</minBridgingArea>')
    fff.append('  <bridgingExtraInflation>0</bridgingExtraInflation>')
    fff.append('  <bridgingExtrusionMultiplier>1</bridgingExtrusionMultiplier>')
    fff.append('  <bridgingSpeedMultiplier>1.5</bridgingSpeedMultiplier>')
    fff.append('  <useFixedBridgingAngle>0</useFixedBridgingAngle>')
    fff.append('  <fixedBridgingAngle>0</fixedBridgingAngle>')
    fff.append('  <applyBridgingToPerimeters>1</applyBridgingToPerimeters>')
    fff.append('  <filamentDiameters>2.85|2.85|2.85|2.85|2.85|2.85</filamentDiameters>')
    fff.append('  <filamentPricesPerKg>19.95|19.95|19.95|19.95|19.95|19.95</filamentPricesPerKg>')
    fff.append('  <filamentDensities>1.25|1.25|1.25|1.25|1.25|1.25</filamentDensities>')
    fff.append('  <useMinPrintHeight>0</useMinPrintHeight>')
    fff.append('  <minPrintHeight>0</minPrintHeight>')
    fff.append('  <useMaxPrintHeight>0</useMaxPrintHeight>')
    fff.append('  <maxPrintHeight>0</maxPrintHeight>')
    fff.append('  <useDiaphragm>0</useDiaphragm>')
    fff.append('  <diaphragmLayerInterval>5</diaphragmLayerInterval>')
    fff.append('  <robustSlicing>1</robustSlicing>')
    fff.append('  <mergeAllIntoSolid>0</mergeAllIntoSolid>')
    fff.append('  <onlyRetractWhenCrossingOutline>0</onlyRetractWhenCrossingOutline>')
    fff.append('  <retractBetweenLayers>1</retractBetweenLayers>')
    fff.append('  <useRetractionMinTravel>1</useRetractionMinTravel>')
    fff.append('  <retractionMinTravel>1.5</retractionMinTravel>')
    fff.append('  <retractWhileWiping>1</retractWhileWiping>')
    fff.append('  <onlyWipeOutlines>1</onlyWipeOutlines>')
    fff.append('  <avoidCrossingOutline>1</avoidCrossingOutline>')
    fff.append('  <maxMovementDetourFactor>3</maxMovementDetourFactor>')
    fff.append('  <toolChangeRetractionDistance>8</toolChangeRetractionDistance>')
    fff.append('  <toolChangeExtraRestartDistance>0</toolChangeExtraRestartDistance>')
    fff.append('  <toolChangeRetractionSpeed>2400</toolChangeRetractionSpeed>')
    fff.append('  <externalThinWallType>0</externalThinWallType>')
    fff.append('  <internalThinWallType>2</internalThinWallType>')
    fff.append('  <thinWallAllowedOverlapPercentage>10</thinWallAllowedOverlapPercentage>')
    fff.append('  <singleExtrusionMinLength>1</singleExtrusionMinLength>')
    fff.append('  <singleExtrusionMinPrintingWidthPercentage>50</singleExtrusionMinPrintingWidthPercentage>')
    fff.append('  <singleExtrusionMaxPrintingWidthPercentage>200</singleExtrusionMaxPrintingWidthPercentage>')
    fff.append('  <singleExtrusionEndpointExtension>0.2</singleExtrusionEndpointExtension>')
    fff.append('  <horizontalSizeCompensation>0</horizontalSizeCompensation>')
    # fff.append('  <overridePrinterModels>1</overridePrinterModels>')
    # fff.append('  <printerModelsOverride>BCN3DSigma.stl</printerModelsOverride>')
    # fff.append('  <autoConfigureMaterial name="'+str(filamentLeft)+" Left, "+str(filamentRight)+" Right"+'">')
    for extruder in extruderPrintOptions:
        for quality in sorted(PS.profilesData['quality'], key=lambda k: k['index']):
            infillPercentage = quality['infillPercentage']
            infillLayerInterval = 1
            overlapInternalInfillAngles = 1
            generateSupport = 0
            supportHorizontalPartOffset = 0.7
            supportUpperSeparationLayers = 1
            supportLowerSeparationLayers = 1
            supportAngles = '90'
            supportInfillPercentage = 25
            denseSupportInfillPercentage = 75
            avoidCrossingOutline = 1
            fanActionOnToolChange1 = ''
            fanActionOnToolChange2 = ''
            if extruder in ['Left Extruder', 'Right Extruder']:
                # MEX
                if extruder == 'Left Extruder':
                    # MEX Left
                    primaryExtruder = 0
                    primaryFilament = filamentLeft
                    primaryHotend = hotendLeft
                    layerHeight = getLayerHeight(primaryHotend, quality)
                    firstLayerHeight = primaryHotend['nozzleSize'] / 2.
                    defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'MEX Left')
                    hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, defaultSpeed)
                    purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed, layerHeight)
                    if 'Both Extruders' in extruderPrintOptions:
                        layerHeightTemp = getLayerHeight(hotendRight, quality)
                        defaultSpeedTemp, firstLayerUnderspeedTemp, outlineUnderspeedTemp, supportUnderspeedTemp = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeightTemp, firstLayerHeight, infillLayerInterval, quality, 'MEX Right')
                        hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeightTemp, defaultSpeedTemp)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeedTemp, layerHeightTemp)
                    else:
                        hotendRightTemperature = hotendLeftTemperature
                        purgeValuesT1 = purgeValuesT0
                else:
                    # MEX Right
                    primaryExtruder = 1
                    primaryFilament = filamentRight
                    primaryHotend = hotendRight
                    layerHeight = getLayerHeight(primaryHotend, quality)
                    firstLayerHeight = primaryHotend['nozzleSize'] / 2.
                    defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'MEX Right')
                    hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, defaultSpeed)
                    purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeed, layerHeight)
                    if 'Both Extruders' in extruderPrintOptions:
                        layerHeightTemp = getLayerHeight(hotendLeft, quality)
                        defaultSpeedTemp, firstLayerUnderspeedTemp, outlineUnderspeedTemp, supportUnderspeedTemp = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeightTemp, firstLayerHeight, infillLayerInterval, quality, 'MEX Left')
                        hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeightTemp, defaultSpeedTemp)
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeedTemp, layerHeightTemp)
                    else:
                        hotendLeftTemperature = hotendRightTemperature
                        purgeValuesT0 = purgeValuesT1
                infillExtruder = primaryExtruder
                supportExtruder = primaryExtruder
                bedTemperature = primaryFilament['bedTemperature']
                secondaryExtruderAction = ' - '
            else:
                # IDEX                
                if filamentLeft['isSupportMaterial'] != filamentRight['isSupportMaterial']:
                    # IDEX, Support Material
                    generateSupport = 1
                    supportHorizontalPartOffset = 0.1
                    supportUpperSeparationLayers = 0
                    supportLowerSeparationLayers = 0
                    supportAngles = '90,0'
                    supportInfillPercentage = 25
                    denseSupportInfillPercentage = 100
                    if filamentLeft['isSupportMaterial']:
                        # IDEX, Support Material in Left Hotend
                        primaryExtruder = 1
                        primaryFilament = filamentRight
                        primaryHotend = hotendRight
                        layerHeight = min(getLayerHeight(hotendRight, quality), hotendLeft['nozzleSize']*0.5)
                        firstLayerHeight = min(hotendLeft['nozzleSize'], hotendRight['nozzleSize']) / 2.
                        secondaryExtruderAction = ' (Left Ext. for supports) - '
                        defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'IDEX, Supports with Left')
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed * supportUnderspeed, layerHeight)
                        purgeValuesT1 = purgeValuesT0
                        hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, defaultSpeed*supportUnderspeed)
                        hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, defaultSpeed)
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M107'+"\t\t"+';disable fan for support material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendRightTemperature, layerHeight))+"\t\t"+';enable fan for part material,'
                    else:
                        # IDEX, Support Material in Right Hotend
                        primaryExtruder = 0
                        primaryFilament = filamentLeft
                        primaryHotend = hotendLeft
                        layerHeight = min(getLayerHeight(hotendLeft, quality), hotendRight['nozzleSize']*0.5)
                        firstLayerHeight = min(hotendLeft['nozzleSize'], hotendRight['nozzleSize']) / 2.
                        secondaryExtruderAction = ' (Right Ext. for supports) - '
                        defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'IDEX, Supports with Right')
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed, layerHeight)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeed * supportUnderspeed, layerHeight)
                        hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, defaultSpeed)
                        hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, defaultSpeed*supportUnderspeed)
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendLeftTemperature, layerHeight))+"\t\t"+';enable fan for part material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M107'+"\t\t"+';disable fan for support material,' 
                    infillExtruder = primaryExtruder
                    supportExtruder = abs(primaryExtruder-1)                    
                else:
                    # IDEX, Combined Infill
                    avoidCrossingOutline = 0
                    if hotendLeft['nozzleSize'] <= hotendRight['nozzleSize']:
                        # IDEX, Combined Infill (Right Hotend has thicker or equal nozzle)
                        primaryExtruder = 0
                        primaryFilament = filamentLeft
                        primaryHotend = hotendLeft
                        layerHeight = min(getLayerHeight(primaryHotend, quality), hotendRight['nozzleSize']*0.5)
                        firstLayerHeight = primaryHotend['nozzleSize'] / 2.
                        infillLayerInterval = int(str((hotendRight['nozzleSize']*0.5)/layerHeight).split('.')[0])
                        defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'IDEX, Infill with Right')
                        hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, max(defaultSpeed,defaultSpeed*outlineUnderspeed))
                        hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight*infillLayerInterval, defaultSpeed)
                        secondaryExtruderAction = ' (Right Ext. for infill) - '
                        if primaryFilament['fanPercentage'][1] != 0:
                            fanActionOnToolChange1 = '' # '{IF NEWTOOL=0} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendLeftTemperature, layerHeight))+"\t\t"+';enable fan for perimeters,'
                            fanActionOnToolChange2 = '' # '{IF NEWTOOL=1} M107'+"\t\t"+';disable fan for infill,'
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed, layerHeight)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeed, layerHeight * infillLayerInterval)
                    else:
                        # IDEX, Combined Infill (Left Hotend has thicker nozzle)
                        primaryExtruder = 1
                        primaryFilament = filamentRight
                        primaryHotend = hotendRight
                        layerHeight = min(getLayerHeight(primaryHotend, quality), hotendLeft['nozzleSize']*0.5)
                        firstLayerHeight = primaryHotend['nozzleSize'] / 2.
                        infillLayerInterval = int(str((hotendLeft['nozzleSize']*0.5)/layerHeight).split('.')[0])
                        defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, 'IDEX, Infill with Left')
                        hotendLeftTemperature = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight*infillLayerInterval, defaultSpeed)
                        hotendRightTemperature = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, max(defaultSpeed,defaultSpeed*outlineUnderspeed))
                        secondaryExtruderAction = ' (Left Ext. for infill) - '
                        if primaryFilament['fanPercentage'][1] != 0:
                            fanActionOnToolChange1 = '' # '{IF NEWTOOL=0} M107'+"\t\t"+';disable fan for infill,'
                            fanActionOnToolChange2 = '' # '{IF NEWTOOL=1} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendRightTemperature, layerHeight))+"\t\t"+';enable fan for perimeters,'
                        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed, layerHeight * infillLayerInterval)
                        purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeed, layerHeight)
                    infillExtruder = abs(primaryExtruder-1)
                    supportExtruder = primaryExtruder
                    firstLayerHeight = primaryHotend['nozzleSize'] / 2.
                bedTemperature = max(filamentLeft['bedTemperature'], filamentRight['bedTemperature'])
                        
            firstLayerHeightPercentage = int(firstLayerHeight * 100 / float(layerHeight))
            perimeterOutlines = max(3, int(round(quality['wallWidth'] / primaryHotend['nozzleSize']))) # 3 minimum Perimeters needed
            topSolidLayers = max(5, int(round(quality['topBottomWidth'] / layerHeight)))        # 5 minimum layers needed
            bottomSolidLayers = topSolidLayers
            raftExtruder = primaryExtruder
            skirtExtruder = primaryExtruder
            useCoasting, useWipe, onlyRetractWhenCrossingOutline, retractBetweenLayers, useRetractionMinTravel, retractWhileWiping, onlyWipeOutlines = retractValues(primaryFilament)
            startPurgeLengthT0, toolChangePurgeLengthT0, purgeSpeedT0, sParameterT0, eParameterT0, pParameterT0 = purgeValuesT0
            startPurgeLengthT1, toolChangePurgeLengthT1, purgeSpeedT1, sParameterT1, eParameterT1, pParameterT1 = purgeValuesT1
            fff.append('  <autoConfigureQuality name="'+extruder+secondaryExtruderAction+str(quality['id'])+'">')
            fff.append('    <globalExtrusionMultiplier>1</globalExtrusionMultiplier>')
            fff.append('    <fanSpeed>')
            fff.append('      <setpoint layer="1" speed="0" />')
            if primaryExtruder == 0:
                fff.append('      <setpoint layer="2" speed="'+str(fanSpeed(primaryHotend, primaryFilament, hotendLeftTemperature, layerHeight))+'" />')
            else:
                fff.append('      <setpoint layer="2" speed="'+str(fanSpeed(primaryHotend, primaryFilament, hotendRightTemperature, layerHeight))+'" />')
            fff.append('    </fanSpeed>')
            fff.append('    <filamentDiameter>'+str(primaryFilament['filamentDiameter'])+'</filamentDiameter>')
            fff.append('    <filamentPricePerKg>'+str(primaryFilament['filamentPricePerKg'])+'</filamentPricePerKg>')
            fff.append('    <filamentDensity>'+str(primaryFilament['filamentDensity'])+'</filamentDensity>')
            if hotendLeft['id'] != 'None':
                fff.append('    <extruder name="Left Extruder '+str(hotendLeft['nozzleSize'])+'">')
                fff.append('      <toolheadNumber>0</toolheadNumber>')
                fff.append('      <diameter>'+str(hotendLeft['nozzleSize'])+'</diameter>')
                fff.append('      <autoWidth>0</autoWidth>')
                fff.append('      <width>'+str(hotendLeft['nozzleSize'])+'</width>')
                fff.append('      <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+'</extrusionMultiplier>')
                fff.append('      <useRetract>1</useRetract>')
                fff.append('      <retractionDistance>'+str(filamentLeft['retractionDistance'])+'</retractionDistance>')
                fff.append('      <extraRestartDistance>0</extraRestartDistance>')
                fff.append('      <retractionZLift>'+("%.2f" % (layerHeight/2.))+'</retractionZLift>')
                fff.append('      <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+'</retractionSpeed>')
                fff.append('      <useCoasting>'+str(retractValues(filamentLeft)[0])+'</useCoasting>')
                fff.append('      <coastingDistance>'+str(coastVolume(hotendLeft, filamentLeft) / (layerHeight * hotendLeft['nozzleSize']))+'</coastingDistance>')
                fff.append('      <useWipe>'+str(retractValues(filamentLeft)[1])+'</useWipe>')
                fff.append('      <wipeDistance>'+str(hotendLeft['nozzleSize']*12.5)+'</wipeDistance>')
                fff.append('    </extruder>')
            if hotendRight['id'] != 'None':
                fff.append('    <extruder name="Right Extruder '+str(hotendRight['nozzleSize'])+'">')
                fff.append('      <toolheadNumber>1</toolheadNumber>')
                fff.append('      <diameter>'+str(hotendRight['nozzleSize'])+'</diameter>')
                fff.append('      <autoWidth>0</autoWidth>')
                fff.append('      <width>'+str(hotendRight['nozzleSize'])+'</width>')
                fff.append('      <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+'</extrusionMultiplier>')
                fff.append('      <useRetract>1</useRetract>')
                fff.append('      <retractionDistance>'+str(filamentRight['retractionDistance'])+'</retractionDistance>')
                fff.append('      <extraRestartDistance>0</extraRestartDistance>')
                fff.append('      <retractionZLift>'+str(layerHeight/2)+'</retractionZLift>')
                fff.append('      <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+'</retractionSpeed>')
                fff.append('      <useCoasting>'+str(retractValues(filamentRight)[0])+'</useCoasting>')
                fff.append('      <coastingDistance>'+str(coastVolume(hotendRight, filamentRight) / (layerHeight * hotendRight['nozzleSize']))+'</coastingDistance>')
                fff.append('      <useWipe>'+str(retractValues(filamentRight)[1])+'</useWipe>')
                fff.append('      <wipeDistance>'+str(hotendRight['nozzleSize']*12.5)+'</wipeDistance>')
                fff.append('    </extruder>')
            fff.append('    <primaryExtruder>'+str(primaryExtruder)+'</primaryExtruder>')
            fff.append('    <raftExtruder>'+str(raftExtruder)+'</raftExtruder>')
            fff.append('    <raftSeparationDistance>'+str(primaryHotend['nozzleSize'] * 0.55)+'</raftSeparationDistance>')
            fff.append('    <skirtExtruder>'+str(skirtExtruder)+'</skirtExtruder>')
            fff.append('    <infillExtruder>'+str(infillExtruder)+'</infillExtruder>')
            fff.append('    <supportExtruder>'+str(supportExtruder)+'</supportExtruder>')
            fff.append('    <generateSupport>'+str(generateSupport)+'</generateSupport>')
            fff.append('    <layerHeight>'+str(layerHeight)+'</layerHeight>')
            fff.append('    <firstLayerHeightPercentage>'+str(firstLayerHeightPercentage)+'</firstLayerHeightPercentage>')
            fff.append('    <topSolidLayers>'+str(topSolidLayers)+'</topSolidLayers>')
            fff.append('    <bottomSolidLayers>'+str(bottomSolidLayers)+'</bottomSolidLayers>')
            fff.append('    <perimeterOutlines>'+str(perimeterOutlines)+'</perimeterOutlines>')
            fff.append('    <infillPercentage>'+str(infillPercentage)+'</infillPercentage>')
            fff.append('    <infillLayerInterval>'+str(infillLayerInterval)+'</infillLayerInterval>')
            fff.append('    <defaultSpeed>'+str(defaultSpeed)+'</defaultSpeed>')
            fff.append('    <firstLayerUnderspeed>'+str(firstLayerUnderspeed)+'</firstLayerUnderspeed>')
            fff.append('    <outlineUnderspeed>'+str(outlineUnderspeed)+'</outlineUnderspeed>')
            fff.append('    <supportUnderspeed>'+str(supportUnderspeed)+'</supportUnderspeed>')
            fff.append('    <supportInfillPercentage>'+str(supportInfillPercentage)+'</supportInfillPercentage>')
            fff.append('    <denseSupportInfillPercentage>'+str(denseSupportInfillPercentage)+'</denseSupportInfillPercentage>')
            fff.append('    <avoidCrossingOutline>'+str(avoidCrossingOutline)+'</avoidCrossingOutline>')
            fff.append('    <overlapInternalInfillAngles>'+str(overlapInternalInfillAngles)+'</overlapInternalInfillAngles>')
            fff.append('    <supportHorizontalPartOffset>'+str(supportHorizontalPartOffset)+'</supportHorizontalPartOffset>')
            fff.append('    <supportUpperSeparationLayers>'+str(supportUpperSeparationLayers)+'</supportUpperSeparationLayers>')
            fff.append('    <supportLowerSeparationLayers>'+str(supportLowerSeparationLayers)+'</supportLowerSeparationLayers>')
            fff.append('    <supportAngles>'+str(supportAngles)+'</supportAngles>')
            fff.append('    <onlyRetractWhenCrossingOutline>'+str(onlyRetractWhenCrossingOutline)+'</onlyRetractWhenCrossingOutline>')
            fff.append('    <retractBetweenLayers>'+str(retractBetweenLayers)+'</retractBetweenLayers>')
            fff.append('    <useRetractionMinTravel>'+str(useRetractionMinTravel)+'</useRetractionMinTravel>')
            fff.append('    <retractWhileWiping>'+str(retractWhileWiping)+'</retractWhileWiping>')
            fff.append('    <onlyWipeOutlines>'+str(onlyWipeOutlines)+'</onlyWipeOutlines>')
            fff.append('    <minBridgingArea>10</minBridgingArea>')
            fff.append('    <bridgingExtraInflation>0</bridgingExtraInflation>')
            if generateSupport == 0:
                bridgingSpeedMultiplier = 1.5
            else:
                bridgingSpeedMultiplier = 1
            fff.append('    <bridgingExtrusionMultiplier>'+str(round(primaryFilament['extrusionMultiplier']*(1/bridgingSpeedMultiplier), 2))+'</bridgingExtrusionMultiplier>')
            fff.append('    <bridgingSpeedMultiplier>'+str(bridgingSpeedMultiplier)+'</bridgingSpeedMultiplier>')
            if hotendLeft['id'] != 'None':
                fff.append('    <temperatureController name="Left Extruder '+str(hotendLeft['nozzleSize'])+'">')
                fff.append('      <temperatureNumber>0</temperatureNumber>')
                fff.append('      <isHeatedBed>0</isHeatedBed>')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>')
                fff.append('      <setpoint layer="1" temperature="'+str(getTemperature(hotendLeft, filamentLeft, "highTemperature"))+'"/>')
                fff.append('      <setpoint layer="2" temperature="'+str(hotendLeftTemperature)+'"/>')
                fff.append('    </temperatureController>')
            if hotendRight['id'] != 'None':
                fff.append('    <temperatureController name="Right Extruder '+str(hotendRight['nozzleSize'])+'">')
                fff.append('      <temperatureNumber>1</temperatureNumber>')
                fff.append('      <isHeatedBed>0</isHeatedBed>')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>')
                fff.append('      <setpoint layer="1" temperature="'+str(getTemperature(hotendRight, filamentRight, "highTemperature"))+'"/>')
                fff.append('      <setpoint layer="2" temperature="'+str(hotendRightTemperature)+'"/>')
                fff.append('    </temperatureController>')
            if (hotendLeft['id'] != 'None' and filamentLeft['bedTemperature'] > 0) or (hotendRight['id'] != 'None' and filamentRight['bedTemperature'] > 0):
                fff.append('    <temperatureController name="Heated Bed">')
                fff.append('      <temperatureNumber>0</temperatureNumber>')
                fff.append('      <isHeatedBed>1</isHeatedBed>')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>')
                fff.append('      <setpoint layer="1" temperature="'+str(bedTemperature)+'"/>')
                fff.append('    </temperatureController>')
            if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':                    
                fff.append('    <toolChangeGcode>\
{IF NEWTOOL=0} T0\t\t\t;Start tool switch 0,\
{IF NEWTOOL=0} G1 F2400 E0,\
{IF NEWTOOL=0} M800 F'+str(purgeSpeedT0)+' S'+str(sParameterT0)+' E'+str(eParameterT0)+' P'+str(pParameterT0)+'\t;SmartPurge - Needs Firmware v01-1.2.3,\
;{IF NEWTOOL=0} G1 F'+str(purgeSpeedT0)+' E'+str(toolChangePurgeLengthT0)+'\t\t;Default purge value,\
'+fanActionOnToolChange1+',\
{IF NEWTOOL=1} T1\t\t\t;Start tool switch 1,\
{IF NEWTOOL=1} G1 F2400 E0,\
{IF NEWTOOL=1} M800 F'+str(purgeSpeedT1)+' S'+str(sParameterT1)+' E'+str(eParameterT1)+' P'+str(pParameterT1)+'\t;SmartPurge - Needs Firmware v01-1.2.3,\
;{IF NEWTOOL=1} G1 F'+str(purgeSpeedT1)+' E'+str(toolChangePurgeLengthT1)+'\t\t;Default purge,\
'+fanActionOnToolChange2+",\
G4 P2000\t\t\t\t;Stabilize Hotend's pressure,\
G92 E0\t\t\t\t;Zero extruder,\
G1 F3000 E-4.5\t\t\t\t;Retract,\
G1 F[travel_speed]\t\t\t;End tool switch,\
G91,\
G1 F[travel_speed] Z2,\
G90</toolChangeGcode>")
            else:
                fff.append('    <toolChangeGcode/>')
            if primaryFilament['isFlexibleMaterial']:
                reducedAccelerationForPerimeters = 2000
            else:
                reducedAccelerationForPerimeters = accelerationForPerimeters(primaryHotend['nozzleSize'], layerHeight, int(defaultSpeed/60. * outlineUnderspeed))
            postProcessingScript = \
r'{REPLACE "; outer perimeter" "; outer perimeter\nM204 S'+str(reducedAccelerationForPerimeters)+'"},'+\
r'{REPLACE "; inner perimeter" "; inner perimeter\nM204 S2000"},'+\
r'{REPLACE "; solid layer" "; solid layer\nM204 S2000"},'+\
r'{REPLACE "; infill" "; infill\nM204 S2000",'+\
r'{REPLACE "; support" "; support\nM204 S2000"},'+\
r'{REPLACE "; layer end" "; layer end\nM204 S2000"},'+\
r'{REPLACE "F12000\nG1 Z'+str(round(layerHeight*firstLayerHeightPercentage/100., 3))+r' F1002\nG92 E0" "F12000G1 Z'+str(round(layerHeight*firstLayerHeightPercentage/100., 3))+r' F1002\nG1 E0.0000 F720\nG92 E0"}'
            fff.append('  </autoConfigureQuality>')

            # if dataLog != '--no-data' :
            #     # Store flows, speeds, temperatures and other data
            #     data = extruder, defaultSpeed, infillLayerInterval, layerHeight, hotendLeft, hotendRight, primaryExtruder, infillExtruder, supportExtruder, filamentLeft, filamentRight, quality, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed, firstLayerHeightPercentage, hotendLeftTemperature, hotendRightTemperature, bedTemperature
            #     Logger.writeData(data)

    # fff.append('  </autoConfigureMaterial>')

    # Start gcode must be defined in autoConfigureExtruders. Otherwise you have problems with the first heat sequence in Dual Color prints.
    if hotendLeft['id'] != 'None':
        fff.append('  <autoConfigureExtruders name="Left Extruder Only"  allowedToolheads="1">')
        fff.append('    <startingGcode>\
;Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+'),\
'+firstHeatSequence(hotendLeft, hotendRight, hotendLeftTemperature, 0, bedTemperature, 'Simplify3D')+',\
G21\t\t;metric values,\
G90\t\t;absolute positioning,\
M82\t\t;set extruder to absolute mode,\
M107\t\t;start with the fan off,\
G28 X0 Y0\t\t;move X/Y to min endstops,\
G28 Z0\t\t;move Z to min endstops,\
G92 E0\t\t;zero the extruded length,\
G1 Z5 F200\t\t;safety Z axis movement,\
G1 F'+str(purgeSpeedT0)+' E'+str(startPurgeLengthT0)+'\t\t;extrude '+str(startPurgeLengthT0)+'mm of feed stock,\
G92 E0\t\t;zero the extruded length again</startingGcode>')
        postProcessingScript += ',{REPLACE "M104 S'+str(hotendRightTemperature)+' T1" ""}'
        fff.append('    <postProcessing>'+postProcessingScript+'</postProcessing>')
        fff.append('  </autoConfigureExtruders>')
    if hotendRight['id'] != 'None':
        fff.append('  <autoConfigureExtruders name="Right Extruder Only"  allowedToolheads="1">')
        fff.append('    <startingGcode>\
;Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+'),\
'+firstHeatSequence(hotendLeft, hotendRight, 0, hotendRightTemperature, bedTemperature, 'Simplify3D')+',\
G21\t\t;metric values,\
G90\t\t;absolute positioning,\
M82\t\t;set extruder to absolute mode,\
M107\t\t;start with the fan off,\
G28 X0 Y0\t\t;move X/Y to min endstops,\
G28 Z0\t\t;move Z to min endstops,\
G92 E0\t\t;zero the extruded length,\
G1 Z5 F200\t\t;safety Z axis movement,\
G1 F'+str(purgeSpeedT1)+' E'+str(startPurgeLengthT1)+'\t\t;extrude '+str(startPurgeLengthT1)+'mm of feed stock,\
G92 E0\t\t;zero the extruded length again</startingGcode>')
        postProcessingScript += ',{REPLACE "M104 S'+str(hotendLeftTemperature)+' T0" ""}'
        fff.append('    <postProcessing>'+postProcessingScript+'</postProcessing>')
        fff.append('  </autoConfigureExtruders>')
    if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':
        fff.append('  <autoConfigureExtruders name="Both Extruders"  allowedToolheads="2">')
        fff.append('    <startingGcode>\
;Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+'),'+firstHeatSequence(hotendLeft, hotendRight, hotendLeftTemperature, hotendRightTemperature, bedTemperature, 'Simplify3D')+',\
G21\t\t;metric values,\
G90\t\t;absolute positioning,\
M108 P1\t\t;enable layer fan for idle extruder,\
M107\t\t;start with the fan off,\
G28 X0 Y0\t\t;move X/Y to min endstops,\
G28 Z0\t\t;move Z to min endstops,\
T1\t\t;switch to the right extruder,\
G92 E0\t\t;zero the extruded length,\
G1 F'+str(purgeSpeedT1)+' E'+str(startPurgeLengthT1)+'\t\t;extrude '+str(startPurgeLengthT1)+'mm of feed stock,G92 E0\t\t;zero the extruded length again,\
T0\t\t;switch to the left extruder,\
G92 E0\t\t;zero the extruded length,\
G1 F'+str(purgeSpeedT0)+' E'+str(startPurgeLengthT0)+'\t\t;extrude '+str(startPurgeLengthT0)+'mm of feed stock,\
G92 E0\t\t;zero the extruded length again</startingGcode>')
        fff.append('    <layerChangeGcode></layerChangeGcode>')
        fff.append('    <postProcessing>'+postProcessingScript+'</postProcessing>')
        fff.append('  </autoConfigureExtruders>')

    fff.append('</profile>')

    fileName = fileName + '.fff'
    fileContent = '\n'.join(fff)
    return fileName, fileContent

def curaProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, quality):
    
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
            hotend, extruder, primaryExtruder, infillExtruder, supportExtruder = hotendRight, "Right Extruder", 1, 1, 1
            layerHeight = getLayerHeight(hotend, quality)
            firstLayerHeight = round(hotend['nozzleSize']/2., 2)
            supportZdistance = layerHeight
            fileName = "BCN3D Sigma - Right Extruder "+str(hotendRight['nozzleSize'])+" Only ("+filamentRight['id']+") - "+quality['id']
            extruderPrintOptions = ["Right Extruder"]
            filamentLeft = dict([('id', '')])
            defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, 1, quality, 'MEX Right')
            printTemperature1 = 0
            printTemperature2 = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, defaultSpeed)
            bedTemperature = filamentRight['bedTemperature']
            filamentDiameter1 = filamentRight['filamentDiameter']
            filamentDiameter2 = 0
            filamentFlow = filamentRight['extrusionMultiplier']*100
            retractionSpeed = filamentRight['retractionSpeed']
            retractionAmount = filamentRight['retractionDistance']
            if filamentRight['fanPercentage'][1] > 0:
                fanEnabled = 'True'
            else:
                fanEnabled = 'False'
            fanPercentage = fanSpeed(hotend, filamentRight, printTemperature2, layerHeight)            
            hotendLeftTemperature, hotendRightTemperature = 0, printTemperature2
            purgeValuesGeneral = purgeValues(hotendRight, filamentRight, defaultSpeed, layerHeight)       
            purgeValuesT0 = purgeValuesGeneral
            purgeValuesT1 = purgeValuesGeneral
    elif hotendRight['id'] == 'None':
        # MEX Left
        hotend, extruder, primaryExtruder, infillExtruder, supportExtruder = hotendLeft, "Left Extruder", 0, 0, 0
        layerHeight = getLayerHeight(hotend, quality)
        firstLayerHeight = round(hotend['nozzleSize']/2., 2)
        supportZdistance = layerHeight
        fileName = "BCN3D Sigma - Left Extruder "+str(hotendLeft['nozzleSize'])+" Only ("+filamentLeft['id']+") - "+quality['id']
        extruderPrintOptions = ["Left Extruder"]
        filamentRight = dict([('id', '')])
        defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, 1, quality, 'MEX Left')
        printTemperature1 = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, defaultSpeed)
        printTemperature2 = 0
        bedTemperature = filamentLeft['bedTemperature']
        filamentDiameter1 = filamentLeft['filamentDiameter']
        filamentDiameter2 = 0
        filamentFlow = filamentLeft['extrusionMultiplier']*100
        retractionSpeed = filamentLeft['retractionSpeed']
        retractionAmount = filamentLeft['retractionDistance']
        if filamentLeft['fanPercentage'][1] > 0:
            fanEnabled = 'True'
        else:
            fanEnabled = 'False'
        fanPercentage = fanSpeed(hotend, filamentLeft, printTemperature1, layerHeight)
        hotendLeftTemperature, hotendRightTemperature = printTemperature1, 0
        purgeValuesGeneral = purgeValues(hotendLeft, filamentLeft, defaultSpeed, layerHeight)       
        purgeValuesT0 = purgeValuesGeneral
        purgeValuesT1 = purgeValuesGeneral
    else:
        # IDEX
        hotend, extruder, primaryExtruder, infillExtruder, supportExtruder = hotendLeft, "Both Extruders", 0, 0, 0
        layerHeight = getLayerHeight(hotend, quality)
        firstLayerHeight = round(hotend['nozzleSize']/2., 2)
        supportZdistance = layerHeight
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
                supportExtruder = 1
                defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, 1, quality, 'IDEX, Supports with Right')
                printTemperature1 = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, defaultSpeed)
                printTemperature2 = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, defaultSpeed*supportUnderspeed)
        else:
            # IDEX, Dual Color / Material
            makeSupports = 'None'
            supportDualExtrusion = 'Both'
            defaultSpeedL, firstLayerUnderspeedL, outlineUnderspeedL, supportUnderspeedL = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, 1, quality, 'MEX Left')
            defaultSpeedR, firstLayerUnderspeedR, outlineUnderspeedR, supportUnderspeedR = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, 1, quality, 'MEX Right')
            defaultSpeed = min(defaultSpeedL, defaultSpeedR)
            firstLayerUnderspeed = min(firstLayerUnderspeedL, firstLayerUnderspeedR)
            outlineUnderspeed = min(outlineUnderspeedL, outlineUnderspeedR)
            supportUnderspeed = min(supportUnderspeedL, supportUnderspeedR)
            printTemperature1 = temperatureAdjustedToFlow(filamentLeft, hotendLeft, layerHeight, defaultSpeed)
            printTemperature2 = temperatureAdjustedToFlow(filamentRight, hotendRight, layerHeight, defaultSpeed)
        bedTemperature = max(filamentLeft['bedTemperature'], filamentRight['bedTemperature'])
        filamentDiameter1 = filamentLeft['filamentDiameter']
        filamentDiameter2 = filamentRight['filamentDiameter']
        filamentFlow = max(filamentLeft['extrusionMultiplier'], filamentRight['extrusionMultiplier'])*100
        retractionSpeed = max(filamentLeft['retractionSpeed'], filamentRight['retractionSpeed'])
        retractionAmount = max(filamentLeft['retractionDistance'], filamentRight['retractionDistance'])
        if filamentLeft['fanPercentage'][1] == 0 or filamentRight['fanPercentage'][1] == 0:
            fanEnabled = 'False'
        else:
            fanEnabled = 'True'
        fanPercentage = max(fanSpeed(hotendLeft, filamentLeft, printTemperature1, layerHeight), fanSpeed(hotendRight, filamentRight, printTemperature2, layerHeight))
        hotendLeftTemperature, hotendRightTemperature = printTemperature1, printTemperature2
        purgeValuesT0 = purgeValues(hotendLeft, filamentLeft, defaultSpeed, layerHeight)
        purgeValuesT1 = purgeValues(hotendRight, filamentRight, defaultSpeed, layerHeight)

    startPurgeLengthT0, toolChangePurgeLengthT0, purgeSpeedT0, sParameterT0, eParameterT0, pParameterT0 = purgeValuesT0
    startPurgeLengthT1, toolChangePurgeLengthT1, purgeSpeedT1, sParameterT1, eParameterT1, pParameterT1 = purgeValuesT1
    purgeValuesGeneral = max(startPurgeLengthT0, startPurgeLengthT1), max(toolChangePurgeLengthT0, toolChangePurgeLengthT1), min(purgeSpeedT0, purgeSpeedT1), max(sParameterT0, sParameterT1), max(eParameterT0, eParameterT1), max(pParameterT0, pParameterT1)
    startPurgeLength, toolChangePurgeLength, purgeSpeed, sParameter, eParameter, pParameter = purgeValuesGeneral
    perimeters = 0
    while perimeters*hotend['nozzleSize'] < quality['wallWidth']:
        perimeters += 1
    wallThickness = perimeters * hotend['nozzleSize']
    bottomLayerSpeed = int(firstLayerUnderspeed * defaultSpeed/60.)
    outerShellSpeed = int(outlineUnderspeed * defaultSpeed/60.)
    innerShellSpeed = int(outerShellSpeed + (defaultSpeed/60.-outerShellSpeed)/2.)

    ini = []
    ini.append('[profile]')
    ini.append('layer_height = '+str(layerHeight))
    ini.append('wall_thickness = '+str(max( 3 * hotend['nozzleSize'], wallThickness)))              # 3 minimum Perimeters needed
    ini.append('retraction_enable = True')
    ini.append('solid_layer_thickness = '+str(max( 5 * layerHeight, quality['topBottomWidth'])))    # 5 minimum layers needed
    ini.append('fill_density = '+str(quality['infillPercentage']))
    ini.append('nozzle_size = '+str(hotend['nozzleSize']))
    ini.append('print_speed = '+str(defaultSpeed/60))
    ini.append('print_temperature = '+str(printTemperature1))
    ini.append('print_temperature2 = '+str(printTemperature2))
    ini.append('print_temperature3 = 0')
    ini.append('print_temperature4 = 0')
    ini.append('print_temperature5 = 0')
    ini.append('print_bed_temperature = '+str(bedTemperature))
    ini.append('support = '+makeSupports)
    ini.append('platform_adhesion = None')
    ini.append('support_dual_extrusion = '+supportDualExtrusion)
    ini.append('wipe_tower = False')
    ini.append('wipe_tower_volume = 50')
    ini.append('ooze_shield = False')
    ini.append('filament_diameter = '+str(filamentDiameter1))
    ini.append('filament_diameter2 = '+str(filamentDiameter2))
    ini.append('filament_diameter3 = 0')
    ini.append('filament_diameter4 = 0')
    ini.append('filament_diameter5 = 0')
    ini.append('filament_flow = '+str(filamentFlow))
    ini.append('retraction_speed = '+str(retractionSpeed))
    ini.append('retraction_amount = '+str(retractionAmount))
    ini.append('retraction_dual_amount = 8')
    ini.append('retraction_min_travel = 1.5')
    if filamentLeft['id'] != '' and filamentLeft['isFlexibleMaterial'] or filamentRight['id'] != '' and filamentRight['isFlexibleMaterial']:
        ini.append('retraction_combing = All')
    else:
        ini.append('retraction_combing = No Skin')
    ini.append('retraction_minimal_extrusion = 0')
    ini.append('retraction_hop = '+("%.2f" % (layerHeight/2.)))
    ini.append('bottom_thickness = '+str(firstLayerHeight))
    ini.append('layer0_width_factor = 100')
    ini.append('object_sink = 0')
    ini.append('overlap_dual = 0.15')
    ini.append('travel_speed = 200')
    ini.append('bottom_layer_speed = '+str(bottomLayerSpeed))
    ini.append('infill_speed = '+str(defaultSpeed/60))
    ini.append('solidarea_speed = '+str(outerShellSpeed))
    ini.append('inset0_speed = '+str(outerShellSpeed))
    ini.append('insetx_speed = '+str(innerShellSpeed))
    ini.append('cool_min_layer_time = 5')
    ini.append('fan_enabled = '+str(fanEnabled))
    ini.append('skirt_line_count = 2')
    ini.append('skirt_gap = 2')
    ini.append('skirt_minimal_length = 150.0')
    ini.append('fan_full_height = 0.5')
    ini.append('fan_speed = '+str(fanPercentage))
    ini.append('fan_speed_max = 100')
    ini.append('cool_min_feedrate = 10')
    ini.append('cool_head_lift = False')
    ini.append('solid_top = True')
    ini.append('solid_bottom = True')
    ini.append('fill_overlap = 15')
    ini.append('perimeter_before_infill = True')
    ini.append('support_type = '+str(supportType))
    ini.append('support_angle = 60')
    ini.append('support_fill_rate = 40')
    ini.append('support_xy_distance = '+str(supportXYDistance))
    ini.append('support_z_distance = '+str(supportZdistance))
    ini.append('spiralize = False')
    ini.append('simple_mode = False')
    ini.append('brim_line_count = 5')
    ini.append('raft_margin = 3.0')
    ini.append('raft_line_spacing = '+str(round(hotend['nozzleSize']*7.5, 2)))
    ini.append('raft_base_thickness = '+str(round(hotend['nozzleSize']*0.75, 2)))
    ini.append('raft_base_linewidth = '+str(round(hotend['nozzleSize']*2.5, 2)))
    ini.append('raft_interface_thickness = '+str(round(hotend['nozzleSize']*0.7, 2)))
    ini.append('raft_interface_linewidth = '+str(round(hotend['nozzleSize']*1.5, 2)))
    ini.append('raft_airgap_all = 0.0')
    ini.append('raft_airgap = '+str(round(hotend['nozzleSize']*0.55, 2)))
    ini.append('raft_surface_layers = 2')
    ini.append('raft_surface_thickness = '+str(layerHeight))
    ini.append('raft_surface_linewidth = '+str(hotend['nozzleSize']))
    ini.append('fix_horrible_union_all_type_a = True')
    ini.append('fix_horrible_union_all_type_b = False')
    ini.append('fix_horrible_use_open_bits = False')
    ini.append('fix_horrible_extensive_stitching = False')
    ini.append('plugin_config = (lp1')
    if filamentLeft['id'] != '' and filamentLeft['isFlexibleMaterial'] or filamentRight['id'] != '' and filamentRight['isFlexibleMaterial']:
        ini.append('\t.')
    else:
        ini.append('\t(dp2')
        ini.append("\tS'params'")
        ini.append('\tp3')
        ini.append('\t(dp4')
        ini.append("\tsS'filename'")
        ini.append('\tp5')
        ini.append("\tS'RingingRemover.py'")
        ini.append('\tp6')
        ini.append('\tsa.')
    ini.append('object_center_x = -1')
    ini.append('object_center_y = -1')
    ini.append('')
    ini.append('[alterations]')
    ini.append('start.gcode = ;Sliced at: {day} {date} {time}')
    ini.append('\t;Profile: '+str(fileName))
    ini.append('\t;Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+')')
    ini.append('\t;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}')
    ini.append('\t;Print time: {print_time}')
    ini.append('\t;Filament used: {filament_amount}m {filament_weight}g')
    ini.append('\t;Filament cost: {filament_cost}')
    if hotendLeft['id'] != 'None':
        ini.append(firstHeatSequence(hotendLeft, hotendRight, printTemperature1, 0, bedTemperature, 'Cura'))
    else:
        ini.append(firstHeatSequence(hotendLeft, hotendRight, 0, printTemperature2, bedTemperature, 'Cura'))
    ini.append('\tG21                               ;metric values')
    ini.append('\tG90                               ;absolute positioning')
    ini.append('\tM82                               ;set extruder to absolute mode')
    ini.append('\tM107                              ;start with the fan off')
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops')
    ini.append('\tG28 Z0                            ;move Z to min endstops')
    ini.append('\tG1 Z5 F200                        ;Safety Z axis movement')
    ini.append('\tG92 E0                            ;zero the extruded length')
    ini.append('\tG1 F'+str(purgeSpeed)+' E'+str(startPurgeLength)+'                    ;extrude '+str(startPurgeLength)+'mm of feed stock')
    ini.append('\tG92 E0                            ;zero the extruded length again')
    ini.append('\tG1 F2400 E-4')
    ini.append('end.gcode = M104 T0 S0                        ;left extruder heater off')
    ini.append('\tM104 T1 S0                        ;right extruder heater off')
    ini.append('\tM140 S0                           ;heated bed heater off')
    ini.append('\tG91                               ;relative positioning')
    ini.append('\tG1 Z+0.5 E-5 Y+10 F{travel_speed} ;move Z up a bit and retract filament')
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops, so the head is out of the way')
    ini.append('\tM84                               ;steppers off')
    ini.append('\tG90                               ;absolute positioning')
    ini.append('\t;{profile_string}')
    ini.append('start2.gcode = ;Sliced at: {day} {date} {time}')
    ini.append('\t;Profile: '+str(fileName))
    ini.append('\t;Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+')')
    ini.append('\t;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}')
    ini.append('\t;Print time: {print_time}')
    ini.append('\t;Filament used: {filament_amount}m {filament_weight}g')
    ini.append('\t;Filament cost: {filament_cost}')
    if printTemperature1 == 0 or printTemperature2 == 0:
        if printTemperature1 == 0:
            ini.append(firstHeatSequence(hotendLeft, hotendRight, 0, printTemperature2, bedTemperature, 'Cura'))
        else:
            ini.append(firstHeatSequence(hotendLeft, hotendRight, printTemperature1, 0, bedTemperature, 'Cura'))
        ini.append('\tG21                               ;metric values')
        ini.append('\tG90                               ;absolute positioning')
        ini.append('\tM82                               ;set extruder to absolute mode')
        ini.append('\tM107                              ;start with the fan off')
        ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops')
        ini.append('\tG28 Z0                            ;move Z to min endstops')
        ini.append('\tG1 Z5 F200                        ;Safety Z axis movement')
        ini.append('\tG92 E0                            ;zero the extruded length')
        ini.append('\tG1 F'+str(purgeSpeed)+' E'+str(startPurgeLength)+'                    ;extrude '+str(startPurgeLength)+'mm of feed stock')
        ini.append('\tG92 E0                            ;zero the extruded length again')
        ini.append('\tG1 F2400 E-4')
    else:
        ini.append(firstHeatSequence(hotendLeft, hotendRight, printTemperature1, printTemperature2, bedTemperature, 'Cura'))
        ini.append('\tG21                               ;metric values')
        ini.append('\tG90                               ;absolute positioning')
        ini.append('\tM107                              ;start with the fan off')
        ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops')
        ini.append('\tG28 Z0                            ;move Z to min endstops')
        ini.append('\tG1 Z5 F200                        ;safety Z axis movement')
        ini.append('\tM108 P1                           ;enable layer fan for idle extruder')
        ini.append('\tT1                                ;switch to the right extruder')
        ini.append('\tG92 E0                            ;zero the extruded length')
        ini.append('\tG1 F'+str(purgeSpeedT1)+' E'+str(startPurgeLengthT1)+'                    ;extrude '+str(startPurgeLengthT1)+'mm of feed stock')
        ini.append('\tG92 E0                            ;zero the extruded length again')
        ini.append('\tG1 F2400 E-{retraction_dual_amount}')
        ini.append('\tT0                                ;switch to the left extruder')
        ini.append('\tG92 E0                            ;zero the extruded length')
        ini.append('\tG1 F'+str(purgeSpeedT0)+' E'+str(startPurgeLengthT0)+'                    ;extrude '+str(startPurgeLengthT0)+'mm of feed stock')
        ini.append('\tG92 E0                            ;zero the extruded length again')
        ini.append('\tG1 F2400 E-4')
    ini.append('end2.gcode = M104 T0 S0                        ;left extruder heater off')
    ini.append('\tM104 T1 S0                        ;right extruder heater off')
    ini.append('\tM140 S0                           ;heated bed heater off')
    ini.append('\tG91                               ;relative positioning')
    ini.append('\tG1 Z+0.5 E-5 Y+10 F{travel_speed} ;move Z up a bit and retract filament')
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops, so the head is out of the way')
    ini.append('\tM84                               ;steppers off')
    ini.append('\tG90                               ;absolute positioning')
    ini.append('\t;{profile_string}')
    ini.append('support_start.gcode = ')
    ini.append('support_end.gcode = ')
    ini.append('cool_start.gcode = ')
    ini.append('cool_end.gcode = ')
    ini.append('replace.csv = ')
    ini.append('preswitchextruder.gcode =          ;Switch between the current extruder and the next extruder, when printing with multiple extruders.')
    ini.append('\t;This code is added before the T(n)')
    ini.append('postswitchextruder.gcode =         ;Switch between the current extruder and the next extruder, when printing with multiple extruders.')
    ini.append('\t;This code is added after the T(n)')
    ini.append('\tG1 F2400 E0')
    ini.append('\tM800 F'+str(purgeSpeed)+' S'+str(sParameter)+' E'+str(eParameter)+' P'+str(pParameter)+' ;SmartPurge - Needs Firmware v01-1.2.3')
    ini.append('\t;G1 F'+str(purgeSpeed)+' E'+str(toolChangePurgeLength)+'                ;Default purge')
    ini.append("\tG4 P2000                       ;Stabilize Hotend's pressure")
    ini.append('\tG92 E0                         ;Zero extruder')
    ini.append('\tG1 F2400 E-4                   ;Retract')
    ini.append('\tG1 F{travel_speed}')
    ini.append('\tG91')
    ini.append('\tG1 F{travel_speed} Z2')
    ini.append('\tG90')

    # if dataLog != '--no-data' :
    #     firstLayerHeightPercentage = int(float(firstLayerHeight) * 100 / float(layerHeight))
    #     # Store flows, speeds, temperatures and other data
    #     data = extruder, defaultSpeed, 1, layerHeight, hotendLeft, hotendRight, primaryExtruder, infillExtruder, supportExtruder, filamentLeft, filamentRight, quality, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed, firstLayerHeightPercentage, hotendLeftTemperature, hotendRightTemperature, bedTemperature
    #     Logger.writeData(data)

    fileName = fileName + '.ini'
    fileContent = '\n'.join(ini)
    return fileName, fileContent

def cura2Profile():

    '''
        Values hierarchy:
            
            quality->material->variant->definition

            We first ask if the top (user) has the setting value. If not, we continue down. So if the quality sets a value (say fan speed) and material sets it as well, the one set by the quality is used.
    '''

    filesList = [] # List containing tuples: (fileName, fileContent)

    for hotend in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
        cura2PreferredVariant = hotend['id'].replace(' ', '_')
        if '0.4mm - Brass' in hotend['id']:
            cura2PreferredVariant = hotend['id'].replace(' ', '_')
            break

    for quality in sorted(PS.profilesData['quality'], key=lambda k: k['index']):
        cura2PreferredQuality = quality['id'].replace(' ', '_')
        if 'Standard' in quality['id']:
            cura2PreferredQuality = quality['id'].replace(' ', '_')
            break

    for filament in sorted(PS.profilesData['filament'], key=lambda k: k['id']):
        cura2PreferredMaterial = filament['id'].replace(' ', '_')
        if 'Colorfila PLA' in filament['id']:
            cura2PreferredMaterial = filament['id'].replace(' ', '_')
            break

    fileName = 'Cura 2/resources/definitions/'+PS.cura2id+'.def.json'
    definition = []
    definition.append('{')
    definition.append('    "id": "'+PS.cura2id+'",')
    definition.append('    "version": 2,')
    definition.append('    "name": "'+PS.cura2Name+'",')
    definition.append('    "inherits": "fdmprinter",')
    definition.append('    "metadata": {')
    definition.append('        "author": "'+PS.cura2Author+'",')
    definition.append('        "category": "'+PS.cura2Category+'",')
    definition.append('        "manufacturer": "'+PS.cura2Manufacturer+'",')
    definition.append('        "file_formats": "text/x-gcode",')
    definition.append('        "platform": "'+PS.cura2id+'_bed.stl",')
    # definition.append('        "platform_texture": "'+PS.cura2id+'backplate.png",')
    definition.append('        "platform_offset": [0, 0, 0],')
    definition.append('        "has_machine_quality": true,')
    definition.append('        "visible": true,')
    definition.append('        "has_materials": true,')
    definition.append('        "has_machine_materials": true,')
    definition.append('        "has_variant_materials": true,')
    definition.append('        "has_variants": true,')
    definition.append('        "preferred_material": "*'+cura2PreferredMaterial+'*",')
    definition.append('        "preferred_variant": "*'+cura2PreferredVariant+'*",')
    definition.append('        "preferred_quality": "*'+cura2PreferredQuality+'*",')
    definition.append('        "variants_name": "Hotend",')
    definition.append('        "machine_extruder_trains":')
    definition.append('        {')
    definition.append('            "0": "'+PS.cura2id+'_extruder_left",')
    definition.append('            "1": "'+PS.cura2id+'_extruder_right"')
    definition.append('        }')
    definition.append('    },')
    definition.append('    "overrides": {')
    definition.append('        "machine_name": { "default_value": "'+PS.cura2Name+'" },')
    definition.append('        "machine_width": { "default_value": 210 },')
    definition.append('        "machine_depth": { "default_value": 297 },')
    definition.append('        "machine_height": { "default_value": 210 },')
    definition.append('        "machine_heated_bed": { "default_value": true },')
    definition.append('        "machine_extruder_count": { "default_value": 2 },')
    definition.append('        "machine_center_is_zero": { "default_value": false },')
    definition.append('        "machine_gcode_flavor": { "default_value": "RepRap (Marlin/Sprinter)" },')
    definition.append('        "machine_head_with_fans_polygon":')
    definition.append('        {')
    definition.append('            "default_value":')
    definition.append('            [')
    definition.append('                [ -27.8, 39.6 ],')
    definition.append('                [ -27.8, -58.8 ],')
    definition.append('                [ 26.2, 39.6 ],')
    definition.append('                [ 26.2, -58.8 ]')
    definition.append('            ]')
    definition.append('        },')
    definition.append('        "gantry_height": { "default_value": 210 },')
    definition.append('        "extruder_prime_pos_z": { "default_value": 2.0 },') # The Z coordinate of the position where the nozzle primes at the start of printing.
    definition.append('        "extruder_prime_pos_abs": { "default_value": false },') # Make the extruder prime position absolute rather than relative to the last-known location of the head.
    definition.append('        "machine_max_feedrate_x": { "default_value": 200 },')
    definition.append('        "machine_max_feedrate_y": { "default_value": 200 },')
    definition.append('        "machine_max_feedrate_z": { "default_value": 15 },')
    definition.append('        "machine_acceleration": { "default_value": 2000 },')
    definition.append('        "material_flow_dependent_temperature":')
    definition.append('        {')
    definition.append('            "enabled": true,')
    definition.append('            "value": true')
    definition.append('        },')
    # definition.append('        "material_flow_temp_graph": { "enabled": "machine_nozzle_temp_enabled and material_flow_dependent_temperature" },') # Bad visualization
    definition.append('        "print_sequence": { "enabled": true },')
    definition.append('        "start_layers_at_same_position": { "enabled": true },')
    definition.append('        "layer_height": { "maximum_value": "0.75 * min(extruderValues('+"'machine_nozzle_size'"+'))" },')
    definition.append('        "layer_height_0":')
    definition.append('        {')
    definition.append('            "maximum_value": "0.75 * min(extruderValues('+"'machine_nozzle_size'"+'))",')
    definition.append('            "value": "min(extruderValues('+"'machine_nozzle_size'"+')) / 2"')
    definition.append('        },')
    # definition.append('        "support_enable":')
    # definition.append('        {')
    # definition.append('            "default_value": false,')
    # definition.append('            "resolve": "'+"'True' if 'True' in extruderValues('support_enable') else 'False'"+'"') # Not working
    # definition.append('        },')
    definition.append('        "machine_start_gcode": { "default_value":'+\
r'";Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+r')\n\n'+\
r'G21          ;metric values\n'+\
r'G90          ;absolute positioning\n'+\
r'M82          ;set extruder to absolute mode\n'+\
r'M108 P1      ;enable layer fan for idle extruder\n'+\
r'M107         ;start with the fan off\n'+\
r'G28 X0 Y0    ;move X/Y to min endstops\n'+\
r'G28 Z0       ;move Z to min endstops\n'+\
r'G1 Z5 F200   ;safety Z axis movement\n'+\
r'T1           ;switch to the right extruder\n'+\
r'G92 E0       ;zero the extruded length\n'+\
r'G1 E20 F50   ;extrude 20mm of feed stock\n'+\
r'G92 E0       ;zero the extruded length\n'+\
r'G4 P2000     ;stabilize hotend'+"'"+r's pressure\n'+\
r'G1 F2400 E-8 ;retract\n'+\
r'T0           ;switch to the left extruder\n'+\
r'G92 E0       ;zero the extruded length\n'+\
r'G1 E20 F50   ;extrude 20mm of feed stock\n'+\
r'G92 E0       ;zero the extruded length\n'+\
r'G4 P2000     ;stabilize hotend'+"'"+r's pressure\n'+\
r'G1 F2400 E-8 ;retract\n" },')
    definition.append(r'        "machine_end_gcode": { "default_value":'+\
r'M104 S0 T0               ;left extruder heater off\n'+\
r'M104 S0 T1               ;right extruder heater off\n'+\
r'M140 S0                  ;heated bed heater off\n'+\
r'G91                      ;relative positioning\n'+\
r'G1 Z+0.5 E-5 Y+10 F12000 ;move Z up a bit and retract filament\n'+\
r'G28 X0 Y0                ;move X/Y to min endstops so the head is out of the way\n'+\
r'M84                      ;steppers off\n'+\
r'G90                      ;absolute positioning\n" },')
    definition.append('        "machine_nozzle_temp_enabled": { "value": true },')
    definition.append('        "material_bed_temp_wait": { "value": true },')
    definition.append('        "material_print_temp_wait": { "value": true },')
    definition.append('        "material_bed_temp_prepend": { "value": false },') # Cura 2.5 ignores it
    definition.append('        "material_print_temp_prepend": { "value": false }') # Cura 2.5 ignores it
    definition.append('    }')
    definition.append('}')
    fileContent = '\n'.join(definition)
    filesList.append((fileName, fileContent))

    fileName = 'Cura 2/resources/extruders/'+PS.cura2id+'_extruder_left.def.json'
    extruder = []
    extruder.append('{')
    extruder.append('    "id": "'+PS.cura2id+'_extruder_left",')
    extruder.append('    "version": 2,')
    extruder.append('    "name": "Extruder Left",')
    extruder.append('    "inherits": "fdmextruder",')
    extruder.append('    "metadata": {')
    extruder.append('        "machine": "'+PS.cura2id+'",')
    extruder.append('        "position": "0"')
    extruder.append('    },')
    extruder.append('')
    extruder.append('    "overrides": {')
    extruder.append('        "extruder_nr": {')
    extruder.append('            "default_value": 0,')
    extruder.append('            "maximum_value": "1"')
    extruder.append('        },')
    extruder.append('        "machine_nozzle_offset_x": { "default_value": 0.0 },')
    extruder.append('        "machine_nozzle_offset_y": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_start_code": { "default_value": "G91\nG1 F12000 Z2\nG90\n" },') # Should be set as a quality parameter, but Cura 2.5 doesn't allow it
    extruder.append('        "machine_extruder_start_pos_abs": { "default_value": false },')
    extruder.append('        "machine_extruder_start_pos_x": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_start_pos_y": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_end_code": { "default_value": "" },')
    extruder.append('        "machine_extruder_end_pos_abs": { "default_value": false },')
    extruder.append('        "machine_extruder_end_pos_x": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_end_pos_y": { "default_value": 0.0 },')
    extruder.append('        "extruder_prime_pos_x": { "default_value": 0.0 },')
    extruder.append('        "extruder_prime_pos_y": { "default_value": 0.0 }')
    extruder.append('    }')
    extruder.append('}')
    fileContent = '\n'.join(extruder)
    filesList.append((fileName, fileContent))

    fileName = 'Cura 2/resources/extruders/'+PS.cura2id+'_extruder_right.def.json'
    extruder = []
    extruder.append('{')
    extruder.append('    "id": "'+PS.cura2id+'_extruder_right",')
    extruder.append('    "version": 2,')
    extruder.append('    "name": "Extruder Right",')
    extruder.append('    "inherits": "fdmextruder",')
    extruder.append('    "metadata": {')
    extruder.append('        "machine": "'+PS.cura2id+'",')
    extruder.append('        "position": "1"')
    extruder.append('    },')
    extruder.append('')
    extruder.append('    "overrides": {')
    extruder.append('        "extruder_nr": {')
    extruder.append('            "default_value": 1,')
    extruder.append('            "maximum_value": "1"')
    extruder.append('        },')
    extruder.append('        "machine_nozzle_offset_x": { "default_value": 0.0 },')
    extruder.append('        "machine_nozzle_offset_y": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_start_code": { "default_value": "G91\nG1 F12000 Z2\nG90\n" },') # Should be set as a quality parameter, but Cura 2.5 doesn't allow it
    extruder.append('        "machine_extruder_start_pos_abs": { "default_value": false },')
    extruder.append('        "machine_extruder_start_pos_x": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_start_pos_y": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_end_code": { "default_value": "" },')
    extruder.append('        "machine_extruder_end_pos_abs": { "default_value": false },')
    extruder.append('        "machine_extruder_end_pos_x": { "default_value": 0.0 },')
    extruder.append('        "machine_extruder_end_pos_y": { "default_value": 0.0 },')
    extruder.append('        "extruder_prime_pos_x": { "default_value": 0.0 },')
    extruder.append('        "extruder_prime_pos_y": { "default_value": 0.0 }')
    extruder.append('    }')
    extruder.append('}')
    fileContent = '\n'.join(extruder)
    filesList.append((fileName, fileContent))

    for filament in sorted(PS.profilesData['filament'], key=lambda k: k['id']):
        for color in filament['colors']:
            fileName = 'Cura 2/resources/materials/'+PS.cura2id+'/'+(filament['brand']+'_'+filament['material']+'_'+color+'.xml.fdm_material').replace(' ', '_')
            material = []
            material.append('<?xml version="1.0" encoding="UTF-8"?>')
            material.append('<fdmmaterial xmlns="http://www.ultimaker.com/material" version="1.3">')
            material.append('    <metadata>')
            material.append('        <name>')
            material.append('            <brand>'+filament['brand']+'</brand>')
            material.append('            <material>'+filament['material']+'</material>')
            material.append('            <color>'+color+'</color>')
            material.append('        </name>')
            material.append('        <GUID>'+str(uuid.uuid1())+'</GUID>')
            material.append('        <version>1</version>')
            material.append('        <color_code>'+filament['colors'][color]+'</color_code>')
            if filament['brand'] == 'Colorfila':
                material.append('        <instructions>http://bcn3dtechnologies.com/en/3d-printer-filaments</instructions>')
                material.append('        <author>')
                material.append('            <organization>BCN3D Technologies</organization>')
                material.append('            <contact>BCN3D Support</contact>')
                material.append('            <email>info@bcn3dtechnologies.com</email>')
                material.append('            <phone>+34 934 137 088</phone>')
                material.append('            <address>')
                material.append('                <street>Esteve Terradas 1</street>')
                material.append('                <city>Castelldefels</city>')
                material.append('                <region>Barcelona</region>')
                material.append('                <zip>08860</zip>')
                material.append('                <country>Spain</country>')
                material.append('            </address>')
                material.append('        </author>')
                material.append('        <supplier>')
                material.append('            <organization>BCN3D Technologies</organization>')
                material.append('            <contact>BCN3D Support</contact>')
                material.append('            <email>info@bcn3dtechnologies.com</email>')
                material.append('            <phone>+34 934 137 088</phone>')
                material.append('            <address>')
                material.append('                <street>Esteve Terradas 1</street>')
                material.append('                <city>Castelldefels</city>')
                material.append('                <region>Barcelona</region>')
                material.append('                <zip>08860</zip>')
                material.append('                <country>Spain</country>')
                material.append('            </address>')
                material.append('        </supplier>')
                # material.append('        <EAN>11 22222 33333 4</EAN>')
                # material.append('        <MSDS>http://...</MSDS>')
                # material.append('        <TDS>http://...</TDS>')
            material.append('    </metadata>')
            material.append('    <properties>')
            material.append('        <density>'+str(filament['filamentDensity'])+'</density>')
            material.append('        <diameter>'+str(filament['filamentDiameter'])+'</diameter>')
            material.append('    </properties>')
            material.append('    <settings>')
            material.append('        <setting key="print temperature">'+str(defaultMaterialPrintTemperature(filament))+'</setting>') # default_material_print_temperature
            material.append('        <setting key="heated bed temperature">'+str(filament['bedTemperature'])+'</setting>') # material_bed_temperature
            material.append('')
            material.append('        <machine>')
            material.append('           <machine_identifier manufacturer="'+PS.cura2Manufacturer+'" product="'+PS.cura2id+'" />')
            for hotend in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
                if hotend['id'] != 'None':
                    material.append('           <hotend id="'+hotend['id']+'">')
                    if filament['isAbrasiveMaterial'] and hotend['material'] == "Brass":
                        material.append('                <setting key="hardware compatible">no</setting>')
                    else:
                        material.append('                <setting key="hardware compatible">yes</setting>')
                    material.append('            </hotend>')
            material.append('       </machine>')
            material.append('')
            material.append('    </settings>')
            material.append('</fdmmaterial>')
            fileContent = '\n'.join(material)
            filesList.append((fileName, fileContent))

    globalQualities = []
    for hotend in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
        if hotend['id'] != 'None':
            for filament in sorted(PS.profilesData['filament'], key=lambda k: k['id']):
                for color in filament['colors']:
                    for quality in sorted(PS.profilesData['quality'], key=lambda k: k['index']):
                        layerHeight = getLayerHeight(hotend, quality)
                        firstLayerHeight = hotend['nozzleSize']/2.
                        defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotend, hotend, filament, filament, layerHeight, firstLayerHeight, 1, quality, 'MEX Left')
                        hotendLeftTemperature = temperatureAdjustedToFlow(filament, hotend, layerHeight, defaultSpeed)
                        startPurgeLength, toolChangePurgeLength, purgeSpeed, sParameter, eParameter, pParameter = purgeValues(hotend, filament, defaultSpeed, layerHeight)
                        # Create a new global quality for the new layer height
                        if layerHeight not in globalQualities:
                            globalQualities.append(layerHeight)
                            fileName = 'Cura 2/resources/quality/'+PS.cura2id+'/'+PS.cura2id+'_global_Layer_'+("%.2f" % layerHeight)+'_mm_Quality.inst.cfg'
                            qualityFile = []
                            qualityFile.append('[general]')
                            qualityFile.append('version = 2')
                            qualityFile.append('name = Global Layer '+("%.2f" % layerHeight)+' mm')
                            qualityFile.append('definition = '+PS.cura2id)
                            qualityFile.append('')
                            qualityFile.append('[metadata]')
                            qualityFile.append('type = quality')
                            qualityFile.append('quality_type = layer'+("%.2f" % layerHeight)+'mm')
                            qualityFile.append('global_quality = True')
                            qualityFile.append('weight = '+str(len(globalQualities)))
                            qualityFile.append('setting_version = 2')
                            qualityFile.append('')
                            qualityFile.append('[values]')
                            qualityFile.append('layer_height = '+("%.2f" % layerHeight))
                            fileContent = '\n'.join(qualityFile)
                            filesList.append((fileName, fileContent))

                        fileName = 'Cura 2/resources/quality/'+PS.cura2id+'/'+'_'.join([PS.cura2id, hotend['id'], filament['brand'], filament['material'], color, quality['id'], 'Quality.inst.cfg']).replace(' ', '_')

                        # keep all default values commented

                        qualityFile = []
                        qualityFile.append('[general]')
                        qualityFile.append('version = 2')
                        qualityFile.append('name = '+quality['id']+' Quality')
                        qualityFile.append('definition = '+PS.cura2id)
                        qualityFile.append('')
                        qualityFile.append('[metadata]')
                        qualityFile.append('type = quality')
                        qualityFile.append('quality_type = layer'+("%.2f" % layerHeight)+'mm')
                        qualityFile.append('material = '+'_'.join([filament['brand'], filament['material'], color, PS.cura2id, hotend['id']]).replace(' ', '_'))
                        for index in range(len(globalQualities)):
                            if globalQualities[index] == layerHeight:
                                qualityFile.append('weight = '+str(index+1))
                                break
                        qualityFile.append('setting_version = 2')
                        qualityFile.append('')
                        qualityFile.append('[values]')

                        
                        # qualityFile.append(r'machine_extruder_start_code = ="\nM800 F'+str(purgeSpeed)+' S'+str(sParameter)+' E'+str(eParameter)+' P'+str(pParameter)+r'\t;SmartPurge - Needs Firmware v01-1.2.3\nG4 P2000\t\t\t\t;Stabilize Hotend'+"'"+r's pressure\nG92 E0\t\t\t\t;Zero extruder\nG1 F3000 E-4.5\t\t\t\t;Retract\nG1 F12000\t\t\t;End tool switch\nG91\nG1 F12000 Z2\nG90\n"') # Keyword NOT WORKING on Cura 2.5

                        # resolution
                        qualityFile.append('layer_height = '+("%.2f" % layerHeight))
                        qualityFile.append('line_width = =round(machine_nozzle_size * 0.875, 3)')
                        # qualityFile.append('wall_line_width = =line_width')
                        # qualityFile.append('wall_line_width_0 = =wall_line_width')
                        qualityFile.append('wall_line_width_x = =machine_nozzle_size * 0.85')
                        # qualityFile.append('roofing_line_width = =skin_line_width')
                        # qualityFile.append('skin_line_width = =line_width')
                        qualityFile.append('infill_line_width = =machine_nozzle_size * 1.25')
                        # qualityFile.append('skirt_brim_line_width = =line_width')
                        qualityFile.append('support_line_width = =infill_line_width')
                        # qualityFile.append('support_interface_line_width = =line_width')
                        # qualityFile.append('support_roof_line_width = =extruderValue(support_roof_extruder_nr, '+"'support_interface_line_width'"+')
                        # qualityFile.append('support_bottom_line_width = =extruderValue(support_bottom_extruder_nr, '+"'support_interface_line_width'"+'')
                        # qualityFile.append('prime_tower_line_width = =line_width')
                        # qualityFile.append('initial_layer_line_width_factor = 100')

                        #shell
                        # qualityFile.append('wall_extruder_nr = =-1')
                        # qualityFile.append('wall_0_extruder_nr = =wall_extruder_nr')
                        # qualityFile.append('wall_x_extruder_nr = =wall_extruder_nr')
                        qualityFile.append('wall_thickness = =max( 3 * machine_nozzle_size, '+("%.2f" % quality['wallWidth'])+')')     # 3 minimum Perimeters needed
                        qualityFile.append('wall_0_wipe_dist = =12.5 * machine_nozzle_size')
                        # qualityFile.append('roofing_extruder_nr = =-1')
                        # qualityFile.append('roofing_layer_count = =0')
                        # qualityFile.append('roofing_pattern = =skin_angles')
                        # qualityFile.append('roofing_angles = =top_bottom_pattern')
                        # qualityFile.append('top_bottom_extruder_nr = =-1')
                        qualityFile.append('top_bottom_thickness = =max( 5 * layer_height, '+("%.2f" % quality['topBottomWidth'])+')') # 5 minimum layers needed
                        # qualityFile.append('top_thickness = =top_bottom_thickness')
                        # qualityFile.append('bottom_thickness = =top_bottom_thickness')
                        # qualityFile.append('top_bottom_pattern = =lines')
                        # qualityFile.append('top_bottom_pattern_0 = =top_bottom_pattern')
                        # qualityFile.append('skin_angles = =[ ]') # ?? check syntax
                        # qualityFile.append('wall_0_inset = 0')
                        # qualityFile.append('outer_inset_first = False')
                        # qualityFile.append('alternate_extra_perimeter = False')
                        if filament['isFlexibleMaterial']:
                            qualityFile.append('travel_compensate_overlapping_walls_enabled = False')
                        else: 
                            qualityFile.append('travel_compensate_overlapping_walls_enabled = True') 
                        # qualityFile.append('fill_perimeter_gaps = everywhere')
                        # qualityFile.append('fill_outline_gaps = everywhere')
                        # qualityFile.append('xy_offset = 0')
                        qualityFile.append('xy_offset_layer_0 = -0.1')
                        qualityFile.append('z_seam_type = back') 
                        qualityFile.append('z_seam_x = 105') 
                        qualityFile.append('z_seam_y = 297')
                        qualityFile.append('z_seam_relative = True')
                        # qualityFile.append('skin_no_small_gaps_heuristic = True') 

                        # infill
                        # qualityFile.append('infill_extruder_nr = =-1')
                        qualityFile.append('infill_sparse_density = ='+str(int(min(100, quality['infillPercentage'] * 1.25)))+" if infill_pattern == 'cubicsubdiv' else "+str(int(quality['infillPercentage']))) # 'if' is not working... # 'if' is not working...
                        qualityFile.append('infill_pattern = grid')
                        # qualityFile.append('infill_angles = []')
                        # qualityFile.append('sub_div_rad_mult = 100')
                        # qualityFile.append('sub_div_rad_add = =wall_line_width_x')
                        # qualityFile.append('infill_overlap = =10 if infill_sparse_density < 95 and infill_pattern != '+"'"+'concentric'+"'"+' else 0')
                        qualityFile.append("skin_overlap = =10 if top_bottom_pattern != 'concentric' else 0")
                        # qualityFile.append('infill_wipe_dist = =wall_line_width_0 / 4 if wall_line_count == 1 else wall_line_width_x / 4')
                        qualityFile.append('infill_sparse_thickness = =layer_height')
                        # qualityFile.append('gradual_infill_steps = 0')
                        # qualityFile.append('gradual_infill_step_height = 5')
                        qualityFile.append('infill_before_walls = False')
                        # qualityFile.append('min_infill_area = 0')
                        # qualityFile.append('max_skin_angle_for_expansion = 20')

                        # material -> default_material_print_temperature, material_bed_temperature,  must be set into material to avoid conflicts
                        qualityFile.append('material_print_temperature = =default_material_print_temperature + '+str(temperatureAdjustedToFlow(filament, hotend, layerHeight, defaultSpeed) - defaultMaterialPrintTemperature(filament)))
                        qualityFile.append('material_print_temperature_layer_0 = =default_material_print_temperature + '+str(int(round((getTemperature(hotend, filament, 'highTemperature')))) - defaultMaterialPrintTemperature(filament)))
                        temperatureInertiaInitialFix = 0
                        qualityFile.append('material_initial_print_temperature = =material_print_temperature + '+str(temperatureInertiaInitialFix))
                        temperatureInertiaFinalFix = -2.5
                        qualityFile.append('material_final_print_temperature = =material_print_temperature + '+str(temperatureInertiaFinalFix))
                        minFlow = 0.3 * 0.05 * 10
                        minTemp = getTemperature(hotend, filament, 'lowTemperature')
                        maxFlow = maxFlowValue(hotend, filament, layerHeight)
                        maxTemp = getTemperature(hotend, filament, 'highTemperature')
                        stdFlow = 0.4 * 0.15 * 60
                        stdTemp = (minTemp + maxTemp) /2.
                        qualityFile.append('material_flow_temp_graph = [['+str(minFlow)+','+str(minTemp)+'], ['+str(stdFlow)+','+str(stdTemp)+'], ['+str(maxFlow)+','+str(maxTemp)+']]')
                        qualityFile.append('material_extrusion_cool_down_speed = 1') # this value depends on extruded flow (not material_flow)
                        qualityFile.append('material_diameter = '+("%.2f" % filament['filamentDiameter']))
                        qualityFile.append('material_flow = '+("%.2f" % (filament['extrusionMultiplier'] * 100)))
                        # qualityFile.append('retraction_enable = True')
                        # qualityFile.append('retract_at_layer_change = False')
                        qualityFile.append('retraction_amount = '+("%.2f" % filament['retractionDistance']))
                        qualityFile.append('retraction_speed = '+("%.2f" % filament['retractionSpeed']))
                        # qualityFile.append('retraction_retract_speed = =retraction_speed')
                        # qualityFile.append('retraction_prime_speed = =retraction_speed')
                        # qualityFile.append('retraction_extra_prime_amount = 0') # Adjust for flex materials
                        qualityFile.append('retraction_min_travel = 1.5')
                        qualityFile.append('retraction_count_max = '+str(int(filament['retractionCount'])))
                        # qualityFile.append('retraction_extrusion_window = =retraction_amount')
                        standbyTemperature = int(getTemperature(hotend, filament, 'standbyTemperature'))
                        qualityFile.append('material_standby_temperature = '+str(standbyTemperature))
                        # qualityFile.append('switch_extruder_retraction_amount = =machine_heat_zone_length')
                        qualityFile.append('switch_extruder_retraction_speed = =retraction_speed')
                        # qualityFile.append('switch_extruder_extra_prime_amount = '+("%.2f" % filament['retractionSpeed'])) # Parameter that should be there to purge on toolchage
                        qualityFile.append('switch_extruder_prime_speed = =retraction_speed')

                        # speed
                        qualityFile.append('speed_print = '+("%.2f" % (defaultSpeed/60.)))
                        # qualityFile.append('speed_infill = =speed_print')
                        qualityFile.append('speed_wall = =round(speed_print - (speed_print - speed_print * '+("%.2f" % outlineUnderspeed)+') / 2, 1)')
                        qualityFile.append('speed_wall_0 = =round(speed_print * '+("%.2f" % outlineUnderspeed)+', 1)')
                        qualityFile.append('speed_wall_x = =speed_wall')
                        # qualityFile.append('speed_roofing = =speed_topbottom')
                        qualityFile.append('speed_topbottom = =speed_wall_0')
                        # qualityFile.append('speed_ironing = =speed_roofing * 20 / 30')
                        qualityFile.append('speed_support = =round(speed_print * '+("%.2f" % supportUnderspeed)+', 1)')
                        # qualityFile.append('speed_support_infill = =speed_support')
                        qualityFile.append('speed_support_interface = =speed_wall')
                        qualityFile.append('speed_travel = =round(speed_print if magic_spiralize else 200)')
                        qualityFile.append('speed_layer_0 = =round(speed_print * '+("%.2f" % firstLayerUnderspeed)+', 1)')
                        # qualityFile.append('speed_print_layer_0 = =speed_layer_0')
                        qualityFile.append('speed_travel_layer_0 = =round(speed_travel / 3, 1)')
                        # qualityFile.append('skirt_brim_speed = =speed_layer_0')
                        # qualityFile.append('speed_slowdown_layers = 2')
                        qualityFile.append('speed_equalize_flow_enabled = True')
                        qualityFile.append('speed_equalize_flow_max = 100')
                        qualityFile.append('acceleration_enabled = True')
                        qualityFile.append('acceleration_print = 2000')
                        # qualityFile.append('acceleration_infill = =acceleration_print')
                        qualityFile.append('acceleration_wall = =round(acceleration_print - (acceleration_print - acceleration_wall_0)/ 2)')
                        qualityFile.append('acceleration_wall_0 = '+str(int(accelerationForPerimeters(hotend['nozzleSize'], layerHeight, int(defaultSpeed/60. * outlineUnderspeed)))))
                        # qualityFile.append('acceleration_wall_x = =acceleration_wall')
                        # qualityFile.append('acceleration_roofing = =acceleration_topbottom')
                        qualityFile.append('acceleration_topbottom = =acceleration_wall_0')
                        # qualityFile.append('acceleration_ironing = =acceleration_roofing')
                        qualityFile.append('acceleration_support = =acceleration_wall')
                        # qualityFile.append('acceleration_support_infill = =acceleration_support')
                        qualityFile.append('acceleration_support_interface = =acceleration_topbottom')
                        qualityFile.append('acceleration_travel = =acceleration_print if magic_spiralize else 2250')
                        qualityFile.append('acceleration_layer_0 = =acceleration_topbottom')
                        # qualityFile.append('acceleration_print_layer_0 = =acceleration_layer_0')
                        # qualityFile.append('acceleration_travel_layer_0 = =acceleration_layer_0 * acceleration_travel / acceleration_print')
                        # qualityFile.append('acceleration_skirt_brim = =acceleration_layer_0')
                        qualityFile.append('jerk_enabled = True')
                        qualityFile.append('jerk_print = =15') # Adjust all jerk
                        # qualityFile.append('jerk_infill = =jerk_print')
                        qualityFile.append('jerk_wall = =jerk_print * 0.75')
                        qualityFile.append('jerk_wall_0 = =jerk_wall * 0.5')
                        # qualityFile.append('jerk_wall_x = =jerk_wall')
                        # qualityFile.append('jerk_roofing = =jerk_topbottom')
                        qualityFile.append('jerk_topbottom = =jerk_print * 0.5')
                        # qualityFile.append('jerk_ironing = =jerk_roofing')
                        qualityFile.append('jerk_support = =jerk_print * 0.75')
                        # qualityFile.append('jerk_support_infill = =jerk_support')
                        qualityFile.append('jerk_support_interface = =jerk_topbottom')
                        qualityFile.append('jerk_prime_tower = =jerk_print * 0.75')
                        qualityFile.append('jerk_travel = =jerk_print if magic_spiralize else 15')
                        qualityFile.append('jerk_layer_0 = =jerk_topbottom')
                        # qualityFile.append('jerk_print_layer_0 = =jerk_layer_0')
                        # qualityFile.append('jerk_travel_layer_0 = =jerk_layer_0 * jerk_travel / jerk_print')
                        # qualityFile.append('jerk_skirt_brim = =jerk_layer_0')

                        # travel
                        if filament['isFlexibleMaterial']:
                            qualityFile.append('retraction_combing = all')
                        else:
                            qualityFile.append('retraction_combing = noskin')
                        # qualityFile.append('travel_retract_before_outer_wall = False')
                        qualityFile.append('travel_avoid_other_parts = False')
                        # qualityFile.append('travel_avoid_distance = =machine_nozzle_tip_outer_diameter / 2 * 1.25')
                        qualityFile.append('start_layers_at_same_position = True') # different than z_seam
                        layerStartX, layerStartY = 105, 297
                        qualityFile.append('layer_start_x = '+str(layerStartX)) # different than z_seam
                        qualityFile.append('layer_start_y = '+str(layerStartY)) # different than z_seam
                        qualityFile.append('retraction_hop_enabled = True')
                        qualityFile.append('retraction_hop_only_when_collides = True')
                        qualityFile.append('retraction_hop = =0.5 * layer_height')
                        # qualityFile.append('retraction_hop_after_extruder_switch = True')

                        # cooling
                        if filament['fanPercentage'][1] > 0:
                            qualityFile.append('cool_fan_enabled = True')
                        else:
                            qualityFile.append('cool_fan_enabled = False')
                        qualityFile.append('cool_fan_speed = '+str(int(filament['fanPercentage'][1])))
                        qualityFile.append('cool_fan_speed_min = '+str(int(filament['fanPercentage'][0])))
                        # qualityFile.append('cool_fan_speed_max = =cool_fan_speed')
                        # qualityFile.append('cool_min_layer_time_fan_speed_max = 10')
                        # qualityFile.append('cool_fan_speed_0 = 0')
                        qualityFile.append("cool_fan_full_at_height = =0 if adhesion_type == 'raft' else layer_height_0 + 4 * layer_height") # after 6 layers
                        # qualityFile.append('cool_min_layer_time = 5')
                        # qualityFile.append('cool_min_speed = 10')
                        # qualityFile.append('cool_lift_head = False')

                        # support
                        if filament['isSupportMaterial']:
                            # qualityFile.append('support_enable = True') # Not working
                            qualityFile.append('support_infill_rate = 25')
                            qualityFile.append('support_xy_distance = 0.5')
                            qualityFile.append('support_z_distance = 0')
                            qualityFile.append('support_interface_density = 100')
                            qualityFile.append('support_conical_enabled = False')
                            # qualityFile.append('support_conical_angle = 30')
                        else:
                            # qualityFile.append('support_enable = False')
                            qualityFile.append('support_infill_rate = 15')
                            qualityFile.append('support_xy_distance = 0.7')
                            qualityFile.append('support_z_distance = =layer_height')
                            qualityFile.append('support_interface_density = 75')
                            qualityFile.append('support_conical_enabled = True')
                            # qualityFile.append('support_conical_angle = 30')
                        # qualityFile.append('support_type = everywhere')
                        # qualityFile.append('support_pattern = zigzag')
                        # qualityFile.append('support_connect_zigzags = True')
                        # qualityFile.append('support_skip_some_zags = False')
                        # qualityFile.append('support_zag_skip_count = =6')
                        # qualityFile.append('support_top_distance = =extruderValue(support_extruder_nr, 'support_z_distance')')
                        # qualityFile.append('support_bottom_distance = =extruderValue(support_extruder_nr, 'support_z_distance') if support_type == 'everywhere' else 0')
                        # qualityFile.append('support_xy_overrides_z = z_overrides_xy')
                        # qualityFile.append('support_xy_distance_overhang = =machine_nozzle_size / 2')
                        # qualityFile.append('support_bottom_stair_step_height = 0.3')
                        qualityFile.append('support_join_distance = 10')
                        qualityFile.append('support_offset = 1')
                        # qualityFile.append('support_infill_sparse_thickness = =resolveOrValue('+"'layer_height'"+')')
                        # qualityFile.append('gradual_support_infill_steps = 0')
                        # qualityFile.append('gradual_support_infill_step_height = 1')
                        qualityFile.append('support_interface_enable = True')
                        qualityFile.append('support_interface_height = =5 * layer_height')
                        # qualityFile.append("support_roof_height =extruderValue(support_interface_extruder_nr, 'support_interface_height')")
                        # qualityFile.append("support_bottom_height = =extruderValue(support_interface_extruder_nr, 'support_interface_height')")
                        qualityFile.append('support_interface_skip_height = =layer_height')
                        qualityFile.append('support_interface_pattern = lines')
                        # qualityFile.append('support_use_towers = True')
                        # qualityFile.append('support_tower_diameter = 3.0')
                        qualityFile.append('support_minimal_diameter = 1.0')
                        # qualityFile.append('support_tower_roof_angle = 65')

                        # platform_adhesion
                        # qualityFile.append('extruder_prime_pos_x = 0')
                        # qualityFile.append('extruder_prime_pos_y = 0')
                        qualityFile.append('adhesion_type = skirt')
                        qualityFile.append('skirt_line_count = 2')
                        # qualityFile.append('skirt_gap = 3')
                        qualityFile.append("skirt_brim_minimal_length = =round((material_diameter/2)**2 / (extruderValue(adhesion_extruder_nr, 'machine_nozzle_size')/2)**2 *"+str(startPurgeLength)+', 2)')
                        # qualityFile.append('brim_width = 8')
                        # qualityFile.append('brim_outside_only = True')
                        qualityFile.append('raft_margin = 3')
                        qualityFile.append("raft_airgap = =min(extruderValues('machine_nozzle_size')) * 0.55")
                        # qualityFile.append('layer_0_z_overlap = =raft_airgap / 2')
                        # qualityFile.append('raft_surface_layers = 2')
                        # qualityFile.append('raft_surface_thickness = =layer_height')
                        # qualityFile.append('raft_surface_line_width = =line_width')
                        # qualityFile.append('raft_surface_line_spacing = =raft_surface_line_width')
                        qualityFile.append("raft_interface_thickness = =extruderValue(adhesion_extruder_nr, 'machine_nozzle_size') * 0.7")
                        qualityFile.append('raft_interface_line_width = =line_width * 1.5')
                        # qualityFile.append('raft_interface_line_spacing = =raft_interface_line_width + 0.2')
                        qualityFile.append("raft_base_thickness = =extruderValue(adhesion_extruder_nr, 'machine_nozzle_size') * 0.75")
                        qualityFile.append("raft_base_line_width = =extruderValue(adhesion_extruder_nr, 'machine_nozzle_size') * 2.5")
                        qualityFile.append("raft_base_line_spacing = =extruderValue(adhesion_extruder_nr, 'machine_nozzle_size') * 7.5")
                        # qualityFile.append('raft_speed = =speed_print / 60 * 30')
                        # qualityFile.append('raft_surface_speed = =raft_speed')
                        # qualityFile.append('raft_interface_speed = =raft_speed * 0.75')
                        # qualityFile.append('raft_base_speed = =raft_speed * 0.75')
                        # qualityFile.append('raft_acceleration = =acceleration_print')
                        # qualityFile.append('raft_surface_acceleration = =raft_acceleration')
                        # qualityFile.append('raft_interface_acceleration = =raft_acceleration')
                        # qualityFile.append('raft_base_acceleration = =raft_acceleration')
                        # qualityFile.append('raft_jerk = =jerk_print')
                        # qualityFile.append('raft_surface_jerk = =raft_jerk')
                        # qualityFile.append('raft_interface_jerk = =raft_jerk')
                        # qualityFile.append('raft_base_jerk = =raft_jerk')
                        # qualityFile.append('raft_fan_speed = 0')
                        # qualityFile.append('raft_surface_fan_speed = =raft_fan_speed')
                        # qualityFile.append('raft_interface_fan_speed = =raft_fan_speed')
                        # qualityFile.append('raft_base_fan_speed = =raft_fan_speed')

                        # dual
                        qualityFile.append('prime_tower_enable = False')
                        qualityFile.append('prime_tower_size = =max(15, round(math.sqrt(prime_tower_min_volume/layer_height), 2))')
                        qualityFile.append("prime_tower_min_volume = =round((material_diameter/2)**2 / (extruderValue(adhesion_extruder_nr, 'machine_nozzle_size')/2)**2 *"+str(toolChangePurgeLength)+', 2)')
                        # qualityFile.append("prime_tower_wall_thickness = =round(max(2 * prime_tower_line_width, 0.5 * (prime_tower_size - math.sqrt(max(0, prime_tower_size ** 2 - prime_tower_min_volume / layer_height)))), 3)")
                        # qualityFile.append('prime_tower_position_x = =machine_width - max(extruderValue(adhesion_extruder_nr, 'brim_width') * extruderValue(adhesion_extruder_nr, 'initial_layer_line_width_factor') / 100 if adhesion_type == 'brim' else (extruderValue(adhesion_extruder_nr, 'raft_margin') if adhesion_type == 'raft' else (extruderValue(adhesion_extruder_nr, 'skirt_gap') if adhesion_type == 'skirt' else 0)), max(extruderValues('travel_avoid_distance'))) - max(extruderValues('support_offset')) - sum(extruderValues('skirt_brim_line_width')) * extruderValue(adhesion_extruder_nr, 'initial_layer_line_width_factor') / 100 - 1')
                        # qualityFile.append('prime_tower_position_y = =machine_depth - prime_tower_size - max(extruderValue(adhesion_extruder_nr, 'brim_width') * extruderValue(adhesion_extruder_nr, 'initial_layer_line_width_factor') / 100 if adhesion_type == 'brim' else (extruderValue(adhesion_extruder_nr, 'raft_margin') if adhesion_type == 'raft' else (extruderValue(adhesion_extruder_nr, 'skirt_gap') if adhesion_type == 'skirt' else 0)), max(extruderValues('travel_avoid_distance'))) - max(extruderValues('support_offset')) - sum(extruderValues('skirt_brim_line_width')) * extruderValue(adhesion_extruder_nr, 'initial_layer_line_width_factor') / 100 - 1')
                        # qualityFile.append('prime_tower_flow = 100')
                        qualityFile.append('prime_tower_wipe_enabled = False')
                        qualityFile.append('dual_pre_wipe = False')
                        # qualityFile.append('prime_tower_purge_volume = 0')
                        qualityFile.append('ooze_shield_enabled = False')
                        # qualityFile.append('ooze_shield_angle = 60')
                        # qualityFile.append('ooze_shield_dist = 2')

                        # meshfix
                        # qualityFile.append('meshfix_union_all = True')
                        # qualityFile.append('meshfix_union_all_remove_holes = False')
                        # qualityFile.append('meshfix_extensive_stitching = False')
                        # qualityFile.append('meshfix_keep_open_polygons = False')
                        qualityFile.append("multiple_mesh_overlap = =0.375 * machine_nozzle_size - xy_offset")
                        # qualityFile.append('carve_multiple_volumes = True')
                        # qualityFile.append('alternate_carve_order = True')

                        # blackmagic
                        # qualityFile.append('print_sequence = all_at_once')
                        # qualityFile.append('infill_mesh = False')
                        # qualityFile.append('infill_mesh_order = 0')
                        # qualityFile.append('support_mesh = False')
                        # qualityFile.append('anti_overhang_mesh = False')
                        # qualityFile.append('magic_mesh_surface_mode = normal')
                        # qualityFile.append('magic_spiralize = False')

                        # experimental
                        # qualityFile.append('draft_shield_enabled = False')
                        # qualityFile.append('draft_shield_dist = 10')
                        # qualityFile.append('draft_shield_height_limitation = False')
                        # qualityFile.append('draft_shield_height = 10')
                        # qualityFile.append('conical_overhang_enabled = False')
                        # qualityFile.append('conical_overhang_angle = 50')
                        qualityFile.append('coasting_enable = False')
                        qualityFile.append('coasting_volume = '+str(coastVolume(hotend, filament)))
                        qualityFile.append('coasting_min_volume = =coasting_volume * 2')
                        # qualityFile.append('coasting_speed = 90')
                        # qualityFile.append('skin_outline_count = 0')
                        # qualityFile.append('skin_alternate_rotation = False')
                        qualityFile.append('support_conical_min_width = 10')
                        # qualityFile.append('infill_hollow = False')
                        # qualityFile.append('magic_fuzzy_skin_enabled = False')
                        # qualityFile.append('magic_fuzzy_skin_thickness = 0.3')
                        # qualityFile.append('magic_fuzzy_skin_point_density = 1.25')
                        # qualityFile.append('wireframe_enabled = False')
                        # qualityFile.append('wireframe_height = =machine_nozzle_head_distance')
                        # qualityFile.append('wireframe_roof_inset = =wireframe_height')
                        # qualityFile.append('wireframe_printspeed = 5')
                        # qualityFile.append('wireframe_printspeed_bottom = =wireframe_printspeed')
                        # qualityFile.append('wireframe_printspeed_up = =wireframe_printspeed')
                        # qualityFile.append('wireframe_printspeed_down = =wireframe_printspeed')
                        # qualityFile.append('wireframe_printspeed_flat = =wireframe_printspeed')
                        # qualityFile.append('wireframe_flow = 100')
                        # qualityFile.append('wireframe_flow_connection = =wireframe_flow')
                        # qualityFile.append('wireframe_flow_flat = =wireframe_flow')
                        # qualityFile.append('wireframe_top_delay = 0')
                        # qualityFile.append('wireframe_bottom_delay = 0')
                        # qualityFile.append('wireframe_flat_delay = 0.1')
                        # qualityFile.append('wireframe_up_half_speed = 0.3')
                        # qualityFile.append('wireframe_top_jump = 0.6')
                        # qualityFile.append('wireframe_fall_down = 0.5')
                        # qualityFile.append('wireframe_drag_along = 0.6')
                        # qualityFile.append('wireframe_strategy = compensate')
                        # qualityFile.append('wireframe_straight_before_down = 20')
                        # qualityFile.append('wireframe_roof_fall_down = 2')
                        # qualityFile.append('wireframe_roof_drag_along = 0.8')
                        # qualityFile.append('wireframe_roof_outer_delay = 0.2')
                        # qualityFile.append('wireframe_nozzle_clearance = 1')
                        # qualityFile.append('ironing_enabled = False')
                        # qualityFile.append('ironing_pattern = zigzag')
                        # qualityFile.append('ironing_line_spacing = zigzag')
                        # qualityFile.append('ironing_pattern = zigzag')
                        # qualityFile.append('ironing_line_spacing = =machine_nozzle_tip_outer_diameter/2')
                        # qualityFile.append('ironing_flow = 10')
                        # qualityFile.append('ironing_inset = =wall_line_width_0 / 2')
                        fileContent = '\n'.join(qualityFile)
                        filesList.append((fileName, fileContent))
   
    for hotend in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
        if hotend['id'] != 'None':
            fileName = 'Cura 2/resources/variants/'+PS.cura2id+'_'+hotend['id'].replace(' ', '_')+'.inst.cfg'
            variant = []
            variant.append('[general]')
            variant.append('name = '+hotend['id'])
            variant.append('version = 2')
            variant.append('definition = '+PS.cura2id)
            variant.append('')
            variant.append('[metadata]')
            variant.append('author = '+PS.cura2Author)
            variant.append('type = variant')
            variant.append('setting_version = 2')
            variant.append('')
            variant.append('[values]')
            # machine settings
            variant.append('machine_nozzle_id = '+str(hotend['id']))
            variant.append('machine_nozzle_size = '+str(hotend['nozzleSize']))
            variant.append('machine_nozzle_tip_outer_diameter = '+str(hotend['nozzleTipOuterDiameter']))
            variant.append('machine_nozzle_head_distance = '+str(hotend['nozzleHeadDistance']))
            variant.append('machine_nozzle_expansion_angle = '+str(hotend['nozzleExpansionAngle']))
            variant.append('machine_heat_zone_length = 8')
            variant.append('machine_nozzle_heat_up_speed = '+str(hotend['heatUpSpeed']))
            variant.append('machine_nozzle_cool_down_speed = '+str(hotend['coolDownSpeed']))
            variant.append('machine_min_cool_heat_time_window = '+str(hotend['minimumCoolHeatTimeWindow']))
            fileContent = '\n'.join(variant)
            filesList.append((fileName, fileContent))

    fileName = 'Cura 2/plugins/PostProcessingPlugin/scripts/'+PS.cura2PostProcessingPluginName.replace(' ','')+'.py'
    postProcessing = []
    postProcessing.append('# Guillem Àvila Padró - May 2017')
    postProcessing.append('# Released under GNU LICENSE')
    postProcessing.append('# https://opensource.org/licenses/GPL-3.0')
    postProcessing.append('')
    postProcessing.append('# Set of post processing algorithms to make the best GCodes for your BCN3D Sigma')
    postProcessing.append('')
    postProcessing.append('from ..Script import Script')
    postProcessing.append('import math')
    postProcessing.append('class '+PS.cura2PostProcessingPluginName.replace(' ','')+'(Script):')
    postProcessing.append('')
    postProcessing.append('    def __init__(self):')
    postProcessing.append('        super().__init__()')
    postProcessing.append('')
    postProcessing.append('    def getSettingDataString(self):')
    postProcessing.append('        return """{')
    postProcessing.append('            "name":"'+PS.cura2PostProcessingPluginName+'",')
    postProcessing.append('            "key": "'+PS.cura2PostProcessingPluginName.replace(' ','')+'",')
    postProcessing.append('            "metadata": {},')
    postProcessing.append('            "version": 2,')
    postProcessing.append('            "settings": ')
    postProcessing.append('            {                ')
    postProcessing.append('                "activeExtruders":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Heat only essentials",')
    postProcessing.append('                    "description": "When printing with one hotend only, avoid heating the other one.",')
    postProcessing.append('                    "type": "bool",')
    postProcessing.append('                    "default_value": true')
    postProcessing.append('                },')
    postProcessing.append('                "fixFirstRetract":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Fix First Extrusion",')
    postProcessing.append('                    "description": "Zero extruders at the beginning, so it starts properly.",')
    postProcessing.append('                    "type": "bool",')
    postProcessing.append('                    "default_value": true')
    postProcessing.append('                },')
    postProcessing.append('                "fixTemperatureOscilation":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Fix Temperature Oscilation",')
    postProcessing.append('                    "description": "Fix bad target temperatures when printing with both extruders.",')
    postProcessing.append('                    "type": "bool",')
    postProcessing.append('                    "default_value": true')
    postProcessing.append('                },')
    postProcessing.append('                "fixToolChangeZHop":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Fix Tool Change Z Hop",')
    postProcessing.append('                    "description": "When changing between toolheads, first move X/Y and then move Z.",')
    postProcessing.append('                    "type": "bool",')
    postProcessing.append('                    "default_value": true')
    postProcessing.append('                },')
    postProcessing.append('                "zHopDistance":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Z Hop Distance",')
    postProcessing.append('                    "description": "Distance to lift Z when changing toolheads.",')
    postProcessing.append('                    "unit": "mm",')
    postProcessing.append('                    "type": "float",')
    postProcessing.append('                    "default_value": 2,')
    postProcessing.append('                    "minimum_value": "0",')
    postProcessing.append('                    "minimum_value_warning": "0",')
    postProcessing.append('                    "maximum_value_warning": "5",')
    postProcessing.append('                    "enabled": "fixToolChangeZHop"')
    postProcessing.append('                },')
    postProcessing.append('                "smartPurge":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "SmartPurge",')
    postProcessing.append('                    "description": "Add an extra prime amount to compensate oozed material while the Extruder was idle. Disable Prime tower to save time and filament.",')
    postProcessing.append('                    "type": "bool",')
    postProcessing.append('                    "default_value": true')
    postProcessing.append('                },')
    postProcessing.append('                "minimumExtrusionL":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Minimum Extrusion (Left)",')
    postProcessing.append('                    "description": "Minimum filament length to be extruded in the layer to avoid purge.",')
    postProcessing.append('                    "unit": "mm",')
    postProcessing.append('                    "type": "float",')
    postProcessing.append('                    "default_value": 1.5,')
    postProcessing.append('                    "minimum_value": "0",')
    postProcessing.append('                    "minimum_value_warning": "0",')
    postProcessing.append('                    "maximum_value_warning": "50",')
    postProcessing.append('                    "enabled": "smartPurge"')
    postProcessing.append('                },')
    postProcessing.append('                "purgeLengthL":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Purge Length (Left)",')
    postProcessing.append('                    "description": "Purged distance when purge is needed.",')
    postProcessing.append('                    "unit": "mm",')
    postProcessing.append('                    "type": "float",')
    postProcessing.append('                    "default_value": 1.5,')
    postProcessing.append('                    "minimum_value": "0",')
    postProcessing.append('                    "minimum_value_warning": "0",')
    postProcessing.append('                    "maximum_value_warning": "50",')
    postProcessing.append('                    "enabled": "smartPurge"')
    postProcessing.append('                },')
    postProcessing.append('                "minimumExtrusionR":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Minimum Extrusion (Right)",')
    postProcessing.append('                    "description": "Minimum filament length to be extruded in the layer to avoid purge.",')
    postProcessing.append('                    "unit": "mm",')
    postProcessing.append('                    "type": "float",')
    postProcessing.append('                    "default_value": 1.5,')
    postProcessing.append('                    "minimum_value": "0",')
    postProcessing.append('                    "minimum_value_warning": "0",')
    postProcessing.append('                    "maximum_value_warning": "50",')
    postProcessing.append('                    "enabled": "smartPurge"')
    postProcessing.append('                },')
    postProcessing.append('                "purgeLengthR":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Purge Length (Right)",')
    postProcessing.append('                    "description": "Purged distance when purge is needed.",')
    postProcessing.append('                    "unit": "mm",')
    postProcessing.append('                    "type": "float",')
    postProcessing.append('                    "default_value": 1.5,')
    postProcessing.append('                    "minimum_value": "0",')
    postProcessing.append('                    "minimum_value_warning": "0",')
    postProcessing.append('                    "maximum_value_warning": "50",')
    postProcessing.append('                    "enabled": "smartPurge"')
    postProcessing.append('                },')
    postProcessing.append('                "retractReduction":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Reduce Retraction",')
    postProcessing.append('                    "description": "Retract only on outer walls and top/bottom layers.",')
    postProcessing.append('                    "type": "bool",')
    postProcessing.append('                    "default_value": false')
    postProcessing.append('                },')
    postProcessing.append('                "avoidGrindingFilament":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Prevent Filament Grinding",')
    postProcessing.append('                    "description": "When retracting repeatedly, this option moves the hotend to the purge tray and primes the needed amount of filament to allow working on a new piece of it. Disabling this feature can flatten the filament and cause grinding issues.",')
    postProcessing.append('                    "type": "bool",')
    postProcessing.append('                    "default_value": true')
    postProcessing.append('                },')
    postProcessing.append('                "maxRetractsL":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Max. Retraction Count (Left)",')
    postProcessing.append('                    "description": "For the Left Extruder: Number of retractions occurring within the retraction distance. When the number of retractions is reached, active extruder will park, prime and come back (stronger than ever ;)",')
    postProcessing.append('                    "type": "int",')
    postProcessing.append('                    "default_value": 75,')
    postProcessing.append('                    "minimum_value": "0",')
    postProcessing.append('                    "minimum_value_warning": "0",')
    postProcessing.append('                    "maximum_value_warning": "90",')
    postProcessing.append('                    "enabled": "avoidGrindingFilament"')
    postProcessing.append('                },')
    postProcessing.append('                "maxRetractsR":')
    postProcessing.append('                {')
    postProcessing.append('                    "label": "Max. Retraction Count (Right)",')
    postProcessing.append('                    "description": "For the Right Extruder: Number of retractions occurring within the retraction distance. When the number of retractions is reached, active extruder will park, prime and come back (stronger than ever ;)",')
    postProcessing.append('                    "type": "int",')
    postProcessing.append('                    "default_value": 75,')
    postProcessing.append('                    "minimum_value": "0",')
    postProcessing.append('                    "minimum_value_warning": "0",')
    postProcessing.append('                    "maximum_value_warning": "90",')
    postProcessing.append('                    "enabled": "avoidGrindingFilament"')
    postProcessing.append('                }')
    postProcessing.append('            }')
    postProcessing.append('        }"""')
    postProcessing.append('')
    postProcessing.append('    def execute(self, data):')
    postProcessing.append('        activeExtruders = self.getSettingValueByKey("activeExtruders")')
    postProcessing.append('        fixFirstRetract = self.getSettingValueByKey("fixFirstRetract")')
    postProcessing.append('        fixTemperatureOscilation = self.getSettingValueByKey("fixTemperatureOscilation")')
    postProcessing.append('        fixToolChangeZHop = self.getSettingValueByKey("fixToolChangeZHop")')
    postProcessing.append('        zHopDistance = self.getSettingValueByKey("zHopDistance")')
    postProcessing.append('        smartPurge = self.getSettingValueByKey("smartPurge")')
    postProcessing.append('        minimumExtrusion = [self.getSettingValueByKey("minimumExtrusionL"), self.getSettingValueByKey("minimumExtrusionR")]')
    postProcessing.append('        purgeLength = [self.getSettingValueByKey("purgeLengthL"), self.getSettingValueByKey("purgeLengthR")]')
    postProcessing.append('        retractReduction = self.getSettingValueByKey("retractReduction")')
    postProcessing.append('        avoidGrindingFilament = self.getSettingValueByKey("avoidGrindingFilament")')
    postProcessing.append('        maxRetracts = [self.getSettingValueByKey("maxRetractsL"), self.getSettingValueByKey("maxRetractsR")]')
    postProcessing.append('')
    postProcessing.append('        startGcodeInfo = [";'+PS.cura2PostProcessingPluginName+' plugin enabled (Build '+PS.progenBuildNumber+')"]')
    postProcessing.append('')
    postProcessing.append('        # Do not change actions order as some may alter others')
    postProcessing.append('')
    postProcessing.append('        if activeExtruders or fixTemperatureOscilation or fixFirstRetract:')
    # postProcessing.append('        if activeExtruders:')
    postProcessing.append('            bothExtruders = False')
    postProcessing.append('            scanning = False')
    postProcessing.append('            printing = False')
    postProcessing.append('            idleExtruder = "T1"')
    postProcessing.append('            for layer in data:')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append('                for line in lines:')
    postProcessing.append('                    if scanning:')
    postProcessing.append('                        if line.startswith("T0") or (line.startswith("T1") and printing):')
    postProcessing.append('                            bothExtruders = True')
    postProcessing.append('                            break')
    postProcessing.append('                        elif line.startswith("T1") and not printing:')
    postProcessing.append('                            idleExtruder = "T0"')
    postProcessing.append('                        elif charsInLine("GXYE", line):')
    postProcessing.append('                            printing = True')
    postProcessing.append('                    else:')
    postProcessing.append('                        if line.startswith(";LAYER_COUNT:"):')
    postProcessing.append('                            scanning = True')
    postProcessing.append('                if bothExtruders:')
    postProcessing.append('                    break')
    postProcessing.append('')
    postProcessing.append('        if activeExtruders:')
    postProcessing.append('            startGcodeInfo.append("; - Heat only essentials")')
    postProcessing.append('            if not bothExtruders:')
    postProcessing.append('                startGcodeCorrected = False')
    postProcessing.append('                for layer in data:')
    postProcessing.append('                    index = data.index(layer)')
    postProcessing.append(r'                    lines = layer.split("\n")')
    postProcessing.append('                    tempIndex = 0')
    postProcessing.append('                    while tempIndex < len(lines):')
    postProcessing.append('                        line = lines[tempIndex]')
    postProcessing.append('                        if not startGcodeCorrected:')
    postProcessing.append('                            try:')
    postProcessing.append('                                if line.startswith("M108 P1"):')
    postProcessing.append('                                    del lines[tempIndex]')
    postProcessing.append('                                    tempIndex -=1')
    postProcessing.append('                                line1 = lines[tempIndex + 1]')
    postProcessing.append('                                line2 = lines[tempIndex + 2]')
    postProcessing.append('                                line3 = lines[tempIndex + 3]')
    postProcessing.append('                                line4 = lines[tempIndex + 4]')
    postProcessing.append('                                line5 = lines[tempIndex + 5]')

    postProcessing.append('                                if line.startswith(idleExtruder) and line1.startswith("G92 E0") and line2.startswith("G1 E") and line3.startswith("G92 E0") and line4.startswith("G4 P2000") and line5.startswith("G1 F2400 E-8"):')
    postProcessing.append('                                    del lines[tempIndex]')
    postProcessing.append('                                    del lines[tempIndex]')
    postProcessing.append('                                    del lines[tempIndex]')
    postProcessing.append('                                    del lines[tempIndex]')
    postProcessing.append('                                    del lines[tempIndex]')
    postProcessing.append('                                    del lines[tempIndex]')
    postProcessing.append('                                    startGcodeCorrected = True')
    postProcessing.append('                                    break')
    postProcessing.append('                            except:')
    postProcessing.append('                                pass')
    postProcessing.append('                        if idleExtruder != "T0":')
    postProcessing.append('                            if "T1" in line:')
    postProcessing.append('                                del lines[tempIndex]')
    postProcessing.append('                                tempIndex -= 1')
    postProcessing.append('                        elif idleExtruder != "T1":')
    postProcessing.append('                            if (line.startswith("M104 S") or line.startswith("M109 S")) and "T1" not in line: ')
    postProcessing.append('                                del lines[tempIndex]')
    postProcessing.append('                                tempIndex -= 1')
    postProcessing.append('                        tempIndex += 1')
    postProcessing.append(r'                    layer = "\n".join(lines)')
    postProcessing.append('                    data[index] = layer')
    postProcessing.append('')
    postProcessing.append('        if fixToolChangeZHop:')
    postProcessing.append('            startGcodeInfo.append("; - Fix Tool Change Z Hop")')
    postProcessing.append('            # Fix hop')
    postProcessing.append('            for layer in data:')
    postProcessing.append('                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append('                tempIndex = 0')
    postProcessing.append('                while tempIndex < len(lines):')
    postProcessing.append('                    try:')
    postProcessing.append('                        line = lines[tempIndex]')
    postProcessing.append('                        line1 = lines[tempIndex + 1]')
    postProcessing.append('                        line2 = lines[tempIndex + 2]')
    postProcessing.append('                        line3 = lines[tempIndex + 3]')
    postProcessing.append('                        line4 = lines[tempIndex + 4]')
    postProcessing.append('                        if (line == "T0" or line == "T1") and line1 == "G92 E0" and line2 == "G91" and "G1 F" in line3 and line4 == "G90":')
    postProcessing.append('                            lines[tempIndex + 3] = line3.split("Z")[0]+"Z"+str(zHopDistance)')
    postProcessing.append('                            lineCount = 6 # According to extruder_start_gcode in Sigma Extruders definitions')
    postProcessing.append('                            while not lines[tempIndex+lineCount].startswith(";TYPE"):')
    postProcessing.append('                                line = lines[tempIndex+lineCount]')
    postProcessing.append('                                if line.startswith("G"):')
    postProcessing.append('                                    if charsInLine(["G0", "F", "X", "Y", "Z"], line):')
    postProcessing.append('                                        zValue = self.getValue(line, "Z")')
    postProcessing.append('                                        fValue = self.getValue(line, "F")')
    postProcessing.append('                                    if lines[tempIndex+lineCount+1].startswith("G"):')
    postProcessing.append('                                        del lines[tempIndex+lineCount]')
    postProcessing.append('                                        lineCount -= 1')
    postProcessing.append('                                    else:')
    postProcessing.append('                                        xValue = self.getValue(line, "X")')
    postProcessing.append('                                        yValue = self.getValue(line, "Y")')
    postProcessing.append(r'                                        lines[tempIndex+lineCount] = "G0 F"+str(int(fValue))+" X"+str(xValue)+" Y"+str(yValue)+"\nG0 Z"+str(zValue)')
    postProcessing.append('                                lineCount += 1')
    postProcessing.append('                            break')
    postProcessing.append('                        tempIndex += 1')
    postProcessing.append('                    except:')
    postProcessing.append('                        break')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append('                data[index] = layer')
    postProcessing.append('            # Fix strange travel to X'+str(layerStartX)+' Y'+str(layerStartY)+'')
    postProcessing.append('            for layer in data:')
    postProcessing.append('                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append('                tempIndex = 0')
    postProcessing.append('                while tempIndex < len(lines):')
    postProcessing.append('                    try:')
    postProcessing.append('                        line = lines[tempIndex]')
    postProcessing.append('                        if " X'+str(layerStartX)+' Y'+str(layerStartY)+'" in line:')
    postProcessing.append('                            del lines[tempIndex]')
    postProcessing.append('                            tempIndex -= 1')
    postProcessing.append('                        tempIndex += 1')
    postProcessing.append('                    except:')
    postProcessing.append('                        break')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append('                data[index] = layer')
    postProcessing.append('')
    postProcessing.append('        if fixFirstRetract:')
    postProcessing.append('            startGcodeInfo.append("; - Fix First Extrusion")')
    postProcessing.append('            startGcodeCorrected = False')
    postProcessing.append('            eValue = 0')
    postProcessing.append('            fixExtruder = "T0"')
    postProcessing.append('            for layer in data:')
    postProcessing.append('                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append('                tempIndex = 0')
    postProcessing.append('                while tempIndex < len(lines):')
    postProcessing.append('                    try:')
    postProcessing.append('                        line = lines[tempIndex]')
    postProcessing.append('                        # Get retract value before starting the first layer')
    postProcessing.append('                        if not layer.startswith(";LAYER") and line.startswith("T1"):')
    postProcessing.append('                            lineCount = 0')
    postProcessing.append('                            while not lineCount > len(lines)-tempIndex or lines[tempIndex+lineCount].startswith("T0"):')
    postProcessing.append('                                line = lines[tempIndex+lineCount]')
    postProcessing.append('                                if charsInLine(["G", "F", "E-"], line):')
    postProcessing.append('                                    eValue = self.getValue(line, "E")')
    postProcessing.append('                                lineCount += 1')
    postProcessing.append('                        # Fix the thing')
    postProcessing.append('                        elif layer.startswith(";LAYER:0"):')
    postProcessing.append('                            line1 = lines[tempIndex + 1]')
    postProcessing.append('                            line2 = lines[tempIndex + 2]')
    postProcessing.append('                            line3 = lines[tempIndex + 3]')
    postProcessing.append('                            line4 = lines[tempIndex + 4]')
    postProcessing.append('                            line5 = lines[tempIndex + 5]')
    postProcessing.append('                            # detect first tool printing and remove unintentional retract before T1')
    postProcessing.append('                            if tempIndex == 0 and charsInLine(["G1 F", "E"], line1) and line2 =="G92 E0" and line4 == "T1" and line5 == "G92 E0":')
    postProcessing.append('                                del lines[tempIndex + 1]')
    postProcessing.append('                                del lines[tempIndex + 1]')
    postProcessing.append('                                tempIndex -= 1')
    postProcessing.append('                                fixExtruder = "T1"')
    postProcessing.append('                            # Add proper prime command to T1')
    postProcessing.append('                            elif fixExtruder == "T0":')
    postProcessing.append('                                lineCount = 0')
    postProcessing.append('                                while not lines[tempIndex+lineCount].startswith(";TYPE"):')
    postProcessing.append('                                    line = lines[tempIndex+lineCount]')
    postProcessing.append('                                    if charsInLine(["G0", "F", "X", "Y"], line):')
    postProcessing.append(r'                                        primeCommandLine = "G1 F2400 E0\nG92 E0 ; T0fix"')
    postProcessing.append(r'                                        lines[tempIndex+lineCount+1] = lines[tempIndex+lineCount+1]+"\n"+primeCommandLine+"\n"')
    postProcessing.append('                                        if bothExtruders:')
    postProcessing.append('                                            fixExtruder = "T1"')
    postProcessing.append('                                        else:')
    postProcessing.append('                                            fixExtruder = "none"')
    postProcessing.append('                                        break')
    postProcessing.append('                                    lineCount += 1')
    postProcessing.append('                                tempIndex += lineCount                                     ')
    postProcessing.append('                            elif fixExtruder == "T1" and line == "T1" and line1 == "G92 E0" and line2 == "G91" and "G1 F" in line3 and line4 == "G90":')
    postProcessing.append('                                lineCount = 6 # According to extruder_start_gcode in Sigma Extruders definitions')
    postProcessing.append('                                while not lines[tempIndex+lineCount].startswith(";TYPE"):')
    postProcessing.append('                                    line = lines[tempIndex+lineCount]')
    postProcessing.append('                                    if charsInLine(["G0", "F", "X", "Y"], line):')
    postProcessing.append('                                        if charsInLine(["G1 F", " E"], lines[tempIndex+lineCount+1]):')
    postProcessing.append('                                            del lines[tempIndex+lineCount + 1]')
    postProcessing.append(r'                                        primeCommandLine = "G1 F2400 E"+str(abs(eValue))+"\nG92 E0 ; T1fix"')
    postProcessing.append(r'                                        lines[tempIndex+lineCount+1] = lines[tempIndex+lineCount+1]+"\n"+primeCommandLine+"\n"')
    postProcessing.append('                                        break')
    postProcessing.append('                                    lineCount += 1')
    postProcessing.append('                            startGcodeCorrected = True')
    postProcessing.append('                        tempIndex += 1')
    postProcessing.append('                    except:')
    postProcessing.append('                        break')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append('                data[index] = layer')
    postProcessing.append('                if startGcodeCorrected:')
    postProcessing.append('                    break')
    postProcessing.append('')
    postProcessing.append('        if smartPurge:')
    postProcessing.append('            startGcodeInfo.append("; - SmartPurge")')
    postProcessing.append('            if bothExtruders:')
    postProcessing.append('                extraPurges = []')
    postProcessing.append('                for layer in data:')
    postProcessing.append('                    index = data.index(layer)')
    postProcessing.append(r'                    lines = layer.split("\n")')
    postProcessing.append('                    tempIndex = 0')
    postProcessing.append('                    while tempIndex < len(lines):')
    postProcessing.append('                        if not layer.startswith(";LAYER:0") and layer.startswith(";LAYER:") and (lines[tempIndex].startswith("T0") or lines[tempIndex].startswith("T1")):')
    postProcessing.append('                            if lines[tempIndex].startswith("T0"):')
    postProcessing.append('                                countingForTool = 0')
    postProcessing.append('                            elif lines[tempIndex].startswith("T1"):')
    postProcessing.append('                                countingForTool = 1')
    postProcessing.append('                            lineCount = tempIndex - 1')
    postProcessing.append('                            while lineCount >= 0:')
    postProcessing.append('                                line = lines[lineCount]')
    postProcessing.append('                                if charsInLine("GFE", line) and self.getValue(line, "E") < minimumExtrusion[abs(countingForTool-1)]:')
    postProcessing.append('                                    extraPurges.append(index - 1)')
    postProcessing.append('                                    break')
    postProcessing.append('                                lineCount -= 1')
    postProcessing.append('                            break')
    postProcessing.append('                        tempIndex += 1')
    postProcessing.append('                for layer in data:')
    postProcessing.append('                    index = data.index(layer)')
    postProcessing.append(r'                    lines = layer.split("\n")')
    postProcessing.append('                    applyFix = False')
    postProcessing.append('                    if len(extraPurges) > 0:')
    postProcessing.append('                        if index == extraPurges[0]:')
    postProcessing.append('                            tempIndex = 0')
    postProcessing.append('                            while tempIndex < len(lines):')
    postProcessing.append('                                if lines[tempIndex].startswith("T0") or lines[tempIndex].startswith("T1"):')
    postProcessing.append('                                    applyFix = True')
    postProcessing.append('                                    if lines[tempIndex].startswith("T0"):')
    postProcessing.append('                                        countingForTool = 0')
    postProcessing.append('                                    elif lines[tempIndex].startswith("T1"):')
    postProcessing.append('                                        countingForTool = 1')
    postProcessing.append('                                elif applyFix and lines[tempIndex].startswith("M109 S"):')
    postProcessing.append('                                    lineCount = tempIndex')
    postProcessing.append('                                    while not lines[lineCount].startswith("M104 S"):')
    postProcessing.append('                                        lineCount += 1')
    postProcessing.append('                                        if charsInLine(["G1", "F", "X", "Y", "E"], lines[lineCount]):')
    postProcessing.append('                                            lineCount = tempIndex')
    postProcessing.append('                                            break')
    postProcessing.append(r'                                    lines[tempIndex] = lines[tempIndex] + "\nM104 S"+str(self.getValue(lines[lineCount], "S"))+"\nG1 F2400 E"+str(8)+"\nG1 F"+str(getPurgeSpeed(lines, tempIndex, self))+" E"+str(8+purgeLength[countingForTool])+"\nG4 P2000\nG1 F2400 E"+str(purgeLength[countingForTool])+"\nG92 E0"')
    postProcessing.append('                                    break')
    postProcessing.append('                                tempIndex += 1')
    postProcessing.append('                            del extraPurges[0]')
    postProcessing.append(r'                    layer = "\n".join(lines)')
    postProcessing.append('                    data[index] = layer')
    postProcessing.append('')
    postProcessing.append('        if fixTemperatureOscilation:')
    postProcessing.append('            startGcodeInfo.append("; - Fix Temperature Oscilation")')
    postProcessing.append('            if bothExtruders:')
    postProcessing.append('                # Scan all temperatures')
    postProcessing.append('                temperatures = [] # [(layerIndex, lineIndex, action, line)]')
    postProcessing.append('                for layer in data:')
    postProcessing.append('                    index = data.index(layer)')
    postProcessing.append(r'                    lines = layer.split("\n")')
    postProcessing.append('                    tempIndex = 0')
    postProcessing.append('                    while tempIndex < len(lines):')
    postProcessing.append('                        line = lines[tempIndex]')
    postProcessing.append('                        if layer.startswith(";LAYER:"):')
    postProcessing.append('                            if line.startswith("M109"):')
    postProcessing.append('                                temperatures.append([index, tempIndex, "heat", line])')
    postProcessing.append('                            elif line.startswith("T"):')
    postProcessing.append('                                temperatures.append([index, tempIndex, "toolChange", line])')
    postProcessing.append('                            elif line.startswith("M104"):')
    postProcessing.append('                                temperatures.append([index, tempIndex, "unknown", line])')
    postProcessing.append('                        tempIndex += 1')
    postProcessing.append('                # Define "unknown" roles')
    postProcessing.append('                for elementIndex in range(len(temperatures)):')
    postProcessing.append('                    action = temperatures[elementIndex][2]')
    postProcessing.append('                    if action == "unknown":')
    postProcessing.append('                        if temperatures[elementIndex][3].startswith("M104 T"):')
    postProcessing.append('                            tempIndex = elementIndex -1')
    postProcessing.append('                            while tempIndex >= 0:')
    postProcessing.append('                                if temperatures[tempIndex][3].startswith("T"):')
    postProcessing.append('                                    action = "coolDownIdle"')
    postProcessing.append('                                    break')
    postProcessing.append('                                elif temperatures[tempIndex][3].startswith("M104 T"):')
    postProcessing.append('                                    action = "preheat"')
    postProcessing.append('                                    break')
    postProcessing.append('                                tempIndex -= 1')
    postProcessing.append('                        elif temperatures[elementIndex][3].startswith("M104 S"):')
    postProcessing.append('                            if elementIndex + 1 < len(temperatures):')
    postProcessing.append('                                if temperatures[elementIndex + 1][3].startswith("T"):')
    postProcessing.append('                                    action = "coolDownActive"')
    postProcessing.append('                                else:')
    postProcessing.append('                                    action = "setpoint"')
    postProcessing.append('                        temperatures[elementIndex][2] = action')
    postProcessing.append('                # Correct all temperatures            ')
    postProcessing.append('                for elementIndex in range(len(temperatures)):')
    postProcessing.append('                    action = temperatures[elementIndex][2]')
    postProcessing.append('                    if action == "preheat":')
    postProcessing.append('                        tempIndex = elementIndex + 1')
    postProcessing.append('                        while tempIndex < len(temperatures):')
    postProcessing.append('                            if temperatures[tempIndex][2] == "preheat":')
    postProcessing.append('                                break')
    postProcessing.append('                            elif temperatures[tempIndex][2] == "setpoint":')
    postProcessing.append('                                correctTemperatureValue = self.getValue(temperatures[tempIndex][3], "S") + '+str(temperatureInertiaInitialFix))
    postProcessing.append('                                temperatures[elementIndex][3] = temperatures[elementIndex][3].split("S")[0]+"S"+str(correctTemperatureValue)')
    postProcessing.append('                                break')
    postProcessing.append('                            tempIndex += 1')
    postProcessing.append('                    elif action == "heat":')
    postProcessing.append('                        tempIndex = elementIndex - 1')
    postProcessing.append('                        while tempIndex >= 0:')
    postProcessing.append('                            if temperatures[tempIndex][2] == "preheat":')
    postProcessing.append('                                correctTemperatureValue = self.getValue(temperatures[tempIndex][3], "S")')
    postProcessing.append('                                temperatures[elementIndex][3] = temperatures[elementIndex][3].split("S")[0]+"S"+str(correctTemperatureValue)')
    postProcessing.append('                                break')
    postProcessing.append('                            tempIndex -= 1')
    postProcessing.append('                    elif action == "coolDownIdle":')
    postProcessing.append('                        correctTemperatureValue = max(self.getValue(temperatures[elementIndex][3], "S") + '+str(temperatureInertiaInitialFix)+', '+str(standbyTemperature)+')')
    postProcessing.append('                        temperatures[elementIndex][3] = temperatures[elementIndex][3].split("S")[0]+"S"+str(correctTemperatureValue)')
    postProcessing.append('                    elif action == "coolDownActive":')
    postProcessing.append('                        tempIndex = elementIndex - 1')
    postProcessing.append('                        while tempIndex >= 0:')
    postProcessing.append('                            if temperatures[tempIndex][2] == "coolDownActive":')
    postProcessing.append('                                break                        ')
    postProcessing.append('                            if temperatures[tempIndex][2] == "setpoint":')
    postProcessing.append('                                correctTemperatureValue = self.getValue(temperatures[tempIndex][3], "S") + '+str(temperatureInertiaFinalFix))
    postProcessing.append('                                temperatures[elementIndex][3] = temperatures[elementIndex][3].split("S")[0]+"S"+str(correctTemperatureValue)')
    postProcessing.append('                                break')
    postProcessing.append('                            tempIndex -= 1')
    postProcessing.append('                # Set back new corrected temperatures')
    postProcessing.append('                for layer in data:')
    postProcessing.append('                    index = data.index(layer)')
    postProcessing.append(r'                    lines = layer.split("\n")')
    postProcessing.append('                    correctionsApplied = 0')
    postProcessing.append('                    tempIndex = 0')
    postProcessing.append('                    while tempIndex < len(lines) and len(temperatures) > 0:')
    postProcessing.append('                        if index == temperatures[0][0] and tempIndex == temperatures[0][1]:')
    postProcessing.append('                            lines[tempIndex] = temperatures[0][3]')
    postProcessing.append('                            del temperatures[0]')
    postProcessing.append('                        tempIndex += 1')
    postProcessing.append(r'                    layer = "\n".join(lines)')
    postProcessing.append('                    data[index] = layer')
    postProcessing.append('')
    postProcessing.append('        if retractReduction:')
    postProcessing.append('            startGcodeInfo.append("; - Reduce Retraction")')
    postProcessing.append('            removeRetracts = False')
    postProcessing.append('            for layer in data:')
    postProcessing.append('                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append('                tempIndex = 0')
    postProcessing.append('                if layer.startswith(";LAYER:") and not layer.startswith(";LAYER:0"):')
    postProcessing.append('                    while tempIndex < len(lines):')
    postProcessing.append('                        line = lines[tempIndex]')
    postProcessing.append('                        if line.startswith(";TYPE:WALL-OUTER") or line.startswith(";TYPE:SKIN") or line.startswith("T"):')
    postProcessing.append('                            removeRetracts = False')
    postProcessing.append('                        elif line.startswith(";TYPE:"):')
    postProcessing.append('                            removeRetracts = True')
    postProcessing.append('                        if removeRetracts:')
    postProcessing.append('                            if " E" in line and "G92" not in line:')
    postProcessing.append('                                eValue = self.getValue(line, "E")')
    postProcessing.append('                                lineCount = tempIndex - 1')
    postProcessing.append('                                try:')
    postProcessing.append('                                    if not lines[tempIndex+1].startswith("G92"):')
    postProcessing.append('                                        while lineCount >= 0:')
    postProcessing.append('                                            line = lines[lineCount]')
    postProcessing.append('                                            if " E" in line and "G92" not in line:')
    postProcessing.append('                                                if eValue < self.getValue(line, "E"):')
    postProcessing.append('                                                    if removeRetracts:')
    postProcessing.append('                                                        del lines[tempIndex]')
    postProcessing.append('                                                        tempIndex -= 1')
    postProcessing.append('                                                break')
    postProcessing.append('                                            lineCount -= 1')
    postProcessing.append('                                except:')
    postProcessing.append('                                    break')
    postProcessing.append('                        tempIndex += 1')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append('                data[index] = layer')
    postProcessing.append('')
    postProcessing.append('        if avoidGrindingFilament:            ')
    postProcessing.append('            startGcodeInfo.append("; - Prevent Filament Grinding")')
    postProcessing.append('            retractionsPerExtruder = [ [], [] ]')
    postProcessing.append('            purgeLength = 0')
    postProcessing.append('            countingForTool = 0')
    postProcessing.append('            for layer in data:')
    postProcessing.append('                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append('                tempIndex = 0')
    postProcessing.append('                if layer.startswith(";LAYER:"):')
    postProcessing.append('                    while tempIndex < len(lines):')
    postProcessing.append('                        line = lines[tempIndex]')
    postProcessing.append('                        if line.startswith("T0"):')
    postProcessing.append('                            countingForTool = 0')
    postProcessing.append('                        elif line.startswith("T1"):')
    postProcessing.append('                            countingForTool = 1')
    postProcessing.append('                        elif " E" in line and "G92" not in line:')
    postProcessing.append('                            eValue = self.getValue(line, "E")')
    postProcessing.append('                            lineCount = tempIndex - 1')
    postProcessing.append('                            try:')
    postProcessing.append('                                if not lines[tempIndex+1].startswith("G92"):')
    postProcessing.append('                                    while lineCount >= 0:')
    postProcessing.append('                                        line = lines[lineCount]')
    postProcessing.append('                                        if " E" in line and "G92" not in line:')
    postProcessing.append('                                            if eValue < self.getValue(line, "E"):')
    postProcessing.append('                                                purgeLength = round(self.getValue(line, "E") - eValue, 5)')
    postProcessing.append('                                                retractionsPerExtruder[countingForTool].append(eValue)')
    postProcessing.append('                                                if len(retractionsPerExtruder[countingForTool]) > maxRetracts[countingForTool]:')
    postProcessing.append('                                                    if (retractionsPerExtruder[countingForTool][-1] - retractionsPerExtruder[countingForTool][0]) < purgeLength:')
    postProcessing.append('                                                        # Delete extra travels')
    postProcessing.append('                                                        lineCount2 = tempIndex + 1')
    postProcessing.append('                                                        while lines[lineCount2].startswith("G0"):')
    postProcessing.append('                                                            if lines[lineCount2 + 1].startswith("G0"):')
    postProcessing.append('                                                                del lines[lineCount2]')
    postProcessing.append('                                                            else:')
    postProcessing.append('                                                                lineCount2 += 1')
    postProcessing.append('                                                        # Add purge commands')
    postProcessing.append(r'                                                        lines[tempIndex] = lines[tempIndex]+" ;prevent filament grinding on T"+str(countingForTool)+"\nT"+str(abs(countingForTool-1))+"\nT"+str(countingForTool)+"\nG91\nG1 F12000 Z2\nG90\nG1 F2400 E"+str(round(eValue+purgeLength, 5))+"\nG1 F"+str(getPurgeSpeed(lines, tempIndex, self))+" E"+str(round(eValue+2*purgeLength, 5))+"\nG4 P2000\nG1 F2400 E"+str(round(eValue+purgeLength, 5))+"\nG92 E"+str(eValue)+"\nG0 F12000\n"+lines[tempIndex+1]+"\nG91\nG1 F12000 Z-2\nG90 ;end of the filament grinding prevention protocol"')
    postProcessing.append('                                                        del lines[tempIndex+1]')
    postProcessing.append('                                                        tempIndex -= 1')
    postProcessing.append('                                                        retractionsPerExtruder[countingForTool] = []')
    postProcessing.append('                                                    else:')
    postProcessing.append('                                                        del retractionsPerExtruder[countingForTool][0]')
    postProcessing.append('                                            break')
    postProcessing.append('                                        elif line.startswith("T") or line.startswith("G92"):')
    postProcessing.append('                                            break')
    postProcessing.append('                                        lineCount -= 1')
    postProcessing.append('                            except:')
    postProcessing.append('                                break')
    postProcessing.append('                        tempIndex += 1')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append('                data[index] = layer')
    postProcessing.append('')
    postProcessing.append('        # Write '+PS.cura2PostProcessingPluginName+' info')
    postProcessing.append('        for layer in data:')
    postProcessing.append('            index = data.index(layer)')
    postProcessing.append(r'            lines = layer.split("\n")')
    postProcessing.append('            for tempIndex in range(len(lines)):')
    postProcessing.append('                if layer.startswith(";Generated with Cura_SteamEngine ") and lines[tempIndex].startswith(";Sigma ProGen"):')
    postProcessing.append(r'                    lines[tempIndex] = lines[tempIndex]+"\n"+"\n".join(startGcodeInfo)')
    postProcessing.append(r'            layer = "\n".join(lines)')
    postProcessing.append('            data[index] = layer')
    postProcessing.append('')
    postProcessing.append('        return data')
    postProcessing.append('')
    postProcessing.append('def getPurgeSpeed(lines, tempIndex, script):')
    postProcessing.append('    lineCount = tempIndex - 1')
    postProcessing.append('    purgeSpeed = 25')
    postProcessing.append('    while lineCount + 1 < len(lines):')
    postProcessing.append('        line0 = lines[lineCount]')
    postProcessing.append('        line1 = lines[lineCount + 1]')
    postProcessing.append('        if charsInLine("GFXYE", line0) and charsInLine("GXYE", line1):')
    postProcessing.append('            fValue = script.getValue(line0, "F")')
    postProcessing.append('            x0Value, y0Value, e0Value = script.getValue(line0, "X"), script.getValue(line0, "Y"), script.getValue(line0, "E")')
    postProcessing.append('            x1Value, y1Value, e1Value = script.getValue(line1, "X"), script.getValue(line1, "Y"), script.getValue(line1, "E")')
    postProcessing.append('            movedDistance = ((x1Value - x0Value)**2 + (y1Value - y0Value)**2)**0.5')
    postProcessing.append('            extrudedDistance = e1Value - e0Value')
    postProcessing.append('            timeExtruding = 1/ (fValue / 60.) * movedDistance')
    postProcessing.append('            purgeSpeed = extrudedDistance / timeExtruding * 60 * 2 # multiplied by 2 to speed up the process')
    postProcessing.append('            break')
    postProcessing.append('        lineCount += 1')
    postProcessing.append('    return round(purgeSpeed, 5)')
    postProcessing.append('')
    postProcessing.append('def charsInLine(characters, line):')
    postProcessing.append('    for c in characters:')
    postProcessing.append('        if c not in line:')
    postProcessing.append('            return False')
    postProcessing.append('    return True')
    postProcessing.append('')
    fileContent = '\n'.join(postProcessing)
    filesList.append((fileName, fileContent))

    return filesList

def getLayerHeight(hotend, quality):
    rawLayerHeight = hotend['nozzleSize'] * quality['layerHeightMultiplier']
    if rawLayerHeight > 0.1:
        if rawLayerHeight > 0.2:
            base = 0.1
        else:
            base = 0.05
    else:
        base = 0.025
    return round(rawLayerHeight / base) * base

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
    maxPrintSpeed = (max(1, temperatureAdjustedToFlow(filament, hotend, layerHeight, speed) - getTemperature(hotend, filament, 'lowTemperature'))/float(max(1, getTemperature(hotend, filament, 'highTemperature')-getTemperature(hotend, filament, 'lowTemperature')))) * maxFlowValue(hotend, filament, layerHeight) / (hotend['nozzleSize']*layerHeight/60.)
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
    P = toolChangePurgeLength

    return (startPurgeLength, toolChangePurgeLength, F, S, E, P)

def retractValues(filament):
    if filament['isFlexibleMaterial']:
        useCoasting = 0
        useWipe = 1
        onlyRetractWhenCrossingOutline = 1
        retractBetweenLayers = 0
        useRetractionMinTravel = 1
        retractWhileWiping = 1
        onlyWipeOutlines = 1
    else:
        useCoasting = 0
        useWipe = 1
        onlyRetractWhenCrossingOutline = 0
        retractBetweenLayers = 0
        useRetractionMinTravel = 1
        retractWhileWiping = 1
        onlyWipeOutlines = 1
    return useCoasting, useWipe, onlyRetractWhenCrossingOutline, retractBetweenLayers, useRetractionMinTravel, retractWhileWiping, onlyWipeOutlines

def coastVolume(hotend, filament):
    return float("%.2f" % ((hotend['nozzleSize'])**3*filament['purgeLength']/16))

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

def getTemperature(hotend, filament, temperatureToAdjust):
    if temperatureToAdjust == "lowTemperature":
        adjustedTemperature = filament['printTemperature'][0] + hotend['temperatureCompensation']
    elif temperatureToAdjust == "highTemperature":
        adjustedTemperature = filament['printTemperature'][1] + hotend['temperatureCompensation']
    elif temperatureToAdjust == "standbyTemperature":
        adjustedTemperature = filament['standbyTemperature'] + hotend['temperatureCompensation']
    return adjustedTemperature

def defaultMaterialPrintTemperature(filament):
    # Exclusive function for Cura 2 to get default_material_print_temperature
    return int(round((filament['printTemperature'][0] + filament['printTemperature'][1])/2.))

def temperatureAdjustedToFlow(filament, hotend, layerHeight, speed, base = 5):
    # adaptative temperature according to flow values. Rounded to base
    flow = hotend['nozzleSize']*layerHeight*float(speed)/60

    # Warning if something is not working properly
    if int(flow) > int(maxFlowValue(hotend, filament, layerHeight)):
        print "\nwarning! you're trying to print at higher flow than allowed:", filament['id']+':', str(int(flow)), str(int(maxFlowValue(hotend, filament, layerHeight)))

    temperature = int(base * round((getTemperature(hotend, filament, 'lowTemperature') + flow/maxFlowValue(hotend, filament, layerHeight) * float(getTemperature(hotend, filament, 'highTemperature')-getTemperature(hotend, filament, 'lowTemperature')))/float(base)))
    return temperature

def fanSpeed(hotend, filament, temperature, layerHeight, base = 5):
    # adaptative fan speed according to temperature values. Rounded to base
    if getTemperature(hotend, filament, 'highTemperature') - getTemperature(hotend, filament, 'lowTemperature') == 0 or filament['fanPercentage'][1] == 0:
        fanSpeed = filament['fanPercentage'][0]
    else:
        fanSpeedForTemperature = int(base * round((filament['fanPercentage'][0] + (temperature-getTemperature(hotend, filament, 'lowTemperature'))/float(getTemperature(hotend, filament, 'highTemperature')-getTemperature(hotend, filament, 'lowTemperature'))*float(filament['fanPercentage'][1]-filament['fanPercentage'][0]))/float(base)))
        LayerHeightAtMaxFanSpeed = 0.025
        LayerHeightAtMinFanSpeed = 0.2
        fanSpeedForLayerHeight = int(base * round((filament['fanPercentage'][0] + (layerHeight - LayerHeightAtMaxFanSpeed)/float(LayerHeightAtMinFanSpeed-LayerHeightAtMaxFanSpeed)*float(filament['fanPercentage'][1]-filament['fanPercentage'][0]))/float(base)))
        fanSpeed = max(fanSpeedForTemperature, fanSpeedForLayerHeight)
    return min(fanSpeed, 100) # Repassar. Aquest 100 no hauria de ser necessari

def timeVsTemperature(element, value, command):

    # bed heating curve parameters
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
        if element['id'] == 'bed':
            if temperature <= 60:
                time = bedParameterA1 * math.log(-(bedParameterA2-bedParameterA3)/(float(temperature)-bedParameterA2))
            else:
                time = bedParameterB1 * math.log(-bedParameterB2/(float(temperature)-bedParameterB2-bedParameterB3))+bedParameterB4
        else:
            time = temperature / float(element['heatUpSpeed'])
        return max(0, time)

    # return temperature (ºC) reached after heating during given time (sec)
    elif command == 'getTemperature':
        time = value
        if element['id'] == 'bed':
            if time <= 180:
                temperature = bedParameterA2 - (bedParameterA2 - bedParameterA3) * math.exp(-time/bedParameterA1)
            else:
                temperature = bedParameterB2 + bedParameterB3 - bedParameterB2 * math.exp(-(time - bedParameterB4)/bedParameterB1)
        else:
            temperature = time * element['heatUpSpeed']
        return max(0, temperature)

def firstHeatSequence(hotendLeft, hotendRight, leftHotendTemp, rightHotendTemp, bedTemp, software):
    useSmartSequence = False
    if useSmartSequence:
        startSequenceString = '; Start Heating Sequence. If you changed temperatures manually all elements may not heat in sync,'
        bed = dict([('id', 'bed')])
        if software == 'Simplify3D':
            if hotendLeft['id'] != 'None':
                timeLeftHotend  = (timeVsTemperature(hotendLeft, leftHotendTemp, 'getTime'), '', hotendLeft, 'M104 ', 'M109 ', 'S[extruder0_temperature]', ' T0,')
            if hotendRight['id'] != 'None':
                timeRightHotend = (timeVsTemperature(hotendRight, rightHotendTemp, 'getTime'), '', hotendRight, 'M104 ', 'M109 ', 'S[extruder1_temperature]', ' T1,')
            timeBed         = (timeVsTemperature(bed, bedTemp, 'getTime'), '', bed, 'M140 ', 'M190 ', 'S[bed0_temperature]',       ',')
        elif software == 'Cura':
            startSequenceString = '\t;' + startSequenceString[2:-1] + '\n'
            if hotendLeft['id'] != 'None':
                timeLeftHotend  = (timeVsTemperature(hotendLeft, leftHotendTemp, 'getTime'), '\t', hotendLeft, 'M104 ', 'M109 ', 'S{print_temperature}',     ' T0\n')
            if hotendRight['id'] != 'None':
                timeRightHotend = (timeVsTemperature(hotendRight, rightHotendTemp, 'getTime'), '\t', hotendRight, 'M104 ', 'M109 ', 'S{print_temperature2}',    ' T1\n')
            timeBed         = (timeVsTemperature(bed, bedTemp, 'getTime'), '\t', bed, 'M140 ', 'M190 ', 'S{print_bed_temperature}', '\n')
        if rightHotendTemp != 0 and leftHotendTemp != 0:
            # IDEX
            startTimes = sorted([timeLeftHotend, timeRightHotend, timeBed])
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-2][0], 'getTemperature')))+startTimes[-1][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-3][0], 'getTemperature')))+startTimes[-1][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-3][-4]+startTimes[-3][-2]+startTimes[-3][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-3][-3]+startTimes[-3][-2]+startTimes[-3][-1]
        elif rightHotendTemp == 0:
            # MEX Left
            startTimes = sorted([timeLeftHotend, timeBed])
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-2][0], 'getTemperature')))+startTimes[-1][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1][-1:]
        elif leftHotendTemp == 0:
            # MEX Right
            startTimes = sorted([timeRightHotend, timeBed])
            startSequenceString += '\tT1\n' if software == 'Cura' else 'T1,'
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-2][0], 'getTemperature')))+startTimes[-1][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1][-1:]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1][-1:]
    else:
        if software == 'Simplify3D':
            if rightHotendTemp != 0 and leftHotendTemp != 0:
                # IDEX
                startSequenceString = 'M190 S[bed0_temperature],M104 S[extruder0_temperature],M104 T1 S[extruder1_temperature],M109 S[extruder0_temperature],M109 T1 S[extruder1_temperature],'
            elif rightHotendTemp == 0:
                # MEX Left
                startSequenceString = 'M190 S[bed0_temperature],M109 S[extruder0_temperature],'
            elif leftHotendTemp == 0:
                # MEX Right
                startSequenceString = 'T1,M190 S[bed0_temperature],M109 S[extruder1_temperature],'
        elif software == 'Cura':
            if rightHotendTemp != 0 and leftHotendTemp != 0:
                # IDEX
                startSequenceString = '\tM190 S{print_bed_temperature}\n\tM104 S{print_temperature}\n\tM104 T1 S{print_temperature2}\n\tM109 S{print_temperature}\n\tM109 T1 S{print_temperature2}\n'
            elif rightHotendTemp == 0:
                # MEX Left
                startSequenceString = '\tM190 S{print_bed_temperature}\n\tM109 S{print_temperature}\n'
            elif leftHotendTemp == 0:
                # MEX Right
                startSequenceString = '\tT1\n\tM190 S{print_bed_temperature}\n\tM109 S{print_temperature2}\n'
    return startSequenceString

def accelerationForPerimeters(nozzleSize, layerHeight, outerWallSpeed, base = 5, multiplier = 30000, defaultAcceleration = 2000):
    return min(defaultAcceleration, int(base * round((nozzleSize * layerHeight * multiplier * 1/(outerWallSpeed**(1/2.)))/float(base))))

def speedMultiplier(hotend, filament):
    if filament['isFlexibleMaterial']:
        return float(filament['defaultPrintSpeed'])/24*hotend['nozzleSize']
        # 24*hotend['nozzleSize'] -> experimental value that works better with flexibles
    else:
        return float(filament['defaultPrintSpeed'])/60
        # 60 -> speed for base material (PLA) at base quality (Standard)

def speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, layerHeight, firstLayerHeight, infillLayerInterval, quality, action):
    if action == 'MEX Left' or action == 'IDEX, Infill with Right' or action == 'IDEX, Supports with Right':
        primaryHotend = hotendLeft
        primaryFilament = filamentLeft
        secondaryHotend = hotendRight
        secondaryFilament = filamentRight
    elif action == 'MEX Right' or action == 'IDEX, Infill with Left' or action == 'IDEX, Supports with Left':
        primaryHotend = hotendRight
        primaryFilament = filamentRight
        secondaryHotend = hotendLeft
        secondaryFilament = filamentLeft

    primaryExtruderDefaultSpeed = quality['defaultSpeed']*speedMultiplier(primaryHotend, primaryFilament)
    primaryExtruderMaxSpeed = maxFlowValue(primaryHotend, primaryFilament, layerHeight)/(primaryHotend['nozzleSize']*layerHeight)
    firstLayerPrimaryExtruderMaxSpeed = maxFlowValue(primaryHotend, primaryFilament, firstLayerHeight)/(primaryHotend['nozzleSize']*firstLayerHeight)

    if 'MEX' in action:
        defaultSpeed = int(str(float(min(primaryExtruderDefaultSpeed, primaryExtruderMaxSpeed, primaryFilament['advisedMaxPrintSpeed']))).split('.')[0])
    else:
        secondaryExtruderMaxSpeed = maxFlowValue(secondaryHotend, secondaryFilament, infillLayerInterval*layerHeight)/(infillLayerInterval*layerHeight*secondaryHotend['nozzleSize'])
        defaultSpeed = int(str(float(min(primaryExtruderDefaultSpeed, primaryExtruderMaxSpeed, secondaryExtruderMaxSpeed, primaryFilament['advisedMaxPrintSpeed'], secondaryFilament['advisedMaxPrintSpeed']))).split('.')[0])

    maxAllowedSpeedMultiplier = primaryExtruderMaxSpeed / float(defaultSpeed)
    firstLayerMaxAllowedSpeedMultiplier = firstLayerPrimaryExtruderMaxSpeed / float(defaultSpeed)

    if primaryFilament['isFlexibleMaterial']:
        outlineUnderspeed = 1.00
    else:
        defaulOulineMultiplier =      primaryExtruderDefaultSpeed*quality['outlineUnderspeed']    /float(defaultSpeed)
        outlineUnderspeed    = float("%.2f" % min(maxAllowedSpeedMultiplier, defaulOulineMultiplier))

    defaultFirstLayerMultiplier = primaryExtruderDefaultSpeed*quality['firstLayerUnderspeed'] /float(defaultSpeed)

    if 'IDEX, Supports with' in action:
        maxAllowedSupportMultiplier = secondaryExtruderMaxSpeed / float(defaultSpeed)
        supportUnderspeed    = float("%.2f" % min(maxAllowedSpeedMultiplier, maxAllowedSupportMultiplier))
        firstLayerSecondaryExtruderMaxSpeed = maxFlowValue(secondaryHotend, secondaryFilament, firstLayerHeight)/(firstLayerHeight*secondaryHotend['nozzleSize'])
        firstLayerSecondaryExtruderMaxAllowedSpeedMultiplier = firstLayerSecondaryExtruderMaxSpeed / float(defaultSpeed)
        firstLayerUnderspeed = float("%.2f" % min(firstLayerMaxAllowedSpeedMultiplier, firstLayerSecondaryExtruderMaxAllowedSpeedMultiplier, defaultFirstLayerMultiplier))
    else:
        supportUnderspeedMultiplier = primaryExtruderDefaultSpeed*0.9 / float(defaultSpeed)
        supportUnderspeed    = float("%.2f" % min(maxAllowedSpeedMultiplier, supportUnderspeedMultiplier))        
        firstLayerUnderspeed = float("%.2f" % min(firstLayerMaxAllowedSpeedMultiplier, defaultFirstLayerMultiplier))

    return defaultSpeed*60, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed