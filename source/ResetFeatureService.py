
import agol
import arcpy
import sys, os, datetime
import ConfigParser

from agol import common
from agol import featureservice

from arcpyhelper import helper

from arcpy import env


logFileName ='.\\logs\\resetOrg.log'
configFilePath =  '.\\configs\\ResetFeatureLayers.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'

def runScript(log,config):
    try:


        # Config File
        username = config.get( 'AGOL', 'USER')
        password = config.get('AGOL', 'PASS')

        url = config.get('FS_INFO', 'FEATURESERVICE')
        serviceInfo = eval(config.get('FS_INFO', 'SERVICEINFO'))

        print "Config file loaded"

        fs = featureservice.FeatureService(url=url,username=username,password=password)

        for serItm in serviceInfo:
            result = fs.layers[int(serItm[0])].deleteFeatures(sql=serItm[1])
            print "Delete Complete: "  + serItm[0] + ": " + str(result)

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
