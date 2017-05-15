#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - May 2017
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

import time
import math
import uuid

import Logger

def simplify3DProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, dataLog, engineData):
    engineDataDecoder(engineData)
    fff = []
    fff.append(r'<?xml version="1.0" encoding="utf-8"?>')
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
    fff.append(r'<profile name="'+fileName+r'" version="'+time.strftime("%Y-%m-%d")+" "+time.strftime("%H:%M:%S")+r'" app="S3D-Software 3.1.1">')
    fff.append('  <baseProfile></baseProfile>')
    fff.append('  <printMaterial></printMaterial>')
    fff.append('  <printQuality>'+defaultPrintQuality+'</printQuality>') #+extruder+secondaryExtruderAction+str(quality['id'])+
    if hotendLeft['id'] != 'None':
        fff.append('  <printExtruders>Left Extruder Only</printExtruders>')
    else:
        fff.append('  <printExtruders>Right Extruder Only</printExtruders>')        
    if hotendLeft['id'] != 'None':
        fff.append(r'  <extruder name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">')
        fff.append('    <toolheadNumber>0</toolheadNumber>')
        fff.append('    <diameter>'+str(hotendLeft['nozzleSize'])+'</diameter>')
        fff.append('    <autoWidth>0</autoWidth>')
        fff.append('    <width>'+str(hotendLeft['nozzleSize'] * 0.875)+'</width>')
        fff.append('    <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+'</extrusionMultiplier>')
        fff.append('    <useRetract>1</useRetract>')
        fff.append('    <retractionDistance>'+str(filamentLeft['retractionDistance'])+'</retractionDistance>')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>')
        fff.append('    <retractionZLift>0.05</retractionZLift>')
        fff.append('    <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+'</retractionSpeed>')
        fff.append('    <useCoasting>0</useCoasting>')
        fff.append('    <coastingDistance>0.2</coastingDistance>')
        fff.append('    <useWipe>0</useWipe>')
        fff.append('    <wipeDistance>5</wipeDistance>')
        fff.append('  </extruder>')
    else:
        fff.append(r'  <extruder name="">')
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
        fff.append('    <useWipe>0</useWipe>')
        fff.append('    <wipeDistance>0</wipeDistance>')
        fff.append('  </extruder>')
    if hotendRight['id'] != 'None':
        fff.append(r'  <extruder name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">')
        fff.append('    <toolheadNumber>1</toolheadNumber>')
        fff.append('    <diameter>'+str(hotendRight['nozzleSize'])+'</diameter>')
        fff.append('    <autoWidth>0</autoWidth>')
        fff.append('    <width>'+str(hotendRight['nozzleSize'] * 0.875)+'</width>')
        fff.append('    <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+'</extrusionMultiplier>')
        fff.append('    <useRetract>1</useRetract>')
        fff.append('    <retractionDistance>'+str(filamentRight['retractionDistance'])+'</retractionDistance>')
        fff.append('    <extraRestartDistance>0</extraRestartDistance>')
        fff.append('    <retractionZLift>0.05</retractionZLift>')
        fff.append('    <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+'</retractionSpeed>')
        fff.append('    <useCoasting>0</useCoasting>')
        fff.append('    <coastingDistance>0.2</coastingDistance>')
        fff.append('    <useWipe>0</useWipe>')
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
    fff.append('  <startPointOriginZ>300</startPointOriginZ>')
    fff.append('  <sequentialIslands>0</sequentialIslands>')
    fff.append('  <spiralVaseMode>0</spiralVaseMode>')
    fff.append('  <firstLayerHeightPercentage>125</firstLayerHeightPercentage>')
    fff.append('  <firstLayerWidthPercentage>100</firstLayerWidthPercentage>')
    fff.append('  <firstLayerUnderspeed>0.85</firstLayerUnderspeed>')
    fff.append('  <useRaft>0</useRaft>')
    fff.append('  <raftExtruder>0</raftExtruder>')
    fff.append('  <raftLayers>2</raftLayers>')
    fff.append('  <raftOffset>3</raftOffset>')
    fff.append('  <raftSeparationDistance>0.2</raftSeparationDistance>')
    fff.append('  <raftInfill>85</raftInfill>')
    fff.append('  <disableRaftBaseLayers>0</disableRaftBaseLayers>')
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
    fff.append('  <infillAngles>45,-45</infillAngles>')
    fff.append('  <overlapInfillAngles>1</overlapInfillAngles>')
    fff.append('  <generateSupport>0</generateSupport>')
    fff.append('  <supportExtruder>0</supportExtruder>')
    fff.append('  <supportInfillPercentage>25</supportInfillPercentage>')
    fff.append('  <supportExtraInflation>1</supportExtraInflation>')
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
        fff.append(r'  <temperatureController name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">')
        fff.append('    <temperatureNumber>0</temperatureNumber>')
        fff.append('    <isHeatedBed>0</isHeatedBed>')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>')
        fff.append(r'    <setpoint layer="1" temperature="150"/>')
        fff.append('  </temperatureController>')
    if hotendRight['id'] != 'None':
        fff.append(r'  <temperatureController name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">')
        fff.append('    <temperatureNumber>1</temperatureNumber>')
        fff.append('    <isHeatedBed>0</isHeatedBed>')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>')
        fff.append(r'    <setpoint layer="1" temperature="150"/>')
        fff.append('  </temperatureController>')
    if (hotendLeft['id'] != 'None' and filamentLeft['bedTemperature'] > 0) or (hotendRight['id'] != 'None' and filamentRight['bedTemperature'] > 0):
        fff.append('  <temperatureController name="Heated Bed">')
        fff.append('    <temperatureNumber>0</temperatureNumber>')
        fff.append('    <isHeatedBed>1</isHeatedBed>')
        fff.append('    <relayBetweenLayers>0</relayBetweenLayers>')
        fff.append('    <relayBetweenLoops>0</relayBetweenLoops>')
        fff.append('    <stabilizeAtStartup>0</stabilizeAtStartup>')
        fff.append(r'    <setpoint layer="1" temperature="50"/>')
        fff.append('  </temperatureController>')
    fff.append('  <fanSpeed>')
    fff.append(r'    <setpoint layer="1" speed="0" />')
    fff.append(r'    <setpoint layer="2" speed="100"/>')
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
    fff.append('  <endingGcode>M104 S0 T0\t\t\t;left extruder heater off,M104 S0 T1\t\t\t;right extruder heater off,M140 S0\t\t\t;heated bed heater off,G91\t\t\t;relative positioning,G1 Z+0.5 E-5 Y+10 F[travel_speed]\t;move Z up a bit and retract filament,G28 X0 Y0\t\t\t;move X/Y to min endstops so the head is out of the way,M84\t\t\t;steppers off,G90\t\t\t;absolute positioning,</endingGcode>')
    fff.append('  <exportFileFormat>gcode</exportFileFormat>')
    fff.append('  <celebration>0</celebration>')
    fff.append('  <celebrationSong></celebrationSong>')
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
    fff.append('  <filamentDiameter>2.85</filamentDiameter>')
    fff.append('  <filamentPricePerKg>19.95</filamentPricePerKg>')
    fff.append('  <filamentDensity>1.25</filamentDensity>')
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
    fff.append('  <allowThinWallGapFill>1</allowThinWallGapFill>')
    fff.append('  <thinWallAllowedOverlapPercentage>10</thinWallAllowedOverlapPercentage>')
    fff.append('  <horizontalSizeCompensation>-0.1</horizontalSizeCompensation>')
    # fff.append('  <overridePrinterModels>1</overridePrinterModels>')
    # fff.append('  <printerModelsOverride>BCN3DSigma.stl</printerModelsOverride>')
    # fff.append('  <autoConfigureMaterial name="'+str(filamentLeft)+" Left, "+str(filamentRight)+" Right"+r'">')
    for extruder in extruderPrintOptions:
        for quality in sorted(profilesData['quality'], key=lambda k: k['index']):
            infillPercentage = quality['infillPercentage']
            infillLayerInterval = 1
            overlapInfillAngles = 1
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
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M107'+"\t\t"+r';disable fan for support material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendRightTemperature, layerHeight))+"\t\t"+r';enable fan for part material,'
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
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendLeftTemperature, layerHeight))+"\t\t"+r';enable fan for part material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M107'+"\t\t"+r';disable fan for support material,' 
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
                            fanActionOnToolChange1 = '' # '{IF NEWTOOL=0} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendLeftTemperature, layerHeight))+"\t\t"+r';enable fan for perimeters,'
                            fanActionOnToolChange2 = '' # '{IF NEWTOOL=1} M107'+"\t\t"+r';disable fan for infill,'
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
                            fanActionOnToolChange1 = '' # '{IF NEWTOOL=0} M107'+"\t\t"+r';disable fan for infill,'
                            fanActionOnToolChange2 = '' # '{IF NEWTOOL=1} M106 S'+str(fanSpeed(primaryHotend, primaryFilament, hotendRightTemperature, layerHeight))+"\t\t"+r';enable fan for perimeters,'
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
            fff.append(r'  <autoConfigureQuality name="'+extruder+secondaryExtruderAction+str(quality['id'])+r'">')
            fff.append('    <globalExtrusionMultiplier>1</globalExtrusionMultiplier>')
            fff.append('    <fanSpeed>')
            fff.append(r'      <setpoint layer="1" speed="0" />')
            if primaryExtruder == 0:
                fff.append(r'      <setpoint layer="2" speed="'+str(fanSpeed(primaryHotend, primaryFilament, hotendLeftTemperature, layerHeight))+r'" />')
            else:
                fff.append(r'      <setpoint layer="2" speed="'+str(fanSpeed(primaryHotend, primaryFilament, hotendRightTemperature, layerHeight))+r'" />')
            fff.append('    </fanSpeed>')
            fff.append('    <filamentDiameter>'+str(primaryFilament['filamentDiameter'])+'</filamentDiameter>')
            fff.append('    <filamentPricePerKg>'+str(primaryFilament['filamentPricePerKg'])+'</filamentPricePerKg>')
            fff.append('    <filamentDensity>'+str(primaryFilament['filamentDensity'])+'</filamentDensity>')
            if hotendLeft['id'] != 'None':
                fff.append(r'    <extruder name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">')
                fff.append('      <toolheadNumber>0</toolheadNumber>')
                fff.append('      <diameter>'+str(hotendLeft['nozzleSize'])+'</diameter>')
                fff.append('      <autoWidth>0</autoWidth>')
                fff.append('      <width>'+str(hotendLeft['nozzleSize'] * 0.875)+'</width>')
                fff.append('      <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+'</extrusionMultiplier>')
                fff.append('      <useRetract>1</useRetract>')
                fff.append('      <retractionDistance>'+str(filamentLeft['retractionDistance'])+'</retractionDistance>')
                fff.append('      <extraRestartDistance>0</extraRestartDistance>')
                fff.append('      <retractionZLift>'+("%.2f" % (layerHeight/2.))+'</retractionZLift>')
                fff.append('      <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+'</retractionSpeed>')
                fff.append('      <useCoasting>'+str(retractValues(filamentLeft)[0])+'</useCoasting>')
                fff.append('      <coastingDistance>'+str(coastValue(hotendLeft, filamentLeft) / (layerHeight * hotendLeft['nozzleSize']))+'</coastingDistance>')
                fff.append('      <useWipe>'+str(retractValues(filamentLeft)[1])+'</useWipe>')
                fff.append('      <wipeDistance>'+str(hotendLeft['nozzleSize']*12.5)+'</wipeDistance>')
                fff.append('    </extruder>')
            if hotendRight['id'] != 'None':
                fff.append(r'    <extruder name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">')
                fff.append('      <toolheadNumber>1</toolheadNumber>')
                fff.append('      <diameter>'+str(hotendRight['nozzleSize'])+'</diameter>')
                fff.append('      <autoWidth>0</autoWidth>')
                fff.append('      <width>'+str(hotendRight['nozzleSize'] * 0.875)+'</width>')
                fff.append('      <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+'</extrusionMultiplier>')
                fff.append('      <useRetract>1</useRetract>')
                fff.append('      <retractionDistance>'+str(filamentRight['retractionDistance'])+'</retractionDistance>')
                fff.append('      <extraRestartDistance>0</extraRestartDistance>')
                fff.append('      <retractionZLift>'+str(layerHeight/2)+'</retractionZLift>')
                fff.append('      <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+'</retractionSpeed>')
                fff.append('      <useCoasting>'+str(retractValues(filamentRight)[0])+'</useCoasting>')
                fff.append('      <coastingDistance>'+str(coastValue(hotendRight, filamentRight) / (layerHeight * hotendRight['nozzleSize']))+'</coastingDistance>')
                fff.append('      <useWipe>'+str(retractValues(filamentRight)[1])+'</useWipe>')
                fff.append('      <wipeDistance>'+str(hotendRight['nozzleSize']*12.5)+'</wipeDistance>')
                fff.append('    </extruder>')
            fff.append('    <primaryExtruder>'+str(primaryExtruder)+'</primaryExtruder>')
            fff.append('    <raftExtruder>'+str(raftExtruder)+'</raftExtruder>')
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
            fff.append('    <overlapInfillAngles>'+str(overlapInfillAngles)+'</overlapInfillAngles>')
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
                fff.append(r'    <temperatureController name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">')
                fff.append('      <temperatureNumber>0</temperatureNumber>')
                fff.append('      <isHeatedBed>0</isHeatedBed>')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>')
                fff.append(r'      <setpoint layer="1" temperature="'+str(getTemperature(hotendLeft, filamentLeft, "highTemperature"))+r'"/>')
                fff.append(r'      <setpoint layer="2" temperature="'+str(hotendLeftTemperature)+r'"/>')
                fff.append('    </temperatureController>')
            if hotendRight['id'] != 'None':
                fff.append(r'    <temperatureController name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">')
                fff.append('      <temperatureNumber>1</temperatureNumber>')
                fff.append('      <isHeatedBed>0</isHeatedBed>')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>')
                fff.append(r'      <setpoint layer="1" temperature="'+str(getTemperature(hotendRight, filamentRight, "highTemperature"))+r'"/>')
                fff.append(r'      <setpoint layer="2" temperature="'+str(hotendRightTemperature)+r'"/>')
                fff.append('    </temperatureController>')
            if (hotendLeft['id'] != 'None' and filamentLeft['bedTemperature'] > 0) or (hotendRight['id'] != 'None' and filamentRight['bedTemperature'] > 0):
                fff.append(r'    <temperatureController name="Heated Bed">')
                fff.append('      <temperatureNumber>0</temperatureNumber>')
                fff.append('      <isHeatedBed>1</isHeatedBed>')
                fff.append('      <relayBetweenLayers>0</relayBetweenLayers>')
                fff.append('      <relayBetweenLoops>0</relayBetweenLoops>')
                fff.append('      <stabilizeAtStartup>0</stabilizeAtStartup>')
                fff.append(r'      <setpoint layer="1" temperature="'+str(bedTemperature)+r'"/>')
                fff.append('    </temperatureController>')
            if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':                    
                fff.append('    <toolChangeGcode>{IF NEWTOOL=0} T0\t\t\t;Start tool switch 0,{IF NEWTOOL=0} G1 F2400 E0,{IF NEWTOOL=0} M800 F'+str(purgeSpeedT0)+' S'+str(sParameterT0)+' E'+str(eParameterT0)+' P'+str(pParameterT0)+'\t\t;SmartPurge - Needs Firmware v01-1.2.3,;{IF NEWTOOL=0} G1 F'+str(purgeSpeedT0)+' E'+str(toolChangePurgeLengthT0)+'\t\t;Default purge value,'+fanActionOnToolChange1+',{IF NEWTOOL=1} T1\t\t\t;Start tool switch 1,{IF NEWTOOL=1} G1 F2400 E0,{IF NEWTOOL=1} M800 F'+str(purgeSpeedT1)+' S'+str(sParameterT1)+' E'+str(eParameterT1)+' P'+str(pParameterT1)+'\t\t;SmartPurge - Needs Firmware v01-1.2.3,;{IF NEWTOOL=1} G1 F'+str(purgeSpeedT1)+' E'+str(toolChangePurgeLengthT1)+'\t\t;Default purge,'+fanActionOnToolChange2+",G4 P2000\t\t\t\t;Stabilize Hotend's pressure,G92 E0\t\t\t\t;Zero extruder,G1 F3000 E-4.5\t\t\t\t;Retract,G1 F[travel_speed]\t\t\t;End tool switch,G91,G1 F[travel_speed] Z2,G90</toolChangeGcode>")
            else:
                fff.append('    <toolChangeGcode/>')
            if primaryFilament['isFlexibleMaterial']:
                reducedAccelerationForPerimeters = 2000
            else:
                reducedAccelerationForPerimeters = accelerationForPerimeters(primaryHotend['nozzleSize'], layerHeight, int(defaultSpeed/60. * outlineUnderspeed))
            fff.append(r'    <postProcessing>{REPLACE "; outer perimeter" "; outer perimeterM204 S'+str(reducedAccelerationForPerimeters)+r'"},{REPLACE "; inner perimeter" "; inner perimeterM204 S2000"},{REPLACE "; solid layer" "; solid layerM204 S2000"},{REPLACE "; infill" "; infillM204 S2000",{REPLACE "; support" "; supportM204 S2000"},{REPLACE "; layer end" "; layer endM204 S2000"},{REPLACE "F12000G1 Z'+str(round(layerHeight*firstLayerHeightPercentage/100., 3))+r' F1002G92 E0" "F12000G1 Z'+str(round(layerHeight*firstLayerHeightPercentage/100., 3))+r' F1002G1 E0.0000 F720G92 E0"}</postProcessing>')
            fff.append('  </autoConfigureQuality>')

            if dataLog != '--no-data' :
                # Store flows, speeds, temperatures and other data
                data = extruder, defaultSpeed, infillLayerInterval, layerHeight, hotendLeft, hotendRight, primaryExtruder, infillExtruder, supportExtruder, filamentLeft, filamentRight, quality, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed, firstLayerHeightPercentage, hotendLeftTemperature, hotendRightTemperature, bedTemperature
                Logger.writeData(data, dataLog)                        

    # fff.append('  </autoConfigureMaterial>')

    # Start gcode must be defined in autoConfigureExtruders. Otherwise you have problems with the first heat sequence in Dual Color prints.
    if hotendLeft['id'] != 'None':
        fff.append(r'  <autoConfigureExtruders name="Left Extruder Only"  allowedToolheads="1">')
        fff.append('    <startingGcode>;Sigma ProGen: '+str(SigmaProgenVersion)+',,'+firstHeatSequence(hotendLeft, hotendRight, hotendLeftTemperature, 0, bedTemperature, 'Simplify3D')+',G21\t\t;metric values,G90\t\t;absolute positioning,M82\t\t;set extruder to absolute mode,M107\t\t;start with the fan off,G28 X0 Y0\t\t;move X/Y to min endstops,G28 Z0\t\t;move Z to min endstops,T0\t\t;change to active toolhead,G92 E0\t\t;zero the extruded length,G1 Z5 F200\t\t;safety Z axis movement,G1 F'+str(purgeSpeedT0)+' E'+str(startPurgeLengthT0)+'\t;extrude '+str(startPurgeLengthT0)+'mm of feed stock,G92 E0\t\t;zero the extruded length again</startingGcode>')
        fff.append('    <layerChangeGcode>M104 S0 T1</layerChangeGcode>')
        fff.append('  </autoConfigureExtruders>')
    if hotendRight['id'] != 'None':
        fff.append(r'  <autoConfigureExtruders name="Right Extruder Only"  allowedToolheads="1">')
        fff.append('    <startingGcode>;Sigma ProGen: '+str(SigmaProgenVersion)+',,'+firstHeatSequence(hotendLeft, hotendRight, 0, hotendRightTemperature, bedTemperature, 'Simplify3D')+',G21\t\t;metric values,G90\t\t;absolute positioning,M82\t\t;set extruder to absolute mode,M107\t\t;start with the fan off,G28 X0 Y0\t\t;move X/Y to min endstops,G28 Z0\t\t;move Z to min endstops,T1\t\t;change to active toolhead,G92 E0\t\t;zero the extruded length,G1 Z5 F200\t\t;safety Z axis movement,G1 F'+str(purgeSpeedT1)+' E'+str(startPurgeLengthT1)+'\t;extrude '+str(startPurgeLengthT1)+'mm of feed stock,G92 E0\t\t;zero the extruded length again</startingGcode>')
        fff.append('    <layerChangeGcode>M104 S0 T0</layerChangeGcode>')
        fff.append('  </autoConfigureExtruders>')
    if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':
        fff.append(r'  <autoConfigureExtruders name="Both Extruders"  allowedToolheads="2">')
        fff.append('    <startingGcode>;Sigma ProGen: '+str(SigmaProgenVersion)+',,'+firstHeatSequence(hotendLeft, hotendRight, hotendLeftTemperature, hotendRightTemperature, bedTemperature, 'Simplify3D')+',G21\t\t;metric values,G90\t\t;absolute positioning,M107\t\t;start with the fan off,G28 X0 Y0\t\t;move X/Y to min endstops,G28 Z0\t\t;move Z to min endstops,T1\t\t;switch to the right extruder,G92 E0\t\t;zero the extruded length,G1 F'+str(purgeSpeedT1)+' E'+str(startPurgeLengthT1)+'\t;extrude '+str(startPurgeLengthT1)+'mm of feed stock,G92 E0\t\t;zero the extruded length again,G1 F200 E-9,T0\t\t;switch to the left extruder,G92 E0\t\t;zero the extruded length,G1 F'+str(purgeSpeedT0)+' E'+str(startPurgeLengthT0)+'\t;extrude '+str(startPurgeLengthT0)+'mm of feed stock,G92 E0\t\t;zero the extruded length again</startingGcode>')
        fff.append('    <layerChangeGcode></layerChangeGcode>')
        fff.append('  </autoConfigureExtruders>')

    fff.append('</profile>')

    fileName = fileName + '.fff'
    fileContent = '\n'.join(fff)
    return fileName, fileContent

def curaProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, dataLog, engineData):
    engineDataDecoder(engineData)
    
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
    ini.append('raft_margin = 3.0')                                     # default 5.0
    ini.append('raft_line_spacing = 2.0')                               # default 3.0
    ini.append('raft_base_thickness = '+str(layerHeight))               # default 0.3
    ini.append('raft_base_linewidth = '+str(hotend['nozzleSize']*5))    # default 1.0
    ini.append('raft_interface_thickness = '+str(layerHeight))          # default 0.27
    ini.append('raft_interface_linewidth = '+str(hotend['nozzleSize'])) # default 0.4
    ini.append('raft_airgap_all = 0.0')                                 # default 0.0
    ini.append('raft_airgap = 0.2')                                     # default 0.22
    ini.append('raft_surface_layers = 2')                               # default 2
    ini.append('raft_surface_thickness = '+str(layerHeight))            # default 0.27
    ini.append('raft_surface_linewidth = '+str(hotend['nozzleSize']))   # default 0.4
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
    ini.append('\t;Sigma ProGen: '+str(SigmaProgenVersion))
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
    ini.append('\tT'+str(primaryExtruder)+'                                 ;change to active toolhead')
    ini.append('\tG92 E0                            ;zero the extruded length')
    ini.append('\tG1 F'+str(purgeSpeed)+' E'+str(startPurgeLength)+'                    ;extrude '+str(startPurgeLength)+'mm of feed stock')
    ini.append('\tG92 E0                            ;zero the extruded length again')
    ini.append('\tG1 F2400 E-4')
    ini.append('end.gcode = M104 S0')
    ini.append('\tM104 T1 S0                        ;extruder heater off')
    ini.append('\tM140 S0                           ;heated bed heater off')
    ini.append('\tG91                               ;relative positioning')
    ini.append('\tG1 Z+0.5 E-5 Y+10 F{travel_speed} ;move Z up a bit and retract filament')
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops, so the head is out of the way')
    ini.append('\tM84                               ;steppers off')
    ini.append('\tG90                               ;absolute positioning')
    ini.append('\t;{profile_string}')
    ini.append('start2.gcode = ;Sliced at: {day} {date} {time}')
    ini.append('\t;Profile: '+str(fileName))
    ini.append('\t;Sigma ProGen: '+str(SigmaProgenVersion))
    ini.append('\t;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}')
    ini.append('\t;Print time: {print_time}')
    ini.append('\t;Filament used: {filament_amount}m {filament_weight}g')
    ini.append('\t;Filament cost: {filament_cost}')
    if printTemperature1 == 0:
        ini.append(firstHeatSequence(hotendLeft, hotendRight, printTemperature2, printTemperature2, bedTemperature, 'Cura'))
    elif printTemperature2 == 0:
        ini.append(firstHeatSequence(hotendLeft, hotendRight, printTemperature1, printTemperature1, bedTemperature, 'Cura'))
    else:
        ini.append(firstHeatSequence(hotendLeft, hotendRight, printTemperature1, printTemperature2, bedTemperature, 'Cura'))
    ini.append('\tG21                               ;metric values')
    ini.append('\tG90                               ;absolute positioning')
    ini.append('\tM107                              ;start with the fan off')
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops')
    ini.append('\tG28 Z0                            ;move Z to min endstops')
    ini.append('\tG1 Z5 F200                        ;safety Z axis movement')
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
    ini.append('end2.gcode = M104 T0 S0')
    ini.append('\tM104 T0 S0                        ;left extruder heater off')
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
    ini.append('\t;G1 F'+str(purgeSpeed)+' E'+str(toolChangePurgeLength)+'             ;Default purge')
    ini.append("\tG4 P2000                   ;Stabilize Hotend's pressure")
    ini.append('\tG92 E0                     ;Zero extruder')
    ini.append('\tG1 F2400 E-4               ;Retract')
    ini.append('\tG1 F{travel_speed}')
    ini.append('\tG91')
    ini.append('\tG1 F{travel_speed} Z2')
    ini.append('\tG90')

    if dataLog != '--no-data' :
        firstLayerHeightPercentage = int(float(firstLayerHeight) * 100 / float(layerHeight))
        # Store flows, speeds, temperatures and other data
        data = extruder, defaultSpeed, 1, layerHeight, hotendLeft, hotendRight, primaryExtruder, infillExtruder, supportExtruder, filamentLeft, filamentRight, quality, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed, firstLayerHeightPercentage, hotendLeftTemperature, hotendRightTemperature, bedTemperature
        Logger.writeData(data, dataLog)

    fileName = fileName + '.ini'
    fileContent = '\n'.join(ini)
    return fileName, fileContent

def cura2Profile(engineData):
    engineDataDecoder(engineData)

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
    cura2PostProcessingPluginName = 'Sigma Vitamins'
    machineSettingsPluginName = 'SigmaSettingsAction'
    filesList = [] # List containing tuples: (fileName, fileContent)

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

    fileName = 'Cura 2/resources/definitions/'+cura2id+'.def.json'
    definition = []
    definition.append(r'{')
    definition.append(r'    "id": "'+cura2id+r'",')
    definition.append(r'    "version": 2,')
    definition.append(r'    "name": "'+cura2Name+r'",')
    definition.append(r'    "inherits": "fdmprinter",')
    definition.append(r'    "metadata": {')
    definition.append(r'        "author": "'+cura2Author+r'",')
    definition.append(r'        "category": "'+cura2Category+r'",')
    definition.append(r'        "manufacturer": "'+cura2Manufacturer+r'",')
    definition.append(r'        "file_formats": "text/x-gcode",')
    definition.append(r'        "platform": "'+cura2id+r'_bed.obj",')
    # definition.append(r'        "platform_texture": "'+cura2id+r'backplate.png",')
    definition.append(r'        "platform_offset": [0, 0, 0],')
    definition.append(r'        "has_machine_quality": true,')
    definition.append(r'        "visible": true,')
    definition.append(r'        "has_materials": true,')
    definition.append(r'        "has_machine_materials": true,')
    definition.append(r'        "has_variant_materials": true,')
    definition.append(r'        "has_variants": true,')
    definition.append(r'        "preferred_material": "*'+cura2PreferredMaterial+r'*",')
    definition.append(r'        "preferred_variant": "*'+cura2PreferredVariant+r'*",')
    definition.append(r'        "preferred_quality": "*'+cura2PreferredQuality+r'*",')
    definition.append(r'        "variants_name": "Hotend",')
    definition.append(r'        "machine_extruder_trains":')
    definition.append(r'        {')
    definition.append(r'            "0": "'+cura2id+r'_extruder_left",')
    definition.append(r'            "1": "'+cura2id+r'_extruder_right"')
    definition.append(r'        },')
    definition.append(r'        "first_start_actions": [ "'+machineSettingsPluginName+r'" ],')
    definition.append(r'        "supported_actions": [ "'+machineSettingsPluginName+r'" ]')
    definition.append(r'    },')
    definition.append(r'    "overrides": {')
    definition.append(r'        "machine_name": { "default_value": "'+cura2Name+r'" },')
    definition.append(r'        "machine_width": { "default_value": 210 },')
    definition.append(r'        "machine_depth": { "default_value": 297 },')
    definition.append(r'        "machine_height": { "default_value": 210 },')
    definition.append(r'        "machine_heated_bed": { "default_value": true },')
    definition.append(r'        "machine_extruder_count": { "default_value": 2 },')
    definition.append(r'        "machine_center_is_zero": { "default_value": false },')
    definition.append(r'        "machine_gcode_flavor": { "default_value": "RepRap (Marlin/Sprinter)" },')
    definition.append(r'        "machine_head_with_fans_polygon":')
    definition.append(r'        {')
    definition.append(r'            "default_value":')
    definition.append(r'            [')
    definition.append(r'                [ -27.8, 39.6 ],')
    definition.append(r'                [ -27.8, -58.8 ],')
    definition.append(r'                [ 26.2, 39.6 ],')
    definition.append(r'                [ 26.2, -58.8 ]')
    definition.append(r'            ]')
    definition.append(r'        },')
    definition.append(r'        "gantry_height": { "default_value": 210 },')
    definition.append(r'        "extruder_prime_pos_z": { "default_value": 2.0 },') # The Z coordinate of the position where the nozzle primes at the start of printing.
    definition.append(r'        "extruder_prime_pos_abs": { "default_value": false },') # Make the extruder prime position absolute rather than relative to the last-known location of the head.
    definition.append(r'        "machine_max_feedrate_x": { "default_value": 200 },')
    definition.append(r'        "machine_max_feedrate_y": { "default_value": 200 },')
    definition.append(r'        "machine_max_feedrate_z": { "default_value": 15 },')
    definition.append(r'        "machine_acceleration": { "default_value": 2000 },')
    definition.append(r'        "layer_height_0": { "value": "min(extruderValues('+"'machine_nozzle_size'"+')) / 2" },')
    # definition.append(r'        "support_enable":')
    # definition.append(r'        {')
    # definition.append(r'            "default_value": false,')
    # definition.append(r'            "resolve": "'+"'True' if 'True' in extruderValues('support_enable') else 'False'"+r'"') # Not working
    # definition.append(r'        },')
    definition.append(r'        "machine_start_gcode": { "default_value": "\n;Sigma ProGen: '+str(SigmaProgenVersion)+r'\n\nG21\t\t;metric values\nG90\t\t;absolute positioning\nM82\t\t;set extruder to absolute mode\nM107\t\t;start with the fan off\nG28 X0 Y0\t\t;move X/Y to min endstops\nG28 Z0\t\t;move Z to min endstops\nG1 Z5 F200\t\t;safety Z axis movement\nT1\t\t;switch to the right extruder\nG92 E0\t\t;zero the extruded length\nG1 E10 F200\t\t;extrude 10mm of feed stock\nG92 E0\t\t;zero the extruded length\nT0\t\t;switch to the left extruder\nG92 E0\t\t;zero the extruded length\nG1 E10 F200\t\t;extrude 10mm of feed stock\nG92 E0\t\t;zero the extruded length\nG4 P2000\t\t;stabilize hotend'+"'"+r's pressure\nG1 F2400 E-8\t\t;retract\n" },')
    definition.append(r'        "machine_end_gcode": { "default_value": "\nM104 S0 T0\t\t;left extruder heater off\nM104 S0 T1\t\t;right extruder heater off\nM140 S0\t\t;heated bed heater off\nG91\t\t;relative positioning\nG1 Z+0.5 E-5 Y+10 F12000\t;move Z up a bit and retract filament\nG28 X0 Y0\t\t;move X/Y to min endstops so the head is out of the way\nM84\t\t;steppers off\nG90\t\t;absolute positioning\n" },')
    definition.append(r'        "prime_tower_position_x": { "default_value": 105 },')
    definition.append(r'        "prime_tower_position_y": { "default_value": 250 },')
    definition.append(r'        "machine_nozzle_temp_enabled": { "value": "True" },')
    definition.append(r'        "material_bed_temp_wait": { "value": "True" },')
    definition.append(r'        "material_print_temp_wait": { "value": "True" },')
    definition.append(r'        "material_bed_temp_prepend": { "value": "False" },') # Cura 2.5 ignores it
    definition.append(r'        "material_print_temp_prepend": { "value": "False" }') # Cura 2.5 ignores it
    definition.append(r'    }')
    definition.append(r'}')
    fileContent = '\n'.join(definition)
    filesList.append((fileName, fileContent))

    fileName = 'Cura 2/resources/extruders/'+cura2id+'_extruder_left.def.json'
    extruder = []
    extruder.append(r'{')
    extruder.append(r'    "id": "'+cura2id+r'_extruder_left",')
    extruder.append(r'    "version": 2,')
    extruder.append(r'    "name": "Extruder Left",')
    extruder.append(r'    "inherits": "fdmextruder",')
    extruder.append(r'    "metadata": {')
    extruder.append(r'        "machine": "'+cura2id+r'",')
    extruder.append(r'        "position": "0"')
    extruder.append(r'    },')
    extruder.append(r'')
    extruder.append(r'    "overrides": {')
    extruder.append(r'        "extruder_nr": {')
    extruder.append(r'            "default_value": 0,')
    extruder.append(r'            "maximum_value": "1"')
    extruder.append(r'        },')
    extruder.append(r'        "machine_nozzle_offset_x": { "default_value": 0.0 },')
    extruder.append(r'        "machine_nozzle_offset_y": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_start_code": { "default_value": "G91\nG1 F12000 Z2\nG90\n" },') # Should be set as a quality parameter, but Cura 2.5 doesn't allow it
    extruder.append(r'        "machine_extruder_start_pos_abs": { "default_value": false },')
    extruder.append(r'        "machine_extruder_start_pos_x": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_start_pos_y": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_end_code": { "default_value": "" },')
    extruder.append(r'        "machine_extruder_end_pos_abs": { "default_value": false },')
    extruder.append(r'        "machine_extruder_end_pos_x": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_end_pos_y": { "default_value": 0.0 },')
    extruder.append(r'        "extruder_prime_pos_x": { "default_value": 0.0 },')
    extruder.append(r'        "extruder_prime_pos_y": { "default_value": 0.0 }')
    extruder.append(r'    }')
    extruder.append(r'}')
    fileContent = '\n'.join(extruder)
    filesList.append((fileName, fileContent))

    fileName = 'Cura 2/resources/extruders/'+cura2id+'_extruder_right.def.json'
    extruder = []
    extruder.append(r'{')
    extruder.append(r'    "id": "'+cura2id+r'_extruder_right",')
    extruder.append(r'    "version": 2,')
    extruder.append(r'    "name": "Extruder Right",')
    extruder.append(r'    "inherits": "fdmextruder",')
    extruder.append(r'    "metadata": {')
    extruder.append(r'        "machine": "'+cura2id+r'",')
    extruder.append(r'        "position": "1"')
    extruder.append(r'    },')
    extruder.append(r'')
    extruder.append(r'    "overrides": {')
    extruder.append(r'        "extruder_nr": {')
    extruder.append(r'            "default_value": 1,')
    extruder.append(r'            "maximum_value": "1"')
    extruder.append(r'        },')
    extruder.append(r'        "machine_nozzle_offset_x": { "default_value": 0.0 },')
    extruder.append(r'        "machine_nozzle_offset_y": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_start_code": { "default_value": "G91\nG1 F12000 Z2\nG90\n" },') # Should be set as a quality parameter, but Cura 2.5 doesn't allow it
    extruder.append(r'        "machine_extruder_start_pos_abs": { "default_value": false },')
    extruder.append(r'        "machine_extruder_start_pos_x": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_start_pos_y": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_end_code": { "default_value": "" },')
    extruder.append(r'        "machine_extruder_end_pos_abs": { "default_value": false },')
    extruder.append(r'        "machine_extruder_end_pos_x": { "default_value": 0.0 },')
    extruder.append(r'        "machine_extruder_end_pos_y": { "default_value": 0.0 },')
    extruder.append(r'        "extruder_prime_pos_x": { "default_value": 0.0 },')
    extruder.append(r'        "extruder_prime_pos_y": { "default_value": 0.0 }')
    extruder.append(r'    }')
    extruder.append(r'}')
    fileContent = '\n'.join(extruder)
    filesList.append((fileName, fileContent))

    for filament in sorted(profilesData['filament'], key=lambda k: k['id']):
        fileName = 'Cura 2/resources/materials/'+cura2id+'/'+filament['brand'].replace(' ', '_')+'_'+filament['material'].replace(' ', '_')+'.xml.fdm_material'
        material = []
        material.append(r'<?xml version="1.0" encoding="UTF-8"?>')
        material.append(r'<fdmmaterial xmlns="http://www.ultimaker.com/material">')
        material.append(r'    <metadata>')
        material.append(r'        <name>')
        material.append(r'            <brand>'+filament['brand']+'</brand>')
        material.append(r'            <material>'+filament['material']+'</material>')
        material.append(r'            <color>'+filament['color']+'</color>')
        material.append(r'        </name>')
        material.append(r'        <GUID>'+str(uuid.uuid1())+'</GUID>')
        material.append(r'        <version>1</version>')
        material.append(r'        <color_code>'+filament['colorCode']+'</color_code>')
        if filament['brand'] == 'Colorfila':
            material.append(r'        <instructions>http://bcn3dtechnologies.com/en/3d-printer-filaments</instructions>')
            material.append(r'        <author>')
            material.append(r'            <organization>BCN3D Technologies</organization>')
            material.append(r'            <contact>BCN3D Support</contact>')
            material.append(r'            <email>info@bcn3dtechnologies.com</email>')
            material.append(r'            <phone>+34 934 137 088</phone>')
            material.append(r'            <address>')
            material.append(r'                <street>Esteve Terradas 1</street>')
            material.append(r'                <city>Castelldefels</city>')
            material.append(r'                <region>Barcelona</region>')
            material.append(r'                <zip>08860</zip>')
            material.append(r'                <country>Spain</country>')
            material.append(r'            </address>')
            material.append(r'        </author>')
            material.append(r'        <supplier>')
            material.append(r'            <organization>BCN3D Technologies</organization>')
            material.append(r'            <contact>BCN3D Support</contact>')
            material.append(r'            <email>info@bcn3dtechnologies.com</email>')
            material.append(r'            <phone>+34 934 137 088</phone>')
            material.append(r'            <address>')
            material.append(r'                <street>Esteve Terradas 1</street>')
            material.append(r'                <city>Castelldefels</city>')
            material.append(r'                <region>Barcelona</region>')
            material.append(r'                <zip>08860</zip>')
            material.append(r'                <country>Spain</country>')
            material.append(r'            </address>')
            material.append(r'        </supplier>')
            # material.append(r'        <EAN>11 22222 33333 4</EAN>')
            # material.append(r'        <MSDS>http://...</MSDS>')
            # material.append(r'        <TDS>http://...</TDS>')
        material.append(r'    </metadata>')
        material.append(r'    <properties>')
        material.append(r'        <density>'+str(filament['filamentDensity'])+'</density>')
        material.append(r'        <diameter>'+str(filament['filamentDiameter'])+'</diameter>')
        material.append(r'    </properties>')
        material.append(r'    <settings>')
        material.append(r'')
        material.append(r'        <machine>')
        material.append(r'           <machine_identifier manufacturer="'+cura2Manufacturer+r'" product="'+cura2id+r'" />')
        for hotend in sorted(profilesData['hotend'], key=lambda k: k['id']):
            if hotend['id'] != 'None':
                material.append(r'           <hotend id="'+hotend['id']+r'">')
                if filament['isAbrasiveMaterial'] and hotend['material'] == "Brass":
                    material.append(r'                <setting key="hardware compatible">no</setting>')
                else:
                    material.append(r'                <setting key="hardware compatible">yes</setting>')
                material.append(r'            </hotend>')
        material.append(r'       </machine>')
        material.append(r'')
        material.append(r'    </settings>')
        material.append(r'</fdmmaterial>')
        fileContent = '\n'.join(material)
        filesList.append((fileName, fileContent))

    for hotend in sorted(profilesData['hotend'], key=lambda k: k['id']):
        if hotend['id'] != 'None':
            for filament in sorted(profilesData['filament'], key=lambda k: k['id']):
                for quality in sorted(profilesData['quality'], key=lambda k: k['index']):
                    layerHeight = getLayerHeight(hotend, quality)
                    firstLayerHeight = hotend['nozzleSize']/2.
                    defaultSpeed, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed = speedValues(hotend, hotend, filament, filament, layerHeight, firstLayerHeight, 1, quality, 'MEX Left')
                    hotendLeftTemperature = temperatureAdjustedToFlow(filament, hotend, layerHeight, defaultSpeed)
                    startPurgeLength, toolChangePurgeLength, purgeSpeed, sParameter, eParameter, pParameter = purgeValues(hotend, filament, defaultSpeed, layerHeight)
                    # Create a new global quality for the new layer height
                    globalQualities = []
                    if layerHeight not in globalQualities:
                        globalQualities.append(layerHeight)
                        fileName = 'Cura 2/resources/quality/'+cura2id+'/'+cura2id+'_global_Layer_'+("%.2f" % layerHeight)+'_mm_Quality.inst.cfg'
                        qualityFile = []
                        qualityFile.append(r'[general]')
                        qualityFile.append(r'version = 2')
                        qualityFile.append(r'name = Global Layer '+("%.2f" % layerHeight)+' mm')
                        qualityFile.append(r'definition = '+cura2id+'\n')
                        qualityFile.append(r'')
                        qualityFile.append(r'[metadata]')
                        qualityFile.append(r'type = quality')
                        qualityFile.append(r'quality_type = layer'+("%.2f" % layerHeight)+'mm')
                        qualityFile.append(r'global_quality = True')
                        qualityFile.append(r'weight = '+str(len(globalQualities))+'\n')
                        qualityFile.append(r'')
                        qualityFile.append(r'[values]')
                        qualityFile.append(r'layer_height = '+("%.2f" % layerHeight)+'\n')
                        fileContent = '\n'.join(qualityFile)
                        filesList.append((fileName, fileContent))

                    fileName = 'Cura 2/resources/quality/'+cura2id+'/'+cura2id+'_'+hotend['id'].replace(' ', '_')+'_'+filament['brand'].replace(' ', '_')+'_'+filament['material'].replace(' ', '_')+'_'+quality['id'].replace(' ', '_')+'_Quality.inst.cfg'

                    # keep all default values commented

                    qualityFile = []
                    qualityFile.append(r'[general]')
                    qualityFile.append(r'version = 2')
                    qualityFile.append(r'name = '+quality['id']+' Quality')
                    qualityFile.append(r'definition = '+cura2id+'\n')
                    qualityFile.append(r'')
                    qualityFile.append(r'[metadata]')
                    qualityFile.append(r'type = quality')
                    qualityFile.append(r'quality_type = layer'+("%.2f" % layerHeight)+'mm')
                    qualityFile.append(r'material = '+filament['brand'].replace(' ', '_')+'_'+filament['material'].replace(' ', '_')+'_'+cura2id+'_'+hotend['id'].replace(' ', '_')+'\n')
                    qualityFile.append(r'weight = '+str(-(quality['index']-3))+'\n')
                    qualityFile.append(r'')
                    qualityFile.append(r'[values]')

                    
                    # qualityFile.append(r'machine_extruder_start_code = ="\nM800 F'+str(purgeSpeed)+' S'+str(sParameter)+' E'+str(eParameter)+' P'+str(pParameter)+r'\t;SmartPurge - Needs Firmware v01-1.2.3\nG4 P2000\t\t\t\t;Stabilize Hotend'+"'"+r's pressure\nG92 E0\t\t\t\t;Zero extruder\nG1 F3000 E-4.5\t\t\t\t;Retract\nG1 F12000\t\t\t;End tool switch\nG91\nG1 F12000 Z2\nG90\n"') # Keyword NOT WORKING on Cura 2.5

                    # resolution
                    qualityFile.append(r'layer_height = '+("%.2f" % layerHeight)+'\n')
                    qualityFile.append(r'line_width = =machine_nozzle_size * 0.875')
                    # qualityFile.append(r'wall_line_width = =line_width')
                    # qualityFile.append(r'wall_line_width_0 = =wall_line_width')
                    qualityFile.append(r'wall_line_width_x = =machine_nozzle_size * 0.85')
                    # qualityFile.append(r'skin_line_width = =line_width')
                    qualityFile.append(r'infill_line_width = =machine_nozzle_size * 1.25')
                    # qualityFile.append(r'skirt_brim_line_width = =line_width')
                    qualityFile.append(r'support_line_width = =infill_line_width')
                    # qualityFile.append(r'support_interface_line_width = =line_width')
                    # qualityFile.append(r'prime_tower_line_width = =line_width')

                    #shell
                    qualityFile.append(r'wall_thickness = =max( 3 * machine_nozzle_size, '+("%.2f" % quality['wallWidth'])+')')     # 3 minimum Perimeters needed
                    qualityFile.append(r'wall_0_wipe_dist = 0')
                    qualityFile.append(r'top_bottom_thickness = =max( 5 * layer_height, '+("%.2f" % quality['topBottomWidth'])+')') # 5 minimum layers needed
                    # qualityFile.append(r'top_thickness = =top_bottom_thickness')
                    # qualityFile.append(r'bottom_thickness = =top_bottom_thickness')
                    # qualityFile.append(r'top_bottom_pattern = =lines')
                    # qualityFile.append(r'top_bottom_pattern_0 = =top_bottom_pattern')
                    # qualityFile.append(r'wall_0_inset = 0')
                    # qualityFile.append(r'outer_inset_first = False')
                    # qualityFile.append(r'alternate_extra_perimeter = False')
                    if filament['isFlexibleMaterial']:
                        qualityFile.append(r'travel_compensate_overlapping_walls_enabled = False')
                    else: 
                        qualityFile.append(r'travel_compensate_overlapping_walls_enabled = True') 
                    # qualityFile.append(r'fill_perimeter_gaps = everywhere')
                    qualityFile.append(r'xy_offset = -0.1') 
                    qualityFile.append(r'z_seam_type = back') 
                    qualityFile.append(r'z_seam_x = 105') 
                    qualityFile.append(r'z_seam_y = 297') 
                    # qualityFile.append(r'skin_no_small_gaps_heuristic = True') 

                    # infill
                    qualityFile.append(r'infill_sparse_density = ='+("%.2f" % min(100, quality['infillPercentage'] * 1.25))+' if infill_pattern == '+"'"+'cubicsubdiv'+"'"+r' else '+("%.2f" % quality['infillPercentage'])+'\n') # 'if' is not working...
                    qualityFile.append(r'infill_pattern = cubic')
                    qualityFile.append(r'infill_angles = [ 0 ]')
                    # qualityFile.append(r'sub_div_rad_mult = 100')
                    # qualityFile.append(r'sub_div_rad_add = =wall_line_width_x')
                    # qualityFile.append(r'infill_overlap = =10 if infill_sparse_density < 95 and infill_pattern != '+"'"+'concentric'+"'"+r' else 0')
                    qualityFile.append("skin_overlap = =5 if top_bottom_pattern != 'concentric' else 0"+'\n')
                    # qualityFile.append(r'infill_wipe_dist = =wall_line_width_0 / 4 if wall_line_count == 1 else wall_line_width_x / 4')
                    qualityFile.append(r'infill_sparse_thickness = =layer_height')
                    # qualityFile.append(r'gradual_infill_steps = 0')
                    # qualityFile.append(r'gradual_infill_step_height = 5')
                    qualityFile.append(r'infill_before_walls = False')
                    # qualityFile.append(r'min_infill_area = 0')
                    # qualityFile.append(r'max_skin_angle_for_expansion = 20')

                    # material -> it's defined here to avoid the translation dictionary from xml file.
                    qualityFile.append(r'material_flow_dependent_temperature = True')
                    qualityFile.append(r'default_material_print_temperature = '+str(round((getTemperature(hotend, filament, 'highTemperature')-getTemperature(hotend, filament, 'lowTemperature'))/2.+getTemperature(hotend, filament, 'lowTemperature')))+'\n')
                    # qualityFile.append(r'material_print_temperature = =default_material_print_temperature')                        
                    qualityFile.append(r'material_print_temperature_layer_0 = ='+str(round((getTemperature(hotend, filament, 'highTemperature'))))+'\n')
                    temperatureInertiaFix = 5
                    qualityFile.append(r'material_initial_print_temperature = =max(-273.15, material_print_temperature - '+str(temperatureInertiaFix)+')')
                    qualityFile.append(r'material_final_print_temperature = =max(-273.15, material_print_temperature - 2.5)')
                    qualityFile.append(r'material_flow_temp_graph = [[1.0,'+str(getTemperature(hotend, filament, 'lowTemperature'))+'], ['+str(maxFlowValue(hotend, filament, layerHeight))+','+str(getTemperature(hotend, filament, 'highTemperature'))+']]')
                    # qualityFile.append(r'material_extrusion_cool_down_speed = 0.7') # this value depends on extruded flow (not material_flow)
                    qualityFile.append(r'material_bed_temperature = '+("%.2f" % filament['bedTemperature'])+'\n')
                    qualityFile.append(r'material_diameter = '+("%.2f" % filament['filamentDiameter'])+'\n')
                    qualityFile.append(r'material_flow = '+("%.2f" % (filament['extrusionMultiplier'] * 100))+'\n')
                    # qualityFile.append(r'retraction_enable = True')
                    # qualityFile.append(r'retract_at_layer_change = False')
                    qualityFile.append(r'retraction_amount = '+("%.2f" % filament['retractionDistance'])+'\n')
                    qualityFile.append(r'retraction_speed = '+("%.2f" % filament['retractionSpeed'])+'\n')
                    # qualityFile.append(r'retraction_retract_speed = =retraction_speed')
                    # qualityFile.append(r'retraction_prime_speed = =retraction_speed')
                    # qualityFile.append(r'retraction_extra_prime_amount = 0') # Adjust for flex materials
                    # qualityFile.append(r'retraction_min_travel = =line_width * 2') # if this value works better, update Cura & S3D
                    # qualityFile.append(r'retraction_count_max = 90')
                    # qualityFile.append(r'retraction_extrusion_window = =retraction_amount')
                    qualityFile.append(r'material_standby_temperature = '+("%.2f" % getTemperature(hotend, filament, 'standbyTemperature'))+'\n')
                    # qualityFile.append(r'switch_extruder_retraction_amount = =machine_heat_zone_length')
                    qualityFile.append(r'switch_extruder_retraction_speed = =retraction_speed')
                    # qualityFile.append(r'switch_extruder_extra_prime_amount = '+("%.2f" % filament['retractionSpeed'])+'\n') # Parameter that should be there to purge on toolchage
                    qualityFile.append(r'switch_extruder_prime_speed = =retraction_speed')

                    # speed
                    qualityFile.append(r'speed_print = '+("%.2f" % (defaultSpeed/60.))+'\n')
                    # qualityFile.append(r'speed_infill = =speed_print')
                    qualityFile.append(r'speed_wall = =round(speed_print - (speed_print - speed_print * '+("%.2f" % outlineUnderspeed)+') / 2, 1)')
                    qualityFile.append(r'speed_wall_0 = =round(speed_print * '+("%.2f" % outlineUnderspeed)+', 1)')
                    qualityFile.append(r'speed_wall_x = =speed_wall')
                    qualityFile.append(r'speed_topbottom = =speed_wall_0')
                    qualityFile.append(r'speed_support = =round(speed_print * '+("%.2f" % supportUnderspeed)+', 1)')
                    # qualityFile.append(r'speed_support_infill = =speed_support')
                    qualityFile.append(r'speed_support_interface = =speed_wall')
                    qualityFile.append(r'speed_travel = =round(speed_print if magic_spiralize else 200)')
                    qualityFile.append(r'speed_layer_0 = =round(speed_print * '+("%.2f" % firstLayerUnderspeed)+', 1)')
                    # qualityFile.append(r'speed_print_layer_0 = =speed_layer_0')
                    qualityFile.append(r'speed_travel_layer_0 = =round(speed_travel / 3, 1)')
                    # qualityFile.append(r'skirt_brim_speed = =speed_layer_0')
                    # qualityFile.append(r'speed_slowdown_layers = 2')
                    qualityFile.append(r'speed_equalize_flow_enabled = True')
                    qualityFile.append(r'speed_equalize_flow_max = 100')
                    qualityFile.append(r'acceleration_enabled = True')
                    qualityFile.append(r'acceleration_print = 2000')
                    # qualityFile.append(r'acceleration_infill = =acceleration_print')
                    qualityFile.append(r'acceleration_wall = =round(acceleration_print - (acceleration_print - acceleration_wall_0)/ 2)')
                    qualityFile.append(r'acceleration_wall_0 = '+str(int(accelerationForPerimeters(hotend['nozzleSize'], layerHeight, int(defaultSpeed/60. * outlineUnderspeed))))+'\n')
                    # qualityFile.append(r'acceleration_wall_x = =acceleration_wall')
                    qualityFile.append(r'acceleration_topbottom = =acceleration_wall_0')
                    qualityFile.append(r'acceleration_support = =acceleration_wall')
                    # qualityFile.append(r'acceleration_support_infill = =acceleration_support')
                    qualityFile.append(r'acceleration_support_interface = =acceleration_topbottom')
                    qualityFile.append(r'acceleration_travel = =acceleration_print if magic_spiralize else 2250')
                    qualityFile.append(r'acceleration_layer_0 = =acceleration_topbottom')
                    # qualityFile.append(r'acceleration_print_layer_0 = =acceleration_layer_0')
                    # qualityFile.append(r'acceleration_travel_layer_0 = =acceleration_layer_0 * acceleration_travel / acceleration_print')
                    # qualityFile.append(r'acceleration_skirt_brim = =acceleration_layer_0')
                    qualityFile.append(r'jerk_enabled = True')
                    qualityFile.append(r'jerk_print = =15') # Adjust all jerk
                    # qualityFile.append(r'jerk_infill = =jerk_print')
                    qualityFile.append(r'jerk_wall = =jerk_print * 0.75')
                    qualityFile.append(r'jerk_wall_0 = =jerk_wall * 0.5')
                    # qualityFile.append(r'jerk_wall_x = =jerk_wall')
                    qualityFile.append(r'jerk_topbottom = =jerk_print * 0.5')
                    qualityFile.append(r'jerk_support = =jerk_print * 0.75')
                    # qualityFile.append(r'jerk_support_infill = =jerk_support')
                    qualityFile.append(r'jerk_support_interface = =jerk_topbottom')
                    qualityFile.append(r'jerk_prime_tower = =jerk_print * 0.75')
                    qualityFile.append(r'jerk_travel = =jerk_print if magic_spiralize else 15')
                    qualityFile.append(r'jerk_layer_0 = =jerk_topbottom')
                    # qualityFile.append(r'jerk_print_layer_0 = =jerk_layer_0')
                    # qualityFile.append(r'jerk_travel_layer_0 = =jerk_layer_0 * jerk_travel / jerk_print')
                    # qualityFile.append(r'jerk_skirt_brim = =jerk_layer_0')

                    # travel
                    qualityFile.append(r'retraction_combing = noskin')
                    # qualityFile.append(r'travel_retract_before_outer_wall = False')
                    # qualityFile.append(r'travel_avoid_other_parts = True')
                    # qualityFile.append(r'travel_avoid_distance = =machine_nozzle_tip_outer_diameter / 2 * 1.25')
                    # qualityFile.append(r'start_layers_at_same_position = False') # different than z_seam
                    layerStartX, layerStartY = 105, 297
                    qualityFile.append(r'layer_start_x = '+str(layerStartX)+'\n') # different than z_seam
                    qualityFile.append(r'layer_start_y = '+str(layerStartY)+'\n') # different than z_seam
                    qualityFile.append(r'retraction_hop_enabled = True')
                    qualityFile.append(r'retraction_hop_only_when_collides = True')
                    qualityFile.append(r'retraction_hop = =0.5 * layer_height')
                    # qualityFile.append(r'retraction_hop_after_extruder_switch = True')

                    # cooling
                    if filament['fanPercentage'][1] > 0:
                        qualityFile.append(r'cool_fan_enabled = True')
                    else:
                        qualityFile.append(r'cool_fan_enabled = False')
                    qualityFile.append(r'cool_fan_speed = '+str(int(filament['fanPercentage'][1]))+'\n')
                    qualityFile.append(r'cool_fan_speed_min = '+str(int(filament['fanPercentage'][0]))+'\n')
                    # qualityFile.append(r'cool_fan_speed_max = =cool_fan_speed')
                    # qualityFile.append(r'cool_min_layer_time_fan_speed_max = 10')
                    # qualityFile.append(r'cool_fan_speed_0 = 0')
                    qualityFile.append("cool_fan_full_at_height = =0 if adhesion_type == 'raft' else layer_height_0 + 4 * layer_height"+'\n') # after 6 layers
                    # qualityFile.append(r'cool_min_layer_time = 5')
                    # qualityFile.append(r'cool_min_speed = 10')
                    # qualityFile.append(r'cool_lift_head = False')

                    # support
                    if filament['isSupportMaterial']:
                        # qualityFile.append(r'support_enable = True') # Not working
                        qualityFile.append(r'support_infill_rate = 25')
                        qualityFile.append(r'support_xy_distance = 0.5')
                        qualityFile.append(r'support_z_distance = 0')
                        qualityFile.append(r'support_interface_density = 100')
                        qualityFile.append(r'support_conical_enabled = False')
                        # qualityFile.append(r'support_conical_angle = 30')
                    else:
                        # qualityFile.append(r'support_enable = False')
                        qualityFile.append(r'support_infill_rate = 15')
                        qualityFile.append(r'support_xy_distance = 0.7')
                        qualityFile.append(r'support_z_distance = =layer_height')
                        qualityFile.append(r'support_interface_density = 75')
                        qualityFile.append(r'support_conical_enabled = True')
                        # qualityFile.append(r'support_conical_angle = 30')
                    # qualityFile.append(r'support_type = everywhere')
                    # qualityFile.append(r'support_pattern = zigzag')
                    # qualityFile.append(r'support_connect_zigzags = True')
                    # qualityFile.append(r'support_top_distance = =extruderValue(support_extruder_nr, 'support_z_distance')')
                    # qualityFile.append(r'support_bottom_distance = =extruderValue(support_extruder_nr, 'support_z_distance') if support_type == 'everywhere' else 0')
                    # qualityFile.append(r'support_xy_overrides_z = z_overrides_xy')
                    # qualityFile.append(r'support_xy_distance_overhang = =machine_nozzle_size / 2')
                    # qualityFile.append(r'support_bottom_stair_step_height = 0.3')
                    qualityFile.append(r'support_join_distance = 10')
                    qualityFile.append(r'support_offset = 1')
                    qualityFile.append(r'support_interface_enable = True')
                    qualityFile.append("support_interface_height = =5 * layer_height"+'\n')
                    # qualityFile.append("support_roof_height =extruderValue(support_interface_extruder_nr, 'support_interface_height')"+'\n')
                    # qualityFile.append("support_bottom_height = =extruderValue(support_interface_extruder_nr, 'support_interface_height')"+'\n')
                    qualityFile.append(r'support_interface_skip_height = =layer_height')
                    qualityFile.append(r'support_interface_pattern = lines')
                    # qualityFile.append(r'support_use_towers = True')
                    # qualityFile.append(r'support_tower_diameter = 3.0')
                    qualityFile.append(r'support_minimal_diameter = 1.0')
                    # qualityFile.append(r'support_tower_roof_angle = 65')

                    # platform_adhesion
                    # qualityFile.append(r'extruder_prime_pos_x = 0')
                    # qualityFile.append(r'extruder_prime_pos_y = 0')
                    qualityFile.append(r'adhesion_type = skirt')
                    qualityFile.append(r'skirt_line_count = 2')
                    # qualityFile.append(r'skirt_gap = 3')
                    qualityFile.append("skirt_brim_minimal_length = =round((material_diameter/2)**2 / (extruderValue(adhesion_extruder_nr, 'machine_nozzle_size')/2)**2 *"+str(startPurgeLength)+', 2)')
                    # qualityFile.append(r'brim_width = 8')
                    # qualityFile.append(r'brim_outside_only = True')
                    # qualityFile.append(r'raft_margin = 15')
                    qualityFile.append("raft_airgap = =min(extruderValues('machine_nozzle_size')) / 2"+'\n')
                    # qualityFile.append(r'layer_0_z_overlap = =raft_airgap / 2')
                    # qualityFile.append(r'raft_surface_layers = 2')
                    # qualityFile.append(r'raft_surface_thickness = =layer_height')
                    # qualityFile.append(r'raft_surface_line_width = =line_width')
                    # qualityFile.append(r'raft_surface_line_spacing = =raft_surface_line_width')
                    # qualityFile.append(r'raft_interface_thickness = =layer_height * 1.5')
                    # qualityFile.append(r'raft_interface_line_width = =line_width * 2')
                    # qualityFile.append(r'raft_interface_line_spacing = =raft_interface_line_width + 0.2')
                    # qualityFile.append(r'raft_base_thickness = =layer_height_0 * 1.2')
                    # qualityFile.append("raft_base_line_width = =extruderValue(adhesion_extruder_nr, 'machine_nozzle_size') * 2"+'\n')
                    # qualityFile.append(r'raft_base_line_spacing = =raft_base_line_width * 2')
                    # qualityFile.append(r'raft_speed = =speed_print / 60 * 30')
                    # qualityFile.append(r'raft_surface_speed = =raft_speed')
                    # qualityFile.append(r'raft_interface_speed = =raft_speed * 0.75')
                    # qualityFile.append(r'raft_base_speed = =raft_speed * 0.75')
                    # qualityFile.append(r'raft_acceleration = =acceleration_print')
                    # qualityFile.append(r'raft_surface_acceleration = =raft_acceleration')
                    # qualityFile.append(r'raft_interface_acceleration = =raft_acceleration')
                    # qualityFile.append(r'raft_base_acceleration = =raft_acceleration')
                    # qualityFile.append(r'raft_jerk = =jerk_print')
                    # qualityFile.append(r'raft_surface_jerk = =raft_jerk')
                    # qualityFile.append(r'raft_interface_jerk = =raft_jerk')
                    # qualityFile.append(r'raft_base_jerk = =raft_jerk')
                    # qualityFile.append(r'raft_fan_speed = 0')
                    # qualityFile.append(r'raft_surface_fan_speed = =raft_fan_speed')
                    # qualityFile.append(r'raft_interface_fan_speed = =raft_fan_speed')
                    # qualityFile.append(r'raft_base_fan_speed = =raft_fan_speed')

                    # dual
                    qualityFile.append(r'prime_tower_enable = False')
                    qualityFile.append(r'prime_tower_size = =max(15, round(math.sqrt(prime_tower_min_volume/layer_height), 2))')
                    qualityFile.append("prime_tower_min_volume = =round((material_diameter/2)**2 / (extruderValue(adhesion_extruder_nr, 'machine_nozzle_size')/2)**2 *"+str(toolChangePurgeLength)+', 2)')
                    qualityFile.append("prime_tower_wall_thickness = =2 * max(extruderValues('machine_nozzle_size'))"+'\n')
                    # qualityFile.append(r'prime_tower_flow = 100')
                    qualityFile.append(r'prime_tower_wipe_enabled = False')
                    qualityFile.append(r'dual_pre_wipe = False')
                    qualityFile.append(r'ooze_shield_enabled = False')
                    # qualityFile.append(r'ooze_shield_angle = 60')
                    # qualityFile.append(r'ooze_shield_dist = 2')

                    # meshfix
                    # qualityFile.append(r'meshfix_union_all = True')
                    # qualityFile.append(r'meshfix_union_all_remove_holes = False')
                    # qualityFile.append(r'meshfix_extensive_stitching = False')
                    # qualityFile.append(r'meshfix_keep_open_polygons = False')
                    # qualityFile.append(r'multiple_mesh_overlap = 0.15')
                    # qualityFile.append(r'carve_multiple_volumes = True')
                    # qualityFile.append(r'alternate_carve_order = True')

                    # blackmagic
                    # qualityFile.append(r'print_sequence = all_at_once')
                    # qualityFile.append(r'infill_mesh = False')
                    # qualityFile.append(r'infill_mesh_order = 0')
                    # qualityFile.append(r'support_mesh = False')
                    # qualityFile.append(r'anti_overhang_mesh = False')
                    # qualityFile.append(r'magic_mesh_surface_mode = normal')
                    # qualityFile.append(r'magic_spiralize = False')

                    # experimental
                    # qualityFile.append(r'draft_shield_enabled = False')
                    # qualityFile.append(r'draft_shield_dist = 10')
                    # qualityFile.append(r'draft_shield_height_limitation = False')
                    # qualityFile.append(r'draft_shield_height = 10')
                    # qualityFile.append(r'conical_overhang_enabled = False')
                    # qualityFile.append(r'conical_overhang_angle = 50')
                    qualityFile.append(r'coasting_enable = True')
                    qualityFile.append(r'coasting_volume = '+str(coastValue(hotend, filament))+'\n')
                    qualityFile.append(r'coasting_min_volume = =coasting_volume * 2')
                    # qualityFile.append(r'coasting_speed = 90')
                    # qualityFile.append(r'skin_outline_count = 0')
                    # qualityFile.append(r'skin_alternate_rotation = False')
                    qualityFile.append(r'support_conical_min_width = 10')
                    # qualityFile.append(r'infill_hollow = False')
                    # qualityFile.append(r'magic_fuzzy_skin_enabled = False')
                    # qualityFile.append(r'magic_fuzzy_skin_thickness = 0.3')
                    # qualityFile.append(r'magic_fuzzy_skin_point_density = 1.25')
                    # qualityFile.append(r'wireframe_enabled = False')
                    # qualityFile.append(r'wireframe_height = =machine_nozzle_head_distance')
                    # qualityFile.append(r'wireframe_roof_inset = =wireframe_height')
                    # qualityFile.append(r'wireframe_printspeed = 5')
                    # qualityFile.append(r'wireframe_printspeed_bottom = =wireframe_printspeed')
                    # qualityFile.append(r'wireframe_printspeed_up = =wireframe_printspeed')
                    # qualityFile.append(r'wireframe_printspeed_down = =wireframe_printspeed')
                    # qualityFile.append(r'wireframe_printspeed_flat = =wireframe_printspeed')
                    # qualityFile.append(r'wireframe_flow = 100')
                    # qualityFile.append(r'wireframe_flow_connection = =wireframe_flow')
                    # qualityFile.append(r'wireframe_flow_flat = =wireframe_flow')
                    # qualityFile.append(r'wireframe_top_delay = 0')
                    # qualityFile.append(r'wireframe_bottom_delay = 0')
                    # qualityFile.append(r'wireframe_flat_delay = 0.1')
                    # qualityFile.append(r'wireframe_up_half_speed = 0.3')
                    # qualityFile.append(r'wireframe_top_jump = 0.6')
                    # qualityFile.append(r'wireframe_fall_down = 0.5')
                    # qualityFile.append(r'wireframe_drag_along = 0.6')
                    # qualityFile.append(r'wireframe_strategy = compensate')
                    # qualityFile.append(r'wireframe_straight_before_down = 20')
                    # qualityFile.append(r'wireframe_roof_fall_down = 2')
                    # qualityFile.append(r'wireframe_roof_drag_along = 0.8')
                    # qualityFile.append(r'wireframe_roof_outer_delay = 0.2')
                    # qualityFile.append(r'wireframe_nozzle_clearance = 1')
                    fileContent = '\n'.join(qualityFile)
                    filesList.append((fileName, fileContent))
   
    for hotend in sorted(profilesData['hotend'], key=lambda k: k['id']):
        if hotend['id'] != 'None':
            fileName = 'Cura 2/resources/variants/'+cura2id+'_'+hotend['id'].replace(' ', '_')+'.inst.cfg'
            variant = []
            variant.append('[general]')
            variant.append('name = '+hotend['id']+'\n')
            variant.append('version = 2')
            variant.append('definition = '+cura2id+'\n')
            variant.append('')
            variant.append('[metadata]')
            variant.append('author = '+cura2Author+'\n')
            variant.append('type = variant')
            variant.append('')
            variant.append('[values]')
            # machine settings
            variant.append('machine_nozzle_size = '+str(hotend['nozzleSize'])+'\n')
            variant.append('machine_nozzle_tip_outer_diameter = '+str(hotend['nozzleTipOuterDiameter'])+'\n')
            variant.append('machine_nozzle_head_distance = '+str(hotend['nozzleHeadDistance'])+'\n')
            variant.append('machine_nozzle_expansion_angle = '+str(hotend['nozzleExpansionAngle'])+'\n')
            variant.append('machine_heat_zone_length = 8')
            variant.append('machine_nozzle_heat_up_speed = =(material_print_temperature-material_standby_temperature)/('+timeVsTemperature(hotend, 'material_print_temperature', 'heating', 'getTime')+'-'+timeVsTemperature(hotend, 'material_standby_temperature', 'heating', 'getTime')+')')
            variant.append('machine_nozzle_cool_down_speed = =(material_print_temperature-material_standby_temperature)/('+timeVsTemperature(hotend, 'material_standby_temperature', 'cooling', 'getTime')+'-'+timeVsTemperature(hotend, 'material_print_temperature', 'cooling', 'getTime')+')')
            variant.append('machine_min_cool_heat_time_window = '+str(hotend['minimumCoolHeatTimeWindow'])+'\n')
            fileContent = '\n'.join(variant)
            filesList.append((fileName, fileContent))

    fileName = 'Cura 2/plugins/PostProcessingPlugin/scripts/'+cura2PostProcessingPluginName.replace(' ','')+'.py'
    postProcessing = []
    postProcessing.append(r'# Guillem Àvila Padró - May 2017')
    postProcessing.append(r'# Released under GNU LICENSE')
    postProcessing.append(r'# https://opensource.org/licenses/GPL-3.0')
    postProcessing.append(r'')
    postProcessing.append(r'# Set of post processing algorithms to make the best GCodes for your BCN3D Sigma')
    postProcessing.append(r'')
    postProcessing.append(r'from ..Script import Script')
    postProcessing.append(r'import math')
    postProcessing.append(r'class '+cura2PostProcessingPluginName.replace(' ','')+'(Script):')
    postProcessing.append(r'')
    postProcessing.append(r'    def __init__(self):')
    postProcessing.append(r'        super().__init__()')
    postProcessing.append(r'')
    postProcessing.append(r'    def getSettingDataString(self):')
    postProcessing.append(r'        return """{')
    postProcessing.append(r'            "name":"'+cura2PostProcessingPluginName+r'",')
    postProcessing.append(r'            "key": "'+cura2PostProcessingPluginName.replace(' ','')+r'",')
    postProcessing.append(r'            "metadata": {},')
    postProcessing.append(r'            "version": 2,')
    postProcessing.append(r'            "settings": ')
    postProcessing.append(r'            {                ')
    postProcessing.append(r'                "activeExtruders":')
    postProcessing.append(r'                {')
    postProcessing.append(r'                    "label": "Heat only essentials",')
    postProcessing.append(r'                    "description": "When printing with one hotend only, avoid heating the other one.",')
    postProcessing.append(r'                    "type": "bool",')
    postProcessing.append(r'                    "default_value": true')
    postProcessing.append(r'                },')
    postProcessing.append(r'                "fixFirstRetract":')
    postProcessing.append(r'                {')
    postProcessing.append(r'                    "label": "Fix First Extrusion",')
    postProcessing.append(r'                    "description": "Avoid zeroing extruders at the beginning.",')
    postProcessing.append(r'                    "type": "bool",')
    postProcessing.append(r'                    "default_value": true')
    postProcessing.append(r'                },')
    postProcessing.append(r'                "fixTemperatureOscilation":')
    postProcessing.append(r'                {')
    postProcessing.append(r'                    "label": "Fix Temperature Oscilation",')
    postProcessing.append(r'                    "description": "Fix bad target temperatures when printing with both extruders.",')
    postProcessing.append(r'                    "type": "bool",')
    postProcessing.append(r'                    "default_value": true')
    postProcessing.append(r'                },')
    postProcessing.append(r'                "fixToolChangeZHop":')
    postProcessing.append(r'                {')
    postProcessing.append(r'                    "label": "Fix Tool Change Z Hop",')
    postProcessing.append(r'                    "description": "When changing between toolheads, first move X/Y and then move Z.",')
    postProcessing.append(r'                    "type": "bool",')
    postProcessing.append(r'                    "default_value": true')
    postProcessing.append(r'                },')
    postProcessing.append(r'                "zHopDistance":')
    postProcessing.append(r'                {')
    postProcessing.append(r'                    "label": "Z Hop Distance",')
    postProcessing.append(r'                    "description": "Distance to lift Z when changing toolheads.",')
    postProcessing.append(r'                    "unit": "mm",')
    postProcessing.append(r'                    "type": "float",')
    postProcessing.append(r'                    "default_value": 2,')
    postProcessing.append(r'                    "minimum_value": "0",')
    postProcessing.append(r'                    "minimum_value_warning": "0",')
    postProcessing.append(r'                    "maximum_value_warning": "5",')
    postProcessing.append(r'                    "enabled": "fixToolChangeZHop"')
    postProcessing.append(r'                },')
    postProcessing.append(r'                "smartPurge":')
    postProcessing.append(r'                {')
    postProcessing.append(r'                    "label": "SmartPurge",')
    postProcessing.append(r'                    "description": "Add an extra prime amount to compensate oozed material while the Extruder was idle. Disable Prime tower to save time and filament.",')
    postProcessing.append(r'                    "type": "bool",')
    postProcessing.append(r'                    "default_value": false')
    postProcessing.append(r'                },')
    postProcessing.append(r'                "leftHotendNozzleSize":')
    postProcessing.append(r'                {')
    postProcessing.append(r'                    "label": "Left Hotend",')
    postProcessing.append(r'                    "description": "Select Left Hotend.",')
    postProcessing.append(r'                    "type": "enum",')
    availableHotends = ""
    for hotend in sorted(profilesData['hotend'], key=lambda k: k['id']):
        if hotend['id'] != 'None':
            availableHotends += '"'+hotend['id'].replace(' ', '_')+'": "'+hotend['id']+'", '
    postProcessing.append(r'                    "options": {'+str(availableHotends[:-2])+'},')
    postProcessing.append(r'                    "default_value": "'+str(cura2PreferredVariant)+'",')
    postProcessing.append(r'                    "enabled": "smartPurge"')
    postProcessing.append(r'                },')
    availableFilaments = ""
    for filament in sorted(profilesData['filament'], key=lambda k: k['id']):
        availableFilaments += '"'+filament['id'].replace(' ', '_')+'": "'+filament['id']+'", '
    postProcessing.append(r'                "leftHotendFilament":')
    postProcessing.append(r'                {')
    postProcessing.append(r'                    "label": "Left Extruder Material",')
    postProcessing.append(r'                    "description": "Select which material is being used in Left Extruder to prime the right amount.",')
    postProcessing.append(r'                    "type": "enum",')
    postProcessing.append(r'                    "options": {'+str(availableFilaments[:-2])+'},')
    postProcessing.append(r'                    "default_value": "'+str(cura2PreferredMaterial)+'",')
    postProcessing.append(r'                    "enabled": "smartPurge"')
    postProcessing.append(r'                },')
    postProcessing.append(r'                "rightHotendNozzleSize":')
    postProcessing.append(r'                {')
    postProcessing.append(r'                    "label": "Right Hotend",')
    postProcessing.append(r'                    "description": "Select Right Hotend.",')
    postProcessing.append(r'                    "type": "enum",')
    postProcessing.append(r'                    "options": {'+str(availableHotends[:-2])+'},')
    postProcessing.append(r'                    "default_value": "'+str(cura2PreferredVariant)+'",')
    postProcessing.append(r'                    "enabled": "smartPurge"')
    postProcessing.append(r'                },')
    postProcessing.append(r'                "rightHotendFilament":')
    postProcessing.append(r'                {')
    postProcessing.append(r'                    "label": "Right Extruder Material",')
    postProcessing.append(r'                    "description": "Select which material is being used in Right Extruder to prime the right amount",')
    postProcessing.append(r'                    "type": "enum",')
    postProcessing.append(r'                    "options": {'+str(availableFilaments[:-2])+'},')
    postProcessing.append(r'                    "default_value": "'+str(cura2PreferredMaterial)+'",')
    postProcessing.append(r'                    "enabled": "smartPurge"')
    postProcessing.append(r'                }')
    postProcessing.append(r'            }')
    postProcessing.append(r'        }"""')
    postProcessing.append(r'')
    postProcessing.append(r'    def execute(self, data):')
    postProcessing.append(r'        activeExtruders = self.getSettingValueByKey("activeExtruders")')
    postProcessing.append(r'        fixFirstRetract = self.getSettingValueByKey("fixFirstRetract")')
    postProcessing.append(r'        fixTemperatureOscilation = self.getSettingValueByKey("fixTemperatureOscilation")')
    postProcessing.append(r'        fixToolChangeZHop = self.getSettingValueByKey("fixToolChangeZHop")')
    postProcessing.append(r'        zHopDistance = self.getSettingValueByKey("zHopDistance")')
    postProcessing.append(r'        smartPurge = self.getSettingValueByKey("smartPurge")')
    postProcessing.append(r'        leftHotendId = self.getSettingValueByKey("leftHotendNozzleSize")')
    postProcessing.append(r'        leftFilamentId = self.getSettingValueByKey("leftHotendFilament")')
    postProcessing.append(r'        rightHotendId = self.getSettingValueByKey("rightHotendNozzleSize")')
    postProcessing.append(r'        rightFilamentId = self.getSettingValueByKey("rightHotendFilament")')
    postProcessing.append(r'')
    postProcessing.append(r'        # Do not alter the order as some actions may alter others')
    postProcessing.append(r'')
    postProcessing.append(r'        if activeExtruders or fixTemperatureOscilation:')
    postProcessing.append(r'            bothExtruders = False')
    postProcessing.append(r'            scanning = False')
    postProcessing.append(r'            printing = False')
    postProcessing.append(r'            idleExtruder = "T1"')
    postProcessing.append(r'            for layer in data:')
    postProcessing.append(r'                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append(r'                for line in lines:                    ')
    postProcessing.append(r'                    if scanning:')
    postProcessing.append(r'                        if "G" in line and "X" in line and "Y" in line and "E" in line:')
    postProcessing.append(r'                            printing = True')
    postProcessing.append(r'                        elif line.startswith("T0") or (line.startswith("T1") and printing):')
    postProcessing.append(r'                            bothExtruders = True')
    postProcessing.append(r'                            break')
    postProcessing.append(r'                        elif line.startswith("T1") and not printing:')
    postProcessing.append(r'                            idleExtruder = "T0"')
    postProcessing.append(r'                    else:')
    postProcessing.append(r'                        if line.startswith(";LAYER_COUNT:"):')
    postProcessing.append(r'                            scanning = True')
    postProcessing.append(r'                if bothExtruders:')
    postProcessing.append(r'                    break')
    postProcessing.append(r'')
    postProcessing.append(r'        if activeExtruders and not bothExtruders:')
    postProcessing.append(r'            startGcodeCorrected = False')
    postProcessing.append(r'            for layer in data:')
    postProcessing.append(r'                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append(r'                tempIndex = 0')
    postProcessing.append(r'                while tempIndex < len(lines):')
    postProcessing.append(r'                    if not startGcodeCorrected:')
    postProcessing.append(r'                        try:')
    postProcessing.append(r'                            line = lines[tempIndex]')
    postProcessing.append(r'                            line1 = lines[tempIndex + 1]')
    postProcessing.append(r'                            line2 = lines[tempIndex + 2]')
    postProcessing.append(r'                            line3 = lines[tempIndex + 3]')
    postProcessing.append(r'                            if line.startswith(idleExtruder) and line1.startswith("G92 E0") and line2.startswith("G1 E") and line3.startswith("G92 E0"):')
    postProcessing.append(r'                                del lines[tempIndex]')
    postProcessing.append(r'                                del lines[tempIndex]')
    postProcessing.append(r'                                del lines[tempIndex]')
    postProcessing.append(r'                                del lines[tempIndex]')
    postProcessing.append(r'                                startGcodeCorrected = True  ')
    postProcessing.append(r'                        except:')
    postProcessing.append(r'                            pass')
    postProcessing.append(r'                    if idleExtruder != "T0":')
    postProcessing.append(r'                        if "T1" in line:')
    postProcessing.append(r'                            del lines[tempIndex]')
    postProcessing.append(r'                    elif idleExtruder != "T1":')
    postProcessing.append(r'                        if (line.startswith("M104 S") or line.startswith("M109 S")) and "T1" not in line: ')
    postProcessing.append(r'                            del lines[tempIndex]')
    postProcessing.append(r'                    tempIndex += 1')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append(r'                data[index] = layer')
    postProcessing.append(r'')
    postProcessing.append(r'        if fixToolChangeZHop:')
    postProcessing.append(r'            # Fix hop')
    postProcessing.append(r'            for layer in data:')
    postProcessing.append(r'                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append(r'                tempIndex = 0')
    postProcessing.append(r'                while tempIndex < len(lines):')
    postProcessing.append(r'                    try:')
    postProcessing.append(r'                        line = lines[tempIndex]')
    postProcessing.append(r'                        line1 = lines[tempIndex + 1]')
    postProcessing.append(r'                        line2 = lines[tempIndex + 2]')
    postProcessing.append(r'                        line3 = lines[tempIndex + 3]')
    postProcessing.append(r'                        line4 = lines[tempIndex + 4]')
    postProcessing.append(r'                        if (line == "T0" or line == "T1") and line1 == "G92 E0" and line2 == "G91" and "G1 F" in line3 and line4 == "G90":')
    postProcessing.append(r'                            lines[tempIndex + 3] = line3.split("Z")[0]+"Z"+str(zHopDistance)')
    postProcessing.append(r'                            lineCount = 6 # According to extruder_start_gcode in Sigma Extruders definitions')
    postProcessing.append(r'                            while not lines[tempIndex+lineCount].startswith(";TYPE"):')
    postProcessing.append(r'                                line = lines[tempIndex+lineCount]')
    postProcessing.append(r'                                if line.startswith("G"):')
    postProcessing.append(r'                                    if "G0" in line and "F" in line and "X" in line and "Y" in line and "Z" in line:')
    postProcessing.append(r'                                        zValue = self.getValue(line, "Z")')
    postProcessing.append(r'                                        fValue = self.getValue(line, "F")')
    postProcessing.append(r'                                    if lines[tempIndex+lineCount+1].startswith("G"):')
    postProcessing.append(r'                                        del lines[tempIndex+lineCount]')
    postProcessing.append(r'                                        lineCount -= 1')
    postProcessing.append(r'                                    else:')
    postProcessing.append(r'                                        xValue = self.getValue(line, "X")')
    postProcessing.append(r'                                        yValue = self.getValue(line, "Y")')
    postProcessing.append(r'                                        lines[tempIndex+lineCount] = "G0 F"+str(int(fValue))+" X"+str(xValue)+" Y"+str(yValue)+"\nG0 Z"+str(zValue)')
    postProcessing.append(r'                                lineCount += 1')
    postProcessing.append(r'                            break')
    postProcessing.append(r'                        tempIndex += 1')
    postProcessing.append(r'                    except:')
    postProcessing.append(r'                        break')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append(r'                data[index] = layer')
    postProcessing.append(r'')
    postProcessing.append(r'            # Fix strange travel to X'+str(layerStartX)+' Y'+str(layerStartY)+'')
    postProcessing.append(r'            for layer in data:')
    postProcessing.append(r'                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append(r'                for tempIndex in range(len(lines)):')
    postProcessing.append(r'                    try:')
    postProcessing.append(r'                        line = lines[tempIndex]')
    postProcessing.append(r'                        if " X'+str(layerStartX)+' Y'+str(layerStartY)+'" in line:')
    postProcessing.append(r'                            del lines[tempIndex]')
    postProcessing.append(r'                    except:')
    postProcessing.append(r'                        break')
    postProcessing.append(r'')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append(r'                data[index] = layer')
    postProcessing.append(r'')
    postProcessing.append(r'        if fixFirstRetract:')
    postProcessing.append(r'            startGcodeCorrected = False')
    postProcessing.append(r'            eValue = 0')
    postProcessing.append(r'            for layer in data:')
    postProcessing.append(r'                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append(r'                tempIndex = 0')
    postProcessing.append(r'                while tempIndex < len(lines):')
    postProcessing.append(r'                    try:')
    postProcessing.append(r'                        line = lines[tempIndex]')
    postProcessing.append(r'                        # Get retract value before starting the first layer')
    postProcessing.append(r'                        if not layer.startswith(";LAYER") and line.startswith("T1"):')
    postProcessing.append(r'                            lineCount = 0')
    postProcessing.append(r'                            while not lineCount > len(lines)-tempIndex or lines[tempIndex+lineCount].startswith("T0"):')
    postProcessing.append(r'                                line = lines[tempIndex+lineCount]')
    postProcessing.append(r'                                if "G" in line and "F" in line and "E-" in line:')
    postProcessing.append(r'                                    eValue = self.getValue(line, "E")')
    postProcessing.append(r'                                lineCount += 1')
    postProcessing.append(r'                        # Fix the thing')
    postProcessing.append(r'                        elif layer.startswith(";LAYER:0"):')
    postProcessing.append(r'                            line1 = lines[tempIndex + 1]')
    postProcessing.append(r'                            line2 = lines[tempIndex + 2]')
    postProcessing.append(r'                            line3 = lines[tempIndex + 3]')
    postProcessing.append(r'                            line4 = lines[tempIndex + 4]')
    postProcessing.append(r'                            line5 = lines[tempIndex + 5]')
    postProcessing.append(r'                            # Remove unintentional retract before T1')
    postProcessing.append(r'                            if tempIndex == 0 and "G1 F" in line1 and "E" in line1 and line2 =="G92 E0" and line4 == "T1" and line5 == "G92 E0":')
    postProcessing.append(r'                                del lines[tempIndex + 1]')
    postProcessing.append(r'                                del lines[tempIndex + 1]                            ')
    postProcessing.append(r'                            # Add proper prime command to T1')
    postProcessing.append(r'                            elif line == "T1" and line1 == "G92 E0" and line2 == "G91" and "G1 F" in line3 and line4 == "G90":')
    postProcessing.append(r'                                lineCount = 6 # According to extruder_start_gcode in Sigma Extruders definitions')
    postProcessing.append(r'                                while not lines[tempIndex+lineCount].startswith(";TYPE"):')
    postProcessing.append(r'                                    line = lines[tempIndex+lineCount]')
    postProcessing.append(r'                                    if "G0" in line and "F" in line and "X" in line and "Y" in line:')
    postProcessing.append(r'                                        primeCommandLine = "G1 F2400 E"+str(abs(eValue))+"\nG92 E0"')
    postProcessing.append(r'                                        lines[tempIndex+lineCount+1] = lines[tempIndex+lineCount+1]+"\n"+primeCommandLine+"\n"')
    postProcessing.append(r'                                        break')
    postProcessing.append(r'                                    lineCount += 1')
    postProcessing.append(r'                            startGcodeCorrected = True')
    postProcessing.append(r'                        tempIndex += 1')
    postProcessing.append(r'                    except:')
    postProcessing.append(r'                        break')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append(r'                data[index] = layer')
    postProcessing.append(r'                if startGcodeCorrected:')
    postProcessing.append(r'                    break')
    postProcessing.append(r'')
    postProcessing.append(r'        if smartPurge:')
    postProcessing.append(r'            for layer in data:')
    postProcessing.append(r'                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append(r'                tempIndex = 0')
    postProcessing.append(r'                while tempIndex < len(lines):')
    postProcessing.append(r'                    try:')
    postProcessing.append(r'                        line = lines[tempIndex]')
    postProcessing.append(r'                        line1 = lines[tempIndex + 1]')
    postProcessing.append(r'                        line2 = lines[tempIndex + 2]')
    postProcessing.append(r'                        line3 = lines[tempIndex + 3]')
    postProcessing.append(r'                        line4 = lines[tempIndex + 4]')
    postProcessing.append(r'                        if line == "T0" and line1 == "G92 E0" and line2 == "G91" and "G1 F" in line3 and line4 == "G90":')
    postProcessing.append(r'                            lineCount = 6 # According to extruder_start_gcode in Sigma Extruders definitions')
    postProcessing.append(r'                            while not lines[tempIndex+lineCount].startswith(";TYPE"):')
    postProcessing.append(r'                                lineCount += 1')
    postProcessing.append(r'                            primeLine = lines[tempIndex+lineCount+1]')
    postProcessing.append(r'                            eValue = self.getValue(primeLine, "E")')
    postProcessing.append(r'                            lines[tempIndex+lineCount+1] = primeLine.split("E")[0]+str(eValue+purgeValues(leftHotendId, leftFilamentId))+"\nG92 E"+str(eValue)')
    postProcessing.append(r'                            break')
    postProcessing.append(r'                        if line == "T1" and line1 == "G92 E0" and line2 == "G91" and "G1 F" in line3 and line4 == "G90":')
    postProcessing.append(r'                            lineCount = 6 # According to extruder_start_gcode in Sigma Extruders definitions')
    postProcessing.append(r'                            while not lines[tempIndex+lineCount].startswith(";TYPE"):')
    postProcessing.append(r'                                lineCount += 1')
    postProcessing.append(r'                            primeLine = lines[tempIndex+lineCount+1]')
    postProcessing.append(r'                            eValue = self.getValue(primeLine, "E")')
    postProcessing.append(r'                            lines[tempIndex+lineCount+1] = primeLine.split("E")[0]+str(eValue+purgeValues(rightHotendId, rightFilamentId))+"\nG92 E"+str(eValue)')
    postProcessing.append(r'                            break')
    postProcessing.append(r'                        tempIndex += 1')
    postProcessing.append(r'                    except:')
    postProcessing.append(r'                        break')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append(r'                data[index] = layer')
    postProcessing.append(r'')
    postProcessing.append(r'        if fixTemperatureOscilation and bothExtruders:')
    postProcessing.append(r'            for layer in data:')
    postProcessing.append(r'                index = data.index(layer)')
    postProcessing.append(r'                lines = layer.split("\n")')
    postProcessing.append(r'                correctionsApplied = 0')
    postProcessing.append(r'                tempIndex = 0')
    postProcessing.append(r'                while tempIndex < len(lines):')
    postProcessing.append(r'                    if layer.startswith(";LAYER:") and lines[tempIndex].startswith("M109 S") and correctionsApplied < 2:')
    postProcessing.append(r'                            lineCount = 0')
    postProcessing.append(r'                            while not lines[tempIndex+lineCount].startswith(";TYPE"):')
    postProcessing.append(r'                                line = lines[tempIndex+lineCount]')
    postProcessing.append(r'                                if line.startswith("M104 S"):')
    postProcessing.append(r'                                    correctTemperatureValue = self.getValue(line, "S") - '+str(temperatureInertiaFix)+'\n')
    postProcessing.append(r'                                    lines[tempIndex] = "M109 S"+str(correctTemperatureValue)')
    postProcessing.append(r'                                    correctionsApplied +=1')
    postProcessing.append(r'                                    break')
    postProcessing.append(r'                                lineCount += 1')
    postProcessing.append(r'                    tempIndex += 1')
    postProcessing.append(r'                layer = "\n".join(lines)')
    postProcessing.append(r'                data[index] = layer')
    postProcessing.append(r'')
    postProcessing.append(r'        return data')
    postProcessing.append(r'')
    postProcessing.append(r'def purgeValues(hotend, filament):')
    availableHotends = ""
    for hotend in sorted(profilesData['hotend'], key=lambda k: k['id']):
        if hotend['id'] != 'None':
            availableHotends += '"'+hotend['id'].replace(' ', '_')+'": '+str(hotend['nozzleSize'])+', '
    postProcessing.append(r'    hotends = {'+str(availableHotends[:-2])+'}')
    availableFilaments = ""
    for filament in sorted(profilesData['filament'], key=lambda k: k['id']):
        availableFilaments += '"'+filament['id'].replace(' ', '_')+'": '+str(filament['purgeLength'])+', '
    postProcessing.append(r'    filaments = {'+str(availableFilaments[:-2])+'}')
    postProcessing.append(r'')
    postProcessing.append(r'    # nozzleSizeBehavior')
    postProcessing.append(r'    maxPurgeLenghtAtHotendTip = 2.25 * filaments[filament]')
    postProcessing.append(r'    minPurgeLenghtAtHotendTip = 0.5  * filaments[filament]')
    postProcessing.append("    curveGrowth = 1 # Here we assume the growth curve is constant for all materials. Change this value if it's not"+'\n')
    postProcessing.append(r'    extraPrimeDistance = (maxPurgeLenghtAtHotendTip - (maxPurgeLenghtAtHotendTip-minPurgeLenghtAtHotendTip)*math.exp(-hotends[hotend]/float(curveGrowth)))/float(filaments[filament])')
    postProcessing.append(r'')
    postProcessing.append(r'    return round(extraPrimeDistance / 10, 5)')
    fileContent = '\n'.join(postProcessing)
    filesList.append((fileName, fileContent))

    fileName = 'Cura 2/plugins/'+machineSettingsPluginName+'/__init__.py'
    sigmaSettings = []
    sigmaSettings.append(r'from . import '+machineSettingsPluginName+'\n')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'from UM.i18n import i18nCatalog')
    sigmaSettings.append(r'catalog = i18nCatalog("cura")')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'def getMetaData():')
    sigmaSettings.append(r'    return {')
    sigmaSettings.append(r'        "plugin": {')
    sigmaSettings.append(r'            "name": catalog.i18nc("@label", "Sigma Settings action"),')
    sigmaSettings.append(r'            "author": "BCN3DTechnologies",')
    sigmaSettings.append(r'            "version": "1.0",')
    sigmaSettings.append(r'            "description": catalog.i18nc("@info:whatsthis", "Provides a way to change Sigma settings"),')
    sigmaSettings.append(r'            "api": 3')
    sigmaSettings.append(r'        }')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'def register(app):')
    sigmaSettings.append(r'    return { "machine_action": '+machineSettingsPluginName+'.'+machineSettingsPluginName+'() }')
    fileContent = '\n'.join(sigmaSettings)
    filesList.append((fileName, fileContent))

    fileName = 'Cura 2/plugins/'+machineSettingsPluginName+'/'+machineSettingsPluginName+'.py'
    sigmaSettings = []
    sigmaSettings.append(r'from PyQt5.QtCore import pyqtProperty, pyqtSignal')
    sigmaSettings.append(r'from UM.FlameProfiler import pyqtSlot')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'from cura.MachineAction import MachineAction')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'from UM.Application import Application')
    sigmaSettings.append(r'from UM.Settings.InstanceContainer import InstanceContainer')
    sigmaSettings.append(r'from UM.Settings.ContainerRegistry import ContainerRegistry')
    sigmaSettings.append(r'from UM.Settings.DefinitionContainer import DefinitionContainer')
    sigmaSettings.append(r'from UM.Logger import Logger')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'from cura.Settings.CuraContainerRegistry import CuraContainerRegistry')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'import UM.i18n')
    sigmaSettings.append(r'catalog = UM.i18n.i18nCatalog("cura")')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'##  This action allows for certain settings that are "machine only") to be modified.')
    sigmaSettings.append(r'#   It automatically detects machine definitions that it knows how to change and attaches itself to those.')
    sigmaSettings.append(r'class '+machineSettingsPluginName+'(MachineAction):')
    sigmaSettings.append(r'    def __init__(self, parent = None):')
    sigmaSettings.append(r'        super().__init__("'+machineSettingsPluginName+r'", catalog.i18nc("@action", "Sigma Settings"))')
    sigmaSettings.append(r'        self._qml_url = "'+machineSettingsPluginName+r'.qml"')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        self._container_index = 0')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        self._container_registry = ContainerRegistry.getInstance()')
    sigmaSettings.append(r'        self._container_registry.containerAdded.connect(self._onContainerAdded)')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    def _reset(self):')
    sigmaSettings.append(r'        global_container_stack = Application.getInstance().getGlobalContainerStack()')
    sigmaSettings.append(r'        if not global_container_stack:')
    sigmaSettings.append(r'            return')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        # Make sure there is a definition_changes container to store the machine settings')
    sigmaSettings.append(r'        definition_changes_container = global_container_stack.findContainer({"type": "definition_changes"})')
    sigmaSettings.append(r'        if not definition_changes_container:')
    sigmaSettings.append(r'            definition_changes_container = self._createDefinitionChangesContainer(global_container_stack)')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        # Notify the UI in which container to store the machine settings data')
    sigmaSettings.append(r'        container_index = global_container_stack.getContainerIndex(definition_changes_container)')
    sigmaSettings.append(r'        if container_index != self._container_index:')
    sigmaSettings.append(r'            self._container_index = container_index')
    sigmaSettings.append(r'            self.containerIndexChanged.emit()')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    def _createDefinitionChangesContainer(self, global_container_stack, container_index = None):')
    sigmaSettings.append(r'        definition_changes_container = InstanceContainer(global_container_stack.getName() + "_settings")')
    sigmaSettings.append(r'        definition = global_container_stack.getBottom()')
    sigmaSettings.append(r'        definition_changes_container.setDefinition(definition)')
    sigmaSettings.append(r'        definition_changes_container.addMetaDataEntry("type", "definition_changes")')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        self._container_registry.addContainer(definition_changes_container)')
    sigmaSettings.append(r'        # Insert definition_changes between the definition and the variant')
    sigmaSettings.append(r'        global_container_stack.insertContainer(-1, definition_changes_container)')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        return definition_changes_container')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    containerIndexChanged = pyqtSignal()')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    @pyqtProperty(int, notify = containerIndexChanged)')
    sigmaSettings.append(r'    def containerIndex(self):')
    sigmaSettings.append(r'        return self._container_index')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    def _onContainerAdded(self, container):')
    sigmaSettings.append(r'        # Add this action as a supported action to all machine definitions')
    sigmaSettings.append(r'        if isinstance(container, DefinitionContainer) and container.getMetaDataEntry("type") == "machine":')
    sigmaSettings.append(r'            if container.getProperty("machine_extruder_count", "value") > 1:')
    sigmaSettings.append(r'                # Multiextruder printers are not currently supported')
    sigmaSettings.append(r'                Logger.log("d", "Not attaching '+machineSettingsPluginName+r' to %s; Multi-extrusion printers are not supported", container.getId())')
    sigmaSettings.append(r'                return')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'            Application.getInstance().getMachineActionManager().addSupportedAction(container.getId(), self.getKey())')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    @pyqtSlot()')
    sigmaSettings.append(r'    def forceUpdate(self):')
    sigmaSettings.append(r'        # Force rebuilding the build volume by reloading the global container stack.')
    sigmaSettings.append(r'        # This is a bit of a hack, but it seems quick enough.')
    sigmaSettings.append(r'        Application.getInstance().globalContainerStackChanged.emit()')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    @pyqtSlot()')
    sigmaSettings.append(r'    def updateHasMaterialsMetadata(self):')
    sigmaSettings.append(r'        # Updates the has_materials metadata flag after switching gcode flavor')
    sigmaSettings.append(r'        global_container_stack = Application.getInstance().getGlobalContainerStack()')
    sigmaSettings.append(r'        if global_container_stack:')
    sigmaSettings.append(r'            definition = global_container_stack.getBottom()')
    sigmaSettings.append(r'            if definition.getProperty("machine_gcode_flavor", "value") == "UltiGCode" and not definition.getMetaDataEntry("has_materials", False):')
    sigmaSettings.append(r'                has_materials = global_container_stack.getProperty("machine_gcode_flavor", "value") != "UltiGCode"')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                material_container = global_container_stack.findContainer({"type": "material"})')
    sigmaSettings.append(r'                material_index = global_container_stack.getContainerIndex(material_container)')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                if has_materials:')
    sigmaSettings.append(r'                    if "has_materials" in global_container_stack.getMetaData():')
    sigmaSettings.append(r'                        global_container_stack.setMetaDataEntry("has_materials", True)')
    sigmaSettings.append(r'                    else:')
    sigmaSettings.append(r'                        global_container_stack.addMetaDataEntry("has_materials", True)')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                    # Set the material container to a sane default')
    sigmaSettings.append(r'                    if material_container.getId() == "empty_material":')
    sigmaSettings.append(r'                        search_criteria = { "type": "material", "definition": "fdmprinter", "id": "*pla*" }')
    sigmaSettings.append(r'                        containers = self._container_registry.findInstanceContainers(**search_criteria)')
    sigmaSettings.append(r'                        if containers:')
    sigmaSettings.append(r'                            global_container_stack.replaceContainer(material_index, containers[0])')
    sigmaSettings.append(r'                else:')
    sigmaSettings.append(r'                    # The metadata entry is stored in an ini, and ini files are parsed as strings only.')
    sigmaSettings.append(r'                    # Because any non-empty string evaluates to a boolean True, we have to remove the entry to make it False.')
    sigmaSettings.append(r'                    if "has_materials" in global_container_stack.getMetaData():')
    sigmaSettings.append(r'                        global_container_stack.removeMetaDataEntry("has_materials")')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                    empty_material = self._container_registry.findInstanceContainers(id = "empty_material")[0]')
    sigmaSettings.append(r'                    global_container_stack.replaceContainer(material_index, empty_material)')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                Application.getInstance().globalContainerStackChanged.emit()')
    fileContent = '\n'.join(sigmaSettings)
    filesList.append((fileName, fileContent))

    fileName = 'Cura 2/plugins/'+machineSettingsPluginName+'/'+machineSettingsPluginName+'.qml'
    sigmaSettings = []
    sigmaSettings.append(r'import QtQuick 2.2')
    sigmaSettings.append(r'import QtQuick.Controls 1.1')
    sigmaSettings.append(r'import QtQuick.Layouts 1.1')
    sigmaSettings.append(r'import QtQuick.Window 2.1')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'import UM 1.2 as UM')
    sigmaSettings.append(r'import Cura 1.0 as Cura')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'Cura.MachineAction')
    sigmaSettings.append(r'{')
    sigmaSettings.append(r'    anchors.fill: parent;')
    sigmaSettings.append(r'    Item')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        id: bedLevelMachineAction')
    sigmaSettings.append(r'        anchors.fill: parent;')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        UM.I18nCatalog { id: catalog; name: "cura"; }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        Label')
    sigmaSettings.append(r'        {')
    sigmaSettings.append(r'            id: pageTitle')
    sigmaSettings.append(r'            width: parent.width')
    sigmaSettings.append(r'            text: catalog.i18nc("@title", "Sigma Settings")')
    sigmaSettings.append(r'            wrapMode: Text.WordWrap')
    sigmaSettings.append(r'            font.pointSize: 18;')
    sigmaSettings.append(r'        }')
    sigmaSettings.append(r'        Label')
    sigmaSettings.append(r'        {')
    sigmaSettings.append(r'            id: pageDescription')
    sigmaSettings.append(r'            anchors.top: pageTitle.bottom')
    sigmaSettings.append(r'            anchors.topMargin: UM.Theme.getSize("default_margin").height')
    sigmaSettings.append(r'            width: parent.width')
    sigmaSettings.append(r'            wrapMode: Text.WordWrap')
    sigmaSettings.append(r'            visible: "'+cura2Name+r'" in Cura.MachineManager.activeMachineId')
    sigmaSettings.append(r'            text: catalog.i18nc("@label", "Attention! In order to get the best results with your BCN3D Sigma, please make sure the '+cura2PostProcessingPluginName+r' plugin is enabled under Extensions > Post Processing > Modify G-Code.")')
    sigmaSettings.append(r'        }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        Column')
    sigmaSettings.append(r'        {')
    sigmaSettings.append(r'            height: parent.height - y')
    sigmaSettings.append(r'            width: parent.width - UM.Theme.getSize("default_margin").width')
    sigmaSettings.append(r'            spacing: UM.Theme.getSize("default_margin").height')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'            anchors.left: parent.left')
    sigmaSettings.append(r'            anchors.top: pageDescription.bottom')
    sigmaSettings.append(r'            anchors.topMargin: UM.Theme.getSize("default_margin").height')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'            Row')
    sigmaSettings.append(r'            {')
    sigmaSettings.append(r'                width: parent.width')
    sigmaSettings.append(r'                spacing: UM.Theme.getSize("default_margin").height')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                Column')
    sigmaSettings.append(r'                {')
    sigmaSettings.append(r'                    width: parent.width / 2')
    sigmaSettings.append(r'                    spacing: UM.Theme.getSize("default_margin").height')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                    Label')
    sigmaSettings.append(r'                    {')
    sigmaSettings.append(r'                        text: catalog.i18nc("@label", "Printer Settings")')
    sigmaSettings.append(r'                        font.bold: true')
    sigmaSettings.append(r'                    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                    Grid')
    sigmaSettings.append(r'                    {')
    sigmaSettings.append(r'                        columns: 3')
    sigmaSettings.append(r'                        columnSpacing: UM.Theme.getSize("default_margin").width')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "X (Width)")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        TextField')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            id: buildAreaWidthField')
    sigmaSettings.append(r'                            text: machineWidthProvider.properties.value')
    sigmaSettings.append(r'                            validator: RegExpValidator { regExp: /[0-9\.]{0,6}/ }')
    sigmaSettings.append(r'                            onEditingFinished: { machineWidthProvider.setPropertyValue("value", text); manager.forceUpdate() }')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "mm")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "Y (Depth)")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        TextField')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            id: buildAreaDepthField')
    sigmaSettings.append(r'                            text: machineDepthProvider.properties.value')
    sigmaSettings.append(r'                            validator: RegExpValidator { regExp: /[0-9\.]{0,6}/ }')
    sigmaSettings.append(r'                            onEditingFinished: { machineDepthProvider.setPropertyValue("value", text); manager.forceUpdate() }')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "mm")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "Z (Height)")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        TextField')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            id: buildAreaHeightField')
    sigmaSettings.append(r'                            text: machineHeightProvider.properties.value')
    sigmaSettings.append(r'                            validator: RegExpValidator { regExp: /[0-9\.]{0,6}/ }')
    sigmaSettings.append(r'                            onEditingFinished: { machineHeightProvider.setPropertyValue("value", text); manager.forceUpdate() }')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "mm")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                    Column')
    sigmaSettings.append(r'                    {')
    sigmaSettings.append(r'                        CheckBox')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            id: printOneAtATimeCheckBox')
    sigmaSettings.append(r'                            text: catalog.i18nc("@option:check", "Enable setting: Print Sequence")')
    sigmaSettings.append( "                            checked: String(machinePrintOneAtATimeProvider.properties.enabled).toLowerCase() != 'false'"+'\n')
    sigmaSettings.append(r'                            onClicked: machinePrintOneAtATimeProvider.setPropertyValue("enabled", checked)')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                    }')
    sigmaSettings.append(r'                }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                Column')
    sigmaSettings.append(r'                {')
    sigmaSettings.append(r'                    width: parent.width / 2')
    sigmaSettings.append(r'                    spacing: UM.Theme.getSize("default_margin").height')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                    Label')
    sigmaSettings.append(r'                    {')
    sigmaSettings.append(r'                        text: catalog.i18nc("@label", "Printhead Settings")')
    sigmaSettings.append(r'                        font.bold: true')
    sigmaSettings.append(r'                    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                    Grid')
    sigmaSettings.append(r'                    {')
    sigmaSettings.append(r'                        columns: 3')
    sigmaSettings.append(r'                        columnSpacing: UM.Theme.getSize("default_margin").width')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "X min")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        TextField')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            id: printheadXMinField')
    sigmaSettings.append(r'                            text: getHeadPolygonCoord("x", "min")')
    sigmaSettings.append(r'                            validator: RegExpValidator { regExp: /[0-9\.]{0,6}/ }')
    sigmaSettings.append(r'                            onEditingFinished: setHeadPolygon()')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "mm")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "Y min")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        TextField')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            id: printheadYMinField')
    sigmaSettings.append(r'                            text: getHeadPolygonCoord("y", "min")')
    sigmaSettings.append(r'                            validator: RegExpValidator { regExp: /[0-9\.]{0,6}/ }')
    sigmaSettings.append(r'                            onEditingFinished: setHeadPolygon()')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "mm")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "X max")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        TextField')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            id: printheadXMaxField')
    sigmaSettings.append(r'                            text: getHeadPolygonCoord("x", "max")')
    sigmaSettings.append(r'                            validator: RegExpValidator { regExp: /[0-9\.]{0,6}/ }')
    sigmaSettings.append(r'                            onEditingFinished: setHeadPolygon()')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "mm")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "Y max")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        TextField')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            id: printheadYMaxField')
    sigmaSettings.append(r'                            text: getHeadPolygonCoord("y", "max")')
    sigmaSettings.append(r'                            validator: RegExpValidator { regExp: /[0-9\.]{0,6}/ }')
    sigmaSettings.append(r'                            onEditingFinished: setHeadPolygon()')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "mm")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                        Item { width: UM.Theme.getSize("default_margin").width; height: UM.Theme.getSize("default_margin").height }')
    sigmaSettings.append(r'                        Item { width: UM.Theme.getSize("default_margin").width; height: UM.Theme.getSize("default_margin").height }')
    sigmaSettings.append(r'                        Item { width: UM.Theme.getSize("default_margin").width; height: UM.Theme.getSize("default_margin").height }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "Gantry height")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        TextField')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            id: gantryHeightField')
    sigmaSettings.append(r'                            text: gantryHeightProvider.properties.value')
    sigmaSettings.append(r'                            validator: RegExpValidator { regExp: /[0-9\.]{0,6}/ }')
    sigmaSettings.append(r'                            onEditingFinished: { gantryHeightProvider.setPropertyValue("value", text) }')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                        Label')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            text: catalog.i18nc("@label", "mm")')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'                        Item { width: UM.Theme.getSize("default_margin").width; height: UM.Theme.getSize("default_margin").height }')
    sigmaSettings.append(r'                        Item { width: UM.Theme.getSize("default_margin").width; height: UM.Theme.getSize("default_margin").height }')
    sigmaSettings.append(r'                        Item { width: UM.Theme.getSize("default_margin").width; height: UM.Theme.getSize("default_margin").height }')
    sigmaSettings.append(r'                    }')
    sigmaSettings.append(r'                }')
    sigmaSettings.append(r'            }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'            Row')
    sigmaSettings.append(r'            {')
    sigmaSettings.append(r'                spacing: UM.Theme.getSize("default_margin").width')
    sigmaSettings.append(r'                anchors.left: parent.left')
    sigmaSettings.append(r'                anchors.right: parent.right')
    sigmaSettings.append(r'                height: parent.height - y')
    sigmaSettings.append(r'                Column')
    sigmaSettings.append(r'                {')
    sigmaSettings.append(r'                    height: parent.height')
    sigmaSettings.append(r'                    width: parent.width / 2')
    sigmaSettings.append(r'                    Label')
    sigmaSettings.append(r'                    {')
    sigmaSettings.append(r'                        text: catalog.i18nc("@label", "Start Gcode")')
    sigmaSettings.append(r'                    }')
    sigmaSettings.append(r'                    TextArea')
    sigmaSettings.append(r'                    {')
    sigmaSettings.append(r'                        id: machineStartGcodeField')
    sigmaSettings.append(r'                        width: parent.width')
    sigmaSettings.append(r'                        height: parent.height - y')
    sigmaSettings.append(r'                        font: UM.Theme.getFont("fixed")')
    sigmaSettings.append(r'                        wrapMode: TextEdit.NoWrap')
    sigmaSettings.append(r'                        text: machineStartGcodeProvider.properties.value')
    sigmaSettings.append(r'                        onActiveFocusChanged:')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            if(!activeFocus)')
    sigmaSettings.append(r'                            {')
    sigmaSettings.append(r'                                machineStartGcodeProvider.setPropertyValue("value", machineStartGcodeField.text)')
    sigmaSettings.append(r'                            }')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                    }')
    sigmaSettings.append(r'                }')
    sigmaSettings.append(r'                Column {')
    sigmaSettings.append(r'                    height: parent.height')
    sigmaSettings.append(r'                    width: parent.width / 2')
    sigmaSettings.append(r'                    Label')
    sigmaSettings.append(r'                    {')
    sigmaSettings.append(r'                        text: catalog.i18nc("@label", "End Gcode")')
    sigmaSettings.append(r'                    }')
    sigmaSettings.append(r'                    TextArea')
    sigmaSettings.append(r'                    {')
    sigmaSettings.append(r'                        id: machineEndGcodeField')
    sigmaSettings.append(r'                        width: parent.width')
    sigmaSettings.append(r'                        height: parent.height - y')
    sigmaSettings.append(r'                        font: UM.Theme.getFont("fixed")')
    sigmaSettings.append(r'                        wrapMode: TextEdit.NoWrap')
    sigmaSettings.append(r'                        text: machineEndGcodeProvider.properties.value')
    sigmaSettings.append(r'                        onActiveFocusChanged:')
    sigmaSettings.append(r'                        {')
    sigmaSettings.append(r'                            if(!activeFocus)')
    sigmaSettings.append(r'                            {')
    sigmaSettings.append(r'                                machineEndGcodeProvider.setPropertyValue("value", machineEndGcodeField.text)')
    sigmaSettings.append(r'                            }')
    sigmaSettings.append(r'                        }')
    sigmaSettings.append(r'                    }')
    sigmaSettings.append(r'                }')
    sigmaSettings.append(r'            }')
    sigmaSettings.append(r'        }')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    function getHeadPolygonCoord(axis, minMax)')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        var polygon = JSON.parse(machineHeadPolygonProvider.properties.value);')
    sigmaSettings.append(r'        var item = (axis == "x") ? 0 : 1')
    sigmaSettings.append(r'        var result = polygon[0][item];')
    sigmaSettings.append(r'        for(var i = 1; i < polygon.length; i++) {')
    sigmaSettings.append(r'            if (minMax == "min") {')
    sigmaSettings.append(r'                result = Math.min(result, polygon[i][item]);')
    sigmaSettings.append(r'            } else {')
    sigmaSettings.append(r'                result = Math.max(result, polygon[i][item]);')
    sigmaSettings.append(r'            }')
    sigmaSettings.append(r'        }')
    sigmaSettings.append(r'        return Math.abs(result);')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    function setHeadPolygon()')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        var polygon = [];')
    sigmaSettings.append(r'        polygon.push([-parseFloat(printheadXMinField.text), parseFloat(printheadYMaxField.text)]);')
    sigmaSettings.append(r'        polygon.push([-parseFloat(printheadXMinField.text),-parseFloat(printheadYMinField.text)]);')
    sigmaSettings.append(r'        polygon.push([ parseFloat(printheadXMaxField.text), parseFloat(printheadYMaxField.text)]);')
    sigmaSettings.append(r'        polygon.push([ parseFloat(printheadXMaxField.text),-parseFloat(printheadYMinField.text)]);')
    sigmaSettings.append(r'        machineHeadPolygonProvider.setPropertyValue("value", JSON.stringify(polygon));')
    sigmaSettings.append(r'        manager.forceUpdate();')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    UM.SettingPropertyProvider')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        id: machineWidthProvider')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        containerStackId: Cura.MachineManager.activeMachineId')
    sigmaSettings.append(r'        key: "machine_width"')
    sigmaSettings.append(r'        watchedProperties: [ "value" ]')
    sigmaSettings.append(r'        storeIndex: manager.containerIndex')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    UM.SettingPropertyProvider')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        id: machineDepthProvider')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        containerStackId: Cura.MachineManager.activeMachineId')
    sigmaSettings.append(r'        key: "machine_depth"')
    sigmaSettings.append(r'        watchedProperties: [ "value" ]')
    sigmaSettings.append(r'        storeIndex: manager.containerIndex')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    UM.SettingPropertyProvider')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        id: machineHeightProvider')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        containerStackId: Cura.MachineManager.activeMachineId')
    sigmaSettings.append(r'        key: "machine_height"')
    sigmaSettings.append(r'        watchedProperties: [ "value" ]')
    sigmaSettings.append(r'        storeIndex: manager.containerIndex')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    UM.SettingPropertyProvider')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        id: machinePrintOneAtATimeProvider')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        containerStackId: Cura.MachineManager.activeMachineId')
    sigmaSettings.append(r'        key: "print_sequence"')
    sigmaSettings.append(r'        watchedProperties: [ "enabled" ]')
    sigmaSettings.append(r'        storeIndex: manager.containerIndex')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    UM.SettingPropertyProvider')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        id: gantryHeightProvider')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        containerStackId: Cura.MachineManager.activeMachineId')
    sigmaSettings.append(r'        key: "gantry_height"')
    sigmaSettings.append(r'        watchedProperties: [ "value" ]')
    sigmaSettings.append(r'        storeIndex: manager.containerIndex')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    UM.SettingPropertyProvider')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        id: machineHeadPolygonProvider')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        containerStackId: Cura.MachineManager.activeMachineId')
    sigmaSettings.append(r'        key: "machine_head_with_fans_polygon"')
    sigmaSettings.append(r'        watchedProperties: [ "value" ]')
    sigmaSettings.append(r'        storeIndex: manager.containerIndex')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    UM.SettingPropertyProvider')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        id: machineStartGcodeProvider')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        containerStackId: Cura.MachineManager.activeMachineId')
    sigmaSettings.append(r'        key: "machine_start_gcode"')
    sigmaSettings.append(r'        watchedProperties: [ "value" ]')
    sigmaSettings.append(r'        storeIndex: manager.containerIndex')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'    UM.SettingPropertyProvider')
    sigmaSettings.append(r'    {')
    sigmaSettings.append(r'        id: machineEndGcodeProvider')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'        containerStackId: Cura.MachineManager.activeMachineId')
    sigmaSettings.append(r'        key: "machine_end_gcode"')
    sigmaSettings.append(r'        watchedProperties: [ "value" ]')
    sigmaSettings.append(r'        storeIndex: manager.containerIndex')
    sigmaSettings.append(r'    }')
    sigmaSettings.append(r'')
    sigmaSettings.append(r'}')
    fileContent = '\n'.join(sigmaSettings)
    filesList.append((fileName, fileContent))

    return filesList

