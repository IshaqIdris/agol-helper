
import agol
import arcpy
import sys, os, datetime
import ConfigParser

from agol import Utilities
from agol import services

from arcpy import env
from agol.Utilities import FeatureServiceError
from agol.Utilities import UtilitiesError

logFileName ='.\\logs\\outageCustomer.log'
configFilePath =  '.\\configs\\OutageCustomer.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'

def runScript(log,config):
    try:

        username = config.get( 'AGOL', 'USER')
        password = config.get('AGOL', 'PASS')



        outageURL = config.get('FS_INFO', 'OUTAGESERVICE')
        outageDelSQL = config.get('FS_INFO', 'OUTAGEDELETESQL')


        outageAreaLayer = config.get('LOCAL_DATA', 'OUTAGELAYER')
        outageAreaCustOutField = config.get('LOCAL_DATA', 'CUSTOMERSOUTFIELD')
        outageAreaCustInField = config.get('LOCAL_DATA', 'CUSTOMERSINFIELD')
        outageAreaTotCustField = config.get('LOCAL_DATA', 'TOTALCUSTOMERSFIELD')
        outageAreaPercOutField = config.get('LOCAL_DATA', 'PERCENTOUTFIELD')
        outageAreaRptDate = eval(config.get('LOCAL_DATA', 'DATEFIELD'))

        eventLayer = config.get('LOCAL_DATA', 'EVENTSLAYER')

        print "Config file loaded"

        # Local variables:
        outageAreaJoinedToEvents = 'in_memory\AreaJoinedWithOutage'##'%scratchgdb%\AreaJoinedWithOutage'

        if arcpy.Exists(outageAreaLayer) == False:
            print "Join Data Does Not Exist, exiting"
            sys.exit()

        if arcpy.Exists(eventLayer) == False:
            print "Input Data Does Not Exist, exiting"
            sys.exit()

        # Process: Spatial Join


        arcpy.SpatialJoin_analysis(outageAreaLayer, eventLayer, outageAreaJoinedToEvents, 'JOIN_ONE_TO_ONE', 'KEEP_ALL',"","INTERSECT","#","#")
        print "Spatial Join Complete"

        #Join the spatial join to the source data and copy the customer count information
        Utilities.JoinAndCalc(outageAreaLayer,"OBJECTID",outageAreaJoinedToEvents,"TARGET_FID",[("Join_Count",outageAreaCustOutField)])

        print "Outage Counts Calculated"

        if Utilities.FieldExist(outageAreaLayer,[outageAreaCustInField,outageAreaTotCustField]):
            # Process: Calc Number In
            arcpy.CalculateField_management(outageAreaLayer, outageAreaCustInField, "!" + outageAreaTotCustField +"!- !" + outageAreaCustOutField + "!", "PYTHON_9.3", "")
            print "Number of people in service calculated"

        if Utilities.FieldExist(outageAreaLayer,[outageAreaCustInField,outageAreaTotCustField,outageAreaPercOutField]):

            # Process: Calc Percent Out
            arcpy.CalculateField_management(outageAreaLayer, outageAreaPercOutField, "calc( !" + outageAreaCustOutField +"!, !" + outageAreaTotCustField +"! )", "PYTHON_9.3", "def calc(numout,numserv):\\n  if numout == 0:\\n    return 0\\n  else:\\n    return round(float((float(numout) / float(numserv)) *100),2)")
            print "Percentage out calculated"

        if Utilities.FieldExist(outageAreaLayer,[outageAreaRptDate[0]]):
            # Process: Set Time
            tz = time.timezone
            dateExp = "import time\\nimport datetime\\nfrom time import mktime\\nfrom datetime import datetime\\ndef calc(dt):\\n  return datetime.fromtimestamp(mktime(time.strptime(str(dt), '" + str(outageAreaRptDate[1]) + "')) + " + str(tz) + ")"
            exp =  "calc('" + datetime.datetime.now().strftime(str(outageAreaRptDate[1])) + "')"
            arcpy.CalculateField_management(outageAreaLayer,outageAreaRptDate[0], exp, "PYTHON_9.3", dateExp)
            print "Report time set"


        fs = services.FeatureService(url=outageURL,
                        username=username,
                        password=password)

        fs.deleteFeatures(outageDelSQL)
        print "Outage Polygon layer cleared"

        results = fs.addFeatures(fc=outageAreaLayer)
        print "Outage Polygon layer features added"


    except FeatureServiceError,e:
        line, filename, synerror = Utilities.trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror
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
