# BCN3DSigma-Profile-Generator
Profile Generator for Simplify3D slicing software. Specifically designed for the BCN3D Sigma.

The python script is capable of generating Simplify3D profiles according to the nozzle sizes, materials and qualities defined in ProfilesData.json

*Note this is an early version of the script. Although profiles are precisely calculated there may be some combinations where quality can still be improved.*

## Requirements

- Have python 2.7 installed.
- Have ProfilesData.json file with at least one Nozzle size, one filament and one quality preconfiguration. Note the included one comes with all Nozzle sizes, materials and qualities we have tested.

## Usage

First you need to clone/download the repository in your computer:

`git clone https://github.com/BCN3D/BCN3DSigma-Profile-Generator`

Decompress it if you need to, open a terminal and go to the directory. 

### **Fast mode**

To generate a profile without entering the GUI. Just call the script and insert 4 valid parameters:

`python Simplify3D-SigmaProfileGenerator.py LHotend RHotend LFilament RFilament`

Valid parameters for Hotends are file names in */Profiles Data/Hotends* or 'None' if not mounted. Valid parameters for Fiamentsare are file in */Profiles Data/Filaments* or 'None' if empty. Example: 

`python Simplify3D-SigmaProfileGenerator.py "0.4 - Brass" "0.4 - Brass" "Colorfila PLA" "Colorfila PLA"`

Generates the file *BCN3D Sigma - 0.4 Left (PLA Colorfila), 0.4 Right (PLA Colorfila).fff*

### **GUI Mode**

To enter the GUI call the script without additional parameters:

`python Simplify3D-SigmaProfileGenerator.py`

Will ask for a functionality:

1. **Generate a bundle of profiles:** Combines all Hotends, Filaments and Quality Preconfigurations stored in *Profiles Data* folder to create a  zip file with all profiles available. The package also includes a csv file with useful data of each combination created.

2. **Generate one single profile:** Will ask for left Hotend, left loaded Filament, right Hotend and right loaded Filament. Then will generate the fff profile file.

3. **Test all combinations:** Like *1. Generate a bundle of profiles* but without storing data neither generating fff profile files. A fast option to just ensure all combinations can be properly created.

4. **Exit:** Quit the program.

In order to add, remove or change a nozzle size, filament or quality preconfiguration edit the files in *Profiles Data* folder.

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

- [ ] Availability to generate Cura profiles
- [ ] Availability to create .json files right from the script
- [ ] Better print speed management for flexible materials
- [ ] Adjust bridging for flexible materials
- [ ] Adjust coast for ABS
