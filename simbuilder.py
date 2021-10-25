#Skellig
#DeltaV Expression Builder for Simulation Modules
#Rev: 2.0

#Importing Python Libraries
import time
import numpy as np
import pandas as pd
import fhxutilities as util

#Importing config files
import fhxconstants as const

#Declaring functions
def GenerateExpression(finalLogic, moduleName, classArray, varAssign):
    '''
    Builds expression and saves to final logic dictionary. Also saves 
    module names assigned to variables.
    Updates final logic and variable assigned in-place.
    '''
    global varValCount
    
    fbsToSimStr = classArray[COL_FBS_TO_SIM]
    
    #Exit if no function blocks to simulate
    if pd.isna(fbsToSimStr):
        return
    
    fbsToSim = fbsToSimStr.split(',')
    fileType = classArray[COL_FILE_TYPES]
    
    varNumLen = len(VAR_DUMMY_VAL)
    
    #Loop through function blocks in list
    for fb in fbsToSim:
        expList = expressionCode[fb]
        
        #Loop through expression lines in list
        for exp in expList:
                if VAR_DUMMY in exp:
                    initVal = ''.join(['0' * varNumLen, str(varValCount)])
                    var = ''.join([VAR_INIT_CHARS, initVal[-1 * varNumLen:]])
                    
                    exp = exp.replace(VAR_DUMMY, var)
                    
                    varAssign[var] = moduleName
                    varValCount += 1
                    
                finalLogic[fileType] += INIT_EXP_TEXT + moduleName + exp + '\r'
    
    finalLogic[fileType] += '\r'

def BuildFiles(finalLogic, moduleFileName):
    '''
    Builds export text files from logic.
    '''
    exportFileNames = []
    
    #Loop through file types
    for fileType in finalLogic:
        expressionLogic = finalLogic[fileType]
        
        #If expression is not empty
        if expressionLogic:
            #Create file name, build new file, add expression text, close file
            fileName = moduleFileName[:-4] + '_' + fileType + 's_' + time.strftime("%Y%m%d-%H%M%S") + '.txt'
            file = open(fileName, 'w+', encoding='ansi')
            file.write(expressionLogic)
            file.close()
            
            #Save file name for final message
            exportFileNames.append(fileName)
    
    return exportFileNames

def UpdateParameterValue(fhxLines, idx, paramName, paramValue, isStringVal=None):
    '''
    Updates a single parameter's value in fhx lines.
    Updates fhx lines in-place.
    '''
    paramAttrNameID = 'ATTRIBUTE NAME="'
    paramInstNameID = 'ATTRIBUTE_INSTANCE NAME="'
    instEndID = '  }'
    paramCvID = 'CV='
    fbNameID = 'FUNCTION_BLOCK NAME="'
    closeValue = ' }'
    typeID = 'TYPE='
    expNameID = '/T_EXPRESSION'
    defID = 'DEFINITION="'
    endID = '}'
    strType = 'UNICODE_STRING'
    actType = 'ACT'
    valueActExp = '    VALUE { TYPE=ACTION EXPRESSION="'
    
    isStringVal = isStringVal or False
    
    #Add quotes to parameter value if parameter type is string
    if isStringVal:
        paramValue = util.AddQuotes(paramValue)
    
    endIdx = fhxLines[idx:].index(endID)
    lines = '\n'.join(fhxLines[idx:endIdx])
    
    attrIdx = lines.index(paramAttrNameID + paramName)
    fbIdx = lines.index(fbNameID + paramName)
    if attrIdx > 0:
        paramType = util.FindString(lines, attrIdx, typeID, '\n')
    if fbIdx > 0:
        paramType = util.FindString(lines, fbIdx, defID)
    if paramType == strType:
        paramValue = util.AddQuotes(paramValue)
        
    if paramType == actType:
        paramName = ''.join([paramName, expNameID])
        
        paramValue = paramValue.join([valueActExp, '"'])
        
    varIdx = lines.index(paramInstNameID + paramName)
    valueIdx = idx + lines[:varIdx].count('\n') + 2
    
    if paramType == actType:
        valueEndIdx = fhxLines[valueIdx:].index(instEndID)
        expLines = paramName.split('\n')
        existExpLines = fhxLines[valueIdx: valueEndIdx]
        
        
        if len(existExpLines) == len(expLines):
            fhxLines[valueIdx: valueEndIdx] = expLines
        elif: 
    
    if paramType == strType:
        valueRow = fhxLines[valueidx]
        valueIdx = valueRow.index(paramCvID) + len(paramCvID)
        
        fhxLines[valueidx] = ''.join([valueRow[:valueIdx], paramValue, closeValue])
        

