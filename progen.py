#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - Oct 2017
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

def selectMachineAndPrintMode(header):
    clearDisplay()
    print header
    print "\n\tSelect your BCN3D machine (1-"+str(len(PS.profilesData['machine']))+'):'
    answer0 = ''
    machineOptions = []
    for c in range(len(PS.profilesData['machine'])):
        machineOptions.append(str(c+1))
    for machine in range(len(PS.profilesData['machine'])):
        print '\t'+str(machine+1)+'. '+sorted(PS.profilesData['machine'], key=lambda k: k['id'])[machine]['name']
    while answer0 not in machineOptions:
        answer0 = raw_input('\t')

    modesList = sorted(PS.profilesData['machine'], key=lambda k: k['id'])[int(answer0)-1]['printMode']
    if len(modesList) > 1:   
        modeOptions = []
        for c in range(len(modesList)):
            modeOptions.append(str(c+1))
        clearDisplay()
        print header
        print "\n\tSelect "+sorted(PS.profilesData['machine'], key=lambda k: k['id'])[int(answer0)-1]['name']+"'s print mode (1-"+str(len(modesList))+'):'
        answer1 = ''
        for mode in range(len(modesList)):
            print '\t'+str(mode+1)+'. '+sorted(modesList)[mode].title()
        while answer1 not in modeOptions:
            answer1 = raw_input('\t')
    else:
        answer1 = '1'
    return (int(answer0)-1, int(answer1)-1)


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
    if answer0 != str(int(hotendOptions[-1])):
        clearDisplay()
        print header
        print "\n\tSelect Sigma's "+extruder+" Extruder Loaded Filament (1-"+str(len(PS.profilesData['filament']))+'):'
        answer1 = ''
        for material in range(len(PS.profilesData['filament'])):
            print '\t'+str(material+1)+'. '+sorted(PS.profilesData['filament'], key=lambda k: k['id'])[material]['id']
        while answer1 not in materialOptions:
            answer1 = raw_input('\t')
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
    if len(sys.argv) > 1 and (len(sys.argv) == 7 or len(sys.argv) == 8):
        machine = sys.argv[1]+'.json' in os.listdir('./resources/machines')
        printMode = False
        for m in PS.profilesData['machine']:
            if m['id'] == sys.argv[1]:
                printMode = sys.argv[2] in m['printMode']
        leftHotend = sys.argv[3]+'.json' in os.listdir('./resources/hotends') or sys.argv[1] == 'None'
        rightHontend = sys.argv[4]+'.json' in os.listdir('./resources/hotends') or sys.argv[2] == 'None'
        leftFilament = sys.argv[5]+'.json' in os.listdir('./resources/filaments') or (sys.argv[1] == 'None' and sys.argv[3] == 'None')
        rightFilament = sys.argv[6]+'.json' in os.listdir('./resources/filaments') or (sys.argv[2] == 'None' and sys.argv[4] == 'None')
        # print machine, printMode, leftHotend, rightHontend, leftFilament, rightFilament
        if len(sys.argv) == 9:
            fileAction = sys.argv[7] == '--no-file' or sys.argv[7] == '--only-filename'
            return machine and printMode and leftHotend and rightHontend and leftFilament and rightFilament and fileAction
        else:
            return machine and printMode and leftHotend and rightHontend and leftFilament and rightFilament
    else:
        return False