def engineDataDecoder(engineData):
    global profilesData
    profilesData = engineData[0]
    global SigmaProgenVersion
    SigmaProgenVersion = engineData[1]

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
    coastVolume = float("%.2f" % ((hotend['nozzleSize'])**3*filament['purgeLength']/16))
    return coastVolume

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

def timeVsTemperature(element, value, action, command):

    if element['id'] != 'bed':
        hotendParameter1 = element['timeToHeatUp150To300'] * 2.05
        hotendParameter1c = element['timeToCoolDown300To150'] * 1.16
    hotendParameter2 = 575 
    hotendParameter2c = 325
    hotendParameter3 = 25
    hotendParameter3c = hotendParameter3

    bedParameterA1 = 51
    bedParameterA2 = 61
    bedParameterA3 = 19
    bedParameterB1 = 1000
    bedParameterB2 = 90
    bedParameterB3 = 47
    bedParameterB4 = 10

    # return needed time (sec) to reach Temperature (ºC)
    if command == 'getTime':
        if type(value) == str:
            if action == 'heating':
                time = '(' + str(hotendParameter1) + '*math.log(-' + str(hotendParameter2-hotendParameter3) + '/('+ value +'-' + str(float(hotendParameter2)) + ')))'
            elif action == 'cooling':
                time = '(-' + str(hotendParameter1c) + '*math.log(('+ value +'-' + str(float(hotendParameter3c))+')/(' + str(float(hotendParameter2c-hotendParameter3c)) + ')))'
        else:
            temperature = value
            if action == 'heating':
                if element['id'] == 'bed':
                    if temperature <= 60:
                        time = bedParameterA1 * math.log(-(bedParameterA2-bedParameterA3)/(float(temperature)-bedParameterA2))
                    else:
                        time = bedParameterB1 * math.log(-bedParameterB2/(float(temperature)-bedParameterB2-bedParameterB3))+bedParameterB4
                else:
                    time = hotendParameter1 * math.log(-(hotendParameter2-hotendParameter3)/(float(temperature)-hotendParameter2))
            elif action == 'cooling':
                if element['id'] == 'bed':
                    time = 0
                else:
                    time = - hotendParameter1c * math.log((float(temperature)-hotendParameter3c)/(hotendParameter2c-hotendParameter3c))
        return max(0, time)

    # return temperature (ºC) reached after heating during given time (sec)
    elif command == 'getTemperature':
        time = value
        if action == 'heating':
            if element['id'] == 'bed':
                if time <= 180:
                    temperature = bedParameterA2 - (bedParameterA2 - bedParameterA3) * math.exp(-time/bedParameterA1)
                else:
                    temperature = bedParameterB2 + bedParameterB3 - bedParameterB2 * math.exp(-(time - bedParameterB4)/bedParameterB1)
            else:
                temperature = hotendParameter2 - (hotendParameter2 - hotendParameter3) * math.exp(-time/hotendParameter1)
        elif action == 'cooling':
            if element['id'] == 'bed':
                temperature = 0
            else:
                temperature = hotendParameter2c + (hotendParameter2c - hotendParameter3c) * math.exp(-time/hotendParameter1c)
        return max(0, temperature)

