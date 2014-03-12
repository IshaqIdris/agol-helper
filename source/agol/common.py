import os
import json
import arcpy
from base import Geometry 
import datetime
#----------------------------------------------------------------------
def get_attachment_data(attachmentTable, sql,
                        nameField="ATT_NAME", blobField="DATA",
                        contentTypeField="CONTENT_TYPE",
                        rel_object_field="REL_OBJECTID"):
    """ gets all the data to pass to a feature service """
    ret_rows = []
    with arcpy.da.SearchCursor(attachmentTable, 
                               [nameField,
                                blobField,
                                contentTypeField,
                                rel_object_field],
                               where_clause=sql) as rows:
        for row in rows:
            temp_f = os.environ['temp'] + os.sep + row[0]
            writer = open(temp_f,'wb')
            writer.write(row[1])
            writer.flush()
            writer.close()
            del writer            
            ret_rows.append({
                "name" : row[0],
                "blob" : temp_f,
                "content" : row[2],
                "rel_oid" : row[3]
            })
            del row
    return ret_rows 
#----------------------------------------------------------------------
def create_feature_layer(ds, sql, name="layer"):
    """ creates a feature layer object """
    result = arcpy.MakeFeatureLayer_management(in_features=ds, 
                                               out_layer=name, 
                                               where_clause=sql)
    return result[0]
#----------------------------------------------------------------------
def get_records_with_attachments(attachment_table, rel_object_field="REL_OBJECTID"):
    """"""
    OIDs = []
    with arcpy.da.SearchCursor(attachment_table, 
                               [rel_object_field]) as rows:
        for row in rows:
            if not row[0] in OIDs:
                OIDs.append("%s" % row[0])
            del row
    return OIDs  
#----------------------------------------------------------------------
def get_OID_field(fs):
    """returns a featureset's object id field"""
    desc = arcpy.Describe(fs)
    if desc.hasOID:
        return desc.OIDFieldName
    return None
#----------------------------------------------------------------------
def featureclass_to_json(fc):
    """ converts a feature class to a json dictionary representation """
    featureSet = arcpy.FeatureSet(fc)# Load the feature layer into a feature set
    desc = arcpy.Describe(featureSet)# this will allow us to use the json property of the feature set
    return json.loads(desc.json)   
#----------------------------------------------------------------------
def getDateFields(fc):
    """
       Returns a list of fields that are of type DATE
       Input:
          fc - feature class or table path
       Output:
          List of date field names as strings
    """
    return [field.name for field in arcpy.ListFields(fc, field_type="Date")]
#----------------------------------------------------------------------
def toDateTime(unix_timestamp):
    """converts a unix time stamp to a datetime object """
    unix_timestamp = unix_timestamp/1000
    return datetime.datetime.fromtimestamp(unix_timestamp)
#----------------------------------------------------------------------
def insert_rows(fc, features, fields):
    """ inserts rows based on a list features object """
    date_fields = getDateFields(fc)
    icur = None
    if len(features) > 0:
        fields.append("SHAPE@")
        icur = arcpy.da.InsertCursor(fc, fields)
        for feat in features:
            row = [""] * len(fields)
            drow = feat.asRow[0]
            dfields = feat.fields
            for field in fields:
                if field in dfields:
                    if field in date_fields:
                        row[fields.index(field)] = toDateTime(drow[dfields.index(field)])
                    else:
                        row[fields.index(field)] = drow[dfields.index(field)]
                del field
            row[fields.index("SHAPE@")] = feat.geometry
            icur.insertRow(row)
            del row
            del drow
            del dfields
            del feat
        del features
        icur = None
        del icur
        del fields
        return fc
    else:
        return fc
#----------------------------------------------------------------------
def create_feature_class(out_path, 
                         out_name,
                         geom_type, 
                         wkid, 
                         fields, 
                         objectIdField):
    """ creates a feature class in a given gdb or folder """
    arcpy.env.overwriteOutput = True
    field_names = []
    fc =arcpy.CreateFeatureclass_management(out_path=out_path,
                                            out_name=out_name,
                                            geometry_type=lookUpGeometry(geom_type),
                                            spatial_reference=arcpy.SpatialReference(wkid))[0]
    for field in fields:
        if field['name'] != objectIdField:
            field_names.append(field['name'])
            arcpy.AddField_management(out_path + os.sep + out_name,
                                      field['name'],
                                      lookUpFieldType(field['type']))
    return fc, field_names
