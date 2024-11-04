import sys, os, platform, shutil, json
from pathlib import Path
from functools import reduce
from multiprocessing import Process


projectName = "minecraft-music-extractor"
originalDir = os.getcwd()
scriptPath = Path(__file__)
scriptDir = scriptPath.parent
moveUpDegrees = lambda originalPath, amount : reduce(lambda x, y : x.parent, range(0, amount), originalPath)
potentials = list(map(lambda x : moveUpDegrees(scriptPath, x), range(0, len(scriptPath.parts))))
rootDir: Path = list(filter(lambda x : x.name == projectName, potentials))[-1] #should always grab the shortest possible, and therefore most likely to be actual root path, even if the root directory name was reused.
sys.path.append(str(rootDir))
sys.path = sorted(list(set(sys.path)))
initial = str(Process.pid)


def findMaxInstalledVersionIndexFile(indexFolder: Path) -> Path:
    """
    figures out what the max installed version of minecraft is based on the max number of the json files in the folder.

    Parameters:
        indexFolder (Path): path to the minecraft index folder

    Returns:
        (Path): path of the index file associated with the max version of minecraft installed
    """

    files = indexFolder.iterdir()
    buffer0 = list(filter(lambda x : x.is_file(), files))
    buffer1 = list(filter(lambda x : x.suffix == ".json", buffer0))
    buffer2 = list(map(lambda x : x.stem, buffer1))
    buffer3 = list(filter(lambda x : x.isdigit(), buffer2))
    buffer4 = list(map(lambda x : int(x), buffer3))
    maxVersion = max(buffer4)
    output = indexFolder / f"{maxVersion}.json"
    return output


def main(scanPath: Path, outputPath: Path) -> None:
    ''' 
    Copies audio files from indescript hashed folders to named sorted folders.
    You may need to change output path.
    '''    

    extractList = []
    assetIndexFolder = scanPath / "assets/indexes"     
    indexFilePath = findMaxInstalledVersionIndexFile(assetIndexFolder)    
    indexFileHandle = open(indexFilePath, "r")
    data = json.load(indexFileHandle)
    indexFileHandle.close()
    objects = data["objects"]

    generateLinks = lambda jsonPath : {
        'original location': scanPath / 'assets/objects' / objects[jsonPath]['hash'][:2] / objects[jsonPath]['hash'],
        'new location': outputPath / f"{str(Path(jsonPath).name)}".replace("_", " ")
    }
    
    pointers = list(objects.keys())        
    music = list(filter(lambda x : x.startswith("minecraft/sounds/music"), pointers))
    records = list(filter(lambda x : x.startswith("minecraft/sounds/records"), pointers))
    extractList.extend(music)
    extractList.extend(records)        
    links = list(map(generateLinks, extractList))
    print(links)
    results = list(map(lambda x : shutil.copyfile(x['original location'], x['new location']), links))
    print(results)



if __name__ == "__main__":
    minecraftDirAssetFile = Path(sys.argv[1])
    outputDirectory = Path(sys.argv[2])

    if not outputDirectory.exists():
        os.mkdir(outputDirectory)
    
    main(minecraftDirAssetFile, outputDirectory)
