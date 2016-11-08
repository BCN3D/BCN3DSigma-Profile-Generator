# BCN3DSigma-Profile-Generator
Profile Generator for Simplify3D slicing software. Specifically designed for the BCN3D Sigma.

The python script is capable of generating Simplify3D profiles according to the nozzle sizes, materials and qualities defined in ProfilesData.json

*Note this is an early version of the script. Although profiles are precisely calculated there may be some combinations where quality can still be improved.*

## Requirements

- Have python 2.7 installed.
- Have ProfilesData.json file with at least one Nozzle size, one filament and one quality preconfiguration. Note the included one comes with all Nozzle sizes, materials and qualities we have tested.

## Usage

first you need to clone/download the repository in your computer:

`git clone https://github.com/BCN3D/BCN3DSigma-Profile-Generator`

Decompress it if you need to, open a terminal and go to the directory:

`python Simplify3D-SigmaProfileGenerator.py`

Will ask for a functionality:

1. **Generate a bundle of profiles:** Creates a compressed zip file with all possible combinations available in *ProfilesData.json*. The package includes a csv file with useful data of each combination created and all the fff profile files, ordered following a folder tree.

2. **Generate one single profile:** Will ask for left nozzle size, left loaded filament, right nozzle size and right loaded filament. Then will generate the fff profile file.

3. **Show available options:** Prints all the options available inside *ProfilesData.json*.

4. **Test all combinations:** Like *1. Generate a bundle of profiles* but without storing data neither generating fff profile files. A fast option to just ensure all combinations can be properly created.

5. **Exit:** Quit the program.

Pick the desired option by writting its number.

In order to add, remove or change a nozzle size, filament or quality preconfiguration edit the file *ProfileData.json*.

## Editing ProfilesData.json

###### Nozzle Sizes
Just add the new nozzle size to the list.

###### Filaments
Add the new material parameters:
* **id** - Filament Name
* **filamentDiameter** - [mm]
* **filamentPricePerKg** - [€]
* **filamentDensity** - [g/cm3]
* **isSupportMaterial** - true/false
* **isFlexibleMaterial** - true/false
* **bedTemperature** - [ºC]
* **printTemperature** - [ºC], a list of the minimum and maximum temperatures the manufacturer recommends.
* **defaultPrintSpeed** - [mm/s], default speed when printing Medium quality with 0.4mm Nozzle and 0.2mm layer height.
* **advisedMaxPrintSpeed** - [mm/s], maximum speed recommended by filament's manufacturer. If "None", then maxFlow value is needed.
* **maxFlow** - [mm3/s], maximum flow a normal Hotend (<0.6mm) can print. "None" if it's unknown.
* **maxFlowForHighFlowHotends** - [mm3/s], maximum flow a High Flow Hotend (>0.6mm) can print. "None" if it's unknown.
* **retractionDistance** - [mm]
* **retractionSpeed** - [mm/s]
* **fanMultiplier** - [0-1], 0 for fan off, 1 for 100% power.
* **extrusionMultiplier** - 1.2 extrudes 120% the needed amount of filament.
* **purgeMultiplier** - multiplies the standard purge lenght used for PLA with 0.4mm Nozzle.

###### Quality Preconfigurations
Add the new quality parameters:
* **id** - Preconfiguration Name
* **layerHeightMultiplier** - Multiply this value for the nozzle size to get the layer height.
* **defaultSpeed** - [mm/s], default speed for PLA
* **firstLayerUnderspeed** - [0-1], to reduce first layer speed.
* **outlineUnderspeed** - [0-1], to reduce perimeters speed.
* **topBottomWidth** - [mm], thickness of solid layers at the top and bottom
* **wallWidth** - [mm], thickness of walls
* **infillPercentage** - [0-100]

## TO-DO

- [ ] Availability to generate profiles for Cura
- [ ] Better print speed management for flexible materials
