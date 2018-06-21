#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - Jun 2018
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

import sys

import ProgenSettings as PS
import ProgenEngine

def testAllCombinations():
    cura2Tests = testCura2()
    curaTests = testCura()
    simplify3DTests = testSimplify3D()
    print '\t\tAll '+str(cura2Tests + curaTests + simplify3DTests)+' profiles can be generated!\n'

def testSimplify3D():

    # Calculate All profiles available to create
    totalSmaProfiles = (len(PS.profilesData['hotend'])-1) *  len(PS.profilesData['filament']) * 2
    totalBigProfiles = (len(PS.profilesData['hotend'])-1)**2 * len(PS.profilesData['filament'])**2
    realSimplify3DProfilesAvailable = totalSmaProfiles + totalBigProfiles

    # Start iteration
    combinationCount = 0
    totalSimplify3DProfilesAvailable = len(PS.profilesData['hotend'])**2 * len(PS.profilesData['filament'])**2
    for hotendLeft in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
        for hotendRight in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
            for filamentLeft in sorted(PS.profilesData['filament'], key=lambda k: k['id']):
                for filamentRight in sorted(PS.profilesData['filament'], key=lambda k: k['id']):
                    ProgenEngine.simplify3DProfile(hotendLeft, hotendRight, filamentLeft, filamentRight)
                    combinationCount += 1
                    sys.stdout.write("\r\t\tTesting Simplify3D Profiles: %d%%" % int(float(combinationCount)/totalSimplify3DProfilesAvailable*100))
                    sys.stdout.flush()
    print '\r\t\tTesting Simplify3D Profiles: OK. Profiles tested: '+str(realSimplify3DProfilesAvailable)
    return realSimplify3DProfilesAvailable

def testCura2():
    
    # Calculate All profiles available to create
    realCura2ProfilesAvailable = 1

    # Start iteration
    for machine in PS.profilesData['machine']:
        ProgenEngine.cura2Profile(machine)
    print '\r\t\tTesting Cura 2 Profiles:     OK. Profiles Tested: '+str(realCura2ProfilesAvailable)
    return realCura2ProfilesAvailable
    
