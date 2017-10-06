#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - May 2017
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

import os
import json
import time
import string

def init():
    # Generic
    global progenVersionNumber
    progenVersionNumber = '2.0.1'
    global progenBuildNumber
    progenBuildNumber = time.strftime("%d")+string.uppercase[int(time.strftime("%m"))]+string.uppercase[int(time.strftime("%y")[-1])]+time.strftime("%H")+time.strftime("%M")
    global profilesData
    profilesData = readProfilesData()
    global loggedData
    loggedData = ["LFilament;RFilament;Extruder;Quality;LNozzle;RNozzle;InfillExt;PrimaryExt;SupportExt;LFlow;RFlow;Layers/Infill;DefaultSpeed;FirstLayerUnderspeed;OutLineUnderspeed;SupportUnderspeed;FirstLayerHeightPercentage;LTemp;RTemp;BTemp;\n"]

    # Cura 2
    global cura2id
    cura2id = 'bcn3dsigma'
    global cura2Name
    cura2Name = 'Sigma'
    global cura2Manufacturer
    cura2Manufacturer = 'BCN3D Technologies'
    global cura2Category
    cura2Category = 'BCN3D Technologies'
    global cura2Author
    cura2Author = 'Guillem'
    global cura2PostProcessingPluginName
    cura2PostProcessingPluginName = 'Sigma Vitamins'
    global machineSettingsPluginName
    machineSettingsPluginName = 'SigmaSettingsAction'

def readProfilesData():
    profilesData = dict([("hotend", []), ("filament", []), ("quality", [])])
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