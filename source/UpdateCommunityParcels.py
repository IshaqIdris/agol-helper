import agol
import arcpy
import sys, os, datetime
import ConfigParser

from arcpy import env

from agol import common
from agol import featureservice
from agol import layer

from arcpyhelper import helper

logFileName ='.\\logs\\ParcelUpdate.log'
configFilePath =  '.\\configs\\UpdateCommunityParcels.ini'
dateTimeFormat = '%Y-%m-%d %H:%M'


# Script tp Update the Community Parcels AGOL feature service
def runScript(log,config):
    try:


        # Config File

        username = config.get( 'AGOL', 'USER')
        password = config.get('AGOL', 'PASS')
        LocalParcels = config.get('LOCAL_DATA', 'LOCALPARCELS')
        CommunityParcelsLocalCopy = config.get('LOCAL_DATA', 'COMMUNITYPARCELSLOCALCOPY')
        url = config.get('FS_INFO', 'URL')
        deleteSQL = config.get('FS_INFO', 'DELETESQL')

        print "Loading Configuration File"
        arcpy.AddMessage("Loading Configuration File")

        if arcpy.Exists(LocalParcels) == False:
            print "Please specify a input parcel layer (LocalParcels=) in the configuration file, exiting"
            arcpy.AddMessage("Please specify a input parcel layer in the configuration file, exiting")
            sys.exit()

        if arcpy.Exists(CommunityParcelsLocalCopy) == False:
            print "Please specify a input community parcel layer (CommunityParcelsLocalCopy=) in the configuration file, exiting"
            arcpy.AddMessage("Please specify a input parcel layer in the configuration file, exiting")
            sys.exit()

        if username == "":
	        print "Please specify a ArcGIS Online Username (username =)in the configuration file, exiting"
	        arcpy.AddMessage(username)
	        sys.exit()

	    if password == "":
	        print "Please specify a ArcGIS Online password (password =)in the configuration file, exiting"
	        arcpy.AddMessage(password)
	        sys.exit()

	    if deleteSQL == "":
	        print "Please specify a SQL query (CVTTXDSCRP = 'some value') in the configuration file, exiting"
	        arcpy.AddMessage("Please specify a SQL query (CVTTXDSCRP = 'some value') in the configuration file, exiting")
	        sys.exit()


        fs = layer.FeatureLayer (url=url,username=username,password=password)
        if fs == None:
            print "Cannot find or connect to service, make sure service is accessible"
            arcpy.AddMessage("Cannot find or connect to service, make sure service is accessible")
            sys.exit()

        # Delete existing dataset that matches the community parcel schema
        arcpy.management.TruncateTable(CommunityParcelsLocalCopy)
        print "Cleaning up local parcel data"

        # Append new parcels into the community parcels schema, field map your data into the community schema.  Add local data field names after the "#" in the list.
        # For example, for STATEAREA "STATEAREA" true true false 50 Text 0 0 ,First,#,LocalParcels,TotalAcres,-1,-1  The local Parcels field name from STATEDAREA (community parcels schema) is TotalAcres.
        Field_Map = arcpy.GetParameterAsText(0)
        arcpy.Append_management(LocalParcels,CommunityParcelsLocalCopy,"NO_TEST",
            """
                LOWPARCELID "LOWPARCELID" true true false 50 Text 0 0 ,First,#;
                PARCELID "PARCELID" true true false 50 Text 0 0 ,First,#;
                FLOORDESIG "FLOORDESIG" true true false 50 Text 0 0 ,First,#;
                SHAPE_Length "SHAPE_Length" false true true 8 Double 0 0 ,First,#;
                SHAPE_Area "SHAPE_Area" false true true 8 Double 0 0 ,First,#;
                STATEAREA "STATEAREA" true true false 50 Text 0 0 ,First,#;
                CNVYNAME "CNVYNAME" LocalParcels,Subdivisio;
                USEDCD "USEDCD" true true false 50 Text 0 0 ,First,#;
                USEDSCRP "USEDSCRP" LocalParcels,PropType;
                CVTTXDSCRP "CVTTXDSCRP" true true false 50 Text 0 0 ,First,#;
                IMPROVED "IMPROVED" true true false 50 Text 0 0 ,First,#;
                OWNTYPE "OWNTYPE" true true false 50 Text 0 0 ,First,#;
                SITEADRESS "SITEADRESS" true true false 50 Text 0 0 ,First,#;
                OWNERNME1 "OWNERNME1" true true false 50 Text 0 0 ,First,#;
                OWNERNME2 "OWNERNME2" true true false 50 Text 0 0 ,First,#;
                PSTLADRESS "PSTLADRESS" true true false 50 Text 0 0 ,First,#;
                USPSBOX "USPSBOX" true true false 50 Text 0 0 ,First,#;
                PSTLCITY "PSTLCITY" true true false 50 Text 0 0 ,First,#;
                PSTLSTATE "PSTLSTATE" true true false 50 Text 0 0 ,First,#;
                PSTLZIP "PSTLZIP" true true false 50 Text 0 0 ,First,#;
                PSTLINTER "PSTLINTER" true true false 50 Text 0 0 ,First,#;
                LNDVALUE "LNDVALUE" true true false 50 Text 0 0 ,First,#;
                IMPVALUE "IMPVALUE" true true false 50 Text 0 0 ,First,#;
                CNTASSDVAL "CNTASSDVAL" true true false 50 Text 0 0 ,First,#;
                CNTTXBLVAL "CNTTXBLVAL" true true false 50 Text 0 0 ,First,#;
                SALEPRICE "SALEPRICE" true true false 50 Text 0 0 ,First,#;
                SALEDATE "SALEDATE" true true false 50 Text 0 0 ,First,#;
                LOCALFIPS "LOCALFIPS" true true false 50 Text 0 0 ,First,#;
                STCOFIPS "STCOFIPS" true true false 50 Text 0 0 ,First,#;
                GNISID "GNISID" true true false 50 Text 0 0 ,First,#;
                LASTEDITOR "LASTEDITOR" true true false 50 Text 0 0 ,First,#;
                LASTUPDATE "LASTUPDATE" true true false 50 Text 0 0 ,First,#;
                COUNTYNAME "COUNTYNAME" true true false 50 Text 0 0 ,First,#""","#")

        print "Mapping Local Parcel data to Community Parcel Schema"
        print "Community Parcel Update to ArcGIS Online Started, please be patient"
        arcpy.AddMessage("Mapping Local Parcel data to Community Parcel Schema")
        arcpy.AddMessage("Community Parcel Update to ArcGIS Online Started, please be patient")

        ##    # Calculate the CVTTXDSCRP to the County Name
        ##        arcpy.CalculateField_management(CommunityParcelsLocalCopy, "CVTTXDSCRP", "\"5\"", "PYTHON", "")
        ##        print "Set County Code information"
        ##        arcpy.AddMessage("Calculate County Code Description")

        # Add Attribute Index
        ##        arcpy.AddIndex_management(CommunityParcelsLocalCopy, "CVTTXDSCRP", "CountyDescriptionIndex", "NON_UNIQUE", "ASCENDING")
        ##        print "Add Attribute Indexes"
        ##        arcpy.AddMessage("Add Attribute Indexes - Performance")


        fs.objectIdField()
        value1=fs.query(sql=deleteSQL,returnIDsOnly=true)
        myids=value1 ['objectIds']

        minId = min(myids)
        i = 0
        maxId = max(myids)

        print minId
        print maxId
        chunkSize = 1000

        while (i <= len(myids)):
            #print myids[i:i+1000]
            oids = ",".join(str(e) for e in myids[i:i+chunkSize])
            #print oids
            if oids == '':
                continue
            else:
                fs.applyEdits(deleteFeatures=oids)
            i+=chunkSize
            print i
            #print len(myids)
            #print i/ float(len(myids))
            print "Completed: {0:2f}%".format( i/ float(len(myids))*100)
            arcpy.AddMessage("Deleted: {0:2f}%".format ( i/ float(len(myids))*100))
        print "Community Parcels upload Started"
        arcpy.AddMessage("Community Parcels upload started, please be patient, may take +- 5 minutes per 80,000 parcels.  For future consideration, please run tool during non-peak internet usage")
        fs.addFeatures(fc=CommunityParcelsLocalCopy)

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

    # Create the log file

    try:
        log = open(logFileName, 'a')

    except:
        print "Log file could not be created"

    # Change the output to both the windows and log file

    original = sys.stdout
    sys.stdout = helper.Tee(sys.stdout, log)

    print "Community Parcel Upload Started"
    print datetime.datetime.now().strftime(dateTimeFormat)

    # Load the config file

    if os.path.isfile(configFilePath):
        config = ConfigParser.ConfigParser()
        config.read(configFilePath)
    else:
        print "INI file not found."
        sys.exit()

    # Run the script

    runScript(log,config)
    print datetime.datetime.now().strftime(dateTimeFormat)
    print "Community Parcel Upload Completed"
    log.close()
