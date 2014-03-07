
import agol
import arcpy
import sys, os, datetime
import ConfigParser

from agol import common

from arcpyhelper import helper

from arcpy import env


logFileName ='.\\logs\\log.log'
configFilePath =  '.\\configs\\_ExampleConfig.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'

def runScript(log,config):
    try:

        exampleConfigValue = config.get('SAMPLE', 'SETTING')
        print exampleConfigValue

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