def UpdateExpression(fhxLines, idx, blkName, exp):
    '''
    Updates a single fb expression in fhx lines.
    Updates fhx lines in-place.
    '''
    paramInstNameID = 'ATTRIBUTE_INSTANCE NAME="'
    expID = 'EXPRESSION="'
    
    
    
#Declare constants
if True:
    #Constants for expression text
    SIM_ENAB = 2
    SIM_VAL = 50
    SIM_STATUS = 128
    SIM_MASK = 0
    IGNPV_VAL = 1
    INIT_EXP_TEXT = "'//"
    
    #Constants for spreadsheet column names
    COL_MODULE_CLASS = 'Module Class'
    COL_FBS_TO_SIM = 'Blocks to Simulate'
    COL_FILE_TYPES = 'File Type'
    
    AI_FILE_TYPE = 'AI'
    AO_FILE_TYPE = 'AO'
    DI_FILE_TYPE = 'DI'
    DO_FILE_TYPE = 'DO'
    VLV_FILE_TYPE = 'VLV'
    MTR_FILE_TYPE = 'MTR'
    PID_FILE_TYPE = 'PID'
    FILE_TYPES = [AI_FILE_TYPE, 
                  AO_FILE_TYPE,
                  DI_FILE_TYPE,
                  DO_FILE_TYPE,
                  VLV_FILE_TYPE,
                  MTR_FILE_TYPE,
                  PID_FILE_TYPE]
    
    #Constants for initial value parameters
    VAR_INIT_CHARS = 'TP'
    VAR_DUMMY_VAL = '000'
    VAR_DUMMY = ''.join([VAR_INIT_CHARS, VAR_DUMMY_VAL])
    VAR_INIT_VAL = 11
    VAR_NAME_DESC = '_DESC'
    VAR_NAME_VAL = '_VALUE'
    VAR_NAME_MIN = '_MIN'
    VAR_NAME_MAX = '_MAX'
    VAR_INIT_VAL_TXT = 'Initial Value'
    
    #Determines order intial value variables will be assigned based on class type
    VAR_ORDER = ('DI', 'DO', 'AI', 'AO', 'VLV', 'MTR', 'PID')
    
    #Name for simulation module template fhx file
    SIM_MOD_NAME = 'SIM_MOD_TEMPLATE'
    
    #Action block names in simulation module
    AI_ACT_BLK_NAME = 'SIM_AI'
    AO_ACT_BLK_NAME = 'SIM_AO'
    DI_ACT_BLK_NAME = 'SIM_DI'
    DO_ACT_BLK_NAME = 'SIM_DO'
    VLV_ACT_BLK_NAME = 'SIM_VLV'
    MTR_ACT_BLK_NAME = 'SIM_MTR'
    PID_ACT_BLK_NAME = 'SIM_PID'

#Build file type to action block name map
typeToActionName = {AI_FILE_TYPE: AI_ACT_BLK_NAME,
                    AO_FILE_TYPE: AO_ACT_BLK_NAME
                    DI_FILE_TYPE: DI_ACT_BLK_NAME
                    DO_FILE_TYPE: DO_ACT_BLK_NAME
                    VLV_FILE_TYPE: VLV_ACT_BLK_NAME
                    MTR_FILE_TYPE: MTR_ACT_BLK_NAME
                    PID_FILE_TYPE: PID_ACT_BLK_NAME}
    
#Build expression lists and dictionary
DIExpressionList = [f"/DI1/SIMULATE_D.ENABLE' := {SIM_ENAB};",
                    f"/DI1/SIMULATE_D.SVALUE' := '^/INIT_VALS/{VAR_INIT_CHARS}{VAR_DUMMY_VAL}_VALUE.CV';",
                    f"/DI1/SIMULATE_D.SSTATUS' := {SIM_STATUS};"]
DOExpressionList = [f"/DO1/SIMULATE_D.ENABLE' := {SIM_ENAB};",
                    f"/DO1/SIMULATE_D.SSTATUS':= {SIM_STATUS};"]
AIExpressionList = [f"/AI1/SIMULATE.ENABLE':= {SIM_ENAB};", 
                    f"/AI1/SIMULATE.SVALUE':= '^/INIT_VALS/{VAR_INIT_CHARS}{VAR_DUMMY_VAL}_VALUE.CV';", 
                    f"/AI1/SIMULATE.SSTATUS':= {SIM_STATUS};"]
