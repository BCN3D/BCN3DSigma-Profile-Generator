#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - May 2017
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

# Version Changelog
# - Internal structure major changes and code clean up & optimization
# - Cura 2 integration
# - SmartPurge activated by default. Needs Firmware v01-1.2.3
# - Raft improvements
# - First layer improvements
# - Layer height standarization

# ToDo:
# - move all generics to definition -> errors when trying to apply
# - add print mode (dupli/mirror) to SigmaVitamins
# - add material colors (& remove generics)
# - speeds heating hotends
# - document version changes
# - rewrite Logger.py

import os
import json
import platform
import sys

from progen import ProgenSettings as PS
PS.init()

from progen import ProfileMaker
from progen import ProfileTester
from progen import ProgenEngine
from progen import Logger

def selectHotendAndFilament(extruder, header):
    clearDisplay()
    print header
    print "\n\tSelect Sigma's "+extruder+" Hotend (1-"+str(len(PS.profilesData['hotend']))+'):'
    answer0 = ''
    hotendOptions = []
    for c in range(len(PS.profilesData['hotend'])):
        hotendOptions.append(str(c+1))
    materialOptions = []
    for c in range(len(PS.profilesData['filament'])):
        materialOptions.append(str(c+1))
    for hotend in range(len(PS.profilesData['hotend'])):
        print '\t'+str(hotend+1)+'. '+sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[hotend]['id']
    while answer0 not in hotendOptions:
        answer0 = raw_input('\t')
    print '\t'+extruder+' Hotend: '+sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[int(answer0)-1]['id']
    if answer0 != str(int(hotendOptions[-1])):
        clearDisplay()
        print header
        print "\n\tSelect Sigma's "+extruder+" Extruder Loaded Filament (1-"+str(len(PS.profilesData['filament']))+'):'
        answer1 = ''
        for material in range(len(PS.profilesData['filament'])):
            print '\t'+str(material+1)+'. '+sorted(PS.profilesData['filament'], key=lambda k: k['id'])[material]['id']
        while answer1 not in materialOptions:
            answer1 = raw_input('\t')
        print '\t'+extruder+' Extruder Filament: '+sorted(PS.profilesData['filament'], key=lambda k: k['id'])[int(answer1)-1]['id']+'.'
    else:
        answer1 = '1'
    return (int(answer0)-1, int(answer1)-1)

def selectQuality(header):
    clearDisplay()
    print header
    print "\n\tSelect Quality:"
    answer0 = ''
    qualityOptions = []
    for c in range(len(PS.profilesData['quality'])):
        qualityOptions.append(str(c+1))
    for quality in range(len(PS.profilesData['quality'])):
        print '\t'+str(quality+1)+'. '+sorted(PS.profilesData['quality'], key=lambda k: k['index'])[quality]['id']
    while answer0 not in qualityOptions:
        answer0 = raw_input('\t')
    print '\tQuality: '+sorted(PS.profilesData['quality'], key=lambda k: k['index'])[int(answer0)-1]['id']
    return int(answer0)-1   

