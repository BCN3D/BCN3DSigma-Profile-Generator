#!/usr/bin/python -tt
# coding: utf-8

#Guillem Àvila Padró - October 2016
#Released under MIT LICENSE
#https://opensource.org/licenses/MIT

import time
import os
import shutil
import sys
import json
import string

with open('ProfilesData.json') as data_file:    
    profilesData = json.load(data_file)

def writeData(extruder, currentDefaultSpeed, currentInfillLayerInterval, currentLayerHeight, nozzleLeft, nozzleRight, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder, filamentLeft, filamentRight, quality, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed, currentFirstLayerHeightPercentage, nozzleLeftLayer2Temperature, nozzleRightLayer2Temperature, currentBedTemperature, dataLog):
    if extruder[0] == 'L':
        printA = "%.2f" % float(float(currentDefaultSpeed)/60*currentInfillLayerInterval*currentLayerHeight*nozzleLeft)
        printB = ""
    elif extruder[0] == 'R':
        printA = ""
        printB = "%.2f" % float(float(currentDefaultSpeed)/60*currentInfillLayerInterval*currentLayerHeight*nozzleRight)
    else:
        if filamentLeft['isSupportMaterial'] != filamentRight['isSupportMaterial']:
            if filamentLeft['isSupportMaterial']:
                supportMaterialLoadedLeft = float(currentSupportUnderspeed)
                supportMaterialLoadedRight = 1
            else:
                supportMaterialLoadedLeft = 1
                supportMaterialLoadedRight = float(currentSupportUnderspeed)
        else:
            supportMaterialLoadedLeft = 1
            supportMaterialLoadedRight = 1
        if nozzleLeft != nozzleRight:
            if currentPrimaryExtruder == 0: 
                printA = "%.2f" % float(float(currentDefaultSpeed)/60*currentLayerHeight*nozzleLeft*supportMaterialLoadedLeft)
                printB = "%.2f" % float(float(currentDefaultSpeed)/60*currentInfillLayerInterval*currentLayerHeight*nozzleRight*supportMaterialLoadedRight)
            else:
                printA = "%.2f" % float(float(currentDefaultSpeed)/60*currentLayerHeight*currentInfillLayerInterval*nozzleLeft*supportMaterialLoadedLeft)
                printB = "%.2f" % float(float(currentDefaultSpeed)/60*currentLayerHeight*nozzleRight*supportMaterialLoadedRight)
        else:
            printA = "%.2f" % float(float(currentDefaultSpeed)/60*currentInfillLayerInterval*currentLayerHeight*nozzleLeft*supportMaterialLoadedLeft)
            printB = "%.2f" % float(float(currentDefaultSpeed)/60*currentInfillLayerInterval*currentLayerHeight*nozzleRight*supportMaterialLoadedRight)
    dataLog.append(filamentLeft['id']+";"+filamentRight['id']+";"+extruder+";"+quality['id'][2:]+";"+str(nozzleLeft)+";"+str(nozzleRight)+";"+'T'+str(currentInfillExtruder)+";"+'T'+str(currentPrimaryExtruder)+";"+'T'+str(currentSupportExtruder)+";"+str(printA)+";"+str(printB)+";"+str(currentInfillLayerInterval)+";"+str("%.2f" % float(currentDefaultSpeed/60.))+";"+str(currentFirstLayerUnderspeed)+";"+str(currentOutlineUnderspeed)+";"+str(currentSupportUnderspeed)+";"+str(currentFirstLayerHeightPercentage)+";"+str(nozzleLeftLayer2Temperature)+";"+str(nozzleRightLayer2Temperature)+";"+str(currentBedTemperature)+";\n")

def speedMultiplier(nozzle, filament):
    if filament['isFlexibleMaterial']:
        return float(filament['printSpeed'][0])/24*nozzle
    else:
        return float(filament['printSpeed'][0])/60

def purgeValues(nozzle, filament):
    baseSpeed04 = 50
    baseStartLenght04 = 7
    baseToolChangeLenght04 = 1.5
    return str("%.2f" % float((nozzle/0.4)**2*baseSpeed04)), str("%.2f" % float((nozzle/0.4)**2*baseStartLenght04*filament['purgeMultiplier'])), str("%.2f" % float((nozzle/0.4)**2*baseToolChangeLenght04*filament['purgeMultiplier']))

def flowValue(nozzle, filament):
    if nozzle <= 0.6:
        if filament['maxFlow'] == 0:
            return 0.4*0.2*filament['printSpeed'][1]
        else:
            return filament['maxFlow']
    else:
        if filament['maxFlowForHighFlowHotends'] == 0:
            if filament['maxFlow'] == 0:
                return 0.4*0.2*filament['printSpeed'][1]
            else:
                return filament['maxFlow']
        else:
            return filament['maxFlowForHighFlowHotends']

def temperatureValue(filament, nozzle, layerHeight, speed, base = 5):
    # adaptative temperature for flow values. Rounded to base
    flow = nozzle*layerHeight*float(speed)/60
    temperature = int(base * round((filament['printTemperature'][0]+flow*float(filament['printTemperature'][1]-filament['printTemperature'][0])/flowValue(nozzle, filament))/float(base)))
    return temperature

def speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, action):
    if action == 'MEX Left' or action == 'IDEX, Infill with Right' or action == 'IDEX, Supports with Right':
        currentFilament = filamentLeft
        leftExtruderDefaultSpeed = quality['defaultSpeed']*speedMultiplier(nozzleLeft, filamentLeft)
        leftExtruderMaxSpeedAtDefaultTemperature = flowValue(nozzleLeft, filamentLeft)/(nozzleLeft*quality['layerHeightMultiplier']*nozzleLeft)
        if action == 'IDEX, Infill with Right':
            rightExtruderMaxSpeedAtHighTemperature = flowValue(nozzleRight, filamentRight)/(nozzleRight*quality['layerHeightMultiplier']*nozzleRight)
            currentDefaultSpeed = int(str(float(min(leftExtruderDefaultSpeed, leftExtruderMaxSpeedAtDefaultTemperature, rightExtruderMaxSpeedAtHighTemperature)*60)).split('.')[0])
        else:
            currentDefaultSpeed = int(str(float(min(leftExtruderDefaultSpeed, leftExtruderMaxSpeedAtDefaultTemperature)*60)).split('.')[0])
        leftExtruderNeededFirstLayerUnderspeed = leftExtruderDefaultSpeed*60*quality['firstLayerUnderspeed']/float(currentDefaultSpeed) 
        leftExtruderNeededOutlineUnderspeed = leftExtruderDefaultSpeed*60*quality['outlineUnderspeed']/float(currentDefaultSpeed)
        leftExtruderNeededSupportUnderspeed = leftExtruderDefaultSpeed*60*0.9/float(currentDefaultSpeed)
        if filamentLeft['isFlexibleMaterial']:
            currentFirstLayerUnderspeed = 1.00
            currentOutlineUnderspeed = 1.00
        else:
            currentFirstLayerUnderspeed = "%.2f" % float(min(leftExtruderNeededFirstLayerUnderspeed, 1))
            currentOutlineUnderspeed = "%.2f" % float(min(leftExtruderNeededOutlineUnderspeed, 1))

        if action == 'IDEX, Supports with Right':
            currentSupportUnderspeed = "%.2f" % float(flowValue(nozzleRight, filamentRight)/float(nozzleLeft * quality['layerHeightMultiplier']*nozzleRight*currentDefaultSpeed/60.))
        else:
            currentSupportUnderspeed = "%.2f" % float(min(leftExtruderNeededSupportUnderspeed, 1))
    elif action == 'MEX Right' or action == 'IDEX, Infill with Left' or action == 'IDEX, Supports with Left':
        currentFilament = filamentRight
        rightExtruderDefaultSpeed = quality['defaultSpeed']*speedMultiplier(nozzleRight, filamentRight)
        rightExtruderMaxSpeedAtDefaultTemperature = flowValue(nozzleRight, filamentRight)/(nozzleRight*quality['layerHeightMultiplier']*nozzleRight)
        if action == 'IDEX, Infill with Left':
            leftExtruderMaxSpeedAtHighTemperature = flowValue(nozzleLeft, filamentLeft)/(nozzleLeft*quality['layerHeightMultiplier']*nozzleLeft)
            currentDefaultSpeed = int(str(float(min(rightExtruderDefaultSpeed, rightExtruderMaxSpeedAtDefaultTemperature, leftExtruderMaxSpeedAtHighTemperature)*60)).split('.')[0])
        else:
            currentDefaultSpeed = int(str(float(min(rightExtruderDefaultSpeed, rightExtruderMaxSpeedAtDefaultTemperature)*60)).split('.')[0])
        rightExtruderNeededFirstLayerUnderspeed = rightExtruderDefaultSpeed*60*quality['firstLayerUnderspeed']/float(currentDefaultSpeed)
        rightExtruderNeededOutlineUnderspeed = rightExtruderDefaultSpeed*60*quality['outlineUnderspeed']/float(currentDefaultSpeed)
        rightExtruderNeededSupportUnderspeed = rightExtruderDefaultSpeed*60*0.9/float(currentDefaultSpeed)
        if filamentRight['isFlexibleMaterial']:
            currentFirstLayerUnderspeed = 1.00
            currentOutlineUnderspeed = 1.00
        else:
            currentFirstLayerUnderspeed = "%.2f" % float(min(rightExtruderNeededFirstLayerUnderspeed, 1))
            currentOutlineUnderspeed = "%.2f" % float(min(rightExtruderNeededOutlineUnderspeed, 1))
        if action == 'IDEX, Supports with Left':
            currentSupportUnderspeed = "%.2f" % float(flowValue(nozzleLeft, filamentLeft)/float(nozzleRight * quality['layerHeightMultiplier']*nozzleLeft*currentDefaultSpeed/60.))
        else:
            currentSupportUnderspeed = "%.2f" % float(min(rightExtruderNeededSupportUnderspeed, 1))
    if currentFilament['isFlexibleMaterial']:
        currentFirstLayerUnderspeed = 1.00
        currentOutlineUnderspeed = 1.00
    return currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed

