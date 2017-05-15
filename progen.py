#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - May 2017
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

SigmaProgenVersion = '2.0.0'
# Version Changelog
# - Internal structure major changes
# - SmartPurge activated by default. Needs Firmware v01-1.2.3
# - Cura 2 integration (under experimental features)
# - Raft improvements

# ToDo:
# - check variables consistency (cura2id etc)
# - Make ProfileTester
# - add Cura2 to ProfileTester
# - update readme
# - document version changes


import os
import json
import platform
import sys

from progen import ProfileMaker
from progen import ProgenEngine
from progen import Logger

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
                    ProgenEngine.simplify3DProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, '--no-data', engineData)
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
                        ProgenEngine.curaProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, '--no-data', engineData)
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
            leftHotend = sys.argv[1]+'.json' in os.listdir('./resources/hotends') or sys.argv[1] == 'None'
            rightHontend = sys.argv[2]+'.json' in os.listdir('./resources/hotends') or sys.argv[2] == 'None'
            leftFilament = sys.argv[3]+'.json' in os.listdir('./resources/filaments') or (sys.argv[1] == 'None' and sys.argv[3] == 'None')
            rightFilament = sys.argv[4]+'.json' in os.listdir('./resources/filaments') or (sys.argv[2] == 'None' and sys.argv[4] == 'None')
            quality = sys.argv[5]+'.json' in os.listdir('./resources/quality')
            if len(sys.argv) == 8:
                fileAction = sys.argv[6] == '--no-file' or sys.argv[6] == '--only-filename'
                return leftHotend and rightHontend and leftFilament and rightFilament and quality and fileAction
            else:
                return leftHotend and rightHontend and leftFilament and rightFilament and quality
        elif sys.argv[-1] == '--simplify3d' and (len(sys.argv) == 6 or len(sys.argv) == 7):
            leftHotend = sys.argv[1]+'.json' in os.listdir('./resources/hotends') or sys.argv[1] == 'None'
            rightHontend = sys.argv[2]+'.json' in os.listdir('./resources/hotends') or sys.argv[2] == 'None'
            leftFilament = sys.argv[3]+'.json' in os.listdir('./resources/filaments') or (sys.argv[1] == 'None' and sys.argv[3] == 'None')
            rightFilament = sys.argv[4]+'.json' in os.listdir('./resources/filaments') or (sys.argv[2] == 'None' and sys.argv[4] == 'None')       
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