def validArguments():
    if len(sys.argv) > 1:
        curaArguments = False
        simplify3DArguments = False
        if sys.argv[-1] == '--cura' and (len(sys.argv) == 7 or len(sys.argv) == 8):
            curaArguments = True
        elif sys.argv[-1] == '--simplify3d' and (len(sys.argv) == 6 or len(sys.argv) == 7):
            simplify3DArguments = True
        if curaArguments or simplify3DArguments:
            leftHotend = sys.argv[1]+'.json' in os.listdir('./resources/hotends') or sys.argv[1] == 'None'
            rightHontend = sys.argv[2]+'.json' in os.listdir('./resources/hotends') or sys.argv[2] == 'None'
            leftFilament = sys.argv[3]+'.json' in os.listdir('./resources/filaments') or (sys.argv[1] == 'None' and sys.argv[3] == 'None')
            rightFilament = sys.argv[4]+'.json' in os.listdir('./resources/filaments') or (sys.argv[2] == 'None' and sys.argv[4] == 'None')
            if curaArguments:
                quality = sys.argv[5]+'.json' in os.listdir('./resources/quality')
                if len(sys.argv) == 8:
                    fileAction = sys.argv[6] == '--no-file' or sys.argv[6] == '--only-filename'
                    return leftHotend and rightHontend and leftFilament and rightFilament and quality and fileAction
                else:
                    return leftHotend and rightHontend and leftFilament and rightFilament and quality 
            else:     
                if len(sys.argv) == 7:
                    fileAction = sys.argv[5] == '--no-file' or sys.argv[5] == '--only-filename'
                    return leftHotend and rightHontend and leftFilament and rightFilament and fileAction
                else:
                    return leftHotend and rightHontend and leftFilament and rightFilament           
        else:
            return False
    else:
        return False

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
            leftFilament = PS.profilesData['filament'][0]
        if sys.argv[4] == 'None':
            rightFilament = PS.profilesData['filament'][0]
        if sys.argv[-1] == '--simplify3d':
            if len(sys.argv) == 7:
                if sys.argv[5] == '--no-file' or sys.argv[5] == '--only-filename':
                    ProfileMaker.simplify3D(leftHotend, rightHotend, leftFilament, rightFilament, '--no-data', sys.argv[5])
            else:
                ProfileMaker.simplify3D(leftHotend, rightHotend, leftFilament, rightFilament, '--no-data', '--file')
        elif sys.argv[-1] == '--cura':
            for quality in os.listdir('./resources/quality'):
                if quality == sys.argv[5]+'.json':
                    with open('./resources/quality/'+quality) as quality_file:    
                        qualityCura = json.load(quality_file)
            if len(sys.argv) == 8:
                if sys.argv[6] == '--no-file' or sys.argv[6] == '--only-filename':
                    ProfileMaker.cura(leftHotend, rightHotend, leftFilament, rightFilament, qualityCura, '--no-data', sys.argv[6])
            else:
                ProfileMaker.cura(leftHotend, rightHotend, leftFilament, rightFilament, qualityCura, '--no-data', '--file')
    else:
        if len(sys.argv) == 1:
            experimentalMenu = False
            title = '\n Welcome to the BCN3D Sigma ProGen '+PS.progenVersionNumber+' (Build '+PS.progenBuildNumber+') \n'
            while True:
                clearDisplay()
                print title
                print ' Choose one option (1-5):'
                print ' 1. Profile for Simplify3D'
                print ' 2. Profile for Cura'
                print ' 3. Profile for Cura 2.6 [Beta]'
                print ' 4. Experimental features'
                print ' 5. Exit'
                if experimentalMenu:
                    x = '4'
                else: 
                    x = 'x'
                y = 'y'
                while x not in ['1','2','3','4', '5']:
                    x = raw_input(' ')
                profilesCreatedCount = 0

                if x == '4':
                    clearDisplay()
                    print title+'\n\n\n\n'
                    print '    Experimental features'
                    print '\n\tChoose one option (1-6):'
                    print '\t1. Generate a bundle of profiles - Simplify3D'
                    print '\t2. Generate a bundle of profiles - Cura'
                    print '\t3. Generate profile files bundle - Cura 2.6 [Beta]'
                    print '\t4. Test all combinations'
                    print '\t5. MacOS Only - Slice a model (with Cura)'
                    print '\t6. Back'
                    x2 = 'x'
                    while x2 not in ['1','2','3','4', '5', '6']:
                        x2 = raw_input('\t')

                singleProfileSimplify3D, singleProfileCura, cura2Files, bundleProfilesSimplify3D, bundleProfilesCura, testComb, sliceModel, cura2FilesBundle = False, False, False, False, False, False, False, False

                if x == '1':
                    singleProfileSimplify3D = True
                    GUIHeader = title+'\n\n    Profile for Simplify3D'
                elif x == '2':
                    singleProfileCura = True
                    GUIHeader = title+'\n\n\n    Profile for Cura'
                elif x == '3':
                    cura2Files = True
                    GUIHeader = title+'\n\n\n\n    Profile for Cura 2.6 [Beta]'
                elif x == '4':
                    experimentalMenu = True               
                    if x2 == '1':
                        bundleProfilesSimplify3D = True
                        GUIHeader = title+'\n\n\n\n\n    Experimental features\n\n\n\t   Generate a bundle of profiles - Simplify3D\n'
                    elif x2 == '2':
                        bundleProfilesCura = True
                        GUIHeader = title+'\n\n\n\n\n    Experimental features\n\n\n\n\t   Generate a bundle of profiles - Cura\n'
                    elif x2 == '3':                        
                        cura2FilesBundle = True
                        GUIHeader = title+'\n\n\n\n\n    Experimental features\n\n\n\n\n\t   Generate profile files bundle - Cura 2.6 [Beta]\n'
                    elif x2 == '4':
                        testComb = True
                        GUIHeader = title+'\n\n\n\n\n    Experimental features\n\n\n\n\n\n\t   Test all combinations\n'
                    elif x2 == '5':
                        sliceModel = True
                        GUIHeader = title+'\n\n\n\n\n    Experimental features\n\n\n\n\n\n\n\t   MacOS Only - Slice a model (with Cura)'
                    elif x2 == '6':
                        experimentalMenu = False

                elif x == '5':
                    if platform.system() != 'Windows':
                        print '\n Until next time!\n'
                    break

                if bundleProfilesSimplify3D or bundleProfilesCura or cura2FilesBundle or singleProfileSimplify3D or singleProfileCura or cura2Files:
                    if bundleProfilesSimplify3D:
                        clearDisplay()
                        print GUIHeader
                        ProfileMaker.simplify3DProfilesBundle(profilesCreatedCount)
                        profilesCreatedCount = ProfileMaker.simplify3DProfilesBundle(profilesCreatedCount)
                    elif bundleProfilesCura:
                        clearDisplay()
                        print GUIHeader
                        profilesCreatedCount = ProfileMaker.curaProfilesBundle(profilesCreatedCount)
                    elif cura2FilesBundle:
                        clearDisplay()
                        print GUIHeader
                        ProfileMaker.cura2FilesBundle()
                        raw_input("\n\t\tCura 2.6 files created and zipped to share ;) Press Enter to continue...")

                    elif cura2Files:
                        clearDisplay()
                        print GUIHeader
                        ProfileMaker.cura2('--file')
                        ProfileMaker.installCura2Files()
                        raw_input("\t\tPress Enter to continue...")
                    elif singleProfileSimplify3D or singleProfileCura:
                        a = selectHotendAndFilament('Left', GUIHeader)
                        b = selectHotendAndFilament('Right', GUIHeader)
                        clearDisplay()
                        print GUIHeader
                        if sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[a[0]]['id'] == 'None' and sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[b[0]]['id'] == 'None':
                            raw_input("\n\tSelect at least one hotend to create a profile. Press Enter to continue...")
                        else:
                            hotendLeft = sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[a[0]]
                            hotendRight = sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[b[0]]
                            filamentLeft = sorted(PS.profilesData['filament'], key=lambda k: k['id'])[a[1]]
                            filamentRight = sorted(PS.profilesData['filament'], key=lambda k: k['id'])[b[1]]
                            if singleProfileSimplify3D:
                                newProfile = ProfileMaker.simplify3D(hotendLeft, hotendRight, filamentLeft, filamentRight, '--file')
                                print "\n\tYour new Simplify3D profile '"+newProfile+"' has been created."
                                profilesCreatedCount = 1
                            elif singleProfileCura:
                                makeProfile = True
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
                                        quality = sorted(PS.profilesData['quality'], key=lambda k: k['index'])[c]
                                        print "\n\tYour new Cura profile '"+ProfileMaker.cura(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, '--file')+"' has been created.\n"
                                        print "\tNOTE: To reduce the Ringing effect use the RingingRemover plugin by BCN3D.\n"
                                        profilesCreatedCount = 1

                    if profilesCreatedCount > 0:
                        while y not in ['Y', 'n']:
                            y = raw_input('\tSee profile(s) data? (Y/n) ')
                    if y == 'Y':
                        # for l in loggedData:
                        #     print '\t',
                        #     for d in l.split(';'):
                        #         print str(d)[:6].rjust(6),
                        # print '\t'+str(profilesCreatedCount)+' profile(s) created with '+str(len(dataLog)-1)+' configurations.\n'
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
                    ProfileTester.testAllCombinations()
                    raw_input("\t\tPress Enter to continue...")

if __name__ == '__main__':
    main() 