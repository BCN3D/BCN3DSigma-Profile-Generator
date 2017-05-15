#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - May 2017
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

import os
import sys
import shutil
import platform
import time
import ctypes

import ProgenEngine

def simplify3D(hotendLeft, hotendRight, filamentLeft, filamentRight, dataLog, fileAction, engineData):
    fileName, fileContent = ProgenEngine.simplify3DProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, dataLog, engineData)
    if fileAction == '--file':
        with open(fileName, "w") as f:
            f.write(fileContent)
    elif fileAction == '--no-file':
        print fileContent
    elif fileAction == '--only-filename':
        print fileName
    return fileName

def cura(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, dataLog, fileAction, engineData):
    fileName, fileContent = ProgenEngine.curaProfile(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, dataLog, engineData)
    if fileAction == '--file':
        with open(fileName, "w") as f:
            f.write(fileContent)
    elif fileAction == '--no-file':
        print fileContent
    elif fileAction == '--only-filename':
        print fileName
    return fileName

def cura2(fileAction, engineData):

    cura2id = 'bcn3dsigma'
    machineSettingsPluginName = 'SigmaSettingsAction'

    # Create Folders structure
    if "Cura 2" in os.listdir('.'):
        shutil.rmtree("Cura 2")
    os.mkdir('Cura 2')
    os.mkdir('Cura 2/resources')
    os.mkdir('Cura 2/resources/definitions')
    os.mkdir('Cura 2/resources/extruders')
    os.mkdir('Cura 2/resources/materials')
    os.mkdir('Cura 2/resources/materials/'+cura2id)
    os.mkdir('Cura 2/resources/meshes')
    shutil.copyfile('resources/meshes/bcn3dsigma_bed.obj', 'Cura 2/resources/meshes/'+cura2id+'_bed.obj')
    os.mkdir('Cura 2/resources/quality')
    os.mkdir('Cura 2/resources/quality/'+cura2id)
    os.mkdir('Cura 2/resources/variants')
    os.mkdir('Cura 2/plugins')
    os.mkdir('Cura 2/plugins/PostProcessingPlugin')
    os.mkdir('Cura 2/plugins/PostProcessingPlugin/scripts')
    os.mkdir('Cura 2/plugins/'+machineSettingsPluginName)

    for fileName, fileContent in ProgenEngine.cura2Profile(engineData):
        if fileAction == '--file':
            with open(fileName, "w") as f:
                f.write(fileContent)
        elif fileAction == '--no-file':
            print fileContent
        elif fileAction == '--only-filename':
            print fileName

    os.mkdir('Cura 2/MacOS')
    shutil.copytree('Cura 2/resources', 'Cura 2/MacOS/resources')
    os.mkdir('Cura 2/MacOS/plugins')
    shutil.copytree('Cura 2/plugins', 'Cura 2/MacOS/plugins/plugins')
    shutil.copytree('Cura 2/resources', 'Cura 2/Windows/resources')
    shutil.copytree('Cura 2/plugins', 'Cura 2/Windows/plugins')
    shutil.rmtree('Cura 2/resources')
    shutil.rmtree('Cura 2/plugins')

def installCura2Files():
    
    allowAutoInstall = False

    if platform.system() == 'Darwin' and 'Cura.app' in os.listdir('/Applications'):
        allowAutoInstall = True
        root_src_dir = 'Cura 2/MacOS'
        root_dst_dir = '/Applications/Cura.app/Contents/Resources'
    
    elif platform.system() == 'Windows':

        installedCuras = []
        
        for folder in os.listdir('C:\Program Files'): # add [::-1] to list folders in reverse order
            if 'Cura 2' in folder and 'Cura.exe' in os.listdir('C:\\Program Files\\'+folder):
                    installedCuras.append(folder)

        if len(installedCuras) >= 1:

            # check permissions for Windows 10
            if platform.release() == '10':
                if is_admin():
                    allowAutoInstall = True
                else:
                    pass
            else:
                allowAutoInstall = True
            
            if allowAutoInstall:
                root_src_dir = 'Cura 2\\Windows'
                if len(installedCuras) > 1:
                    print "\n\t\tYou have more than one Cura 2 installed! Select where you want to add the BCN3D Sigma:"
                    answer0 = ''
                    folderOptions = []
                    for c in range(len(installedCuras)):
                        folderOptions.append(str(c+1))
                        print '\t\t'+str(c+1)+'. '+installedCuras[c]
                    while answer0 not in folderOptions:
                        answer0 = raw_input('\t\t')            
                    allowAutoInstall = True
                    root_dst_dir = 'C:\\Program Files\\'+installedCuras[int(answer0)-1]
                else:
                    allowAutoInstall = True
                    root_dst_dir = 'C:\\Program Files\\'+installedCuras[0]

    if allowAutoInstall:
        for src_dir, dirs, files in os.walk(root_src_dir):
            dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                if os.path.exists(dst_file):
                    os.remove(dst_file)
                shutil.move(src_file, dst_dir)
        if "Cura 2" in os.listdir('.'):
            shutil.rmtree("Cura 2")
        print '\n\t\tThe BCN3D Sigma has been successfully added to Cura 2. Enjoy!\n'
    else:
        print "\n\t\tUnable to install files automatically.\n"
        print "\t\tA new folder called 'Cura 2' has been created in your working directory."
        print "\t\tCOMBINE the folders inside MacOS or Windows, according to your OS with the ones"
        print "\t\tinside your Cura 2 installation folder. Be careful to NOT replace it!\n"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def simplify3DProfilesBundle(dataLog, profilesCreatedCount, engineData):
    profilesData = engineData[0]
    y = 'y'
    if getSimplify3DBundleSize(engineData)/1024/1024 >= 150: # define Size limit to notice (in MB)
        print '\t\tEstimated space needed during the process: '+str(int(getSimplify3DBundleSize(engineData)*1.075/1024/1024))+' MB.'
        print '\t\tEstimated final bundle size: '+str(int(getSimplify3DBundleSize(engineData)*0.075/1024/1024))+' MB.'
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
                        simplify3D(hotendLeft, hotendRight, filamentLeft, filamentRight, dataLog, '--file' , engineData)
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

