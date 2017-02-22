                                for lineIndex in range(len(originalLines)):
                                    if originalLines[lineIndex].endswith(';slow purge\r\n'):
                                        i = 1
                                        idleExtrusion = 0
                                        activeNozzleSizeWhileIdle = 0
                                        purgeLength = float(originalLines[lineIndex].split('E')[1].split('\t')[0])
                                        while i < lineIndex:
                                            if originalLines[lineIndex-i].startswith('G92 E0'):
                                                i += 1
                                                while 'E' not in originalLines[lineIndex-i]:
                                                    i += 1
                                                if originalLines[lineIndex-i].startswith('G1 X'):
                                                    idleExtrusion += float(originalLines[lineIndex-i][originalLines[lineIndex-i].find('E')+1:originalLines[lineIndex-i].find('E')+7])
                                            elif originalLines[lineIndex-i].endswith(';slow purge\r\n'):
                                                break
                                            i += 1
                                            if originalLines[lineIndex-i].startswith('T0'):
                                                activeNozzleSizeWhileIdle = nozzleSizeT0
                                                activeNozzleSizeEntering = nozzleSizeT1
                                            elif originalLines[lineIndex-i].startswith('T1'):
                                                activeNozzleSizeWhileIdle = nozzleSizeT1
                                                activeNozzleSizeEntering = nozzleSizeT0                                  

                                        if activeNozzleSizeWhileIdle > 0:
                                            if activeNozzleSizeEntering >= 0.8:
                                                maxPurgeLength = 8 + 18 # llargada max highFlow
                                            else:
                                                maxPurgeLength = 8 + 14 # llargada max standard
                                            materialDefaultPurgeLength = purgeLength / ((activeNozzleSizeEntering/0.4)**2)
                                            idleTimeEstimator = (filamentDiameter/activeNozzleSizeWhileIdle)**2 * idleExtrusion * buildTime/filamentLength
                                            pressureParameter = math.pi * ((filamentDiameter/2)**2 - (activeNozzleSizeEntering/2)**2) * yeldCurve/activeNozzleSizeEntering
                                            newPurgeLength = maxPurgeLength * materialDefaultPurgeLength - maxPurgeLength * materialDefaultPurgeLength * math.exp(-idleTimeEstimator/pressureParameter)
                                            originalLines[lineIndex] = originalLines[lineIndex].split('E')[0] + 'E' + ("%.4f" % newPurgeLength) + '\t' + originalLines[lineIndex].split('\t')[1]

                                    sys.stdout.write("\r\t\tProgress: %d%%" % int(float(lineIndex)/len(originalLines)*100))
                                    sys.stdout.flush()

                                    newFile.write(originalLines[lineIndex])
                                break