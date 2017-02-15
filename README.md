# BCN3DSigma-Profile-Generator
Profile Generator for Simplify3D & Cura slicing softwares. Specifically designed for the BCN3D Sigma.

The official code behind the [Sigma ProGen web interface](https://www.bcn3dtechnologies.com/en/sigma-progen/). It generates profiles according to hotends, filaments and qualities defined in *Profiles Data* folder.

## Requirements

- Python 2.7 installed.
- *Profiles Data* folder with at least one hotend, one filament and one quality preset. The included one comes with all hotends, filaments and qualities we have tested.

## Usage

Clone/download the repository in your computer:

`git clone https://github.com/BCN3D/BCN3DSigma-Profile-Generator`

Decompress it if you need to, open a terminal, go to the directory and call the script: 

`python SigmaProfileGenerator.py`

Will ask for a functionality:

1. **Profile for Simplify3D:** Will ask for left Hotend, left loaded Filament, right Hotend and right loaded Filament. Then will generate the fff profile file.

2. **Profile for Cura:** Same as *1*, now for Cura (will ask for Quality at the end).

3. **Experimental features:** Some experimental extra features.

4. **Exit:** Quit the program.

In order to add, remove or change a hotend, filament or quality preconfiguration edit the files in *Profiles Data* folder.

### **Fast mode (No GUI)**

To generate a profile without entering the GUI. 

Simplify3D: call the script and insert 4 valid parameters:

`python SigmaProfileGenerator.py LHotend RHotend LFilament RFilament --software`

Cura: call the script and insert 5 valid parameters:

`python SigmaProfileGenerator.py LHotend RHotend LFilament RFilament Quality --software`

Valid parameters for Hotends are filenames in */Profiles Data/Hotends* or 'None' if not mounted. Valid parameters for Fiaments are filenames in */Profiles Data/Filaments* or 'None' if empty. Valid parameters for Quality are filenames in */Profiles Data/Quality Presets*. Examples: 

`python SigmaProfileGenerator.py "0.4 - Brass" "0.4 - Brass" "Colorfila PLA" "Colorfila PLA" --simplify3d`

Generates the file *BCN3D Sigma - 0.4 Left (PLA Colorfila), 0.4 Right (PLA Colorfila).fff*

`python SigmaProfileGenerator.py "0.4 - Brass" "0.4 - Brass" "Colorfila PLA" "Colorfila PLA" "Standard" --cura`

Generates the file *BCN3D Sigma - 0.4 Left (PLA Colorfila), 0.4 Right (PLA Colorfila) - Standard.ini*


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
    "id": "Colorfila PLA",					// Filament Name
    "filamentDiameter": 2.85,				// [mm]
    "filamentPricePerKg": 19.95,			// [€]
    "filamentDensity": 1.25,				// [g/cm3]
    "isSupportMaterial": false,				// true/false
    "isFlexibleMaterial": false,			// true/false
    "bedTemperature": 50,					// [ºC]
    "printTemperature": [195, 225],			// [ºC],    minimum and maximum print temperatures.
    "defaultPrintSpeed": 60,				// [mm/s],  default speed when printing Standard quality with 0.4mm Nozzle and 0.2mm layer height.
    "advisedMaxPrintSpeed": "None",			// [mm/s],  maximum speed recommended by filament's manufacturer. If "None", maxFlow value is needed.
    "maxFlow": 15,							// [mm3/s], maximum flow a default Hotend can print. "None" if unknown.
    "maxFlowForHighFlowHotend": "None",	    // [mm3/s], maximum flow a High Flow Hotend can print. "None" if unknown.
    "retractionDistance": 4,				// [mm]
    "retractionSpeed": 40,					// [mm/s]
    "fanPercentage": [50, 100],				// [0-100],    minimum and maximum percentage of layer fan power.
    "extrusionMultiplier": 1,				// 1.2 extrudes 120% the needed amount of filament.
    "purgeLenght": 1.5 						// [mm],    lenght to purge at Tool Change with 0.4mm Nozzle.
}
```

Quality Preconfigurations
```json5
{
    "id": "Standard",							// Preconfiguration Name
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

## Development branch

Branch where we upload beta versions. Find the latest stable version in the **Master** branch.
 