#----------------------------------------------------------------------
def lookUpGeometry(geom_type):
    """ converts ArcRest API geometry name to Python names
        Input:
           geom_type - string - name of geometry
        Output:
           name of python geometry type for create feature class function
    """
    if geom_type == "esriGeometryPoint":
        return "POINT"
    elif geom_type == "esriGeometryPolygon":
        return "POLYGON"
    elif geom_type == "esriGeometryLine":
        return "POLYLINE"
    else:
        return "POINT"
#----------------------------------------------------------------------
def lookUpFieldType(field_type):
    """ Converts the ArcGIS REST field types to Python Types
        Input:
           field_type - string - type of field as string
        Output:
           Python field type as string
    """
    if field_type == "esriFieldTypeDate":
        return "DATE"
    elif field_type == "esriFieldTypeInteger":
        return "LONG"
    elif field_type == "esriFieldTypeSmallInteger":
        return "SHORT"
    elif field_type == "esriFieldTypeDouble":
        return "DOUBLE"
    elif field_type == "esriFieldTypeString":
        return "TEXT"
    elif field_type == "esriFieldTypeBlob":
        return "BLOB"
    elif field_type == "esriFieldTypeSingle":
        return "FLOAT"
    elif field_type == "esriFieldTypeRaster":
        return "RASTER"
    elif field_type == "esriFieldTypeGUID":
        return "GUID"
    elif field_type == "esriFieldTypeGlobalID":
        return "TEXT"
    else:
        return "TEXT"
#----------------------------------------------------------------------
########################################################################
class SpatialReference:
    """ creates a spatial reference instance """
    _wkid = None
    #----------------------------------------------------------------------
    def __init__(self, wkid):
        """Constructor"""
        self._wkid = wkid
    #----------------------------------------------------------------------
    @property
    def wkid(self):
        """ get/set the wkid """
        return self._wkid
    @wkid.setter
    def wkid(self, wkid):
        """ get/set the wkid """
        self._wkid = wkid
    @property
    def asDictionary(self):
        """returns the wkid id for use in json calls"""
        return {"wkid": self._wkid}
########################################################################
class Point(Geometry):
    """ Point Geometry 
        
    """
    _x = None
    _y = None
    _z = None
    _m = None
    _wkid = None
    _json = None
    _geom = None
    _dict = None
    #----------------------------------------------------------------------
    def __init__(self, x, y, wkid, z=None, m=None):
        """Constructor"""
        self._x = float(x)
        self._y = float(y)
        self._wkid = wkid
        if not z is None:
            self._z = float(z)
        self._m = m
        self._dict = self.asDictionary
        self._json = self.asJSON
        self._geom = self.asArcPyObject
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return {'wkid' : self._wkid}
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryPoint"
    #----------------------------------------------------------------------    
    @property
    def asJSON(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.asDictionary)
            self._json = value
        return self._json
    #----------------------------------------------------------------------
    @property
    def asArcPyObject(self):
        """ returns the Point as an ESRI arcpy.Point object """
        return arcpy.AsShape(self.asDictionary, True)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a python dictionary """
        #
        value = self._dict
        if value is None:
            template = {"x" : self._x, 
                        "y" : self._y, 
                        "spatialReference" : {"wkid" : self._wkid}
                        }
            if not self._z is None:
                template['z'] = self._z
            if not self._m is None:
                template['z'] = self._m
            self._dict = template
        return self._dict
    #----------------------------------------------------------------------
    @property
    def asList(self):
        """ returns a Point value as a list of [x,y,<z>,<m>] """
        base = [self._x, self._y]
        if not self._z is None:
            base.append(self._z)
        elif not self._m is None:
            base.append(self._m)
        return base

########################################################################
class MultiPoint(Geometry):
    """ Implements the ArcGIS JSON MultiPoint Geometry Object """
    _geom = None
    _json = None
    _dict = None
    _wkid = None
    _points = None
    _hasZ = False
    _hasM = False
    #----------------------------------------------------------------------
    def __init__(self, points, wkid, hasZ=False, hasM=False):
        """Constructor"""
        self._points = points
        self._wkid = wkid
        self._hasZ = hasZ
        self._hasM = hasM
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return {'wkid' : self._wkid}
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryMultipoint"    
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.asDictionary)
            self._json = value
        return self._json
    #----------------------------------------------------------------------
    @property
    def asArcPyObject(self):
        """ returns the Point as an ESRI arcpy.MultiPoint object """
        return arcpy.AsShape(self.asDictionary, True)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a python dictionary """
        #
        value = self._dict
        if value is None:
            template = {
                "hasM" : self._hasM,
                "hasZ" : self._hasZ,
                "points" : [], 
                "spatialReference" : {"wkid" : self._wkid}
            }
            for pt in self._points:
                template['points'].append(pt.asList)
            self._dict = template
        return self._dict  
