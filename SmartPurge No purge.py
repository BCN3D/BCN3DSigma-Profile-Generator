                elif smartPurge:
                    clearDisplay()
                    print GUIHeader
                    if platform.system() == 'Windows':
                        gcodeFile = raw_input('\n\t\tDrag & Drop your .gcode file to this window. Then press Enter.\n\t\t').replace('"', '')
                    else:
                        gcodeFile = raw_input('\n\t\tDrag & Drop your .gcode file to this window. Then press Enter.\n\t\t')[:-1].replace('\\', '')
                    
                    newLines = []

                    dataLog = ['Active Toolhead;Nozzle Size [mm];Extruded Length [mm];Extruded Volume [mm^3];Estimated Time [sec];\n'] # just to get different data
                    idleTimeEstimator = 0 # just for dataLog (comment if not used)
                    activeToolHeadWhileIdle = 'T0' # just for dataLog (comment if not used)

                    with open(gcodeFile, 'r') as originalFile:
                        originalLines = originalFile.readlines()

                    for line in originalLines[:3]:
                        if 'Simplify3D' in line:
                            for d in originalLines[-10:]:
                                if 'Filament length' in d:
                                    filamentLength = float(d[21:].split(' mm')[0])
                                elif 'Build time' in d:
                                    if 'hours' in d:
                                        buildTime = int(d[16:].split(' hours ')[0])*60+int(d[16:].split(' hours ')[1].split(' minutes')[0])
                                    else:
                                        buildTime = int(d[16:].split(' hour ')[0])*60+int(d[16:].split(' hour ')[1].split(' minutes')[0])
                                elif 'Plastic weight' in d:
                                    plasticWeight = float(d[20:].split(' g ')[0])
                            for e in originalLines[:184]:
                                if 'extruderDiameter' in e:
                                    nozzleSizeT0 = float(e[21:].split(',')[0])
                                    nozzleSizeT1 = float(e[21:].split(',')[1])

                            filamentDiameter = 2.85 # adaptar a filamentDiameter
                            yeldCurve = 1000
                            newPurgeLength = 0
                            lastToolChange = 0
                            purgeDone = False
                            for lineIndex in range(len(originalLines)):
                                if originalLines[lineIndex].endswith(';fast purge\r\n') or originalLines[lineIndex].endswith(';retract\r\n') or originalLines[lineIndex].endswith(';travel\r\n') or originalLines[lineIndex].endswith(';retract\r\n') or originalLines[lineIndex].endswith(';reset t0\r\n') or originalLines[lineIndex].endswith(';reset t1\r\n'):
                                    originalLines[lineIndex] = ''
                                elif originalLines[lineIndex].endswith(';slow purge\r\n'):
                                    i = 1
                                    idleExtrusion = 0
                                    activeNozzleSizeWhileIdle = 0
                                    purgeLength = float(originalLines[lineIndex].split('E')[1].split('\t')[0])
                                    purgeDone = False
                                    originalLines[lineIndex] = ''
                                    while i < (lineIndex-lastToolChange):
                                        if originalLines[lineIndex-i].startswith('G92 E0'):
                                            i += 1
                                            while 'E' not in originalLines[lineIndex-i]:
                                                i += 1
                                            if originalLines[lineIndex-i].startswith('G1 X'):
                                                idleExtrusion += float(originalLines[lineIndex-i].split('E')[1].split(' F')[0])
                                        elif originalLines[lineIndex-i].endswith(';slow purge\r\n'):
                                            i = lineIndex
                                        i += 1
                                        if originalLines[lineIndex-i].startswith('T0'):
                                            activeNozzleSizeWhileIdle = nozzleSizeT0
                                            activeNozzleSizeEntering = nozzleSizeT1
                                            activeToolHeadWhileIdle = 'T0' # just for dataLog
                                            lastToolChange = lineIndex-i
                                        elif originalLines[lineIndex-i].startswith('T1'):
                                            activeNozzleSizeWhileIdle = nozzleSizeT1
                                            activeNozzleSizeEntering = nozzleSizeT0
                                            activeToolHeadWhileIdle = 'T1' # just for dataLog
                                            lastToolChange = lineIndex-i
                                    if activeNozzleSizeWhileIdle > 0:
                                        if activeNozzleSizeEntering >= 0.8:
                                            maxPurgeLength = 8 + 18 # llargada max highFlow
                                        else:
                                            maxPurgeLength = 8 + 14 # llargada max standard
                                        materialDefaultPurgeLength = purgeLength / ((activeNozzleSizeEntering/0.4)**2)
                                        idleTimeEstimator = (filamentDiameter/activeNozzleSizeWhileIdle)**2 * idleExtrusion * buildTime/filamentLength
                                        pressureParameter = math.pi * ((filamentDiameter/2)**2 - (activeNozzleSizeEntering/2)**2) * yeldCurve/activeNozzleSizeEntering
                                        newPurgeLength = maxPurgeLength * materialDefaultPurgeLength/1.5 - maxPurgeLength * materialDefaultPurgeLength/1.5 * math.exp(-idleTimeEstimator/pressureParameter)
                                elif originalLines[lineIndex].startswith('G1 X') and originalLines[lineIndex-1].startswith('G92 E0') and purgeDone == False:
                                    currentExtrusion = float(originalLines[lineIndex][originalLines[lineIndex].find('E')+1:originalLines[lineIndex].find('E')+7])

                                    originalLines[lineIndex] = originalLines[lineIndex].split('E')[0]+'E'+str(round(currentExtrusion+newPurgeLength, 4))+' F'+originalLines[lineIndex].split(' F')[1]+'G92 E'+str(currentExtrusion)+'\r\n'
                                    
                                    dataLog.append(activeToolHeadWhileIdle+';'+str(activeNozzleSizeWhileIdle)+";"+str(round(idleExtrusion,4)).replace('.',',')+';'+str(round(idleExtrusion*math.pi*(2.85/2)**2,4)).replace('.',',')+";"+str(round(idleTimeEstimator,0)).replace('.',',')+";\n") # data logging

                                    purgeDone = True

                                sys.stdout.write("\r\t\tProgress: %d%%" % int(float(lineIndex)/len(originalLines)*100))
                                sys.stdout.flush()

                                newLines.append(originalLines[lineIndex])
                            break
                    for line in originalLines[-3:]:
                        if 'CURA' in line:
                            break

                    with open("DataLog.csv", "w") as csv:
                        csv.writelines(dataLog)

                    with open(gcodeFile, 'w') as newFile:
                        newFile.writelines(newLines)
                    raw_input("\r\t\tWelcome to the future. All tool changes have been adjusted using the SmartPurge algorithm.\n\t\tPress Enter to continue...")

                    

                    '''
                    Release Notes

                    Many improvements (read commit description)

                  * - SmartPurge. Algorithm to recalculate purge lengths according to machine setup and idle times. Find it under the experimental features.
                  * - RingingRemover. Algorithm to change accelerations and avoid the ringing effect on corners.
                    - Default purge speeds now are calculated to improve surplus material storage.
                    - Adjusted speeds for support materials
                    - S3D: When combining hotends, infill will be printed at maximum flow, speeding up everything & minimizing tool changes.
                    - Cura: adjusted XY distance for better supports.
                    - Cura: disabled support material on T0 for IDEX profiles.
                    - Cura: corrected temperature setup.
                    - Corrected printed flows when showing data.
                    '''