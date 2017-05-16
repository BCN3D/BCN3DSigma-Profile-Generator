#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - May 2017
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
                    ProgenEngine.simplify3DProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, '--no-data')
                    combinationCount += 1
                    sys.stdout.write("\r\t\tTesting Simplify3D Profiles: %d%%" % int(float(combinationCount)/totalSimplify3DProfilesAvailable*100))
                    sys.stdout.flush()
    print '\r\t\tTesting Simplify3D Profiles: OK. Profiles tested: '+str(realSimplify3DProfilesAvailable)
    return realSimplify3DProfilesAvailable

def testCura():

    # Calculate All profiles available to create
    totalSmaProfiles = (len(PS.profilesData['hotend'])-1) *  len(PS.profilesData['filament']) * 2
    nozzleSizes = []
    for hotend in sorted(PS.profilesData['hotend'], key=lambda k: k['id'])[:-1]:
        nozzleSizes.append(hotend['nozzleSize'])
    curaGroupedSizes = {x:nozzleSizes.count(x) for x in nozzleSizes}
    curaIDEXHotendsCombinations = 0
    for size in curaGroupedSizes:
        curaIDEXHotendsCombinations += curaGroupedSizes[size]**2

    realCuraProfilesAvailable = (totalSmaProfiles + curaIDEXHotendsCombinations * len(PS.profilesData['filament'])**2) * len(PS.profilesData['quality'])

    # Start iteration
    combinationCount = 0
    totalProfilesAvailable = len(PS.profilesData['hotend'])**2 * len(PS.profilesData['filament'])**2 * len(PS.profilesData['quality'])
    for hotendLeft in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
        for hotendRight in sorted(PS.profilesData['hotend'], key=lambda k: k['id']):
            for filamentLeft in sorted(PS.profilesData['filament'], key=lambda k: k['id']):
                for filamentRight in sorted(PS.profilesData['filament'], key=lambda k: k['id']):
                    for quality in sorted(PS.profilesData['quality'], key=lambda k: k['index']):
                        ProgenEngine.curaProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, '--no-data')
                        combinationCount += 1
                        sys.stdout.write("\r\t\tTesting Cura Profiles:       %d%%" % int(float(combinationCount)/totalProfilesAvailable*100))
                        sys.stdout.flush()
    print '\r\t\tTesting Cura Profiles:       OK. Profiles Tested: '+str(realCuraProfilesAvailable)
    return realCuraProfilesAvailable

def testCura2():
    
    # Calculate All profiles available to create
    realCura2ProfilesAvailable = 1

    # Start iteration
    print ProgenEngine.cura2Profile()
    print '\r\t\tTesting Cura 2 Profiles:     OK. Profiles Tested: '+str(realCura2ProfilesAvailable)
    return realCura2ProfilesAvailable
    
