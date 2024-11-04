# Minecraft Music Extractor

This is a simple python program which will extract all of the music tracks from your latest minecraft install, automatically to a folder of your choice.  

---
### Requirements
1. you know where your minecraft folder is
2. you have python 3 installed

---
### Why was this necessary?

The way that minecraft stores its files makes extracting them difficult to do by hand.  While the files aren't encrypted or stored in strange formats, they are all stored as their file hashs.  I *think* this is to make storing all of the different game assets in the same folder structure for different versions, while allowing for file version updates, but not changing the actual asset names possible and convenient.  Each version of the game comes with a new json based index file containing the necessary lookup values to go from the asset name and path to the hash file name.  The program simply finds the latest version of that file, and does all the table lookups for you.  

---
### Usage
**example**: 
python3 extractor.py /home/user/.minecraft/ /home/user/Music/minecraft-music

this will copy all of the music from the lastest version of the game to the folder /home/user/Music/minecraft

**syntax**:
python3 extractor.py [minecraft folder] [output folder]

the program will copy the music files from the latest version of minecraft installed in the [minecraft folder] to the [output folder]

---
### Note
this program was inspired by the program listings here: [wiki](https://minecraft.fandom.com/wiki/Tutorials/Sound_directory) The main difference is that this version targets *only* music tracks, rather than **all** sound files.  

Also, it will replace all underscores in the output file names with spaces for better readiblity.