########################################################################
class Polyline(Geometry):
    """ Implements the ArcGIS REST API Polyline Object 
        Inputs:
           paths - list - list of lists of Point objects
           wkid - integer - well know spatial reference id
           hasZ - boolean - 
           hasM - boolean - 
    """
    _paths = None
    _wkid = None
    _json = None
    _dict = None
    _geom = None
    _hasZ = None
    _hasM = None
    #----------------------------------------------------------------------
    def __init__(self, paths, wkid, hasZ=False, hasM=False):
        """Constructor"""
        self._paths = paths
        self._wkid = wkid
        self._hasM = hasM
        self._hasZ = hasZ
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return {'wkid' : self._wkid}    
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryPolyline"    
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.asDictionary)
            self._json = value
        return self._json
    #----------------------------------------------------------------------
    @property
    def asArcPyObject(self):
        """ returns the Polyline as an ESRI arcpy.Polyline object """
        return arcpy.AsShape(self.asDictionary, True)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a python dictionary """
        value = self._dict
        if value is None:
            template = {
                "hasM" : self._hasM,
                "hasZ" : self._hasZ,
                "paths" : [], 
                "spatialReference" : {"wkid" : self._wkid}
            }
            for part in self._paths:
                lpart = []
                for pt in part:
                    lpart.append(pt.asList)
                template['paths'].append(lpart)
                del lpart
            self._dict = template
        return self._dict        
########################################################################
class Polygon(Geometry):
    """ Implements the ArcGIS REST JSON for Polygon Object """
    _rings = None
    _wkid = None
    _json = None
    _dict = None
    _geom = None
    _hasZ = None
    _hasM = None    
    #----------------------------------------------------------------------
    def __init__(self, rings, wkid, hasZ=False, hasM=False):
        """Constructor"""
        self._rings = rings
        self._wkid = wkid
        self._hasM = hasM
        self._hasZ = hasZ
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return {'wkid' : self._wkid}    
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryPolygon"           
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.asDictionary)
            self._json = value
        return self._json
    #----------------------------------------------------------------------
    @property
    def asArcPyObject(self):
        """ returns the Polyline as an ESRI arcpy.Polyline object """
        return arcpy.AsShape(self.asDictionary, True)
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the object as a python dictionary """
        value = self._dict
        if value is None:
            template = {
                "hasM" : self._hasM,
                "hasZ" : self._hasZ,
                "rings" : [], 
                "spatialReference" : {"wkid" : self._wkid}
            }
            for part in self._rings:
                lpart = []
                for pt in part:
                    lpart.append(pt.asList)
                template['rings'].append(lpart)
                del lpart
            self._dict = template
        return self._dict         
