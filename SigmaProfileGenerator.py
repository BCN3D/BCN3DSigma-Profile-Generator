#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - October 2016
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0
# version 1.0.0

import time, math, os, platform, sys, json, string, shutil, zipfile

def createSimplify3DProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, dataLog, createFile):
    fff = []
    fff.append(r'<?xml version="1.0" encoding="utf-8"?>'+"\n")
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
    fff.append(r'<profile name="'+fileName+r'" version="'+time.strftime("%Y-%m-%d")+" "+time.strftime("%H:%M:%S")+r'" app="S3D-Software 3.1.1">'+"\n")
    fff.append(r'  <baseProfile></baseProfile>'+"\n")
    fff.append(r'  <printMaterial></printMaterial>'+"\n")
    fff.append(r'  <printQuality>'+defaultPrintQuality+'</printQuality>'+"\n") #+extruder+secondaryExtruderAction+str(quality['id'])+
    if hotendLeft['id'] != 'None':
        fff.append(r'  <printExtruders>Left Extruder Only</printExtruders>'+"\n")
    else:
        fff.append(r'  <printExtruders>Right Extruder Only</printExtruders>'+"\n")        
    if hotendLeft['id'] != 'None':
        fff.append(r'  <extruder name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">'+"\n")
        fff.append(r'    <toolheadNumber>0</toolheadNumber>'+"\n")
        fff.append(r'    <diameter>'+str(hotendLeft['nozzleSize'])+r'</diameter>'+"\n")
        fff.append(r'    <autoWidth>0</autoWidth>'+"\n")
        fff.append(r'    <width>'+str(hotendLeft['nozzleSize'])+r'</width>'+"\n")
        fff.append(r'    <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+r'</extrusionMultiplier>'+"\n")
        fff.append(r'    <useRetract>1</useRetract>'+"\n")
        fff.append(r'    <retractionDistance>'+str(filamentLeft['retractionDistance'])+r'</retractionDistance>'+"\n")
        fff.append(r'    <extraRestartDistance>0</extraRestartDistance>'+"\n")
        fff.append(r'    <retractionZLift>0.05</retractionZLift>'+"\n")
        fff.append(r'    <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+r'</retractionSpeed>'+"\n")
        fff.append(r'    <useCoasting>0</useCoasting>'+"\n")
        fff.append(r'    <coastingDistance>0.2</coastingDistance>'+"\n")
        fff.append(r'    <useWipe>0</useWipe>'+"\n")
        fff.append(r'    <wipeDistance>5</wipeDistance>'+"\n")
        fff.append(r'  </extruder>'+"\n")
    else:
        fff.append(r'  <extruder name="">'+"\n")
        fff.append(r'    <toolheadNumber>0</toolheadNumber>'+"\n")
        fff.append(r'    <diameter>0</diameter>'+"\n")
        fff.append(r'    <autoWidth>0</autoWidth>'+"\n")
        fff.append(r'    <width>0</width>'+"\n")
        fff.append(r'    <extrusionMultiplier>0</extrusionMultiplier>'+"\n")
        fff.append(r'    <useRetract>0</useRetract>'+"\n")
        fff.append(r'    <retractionDistance>0</retractionDistance>'+"\n")
        fff.append(r'    <extraRestartDistance>0</extraRestartDistance>'+"\n")
        fff.append(r'    <retractionZLift>0</retractionZLift>'+"\n")
        fff.append(r'    <retractionSpeed>0</retractionSpeed>'+"\n")
        fff.append(r'    <useCoasting>0</useCoasting>'+"\n")
        fff.append(r'    <coastingDistance>0</coastingDistance>'+"\n")
        fff.append(r'    <useWipe>0</useWipe>'+"\n")
        fff.append(r'    <wipeDistance>0</wipeDistance>'+"\n")
        fff.append(r'  </extruder>'+"\n")
    if hotendRight['id'] != 'None':
        fff.append(r'  <extruder name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">'+"\n")
        fff.append(r'    <toolheadNumber>1</toolheadNumber>'+"\n")
        fff.append(r'    <diameter>'+str(hotendRight['nozzleSize'])+r'</diameter>'+"\n")
        fff.append(r'    <autoWidth>0</autoWidth>'+"\n")
        fff.append(r'    <width>'+str(hotendRight['nozzleSize'])+r'</width>'+"\n")
        fff.append(r'    <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+r'</extrusionMultiplier>'+"\n")
        fff.append(r'    <useRetract>1</useRetract>'+"\n")
        fff.append(r'    <retractionDistance>'+str(filamentRight['retractionDistance'])+r'</retractionDistance>'+"\n")
        fff.append(r'    <extraRestartDistance>0</extraRestartDistance>'+"\n")
        fff.append(r'    <retractionZLift>0.05</retractionZLift>'+"\n")
        fff.append(r'    <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+r'</retractionSpeed>'+"\n")
        fff.append(r'    <useCoasting>0</useCoasting>'+"\n")
        fff.append(r'    <coastingDistance>0.2</coastingDistance>'+"\n")
        fff.append(r'    <useWipe>0</useWipe>'+"\n")
        fff.append(r'    <wipeDistance>5</wipeDistance>'+"\n")
        fff.append(r'  </extruder>'+"\n")
    fff.append(r'  <primaryExtruder>0</primaryExtruder>'+"\n")
    fff.append(r'  <layerHeight>0.2</layerHeight>'+"\n")
    fff.append(r'  <topSolidLayers>4</topSolidLayers>'+"\n")
    fff.append(r'  <bottomSolidLayers>4</bottomSolidLayers>'+"\n")
    fff.append(r'  <perimeterOutlines>3</perimeterOutlines>'+"\n")
    fff.append(r'  <printPerimetersInsideOut>1</printPerimetersInsideOut>'+"\n")
    fff.append(r'  <startPointOption>3</startPointOption>'+"\n")
    fff.append(r'  <startPointOriginX>105</startPointOriginX>'+"\n")
    fff.append(r'  <startPointOriginY>300</startPointOriginY>'+"\n")
    fff.append(r'  <startPointOriginZ>300</startPointOriginZ>'+"\n")
    fff.append(r'  <sequentialIslands>0</sequentialIslands>'+"\n")
    fff.append(r'  <spiralVaseMode>0</spiralVaseMode>'+"\n")
    fff.append(r'  <firstLayerHeightPercentage>125</firstLayerHeightPercentage>'+"\n")
    fff.append(r'  <firstLayerWidthPercentage>100</firstLayerWidthPercentage>'+"\n")
    fff.append(r'  <firstLayerUnderspeed>0.85</firstLayerUnderspeed>'+"\n")
    fff.append(r'  <useRaft>0</useRaft>'+"\n")
    fff.append(r'  <raftExtruder>0</raftExtruder>'+"\n")
    fff.append(r'  <raftLayers>2</raftLayers>'+"\n")
    fff.append(r'  <raftOffset>3</raftOffset>'+"\n")
    fff.append(r'  <raftSeparationDistance>0.1</raftSeparationDistance>'+"\n")
    fff.append(r'  <raftInfill>85</raftInfill>'+"\n")
    fff.append(r'  <disableRaftBaseLayers>0</disableRaftBaseLayers>'+"\n")
    fff.append(r'  <useSkirt>1</useSkirt>'+"\n")
    fff.append(r'  <skirtExtruder>999</skirtExtruder>'+"\n")
    fff.append(r'  <skirtLayers>1</skirtLayers>'+"\n")
    fff.append(r'  <skirtOutlines>2</skirtOutlines>'+"\n")
    fff.append(r'  <skirtOffset>4</skirtOffset>'+"\n")
    fff.append(r'  <usePrimePillar>0</usePrimePillar>'+"\n")
    fff.append(r'  <primePillarExtruder>999</primePillarExtruder>'+"\n")
    fff.append(r'  <primePillarWidth>15</primePillarWidth>'+"\n")
    fff.append(r'  <primePillarLocation>7</primePillarLocation>'+"\n")
    fff.append(r'  <primePillarSpeedMultiplier>1</primePillarSpeedMultiplier>'+"\n")
    fff.append(r'  <useOozeShield>0</useOozeShield>'+"\n")
    fff.append(r'  <oozeShieldExtruder>999</oozeShieldExtruder>'+"\n")
    fff.append(r'  <oozeShieldOffset>2</oozeShieldOffset>'+"\n")
    fff.append(r'  <oozeShieldOutlines>1</oozeShieldOutlines>'+"\n")
    fff.append(r'  <oozeShieldSidewallShape>1</oozeShieldSidewallShape>'+"\n")
    fff.append(r'  <oozeShieldSidewallAngle>30</oozeShieldSidewallAngle>'+"\n")
    fff.append(r'  <oozeShieldSpeedMultiplier>1</oozeShieldSpeedMultiplier>'+"\n")
    fff.append(r'  <infillExtruder>1</infillExtruder>'+"\n")
    fff.append(r'  <internalInfillPattern>Grid</internalInfillPattern>'+"\n")
    fff.append(r'  <externalInfillPattern>Rectilinear</externalInfillPattern>'+"\n")
    fff.append(r'  <infillPercentage>20</infillPercentage>'+"\n")
    fff.append(r'  <outlineOverlapPercentage>25</outlineOverlapPercentage>'+"\n")
    fff.append(r'  <infillExtrusionWidthPercentage>100</infillExtrusionWidthPercentage>'+"\n")
    fff.append(r'  <minInfillLength>3</minInfillLength>'+"\n")
    fff.append(r'  <infillLayerInterval>1</infillLayerInterval>'+"\n")
    fff.append(r'  <infillAngles>45,-45</infillAngles>'+"\n")
    fff.append(r'  <overlapInfillAngles>1</overlapInfillAngles>'+"\n")
    fff.append(r'  <generateSupport>0</generateSupport>'+"\n")
    fff.append(r'  <supportExtruder>0</supportExtruder>'+"\n")
    fff.append(r'  <supportInfillPercentage>25</supportInfillPercentage>'+"\n")
    fff.append(r'  <supportExtraInflation>1</supportExtraInflation>'+"\n")
    fff.append(r'  <denseSupportLayers>5</denseSupportLayers>'+"\n")
    fff.append(r'  <denseSupportInfillPercentage>75</denseSupportInfillPercentage>'+"\n")
    fff.append(r'  <supportLayerInterval>1</supportLayerInterval>'+"\n")

    fff.append(r'  <supportHorizontalPartOffset>0.7</supportHorizontalPartOffset>'+"\n")
    fff.append(r'  <supportUpperSeparationLayers>1</supportUpperSeparationLayers>'+"\n")
    fff.append(r'  <supportLowerSeparationLayers>1</supportLowerSeparationLayers>'+"\n")

    fff.append(r'  <supportType>0</supportType>'+"\n")
    fff.append(r'  <supportGridSpacing>1</supportGridSpacing>'+"\n")
    fff.append(r'  <maxOverhangAngle>60</maxOverhangAngle>'+"\n")
    fff.append(r'  <supportAngles>90</supportAngles>'+"\n")
    if hotendLeft['id'] != 'None':
        fff.append(r'  <temperatureController name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">'+"\n")
        fff.append(r'    <temperatureNumber>0</temperatureNumber>'+"\n")
        fff.append(r'    <isHeatedBed>0</isHeatedBed>'+"\n")
        fff.append(r'    <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
        fff.append(r'    <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
        fff.append(r'    <stabilizeAtStartup>0</stabilizeAtStartup>'+"\n")
        fff.append(r'    <setpoint layer="1" temperature="150"/>'+"\n")
        fff.append(r'  </temperatureController>'+"\n")
    if hotendRight['id'] != 'None':
        fff.append(r'  <temperatureController name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">'+"\n")
        fff.append(r'    <temperatureNumber>1</temperatureNumber>'+"\n")
        fff.append(r'    <isHeatedBed>0</isHeatedBed>'+"\n")
        fff.append(r'    <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
        fff.append(r'    <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
        fff.append(r'    <stabilizeAtStartup>0</stabilizeAtStartup>'+"\n")
        fff.append(r'    <setpoint layer="1" temperature="150"/>'+"\n")
        fff.append(r'  </temperatureController>'+"\n")
    if (hotendLeft['id'] != 'None' and filamentLeft['bedTemperature'] > 0) or (hotendRight['id'] != 'None' and filamentRight['bedTemperature'] > 0):
        fff.append(r'  <temperatureController name="Heated Bed">'+"\n")
        fff.append(r'    <temperatureNumber>0</temperatureNumber>'+"\n")
        fff.append(r'    <isHeatedBed>1</isHeatedBed>'+"\n")
        fff.append(r'    <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
        fff.append(r'    <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
        fff.append(r'    <stabilizeAtStartup>0</stabilizeAtStartup>'+"\n")
        fff.append(r'    <setpoint layer="1" temperature="50"/>'+"\n")
        fff.append(r'  </temperatureController>'+"\n")
    fff.append(r'  <fanSpeed>'+"\n")
    fff.append(r'    <setpoint layer="1" speed="0" />'+"\n")
    fff.append(r'    <setpoint layer="2" speed="100"/>'+"\n")
    fff.append(r'  </fanSpeed>'+"\n")
    fff.append(r'  <blipFanToFullPower>0</blipFanToFullPower>'+"\n")
    fff.append(r'  <adjustSpeedForCooling>1</adjustSpeedForCooling>'+"\n")
    fff.append(r'  <minSpeedLayerTime>5</minSpeedLayerTime>'+"\n")
    fff.append(r'  <minCoolingSpeedSlowdown>75</minCoolingSpeedSlowdown>'+"\n")
    fff.append(r'  <increaseFanForCooling>1</increaseFanForCooling>'+"\n")
    fff.append(r'  <minFanLayerTime>5</minFanLayerTime>'+"\n")
    fff.append(r'  <maxCoolingFanSpeed>100</maxCoolingFanSpeed>'+"\n")
    fff.append(r'  <increaseFanForBridging>1</increaseFanForBridging>'+"\n")
    fff.append(r'  <bridgingFanSpeed>100</bridgingFanSpeed>'+"\n")
    fff.append(r'  <use5D>1</use5D>'+"\n")
    fff.append(r'  <relativeEdistances>0</relativeEdistances>'+"\n")
    fff.append(r'  <allowEaxisZeroing>1</allowEaxisZeroing>'+"\n")
    fff.append(r'  <independentExtruderAxes>0</independentExtruderAxes>'+"\n")
    fff.append(r'  <includeM10123>0</includeM10123>'+"\n")
    fff.append(r'  <stickySupport>1</stickySupport>'+"\n")
    fff.append(r'  <applyToolheadOffsets>0</applyToolheadOffsets>'+"\n")
    fff.append(r'  <gcodeXoffset>0</gcodeXoffset>'+"\n")
    fff.append(r'  <gcodeYoffset>0</gcodeYoffset>'+"\n")
    fff.append(r'  <gcodeZoffset>0</gcodeZoffset>'+"\n")
    fff.append(r'  <overrideMachineDefinition>1</overrideMachineDefinition>'+"\n")
    fff.append(r'  <machineTypeOverride>0</machineTypeOverride>'+"\n")
    fff.append(r'  <strokeXoverride>210</strokeXoverride>'+"\n")
    fff.append(r'  <strokeYoverride>297</strokeYoverride>'+"\n")
    fff.append(r'  <strokeZoverride>210</strokeZoverride>'+"\n")
    fff.append(r'  <originOffsetXoverride>0</originOffsetXoverride>'+"\n")
    fff.append(r'  <originOffsetYoverride>0</originOffsetYoverride>'+"\n")
    fff.append(r'  <originOffsetZoverride>0</originOffsetZoverride>'+"\n")
    fff.append(r'  <homeXdirOverride>-1</homeXdirOverride>'+"\n")
    fff.append(r'  <homeYdirOverride>-1</homeYdirOverride>'+"\n")
    fff.append(r'  <homeZdirOverride>-1</homeZdirOverride>'+"\n")
    fff.append(r'  <flipXoverride>1</flipXoverride>'+"\n")
    fff.append(r'  <flipYoverride>-1</flipYoverride>'+"\n")
    fff.append(r'  <flipZoverride>1</flipZoverride>'+"\n")
    fff.append(r'  <toolheadOffsets>0,0|0,0|0,0|0,0|0,0|0,0</toolheadOffsets>'+"\n")
    fff.append(r'  <overrideFirmwareConfiguration>1</overrideFirmwareConfiguration>'+"\n")
    fff.append(r'  <firmwareTypeOverride>RepRap (Marlin/Repetier/Sprinter)</firmwareTypeOverride>'+"\n")
    fff.append(r'  <GPXconfigOverride>r2</GPXconfigOverride>'+"\n")
    fff.append(r'  <baudRateOverride>250000</baudRateOverride>'+"\n")
    fff.append(r'  <overridePrinterModels>0</overridePrinterModels>'+"\n")
    fff.append(r'  <printerModelsOverride></printerModelsOverride>'+"\n")
    fff.append(r'  <startingGcode></startingGcode>'+"\n")
    fff.append(r'  <layerChangeGcode></layerChangeGcode>'+"\n")
    fff.append(r'  <retractionGcode></retractionGcode>'+"\n")
    fff.append(r'  <toolChangeGcode></toolChangeGcode>'+"\n")
    fff.append(r'  <endingGcode>M104 S0 T0,M104 S0 T1,M140 S0'+"\t\t"+r';heated bed heater off,G91'+"\t\t"+r';relative positioning,G1 Z+0.5 E-5 Y+10 F[travel_speed]'+"\t"+r';move Z up a bit and retract filament even more,G28 X0 Y0'+"\t\t"+r';move X/Y to min endstops so the head is out of the way,M84'+"\t\t"+r';steppers off,G90'+"\t\t"+r';absolute positioning,</endingGcode>'+"\n")
    fff.append(r'  <exportFileFormat>gcode</exportFileFormat>'+"\n")
    fff.append(r'  <celebration>0</celebration>'+"\n")
    fff.append(r'  <celebrationSong></celebrationSong>'+"\n")
    fff.append(r'  <postProcessing></postProcessing>'+"\n")
    fff.append(r'  <defaultSpeed>2400</defaultSpeed>'+"\n")
    fff.append(r'  <outlineUnderspeed>0.85</outlineUnderspeed>'+"\n")
    fff.append(r'  <solidInfillUnderspeed>0.85</solidInfillUnderspeed>'+"\n")
    fff.append(r'  <supportUnderspeed>0.9</supportUnderspeed>'+"\n")
    fff.append(r'  <rapidXYspeed>12000</rapidXYspeed>'+"\n")
    fff.append(r'  <rapidZspeed>1002</rapidZspeed>'+"\n") # If this value changes, Simplify3D bug correction post script should be adapted
    fff.append(r'  <minBridgingArea>10</minBridgingArea>'+"\n")
    fff.append(r'  <bridgingExtraInflation>0</bridgingExtraInflation>'+"\n")
    fff.append(r'  <bridgingExtrusionMultiplier>1</bridgingExtrusionMultiplier>'+"\n")
    fff.append(r'  <bridgingSpeedMultiplier>1.5</bridgingSpeedMultiplier>'+"\n")
    fff.append(r'  <filamentDiameter>2.85</filamentDiameter>'+"\n")
    fff.append(r'  <filamentPricePerKg>19.95</filamentPricePerKg>'+"\n")
    fff.append(r'  <filamentDensity>1.25</filamentDensity>'+"\n")
    fff.append(r'  <useMinPrintHeight>0</useMinPrintHeight>'+"\n")
    fff.append(r'  <minPrintHeight>0</minPrintHeight>'+"\n")
    fff.append(r'  <useMaxPrintHeight>0</useMaxPrintHeight>'+"\n")
    fff.append(r'  <maxPrintHeight>0</maxPrintHeight>'+"\n")
    fff.append(r'  <useDiaphragm>0</useDiaphragm>'+"\n")
    fff.append(r'  <diaphragmLayerInterval>5</diaphragmLayerInterval>'+"\n")
    fff.append(r'  <robustSlicing>1</robustSlicing>'+"\n")
    fff.append(r'  <mergeAllIntoSolid>0</mergeAllIntoSolid>'+"\n")
    fff.append(r'  <onlyRetractWhenCrossingOutline>0</onlyRetractWhenCrossingOutline>'+"\n")
    fff.append(r'  <retractBetweenLayers>1</retractBetweenLayers>'+"\n")
    fff.append(r'  <useRetractionMinTravel>1</useRetractionMinTravel>'+"\n")
    fff.append(r'  <retractionMinTravel>1.5</retractionMinTravel>'+"\n")
    fff.append(r'  <retractWhileWiping>1</retractWhileWiping>'+"\n")
    fff.append(r'  <onlyWipeOutlines>1</onlyWipeOutlines>'+"\n")
    fff.append(r'  <avoidCrossingOutline>1</avoidCrossingOutline>'+"\n")
    fff.append(r'  <maxMovementDetourFactor>3</maxMovementDetourFactor>'+"\n")
    fff.append(r'  <toolChangeRetractionDistance>8</toolChangeRetractionDistance>'+"\n")
    fff.append(r'  <toolChangeExtraRestartDistance>0</toolChangeExtraRestartDistance>'+"\n")
    fff.append(r'  <toolChangeRetractionSpeed>2400</toolChangeRetractionSpeed>'+"\n")
    fff.append(r'  <allowThinWallGapFill>1</allowThinWallGapFill>'+"\n")
    fff.append(r'  <thinWallAllowedOverlapPercentage>10</thinWallAllowedOverlapPercentage>'+"\n")
    fff.append(r'  <horizontalSizeCompensation>-0.1</horizontalSizeCompensation>'+"\n")
    # fff.append(r'  <overridePrinterModels>1</overridePrinterModels>'+"\n")
    # fff.append(r'  <printerModelsOverride>BCN3DSigma.stl</printerModelsOverride>'+"\n")
    # fff.append(r'  <autoConfigureMaterial name="'+str(filamentLeft)+" Left, "+str(filamentRight)+" Right"+r'">'+"\n")
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
                    currentLayerHeight = hotendLeft['nozzleSize'] * quality['layerHeightMultiplier']
                    currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'MEX Left')
                    hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, currentDefaultSpeed)
                    hotendRightTemperature = hotendLeftTemperature
                    currentPurgeSpeedT0, currentStartPurgeLengthT0, currentToolChangePurgeLengthT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight)
                    currentPurgeSpeedT1, currentStartPurgeLengthT1, currentToolChangePurgeLengthT1 = currentPurgeSpeedT0, currentStartPurgeLengthT0, currentToolChangePurgeLengthT0
                else:
                    # MEX Right
                    currentPrimaryExtruder = 1
                    currentFilament = filamentRight
                    currentHotend = hotendRight
                    currentLayerHeight = hotendRight['nozzleSize'] * quality['layerHeightMultiplier']
                    currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'MEX Right')
                    hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeight, currentDefaultSpeed)
                    hotendLeftTemperature = hotendRightTemperature
                    currentPurgeSpeedT1, currentStartPurgeLengthT1, currentToolChangePurgeLengthT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight)
                    currentPurgeSpeedT0, currentStartPurgeLengthT0, currentToolChangePurgeLengthT0 = currentPurgeSpeedT1, currentStartPurgeLengthT1, currentToolChangePurgeLengthT1
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
                    currentSupportInfillPercentage = 15
                    currentDenseSupportInfillPercentage = 100
                    if filamentLeft['isSupportMaterial']:
                        # IDEX, Support Material in Left Hotend
                        currentPrimaryExtruder = 1
                        currentFilament = filamentRight
                        currentHotend = hotendRight
                        currentLayerHeight = min(hotendRight['nozzleSize'] * quality['layerHeightMultiplier'], hotendLeft['nozzleSize']*0.5)
                        supportFilament = filamentLeft
                        supportHotend = hotendLeft
                        secondaryExtruderAction = ' (Left Ext. for supports) - '
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'IDEX, Supports with Left')
                        currentPurgeSpeedT0, currentStartPurgeLengthT0, currentToolChangePurgeLengthT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed * currentSupportUnderspeed, currentLayerHeight)
                        currentPurgeSpeedT1, currentStartPurgeLengthT1, currentToolChangePurgeLengthT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight)
                        hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, currentDefaultSpeed*currentSupportUnderspeed)
                        hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeight, currentDefaultSpeed)
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M107'+"\t\t"+r';disable fan for support material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M106 S'+str(fanSpeed(currentFilament, hotendRightTemperature))+"\t\t"+r';enable fan for part material,'
                    else:
                        # IDEX, Support Material in Right Hotend
                        currentPrimaryExtruder = 0
                        currentFilament = filamentLeft
                        currentHotend = hotendLeft
                        currentLayerHeight = min(hotendLeft['nozzleSize'] * quality['layerHeightMultiplier'], hotendRight['nozzleSize']*0.5)
                        supportFilament = filamentRight
                        supportHotend = hotendRight
                        secondaryExtruderAction = ' (Right Ext. for supports) - '
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'IDEX, Supports with Right')
                        currentPurgeSpeedT0, currentStartPurgeLengthT0, currentToolChangePurgeLengthT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight)
                        currentPurgeSpeedT1, currentStartPurgeLengthT1, currentToolChangePurgeLengthT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed * currentSupportUnderspeed, currentLayerHeight)
                        hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, currentDefaultSpeed)
                        hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeight, currentDefaultSpeed*currentSupportUnderspeed)
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M106 S'+str(fanSpeed(currentFilament, hotendLeftTemperature))+"\t\t"+r';enable fan for part material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M107'+"\t\t"+r';disable fan for support material,' 
                    currentInfillExtruder = currentPrimaryExtruder
                    currentSupportExtruder = abs(currentPrimaryExtruder-1)
                else:
                    # IDEX, Combined Infill
                    currentAvoidCrossingOutline = 0l

                    # correccions pel combined infil
                    if hotendLeft['nozzleSize'] != hotendRight['nozzleSize']:
                        currentInfillPercentage = 100 #canviar?
                        currentOverlapInfillAngles = 0
                        if hotendLeft['nozzleSize'] < hotendRight['nozzleSize']: 
                            currentToolChangePurgeLengthT1 = str("%.2f" % (float(currentToolChangePurgeLengthT1)/4))
                        else:
                            currentToolChangePurgeLengthT0 = str("%.2f" % (float(currentToolChangePurgeLengthT0)/4))
                    # fi de les correccions

                    if hotendLeft['nozzleSize'] <= hotendRight['nozzleSize']:
                        # IDEX, Combined Infill (Right Hotend has thicker or equal nozzle)
                        currentPrimaryExtruder = 0
                        currentFilament = filamentLeft
                        currentHotend = hotendLeft
                        currentLayerHeight = min(currentHotend['nozzleSize'] * quality['layerHeightMultiplier'], hotendRight['nozzleSize']*0.5)
                        currentInfillLayerInterval = int(str((hotendRight['nozzleSize']*0.5)/currentLayerHeight).split('.')[0])
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'IDEX, Infill with Right')
                        hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight, max(currentDefaultSpeed,currentDefaultSpeed*currentOutlineUnderspeed))
                        hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeight*currentInfillLayerInterval, currentDefaultSpeed)
                        secondaryExtruderAction = ' (Right Ext. for infill) - '
                        if currentFilament['fanPercentage'] != 0:
                            fanActionOnToolChange1 = '' # '{IF NEWTOOL=0} M106 S'+str(fanSpeed(currentFilament, hotendLeftTemperature))+"\t\t"+r';enable fan for perimeters,'
                            fanActionOnToolChange2 = '' # '{IF NEWTOOL=1} M107'+"\t\t"+r';disable fan for infill,'
                        currentPurgeSpeedT0, currentStartPurgeLengthT0, currentToolChangePurgeLengthT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight)
                        currentPurgeSpeedT1, currentStartPurgeLengthT1, currentToolChangePurgeLengthT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight * currentInfillLayerInterval)
                    else:
                        # IDEX, Combined Infill (Left Hotend has thicker nozzle)
                        currentPrimaryExtruder = 1
                        currentFilament = filamentRight
                        currentHotend = hotendRight
                        currentLayerHeight = min(currentHotend['nozzleSize'] * quality['layerHeightMultiplier'], hotendLeft['nozzleSize']*0.5)
                        currentInfillLayerInterval = int(str((hotendLeft['nozzleSize']*0.5)/currentLayerHeight).split('.')[0])
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, 'IDEX, Infill with Left')
                        hotendLeftTemperature = temperatureValue(filamentLeft, hotendLeft, currentLayerHeight*currentInfillLayerInterval, currentDefaultSpeed)
                        hotendRightTemperature = temperatureValue(filamentRight, hotendRight, currentLayerHeight, max(currentDefaultSpeed,currentDefaultSpeed*currentOutlineUnderspeed))
                        secondaryExtruderAction = ' (Left Ext. for infill) - '
                        if currentFilament['fanPercentage'] != 0:
                            fanActionOnToolChange1 = '' # '{IF NEWTOOL=0} M107'+"\t\t"+r';disable fan for infill,'
                            fanActionOnToolChange2 = '' # '{IF NEWTOOL=1} M106 S'+str(fanSpeed(currentFilament, hotendRightTemperature))+"\t\t"+r';enable fan for perimeters,'
                        currentPurgeSpeedT0, currentStartPurgeLengthT0, currentToolChangePurgeLengthT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight * currentInfillLayerInterval)
                        currentPurgeSpeedT1, currentStartPurgeLengthT1, currentToolChangePurgeLengthT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight)
                    currentInfillExtruder = abs(currentPrimaryExtruder-1)
                    currentSupportExtruder = currentPrimaryExtruder
                currentBedTemperature = max(filamentLeft['bedTemperature'], filamentRight['bedTemperature'])
            currentFirstLayerHeightPercentage = int(min(125, (currentHotend['nozzleSize']/2)/currentLayerHeight*100, maxFlowValue(currentHotend, currentFilament)*100/(currentHotend['nozzleSize']*currentLayerHeight*(currentDefaultSpeed/60)*float(currentFirstLayerUnderspeed))))      
            currentPerimeterOutlines = max(2, int(round(quality['wallWidth'] / currentHotend['nozzleSize']))) #2 minimum Perimeters needed
            currentTopSolidLayers = max(4, int(round(quality['topBottomWidth'] / currentLayerHeight))) #4 minimum layers needed
            currentBottomSolidLayers = currentTopSolidLayers
            currentRaftExtruder = currentPrimaryExtruder
            currentSkirtExtruder = currentPrimaryExtruder
            useCoasting, useWipe, onlyRetractWhenCrossingOutline, retractBetweenLayers, useRetractionMinTravel, retractWhileWiping, onlyWipeOutlines = retractValues(currentFilament)
            fff.append(r'  <autoConfigureQuality name="'+extruder+secondaryExtruderAction+str(quality['id'])+r'">'+"\n")
            fff.append(r'    <globalExtrusionMultiplier>1</globalExtrusionMultiplier>'+"\n")
            fff.append(r'    <fanSpeed>'+"\n")
            fff.append(r'      <setpoint layer="1" speed="0" />'+"\n")
            if currentPrimaryExtruder == 0:
                fff.append(r'      <setpoint layer="2" speed="'+str(fanSpeed(currentFilament, hotendLeftTemperature))+r'" />'+"\n")
            else:
                fff.append(r'      <setpoint layer="2" speed="'+str(fanSpeed(currentFilament, hotendRightTemperature))+r'" />'+"\n")
            fff.append(r'    </fanSpeed>'+"\n")
            fff.append(r'    <filamentDiameter>'+str(currentFilament['filamentDiameter'])+r'</filamentDiameter>'+"\n")
            fff.append(r'    <filamentPricePerKg>'+str(currentFilament['filamentPricePerKg'])+r'</filamentPricePerKg>'+"\n")
            fff.append(r'    <filamentDensity>'+str(currentFilament['filamentDensity'])+r'</filamentDensity>'+"\n")
            if hotendLeft['id'] != 'None':
                fff.append(r'    <extruder name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">'+"\n")
                fff.append(r'      <toolheadNumber>0</toolheadNumber>'+"\n")
                fff.append(r'      <diameter>'+str(hotendLeft['nozzleSize'])+r'</diameter>'+"\n")
                fff.append(r'      <autoWidth>0</autoWidth>'+"\n")
                fff.append(r'      <width>'+str(hotendLeft['nozzleSize'])+r'</width>'+"\n")
                fff.append(r'      <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+r'</extrusionMultiplier>'+"\n")
                fff.append(r'      <useRetract>1</useRetract>'+"\n")
                fff.append(r'      <retractionDistance>'+str(filamentLeft['retractionDistance'])+r'</retractionDistance>'+"\n")
                fff.append(r'      <extraRestartDistance>0</extraRestartDistance>'+"\n")
                fff.append(r'      <retractionZLift>'+str("%.2f" % (currentLayerHeight/2.))+'</retractionZLift>'+"\n")
                fff.append(r'      <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+r'</retractionSpeed>'+"\n")
                fff.append(r'      <useCoasting>'+str(retractValues(filamentLeft)[0])+'</useCoasting>'+"\n")
                fff.append(r'      <coastingDistance>'+str(coastValue(hotendLeft, filamentLeft))+r'</coastingDistance>'+"\n")
                fff.append(r'      <useWipe>'+str(retractValues(filamentLeft)[1])+'</useWipe>'+"\n")
                fff.append(r'      <wipeDistance>'+str(hotendLeft['nozzleSize']*12.5)+r'</wipeDistance>'+"\n")
                fff.append(r'    </extruder>'+"\n")
            if hotendRight['id'] != 'None':
                fff.append(r'    <extruder name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">'+"\n")
                fff.append(r'      <toolheadNumber>1</toolheadNumber>'+"\n")
                fff.append(r'      <diameter>'+str(hotendRight['nozzleSize'])+r'</diameter>'+"\n")
                fff.append(r'      <autoWidth>0</autoWidth>'+"\n")
                fff.append(r'      <width>'+str(hotendRight['nozzleSize'])+r'</width>'+"\n")
                fff.append(r'      <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+r'</extrusionMultiplier>'+"\n")
                fff.append(r'      <useRetract>1</useRetract>'+"\n")
                fff.append(r'      <retractionDistance>'+str(filamentRight['retractionDistance'])+r'</retractionDistance>'+"\n")
                fff.append(r'      <extraRestartDistance>0</extraRestartDistance>'+"\n")
                fff.append(r'      <retractionZLift>'+str(currentLayerHeight/2)+'</retractionZLift>'+"\n")
                fff.append(r'      <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+r'</retractionSpeed>'+"\n")
                fff.append(r'      <useCoasting>'+str(retractValues(filamentRight)[0])+'</useCoasting>'+"\n")
                fff.append(r'      <coastingDistance>'+str(coastValue(hotendRight, filamentRight))+r'</coastingDistance>'+"\n")
                fff.append(r'      <useWipe>'+str(retractValues(filamentRight)[1])+'</useWipe>'+"\n")
                fff.append(r'      <wipeDistance>'+str(hotendRight['nozzleSize']*12.5)+r'</wipeDistance>'+"\n")
                fff.append(r'    </extruder>'+"\n")
            fff.append(r'    <primaryExtruder>'+str(currentPrimaryExtruder)+r'</primaryExtruder>'+"\n")
            fff.append(r'    <raftExtruder>'+str(currentRaftExtruder)+r'</raftExtruder>'+"\n")
            fff.append(r'    <skirtExtruder>'+str(currentSkirtExtruder)+r'</skirtExtruder>'+"\n")
            fff.append(r'    <infillExtruder>'+str(currentInfillExtruder)+r'</infillExtruder>'+"\n")
            fff.append(r'    <supportExtruder>'+str(currentSupportExtruder)+r'</supportExtruder>'+"\n")
            fff.append(r'    <generateSupport>'+str(currentGenerateSupport)+r'</generateSupport>'+"\n")
            fff.append(r'    <layerHeight>'+str(currentLayerHeight)+r'</layerHeight>'+"\n")
            fff.append(r'    <firstLayerHeightPercentage>'+str(currentFirstLayerHeightPercentage)+r'</firstLayerHeightPercentage>'+"\n")
            fff.append(r'    <topSolidLayers>'+str(currentTopSolidLayers)+r'</topSolidLayers>'+"\n")
            fff.append(r'    <bottomSolidLayers>'+str(currentBottomSolidLayers)+r'</bottomSolidLayers>'+"\n")
            fff.append(r'    <perimeterOutlines>'+str(currentPerimeterOutlines)+r'</perimeterOutlines>'+"\n")
            fff.append(r'    <infillPercentage>'+str(currentInfillPercentage)+r'</infillPercentage>'+"\n")
            fff.append(r'    <infillLayerInterval>'+str(currentInfillLayerInterval)+r'</infillLayerInterval>'+"\n")
            fff.append(r'    <defaultSpeed>'+str(currentDefaultSpeed)+r'</defaultSpeed>'+"\n")
            fff.append(r'    <firstLayerUnderspeed>'+str(currentFirstLayerUnderspeed)+r'</firstLayerUnderspeed>'+"\n")
            fff.append(r'    <outlineUnderspeed>'+str(currentOutlineUnderspeed)+r'</outlineUnderspeed>'+"\n")
            fff.append(r'    <supportUnderspeed>'+str(currentSupportUnderspeed)+r'</supportUnderspeed>'+"\n")
            fff.append(r'    <supportInfillPercentage>'+str(currentSupportInfillPercentage)+r'</supportInfillPercentage>'+"\n")
            fff.append(r'    <denseSupportInfillPercentage>'+str(currentDenseSupportInfillPercentage)+r'</denseSupportInfillPercentage>'+"\n")
            fff.append(r'    <avoidCrossingOutline>'+str(currentAvoidCrossingOutline)+'</avoidCrossingOutline>'+"\n")
            fff.append(r'    <overlapInfillAngles>'+str(currentOverlapInfillAngles)+'</overlapInfillAngles>'+"\n")
            fff.append(r'    <supportHorizontalPartOffset>'+str(currentSupportHorizontalPartOffset)+'</supportHorizontalPartOffset>'+"\n")
            fff.append(r'    <supportUpperSeparationLayers>'+str(currentSupportUpperSeparationLayers)+'</supportUpperSeparationLayers>'+"\n")
            fff.append(r'    <supportLowerSeparationLayers>'+str(currentSupportLowerSeparationLayers)+'</supportLowerSeparationLayers>'+"\n")
            fff.append(r'    <supportAngles>'+str(currentSupportAngles)+'</supportAngles>'+"\n")
            fff.append(r'    <onlyRetractWhenCrossingOutline>'+str(onlyRetractWhenCrossingOutline)+'</onlyRetractWhenCrossingOutline>'+"\n")
            fff.append(r'    <retractBetweenLayers>'+str(retractBetweenLayers)+'</retractBetweenLayers>'+"\n")
            fff.append(r'    <useRetractionMinTravel>'+str(useRetractionMinTravel)+'</useRetractionMinTravel>'+"\n")
            fff.append(r'    <retractWhileWiping>'+str(retractWhileWiping)+'</retractWhileWiping>'+"\n")
            fff.append(r'    <onlyWipeOutlines>'+str(onlyWipeOutlines)+'</onlyWipeOutlines>'+"\n")
            fff.append(r'    <minBridgingArea>10</minBridgingArea>'+"\n")
            fff.append(r'    <bridgingExtraInflation>0</bridgingExtraInflation>'+"\n")
            bridgingSpeedMultiplier = 1.5
            fff.append(r'    <bridgingExtrusionMultiplier>'+str(currentFilament['extrusionMultiplier']*(1/bridgingSpeedMultiplier))+'</bridgingExtrusionMultiplier>'+"\n")
            fff.append(r'    <bridgingSpeedMultiplier>'+str(bridgingSpeedMultiplier)+'</bridgingSpeedMultiplier>'+"\n")
            if hotendLeft['id'] != 'None':
                fff.append(r'    <temperatureController name="Left Extruder '+str(hotendLeft['nozzleSize'])+r'">'+"\n")
                fff.append(r'      <temperatureNumber>0</temperatureNumber>'+"\n")
                fff.append(r'      <isHeatedBed>0</isHeatedBed>'+"\n")
                fff.append(r'      <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
                fff.append(r'      <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
                fff.append(r'      <stabilizeAtStartup>0</stabilizeAtStartup>'+"\n")
                fff.append(r'      <setpoint layer="1" temperature="'+str(hotendLeftTemperature)+r'"/>'+"\n")
                fff.append(r'    </temperatureController>'+"\n")
            if hotendRight['id'] != 'None':
                fff.append(r'    <temperatureController name="Right Extruder '+str(hotendRight['nozzleSize'])+r'">'+"\n")
                fff.append(r'      <temperatureNumber>1</temperatureNumber>'+"\n")
                fff.append(r'      <isHeatedBed>0</isHeatedBed>'+"\n")
                fff.append(r'      <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
                fff.append(r'      <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
                fff.append(r'      <stabilizeAtStartup>0</stabilizeAtStartup>'+"\n")
                fff.append(r'      <setpoint layer="1" temperature="'+str(hotendRightTemperature)+r'"/>'+"\n")
                fff.append(r'    </temperatureController>'+"\n")
            if (hotendLeft['id'] != 'None' and filamentLeft['bedTemperature'] > 0) or (hotendRight['id'] != 'None' and filamentRight['bedTemperature'] > 0):
                fff.append(r'    <temperatureController name="Heated Bed">'+"\n")
                fff.append(r'      <temperatureNumber>0</temperatureNumber>'+"\n")
                fff.append(r'      <isHeatedBed>1</isHeatedBed>'+"\n")
                fff.append(r'      <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
                fff.append(r'      <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
                fff.append(r'      <stabilizeAtStartup>0</stabilizeAtStartup>'+"\n")
                fff.append(r'      <setpoint layer="1" temperature="'+str(currentBedTemperature)+r'"/>'+"\n")
                fff.append(r'    </temperatureController>'+"\n")
            if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':                    
                fff.append(r'    <toolChangeGcode>; To use dynamic purge values:,;    1. Gererate the gcode,;    2. Open the Sigma profile Generator -> 3. Experimental features -> 5. SmartPurge,,{IF NEWTOOL=0} T0'+"\t\t"+r';start tool switch 0,{IF NEWTOOL=0} G1 F500 E-0.5'+"\t\t"+r';fast purge,{IF NEWTOOL=0} G1 F'+str(currentPurgeSpeedT0)+' E'+str(currentToolChangePurgeLengthT0)+"\t"+r';slow purge,{IF NEWTOOL=0} G92 E0'+"\t\t"+r';reset t0,{IF NEWTOOL=0} G1 F3000 E-4.5'+"\t"+r';retract,{IF NEWTOOL=0} G1 F[travel_speed]'+"\t"+r';end tool switch,'+fanActionOnToolChange1+r',{IF NEWTOOL=1} T1'+"\t\t"+r';start tool switch 1,{IF NEWTOOL=1} G1 F500 E-0.5'+"\t\t"+r';fast purge,{IF NEWTOOL=1} G1 F'+str(currentPurgeSpeedT1)+' E'+str(currentToolChangePurgeLengthT1)+"\t"+r';slow purge,{IF NEWTOOL=1} G92 E0'+"\t\t"+r';reset t1,{IF NEWTOOL=1} G1 F3000 E-4.5'+"\t"+r';retract,{IF NEWTOOL=1} G1 F[travel_speed]'+"\t"+r';end tool switch,'+fanActionOnToolChange2+r',G91,G1 F[travel_speed] Z2,G90</toolChangeGcode>'+"\n")
            else:
                fff.append(r'    <toolChangeGcode/>'+"\n")
            if extruder == 'Left Extruder':
                fff.append(r'    <startingGcode>'+firstHeatSequence(hotendLeftTemperature, 0, currentBedTemperature, 'Simplify3D')+',G21'+"\t\t"+r';metric values,G90'+"\t\t"+r';absolute positioning,M82'+"\t\t"+r';set extruder to absolute mode,M107'+"\t\t"+r';start with the fan off,G28 X0 Y0'+"\t\t"+r';move X/Y to min endstops,G28 Z0'+"\t\t"+r';move Z to min endstops,T0'+"\t\t"+r';change to active toolhead,G92 E0'+"\t\t"+r';zero the extruded length,G1 Z5 F200'+"\t\t"+r';Safety Z axis movement,G1 F'+str(currentPurgeSpeedT0)+' E'+str(currentStartPurgeLengthT0)+"\t"+r';extrude '+str(currentStartPurgeLengthT0)+r'mm of feed stock,G92 E0'+"\t\t"+r';zero the extruded length again,G1 F[travel_speed],</startingGcode>'+"\n")
            elif extruder == 'Right Extruder':
                fff.append(r'    <startingGcode>'+firstHeatSequence(0, hotendRightTemperature, currentBedTemperature, 'Simplify3D')+',G21'+"\t\t"+r';metric values,G90'+"\t\t"+r';absolute positioning,M82'+"\t\t"+r';set extruder to absolute mode,M107'+"\t\t"+r';start with the fan off,G28 X0 Y0'+"\t\t"+r';move X/Y to min endstops,G28 Z0'+"\t\t"+r';move Z to min endstops,T1'+"\t\t"+r';change to active toolhead,G92 E0'+"\t\t"+r';zero the extruded length,G1 Z5 F200'+"\t\t"+r';Safety Z axis movement,G1 F'+str(currentPurgeSpeedT1)+' E'+str(currentStartPurgeLengthT1)+"\t"+r';extrude '+str(currentStartPurgeLengthT1)+r'mm of feed stock,G92 E0'+"\t\t"+r';zero the extruded length again,G1 F[travel_speed],</startingGcode>'+"\n")
            else:
                fff.append(r'    <startingGcode>'+firstHeatSequence(hotendLeftTemperature, hotendRightTemperature, currentBedTemperature, 'Simplify3D')+',G21'+"\t\t"+r';metric values,G90'+"\t\t"+r';absolute positioning,M107'+"\t\t"+r';start with the fan off,G28 X0 Y0'+"\t\t"+r';move X/Y to min endstops,G28 Z0'+"\t\t"+r';move Z to min endstops,T1'+"\t\t"+r';switch to the 2nd extruder,G92 E0'+"\t\t"+r';zero the extruded length,G1 F'+str(currentPurgeSpeedT1)+' E'+str(currentStartPurgeLengthT1)+"\t"+r';extrude '+str(currentStartPurgeLengthT1)+r'mm of feed stock,G92 E0'+"\t\t"+r';zero the extruded length again,G1 F200 E-9,T0'+"\t\t"+r';switch to the 1st extruder,G92 E0'+"\t\t"+r';zero the extruded length,G1 F'+str(currentPurgeSpeedT0)+' E'+str(currentStartPurgeLengthT0)+"\t"+r';extrude '+str(currentStartPurgeLengthT0)+r'mm of feed stock,G92 E0'+"\t\t"+r';zero the extruded length again,G1 Z5 F200'+"\t\t"+r';Safety Z axis movement,G1 F[travel_speed]</startingGcode>'+"\n")
            fff.append(r'    <postProcessing>{REPLACE "; outer perimeter" "; outer perimeter\nM204 S'+str(accelerationForPerimeters(currentHotend['nozzleSize'], currentLayerHeight, int(currentDefaultSpeed/60. * currentOutlineUnderspeed)))+r'"},{REPLACE "; inner perimeter" "; inner perimeter\nM204 S2000"},{REPLACE "; solid layer" "; solid layer\nM204 S2000"},{REPLACE "; infill" "; infill\nM204 S2000",{REPLACE "; support" "; support\nM204 S2000"},{REPLACE "; layer end" "; layer end\nM204 S2000"},{REPLACE "F12000\nG1 Z'+str(round(currentLayerHeight*currentFirstLayerHeightPercentage/100., 3))+r' F1002\nG92 E0" "F12000\nG1 Z'+str(round(currentLayerHeight*currentFirstLayerHeightPercentage/100., 3))+r' F1002\nG1 E0.0000 F720\nG92 E0"}</postProcessing>'+"\n")
            fff.append(r'  </autoConfigureQuality>'+"\n")

            if dataLog != 'noData' :
                # Store flows, speeds, temperatures and other data
                writeData(extruder, currentDefaultSpeed, currentInfillLayerInterval, currentLayerHeight, hotendLeft, hotendRight, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder, filamentLeft, filamentRight, quality, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed, currentFirstLayerHeightPercentage, hotendLeftTemperature, hotendRightTemperature, currentBedTemperature, dataLog)                        

    # fff.append(r'  </autoConfigureMaterial>'+"\n")

    if hotendLeft['id'] != 'None':
        fff.append(r'  <autoConfigureExtruders name="Left Extruder Only"  allowedToolheads="1">'+"\n")
        fff.append(r'    <layerChangeGcode>M104 S0 T1</layerChangeGcode>'+"\n")
        fff.append(r'  </autoConfigureExtruders>'+"\n")
    if hotendRight['id'] != 'None':
        fff.append(r'  <autoConfigureExtruders name="Right Extruder Only"  allowedToolheads="1">'+"\n")
        fff.append(r'    <layerChangeGcode>M104 S0 T0</layerChangeGcode>'+"\n")
        fff.append(r'  </autoConfigureExtruders>'+"\n")
    if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':
        fff.append(r'  <autoConfigureExtruders name="Both Extruders"  allowedToolheads="2">'+"\n")
        fff.append(r'    <layerChangeGcode></layerChangeGcode>'+"\n")
        fff.append(r'  </autoConfigureExtruders>'+"\n")

    fff.append(r'</profile>'+"\n")
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
            currentLayerHeight = hotend['nozzleSize'] * quality['layerHeightMultiplier']
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
            currentFirstLayerHeightPercentage = int(min(125, (hotend['nozzleSize']/2)/currentLayerHeight*100, maxFlowValue(hotendRight, filamentRight)*100/(hotend['nozzleSize']*currentLayerHeight*(currentDefaultSpeed/60.)*float(currentFirstLayerUnderspeed))))
            firstLayerHeight = "%.2f" % (currentLayerHeight * currentFirstLayerHeightPercentage/100.)
            if filamentRight['fanPercentage'] > 0:
                fanEnabled = 'True'
            else:
                fanEnabled = 'False'
            fanPercentage = fanSpeed(filamentRight, printTemperature2)            
            hotendLeftTemperature, hotendRightTemperature = 0, printTemperature2
            currentPurgeSpeed, currentStartPurgeLength, currentToolChangePurgeLength = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight)       
            currentPurgeSpeedT0, currentStartPurgeLengthT0, currentToolChangePurgeLengthT0 = currentPurgeSpeed, currentStartPurgeLength, currentToolChangePurgeLength
            currentPurgeSpeedT1, currentStartPurgeLengthT1, currentToolChangePurgeLengthT1 = currentPurgeSpeed, currentStartPurgeLength, currentToolChangePurgeLength
    elif hotendRight['id'] == 'None':
        # MEX Left
        hotend, extruder, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder = hotendLeft, "Left Extruder", 0, 0, 0
        currentLayerHeight = hotend['nozzleSize'] * quality['layerHeightMultiplier']
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
        currentFirstLayerHeightPercentage = int(min(125, (hotend['nozzleSize']/2)/currentLayerHeight*100, maxFlowValue(hotendLeft, filamentLeft)*100/(hotend['nozzleSize']*currentLayerHeight*(currentDefaultSpeed/60.)*float(currentFirstLayerUnderspeed))))
        firstLayerHeight = "%.2f" % (currentLayerHeight * currentFirstLayerHeightPercentage/100.)
        if filamentLeft['fanPercentage'] > 0:
            fanEnabled = 'True'
        else:
            fanEnabled = 'False'
        fanPercentage = fanSpeed(filamentLeft, printTemperature1)
        hotendLeftTemperature, hotendRightTemperature = printTemperature1, 0
        currentPurgeSpeed, currentStartPurgeLength, currentToolChangePurgeLength = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight)
        currentPurgeSpeedT0, currentStartPurgeLengthT0, currentToolChangePurgeLengthT0 = currentPurgeSpeed, currentStartPurgeLength, currentToolChangePurgeLength
        currentPurgeSpeedT1, currentStartPurgeLengthT1, currentToolChangePurgeLengthT1 = currentPurgeSpeed, currentStartPurgeLength, currentToolChangePurgeLength
    else:
        # IDEX
        hotend, extruder, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder = hotendLeft, "Both Extruders", 0, 0, 0
        currentLayerHeight = hotend['nozzleSize'] * quality['layerHeightMultiplier']
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
        currentFirstLayerHeightPercentage = int(min(125, (hotend['nozzleSize']/2)/currentLayerHeight*100, min(maxFlowValue(hotendLeft, filamentLeft),maxFlowValue(hotendRight, filamentRight))*100/(hotend['nozzleSize']*currentLayerHeight*(currentDefaultSpeed/60)*float(currentFirstLayerUnderspeed))))
        firstLayerHeight = "%.2f" % (currentLayerHeight * currentFirstLayerHeightPercentage/100.)
        if filamentLeft['fanPercentage'] == 0 or filamentRight['fanPercentage'] == 0:
            fanEnabled = 'False'
        else:
            fanEnabled = 'True'
        fanPercentage = max(fanSpeed(filamentLeft, printTemperature1), fanSpeed(filamentRight, printTemperature2))
        hotendLeftTemperature, hotendRightTemperature = printTemperature1, printTemperature2

        currentPurgeSpeedT0, currentStartPurgeLengthT0, currentToolChangePurgeLengthT0 = purgeValues(hotendLeft, filamentLeft, currentDefaultSpeed, currentLayerHeight)
        currentPurgeSpeedT1, currentStartPurgeLengthT1, currentToolChangePurgeLengthT1 = purgeValues(hotendRight, filamentRight, currentDefaultSpeed, currentLayerHeight)
        currentPurgeSpeed, currentStartPurgeLength, currentToolChangePurgeLength = min(currentPurgeSpeedT0, currentPurgeSpeedT1), max(currentStartPurgeLengthT0, currentStartPurgeLengthT1), max(currentToolChangePurgeLengthT0, currentToolChangePurgeLengthT0)

    perimeters = 0
    while perimeters*hotend['nozzleSize'] < quality['wallWidth']:
        perimeters += 1
    currentWallThickness = perimeters * hotend['nozzleSize']
    bottomLayerSpeed = int(currentFirstLayerUnderspeed * currentDefaultSpeed/60.)
    outerShellSpeed = int(currentOutlineUnderspeed * currentDefaultSpeed/60.)
    innerShellSpeed = int(outerShellSpeed + (currentDefaultSpeed/60.-outerShellSpeed)/2.)

    ini = []
    ini.append(r'[profile]'+"\n")
    ini.append(r'layer_height = '+str(currentLayerHeight)+"\n")
    ini.append(r'wall_thickness = '+str(currentWallThickness)+"\n")
    ini.append(r'retraction_enable = True'+"\n")
    ini.append(r'solid_layer_thickness = '+str(quality['topBottomWidth'])+"\n")
    ini.append(r'fill_density = '+str(quality['infillPercentage'])+"\n")
    ini.append(r'nozzle_size = '+str(hotend['nozzleSize'])+"\n")
    ini.append(r'print_speed = '+str(currentDefaultSpeed/60)+"\n")
    ini.append(r'print_temperature = '+str(printTemperature1)+"\n")
    ini.append(r'print_temperature2 = '+str(printTemperature2)+"\n")
    ini.append(r'print_temperature3 = 0'+"\n")
    ini.append(r'print_temperature4 = 0'+"\n")
    ini.append(r'print_temperature5 = 0'+"\n")
    ini.append(r'print_bed_temperature = '+str(bedTemperature)+"\n")
    ini.append(r'support = '+makeSupports+"\n")
    ini.append(r'platform_adhesion = None'+"\n")
    ini.append(r'support_dual_extrusion = '+supportDualExtrusion+"\n")
    ini.append(r'wipe_tower = False'+"\n")
    ini.append(r'wipe_tower_volume = 50'+"\n")
    ini.append(r'ooze_shield = False'+"\n")
    ini.append(r'filament_diameter = '+str(filamentDiameter1)+"\n")
    ini.append(r'filament_diameter2 = '+str(filamentDiameter2)+"\n")
    ini.append(r'filament_diameter3 = 0'+"\n")
    ini.append(r'filament_diameter4 = 0'+"\n")
    ini.append(r'filament_diameter5 = 0'+"\n")
    ini.append(r'filament_flow = '+str(filamentFlow)+"\n")
    ini.append(r'retraction_speed = '+str(retractionSpeed)+"\n")
    ini.append(r'retraction_amount = '+str(retractionAmount)+"\n")
    ini.append(r'retraction_dual_amount = 8'+"\n")
    ini.append(r'retraction_min_travel = 1.5'+"\n")
    ini.append(r'retraction_combing = All'+"\n")
    ini.append(r'retraction_minimal_extrusion = 0'+"\n")
    ini.append(r'retraction_hop = '+str("%.2f" % (currentLayerHeight/2.))+"\n")
    ini.append(r'bottom_thickness = '+str(firstLayerHeight)+"\n")
    ini.append(r'layer0_width_factor = 100'+"\n")
    ini.append(r'object_sink = 0'+"\n")
    ini.append(r'overlap_dual = 0.15'+"\n")
    ini.append(r'travel_speed = 200'+"\n")
    ini.append(r'bottom_layer_speed = '+str(bottomLayerSpeed)+"\n")
    ini.append(r'infill_speed = '+str(currentDefaultSpeed/60)+"\n")
    ini.append(r'solidarea_speed = '+str(bottomLayerSpeed)+"\n")
    ini.append(r'inset0_speed = '+str(outerShellSpeed)+"\n")
    ini.append(r'insetx_speed = '+str(innerShellSpeed)+"\n")
    ini.append(r'cool_min_layer_time = 5'+"\n")
    ini.append(r'fan_enabled = '+str(fanEnabled)+"\n")
    ini.append(r'skirt_line_count = 2'+"\n")
    ini.append(r'skirt_gap = 2'+"\n")
    ini.append(r'skirt_minimal_length = 150.0'+"\n")
    ini.append(r'fan_full_height = 0.5'+"\n")
    ini.append(r'fan_speed = '+str(fanPercentage)+"\n")
    ini.append(r'fan_speed_max = 100'+"\n")
    ini.append(r'cool_min_feedrate = 10'+"\n")
    ini.append(r'cool_head_lift = False'+"\n")
    ini.append(r'solid_top = True'+"\n")
    ini.append(r'solid_bottom = True'+"\n")
    ini.append(r'fill_overlap = 15'+"\n")
    ini.append(r'perimeter_before_infill = True'+"\n")
    ini.append(r'support_type = '+str(supportType)+"\n")
    ini.append(r'support_angle = 60'+"\n")
    ini.append(r'support_fill_rate = 40'+"\n")
    ini.append(r'support_xy_distance = '+str(supportXYDistance)+"\n")
    ini.append(r'support_z_distance = '+str(supportZdistance)+"\n")
    ini.append(r'spiralize = False'+"\n")
    ini.append(r'simple_mode = False'+"\n")
    ini.append(r'brim_line_count = 5'+"\n")
    ini.append(r'raft_margin = 5.0'+"\n")
    ini.append(r'raft_line_spacing = 3.0'+"\n")
    ini.append(r'raft_base_thickness = 0.3'+"\n")
    ini.append(r'raft_base_linewidth = 1.0'+"\n")
    ini.append(r'raft_interface_thickness = 0.27'+"\n")
    ini.append(r'raft_interface_linewidth = 0.4'+"\n")
    ini.append(r'raft_airgap_all = 0.0'+"\n")
    ini.append(r'raft_airgap = 0.22'+"\n")
    ini.append(r'raft_surface_layers = 2'+"\n")
    ini.append(r'raft_surface_thickness = 0.27'+"\n")
    ini.append(r'raft_surface_linewidth = 0.4'+"\n")
    ini.append(r'fix_horrible_union_all_type_a = True'+"\n")
    ini.append(r'fix_horrible_union_all_type_b = False'+"\n")
    ini.append(r'fix_horrible_use_open_bits = False'+"\n")
    ini.append(r'fix_horrible_extensive_stitching = False'+"\n")
    ini.append(r'plugin_config = '+'(lp1'+"\n")
    ini.append("\t(dp2"+"\n")
    ini.append("\tS'params'"+"\n")
    ini.append("\tp3"+"\n")
    ini.append("\t(dp4"+"\n")
    ini.append("\tsS'filename'"+"\n")
    ini.append("\tp5"+"\n")
    ini.append("\tS'RingingRemover.py'"+"\n")
    ini.append("\tp6"+"\n")
    ini.append("\tsa."+"\n")
    ini.append(r'object_center_x = -1'+"\n")
    ini.append(r'object_center_y = -1'+"\n")
    ini.append(r'quality_fast = False'+"\n")
    ini.append(r'quality_standard = False'+"\n")
    ini.append(r'quality_high = False'+"\n")
    ini.append(r'quality_strong = False'+"\n")
    ini.append(r'extruder_left = False'+"\n")
    ini.append(r'extruder_right = False'+"\n")
    ini.append(r'material_pla = False'+"\n")
    ini.append(r'material_abs = False'+"\n")
    ini.append(r'material_fila = False'+"\n")
    ini.append(r'quality_fast_dual = False'+"\n")
    ini.append(r'quality_standard_dual = False'+"\n")
    ini.append(r'quality_high_dual = False'+"\n")
    ini.append(r'quality_strong_dual = False'+"\n")
    ini.append(r'pla_left_dual = False'+"\n")
    ini.append(r'abs_left_dual = False'+"\n")
    ini.append(r'fila_left_dual = False'+"\n")
    ini.append(r'pla_right_dual = False'+"\n")
    ini.append(r'abs_right_dual = False'+"\n")
    ini.append(r'fila_right_dual = False'+"\n")
    ini.append(r'pva_right_dual = False'+"\n")
    ini.append(r'dual_support = False'+"\n")
    ini.append("\n")
    ini.append(r'[alterations]'+"\n")
    ini.append(r'start.gcode = ;Sliced at: {day} {date} {time}'+"\n")
    ini.append('\t;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}'+"\n")
    ini.append('\t;Print time: {print_time}'+"\n")
    ini.append('\t;Filament used: {filament_amount}m {filament_weight}g'+"\n")
    ini.append('\t;Filament cost: {filament_cost}'+"\n")
    if hotendLeft['id'] != 'None':
        ini.append(firstHeatSequence(printTemperature1, 0, bedTemperature, 'Cura'))
    else:
        ini.append(firstHeatSequence(0, printTemperature2, bedTemperature, 'Cura'))
    ini.append('\tG21                               ;metric values'+"\n")
    ini.append('\tG90                               ;absolute positioning'+"\n")
    ini.append('\tM82                               ;set extruder to absolute mode'+"\n")
    ini.append('\tM107                              ;start with the fan off'+"\n")
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops'+"\n")
    ini.append('\tG28 Z0                            ;move Z to min endstops'+"\n")
    ini.append('\tT'+str(currentPrimaryExtruder)+'  ;change to active toolhead'+"\n")
    ini.append('\tG92 E0                            ;zero the extruded length'+"\n")
    ini.append('\tG1 Z5 F1200                       ;Safety Z axis movement'+"\n")
    ini.append('\tG1 F'+str(currentPurgeSpeed)+' E'+str(currentStartPurgeLength)+' ;extrude '+str(currentStartPurgeLength)+'mm of feed stock'+"\n")
    ini.append('\tG92 E0                            ;zero the extruded length again'+"\n")
    ini.append('\tG1 F2400 E-4                      ;Retract before printing'+"\n")
    ini.append('\tG1 F{travel_speed}'+"\n")
    ini.append(r'end.gcode = M104 S0'+"\n")
    ini.append('\tM140 S0                           ;heated bed heater off'+"\n")
    ini.append('\tG91                               ;relative positioning'+"\n")
    ini.append('\tG1 Z+0.5 E-5 Y+10 F{travel_speed} ;move Z up a bit and retract filament even more'+"\n")
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops, so the head is out of the way'+"\n")
    ini.append('\tM84                               ;steppers off'+"\n")
    ini.append('\tG90                               ;absolute positioning'+"\n")
    ini.append('\t;{profile_string}'+"\n")
    ini.append(r'start2.gcode = ;Sliced at: {day} {date} {time}'+"\n")
    ini.append('\t;Basic settings: Layer height: {layer_height} Walls: {wall_thickness} Fill: {fill_density}'+"\n")
    ini.append('\t;Print time: {print_time}'+"\n")
    ini.append('\t;Filament used: {filament_amount}m {filament_weight}g'+"\n")
    ini.append('\t;Filament cost: {filament_cost}'+"\n")
    ini.append(firstHeatSequence(printTemperature1, printTemperature2, bedTemperature, 'Cura'))
    ini.append('\tG21                               ;metric values'+"\n")
    ini.append('\tG90                               ;absolute positioning'+"\n")
    ini.append('\tM107                              ;start with the fan off'+"\n")
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops'+"\n")
    ini.append('\tG28 Z0                            ;move Z to min endstops'+"\n")
    ini.append('\tT1                                ;switch to the 2nd extruder'+"\n")
    ini.append('\tG92 E0                            ;zero the extruded length'+"\n")
    ini.append('\tG1 F'+str(currentPurgeSpeedT1)+' E'+str(currentStartPurgeLengthT1)+' ;extrude '+str(currentStartPurgeLengthT1)+'mm of feed stock'+"\n")
    ini.append('\tG92 E0                            ;zero the extruded length again'+"\n")
    ini.append('\tG1 F2400 E-{retraction_dual_amount}'+"\n")
    ini.append('\tT0                                ;switch to the 1st extruder'+"\n")
    ini.append('\tG92 E0                            ;zero the extruded length'+"\n")
    ini.append('\tG1 F'+str(currentPurgeSpeedT0)+' E'+str(currentStartPurgeLengthT0)+' ;extrude '+str(currentStartPurgeLengthT0)+'mm of feed stock'+"\n")
    ini.append('\tG92 E0                            ;zero the extruded length again'+"\n")
    ini.append('\tG1 Z5 F1200                       ;Safety Z axis movement'+"\n")
    ini.append('\tG1 F{travel_speed}'+"\n")
    ini.append(r'end2.gcode = M104 T0 S0'+"\n")
    ini.append('\tM104 T1 S0                        ;extruder heater off'+"\n")
    ini.append('\tM140 S0                           ;heated bed heater off'+"\n")
    ini.append('\tG91                               ;relative positioning'+"\n")
    ini.append('\tG1 Z+0.5 E-5 Y+10 F{travel_speed} ;move Z up a bit and retract filament even more'+"\n")
    ini.append('\tG28 X0 Y0                         ;move X/Y to min endstops, so the head is out of the way'+"\n")
    ini.append('\tM84                               ;steppers off'+"\n")
    ini.append('\tG90                               ;absolute positioning'+"\n")
    ini.append('\t;{profile_string}'+"\n")
    ini.append(r'support_start.gcode = '+"\n")
    ini.append(r'support_end.gcode = '+"\n")
    ini.append(r'cool_start.gcode = '+"\n")
    ini.append(r'cool_end.gcode = '+"\n")
    ini.append(r'replace.csv = '+"\n")
    ini.append(r'preswitchextruder.gcode =          ;Switch between the current extruder and the next extruder, when printing with multiple extruders.'+"\n")
    ini.append('\t;This code is added before the T(n)'+"\n")
    ini.append(r'postswitchextruder.gcode =         ;Switch between the current extruder and the next extruder, when printing with multiple extruders.'+"\n")
    ini.append('\t;This code is added after the T(n)'+"\n")
    ini.append('\tG1 F500 E-0.5'+"\n")
    ini.append('\tG1 F'+str(currentPurgeSpeed)+' E'+str(currentToolChangePurgeLength)+"\n")
    ini.append('\tG92 E0'+"\n")
    ini.append('\tG1 F2400 E-4'+"\n")
    ini.append('\tG1 F{travel_speed}'+"\n")
    ini.append('\tG91'+"\n")
    ini.append('\tG1 F{travel_speed} Z2'+"\n")
    ini.append('\tG90'+"\n")

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

def speedMultiplier(hotend, filament):
    if filament['isFlexibleMaterial']:
        return float(filament['defaultPrintSpeed'])/24*hotend['nozzleSize']
    else:
        return float(filament['defaultPrintSpeed'])/60

def purgeValues(hotend, filament, speed, layerHeight):
    baseStartLength04 = 7
    baseToolChangeLength04 = 1.5
    
    # speed adapted to printed area
    # purgeSpeed = float("%.2f" % (speed * hotend['nozzleSize'] * layerHeight / (math.pi * (filament['filamentDiameter']/2.)**2)))
    
    # speed adapted to improve surplus material storage, 6000 is a experimental value that defines material speed at the nozzle tip
    purgeSpeed = float("%.2f" % (6000 * hotend['nozzleSize'] / (math.pi * (filament['filamentDiameter']/2.)**2)))

    startPurgeLength = float("%.2f" % max(10, ((hotend['nozzleSize']/0.4)**2*baseStartLength04*filament['purgeLength']/baseToolChangeLength04)))
    toolChangePurgeLength = float("%.2f" % ((hotend['nozzleSize']/0.4)**2*filament['purgeLength']))

    return purgeSpeed, startPurgeLength, toolChangePurgeLength

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

def maxFlowValue(hotend, filament):
    if hotend['nozzleSize'] <= 0.6:
        if filament['maxFlow'] == 'None':
            return 0.4*0.2*filament['advisedMaxPrintSpeed']
        else:
            return filament['maxFlow']
    else:
        if filament['maxFlowForHighFlowHotend'] == 'None':
            if filament['maxFlow'] == 'None':
                return 0.4*0.2*filament['advisedMaxPrintSpeed']
            else:
                return filament['maxFlow']
        else:
            return filament['maxFlowForHighFlowHotend']

def temperatureValue(filament, hotend, layerHeight, speed, base = 5):
    # adaptative temperature according to flow values. Rounded to base
    flow = hotend['nozzleSize']*layerHeight*float(speed)/60

    # Warning if something is not working properly
    if int(flow) > int(maxFlowValue(hotend, filament)):
        print "warning! you're trying to print at higher flow than allowed"

    temperature = int(base * round((filament['printTemperature'][0] + flow/maxFlowValue(hotend, filament) * float(filament['printTemperature'][1]-filament['printTemperature'][0]))/float(base)))
    return temperature

def fanSpeed(filament, temperature, base = 5):
    # adaptative fan speed according to temperature values. Rounded to base
    if filament['printTemperature'][1] - filament['printTemperature'][0] == 0 or filament['fanPercentage'] == 0:
        fanSpeed = filament['fanPercentage']
    else:
        fanSpeed = int(base * round((filament['fanPercentage'] + (temperature-filament['printTemperature'][0])/float(filament['printTemperature'][1]-filament['printTemperature'][0])*float(100-filament['fanPercentage']))/float(base)))
    return fanSpeed

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
    return startSequenceString

def accelerationForPerimeters(nozzleSize, layerHeight, outerWallSpeed, base = 5, multiplier = 30000, defaultAcceleration = 2000):
    return min(defaultAcceleration, int(base * round((nozzleSize * layerHeight * multiplier * 1/(outerWallSpeed**(1/2.)))/float(base))))

def speedValues(hotendLeft, hotendRight, filamentLeft, filamentRight, currentLayerHeight, currentInfillLayerInterval, quality, action):
    if action == 'MEX Left' or action == 'IDEX, Infill with Right' or action == 'IDEX, Supports with Right':
        leftExtruderDefaultSpeed = quality['defaultSpeed']*speedMultiplier(hotendLeft, filamentLeft)
        leftExtruderMaxSpeedAtMaxFlow = maxFlowValue(hotendLeft, filamentLeft)/(hotendLeft['nozzleSize']*currentLayerHeight)
        if action == 'IDEX, Infill with Right':
            rightExtruderMaxSpeedAtMaxFlow = maxFlowValue(hotendRight, filamentRight)/(currentInfillLayerInterval*currentLayerHeight*hotendRight['nozzleSize'])
        else:
            rightExtruderMaxSpeedAtMaxFlow = leftExtruderMaxSpeedAtMaxFlow
        currentDefaultSpeed = int(str(float(min(leftExtruderDefaultSpeed, leftExtruderMaxSpeedAtMaxFlow, rightExtruderMaxSpeedAtMaxFlow)*60)).split('.')[0])
        maxAllowedUnderspeed = maxFlowValue(hotendLeft, filamentLeft)/(currentLayerHeight*hotendLeft['nozzleSize']*float(currentDefaultSpeed)/60)
        
        if filamentLeft['isFlexibleMaterial']:
            currentFirstLayerUnderspeed = 1.00
            currentOutlineUnderspeed = 1.00
        else:
            currentFirstLayerUnderspeed = float("%.2f" % min(maxAllowedUnderspeed, (leftExtruderDefaultSpeed*60*quality['firstLayerUnderspeed']/float(currentDefaultSpeed))))
            currentOutlineUnderspeed    = float("%.2f" % min(maxAllowedUnderspeed, (leftExtruderDefaultSpeed*60*quality['outlineUnderspeed']   /float(currentDefaultSpeed))))

        if action == 'IDEX, Supports with Right':
            currentSupportUnderspeed    = float("%.2f" % min((currentDefaultSpeed/60.), (maxFlowValue(hotendRight, filamentRight)/float(hotendLeft['nozzleSize'] * quality['layerHeightMultiplier']*hotendRight['nozzleSize']*currentDefaultSpeed/60.)))) # needs better adjust
        else:
            currentSupportUnderspeed    = float("%.2f" % (leftExtruderDefaultSpeed*60*0.9                            /float(currentDefaultSpeed)))

    elif action == 'MEX Right' or action == 'IDEX, Infill with Left' or action == 'IDEX, Supports with Left':
        rightExtruderDefaultSpeed = quality['defaultSpeed']*speedMultiplier(hotendRight, filamentRight)
        rightExtruderMaxSpeedAtMaxFlow = maxFlowValue(hotendRight, filamentRight)/(hotendRight['nozzleSize']*currentLayerHeight)
        if action == 'IDEX, Infill with Left':
            leftExtruderMaxSpeedAtMaxFlow = maxFlowValue(hotendLeft, filamentLeft)/(currentInfillLayerInterval*currentLayerHeight*hotendLeft['nozzleSize'])
        else:
            leftExtruderMaxSpeedAtMaxFlow = rightExtruderMaxSpeedAtMaxFlow
        currentDefaultSpeed = int(str(float(min(rightExtruderDefaultSpeed, rightExtruderMaxSpeedAtMaxFlow, leftExtruderMaxSpeedAtMaxFlow)*60)).split('.')[0])
        maxAllowedUnderspeed = maxFlowValue(hotendRight, filamentRight)/(currentLayerHeight*hotendRight['nozzleSize']*float(currentDefaultSpeed)/60)

        if filamentRight['isFlexibleMaterial']:
            currentFirstLayerUnderspeed = 1.00
            currentOutlineUnderspeed = 1.00
        else:
            currentFirstLayerUnderspeed = float("%.2f" % min(maxAllowedUnderspeed, (rightExtruderDefaultSpeed*60*quality['firstLayerUnderspeed']/float(currentDefaultSpeed))))
            currentOutlineUnderspeed    = float("%.2f" % min(maxAllowedUnderspeed, (rightExtruderDefaultSpeed*60*quality['outlineUnderspeed']   /float(currentDefaultSpeed))))

        if action == 'IDEX, Supports with Left':
            currentSupportUnderspeed    = float("%.2f" % min((currentDefaultSpeed/60.), (maxFlowValue(hotendLeft, filamentLeft)/float(hotendRight['nozzleSize']*quality['layerHeightMultiplier']*hotendLeft['nozzleSize']*currentDefaultSpeed/60.)))) # needs better adjust
        else:
            currentSupportUnderspeed    = float("%.2f" % (rightExtruderDefaultSpeed*60*0.9                            /float(currentDefaultSpeed)))

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

    realCuraProfileaAvailable = (totalSmaProfiles + curaIDEXHotendsCombinations * len(profilesData['filament'])**2) * len(profilesData['quality'])

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
                        sys.stdout.write("\r\t\tTesting Cura Profiles: %d%%" % int(float(combinationCount)/totalProfilesAvailable*100))
                        sys.stdout.flush()
    print '\r\t\tTesting Cura Profiles: OK. Profiles Tested:'+str(realCuraProfileaAvailable)

    print '\t\tAll '+str(realSimplify3DProfilesAvailable + realCuraProfileaAvailable)+' profiles can be generated!\n'

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


    dataLog.append(filamentLeft['id']+";"+filamentRight['id']+";"+extruder+";"+quality['id']+";"+hotendLeft['id']+";"+hotendRight['id']+";"+'T'+str(currentInfillExtruder)+";"+'T'+str(currentPrimaryExtruder)+";"+'T'+str(currentSupportExtruder)+";"+str(printA)+";"+str(printB)+";"+str(currentInfillLayerInterval)+";"+str("%.2f" % (currentDefaultSpeed/60.))+";"+str(currentFirstLayerUnderspeed)+";"+str(currentOutlineUnderspeed)+";"+str(currentSupportUnderspeed)+";"+str(currentFirstLayerHeightPercentage)+";"+str(hotendLeftTemperature)+";"+str(hotendRightTemperature)+";"+str(currentBedTemperature)+";\n")

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
                print '\n Welcome to the BCN3D Sigma Profile Generator \n'
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
                    print '\n\tChoose one option (1-5):'
                    print '\t1. Generate a bundle of profiles - Simplify3D'
                    print '\t2. Generate a bundle of profiles - Cura'
                    print '\t3. Test all combinations'
                    print '\t4. MacOS Only - Slice a model (with Cura)'
                    print '\t5. Use the SmartPurge algorithm to recalculate purge lengths'
                    print '\t6. Back'
                    x2 = 'x'
                    while x2 not in ['1','2','3','4', '5', '6']:
                        x2 = raw_input('\t')

                singleProfileSimplify3D, singleProfileCura, bundleProfilesSimplify3D, bundleProfilesCura, testComb, sliceModel, smartPurge = False, False, False, False, False, False, False

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
                        smartPurge = True
                        GUIHeader = '\n Welcome to the BCN3D Sigma Profile Generator \n\n\n\n\n    Experimental features\n\n\n\n\n\n\n\t   Use the SmartPurge algorithm to recalculate purge lengths'
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
                elif smartPurge:
                    clearDisplay()
                    print GUIHeader
                    print '\n\t\tWork in progress... Stay tuned!\n\t\t'
                    raw_input("\t\tPress Enter to continue...")

if __name__ == '__main__':
    main() 