#!/usr/bin/python -tt
# coding: utf-8

# Guillem Àvila Padró - May 2017
# Released under GNU LICENSE
# https://opensource.org/licenses/GPL-3.0

def writeData(data, dataLog):
    extruder, defaultSpeed, infillLayerInterval, layerHeight, hotendLeft, hotendRight, primaryExtruder, infillExtruder, supportExtruder, filamentLeft, filamentRight, quality, firstLayerUnderspeed, outlineUnderspeed, supportUnderspeed, firstLayerHeightPercentage, hotendLeftTemperature, hotendRightTemperature, bedTemperature = data
    if extruder == 'Left Extruder':
        printA = "%.2f" % (float(defaultSpeed)/60*infillLayerInterval*layerHeight*hotendLeft['nozzleSize'])
        printB = ""
    elif extruder == 'Right Extruder':
        printA = ""
        printB = "%.2f" % (float(defaultSpeed)/60*infillLayerInterval*layerHeight*hotendRight['nozzleSize'])
    else:
        # IDEX
        if filamentLeft['isSupportMaterial'] != filamentRight['isSupportMaterial']:
            if filamentLeft['isSupportMaterial']:
                supportMaterialLoadedLeft  = float(supportUnderspeed)
                supportMaterialLoadedRight = 1
            else:
                supportMaterialLoadedLeft  = 1
                supportMaterialLoadedRight = float(supportUnderspeed)
        else:
            supportMaterialLoadedLeft  = 1
            supportMaterialLoadedRight = 1
        if hotendLeft['nozzleSize'] != hotendRight['nozzleSize']:
            if primaryExtruder == 0: 
                printA = "%.2f" % (float(defaultSpeed)/60*layerHeight*hotendLeft['nozzleSize']*supportMaterialLoadedLeft)
                printB = "%.2f" % (float(defaultSpeed)/60*infillLayerInterval*layerHeight*hotendRight['nozzleSize']*supportMaterialLoadedRight)
            else:
                printA = "%.2f" % (float(defaultSpeed)/60*layerHeight*infillLayerInterval*hotendLeft['nozzleSize']*supportMaterialLoadedLeft)
                printB = "%.2f" % (float(defaultSpeed)/60*layerHeight*hotendRight['nozzleSize']*supportMaterialLoadedRight)
        else:
            printA = "%.2f" % (float(defaultSpeed)/60*1*layerHeight*hotendLeft['nozzleSize']*supportMaterialLoadedLeft)
            printB = "%.2f" % (float(defaultSpeed)/60*infillLayerInterval*layerHeight*hotendRight['nozzleSize']*supportMaterialLoadedRight)

        if primaryExtruder == 0:
            printA = "%.2f" % max(float(printA), float(printA) * outlineUnderspeed, float(printA) * firstLayerHeightPercentage/100. * firstLayerUnderspeed)
        else:
            printB = "%.2f" % max(float(printB), float(printB) * outlineUnderspeed, float(printB) * firstLayerHeightPercentage/100. * firstLayerUnderspeed)


    dataLog.append(filamentLeft['id']+";"+filamentRight['id']+";"+extruder+";"+quality['id']+";"+hotendLeft['id']+";"+hotendRight['id']+";"+'T'+str(infillExtruder)+";"+'T'+str(primaryExtruder)+";"+'T'+str(supportExtruder)+";"+str(printA)+";"+str(printB)+";"+str(infillLayerInterval)+";"+("%.2f" % (defaultSpeed/60.))+";"+str(firstLayerUnderspeed)+";"+str(outlineUnderspeed)+";"+str(supportUnderspeed)+";"+str(firstLayerHeightPercentage)+";"+str(hotendLeftTemperature)+";"+str(hotendRightTemperature)+";"+str(bedTemperature)+";\n")