########################################################################
class Envelope(Geometry):
    """
       An envelope is a rectangle defined by a range of values for each 
       coordinate and attribute. It also has a spatialReference field. 
       The fields for the z and m ranges are optional. 
    """
    _json = None
    _dict = None
    _geom = None
    _xmin = None
    _ymin = None
    _zmin = None
    _mmin = None
    _xmax = None
    _ymax = None
    _zmax = None
    _mmax = None
    _wkid = None
    #----------------------------------------------------------------------
    def __init__(self, xmin, ymin, xmax, ymax, wkid, 
                 zmin=None, zmax=None, mmin=None, mmax=None):
        """Constructor"""
        self._xmin = xmin
        self._ymin = ymin
        self._zmin = zmin
        self._mmin = mmin
        self._xmax = xmax
        self._ymax = ymax
        self._zmax = zmax
        self._mmax = mmax        
        self._wkid = wkid
    #----------------------------------------------------------------------
    @property
    def spatialReference(self):
        """returns the geometry spatial reference"""
        return {'wkid' : self._wkid}    
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the geometry type """
        return "esriGeometryEnvelope"    
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """ returns the envelope as a dictionary """
        template = {
            "xmin" : self._xmin, 
            "ymin" : self._ymin, 
            "xmax" : self._xmax, 
            "ymax" : self._ymax,
            "spatialReference" : {"wkid" : self._wkid}
        }
        if self._zmax is not None and \
           self._zmin is not None:
            template['zmin'] = self._zmin
            template['zmax'] = self._zmax
        
        if self._mmin is not None and \
           self._mmax is not None:
            template['mmax'] = self._mmax
            template['mmin'] = self._mmin
            
        return template
    #----------------------------------------------------------------------
    @property
    def asJSON(self):
        """ returns a geometry as JSON """
        value = self._json
        if value is None:
            value = json.dumps(self.asDictionary)
            self._json = value
        return self._json    
    #----------------------------------------------------------------------
    @property
    def asArcPyObject(self):
        """ returns the Envelope as an ESRI arcpy.Polygon object """
        env = self.asDictionary
        ring = [[
            Point(env['xmin'], env['ymin'], self._wkid), 
            Point(env['xmax'], env['ymin'], self._wkid),
            Point(env['xmax'], env['ymax'], self._wkid),
            Point(env['xmin'], env['ymax'], self._wkid)
            ]]
        return Polygon(ring, self._wkid).asArcPyObject
########################################################################
class Feature(object):
    """ returns a feature  """
    _geom = None
    _json = None
    _dict = None
    _geom = None
    _geomType = None
    _attributes = None
    #----------------------------------------------------------------------
    def __init__(self, json_string):
        """Constructor"""
        if type(json_string) is dict:
            self._json = json.dumps(json_string)
            self._dict = json_string
        elif type(json_string) is str:
            self._dict = json.loads(json_string)
            self._json = json_string
        else:
            raise TypeError("Invalid Input, only dictionary of string allowed")
    #----------------------------------------------------------------------
    @property
    def asDictionary(self):
        """returns the feature as a dictionary"""
        feat_dict = {}
        if self._geom is not None:
            if self._dict.has_key('feature'):
                feat_dict['geometry'] =  self._dict['feature']['geometry']
            elif self._dict.has_key('geometry'):        
                feat_dict['geometry'] =  self._dict['geometry']
        if self._dict.has_key("feature"):
            feat_dict['attributes'] = self._dict['feature']['attributes']
        else:
            feat_dict['attributes'] = self._dict['attributes']        
        return self._dict
    #----------------------------------------------------------------------
    @property
    def asRow(self):
        """ converts a feature to a list for insertion into an insert cursor 
            Output:
               [row items], [field names]
               returns a list of fields and the row object
        """
        fields = self.fields
        row = [""] * len(fields)
        for k,v in self._attributes.iteritems():
            row[fields.index(k)] = v
            del v
            del k
        if self.geometry is not None:
            row.append(self.geometry)
            fields.append("SHAPE@")
        return row, fields
    #----------------------------------------------------------------------
    @property
    def geometry(self):
        """returns the feature geometry"""
        if self._geom is None:
            if self._dict.has_key('feature'):
                self._geom = arcpy.AsShape(self._dict['feature']['geometry'], esri_json=True)
            elif self._dict.has_key('geometry'):
                self._geom = arcpy.AsShape(self._dict['geometry'], esri_json=True)
        return self._geom
    #----------------------------------------------------------------------
    @property
    def fields(self):
        """ returns a list of feature fields """
        if self._dict.has_key("feature"):
            self._attributes = self._dict['feature']['attributes']
        else:
            self._attributes = self._dict['attributes']
        return self._attributes.keys()
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """ returns the feature's geometry type """
        if self._geomType is None:
            if self.geometry is not None:
                self._geomType = self.geometry.type
            else:
                self._geomType = "Table"
        return self._geomType