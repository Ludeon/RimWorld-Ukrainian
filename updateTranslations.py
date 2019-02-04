import io
import os
import sys
from os import listdir
from os.path import isfile, join
from os import walk
import xml.etree.ElementTree as ET
import getopt

def updateKeyedTranslation(englishFilePath, translationFilePath):
    # print("Processing file: " + englishFilePath)
    resultFilePath = translationFilePath

    translatedItems = {}
    translatedLines = {}

    try:
        translationsFile = io.open(translationFilePath, encoding="utf-8", mode="r")
        translationsLines = tuple(translationsFile)
        for line in translationsLines:
            strippedLine = line.encode('utf-8').strip()
            try:
                element = ET.fromstring(strippedLine)
                translatedItems[element.tag] = element.text;
                translatedLines[element.tag] = strippedLine;
            except:
                pass
        translationsFile.close()
    except:
        pass

    resultFile = io.open(resultFilePath, encoding="utf-8", mode="w")
    englishFile = io.open(englishFilePath, encoding="utf-8", mode="r")
    englishLines = tuple(englishFile)
    for line in englishLines:
        strippedLine = line.encode('utf-8').strip()
        try:
            element = ET.fromstring(strippedLine)
            lineToWrite = "\t<!-- EN: " + element.text + " -->\n"
            resultFile.write(lineToWrite.decode("utf-8"))
            if element.tag in translatedLines:
                lineToWrite = "\t" + translatedLines[element.tag] + "\n"
                del translatedItems[element.tag]
                resultFile.write(lineToWrite.decode("utf-8"))
            else:
                lineToWrite = "\t<!-- <" + element.tag + ">" + "</" + element.tag +"> -->\n"
                resultFile.write(lineToWrite.decode("utf-8"))
        except Exception as e:
            resultFile.write(line)
    englishFile.close()

    for tag in translatedItems:
        print("Unused translation: " + os.path.basename(englishFilePath) + "->" + tag + ": " + translatedItems[tag].encode('utf-8'))
        resultFile.write("\t<!-- REMOVED FROM ORIGINAL RESOURCES -->\n".decode("utf-8"))
        lineToWrite = "\t<" + tag + ">" + translatedItems[tag].encode("utf-8") + "</" + tag + ">\n\n"
        resultFile.write(lineToWrite.decode("utf-8"))

    resultFile.write("\n".decode("utf-8"))
    resultFile.close()

def updateKeyedTranslations(pathToGameRoot, workPathToTranslation):
    print("Updating Keyed translations...")
    englishKeyedRoot = join(pathToGameRoot, "Mods/Core/Languages/English/Keyed")
    for fileName in listdir(englishKeyedRoot):
        if fileName.endswith(".xml"):
            updateKeyedTranslation(join(englishKeyedRoot, fileName), join(workPathToTranslation, "Keyed", fileName))

def handleDefTranslationFile(filePath, translationsMap):
    dirName = os.path.basename(os.path.dirname(filePath))
    fileName = os.path.basename(filePath)

    if not dirName in translationsMap:
        translationsMap[dirName] = {}

    try:
        tree = ET.parse(filePath)
        for child in tree.getroot():
            translationsMap[dirName][child.tag] = child.text
    except Exception as e:
        print("exception while parsing file: " + filePath)

def handleDefNode(node, translationsMap, nodePath):
    labelsToCheck = ['label', 'description', 'customLabel', 'text',
        'rejectInputMessage', 'onMapInstruction', 'pawnsPlural', 'leaderTitle',
        'labelTendedWell', 'labelTendedWellInner', 'labelSolidTendedWell',
        'destroyedLabel', 'destroyedOutLabel', 'oldLabel', 'labelShort',
        'gerundLabel', 'verb', 'gerundLabel', 'headerTip', 'rulesStrings',
        "pawnLabel", "labelPlural"]

    for labelName in labelsToCheck:
        elements = node.findall(labelName)
        if  len(elements) == 1:
            element = elements[0]
            value = element.text
            tagName = nodePath + "." + labelName
            translationsMap[tagName] = value

    index = 0
    for child in node:
        if child.tag == "li":
            handleDefNode(child, translationsMap, nodePath + "." + str(index))
        else:
            handleDefNode(child, translationsMap, nodePath + "." + child.tag)
        index = index + 1

