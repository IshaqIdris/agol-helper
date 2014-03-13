
import agol
import arcpy
import sys, os, datetime
import ConfigParser

from arcpy import env

from agol import common
from agol import featureservice
from agol import layer

from arcpyhelper import helper

logFileName ='.\\logs\\ImpactAnalysis.log'
configFilePath =  '.\\configs\\ImpactAnalysis.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'

def runScript(log,config):
    try:

        # Config File
        username = config.get( 'AGOL', 'USER')
        password = config.get('AGOL', 'PASS')
        dataToField = eval(config.get('LOCAL_DATA', 'DATATOFIELD'))
        url = config.get('FS_INFO', 'URL')
        sql = config.get('FS_INFO', 'SQL')

        print "Config file loaded"
        out_path=arcpy.env.scratchGDB + r'\temp1'
        #out_path=r'C:\temp\temp.gdb\temp1'


        fs = layer.FeatureLayer(url=url,username=username,password=password)
        if fs == None:
            print "Cannot find Service, exiting"
            sys.exit()

        fc = fs.query(where=sql,returnFeatureClass=True,out_fc=out_path)
        spJoinTemp = 'in_memory\join'

        for itm in dataToField:
            if arcpy.Exists(itm[0]):
                desc = arcpy.Describe(itm[0])
                if desc.shapeType == 'Point':
                    arcpy.SpatialJoin_analysis(fc, itm[0], spJoinTemp , 'JOIN_ONE_TO_ONE', 'KEEP_ALL',"","INTERSECT","#","#")

                    print "Spatial Join Complete"
                    #Join the spatial join to the source data and copy the customer count information
                    helper.JoinAndCalc(fc,"OBJECTID",spJoinTemp ,"TARGET_FID",[("Join_Count",itm[1])])

                elif desc.shapeType == 'Polyline':


                    arcpy.SpatialJoin_analysis(fc, itm[0], spJoinTemp , 'JOIN_ONE_TO_ONE', 'KEEP_ALL',"SHAPE_Length 'SHAPE_Length' false true true 8 Double 0 0 ,First,#," + itm[0] +",SHAPE_Length,-1,-1;SUMLEN 'SUMLEN' true true false 50 Long 0 0 ,Sum,#," + itm[0] + ",SHAPE_Length,-1,-1","INTERSECT","#","#")
                    helper.JoinAndCalc(fc,"OBJECTID",spJoinTemp ,"TARGET_FID",[("SUMLEN",itm[1])])
            else:
                print itm[0] + ' does not exist'
##        cursor = arcpy.UpdateCursor(fc)
##        row = cursor.next()
##        while row:
##            row.setValue("EStatus", 'Analyzed')
##            cursor.updateRow(row)
##            row = cursor.next()
        arcpy.CalculateField_management(fc,'EStatus', "'Analyzed'", "PYTHON_9.3", "")

        fs.deleteFeatures(sql=sql)
        fs.addFeatures(fc=fc)
        print "Scipt Complete"
        arcpy.Delete_management(out_path)



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
