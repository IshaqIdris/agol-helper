import os
import arcpy
import time
import datetime
import inspect
from time import gmtime, strftime

class HelperError(Exception):
    """ raised when error occurs in utility module functions """
    pass

#----------------------------------------------------------------------
def trace():
    """
        trace finds the line, the filename
        and error message and returns it
        to the user
    """
    import traceback
    import sys
    tb = sys.exc_info()[2]
    tbinfo = traceback.format_tb(tb)[0]
    filename = inspect.getfile( inspect.currentframe() )
    # script name + line number
    line = tbinfo.split(", ")[1]
    # Get Python syntax error
    #
    synerror = traceback.format_exc().splitlines()[-1]
    return line, filename, synerror
#----------------------------------------------------------------------
class Tee(object):
    """ Combines standard output with a file for logging"""

    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            f.write(obj)
#----------------------------------------------------------------------

def JoinAndCalc(inputDataset, inputJoinField, joinTable, joinTableJoinField,copyFields):
    try:
        inputLayer = "inputLayer"
        arcpy.MakeFeatureLayer_management (inputDataset, inputLayer)

        joinTableDesc = arcpy.Describe(joinTable)
        joinName = str(joinTableDesc.name)
        arcpy.AddJoin_management(inputLayer, inputJoinField, joinTable, joinTableJoinField)
        removeJoin = True

        tz = time.timezone # num of seconds to add to GMT based on current TimeZone
##        fields = arcpy.ListFields(inputLayer)
##        for field in fields:
##            print("{0} is a type of {1} with a length of {2}"
##                .format(field.name, field.type, field.length))
        for copyField in copyFields:
            if len(copyField) == 3:
                dateExp = "import time\\nimport datetime\\nfrom time import mktime\\nfrom datetime import datetime\\ndef calc(dt):\\n  return datetime.fromtimestamp(mktime(time.strptime(str(dt), '" + str(copyField[2]) + "')) +  time.timezone)"
                exp =  'calc(!' + joinName +'.' + copyField[0] + '!)'
                arcpy.CalculateField_management(inputLayer,copyField[1], exp, 'PYTHON_9.3', dateExp)

            else:
                arcpy.CalculateField_management(inputLayer,copyField[1], '!' + joinName +'.' + copyField[0] + '!', "PYTHON_9.3", "")

            print copyField[0] + " Calculated from " + copyField[1]

        arcpy.RemoveJoin_management(inputLayer,joinName)
    except arcpy.ExecuteError:
        line, filename, synerror = trace()
        raise HelperError({
                    "function": "JoinAndCalc",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                    "arcpyError": arcpy.GetMessages(2),
                                    }
                                    )
    except:
        line, filename, synerror = trace()
        raise HelperError({
                    "function": "JoinAndCalc",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )

def FieldExist(featureclass, fieldNames):
    """FieldExist(dataset, [fieldNames])

       Determines if the array of fields exist in the dataset

         dataset(String):
       The specified feature class or table whose indexes will be returned.

         fieldNames{Array}:
       The the array of field name to verify existance."""
    try:
        fieldList = arcpy.ListFields(featureclass)
        fndCnt = 0
        for field in fieldList:
            if field.name in fieldNames:
                fndCnt = fndCnt + 1

            if fndCnt == len(fieldNames):
                return True
        if fndCnt != len(fieldNames):
                return False

    except:
        line, filename, synerror = trace()
        raise HelperError({
                    "function": "FieldExist",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )



def currentToPrevious(inputDataset,fieldsPairs):
    """currentToPrevious(dataset, [{ToField,FromField},])

    Copies values from one field to another field

     dataset(String):
    The specified feature class or table

     fieldPairs{Array of Field Tuples}:
    The the array of field name to verify existance."""

    try:
        for fieldsPair in fieldsPairs:

            print fieldsPair[0] + " Calculated from " + fieldsPair[1]
            arcpy.CalculateField_management(inputDataset,fieldsPair[0], '!' + fieldsPair[1] + '!', "PYTHON_9.3", "")

    except:
        line, filename, synerror = trace()
        raise UtilitiesError({
                    "function": "currentToPrevious",
                    "line": line,
                    "filename":  filename,
                    "synerror": synerror,
                                    }
                                    )