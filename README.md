# BCN3DSigma-Profile-Generator
Profile Generator for Simplify3D & Cura slicing softwares. Specifically designed for the BCN3D Sigma.

The python script is capable of generating profiles according to nozzle sizes, materials and qualities defined in *Profiles Data* folder.

*Note this is an early version of the script. Although profiles are precisely calculated there may be some combinations where quality can still be improved.*

## Requirements

- Python 2.7 installed.
- *Profiles Data* folder with at least one Nozzle size, one filament and one quality preset. The included one comes with all Nozzle sizes, materials and qualities we have tested.

## Usage

Clone/download the repository in your computer:

`git clone https://github.com/BCN3D/BCN3DSigma-Profile-Generator`

Decompress it if you need to, open a terminal, go to the directory and call the script: 

`python SigmaProfileGenerator.py`

Will ask for a functionality:

1. **Simplify3D: Generate a bundle of profiles:** Combines all Hotends, Filaments and Quality Preconfigurations stored in *Profiles Data* folder to create a  zip file with all profiles available. The package also includes a csv file with useful data of each combination created.

2. **Simplify3D: Generate one single profile:** Will ask for left Hotend, left loaded Filament, right Hotend and right loaded Filament. Then will generate the fff profile file.

3. **Cura: Generate a bundle of profiles:** Same as *1*, now for Cura.

4. **Cura: Generate one single profile:** Same as *2*, now for Cura (will ask for Quality at the end).

5. **Test all combinations:** Without storing any data neither generating profile files. A fast option to just ensure all combinations can be properly created.

6. **Exit:** Quit the program.

In order to add, remove or change a nozzle size, filament or quality preconfiguration edit the files in *Profiles Data* folder.

### **Fast mode (No GUI)**

To generate a profile without entering the GUI. 

Simplify3D: call the script and insert 4 valid parameters:

`python SigmaProfileGenerator.py LHotend RHotend LFilament RFilament --software`

Cura: call the script and insert 5 valid parameters:

`python SigmaProfileGenerator.py LHotend RHotend LFilament RFilament Quality --software`

Valid parameters for Hotends are filenames in */Profiles Data/Hotends* or 'None' if not mounted. Valid parameters for Fiaments are filenames in */Profiles Data/Filaments* or 'None' if empty. Valid parameters for Quality are filenames in */Profiles Data/Quality Presets*. Examples: 

`python SigmaProfileGenerator.py "0.4 - Brass" "0.4 - Brass" "Colorfila PLA" "Colorfila PLA" --simplify3d`

Generates the file *BCN3D Sigma - 0.4 Left (PLA Colorfila), 0.4 Right (PLA Colorfila).fff*

`python SigmaProfileGenerator.py "0.4 - Brass" "0.4 - Brass" "Colorfila PLA" "Colorfila PLA" "Medium" --cura`

Generates the file *BCN3D Sigma - 0.4 Left (PLA Colorfila), 0.4 Right (PLA Colorfila) - Medium.ini*


## Editing *Profiles Data* files

Hotends
```json5
{
    "id": "0.4mm - Brass", 					// Hotend Name
    "nozzleSize": 0.4,						// [mm]
    "material": "Brass",					// Nozzle material
    "hotBlock": "Standard"					// Block style
} 
```

Filaments
```json5
{
    "id": "PLA Colorfila",					// Filament Name
    "filamentDiameter": 2.85,				// [mm]
    "filamentPricePerKg": 19.95,			// [€]
    "filamentDensity": 1.25,				// [g/cm3]
    "isSupportMaterial": false,				// true/false
    "isFlexibleMaterial": false,			// true/false
    "bedTemperature": 50,					// [ºC]
    "printTemperature": [195, 225],			// [ºC],    minimum and maximum print temperatures.
    "defaultPrintSpeed": 60,				// [mm/s],  default speed when printing Medium quality with 0.4mm Nozzle and 0.2mm layer height.
    "advisedMaxPrintSpeed": "None",			// [mm/s],  maximum speed recommended by filament's manufacturer. If "None", maxFlow value is needed.
    "maxFlow": 15,							// [mm3/s], maximum flow a default Hotend can print. "None" if unknown.
    "maxFlowForHighFlowHotend": "None",	    // [mm3/s], maximum flow a High Flow Hotend can print. "None" if unknown.
    "retractionDistance": 4,				// [mm]
    "retractionSpeed": 40,					// [mm/s]
    "fanPercentage": 100,					// [0-100]
    "extrusionMultiplier": 1,				// 1.2 extrudes 120% the needed amount of filament.
    "purgeLenght": 1.5 						// [mm],    lenght to purge at Tool Change with 0.4mm Nozzle.
}
```

Quality Preconfigurations
```json5
{
    "id": "Medium",							// Preconfiguration Name
    "index": 2,								// Order to show the option in Simplify3D
    "layerHeightMultiplier": 0.5,			// Multiply this value for the nozzle size to get the layer height.
    "defaultSpeed": 60,						// [mm/s],  default speed for PLA
    "firstLayerUnderspeed": 0.67,			// [0-1]
    "outlineUnderspeed": 0.58,				// [0-1]
    "topBottomWidth": 0.8,					// [mm],    thickness of solid layers at the top and bottom
    "wallWidth": 1.2,						// [mm],    thickness of walls
    "infillPercentage": 20					// [0-100]
}
```

## TO-DO

- [ ] Fix temperature values when using dual extruder assistant.
- [x] Availability to generate Cura profiles
- [ ] Availability to create .json files right from the script
- [ ] Better print speed management for flexible materials
- [ ] Adjust bridging for flexible materials
- [ ] Adjust coast for ABS