def clearDisplay():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def main():
    readProfilesData()
    global engineData
    engineData = (profilesData, SigmaProgenVersion)
    if platform.system() == 'Windows':
        # os.system('color f0')
        os.system('mode con: cols=154 lines=35')
    if validArguments():
        for hotend in os.listdir('./resources/hotends'):
            if hotend == sys.argv[1]+'.json':
                with open('./resources/hotends/'+hotend) as hotend_file:    
                    leftHotend = json.load(hotend_file)
            if hotend == sys.argv[2]+'.json':
                with open('./resources/hotends/'+hotend) as hotend_file:    
                    rightHotend = json.load(hotend_file)
        for filament in os.listdir('./resources/filaments'):
            if filament == sys.argv[3]+'.json':
                with open('./resources/filaments/'+filament) as filament_file:    
                    leftFilament = json.load(filament_file)
            if filament == sys.argv[4]+'.json':
                with open('./resources/filaments/'+filament) as filament_file:    
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
                    ProfileMaker.simplify3D(leftHotend, rightHotend, leftFilament, rightFilament, '--no-data', sys.argv[5], engineData)
            else:
                ProfileMaker.simplify3D(leftHotend, rightHotend, leftFilament, rightFilament, '--no-data', '--file', engineData)
        elif sys.argv[-1] == '--cura':
            for quality in os.listdir('./resources/quality'):
                if quality == sys.argv[5]+'.json':
                    with open('./resources/quality/'+quality) as quality_file:    
                        qualityCura = json.load(quality_file)
            if len(sys.argv) == 8:
                if sys.argv[6] == '--no-file' or sys.argv[6] == '--only-filename':
                    ProfileMaker.cura(leftHotend, rightHotend, leftFilament, rightFilament, qualityCura, '--no-data', sys.argv[6], engineData)
            else:
                ProfileMaker.cura(leftHotend, rightHotend, leftFilament, rightFilament, qualityCura, '--no-data', '--file', engineData)
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
                    elif x2 == '7':
                        ProfileMaker.cura2FilesBundle(engineData)
                        raw_input("\n\tEaster egg. Cura 2 files created and zipped to share ;) Press Enter to continue...")

                elif x == '4':
                    if platform.system() != 'Windows':
                        print '\n Until next time!\n'
                    break

                if bundleProfilesSimplify3D or bundleProfilesCura or singleProfileSimplify3D or singleProfileCura:
                    if bundleProfilesSimplify3D:
                        clearDisplay()
                        print GUIHeader
                        ProfileMaker.simplify3DProfilesBundle(dataLog, profilesCreatedCount, engineData)
                        # profilesCreatedCount = simplify3DProfilesBundle(dataLog, profilesCreatedCount)
                    elif bundleProfilesCura:
                        clearDisplay()
                        print GUIHeader
                        profilesCreatedCount = ProfileMaker.curaProfilesBundle(dataLog, profilesCreatedCount, engineData)
                    elif singleProfileSimplify3D or singleProfileCura:
                        a = selectHotendAndFilament('Left', GUIHeader)
                        b = selectHotendAndFilament('Right', GUIHeader)
                        clearDisplay()
                        print GUIHeader
                        if sorted(profilesData['hotend'], key=lambda k: k['id'])[a[0]]['id'] == 'None' and sorted(profilesData['hotend'], key=lambda k: k['id'])[b[0]]['id'] == 'None':
                            raw_input("\n\tSelect at least one hotend to create a profile. Press Enter to continue...")
                        else:
                            if singleProfileSimplify3D:
                                hotendLeft = sorted(profilesData['hotend'], key=lambda k: k['id'])[a[0]]
                                hotendRight = sorted(profilesData['hotend'], key=lambda k: k['id'])[b[0]]
                                filamentLeft = sorted(profilesData['filament'], key=lambda k: k['id'])[a[1]]
                                filamentRight = sorted(profilesData['filament'], key=lambda k: k['id'])[b[1]]
                                newProfile = ProfileMaker.simplify3D(hotendLeft, hotendRight, filamentLeft, filamentRight, dataLog, '--file', engineData)
                                print "\n\tYour new Simplify3D profile '"+newProfile+"' has been created."
                                profilesCreatedCount = 1
                            elif singleProfileCura:
                                makeProfile = True
                                hotendLeft = sorted(profilesData['hotend'], key=lambda k: k['id'])[a[0]]
                                hotendRight = sorted(profilesData['hotend'], key=lambda k: k['id'])[b[0]]
                                filamentLeft = sorted(profilesData['filament'], key=lambda k: k['id'])[a[1]]
                                filamentRight = sorted(profilesData['filament'], key=lambda k: k['id'])[b[1]]
                                if hotendLeft['id'] != 'None' and hotendRight['id'] != 'None':
                                    if hotendLeft['nozzleSize'] != hotendRight['nozzleSize']:
                                        raw_input("\n\tSelect two hotends with the same nozzle size to create a Cura profile. Press Enter to continue...")
                                        makeProfile = False
                                    elif filamentLeft['isSupportMaterial'] and not filamentRight['isSupportMaterial']:
                                        raw_input("\n\tTo make IDEX prints with Cura using support material, please load the support material to the Right Extruder. Press Enter to continue...")
                                        makeProfile = False
                                if makeProfile:
                                    c = selectQuality(GUIHeader)
                                    clearDisplay()
                                    print GUIHeader
                                    if singleProfileCura:
                                        quality = sorted(profilesData['quality'], key=lambda k: k['index'])[c]
                                        print "\n\tYour new Cura profile '"+ProfileMaker.cura(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, dataLog, '--file', engineData)+"' has been created.\n"
                                        print "\tNOTE: To reduce the Ringing effect use the RingingRemover plugin by BCN3D.\n"
                                        profilesCreatedCount = 1

                    if profilesCreatedCount > 0:
                        while y not in ['Y', 'n']:
                            y = raw_input('\tSee profile(s) data? (Y/n) ')
                    if y == 'Y':
                        for l in dataLog:
                            print '\t',
                            for d in l.split(';'):
                                print str(d)[:6].rjust(6),
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
                        raw_input("\n\t\tYour gcode file '"+stlFile.split('/')[-1][:-4]+'.gcode'+"' has been created! Find it in the same folder as the .stl file.\n\t\tPress Enter to continue...")
                elif testComb:
                    clearDisplay()
                    print GUIHeader              
                    testAllCombinations()
                    raw_input("\t\tPress Enter to continue...")
                elif cura2Files:
                    clearDisplay()
                    print GUIHeader
                    ProfileMaker.cura2('--file', engineData)
                    ProfileMaker.installCura2Files()
                    raw_input("\t\tPress Enter to continue...")

if __name__ == '__main__':
    main() 