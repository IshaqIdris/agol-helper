
import agol
import arcpy
import sys, os, datetime
import ConfigParser

from agol import Utilities
from agol import services

from arcpy import env
from agol.Utilities import FeatureServiceError
from agol.Utilities import UtilitiesError

logFileName ='.\\logs\\ParcelUpdate.log'
configFilePath =  '.\\configs\\UpdateCommunityParcels.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'

def runScript(log,config):
    try:

        # Config File
        username = config.get( 'AGOL', 'USER')
        password = config.get('AGOL', 'PASS')
        inputData = config.get('LOCAL_DATA', 'INPUTDATA')
        createCurrent = config.get('LOCAL_DATA', 'CREATECURRENT')
        reportCurrentURL = config.get('FS_INFO', 'REPORTCURRENTURL')
        deleteSQL = config.get('FS_INFO', 'DELETESQL')

        print "Config file loaded"

        if arcpy.Exists(inputData) == False:
            print "Input Data Does Not Exist, exiting"
            sys.exit()

        #Update Current service if used
        if createCurrent == "True":
            fs.url = reportCurrentURL
            fs.deleteFeatures(deleteSQL)
            print "Current service reset"
            fs.addFeatures(inputData)
            print "Current service updated"

    except FeatureServiceError,e:
        line, filename, synerror = Utilities.trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror
        print "Add. Error Message: %s" % e
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    except UtilitiesError, e:
        line, filename, synerror = Utilities.trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror
        print "Add. Error Message: %s" % e
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    except arcpy.ExecuteError:

        line, filename, synerror = Utilities.trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror
        print "ArcPy Error Message: %s" % arcpy.GetMessages(2)
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


    except:
        line, filename, synerror = Utilities.trace()
        print ("error on line: %s" % line)
        print ("error in file name: %s" % filename)
        print ("with error message: %s" % synerror)
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


if __name__ == "__main__":




    #Load the config file

    if os.path.isfile(configFilePath):
        config = ConfigParser.ConfigParser()
        config.read(configFilePath)
    else:
        print "INI file not found."
        sys.exit()

    #Run the script

    runScript(log,config)
    print datetime.datetime.now().strftime(dateTimeFormat)
    print "###############Script Completed#################"
    print ""
    log.close()