def clearDisplay():
    # pass
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def main():
    # if platform.system() == 'Windows':
    #     # os.system('color f0')
    #     os.system('mode con: cols=154 lines=35')
    #     pass
    if validArguments():
        with open('./resources/machines/'+sys.argv[1]+'.json') as machine_file:    
            machine = json.load(machine_file)
        printMode = sys.argv[2]
        with open('./resources/hotends/'+sys.argv[3]+'.json') as machine_file:    
            leftHotend = json.load(machine_file)
        with open('./resources/hotends/'+sys.argv[4]+'.json') as machine_file:    
            rightHotend = json.load(machine_file)
        with open('./resources/filaments/'+sys.argv[5]+'.json') as machine_file:    
            leftFilament = json.load(machine_file)
        with open('./resources/filaments/'+sys.argv[6]+'.json') as machine_file:    
            rightFilament = json.load(machine_file)
        if sys.argv[1] == 'None':
            leftHotend = dict([('id', 'None')])
        if sys.argv[2] == "None":
            rightHotend = dict([('id', 'None')])
        if sys.argv[3] == 'None':
            leftFilament = PS.profilesData['filament'][0]
        if sys.argv[4] == 'None':
            rightFilament = PS.profilesData['filament'][0]
        if len(sys.argv) == 8:
            if sys.argv[7] == '--no-file' or sys.argv[7] == '--only-filename':
                ProfileMaker.simplify3D(machine, printMode, leftHotend, rightHotend, leftFilament, rightFilament, sys.argv[7])
        else:
            ProfileMaker.simplify3D(machine, printMode, leftHotend, rightHotend, leftFilament, rightFilament, '--file')
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
                print ' 3. Experimental features'
                print ' 4. Exit'
                if experimentalMenu:
                    x = '3'
                else: 
                    x = 'x'
                y = 'y'
                while x not in ['1','2','3','4']:
                    x = raw_input(' ')
                profilesCreatedCount = 0

                if x == '3':
                    clearDisplay()
                    print title+'\n\n\n\n'
                    print '    Experimental features'
                    print '\n\tChoose one option (1-6):'
                    print '\t1. Generate a bundle of profiles - Simplify3D'
                    print '\t2. Generate profile files bundle - Cura'
                    print '\t3. Test all combinations'
                    print '\t4. Back'
                    x2 = 'x'
                    while x2 not in ['1','2','3','4']:
                        x2 = raw_input('\t')

                singleProfileSimplify3D, curaFiles, bundleProfilesSimplify3D, testComb, curaFilesBundle = False, False, False, False, False

                if x == '1':
                    singleProfileSimplify3D = True
                    GUIHeader = title+'\n\n    Profile for Simplify3D'
                elif x == '2':
                    curaFiles = True
                    GUIHeader = title+'\n\n\n    Profile for Cura'
                elif x == '3':
                    experimentalMenu = True               
                    if x2 == '1':
                        bundleProfilesSimplify3D = True
                        GUIHeader = title+'\n\n\n\n\n    Experimental features\n\n\n\t   Generate a bundle of profiles - Simplify3D\n'
                    elif x2 == '2':
                        curaFilesBundle = True
                        GUIHeader = title+'\n\n\n\n\n    Experimental features\n\n\n\n\t   Generate a bundle of profiles - Cura\n'
                    elif x2 == '3':
                        testComb = True
                        GUIHeader = title+'\n\n\n\n\n    Experimental features\n\n\n\n\n\n\t   Test all combinations\n'
                    elif x2 == '4':
                        experimentalMenu = False

                elif x == '4':
                    break

                if bundleProfilesSimplify3D or curaFilesBundle or singleProfileSimplify3D or curaFiles:
                    if bundleProfilesSimplify3D:
                        clearDisplay()
                        print GUIHeader
                        ProfileMaker.simplify3DProfilesBundle(profilesCreatedCount)
                        profilesCreatedCount = ProfileMaker.simplify3DProfilesBundle(profilesCreatedCount)
                    elif curaFilesBundle:
                        clearDisplay()
                        print GUIHeader
                        ProfileMaker.curaFilesBundle()
                        raw_input("\n\t\tCura files created and zipped to share ;) Press Enter to continue...")

                    elif curaFiles:
                        clearDisplay()
                        print GUIHeader
                        ProfileMaker.cura('--file')
                        ProfileMaker.installCuraFiles()
                        raw_input("\t\tPress Enter to continue...")
                    elif singleProfileSimplify3D:
                        
                        c = selectMachineAndPrintMode(GUIHeader)
                        machine = sorted(PS.profilesData['machine'], key=lambda k: k['id'])[c[0]]
                        for m in PS.profilesData['machine']:
                            if m == machine:
                                printMode = sorted(m['printMode'])[c[1]]
                        a = selectHotendAndFilament('Left', GUIHeader)
                        hotendLeft = sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[a[0]]
                        filamentLeft = sorted(PS.profilesData['filament'], key=lambda k: k['id'])[a[1]]
                        if printMode == 'regular':
                            b = selectHotendAndFilament('Right', GUIHeader)
                            hotendRight = sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[b[0]]
                            filamentRight = sorted(PS.profilesData['filament'], key=lambda k: k['id'])[b[1]]
                        else:
                            hotendRight = hotendLeft
                            filamentRight = filamentLeft
                        clearDisplay()
                        print GUIHeader
                        if sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[a[0]]['id'] == 'None' and sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[b[0]]['id'] == 'None':
                            raw_input("\n\tSelect at least one hotend to create a profile. Press Enter to continue...")
                        else:
                            newProfile = ProfileMaker.simplify3D(machine, printMode, hotendLeft, hotendRight, filamentLeft, filamentRight, '--file')
                            print "\n\tYour new Simplify3D profile '"+newProfile+"' has been created."
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
                elif testComb:
                    clearDisplay()
                    print GUIHeader              
                    ProfileTester.testAllCombinations()
                    raw_input("\t\tPress Enter to continue...")

if __name__ == '__main__':
    main() 