def getSimplify3DBundleSize(engineData, oneLineCsvSize = float(10494984)/78480): # experimental value
    profilesData = engineData[0]
    if ".BCN3D Sigma - Simplify3D Profiles temp" in os.listdir('.'):
        shutil.rmtree(".BCN3D Sigma - Simplify3D Profiles temp")
    os.mkdir(".BCN3D Sigma - Simplify3D Profiles temp")
    os.chdir(".BCN3D Sigma - Simplify3D Profiles temp")
    
    totalSmaProfiles = (len(profilesData['hotend'])-1) *  len(profilesData['filament']) * 2
    totalBigProfiles = (len(profilesData['hotend'])-1)**2 * len(profilesData['filament'])**2

    fileNameBig = simplify3D(profilesData['hotend'][0], profilesData['hotend'][0], profilesData['filament'][0], profilesData['filament'][0], 'noData', '--file', engineData)
    fileNameSmall = simplify3D(profilesData['hotend'][0], profilesData['hotend'][-1], profilesData['filament'][0], profilesData['filament'][0], 'noData', '--file', engineData)
    
    csvSize = oneLineCsvSize * (totalSmaProfiles*len(profilesData['quality']) + totalBigProfiles*len(profilesData['quality'])*3)
    bundleSize = totalSmaProfiles*os.path.getsize(fileNameSmall)+totalBigProfiles*os.path.getsize(fileNameBig) + csvSize

    os.chdir('..')
    shutil.rmtree(".BCN3D Sigma - Simplify3D Profiles temp")
    return bundleSize*1.05

def curaProfilesBundle(dataLog, profilesCreatedCount, engineData):  
    profilesData = engineData[0]
    y = 'y'
    if getCuraBundleSize(engineData)/1024/1024 >= 150: # define Size limit to notice (in MB)
        print '\t\tEstimated space needed during the process: '+str(int(getCuraBundleSize(engineData)*1.075/1024/1024))+' MB.'
        print '\t\tEstimated final bundle size: '+str(int(getCuraBundleSize(engineData)*0.075/1024/1024))+' MB.'
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
                            try:
                                cura(hotendLeft, hotendRight, filamentLeft, filamentRight, quality, dataLog, '--file', engineData)
                            except:
                                pass
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

def getCuraBundleSize(engineData, oneLineCsvSize = float(10494984)/78480): # experimental value
    profilesData = engineData[0]
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

    fileName = cura(profilesData['hotend'][0], profilesData['hotend'][0], profilesData['filament'][0], profilesData['filament'][0], profilesData['quality'][0], 'noData', '--file', engineData)
    
    csvSize = oneLineCsvSize * totalProfiles
    bundleSize = totalProfiles*os.path.getsize(fileName) + csvSize

    os.chdir('..')
    shutil.rmtree(".BCN3D Sigma - Cura Profiles temp")
    return bundleSize*1.05

def cura2FilesBundle(engineData):
    cura2('--file', engineData)
    with open('Cura 2/Readme.txt', 'w') as f:
        lines = []
        lines.append(r'Bundle make time:'+'\n')
        lines.append(r''+'\n')
        lines.append(r'    '+time.strftime("%Y-%m-%d")+" "+time.strftime("%H:%M:%S")+'\n')
        lines.append(r''+'\n')
        lines.append(r'Instructions:'+'\n')
        lines.append(r''+'\n')
        lines.append(r'    Mac OS:'+'\n')
        lines.append(r'        1 - COMBINE all folders inside "MacOS" with the ones inside "/Applications/Cura.app/Contents/Resources"'+'\n')
        lines.append(r'        2 - Restart Cura 2'+'\n')
        lines.append(r''+'\n')
        lines.append(r'    Windows:'+'\n')
        lines.append(r'        1 - COMBINE all folders inside "Windows" with the ones inside "C:/Program Files/Cura 2.5"'+'\n')
        lines.append(r'        2 - Restart Cura 2'+'\n')
        f.writelines(lines)
    shutil.make_archive('BCN3D Sigma - Cura 2', 'zip', 'Cura 2')    

    # # Copy files to BCN3D Utilities repository
    # try:
    #     if "MacOS" in os.listdir("../BCN3D-Utilities/Sigma - Cura 2"):
    #         shutil.rmtree("../BCN3D-Utilities/Sigma - Cura 2/MacOS")
    #     shutil.copytree("Cura 2/MacOS", "../BCN3D-Utilities/Sigma - Cura 2/MacOS")
    #     if "Windows" in os.listdir("../BCN3D-Utilities/Sigma - Cura 2"):
    #         shutil.rmtree("../BCN3D-Utilities/Sigma - Cura 2/Windows")
    #     shutil.copytree("Cura 2/Windows", "../BCN3D-Utilities/Sigma - Cura 2/Windows")
    # except:
    #     pass

    shutil.rmtree("Cura 2")