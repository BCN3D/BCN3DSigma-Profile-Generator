# BCN3DSigma-Profile-Generator
Profile Generator for Simplify3D slicing software. Specifically designed for the BCN3D Sigma.

The python script is capable of generating Simplify3D profiles according to the nozzle sizes, materials and qualities defined in ProfilesData.json

## Requirements

- Have python 2.7 installed.
- Have ProfilesData.json file with at least one Nozzle size, one filament and one quality preconfiguration. Note the included one comes with all Nozzle sizes, materials and qualities we have tested.

## Usage

first you need to clone/download the repository in your computer:

`git clone https://github.com/BCN3D/BCN3DSigma-Profile-Generator`

Decompress it if you need to, open a terminal and go to the directory:

`python Simplify3D-SigmaProfileGenerator.py`

will ask for a functionality:
> 1. Generate a bundle of profiles
> 2. Generate one single profile
> 3. Show available options
> 4. Test all combinations
> 5. Exit

Pick the desired option by writting its number.

###### 1. Generate a bundle of profiles
  Creates a compressed zip file with all possible combinations available in ProfilesData.json.
  The package includes a csv file with useful data of each combination created and all the fff profile files ordered following a folder tree.

###### 2. Generate one single profile
  Will ask for left nozzle size, left loaded filament, right nozzle size and right loaded filament. Then will generate the fff profile file.

###### 3. Show available options
  Prints all the options available inside ProfilesData.json.

###### 4. Test all combinations
  Like *1. Generate a bundle of profiles* but without storing data neither generating fff profile files. A fast option if you just want to ensure all combinations can be properly created.

###### 5. Exit
  Quit the program.

In order to add, remove or change a nozzle size, filament or quality preconfiguration edit the file ProfileData.json

## TO-DO

- [ ] Availability to generate profiles for Cura
- [ ] Better print speed management for flexible materials
