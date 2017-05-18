# BCN3DSigma-ProGen

*NOTE: This is a development Branch where we upload beta versions. Find the latest stable version in the [Master](https://github.com/BCN3D/BCN3DSigma-Profile-Generator/tree/master) branch.*

Profile Generator for Simplify3D, Cura & Cura 2 slicing softwares. Specifically designed for the BCN3D Sigma.

The official code behind the [Sigma ProGen web interface](https://www.bcn3dtechnologies.com/en/sigma-progen/). It generates profiles according to hotends, filaments and qualities defined in *resources* folder.

## Requirements

- Python 2.7 installed.
- *resources* folder with at least one hotend in *hotends* folder, one filament in *filaments* and one quality preset in *quality*. The included one comes with all hotends, filaments and qualities we have tested.

## Usage

Clone/download the repository in your computer:

`git clone https://github.com/BCN3D/BCN3DSigma-Profile-Generator`

Decompress it if you need to, open a terminal, go to the directory and call the script: 

`python progen.py`

Will ask for a functionality:

1. **Profile for Simplify3D:** Will ask for left Hotend, left loaded Filament, right Hotend and right loaded Filament. Then will generate the fff profile file.

2. **Profile for Cura:** Same as *1*, now for Cura (will ask for Quality at the end).

2. **Profile for Cura 2 [Beta]:** Asks nothig. Generates all the files to add the Sigma to Cura 2 and, if Cura 2 is already installed, copies all the files to the right places.

4. **Experimental features:** Some experimental extra features.

5. **Exit:** Quit the program.

In order to add, remove or change a hotend, filament or quality preconfiguration edit the files in *Profiles Data* folder.

### Fast mode (No GUI)

To generate a profile without entering the GUI. 

Simplify3D: call the script and insert 4 valid parameters:

`python progen.py LHotend RHotend LFilament RFilament --software`

Cura: call the script and insert 5 valid parameters:

`python progen.py LHotend RHotend LFilament RFilament Quality --software`

Cura 2: Still not available.

Valid parameters for Hotends are filenames in */resources/hotends* or 'None' if not mounted. Valid parameters for Fiaments are filenames in */resources/filaments* or 'None' if empty. Valid parameters for Quality are filenames in */resources/quality*. Examples: 

`python progen.py "0.4 - Brass" "0.4 - Brass" "Colorfila PLA" "Colorfila PLA" --simplify3d`

Generates the file *BCN3D Sigma - 0.4 Left (PLA Colorfila), 0.4 Right (PLA Colorfila).fff*

`python progen.py "0.4 - Brass" "0.4 - Brass" "Colorfila PLA" "Colorfila PLA" "Standard" --cura`

Generates the file *BCN3D Sigma - 0.4 Left (PLA Colorfila), 0.4 Right (PLA Colorfila) - Standard.ini*


## Editing *resources* files

Hotends
```json5
{
    "id": "0.4mm - Brass",          //         Hotend Name
    "nozzleSize": 0.4,              // [mm]    Inner diameter of the nozzle
    "nozzleTipOuterDiameter": 0.99, // [mm]    Outer diameter of the tip of the nozzle
    "nozzleHeadDistance": 3.5,      // [mm]    Height difference between the tip of the nozzle and the lowest part of the print head
    "nozzleExpansionAngle": 46.68,  // [º]     Angle between the horizontal plane and the conical part right above the tip of the nozzle
    "material": "Brass",            //         Nozzle material
    "temperatureCompensation": 0,   // [C]     Temperature compensation for this hotend, sometimes the hotend needs to print always some degrees higher or lower
    "hotBlock": "Standard",         //         Block style
    "timeToHeatUp150To300": 99,     // [s]     Time to heat from 150C to 300C
    "timeToCoolDown300To150": 69,   // [s]     Time to cooldown from 300C to 150C
    "minimumCoolHeatTimeWindow": 5  // [s]     Minimal time an extruder has to be inactive before the nozzle is cooled
}
```

Filaments
```json5
{
    "id": "Colorfila PLA",          //         Filament Name
    "brand": "Colorfila",           //         Filament Manufacturer
    "material": "PLA",              //         Material type
    "color": "Generic",             //         Color name
    "colorCode": "#ffc924",         //         HTML color code
    "filamentDiameter": 2.85,       // [mm]
    "filamentPricePerKg": 19.95,    // [€]
    "filamentDensity": 1.25,        // [g/cm3]
    "isSupportMaterial": false,     //
    "isFlexibleMaterial": false,    // 
    "isAbrasiveMaterial": false,    // 
    "bedTemperature": 50,           // [C]
    "printTemperature": [200, 220], // [C]     Minimum and maximum print temperatures
    "standbyTemperature": 150,      // [C]     Temperature while not printing
    "defaultPrintSpeed": 60,        // [mm/s]  Default speed when printing Standard quality with 0.4mm Nozzle and 0.2mm layer height
    "advisedMaxPrintSpeed": "None", // [mm/s]  Maximum speed recommended by filament's manufacturer. If "None", maxFlow value is needed
    "maxFlow": 15,                  // [mm3/s] Maximum flow a default Hotend can print. "None" if unknown
    "maxFlowForHighFlowHotend": 18, // [mm3/s] Maximum flow a High Flow Hotend can print. "None" if unknown
    "retractionDistance": 4,        // [mm]
    "retractionSpeed": 40,          // [mm/s]
    "fanPercentage": [50, 100],     // (0-100) Standard and maximum fan speeds
    "extrusionMultiplier": 1,       //         1.2 extrudes 120% the needed amount of filament
    "purgeLenght": 16               // [mm]    Lenght to purge at Tool Change with 0.4mm Nozzle
}
```

Quality Preconfigurations
```json5
{
    "id": "Standard",               //         Preconfiguration Name
    "index": 3,                     //         Order to show the option in Simplify3D
    "layerHeightMultiplier": 0.375, //         Multiply this value for the nozzle size to get the layer height.
    "defaultSpeed": 60,             // [mm/s]  Default speed for PLA
    "firstLayerUnderspeed": 0.67,   // (0-1)
    "outlineUnderspeed": 0.58,      // [0-1]
    "topBottomWidth": 0.8,          // [mm]    Thickness of solid layers at the top and bottom
    "wallWidth": 1.2,               // [mm]    Thickness of walls
    "infillPercentage": 20          // (0-100)
}
```
 