def handleDefRootNode(node, translationsMap):
    for child in node:
        defName = None
        if  len(child.findall('defName')) > 0:
            element = child.findall('defName')[0]
            defName = element.text

        if defName != None:
            if not child.tag in translationsMap:
                translationsMap[child.tag] = {}

            handleDefNode(child, translationsMap[child.tag], defName)

def updateDefsTranslations(pathToGameRoot, workPathToTranslation):
    print("Updating Defs translations...")
    englishDefsRootPath = join(pathToGameRoot, "Mods/Core/Defs")
    translationsDefsRootPath = join(workPathToTranslation, "DefInjected")

    translationsMap = {}
    for root,d_names,f_names in os.walk(translationsDefsRootPath):
    	for fileName in f_names:
            if fileName.endswith(".xml"):
                handleDefTranslationFile(os.path.join(root, fileName), translationsMap)

    englishMap = {}
    for root,d_names,f_names in os.walk(englishDefsRootPath):
    	for fileName in f_names:
            if fileName.endswith(".xml"):
                defFilePath = os.path.join(root, fileName)
                # print("Processing: " + defFilePath)
                tree = ET.parse(defFilePath)
                handleDefRootNode(tree.getroot(), englishMap)

    for refName in englishMap:
        if len(englishMap[refName]):
            resultFilePath = join(workPathToTranslation, "DefInjected", refName, "translations.xml")
            if not os.path.exists(os.path.dirname(resultFilePath)):
                os.makedirs(os.path.dirname(resultFilePath))

            resultFile = io.open(resultFilePath, encoding="utf-8", mode="w")
            resultFile.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n".decode("utf-8"))
            resultFile.write("<LanguageData>\n\n".decode("utf-8"))

            sortedKeys = englishMap[refName].keys()
            sortedKeys.sort()

            for tag in sortedKeys:
                lineToWrite = "\t<!-- EN: " + englishMap[refName][tag].encode("utf-8") + " -->\n"
                resultFile.write(lineToWrite.decode("utf-8"))

                if ((refName in translationsMap) and (tag in translationsMap[refName])):
                    translation = translationsMap[refName][tag]
                    lineToWrite = "\t<" + tag + ">" + translation.encode("utf-8") + "</" + tag + ">\n"
                    del translationsMap[refName][tag]
                else:
                    lineToWrite = "\t<!-- <" + tag + "></" + tag + "> -->\n"

                resultFile.write(lineToWrite.decode("utf-8"))
                resultFile.write("\n".decode("utf-8"))

            if refName in translationsMap:
                for tag in translationsMap[refName]:
                    resultFile.write("\t<!-- REMOVED FROM ORIGINAL RESOURCES -->\n".decode("utf-8"))
                    lineToWrite = "\t<" + tag + ">" + translationsMap[refName][tag].encode("utf-8") + "</" + tag + ">\n\n"
                    resultFile.write(lineToWrite.decode("utf-8"))

            resultFile.write("</LanguageData>\n".decode("utf-8"))
            resultFile.write("\n".decode("utf-8"))
            resultFile.close()

    for refName in translationsMap:
        for tag in translationsMap[refName]:
            print("Unused translation: " + refName + "->" + tag + " = " + translationsMap[refName][tag].encode('utf-8'))

print("Running RimWorld translation update tool...")
GAME_PATH = "/Volumes/HDD/Games/SteamLibrary/steamapps/common/RimWorld/RimWorldMac.app"

if len(sys.argv) > 1:
    GAME_PATH = sys.argv[1]
else:
    print("usage:  python " + os.path.basename(__file__) + " <path_to_game_dir>")
    sys.exit(1)


if not os.path.exists(GAME_PATH):
    print("Game directory not found at path: " + GAME_PATH)
    sys.exit(1)

TRANSLATION_PATH = os.path.dirname(os.path.realpath(__file__))

updateKeyedTranslations(GAME_PATH, TRANSLATION_PATH)
updateDefsTranslations(GAME_PATH, TRANSLATION_PATH)

print("Done.")