AOExpressionList = [f"/AO1/SIMULATE.ENABLE':= {SIM_ENAB};", 
                    f"/AO1/SIMULATE.SSTATUS':= {SIM_STATUS};"]
EDCExpressionList = [f"/EDC1/IGNORE_PV.CV' := {IGNPV_VAL};"]
PIDExpressionList = [f"/PID1/SIMULATE.ENABLE':= {SIM_ENAB};", 
                    f"/PID1/SIMULATE.SVALUE':= '^/INIT_VALS/{VAR_INIT_CHARS}{VAR_DUMMY_VAL}_VALUE.CV';", 
                    f"/PID1/SIMULATE.SSTATUS':= {SIM_STATUS};"]
expressionCode = {'DI': DIExpressionList,
                  'DO': DOExpressionList,
                  'AI': AIExpressionList,
                  'AO': AOExpressionList,
                  'EDC': EDCExpressionList,
                  'PID': PIDExpressionList}

#Prompt for class info file name
classFileName = input('\nEnter name of the Class Information spreadsheet (.xlsx) without file extension.\n') + '.xlsx'

#Import classes and set index
classDf = pd.read_excel(classFileName)
classDf.set_index(COL_MODULE_CLASS, inplace=True)
classes = classDf.index

#Prompt for module file name
moduleFileName = input('\nEnter name of the DeltaV Export (.fhx) file without file extension.\n') + '.fhx'

#Build list of strings from file
fhxLines = util.BuildLinesFromFhx(moduleFileName)

#Save sections of fhx as paragraph objects
[modules] = util.SaveParagraphs(fhxLines, [const.MODULES])

#Build module data from fhx lines and module objects
moduleData = []

for module in modules:
    moduleName = module.name
    className = util.FindString(fhxLines[module.idx], 'MODULE_CLASS="')
    
    if className in classes:
        classType = classDf.at[className, COL_FILE_TYPES]
    else:
        classType = ''
    
    #Append module to module data dictionary
    moduleData.append({'Name': moduleName, 'Class': className, 'Type': classType})

#Sort module data alphabetically then by class type
DetermineOrder = lambda module: VAR_ORDER.index(module['Type']) if module['Type'] in VAR_ORDER else 999
moduleData.sort(key = DetermineOrder)

#Build dictionary for final logic
#fileTypes = classDf[COL_FILE_TYPES].tolist()
finalLogic = dict.fromkeys(FILE_TYPES, '')

#Loop through modules and add generate expression to final logic
moduleClassesNotFound = []
varAssign = {}
varValCount = VAR_INIT_VAL

for module in moduleData:
    moduleName = module['Name']
    className = module['Class']
    
    #If class exists in spreadsheet, then generate expression logic
    if className in classDf.index:
        classArray = classDf.loc[className]
        
        GenerateExpression(finalLogic, moduleName, classArray, varAssign)
    
    #Record error
    else:
        moduleClassesNotFound.append({'Name': moduleName, 'Class': className})

#Build list of strings from simulation module template file
simFhxLines = util.BuildLinesFromFhx(SIM_MOD_NAME)

#Create initial values composite object
[fbDefinitions] = util.SaveParagraphs(simFhxLines, [FB_DEF])
initVals = fbDefinitions[0]

#Update description of variables in initial values composite
initValIdx = initVals.idx

for var in varAssign.keys():
    varName = ''.join([var, VAR_NAME_DESC])
    desc = ' '.join([varAssign[var], VAR_INIT_VAL_TXT])
    
    UpdateParameterValue(simFhxLines, initValIdx, varName, desc, isStringVal=True)

#Update action expressions
for fileType in finalLogic.keys():
    expressionLogic = finalLogic[fileType]
    actBlkName = typeToActionName[fileType]
    
    if expressionLogic:
        UpdateParameterValue(simFhxLines, 0, actBlkName, expressionLogic)

#Save expression logic to text files
exportFileNames = BuildFiles(finalLogic, moduleFileName)

#Build final message
finalMessage = '\nThe following files have been built:'
for fileName in exportFileNames:
    finalMessage += '\n' + fileName

if moduleClassesNotFound:
    finalMessage += "\n\nThe following module classes were not found in spreadsheet " + classFileName + ':'
    for module in moduleClassesNotFound:
        finalMessage += ''.join(['\nModule:', module['Name'], '  Class: ', module['Class']])

#Display final message
print(finalMessage)