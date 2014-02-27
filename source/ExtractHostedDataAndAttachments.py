
import agol
import arcpy
import sys, os, datetime
import ConfigParser

from agol import Utilities
from agol import services

from arcpy import env
from agol.Utilities import FeatureServiceError
from agol.Utilities import UtilitiesError

logFileName ='.\\logs\\extractData.log'
configFilePath =  '.\\configs\\ExtractHostedData.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'

def runScript(log,config):
    try:


        # Config File
        username = config.get( 'AGOL', 'USER')
        password = config.get('AGOL', 'PASS')

        serviceUrl = config.get('FS_INFO', 'SERVICEURL')

        print "Config file loaded"
        fs = services.FeatureService(url=serviceUrl,username=username,password=password)
        fs.extractDataUsingSync(r"c:\temp\AttachmentTest\AttachmentTest.gdb", "grid", "attachments", attachment_folder=r"c:\temp\AttachmentTest")


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
