#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - Oct 2017
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

import os
import json
import time
import string

def init():
    # Generic
    global progenVersionNumber
    progenVersionNumber = '2.1.0'
    global progenBuildNumber
    progenBuildNumber = time.strftime("%d")+string.uppercase[int(time.strftime("%m"))]+string.uppercase[int(time.strftime("%y")[-1])]+time.strftime("%H")+time.strftime("%M")
    global profilesData
    profilesData = readProfilesData()
    global loggedData
    loggedData = ["LFilament;RFilament;Extruder;Quality;LNozzle;RNozzle;InfillExt;PrimaryExt;SupportExt;LFlow;RFlow;Layers/Infill;DefaultSpeed;FirstLayerUnderspeed;OutLineUnderspeed;SupportUnderspeed;FirstLayerHeightPercentage;LTemp;RTemp;BTemp;\n"]

    global cura2PostProcessingPluginName
    cura2PostProcessingPluginName = 'Sigma Vitamins'

def readProfilesData():
    profilesData = dict([("machine", []), ("hotend", []), ("filament", []), ("quality", [])])
    for machine in os.listdir('./resources/machines'):
        if machine[-5:] == '.json':
            with open('./resources/machines/'+machine) as machine_file:    
                machineData = json.load(machine_file)
                profilesData['machine'].append(machineData)
    for hotend in os.listdir('./resources/hotends'):
        if hotend[-5:] == '.json':
            with open('./resources/hotends/'+hotend) as hotend_file:    
                hotendData = json.load(hotend_file)
                profilesData['hotend'].append(hotendData)
    profilesData['hotend'].append(dict([('id', 'None')]))
    for filament in os.listdir('./resources/filaments'):
        if filament[-5:] == '.json':
            with open('./resources/filaments/'+filament) as filament_file:    
                filamentData = json.load(filament_file)
                profilesData['filament'].append(filamentData)
    for quality in os.listdir('./resources/quality'):
        if quality[-5:] == '.json':
            with open('./resources/quality/'+quality) as quality_file:    
                qualityData = json.load(quality_file)
                profilesData['quality'].append(qualityData)
    return profilesData