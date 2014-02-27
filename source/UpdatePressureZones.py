
import agol
import arcpy
import sys, os, datetime
import ConfigParser

from agol import Utilities
from agol import services

from arcpy import env
from agol.Utilities import FeatureServiceError
from agol.Utilities import UtilitiesError

logFileName ='.\\logs\\UpdatePressureZonesPrev.log'
configFilePath =  '.\\configs\\UpdatePressureZonesPrev.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'

def runScript(log,config):
    try:

        # Config File
        username = config.get( 'AGOL', 'USER')
        password = config.get('AGOL', 'PASS')
        joinData = config.get('LOCAL_DATA', 'JOINDATA')
        joinDataJoinField = config.get('LOCAL_DATA', 'JOINDATAJOINFIELD')
        inputData = config.get('LOCAL_DATA', 'INPUTDATA')
        inputJoinField = config.get('LOCAL_DATA', 'INPUTJOINFIELD')
        copyFields = eval(config.get('LOCAL_DATA', 'COPYFIELDS'))
        prevFields =eval(config.get('LOCAL_DATA', 'PREVIOUSFIELDS'))
        createCurrent = config.get('LOCAL_DATA', 'CREATECURRENT')
        reportArchiveURL = config.get('FS_INFO', 'REPORTARCHIVEURL')
        reportCurrentURL = config.get('FS_INFO', 'REPORTCURRENTURL')
        deleteSQL = config.get('FS_INFO', 'DELETESQL')

        print "Config file loaded"

        if arcpy.Exists(joinData) == False:
            print "Join Data Does Not Exist, exiting"
            sys.exit()

        if arcpy.Exists(inputData) == False:
            print "Input Data Does Not Exist, exiting"
            sys.exit()

        fs = services.FeatureService(url=reportArchiveURL,username=username,password=password)
        if fs == None:
            print "Cannot find Archive Service, exiting"
            sys.exit()

        Utilities.currentToPrevious(inputData,prevFields)
        print "Existing data moved to previous fields"

        Utilities.JoinAndCalc(inputData,inputJoinField,joinData,joinDataJoinField,copyFields)
        print "Data joined and calculated"

        #Save results to historical service
        fs.addFeatures(inputData)
        print "Historical data updated"

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

    env.overwriteOutput = True
    #Create the log file
    try:
        log = open(logFileName, 'a')

    except:
        print "Log file could not be created"

    #Change the output to both the windows and log file
    original = sys.stdout
    sys.stdout = Utilities.Tee(sys.stdout, log)

    print "***************Script Started******************"
    print datetime.datetime.now().strftime(dateTimeFormat)

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
