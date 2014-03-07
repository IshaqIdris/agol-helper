
import agol
import arcpy
import sys, os, datetime
import ConfigParser

from arcpy import env

from agol import common
from agol import featureservice
from agol import layer

from arcpyhelper import helper

logFileName ='.\\logs\\outageEvent.log'
configFilePath =  '.\\configs\\OutageEvent.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'

def runScript(log,config):
    try:


        # Config File
        username = config.get( 'AGOL', 'USER')
        password = config.get('AGOL', 'PASS')

        outageURL = config.get('FS_INFO', 'OUTAGESERVICE')
        outageDelSQL = config.get('FS_INFO', 'OUTAGEDELETESQL')
        eventsURL = config.get('FS_INFO', 'EVENTSERVICE')
        eventDelSQL = config.get('FS_INFO', 'EVENTDELETESQL')

        outageAreaLayer = config.get('LOCAL_DATA', 'OUTAGELAYER')
        outageAreaCustOutField = config.get('LOCAL_DATA', 'CUSTOMERSOUTFIELD')
        outageAreaCustInField = config.get('LOCAL_DATA', 'CUSTOMERSINFIELD')
        outageAreaTotCustField = config.get('LOCAL_DATA', 'TOTALCUSTOMERSFIELD')
        outageAreaPercOutField = config.get('LOCAL_DATA', 'PERCENTOUTFIELD')
        outageAreaRptDate = eval(config.get('LOCAL_DATA', 'DATEFIELD'))

        eventLayer = config.get('LOCAL_DATA', 'EVENTSLAYER')
        eventCustCntField = config.get('LOCAL_DATA', 'CUSTOMERCOUNTFIELD')

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

        fieldString = outageAreaCustOutField + " " + outageAreaCustOutField + " true true false 4 Long 0 0 ,Sum,#," + eventLayer + "," + eventCustCntField + ",-1,-1"

        arcpy.SpatialJoin_analysis(outageAreaLayer, eventLayer, outageAreaJoinedToEvents, 'JOIN_ONE_TO_ONE', 'KEEP_ALL',fieldString,"INTERSECT","#","#")
        print "Spatial Join Complete"

        #Join the spatial join to the source data and copy the customer count information
        helper.JoinAndCalc(outageAreaLayer,"OBJECTID",outageAreaJoinedToEvents,"TARGET_FID",[(outageAreaCustOutField,outageAreaCustOutField)])

        print "Outage Counts Calculated"

        if helper.FieldExist(outageAreaLayer,[outageAreaCustInField,outageAreaTotCustField]):
            # Process: Calc Number In
            arcpy.CalculateField_management(outageAreaLayer, outageAreaCustInField, "!" + outageAreaTotCustField +"!- !" + outageAreaCustOutField + "!", "PYTHON_9.3", "")
            print "Number of people in service calculated"

        if helper.FieldExist(outageAreaLayer,[outageAreaCustInField,outageAreaTotCustField,outageAreaPercOutField]):

            # Process: Calc Percent Out
            arcpy.CalculateField_management(outageAreaLayer, outageAreaPercOutField, "calc( !" + outageAreaCustOutField +"!, !" + outageAreaTotCustField +"! )", "PYTHON_9.3", "def calc(numout,numserv):\\n  if numout == 0:\\n    return 0\\n  else:\\n    return round(float((float(numout) / float(numserv)) *100),2)")
            print "Percentage out calculated"

        if helper.FieldExist(outageAreaLayer,[outageAreaRptDate[0]]):
            # Process: Set Time
            tz = time.timezone
            dateExp = "import time\\nimport datetime\\nfrom time import mktime\\nfrom datetime import datetime\\ndef calc(dt):\\n  return datetime.fromtimestamp(mktime(time.strptime(str(dt), '" + str(outageAreaRptDate[1]) + "')) + " + str(tz) + ")"
            exp =  "calc('" + datetime.datetime.now().strftime(str(outageAreaRptDate[1])) + "')"
            arcpy.CalculateField_management(outageAreaLayer,outageAreaRptDate[0], exp, "PYTHON_9.3", dateExp)
            print "Report time set"



        fs = layer.FeatureLayer(url=outageURL,
                        username=username,
                        password=password)

        fs.deleteFeatures(sql=outageDelSQL)
        print "Outage Polygon layer cleared"

        results = fs.addFeatures(fc=outageAreaLayer)

        print "Outage Polygon layer features added"

        fs.url = eventsURL
        fs.deleteFeatures(eventDelSQL)

        print "Event location layer cleared"
        fs.addFeatures(fc=eventLayer)

        print "Event location layer features added"

    except helper.HelperError,e:
        line, filename, synerror = helper.trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror
        print "Add. Error Message: %s" % e
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    except arcpy.ExecuteError:

        line, filename, synerror = helper.trace()
        print "error on line: %s" % line
        print "error in file name: %s" % filename
        print "with error message: %s" % synerror
        print "ArcPy Error Message: %s" % arcpy.GetMessages(2)
        print datetime.datetime.now().strftime("%Y-%m-%d %H:%M")


    except:
        line, filename, synerror = helper.trace()
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
    sys.stdout = helper.Tee(sys.stdout, log)

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