def createProfile(nozzleLeft, nozzleRight, filamentLeft, filamentRight, dataLog, createFile):
    fff = []
    fff.append(r'<?xml version="1.0" encoding="utf-8"?>'+"\n")
    for q in profilesData['quality']:
        if q['id'][2:] == 'Medium':
            defaultPrintQualityBase = 'Medium'
            break
        else:
            defaultPrintQualityBase = profilesData['quality'][0]['id'][2:]
    if nozzleLeft == 'None':
        fileName = "BCN3D Sigma - Right Extruder "+str(nozzleRight)+" Only ("+filamentRight['id']+")"
        defaultPrintMaterial = filamentRight['id']
        defaultPrintQuality = 'Right Extruder ('+defaultPrintMaterial+') - '+defaultPrintQualityBase
        extruderPrintOptions = ["Right Extruder"]
        filamentLeft = dict([('id', '')])
        if nozzleRight == 'None':
            return
    elif nozzleRight == 'None':
        fileName = "BCN3D Sigma - Left Extruder "+str(nozzleLeft)+" Only ("+filamentLeft['id']+")"
        defaultPrintMaterial = filamentLeft['id']
        defaultPrintQuality = 'Left Extruder ('+defaultPrintMaterial+') - '+defaultPrintQualityBase
        extruderPrintOptions = ["Left Extruder"]
        filamentRight = dict([('id', '')])
    else:
        fileName = "BCN3D Sigma - "+str(nozzleLeft)+" Left ("+filamentLeft['id']+"), "+str(nozzleRight)+" Right ("+filamentRight['id']+")"
        defaultPrintMaterial = profilesData['filament'][0]['id']+' Left, '+profilesData['filament'][0]['id']+' Right'
        defaultPrintQuality = 'Left Extruder ('+defaultPrintMaterial+') - '+defaultPrintQualityBase
        extruderPrintOptions = ["Left Extruder", "Right Extruder", "Both Extruders"]
    fff.append(r'<profile name="'+fileName+r'" version="'+time.strftime("%Y-%m-%d")+" "+time.strftime("%H:%M:%S")+r'" app="S3D-Software 3.1.1">'+"\n")    
    fff.append(r'  <baseProfile></baseProfile>'+"\n")
    fff.append(r'  <printMaterial>'+defaultPrintMaterial+'</printMaterial>'+"\n")
    fff.append(r'  <printQuality>'+defaultPrintQuality+'</printQuality>'+"\n") #+extruder+secondaryExtruderAction+str(quality['id'][2:])+
    fff.append(r'  <printExtruders></printExtruders>'+"\n")
    if nozzleLeft != 'None':
        fff.append(r'  <extruder name="Left Extruder '+str(nozzleLeft)+r'">'+"\n")
        fff.append(r'    <toolheadNumber>0</toolheadNumber>'+"\n")
        fff.append(r'    <diameter>'+str(nozzleLeft)+r'</diameter>'+"\n")
        fff.append(r'    <autoWidth>0</autoWidth>'+"\n")
        fff.append(r'    <width>'+str(nozzleLeft)+r'</width>'+"\n")
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
    if nozzleRight != 'None':
        fff.append(r'  <extruder name="Right Extruder '+str(nozzleRight)+r'">'+"\n")
        fff.append(r'    <toolheadNumber>1</toolheadNumber>'+"\n")
        fff.append(r'    <diameter>'+str(nozzleRight)+r'</diameter>'+"\n")
        fff.append(r'    <autoWidth>0</autoWidth>'+"\n")
        fff.append(r'    <width>'+str(nozzleRight)+r'</width>'+"\n")
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
    fff.append(r'  <startPointOption>2</startPointOption>'+"\n")
    fff.append(r'  <startPointOriginX>0</startPointOriginX>'+"\n")
    fff.append(r'  <startPointOriginY>0</startPointOriginY>'+"\n")
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
    fff.append(r'  <internalInfillPattern>Rectilinear</internalInfillPattern>'+"\n")
    fff.append(r'  <externalInfillPattern>Rectilinear</externalInfillPattern>'+"\n")
    fff.append(r'  <infillPercentage>20</infillPercentage>'+"\n")
    fff.append(r'  <outlineOverlapPercentage>25</outlineOverlapPercentage>'+"\n")
    fff.append(r'  <infillExtrusionWidthPercentage>100</infillExtrusionWidthPercentage>'+"\n")
    fff.append(r'  <minInfillLength>3</minInfillLength>'+"\n")
    fff.append(r'  <infillLayerInterval>1</infillLayerInterval>'+"\n")
    fff.append(r'  <infillAngles>45,-45</infillAngles>'+"\n")
    fff.append(r'  <overlapInfillAngles>0</overlapInfillAngles>'+"\n")
    fff.append(r'  <generateSupport>0</generateSupport>'+"\n")
    fff.append(r'  <supportExtruder>0</supportExtruder>'+"\n")
    fff.append(r'  <supportInfillPercentage>25</supportInfillPercentage>'+"\n")
    fff.append(r'  <supportExtraInflation>0</supportExtraInflation>'+"\n")
    fff.append(r'  <denseSupportLayers>5</denseSupportLayers>'+"\n")
    fff.append(r'  <denseSupportInfillPercentage>75</denseSupportInfillPercentage>'+"\n")
    fff.append(r'  <supportLayerInterval>1</supportLayerInterval>'+"\n")
    fff.append(r'  <supportHorizontalPartOffset>0.2</supportHorizontalPartOffset>'+"\n")
    fff.append(r'  <supportUpperSeparationLayers>1</supportUpperSeparationLayers>'+"\n")
    fff.append(r'  <supportLowerSeparationLayers>1</supportLowerSeparationLayers>'+"\n")
    fff.append(r'  <supportType>0</supportType>'+"\n")
    fff.append(r'  <supportGridSpacing>3</supportGridSpacing>'+"\n")
    fff.append(r'  <maxOverhangAngle>45</maxOverhangAngle>'+"\n")
    fff.append(r'  <supportAngles>0</supportAngles>'+"\n")
    if nozzleLeft != 'None':
        fff.append(r'  <temperatureController name="Left Extruder '+str(nozzleLeft)+r'">'+"\n")
        fff.append(r'    <temperatureNumber>0</temperatureNumber>'+"\n")
        fff.append(r'    <isHeatedBed>0</isHeatedBed>'+"\n")
        fff.append(r'    <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
        fff.append(r'    <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
        fff.append(r'    <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
        fff.append(r'    <setpoint layer="1" temperature="150"/>'+"\n")
        fff.append(r'  </temperatureController>'+"\n")
    if nozzleRight != 'None':
        fff.append(r'  <temperatureController name="Right Extruder '+str(nozzleRight)+r'">'+"\n")
        fff.append(r'    <temperatureNumber>1</temperatureNumber>'+"\n")
        fff.append(r'    <isHeatedBed>0</isHeatedBed>'+"\n")
        fff.append(r'    <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
        fff.append(r'    <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
        fff.append(r'    <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
        fff.append(r'    <setpoint layer="1" temperature="150"/>'+"\n")
        fff.append(r'  </temperatureController>'+"\n")
    if (nozzleLeft != 'None' and filamentLeft['bedTemperature'] > 0) or (nozzleRight != 'None' and filamentRight['bedTemperature'] > 0):
        fff.append(r'  <temperatureController name="Heated Bed">'+"\n")
        fff.append(r'    <temperatureNumber>0</temperatureNumber>'+"\n")
        fff.append(r'    <isHeatedBed>1</isHeatedBed>'+"\n")
        fff.append(r'    <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
        fff.append(r'    <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
        fff.append(r'    <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
        fff.append(r'    <setpoint layer="1" temperature="50"/>'+"\n")
        fff.append(r'  </temperatureController>'+"\n")
    fff.append(r'  <fanSpeed>'+"\n")
    fff.append(r'    <setpoint layer="1" speed="0" />'+"\n")
    fff.append(r'    <setpoint layer="2" speed="100"/>'+"\n")
    fff.append(r'  </fanSpeed>'+"\n")
    fff.append(r'  <blipFanToFullPower>0</blipFanToFullPower>'+"\n")
    fff.append(r'  <adjustSpeedForCooling>1</adjustSpeedForCooling>'+"\n")
    fff.append(r'  <minSpeedLayerTime>5</minSpeedLayerTime>'+"\n")
    fff.append(r'  <minCoolingSpeedSlowdown>20</minCoolingSpeedSlowdown>'+"\n")
    fff.append(r'  <increaseFanForCooling>0</increaseFanForCooling>'+"\n")
    fff.append(r'  <minFanLayerTime>45</minFanLayerTime>'+"\n")
    fff.append(r'  <maxCoolingFanSpeed>100</maxCoolingFanSpeed>'+"\n")
    fff.append(r'  <increaseFanForBridging>0</increaseFanForBridging>'+"\n")
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
    fff.append(r'  <endingGcode>M104 S0 T0,M104 S0 T1,M140 S0'+"\t\t"+r';heated bed heater off (if you have it),G91'+"\t\t"+r';relative positioning,G1 Y+10 F[travel_speed]'+"\t"+r';move Z up a bit and retract filament even more,G28 X0 Y0'+"\t\t"+r';move X/Y to min endstops so the head is out of the way,M84'+"\t\t"+r';steppers off,G90'+"\t\t"+r';absolute positioning,</endingGcode>'+"\n")
    fff.append(r'  <exportFileFormat>gcode</exportFileFormat>'+"\n")
    fff.append(r'  <celebration>0</celebration>'+"\n")
    fff.append(r'  <celebrationSong></celebrationSong>'+"\n")
    fff.append(r'  <postProcessing></postProcessing>'+"\n")
    fff.append(r'  <defaultSpeed>2400</defaultSpeed>'+"\n")
    fff.append(r'  <outlineUnderspeed>0.85</outlineUnderspeed>'+"\n")
    fff.append(r'  <solidInfillUnderspeed>0.85</solidInfillUnderspeed>'+"\n")
    fff.append(r'  <supportUnderspeed>0.9</supportUnderspeed>'+"\n")
    fff.append(r'  <rapidXYspeed>12000</rapidXYspeed>'+"\n")
    fff.append(r'  <rapidZspeed>1002</rapidZspeed>'+"\n")
    fff.append(r'  <minBridgingArea>50</minBridgingArea>'+"\n")
    fff.append(r'  <bridgingExtraInflation>0</bridgingExtraInflation>'+"\n")
    fff.append(r'  <bridgingExtrusionMultiplier>1</bridgingExtrusionMultiplier>'+"\n")
    fff.append(r'  <bridgingSpeedMultiplier>1</bridgingSpeedMultiplier>'+"\n")
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
    fff.append(r'  <retractBetweenLayers>0</retractBetweenLayers>'+"\n")
    fff.append(r'  <useRetractionMinTravel>1</useRetractionMinTravel>'+"\n")
    fff.append(r'  <retractionMinTravel>1.5</retractionMinTravel>'+"\n")
    fff.append(r'  <retractWhileWiping>1</retractWhileWiping>'+"\n")
    fff.append(r'  <onlyWipeOutlines>1</onlyWipeOutlines>'+"\n")
    fff.append(r'  <avoidCrossingOutline>0</avoidCrossingOutline>'+"\n")
    fff.append(r'  <maxMovementDetourFactor>3</maxMovementDetourFactor>'+"\n")
    fff.append(r'  <toolChangeRetractionDistance>8</toolChangeRetractionDistance>'+"\n")
    fff.append(r'  <toolChangeExtraRestartDistance>0</toolChangeExtraRestartDistance>'+"\n")
    fff.append(r'  <toolChangeRetractionSpeed>2400</toolChangeRetractionSpeed>'+"\n")
    fff.append(r'  <allowThinWallGapFill>1</allowThinWallGapFill>'+"\n")
    fff.append(r'  <thinWallAllowedOverlapPercentage>10</thinWallAllowedOverlapPercentage>'+"\n")
    fff.append(r'  <horizontalSizeCompensation>0</horizontalSizeCompensation>'+"\n")
    # fff.append(r'  <overridePrinterModels>1</overridePrinterModels>'+"\n")
    # fff.append(r'  <printerModelsOverride>zyyx3dprinter.stl</printerModelsOverride>'+"\n")
    # fff.append(r'  <autoConfigureMaterial name="'+str(filamentLeft)+" Left, "+str(filamentRight)+" Right"+r'">'+"\n")
    for extruder in extruderPrintOptions:
        for quality in sorted(profilesData['quality'], key=lambda k: k['id']):
            currentInfillLayerInterval = 1
            currentGenerateSupport = 0
            # MEX
            if extruder[0] == 'L' or extruder[0] == 'R':
                if extruder[0] == 'L':
                    currentPrimaryExtruder = 0
                    currentFilament = filamentLeft
                    currentNozzle = nozzleLeft
                    currentLayerHeight = currentNozzle * quality['layerHeightMultiplier']
                    currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'MEX Left')
                    nozzleLeftLayer1Temperature = temperatureValue(currentFilament, currentNozzle, currentLayerHeight, currentDefaultSpeed)
                    nozzleLeftLayer2Temperature = temperatureValue(currentFilament, currentNozzle, currentLayerHeight, currentDefaultSpeed)
                    nozzleRightLayer1Temperature = 150
                    nozzleRightLayer2Temperature = 0
                else:
                    currentPrimaryExtruder = 1
                    currentFilament = filamentRight
                    currentNozzle = nozzleRight
                    currentLayerHeight = currentNozzle * quality['layerHeightMultiplier']
                    currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'MEX Right')
                    nozzleLeftLayer1Temperature = 150
                    nozzleLeftLayer2Temperature = 0
                    nozzleRightLayer1Temperature = temperatureValue(currentFilament, currentNozzle, currentLayerHeight, currentDefaultSpeed)
                    nozzleRightLayer2Temperature = temperatureValue(currentFilament, currentNozzle, currentLayerHeight, currentDefaultSpeed)
                currentPurgeSpeed, currentStartPurgeLenght, currentToolChangePurgeLenght = purgeValues(currentNozzle, currentFilament)
                currentStartingGcode = r'      <startingGcode>G21'+"\t\t"+r';metric values,G90'+"\t\t"+r';absolute positioning,M82'+"\t\t"+r';set extruder to absolute mode,M107'+"\t\t"+r';start with the fan off,G28 X0 Y0'+"\t\t"+r';move X/Y to min endstops,G28 Z0'+"\t\t"+r';move Z to min endstops,T'+str(currentPrimaryExtruder)+"\t\t"+r';change to active toolhead,G92 E0'+"\t\t"+r';zero the extruded length,G1 Z5 F200'+"\t\t"+r';Safety Z axis movement,G1 F'+currentPurgeSpeed+' E'+currentStartPurgeLenght+"\t"+r';extrude '+currentStartPurgeLenght+r'mm of feed stock,G92 E0'+"\t\t"+r';zero the extruded length again,G1 F200 E-4'+"\t\t"+r';Retract before printing,G1 F[travel_speed],</startingGcode>'+"\n"
                currentToolChangeGCode = r'      <toolChangeGcode/>'+"\n"
                currentInfillExtruder = currentPrimaryExtruder
                currentSupportExtruder = currentPrimaryExtruder
                currentBedTemperature = currentFilament['bedTemperature']
                if filamentLeft['id'] != filamentRight['id']:
                    secondaryExtruderAction = ' ('+currentFilament['id']+') - '
                else:
                    secondaryExtruderAction = ' - '
            # IDEX
            else:
                # IDEX, Support Material
                if filamentLeft['isSupportMaterial'] != filamentRight['isSupportMaterial']:
                    currentGenerateSupport = 1
                    if filamentLeft['isSupportMaterial']:
                        currentPrimaryExtruder = 1
                        currentFilament = filamentRight
                        currentNozzle = nozzleRight
                        supportFilament = filamentLeft
                        supportNozzle = nozzleLeft
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M107'+"\t\t"+r';disable fan for support material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M106'+"\t\t"+r';enable fan for part material,'
                        secondaryExtruderAction = ' (Left Ext. for supports) - '
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'IDEX, Supports with Left')
                    else:
                        currentPrimaryExtruder = 0
                        currentFilament = filamentLeft
                        currentNozzle = nozzleLeft
                        supportFilament = filamentRight
                        supportNozzle = nozzleRight
                        fanActionOnToolChange1 = '{IF NEWTOOL=0} M106'+"\t\t"+r';enable fan for part material,'
                        fanActionOnToolChange2 = '{IF NEWTOOL=1} M107'+"\t\t"+r';disable fan for support material,' 
                        secondaryExtruderAction = ' (Right Ext. for supports) - '
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'IDEX, Supports with Right')
                    currentInfillExtruder = currentPrimaryExtruder
                    currentSupportExtruder = abs(currentPrimaryExtruder-1)
                    currentLayerHeight = currentNozzle * quality['layerHeightMultiplier']
                    nozzleLeftLayer1Temperature = temperatureValue(filamentLeft, nozzleLeft, currentLayerHeight, currentDefaultSpeed)
                    nozzleLeftLayer2Temperature = temperatureValue(filamentLeft, nozzleLeft, currentLayerHeight, currentDefaultSpeed)
                    nozzleRightLayer1Temperature = temperatureValue(filamentRight, nozzleRight, currentLayerHeight, currentDefaultSpeed)
                    nozzleRightLayer2Temperature = temperatureValue(filamentRight, nozzleRight, currentLayerHeight, currentDefaultSpeed)
                # IDEX, Combined Infill
                else:
                    fanActionOnToolChange1 = ''
                    fanActionOnToolChange2 = ''
                    if nozzleLeft <= nozzleRight:
                        currentPrimaryExtruder = 0
                        currentFilament = filamentLeft
                        currentNozzle = nozzleLeft
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'IDEX, Infill with Right')
                        if nozzleLeft != nozzleRight:
                            currentInfillLayerInterval = int(str(min(flowValue(nozzleRight, filamentRight)/(max(nozzleLeft, nozzleRight)*currentDefaultSpeed/60*quality['layerHeightMultiplier']*min(nozzleLeft, nozzleRight)),(max(nozzleLeft, nozzleRight)*0.75)/(quality['layerHeightMultiplier']*min(nozzleLeft, nozzleRight)))).split('.')[0])
                        currentLayerHeight = currentNozzle * quality['layerHeightMultiplier']
                        nozzleLeftLayer1Temperature = temperatureValue(filamentLeft, nozzleLeft, currentLayerHeight, currentDefaultSpeed)
                        nozzleLeftLayer2Temperature = temperatureValue(filamentLeft, nozzleLeft, currentLayerHeight, currentDefaultSpeed)
                        nozzleRightLayer1Temperature = temperatureValue(filamentRight, nozzleRight, currentLayerHeight*currentInfillLayerInterval, currentDefaultSpeed)
                        nozzleRightLayer2Temperature = temperatureValue(filamentRight, nozzleRight, currentLayerHeight*currentInfillLayerInterval, currentDefaultSpeed)
                        secondaryExtruderAction = ' (Right Ext. for infill) - '
                        if currentFilament['fanMultiplier'] != 0:
                            fanActionOnToolChange1 = '{IF NEWTOOL=0} M106'+"\t\t"+r';enable fan for perimeters,'
                            fanActionOnToolChange2 = '{IF NEWTOOL=1} M107'+"\t\t"+r';disable fan for infill,'
                        if nozzleLeft == nozzleRight:
                            nozzleRightLayer1Temperature = temperatureValue(filamentRight, nozzleRight, currentLayerHeight, currentDefaultSpeed)
                            nozzleRightLayer2Temperature = temperatureValue(filamentRight, nozzleRight, currentLayerHeight, currentDefaultSpeed)
                    else:
                        currentPrimaryExtruder = 1
                        currentFilament = filamentRight
                        currentNozzle = nozzleRight
                        currentLayerHeight = currentNozzle * quality['layerHeightMultiplier']
                        currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'IDEX, Infill with Left')
                        currentInfillLayerInterval = int(str(min(flowValue(nozzleLeft, filamentLeft)/(max(nozzleLeft, nozzleRight)*currentDefaultSpeed/60*quality['layerHeightMultiplier']*min(nozzleLeft, nozzleRight)),(max(nozzleLeft, nozzleRight)*0.75)/(quality['layerHeightMultiplier']*min(nozzleLeft, nozzleRight)))).split('.')[0])
                        nozzleLeftLayer1Temperature = temperatureValue(filamentLeft, nozzleLeft, currentLayerHeight*currentInfillLayerInterval, currentDefaultSpeed)
                        nozzleLeftLayer2Temperature = temperatureValue(filamentLeft, nozzleLeft, currentLayerHeight*currentInfillLayerInterval, currentDefaultSpeed)
                        nozzleRightLayer1Temperature = temperatureValue(filamentRight, nozzleRight, currentLayerHeight, currentDefaultSpeed)
                        nozzleRightLayer2Temperature = temperatureValue(filamentRight, nozzleRight, currentLayerHeight, currentDefaultSpeed)
                        secondaryExtruderAction = ' (Left Ext. for infill) - '
                        if currentFilament['fanMultiplier'] != 0:
                            fanActionOnToolChange1 = '{IF NEWTOOL=0} M107'+"\t\t"+r';disable fan for infill,'
                            fanActionOnToolChange2 = '{IF NEWTOOL=1} M106'+"\t\t"+r';enable fan for perimeters,'
                    currentInfillExtruder = abs(currentPrimaryExtruder-1)
                    currentSupportExtruder = currentPrimaryExtruder
                currentBedTemperature = max(filamentLeft['bedTemperature'], filamentRight['bedTemperature'])
                currentPurgeSpeedT0, currentStartPurgeLenghtT0, currentToolChangePurgeLenghtT0 = purgeValues(nozzleLeft, filamentLeft)
                currentPurgeSpeedT1, currentStartPurgeLenghtT1, currentToolChangePurgeLenghtT1 = purgeValues(nozzleRight, filamentRight)       
                currentStartingGcode = r'      <startingGcode>G21'+"\t\t"+r';metric values,G90'+"\t\t"+r';absolute positioning,M107'+"\t\t"+r';start with the fan off,G28 X0 Y0'+"\t\t"+r';move X/Y to min endstops,G28 Z0'+"\t\t"+r';move Z to min endstops,T1'+"\t\t"+r';Switch to the 2nd extruder,G92 E0'+"\t\t"+r';zero the extruded length,G1 F'+currentPurgeSpeedT1+' E'+currentStartPurgeLenghtT1+"\t"+r';extrude '+currentStartPurgeLenghtT1+r'mm of feed stock,G92 E0'+"\t\t"+r';zero the extruded length again,G1 F200 E-9,T0'+"\t\t"+r';Switch to the first extruder,G92 E0'+"\t\t"+r';zero the extruded length,G1 F'+currentPurgeSpeedT0+' E'+currentStartPurgeLenghtT0+"\t"+r';extrude '+currentStartPurgeLenghtT0+r'mm of feed stock,G92 E0'+"\t\t"+r';zero the extruded length again,G1 Z5 F200'+"\t\t"+r';Safety Z axis movement,G1 F[travel_speed]</startingGcode>'+"\n"              
                currentToolChangeGCode = r'      <toolChangeGcode>{IF NEWTOOL=0} T0'+"\t\t"+r';start tool switch 0,;{IF NEWTOOL=0} G1 X0 Y0 F[travel_speed]'+"\t"+r';travel,{IF NEWTOOL=0} G1 F500 E-0.5'+"\t\t"+r';fast purge,{IF NEWTOOL=0} G1 F'+currentPurgeSpeedT0+' E'+currentToolChangePurgeLenghtT0+"\t"+r';slow purge,{IF NEWTOOL=0} G92 E0'+"\t\t"+r';reset t0,{IF NEWTOOL=0} G1 F3000 E-4.5'+"\t"+r';retract,{IF NEWTOOL=0} G1 F[travel_speed]'+"\t"+r';end tool switch,'+fanActionOnToolChange1+r',{IF NEWTOOL=1} T1'+"\t\t"+r';start tool switch 1,;{IF NEWTOOL=1} G1 X210 Y0 F[travel_speed]'+"\t"+r';travel,{IF NEWTOOL=1} G1 F500 E-0.5'+"\t\t"+r';fast purge,{IF NEWTOOL=1} G1 F'+currentPurgeSpeedT1+' E'+currentToolChangePurgeLenghtT1+"\t"+r';slow purge,{IF NEWTOOL=1} T1'+"\t\t"+r';start tool switch 1,{IF NEWTOOL=1} G92 E0'+"\t\t"+r';reset t1,{IF NEWTOOL=1} G1 F3000 E-4.5'+"\t"+r';retract,{IF NEWTOOL=1} G1 F[travel_speed]'+"\t"+r';end tool switch,'+fanActionOnToolChange2+r',G91,G1 F[travel_speed] Z2,G90</toolChangeGcode>'+"\n"
            currentFirstLayerHeightPercentage = int(min(125, flowValue(currentNozzle, currentFilament)*100/(min(nozzleLeft, nozzleRight)*currentLayerHeight*(currentDefaultSpeed/60)*float(currentFirstLayerUnderspeed))))       
            currentPerimeterOutlines = max(2, int(round(quality['wallWidth'] / currentNozzle))) #2 minimum Perimeters needed
            currentTopSolidLayers = max(4, int(round(quality['topBottomWidth'] / currentLayerHeight))) #4 minimum layers needed
            currentBottomSolidLayers = currentTopSolidLayers
            currentRaftExtruder = currentPrimaryExtruder
            currentSkirtExtruder = currentPrimaryExtruder
            fff.append(r'  <autoConfigureQuality name="'+extruder+secondaryExtruderAction+str(quality['id'][2:])+r'">'+"\n")
            fff.append(r'    <globalExtrusionMultiplier>1</globalExtrusionMultiplier>'+"\n")
            fff.append(r'    <fanSpeed>'+"\n")
            fff.append(r'      <setpoint layer="1" speed="0" />'+"\n")
            fff.append(r'      <setpoint layer="2" speed="'+str(currentFilament['fanMultiplier']*100)+r'" />'+"\n")
            fff.append(r'    </fanSpeed>'+"\n")
            fff.append(r'    <filamentDiameter>'+str(currentFilament['filamentDiameter'])+r'</filamentDiameter>'+"\n")
            fff.append(r'    <filamentPricePerKg>'+str(currentFilament['filamentPricePerKg'])+r'</filamentPricePerKg>'+"\n")
            fff.append(r'    <filamentDensity>'+str(currentFilament['filamentDensity'])+r'</filamentDensity>'+"\n")
            if nozzleLeft != 'None':
                fff.append(r'    <extruder name="Left Extruder '+str(nozzleLeft)+r'">'+"\n")
                fff.append(r'      <toolheadNumber>0</toolheadNumber>'+"\n")
                fff.append(r'      <diameter>'+str(nozzleLeft)+r'</diameter>'+"\n")
                fff.append(r'      <autoWidth>0</autoWidth>'+"\n")
                fff.append(r'      <width>'+str(nozzleLeft)+r'</width>'+"\n")
                fff.append(r'      <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+r'</extrusionMultiplier>'+"\n")
                fff.append(r'      <useRetract>1</useRetract>'+"\n")
                fff.append(r'      <retractionDistance>'+str(filamentLeft['retractionDistance'])+r'</retractionDistance>'+"\n")
                fff.append(r'      <extraRestartDistance>0</extraRestartDistance>'+"\n")
                fff.append(r'      <retractionZLift>0.05</retractionZLift>'+"\n")
                fff.append(r'      <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+r'</retractionSpeed>'+"\n")
                fff.append(r'      <useCoasting>0</useCoasting>'+"\n")
                fff.append(r'      <coastingDistance>0.2</coastingDistance>'+"\n")
                fff.append(r'      <useWipe>0</useWipe>'+"\n")
                fff.append(r'      <wipeDistance>5</wipeDistance>'+"\n")
                fff.append(r'    </extruder>'+"\n")
            if nozzleRight != 'None':
                fff.append(r'    <extruder name="Right Extruder '+str(nozzleRight)+r'">'+"\n")
                fff.append(r'      <toolheadNumber>1</toolheadNumber>'+"\n")
                fff.append(r'      <diameter>'+str(nozzleRight)+r'</diameter>'+"\n")
                fff.append(r'      <autoWidth>0</autoWidth>'+"\n")
                fff.append(r'      <width>'+str(nozzleRight)+r'</width>'+"\n")
                fff.append(r'      <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+r'</extrusionMultiplier>'+"\n")
                fff.append(r'      <useRetract>1</useRetract>'+"\n")
                fff.append(r'      <retractionDistance>'+str(filamentRight['retractionDistance'])+r'</retractionDistance>'+"\n")
                fff.append(r'      <extraRestartDistance>0</extraRestartDistance>'+"\n")
                fff.append(r'      <retractionZLift>0.05</retractionZLift>'+"\n")
                fff.append(r'      <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+r'</retractionSpeed>'+"\n")
                fff.append(r'      <useCoasting>0</useCoasting>'+"\n")
                fff.append(r'      <coastingDistance>0.2</coastingDistance>'+"\n")
                fff.append(r'      <useWipe>0</useWipe>'+"\n")
                fff.append(r'      <wipeDistance>5</wipeDistance>'+"\n")
                fff.append(r'    </extruder>'+"\n")
            fff.append(r'    <primaryExtruder>'+str(currentPrimaryExtruder)+r'</primaryExtruder>'+"\n")
            fff.append(r'    <raftExtruder>'+str(currentRaftExtruder)+r'</raftExtruder>'+"\n")
            fff.append(r'    <skirtExtruder>'+str(currentSkirtExtruder)+r'</skirtExtruder>'+"\n")
            fff.append(r'    <infillExtruder>'+str(currentInfillExtruder)+r'</infillExtruder>'+"\n")
            fff.append(r'    <supportExtruder>'+str(currentSupportExtruder)+r'</supportExtruder>'+"\n")
            fff.append(r'    <generateSupport>'+str(currentGenerateSupport)+r'</generateSupport>'+"\n")
            fff.append(currentStartingGcode)
            fff.append(currentToolChangeGCode)
            fff.append(r'    <layerHeight>'+str(currentLayerHeight)+r'</layerHeight>'+"\n")
            fff.append(r'    <firstLayerHeightPercentage>'+str(currentFirstLayerHeightPercentage)+r'</firstLayerHeightPercentage>'+"\n")
            fff.append(r'    <topSolidLayers>'+str(currentTopSolidLayers)+r'</topSolidLayers>'+"\n")
            fff.append(r'    <bottomSolidLayers>'+str(currentBottomSolidLayers)+r'</bottomSolidLayers>'+"\n")
            fff.append(r'    <perimeterOutlines>'+str(currentPerimeterOutlines)+r'</perimeterOutlines>'+"\n")
            fff.append(r'    <infillPercentage>'+str(quality['infillPercentage'])+r'</infillPercentage>'+"\n")
            fff.append(r'    <infillLayerInterval>'+str(currentInfillLayerInterval)+r'</infillLayerInterval>'+"\n")
            fff.append(r'    <defaultSpeed>'+str(currentDefaultSpeed)+r'</defaultSpeed>'+"\n")
            fff.append(r'    <firstLayerUnderspeed>'+str(currentFirstLayerUnderspeed)+r'</firstLayerUnderspeed>'+"\n")
            fff.append(r'    <outlineUnderspeed>'+str(currentOutlineUnderspeed)+r'</outlineUnderspeed>'+"\n")
            fff.append(r'    <supportUnderspeed>'+str(currentSupportUnderspeed)+r'</supportUnderspeed>'+"\n")
            if nozzleLeft != 'None':
                fff.append(r'    <temperatureController name="Left Extruder '+str(nozzleLeft)+r'">'+"\n")
                fff.append(r'      <temperatureNumber>0</temperatureNumber>'+"\n")
                fff.append(r'      <isHeatedBed>0</isHeatedBed>'+"\n")
                fff.append(r'      <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
                fff.append(r'      <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
                fff.append(r'      <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
                fff.append(r'      <setpoint layer="1" temperature="'+str(nozzleLeftLayer1Temperature)+r'"/>'+"\n")
                if nozzleLeftLayer1Temperature != nozzleLeftLayer2Temperature:
                    fff.append(r'      <setpoint layer="2" temperature="'+str(nozzleLeftLayer2Temperature)+r'"/>'+"\n")
                fff.append(r'    </temperatureController>'+"\n")
            if nozzleRight != 'None':
                fff.append(r'    <temperatureController name="Right Extruder '+str(nozzleRight)+r'">'+"\n")
                fff.append(r'      <temperatureNumber>1</temperatureNumber>'+"\n")
                fff.append(r'      <isHeatedBed>0</isHeatedBed>'+"\n")
                fff.append(r'      <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
                fff.append(r'      <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
                fff.append(r'      <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
                fff.append(r'      <setpoint layer="1" temperature="'+str(nozzleRightLayer1Temperature)+r'"/>'+"\n")
                if nozzleRightLayer1Temperature != nozzleRightLayer2Temperature:
                    fff.append(r'      <setpoint layer="2" temperature="'+str(nozzleRightLayer2Temperature)+r'"/>'+"\n")
                fff.append(r'    </temperatureController>'+"\n")
            if (nozzleLeft != 'None' and filamentLeft['bedTemperature'] > 0) or (nozzleRight != 'None' and filamentRight['bedTemperature'] > 0):
                fff.append(r'    <temperatureController name="Heated Bed">'+"\n")
                fff.append(r'      <temperatureNumber>0</temperatureNumber>'+"\n")
                fff.append(r'      <isHeatedBed>1</isHeatedBed>'+"\n")
                fff.append(r'      <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
                fff.append(r'      <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
                fff.append(r'      <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
                fff.append(r'      <setpoint layer="1" temperature="'+str(currentBedTemperature)+r'"/>'+"\n")
                fff.append(r'    </temperatureController>'+"\n")
            fff.append(r'  </autoConfigureQuality>'+"\n")

            if dataLog != 'noData' :
                # Store flows, speeds, temperatures and other data
                writeData(extruder, currentDefaultSpeed, currentInfillLayerInterval, currentLayerHeight, nozzleLeft, nozzleRight, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder, filamentLeft, filamentRight, quality, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed, currentFirstLayerHeightPercentage, nozzleLeftLayer2Temperature, nozzleRightLayer2Temperature, currentBedTemperature, dataLog)                        

    # fff.append(r'  </autoConfigureMaterial>'+"\n")
    fff.append(r'  <autoConfigureExtruders name="IDEX Enabled"  allowedToolheads="2">'+"\n")
    if nozzleLeft != 'None':
        fff.append(r'    <toggleTemperatureController name="Left Extruder '+str(nozzleLeft)+r'" status="on" stabilize="on"/>'+"\n")
    if nozzleRight != 'None':
        fff.append(r'    <toggleTemperatureController name="Right Extruder '+str(nozzleRight)+r'" status="on" stabilize="on"/>'+"\n")
    if (nozzleLeft != 'None' and filamentLeft['bedTemperature'] > 0) or (nozzleRight != 'None' and filamentRight['bedTemperature'] > 0):
        fff.append(r'    <toggleTemperatureController name="Heated Bed" status="on" stabilize="on"/>'+"\n")
    fff.append(r'  </autoConfigureExtruders>'+"\n")
    fff.append(r'</profile>'+"\n")
    if createFile == 'fffFile':
        f = open(fileName+".fff", "w")
        f.writelines(fff)
        f.close()
    return fileName

def createProfileWithNestedFilaments(nozzleLeft, nozzleRight, dataLog, createFile):
    fff = []
    fff.append(r'<?xml version="1.0" encoding="utf-8"?>'+"\n")
    for q in profilesData['quality']:
        if q['id'][2:] == 'Medium':
            defaultPrintQualityBase = 'Medium'
            break
        else:
            defaultPrintQualityBase = profilesData['quality'][0]['id'][2:]
    for f in profilesData['filament']:
        if f['id'] == 'Colorfila PLA':
            defaultPrintMaterial = 'Colorfila PLA'
            break
        else:
            defaultPrintMaterial = profilesData['filament'][0]['id']
    filamentLeft = profilesData['filament'][0]
    filamentRight = profilesData['filament'][0]
    if nozzleLeft == 'None':
        fileName = "BCN3D Sigma - Right Extruder "+str(nozzleRight)+" Only"
        defaultPrintQuality = 'Right Extruder ('+defaultPrintMaterial+') - '+defaultPrintQualityBase
        extruderPrintOptions = ["Right Extruder"]
        filamentLeft = dict([('id', '')])
        if nozzleRight == 'None':
            return
    elif nozzleRight == 'None':
        fileName = "BCN3D Sigma - Left Extruder "+str(nozzleLeft)+" Only ("+filamentLeft['id']+")"
        defaultPrintQuality = 'Left Extruder ('+defaultPrintMaterial+') - '+defaultPrintQualityBase
        extruderPrintOptions = ["Left Extruder"]
        filamentRight = dict([('id', '')])
    else:
        fileName = "BCN3D Sigma - "+str(nozzleLeft)+" Left, "+str(nozzleRight)+" Right"
        defaultPrintMaterial = profilesData['filament'][0]['id']+' Left, '+profilesData['filament'][0]['id']+' Right'
        defaultPrintQuality = 'Left Extruder - '+defaultPrintQualityBase
        extruderPrintOptions = ["Left Extruder", "Right Extruder", "Both Extruders"]
    fff.append(r'<profile name="'+fileName+r'" version="'+time.strftime("%Y-%m-%d")+" "+time.strftime("%H:%M:%S")+r'" app="S3D-Software 3.1.1">'+"\n")    
    fff.append(r'  <baseProfile></baseProfile>'+"\n")
    fff.append(r'  <printMaterial>'+defaultPrintMaterial+'</printMaterial>'+"\n")
    fff.append(r'  <printQuality>'+defaultPrintQuality+'</printQuality>'+"\n") #+extruder+secondaryExtruderAction+str(quality['id'][2:])+
    fff.append(r'  <printExtruders></printExtruders>'+"\n")
    if nozzleLeft != 'None':
        fff.append(r'  <extruder name="Left Extruder '+str(nozzleLeft)+r'">'+"\n")
        fff.append(r'    <toolheadNumber>0</toolheadNumber>'+"\n")
        fff.append(r'    <diameter>'+str(nozzleLeft)+r'</diameter>'+"\n")
        fff.append(r'    <autoWidth>0</autoWidth>'+"\n")
        fff.append(r'    <width>'+str(nozzleLeft)+r'</width>'+"\n")
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
    if nozzleRight != 'None':
        fff.append(r'  <extruder name="Right Extruder '+str(nozzleRight)+r'">'+"\n")
        fff.append(r'    <toolheadNumber>1</toolheadNumber>'+"\n")
        fff.append(r'    <diameter>'+str(nozzleRight)+r'</diameter>'+"\n")
        fff.append(r'    <autoWidth>0</autoWidth>'+"\n")
        fff.append(r'    <width>'+str(nozzleRight)+r'</width>'+"\n")
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
    fff.append(r'  <startPointOption>2</startPointOption>'+"\n")
    fff.append(r'  <startPointOriginX>0</startPointOriginX>'+"\n")
    fff.append(r'  <startPointOriginY>0</startPointOriginY>'+"\n")
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
    fff.append(r'  <internalInfillPattern>Rectilinear</internalInfillPattern>'+"\n")
    fff.append(r'  <externalInfillPattern>Rectilinear</externalInfillPattern>'+"\n")
    fff.append(r'  <infillPercentage>20</infillPercentage>'+"\n")
    fff.append(r'  <outlineOverlapPercentage>25</outlineOverlapPercentage>'+"\n")
    fff.append(r'  <infillExtrusionWidthPercentage>100</infillExtrusionWidthPercentage>'+"\n")
    fff.append(r'  <minInfillLength>3</minInfillLength>'+"\n")
    fff.append(r'  <infillLayerInterval>1</infillLayerInterval>'+"\n")
    fff.append(r'  <infillAngles>45,-45</infillAngles>'+"\n")
    fff.append(r'  <overlapInfillAngles>0</overlapInfillAngles>'+"\n")
    fff.append(r'  <generateSupport>0</generateSupport>'+"\n")
    fff.append(r'  <supportExtruder>0</supportExtruder>'+"\n")
    fff.append(r'  <supportInfillPercentage>25</supportInfillPercentage>'+"\n")
    fff.append(r'  <supportExtraInflation>0</supportExtraInflation>'+"\n")
    fff.append(r'  <denseSupportLayers>5</denseSupportLayers>'+"\n")
    fff.append(r'  <denseSupportInfillPercentage>75</denseSupportInfillPercentage>'+"\n")
    fff.append(r'  <supportLayerInterval>1</supportLayerInterval>'+"\n")
    fff.append(r'  <supportHorizontalPartOffset>0.2</supportHorizontalPartOffset>'+"\n")
    fff.append(r'  <supportUpperSeparationLayers>1</supportUpperSeparationLayers>'+"\n")
    fff.append(r'  <supportLowerSeparationLayers>1</supportLowerSeparationLayers>'+"\n")
    fff.append(r'  <supportType>0</supportType>'+"\n")
    fff.append(r'  <supportGridSpacing>3</supportGridSpacing>'+"\n")
    fff.append(r'  <maxOverhangAngle>45</maxOverhangAngle>'+"\n")
    fff.append(r'  <supportAngles>0</supportAngles>'+"\n")
    if nozzleLeft != 'None':
        fff.append(r'  <temperatureController name="Left Extruder '+str(nozzleLeft)+r'">'+"\n")
        fff.append(r'    <temperatureNumber>0</temperatureNumber>'+"\n")
        fff.append(r'    <isHeatedBed>0</isHeatedBed>'+"\n")
        fff.append(r'    <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
        fff.append(r'    <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
        fff.append(r'    <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
        fff.append(r'    <setpoint layer="1" temperature="150"/>'+"\n")
        fff.append(r'  </temperatureController>'+"\n")
    if nozzleRight != 'None':
        fff.append(r'  <temperatureController name="Right Extruder '+str(nozzleRight)+r'">'+"\n")
        fff.append(r'    <temperatureNumber>1</temperatureNumber>'+"\n")
        fff.append(r'    <isHeatedBed>0</isHeatedBed>'+"\n")
        fff.append(r'    <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
        fff.append(r'    <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
        fff.append(r'    <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
        fff.append(r'    <setpoint layer="1" temperature="150"/>'+"\n")
        fff.append(r'  </temperatureController>'+"\n")
    if (nozzleLeft != 'None' and filamentLeft['bedTemperature'] > 0) or (nozzleRight != 'None' and filamentRight['bedTemperature'] > 0):
        fff.append(r'  <temperatureController name="Heated Bed">'+"\n")
        fff.append(r'    <temperatureNumber>0</temperatureNumber>'+"\n")
        fff.append(r'    <isHeatedBed>1</isHeatedBed>'+"\n")
        fff.append(r'    <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
        fff.append(r'    <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
        fff.append(r'    <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
        fff.append(r'    <setpoint layer="1" temperature="50"/>'+"\n")
        fff.append(r'  </temperatureController>'+"\n")
    fff.append(r'  <fanSpeed>'+"\n")
    fff.append(r'    <setpoint layer="1" speed="0" />'+"\n")
    fff.append(r'    <setpoint layer="2" speed="100"/>'+"\n")
    fff.append(r'  </fanSpeed>'+"\n")
    fff.append(r'  <blipFanToFullPower>0</blipFanToFullPower>'+"\n")
    fff.append(r'  <adjustSpeedForCooling>1</adjustSpeedForCooling>'+"\n")
    fff.append(r'  <minSpeedLayerTime>5</minSpeedLayerTime>'+"\n")
    fff.append(r'  <minCoolingSpeedSlowdown>20</minCoolingSpeedSlowdown>'+"\n")
    fff.append(r'  <increaseFanForCooling>0</increaseFanForCooling>'+"\n")
    fff.append(r'  <minFanLayerTime>45</minFanLayerTime>'+"\n")
    fff.append(r'  <maxCoolingFanSpeed>100</maxCoolingFanSpeed>'+"\n")
    fff.append(r'  <increaseFanForBridging>0</increaseFanForBridging>'+"\n")
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
    fff.append(r'  <endingGcode>M104 S0 T0,M104 S0 T1,M140 S0'+"\t\t"+r';heated bed heater off (if you have it),G91'+"\t\t"+r';relative positioning,G1 Y+10 F[travel_speed]'+"\t"+r';move Z up a bit and retract filament even more,G28 X0 Y0'+"\t\t"+r';move X/Y to min endstops so the head is out of the way,M84'+"\t\t"+r';steppers off,G90'+"\t\t"+r';absolute positioning,</endingGcode>'+"\n")
    fff.append(r'  <exportFileFormat>gcode</exportFileFormat>'+"\n")
    fff.append(r'  <celebration>0</celebration>'+"\n")
    fff.append(r'  <celebrationSong></celebrationSong>'+"\n")
    fff.append(r'  <postProcessing></postProcessing>'+"\n")
    fff.append(r'  <defaultSpeed>2400</defaultSpeed>'+"\n")
    fff.append(r'  <outlineUnderspeed>0.85</outlineUnderspeed>'+"\n")
    fff.append(r'  <solidInfillUnderspeed>0.85</solidInfillUnderspeed>'+"\n")
    fff.append(r'  <supportUnderspeed>0.9</supportUnderspeed>'+"\n")
    fff.append(r'  <rapidXYspeed>12000</rapidXYspeed>'+"\n")
    fff.append(r'  <rapidZspeed>1002</rapidZspeed>'+"\n")
    fff.append(r'  <minBridgingArea>50</minBridgingArea>'+"\n")
    fff.append(r'  <bridgingExtraInflation>0</bridgingExtraInflation>'+"\n")
    fff.append(r'  <bridgingExtrusionMultiplier>1</bridgingExtrusionMultiplier>'+"\n")
    fff.append(r'  <bridgingSpeedMultiplier>1</bridgingSpeedMultiplier>'+"\n")
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
    fff.append(r'  <retractBetweenLayers>0</retractBetweenLayers>'+"\n")
    fff.append(r'  <useRetractionMinTravel>1</useRetractionMinTravel>'+"\n")
    fff.append(r'  <retractionMinTravel>1.5</retractionMinTravel>'+"\n")
    fff.append(r'  <retractWhileWiping>1</retractWhileWiping>'+"\n")
    fff.append(r'  <onlyWipeOutlines>1</onlyWipeOutlines>'+"\n")
    fff.append(r'  <avoidCrossingOutline>0</avoidCrossingOutline>'+"\n")
    fff.append(r'  <maxMovementDetourFactor>3</maxMovementDetourFactor>'+"\n")
    fff.append(r'  <toolChangeRetractionDistance>8</toolChangeRetractionDistance>'+"\n")
    fff.append(r'  <toolChangeExtraRestartDistance>0</toolChangeExtraRestartDistance>'+"\n")
    fff.append(r'  <toolChangeRetractionSpeed>2400</toolChangeRetractionSpeed>'+"\n")
    fff.append(r'  <allowThinWallGapFill>1</allowThinWallGapFill>'+"\n")
    fff.append(r'  <thinWallAllowedOverlapPercentage>10</thinWallAllowedOverlapPercentage>'+"\n")
    fff.append(r'  <horizontalSizeCompensation>0</horizontalSizeCompensation>'+"\n")
    # fff.append(r'  <overridePrinterModels>1</overridePrinterModels>'+"\n")
    # fff.append(r'  <printerModelsOverride>zyyx3dprinter.stl</printerModelsOverride>'+"\n")
    for filamentLeft in sorted(profilesData['filament'], key=lambda k: k['id']):
        for filamentRight in sorted(profilesData['filament'], key=lambda k: k['id']):
            fff.append(r'  <autoConfigureMaterial name="'+str(filamentLeft['id'])+" Left, "+str(filamentRight['id'])+" Right"+r'">'+"\n")
            for extruder in extruderPrintOptions:
                for quality in sorted(profilesData['quality'], key=lambda k: k['id']):
                    currentInfillLayerInterval = 1
                    currentGenerateSupport = 0
                    # MEX
                    if extruder[0] == 'L' or extruder[0] == 'R':
                        if extruder[0] == 'L':
                            currentPrimaryExtruder = 0
                            currentFilament = filamentLeft
                            currentNozzle = nozzleLeft
                            nozzleLeftLayer1Temperature = currentFilament['printTemperature'][0]
                            nozzleLeftLayer2Temperature = currentFilament['printTemperature'][0]
                            nozzleRightLayer1Temperature = 150
                            nozzleRightLayer2Temperature = 0
                            currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'MEX Left')
                        else:
                            currentPrimaryExtruder = 1
                            currentFilament = filamentRight
                            currentNozzle = nozzleRight
                            nozzleLeftLayer1Temperature = 150
                            nozzleLeftLayer2Temperature = 0
                            nozzleRightLayer1Temperature = currentFilament['printTemperature'][0]
                            nozzleRightLayer2Temperature = currentFilament['printTemperature'][0]
                            currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'MEX Right')
                        currentPurgeSpeed, currentStartPurgeLenght, currentToolChangePurgeLenght = purgeValues(currentNozzle, currentFilament)
                        currentStartingGcode = r'      <startingGcode>G21'+"\t\t"+r';metric values,G90'+"\t\t"+r';absolute positioning,M82'+"\t\t"+r';set extruder to absolute mode,M107'+"\t\t"+r';start with the fan off,G28 X0 Y0'+"\t\t"+r';move X/Y to min endstops,G28 Z0'+"\t\t"+r';move Z to min endstops,T'+str(currentPrimaryExtruder)+"\t\t"+r';change to active toolhead,G92 E0'+"\t\t"+r';zero the extruded length,G1 Z5 F200'+"\t\t"+r';Safety Z axis movement,G1 F'+currentPurgeSpeed+' E'+currentStartPurgeLenght+"\t"+r';extrude '+currentStartPurgeLenght+r'mm of feed stock,G92 E0'+"\t\t"+r';zero the extruded length again,G1 F200 E-4'+"\t\t"+r';Retract before printing,G1 F[travel_speed],</startingGcode>'+"\n"
                        currentToolChangeGCode = r'      <toolChangeGcode/>'+"\n"
                        currentInfillExtruder = currentPrimaryExtruder
                        currentSupportExtruder = currentPrimaryExtruder
                        currentBedTemperature = currentFilament['bedTemperature']
                        if filamentLeft['id'] != filamentRight['id']:
                            secondaryExtruderAction = ' ('+currentFilament['id']+') - '
                        else:
                            secondaryExtruderAction = ' - '
                    # IDEX
                    else:
                        # IDEX, Support Material
                        if filamentLeft['isSupportMaterial'] != filamentRight['isSupportMaterial']:
                            currentGenerateSupport = 1
                            if filamentLeft['isSupportMaterial']:
                                currentPrimaryExtruder = 1
                                currentFilament = filamentRight
                                currentNozzle = nozzleRight
                                supportFilament = filamentLeft
                                supportNozzle = nozzleLeft
                                fanActionOnToolChange1 = '{IF NEWTOOL=0} M107'+"\t\t"+r';disable fan for support material,'
                                fanActionOnToolChange2 = '{IF NEWTOOL=1} M106'+"\t\t"+r';enable fan for part material,'
                                secondaryExtruderAction = ' (Left Ext. for supports) - '
                                currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'IDEX, Supports with Left')
                            else:
                                currentPrimaryExtruder = 0
                                currentFilament = filamentLeft
                                currentNozzle = nozzleLeft
                                supportFilament = filamentRight
                                supportNozzle = nozzleRight
                                fanActionOnToolChange1 = '{IF NEWTOOL=0} M106'+"\t\t"+r';enable fan for part material,'
                                fanActionOnToolChange2 = '{IF NEWTOOL=1} M107'+"\t\t"+r';disable fan for support material,' 
                                secondaryExtruderAction = ' (Right Ext. for supports) - '
                                currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'IDEX, Supports with Right')
                            currentInfillExtruder = currentPrimaryExtruder
                            currentSupportExtruder = abs(currentPrimaryExtruder-1)
                            nozzleLeftLayer1Temperature = filamentLeft['printTemperature'][0]
                            nozzleLeftLayer2Temperature = filamentLeft['printTemperature'][0]
                            nozzleRightLayer1Temperature = filamentRight['printTemperature'][0]
                            nozzleRightLayer2Temperature = filamentRight['printTemperature'][0]
                        # IDEX, Combined Infill
                        else:
                            fanActionOnToolChange1 = ''
                            fanActionOnToolChange2 = ''
                            if nozzleLeft <= nozzleRight:
                                currentPrimaryExtruder = 0
                                currentFilament = filamentLeft
                                currentNozzle = nozzleLeft
                                currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'IDEX, Infill with Right')
                                if nozzleLeft != nozzleRight:
                                    currentInfillLayerInterval = int(str(min(flowValue(nozzleRight, filamentRight)/(max(nozzleLeft, nozzleRight)*currentDefaultSpeed/60*quality['layerHeightMultiplier']*min(nozzleLeft, nozzleRight)),(max(nozzleLeft, nozzleRight)*0.75)/(quality['layerHeightMultiplier']*min(nozzleLeft, nozzleRight)))).split('.')[0])
                                nozzleLeftLayer1Temperature = filamentLeft['printTemperature'][0]
                                nozzleLeftLayer2Temperature = filamentLeft['printTemperature'][0]
                                nozzleRightLayer1Temperature = filamentRight['printTemperature'][1]
                                nozzleRightLayer2Temperature = filamentRight['printTemperature'][1]
                                secondaryExtruderAction = ' (Right Ext. for infill) - '
                                if currentFilament['fanMultiplier'] != 0:
                                    fanActionOnToolChange1 = '{IF NEWTOOL=0} M106'+"\t\t"+r';enable fan for perimeters,'
                                    fanActionOnToolChange2 = '{IF NEWTOOL=1} M107'+"\t\t"+r';disable fan for infill,'
                                if nozzleLeft == nozzleRight:
                                    nozzleRightLayer1Temperature = filamentRight['printTemperature'][0]
                                    nozzleRightLayer2Temperature = filamentRight['printTemperature'][0]
                            else:
                                currentPrimaryExtruder = 1
                                currentFilament = filamentRight
                                currentNozzle = nozzleRight
                                currentDefaultSpeed, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed = speedValues(nozzleLeft, nozzleRight, filamentLeft, filamentRight, quality, 'IDEX, Infill with Left')
                                currentInfillLayerInterval = int(str(min(flowValue(nozzleLeft, filamentLeft)/(max(nozzleLeft, nozzleRight)*currentDefaultSpeed/60*quality['layerHeightMultiplier']*min(nozzleLeft, nozzleRight)),(max(nozzleLeft, nozzleRight)*0.75)/(quality['layerHeightMultiplier']*min(nozzleLeft, nozzleRight)))).split('.')[0])
                                nozzleLeftLayer1Temperature = filamentLeft['printTemperature'][1]
                                nozzleLeftLayer2Temperature = filamentLeft['printTemperature'][1]
                                nozzleRightLayer1Temperature = filamentRight['printTemperature'][0]
                                nozzleRightLayer2Temperature = filamentRight['printTemperature'][0]
                                secondaryExtruderAction = ' (Left Ext. for infill) - '
                                if currentFilament['fanMultiplier'] != 0:
                                    fanActionOnToolChange1 = '{IF NEWTOOL=0} M107'+"\t\t"+r';disable fan for infill,'
                                    fanActionOnToolChange2 = '{IF NEWTOOL=1} M106'+"\t\t"+r';enable fan for perimeters,'
                            currentInfillExtruder = abs(currentPrimaryExtruder-1)
                            currentSupportExtruder = currentPrimaryExtruder
                        currentBedTemperature = max(filamentLeft['bedTemperature'], filamentRight['bedTemperature'])
                        currentPurgeSpeedT0, currentStartPurgeLenghtT0, currentToolChangePurgeLenghtT0 = purgeValues(nozzleLeft, filamentLeft)
                        currentPurgeSpeedT1, currentStartPurgeLenghtT1, currentToolChangePurgeLenghtT1 = purgeValues(nozzleRight, filamentRight)       
                        currentStartingGcode = r'      <startingGcode>G21'+"\t\t"+r';metric values,G90'+"\t\t"+r';absolute positioning,M107'+"\t\t"+r';start with the fan off,G28 X0 Y0'+"\t\t"+r';move X/Y to min endstops,G28 Z0'+"\t\t"+r';move Z to min endstops,T1'+"\t\t"+r';Switch to the 2nd extruder,G92 E0'+"\t\t"+r';zero the extruded length,G1 F'+currentPurgeSpeedT1+' E'+currentStartPurgeLenghtT1+"\t"+r';extrude '+currentStartPurgeLenghtT1+r'mm of feed stock,G92 E0'+"\t\t"+r';zero the extruded length again,G1 F200 E-9,T0'+"\t\t"+r';Switch to the first extruder,G92 E0'+"\t\t"+r';zero the extruded length,G1 F'+currentPurgeSpeedT0+' E'+currentStartPurgeLenghtT0+"\t"+r';extrude '+currentStartPurgeLenghtT0+r'mm of feed stock,G92 E0'+"\t\t"+r';zero the extruded length again,G1 Z5 F200'+"\t\t"+r';Safety Z axis movement,G1 F[travel_speed]</startingGcode>'+"\n"              
                        currentToolChangeGCode = r'      <toolChangeGcode>{IF NEWTOOL=0} T0'+"\t\t"+r';start tool switch 0,;{IF NEWTOOL=0} G1 X0 Y0 F[travel_speed]'+"\t"+r';travel,{IF NEWTOOL=0} G1 F500 E-0.5'+"\t\t"+r';fast purge,{IF NEWTOOL=0} G1 F'+currentPurgeSpeedT0+' E'+currentToolChangePurgeLenghtT0+"\t"+r';slow purge,{IF NEWTOOL=0} G92 E0'+"\t\t"+r';reset t0,{IF NEWTOOL=0} G1 F3000 E-4.5'+"\t"+r';retract,{IF NEWTOOL=0} G1 F[travel_speed]'+"\t"+r';end tool switch,'+fanActionOnToolChange1+r',{IF NEWTOOL=1} T1'+"\t\t"+r';start tool switch 1,;{IF NEWTOOL=1} G1 X210 Y0 F[travel_speed]'+"\t"+r';travel,{IF NEWTOOL=1} G1 F500 E-0.5'+"\t\t"+r';fast purge,{IF NEWTOOL=1} G1 F'+currentPurgeSpeedT1+' E'+currentToolChangePurgeLenghtT1+"\t"+r';slow purge,{IF NEWTOOL=1} T1'+"\t\t"+r';start tool switch 1,{IF NEWTOOL=1} G92 E0'+"\t\t"+r';reset t1,{IF NEWTOOL=1} G1 F3000 E-4.5'+"\t"+r';retract,{IF NEWTOOL=1} G1 F[travel_speed]'+"\t"+r';end tool switch,'+fanActionOnToolChange2+r',G91,G1 F[travel_speed] Z2,G90</toolChangeGcode>'+"\n"
                    currentLayerHeight = currentNozzle * quality['layerHeightMultiplier']
                    currentFirstLayerHeightPercentage = int(min(125, flowValue(currentNozzle, currentFilament)*100/(min(nozzleLeft, nozzleRight)*currentLayerHeight*(currentDefaultSpeed/60)*float(currentFirstLayerUnderspeed))))       
                    currentPerimeterOutlines = max(2, int(round(quality['wallWidth'] / currentNozzle))) #2 minimum Perimeters needed
                    currentTopSolidLayers = max(4, int(round(quality['topBottomWidth'] / currentLayerHeight))) #4 minimum layers needed
                    currentBottomSolidLayers = currentTopSolidLayers
                    currentRaftExtruder = currentPrimaryExtruder
                    currentSkirtExtruder = currentPrimaryExtruder
                    fff.append(r'    <autoConfigureQuality name="'+extruder+' - '+str(quality['id'][2:])+r'">'+"\n")
                    # fff.append(r'    <autoConfigureQuality name="'+extruder+secondaryExtruderAction+str(quality['id'][2:])+r'">'+"\n")
                    fff.append(r'      <globalExtrusionMultiplier>1</globalExtrusionMultiplier>'+"\n")
                    fff.append(r'      <fanSpeed>'+"\n")
                    fff.append(r'        <setpoint layer="1" speed="0" />'+"\n")
                    fff.append(r'        <setpoint layer="2" speed="'+str(currentFilament['fanMultiplier']*100)+r'" />'+"\n")
                    fff.append(r'      </fanSpeed>'+"\n")
                    fff.append(r'      <filamentDiameter>'+str(currentFilament['filamentDiameter'])+r'</filamentDiameter>'+"\n")
                    fff.append(r'      <filamentPricePerKg>'+str(currentFilament['filamentPricePerKg'])+r'</filamentPricePerKg>'+"\n")
                    fff.append(r'      <filamentDensity>'+str(currentFilament['filamentDensity'])+r'</filamentDensity>'+"\n")
                    if nozzleLeft != 'None':
                        fff.append(r'      <extruder name="Left Extruder '+str(nozzleLeft)+r'">'+"\n")
                        fff.append(r'        <toolheadNumber>0</toolheadNumber>'+"\n")
                        fff.append(r'        <diameter>'+str(nozzleLeft)+r'</diameter>'+"\n")
                        fff.append(r'        <autoWidth>0</autoWidth>'+"\n")
                        fff.append(r'        <width>'+str(nozzleLeft)+r'</width>'+"\n")
                        fff.append(r'        <extrusionMultiplier>'+str(filamentLeft['extrusionMultiplier'])+r'</extrusionMultiplier>'+"\n")
                        fff.append(r'        <useRetract>1</useRetract>'+"\n")
                        fff.append(r'        <retractionDistance>'+str(filamentLeft['retractionDistance'])+r'</retractionDistance>'+"\n")
                        fff.append(r'        <extraRestartDistance>0</extraRestartDistance>'+"\n")
                        fff.append(r'        <retractionZLift>0.05</retractionZLift>'+"\n")
                        fff.append(r'        <retractionSpeed>'+str(filamentLeft['retractionSpeed']*60)+r'</retractionSpeed>'+"\n")
                        fff.append(r'        <useCoasting>0</useCoasting>'+"\n")
                        fff.append(r'        <coastingDistance>0.2</coastingDistance>'+"\n")
                        fff.append(r'        <useWipe>0</useWipe>'+"\n")
                        fff.append(r'        <wipeDistance>5</wipeDistance>'+"\n")
                        fff.append(r'      </extruder>'+"\n")
                    if nozzleRight != 'None':
                        fff.append(r'      <extruder name="Right Extruder '+str(nozzleRight)+r'">'+"\n")
                        fff.append(r'        <toolheadNumber>1</toolheadNumber>'+"\n")
                        fff.append(r'        <diameter>'+str(nozzleRight)+r'</diameter>'+"\n")
                        fff.append(r'        <autoWidth>0</autoWidth>'+"\n")
                        fff.append(r'        <width>'+str(nozzleRight)+r'</width>'+"\n")
                        fff.append(r'        <extrusionMultiplier>'+str(filamentRight['extrusionMultiplier'])+r'</extrusionMultiplier>'+"\n")
                        fff.append(r'        <useRetract>1</useRetract>'+"\n")
                        fff.append(r'        <retractionDistance>'+str(filamentRight['retractionDistance'])+r'</retractionDistance>'+"\n")
                        fff.append(r'        <extraRestartDistance>0</extraRestartDistance>'+"\n")
                        fff.append(r'        <retractionZLift>0.05</retractionZLift>'+"\n")
                        fff.append(r'        <retractionSpeed>'+str(filamentRight['retractionSpeed']*60)+r'</retractionSpeed>'+"\n")
                        fff.append(r'        <useCoasting>0</useCoasting>'+"\n")
                        fff.append(r'        <coastingDistance>0.2</coastingDistance>'+"\n")
                        fff.append(r'        <useWipe>0</useWipe>'+"\n")
                        fff.append(r'        <wipeDistance>5</wipeDistance>'+"\n")
                        fff.append(r'      </extruder>'+"\n")
                    fff.append(r'      <primaryExtruder>'+str(currentPrimaryExtruder)+r'</primaryExtruder>'+"\n")
                    fff.append(r'      <raftExtruder>'+str(currentRaftExtruder)+r'</raftExtruder>'+"\n")
                    fff.append(r'      <skirtExtruder>'+str(currentSkirtExtruder)+r'</skirtExtruder>'+"\n")
                    fff.append(r'      <infillExtruder>'+str(currentInfillExtruder)+r'</infillExtruder>'+"\n")
                    fff.append(r'      <supportExtruder>'+str(currentSupportExtruder)+r'</supportExtruder>'+"\n")
                    fff.append(r'      <generateSupport>'+str(currentGenerateSupport)+r'</generateSupport>'+"\n")
                    fff.append(currentStartingGcode)
                    fff.append(currentToolChangeGCode)
                    fff.append(r'      <layerHeight>'+str(currentLayerHeight)+r'</layerHeight>'+"\n")
                    fff.append(r'      <firstLayerHeightPercentage>'+str(currentFirstLayerHeightPercentage)+r'</firstLayerHeightPercentage>'+"\n")
                    fff.append(r'      <topSolidLayers>'+str(currentTopSolidLayers)+r'</topSolidLayers>'+"\n")
                    fff.append(r'      <bottomSolidLayers>'+str(currentBottomSolidLayers)+r'</bottomSolidLayers>'+"\n")
                    fff.append(r'      <perimeterOutlines>'+str(currentPerimeterOutlines)+r'</perimeterOutlines>'+"\n")
                    fff.append(r'      <infillPercentage>'+str(quality['infillPercentage'])+r'</infillPercentage>'+"\n")
                    fff.append(r'      <infillLayerInterval>'+str(currentInfillLayerInterval)+r'</infillLayerInterval>'+"\n")
                    fff.append(r'      <defaultSpeed>'+str(currentDefaultSpeed)+r'</defaultSpeed>'+"\n")
                    fff.append(r'      <firstLayerUnderspeed>'+str(currentFirstLayerUnderspeed)+r'</firstLayerUnderspeed>'+"\n")
                    fff.append(r'      <outlineUnderspeed>'+str(currentOutlineUnderspeed)+r'</outlineUnderspeed>'+"\n")
                    fff.append(r'      <supportUnderspeed>'+str(currentSupportUnderspeed)+r'</supportUnderspeed>'+"\n")
                    if nozzleLeft != 'None':
                        fff.append(r'      <temperatureController name="Left Extruder '+str(nozzleLeft)+r'">'+"\n")
                        fff.append(r'        <temperatureNumber>0</temperatureNumber>'+"\n")
                        fff.append(r'        <isHeatedBed>0</isHeatedBed>'+"\n")
                        fff.append(r'        <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
                        fff.append(r'        <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
                        fff.append(r'        <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
                        fff.append(r'        <setpoint layer="1" temperature="'+str(nozzleLeftLayer1Temperature)+r'"/>'+"\n")
                        if nozzleLeftLayer1Temperature != nozzleLeftLayer2Temperature:
                            fff.append(r'        <setpoint layer="2" temperature="'+str(nozzleLeftLayer2Temperature)+r'"/>'+"\n")
                        fff.append(r'      </temperatureController>'+"\n")
                    if nozzleRight != 'None':
                        fff.append(r'      <temperatureController name="Right Extruder '+str(nozzleRight)+r'">'+"\n")
                        fff.append(r'        <temperatureNumber>1</temperatureNumber>'+"\n")
                        fff.append(r'        <isHeatedBed>0</isHeatedBed>'+"\n")
                        fff.append(r'        <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
                        fff.append(r'        <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
                        fff.append(r'        <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
                        fff.append(r'        <setpoint layer="1" temperature="'+str(nozzleRightLayer1Temperature)+r'"/>'+"\n")
                        if nozzleRightLayer1Temperature != nozzleRightLayer2Temperature:
                            fff.append(r'        <setpoint layer="2" temperature="'+str(nozzleRightLayer2Temperature)+r'"/>'+"\n")
                        fff.append(r'      </temperatureController>'+"\n")
                    if (nozzleLeft != 'None' and filamentLeft['bedTemperature'] > 0) or (nozzleRight != 'None' and filamentRight['bedTemperature'] > 0):
                        fff.append(r'      <temperatureController name="Heated Bed">'+"\n")
                        fff.append(r'        <temperatureNumber>0</temperatureNumber>'+"\n")
                        fff.append(r'        <isHeatedBed>1</isHeatedBed>'+"\n")
                        fff.append(r'        <relayBetweenLayers>0</relayBetweenLayers>'+"\n")
                        fff.append(r'        <relayBetweenLoops>0</relayBetweenLoops>'+"\n")
                        fff.append(r'        <stabilizeAtStartup>1</stabilizeAtStartup>'+"\n")
                        fff.append(r'        <setpoint layer="1" temperature="'+str(currentBedTemperature)+r'"/>'+"\n")
                        fff.append(r'      </temperatureController>'+"\n")
                    fff.append(r'    </autoConfigureQuality>'+"\n")

                    if dataLog != 'noData' :
                        # Store flows, speeds, temperatures and other data
                        writeData(extruder, currentDefaultSpeed, currentInfillLayerInterval, currentLayerHeight, nozzleLeft, nozzleRight, currentPrimaryExtruder, currentInfillExtruder, currentSupportExtruder, filamentLeft, filamentRight, quality, currentFirstLayerUnderspeed, currentOutlineUnderspeed, currentSupportUnderspeed, currentFirstLayerHeightPercentage, nozzleLeftLayer2Temperature, nozzleRightLayer2Temperature, currentBedTemperature, dataLog)                        

            fff.append(r'  </autoConfigureMaterial>'+"\n")
    fff.append(r'  <autoConfigureExtruders name="IDEX Enabled"  allowedToolheads="2">'+"\n")
    # if nozzleLeft != 'None':
    #     fff.append(r'    <toggleTemperatureController name="Left Extruder '+str(nozzleLeft)+r'" status="on" stabilize="on"/>'+"\n")
    # if nozzleRight != 'None':
    #     fff.append(r'    <toggleTemperatureController name="Right Extruder '+str(nozzleRight)+r'" status="on" stabilize="on"/>'+"\n")
    # if (nozzleLeft != 'None' and filamentLeft['bedTemperature'] > 0) or (nozzleRight != 'None' and filamentRight['bedTemperature'] > 0):
    #     fff.append(r'    <toggleTemperatureController name="Heated Bed" status="on" stabilize="on"/>'+"\n")
    fff.append(r'  </autoConfigureExtruders>'+"\n")
    fff.append(r'</profile>'+"\n")
    if createFile == 'fffFile':
        f = open(fileName+".fff", "w")
        f.writelines(fff)
        f.close()
    return fileName

def createProfilesBundle(dataLog, profilesCreatedCount):
    sys.stdout.write('\n Working') 
    for f in os.listdir('.'):
        if f == "BCN3D Sigma - Simplify3D Profiles temp":
            shutil.rmtree("BCN3D Sigma - Simplify3D Profiles temp")
    os.mkdir("BCN3D Sigma - Simplify3D Profiles temp")
    os.chdir("BCN3D Sigma - Simplify3D Profiles temp")
    for nozzleLeft in profilesData['nozzle']:
        if nozzleLeft != 'None':
            os.mkdir("Left Hotend "+str(nozzleLeft))
            os.chdir("Left Hotend "+str(nozzleLeft))
        else:            
            os.mkdir("No Left Hotend")
            os.chdir("No Left Hotend")
        for nozzleRight in profilesData['nozzle']:
            if nozzleRight != 'None':
                os.mkdir("Right Hotend "+str(nozzleRight))
                os.chdir("Right Hotend "+str(nozzleRight))
            else:                
                os.mkdir("No Right Hotend")
                os.chdir("No Right Hotend")
            for filamentLeft in sorted(profilesData['filament'], key=lambda k: k['id']):
                for filamentRight in sorted(profilesData['filament'], key=lambda k: k['id']):
                    createProfile(nozzleLeft, nozzleRight, filamentLeft, filamentRight, dataLog, 'fffFile')
                    profilesCreatedCount += 1
            os.chdir('..')
        os.chdir('..')
        sys.stdout.flush()
        sys.stdout.write('.') 
    csv = open("BCN3D Sigma - Simplify3D Profiles.csv", "w")
    csv.writelines(dataLog)
    csv.close()
    os.chdir('..')
    shutil.make_archive('BCN3D Sigma - Simplify3D Profiles', 'zip', 'BCN3D Sigma - Simplify3D Profiles temp')
    shutil.rmtree("BCN3D Sigma - Simplify3D Profiles temp")
    print(" Your bundle 'BCN3D Sigma - Simplify3D Profiles.zip' is ready. Enjoy!\n")
    return profilesCreatedCount

def testAllCombinations():
    sys.stdout.write('\n Working')
    combinationCount = 0
    for nozzleLeft in profilesData['nozzle']:
        for nozzleRight in profilesData['nozzle']:
            for filamentLeft in sorted(profilesData['filament'], key=lambda k: k['id']):
                for filamentRight in sorted(profilesData['filament'], key=lambda k: k['id']):
                    createProfile(nozzleLeft, nozzleRight, filamentLeft, filamentRight, 'noData', 'noFile')
                    combinationCount += 1
        sys.stdout.flush()
        sys.stdout.write('.') 
    print ' All '+str(combinationCount)+' profiles can be generated!\n'

def selectNozzleSizeAndFilament(extruder):
                print "\n Select Sigma's "+extruder+" Extruder Nozzle Size (1-"+str(len(profilesData['nozzle']))+'):'
                answer0 = ''
                nozzleOptions = []
                for c in range(len(profilesData['nozzle'])):
                    nozzleOptions.append(str(c+1))
                materialOptions = []
                for c in range(len(profilesData['filament'])):
                    materialOptions.append(str(c+1))
                for size in range(len(profilesData['nozzle'])):
                    if profilesData['nozzle'][size] != 'None':
                        print ' '+str(size+1)+'. '+str(profilesData['nozzle'][size])+'mm'
                    else:
                        print ' '+str(size+1)+'. '+str(profilesData['nozzle'][size])
                while answer0 not in nozzleOptions:
                    answer0 = raw_input(' ')
                if profilesData['nozzle'][int(answer0)-1] != 'None':
                    print ' '+extruder+' Extruder Nozzle Size: '+str(profilesData['nozzle'][int(answer0)-1])+'mm.'
                    print "\n Select Sigma's "+extruder+" Extruder Loaded Filament (1-"+str(len(profilesData['filament']))+'):'
                    answer1 = ''
                    for material in range(len(profilesData['filament'])):
                        print ' '+str(material+1)+'. '+str(sorted(profilesData['filament'], key=lambda k: k['id'])[material]['id'])
                    while answer1 not in materialOptions:
                        answer1 = raw_input(' ')
                    print ' '+extruder+' Extruder Filament: '+sorted(profilesData['filament'], key=lambda k: k['id'])[int(answer1)-1]['id']+'.'
                else:
                    print ' '+extruder+' Extruder Nozzle Size: '+str(profilesData['nozzle'][int(answer0)-1])
                    answer1 = '1'
                return (answer0, answer1)

def printAvailableOptions():
    print '\n Available Nozzle Size(s):',
    for n in sorted(profilesData['nozzle']):
        if n != sorted(profilesData['nozzle'])[len(profilesData['nozzle'])-1]:
            if type(n) == float:
                print str(n)+'mm,',
            else:
                print n+',',
        else:
            if type(n) == float:
                print str(n)+'mm.'
            else:
                print n+'.'
    print ' Available Filament(s):',
    for n in sorted(profilesData['filament'], key=lambda k: k['id']):
        if n != sorted(profilesData['filament'], key=lambda k: k['id'])[len(profilesData['filament'])-1]:
            print n['id']+',',
        else:
            print n['id']+'.'

    print ' Available Quality Preconfiguration(s):',
    for n in sorted(profilesData['quality'], key=lambda k: k['id']):
        if n != sorted(profilesData['quality'], key=lambda k: k['id'])[len(profilesData['quality'])-1]:
            print n['id'][2:]+',',
        else:
            print n['id'][2:]+'.'
    print " Add, remove options or change its own parameters by editing 'ProfilesData.json' file.\n"

def main():
    print '\n Welcome to the BCN3D Sigma Profile Generator for Simplify3D \n'
    while True:
        print ' Choose your option (1-5):'
        print ' 1. Generate a bundle of profiles'
        print ' 2. Generate one single profile'
        print ' 3. Show available options'
        print ' 4. Test all combinations'
        print ' 5. Exit'
        x = 'x'
        y = 'y'
        dataLog = ["LFilament;RFilament;Extruder;Quality;LNozzle;RNozzle;InfillExt;PrimaryExt;SupportExt;LFlow;RFlow;Layers/Infill;DefaultSpeed;FirstLayerUnderspeed;OutLineUnderspeed;SupportUnderspeed;FirstLayerHeightPercentage;LTemp;RTemp;BTemp;\n"]
        profilesCreatedCount = 0
        while x not in '12345':
            x = raw_input(' ')
        if x in '12':
            if x == '1':
                profilesCreatedCount = createProfilesBundle(dataLog, profilesCreatedCount)
            elif x == '2':
                a = selectNozzleSizeAndFilament('Left')
                b = selectNozzleSizeAndFilament('Right')
                if profilesData['nozzle'][int(a[0])-1] == 'None' and profilesData['nozzle'][int(b[0])-1] == 'None':
                    print "\n Select at least one nozzle size to create a profile.\n"
                else:
                    print "\n Your new profile '"+createProfile(profilesData['nozzle'][int(a[0])-1], profilesData['nozzle'][int(b[0])-1], sorted(profilesData['filament'], key=lambda k: k['id'])[int(a[1])-1], sorted(profilesData['filament'], key=lambda k: k['id'])[int(b[1])-1], dataLog, 'fffFile')+".fff' has been created.\n"
                    profilesCreatedCount = 1
            print ' See profile(s) data? (Y/n)'
            while y not in ['Y', 'n']:
                y = raw_input(' ')
            if y == 'Y':
                for l in dataLog:
                    print '',
                    for d in string.split(l, ';'):
                        print string.rjust(str(d)[:6], 6),
                print ' '+str(profilesCreatedCount)+' profile(s) created with '+str(len(dataLog)-1)+' configurations.\n'
        elif x == '3':
            printAvailableOptions()
        elif x == '4':
            testAllCombinations()
        elif x == '5':
            print '\n Until next time!\n'
            break

if __name__ == '__main__':
    main() 