def firstHeatSequence(hotendLeft, hotendRight, leftHotendTemp, rightHotendTemp, bedTemp, software):
    startSequenceString = '; Start Heating Sequence. If you changed temperatures manually all elements may not heat in sync,'
    bed = dict([('id', 'bed')])
    if software == 'Simplify3D':
        if hotendLeft['id'] != 'None':
            timeLeftHotend  = (timeVsTemperature(hotendLeft, leftHotendTemp,  'heating', 'getTime'), '', hotendLeft, 'M104 ', 'M109 ', 'S[extruder0_temperature]', ' T0,')
        if hotendRight['id'] != 'None':
            timeRightHotend = (timeVsTemperature(hotendRight, rightHotendTemp, 'heating', 'getTime'), '', hotendRight, 'M104 ', 'M109 ', 'S[extruder1_temperature]', ' T1,')
        timeBed         = (timeVsTemperature(bed, bedTemp, 'heating', 'getTime'), '', bed, 'M140 ', 'M190 ', 'S[bed0_temperature]',       ',')
    elif software == 'Cura':
        startSequenceString = '\t;' + startSequenceString[2:-1] + '\n'
        if hotendLeft['id'] != 'None':
            timeLeftHotend  = (timeVsTemperature(hotendLeft, leftHotendTemp,  'heating', 'getTime'), '\t', hotendLeft, 'M104 ', 'M109 ', 'S{print_temperature}',     ' T0\n')
        if hotendRight['id'] != 'None':
            timeRightHotend = (timeVsTemperature(hotendRight, rightHotendTemp, 'heating', 'getTime'), '\t', hotendRight, 'M104 ', 'M109 ', 'S{print_temperature2}',    ' T1\n')
        timeBed         = (timeVsTemperature(bed, bedTemp, 'heating', 'getTime'), '\t', bed, 'M140 ', 'M190 ', 'S{print_bed_temperature}', '\n')
    elif software == 'Cura2':
        # Using Cura 2.5.0 the only labels we know to point to extruder being used are:
        #   adhesion_extruder_nr
        #   support_infill_extruder_nr
        #   support_extruder_nr
        #   support_interface_extruder_nr
        startSequenceString = r'\n;' + startSequenceString[2:-1] + r'\n'
        if hotendLeft['id'] != 'None':
            timeLeftHotend  = (timeVsTemperature(hotendLeft, leftHotendTemp, 'heating', 'getTime'), '', hotendLeft, 'M104 ', 'M109 ', 'S{material_print_temperature_layer_0}',     r' T0\n')
        if hotendRight['id'] != 'None':
            timeRightHotend = (timeVsTemperature(hotendRight, rightHotendTemp, 'heating', 'getTime'), '', hotendRight, 'M104 ', 'M109 ', 'S{material_print_temperature_layer_0}',    r' T1\n')
        timeBed         = (timeVsTemperature(bed, bedTemp, 'heating', 'getTime'), '', bed, 'M140 ', 'M190 ', 'S{material_bed_temperature}', r'\n')

    if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':
        # IDEX
        startTimes = sorted([timeLeftHotend, timeRightHotend, timeBed])
        startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-2][0], 'heating', 'getTemperature')))+startTimes[-1][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-3][0], 'heating', 'getTemperature')))+startTimes[-1][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-3][-4]+startTimes[-3][-2]+startTimes[-3][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
        startSequenceString += startTimes[-1][-6]+startTimes[-3][-3]+startTimes[-3][-2]+startTimes[-3][-1]
    else:
        if hotendRight['id'] == 'None':
            # MEX Left
            startTimes = sorted([timeLeftHotend, timeBed])
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-2][0], 'heating', 'getTemperature')))+startTimes[-1][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
        else:
            # MEX Right
            startTimes = sorted([timeRightHotend, timeBed])
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+'S'+str(int(timeVsTemperature(startTimes[-1][-5], startTimes[-1][0]-startTimes[-2][0], 'heating', 'getTemperature')))+startTimes[-1][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-4]+startTimes[-2][-2]+startTimes[-2][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-1][-3]+startTimes[-1][-2]+startTimes[-1][-1]
            startSequenceString += startTimes[-1][-6]+startTimes[-2][-3]+startTimes[-2][-2]+startTimes[-2][-1]
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