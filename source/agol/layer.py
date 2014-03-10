import common
import filters
import featureservice
from base import BaseAGOLClass
import os
import json
import math
import urlparse
import mimetypes

########################################################################
class FeatureLayer(BaseAGOLClass):
    """
       This contains information about a feature service's layer.
    """
    _objectIdField = None
    _allowGeometryUpdates = None
    _globalIdField = None
    _token_url = None
    _currentVersion = None
    _id = None
    _name = None
    _type = None
    _description = None
    _definitionExpression = None
    _geometryType = None
    _hasZ = None
    _hasM = None
    _copyrightText = None
    _parentLayer = None
    _subLayers = None
    _minScale = None
    _maxScale = None
    _effectiveMinScale = None
    _effectiveMaxScale = None
    _defaultVisibility = None
    _extent = None
    _timeInfo = None
    _drawingInfo = None
    _hasAttachments = None
    _htmlPopupType = None
    _displayField = None
    _typeIdField = None
    _fields = None
    _types = None # sub-types
    _relationships = None
    _maxRecordCount = None
    _canModifyLayer = None
    _supportsStatistics = None
    _supportsAdvancedQueries = None
    _hasLabels = None
    _canScaleSymbols = None
    _capabilities = None
    _supportedQueryFormats =  None
    _isDataVersioned = None
    _ownershipBasedAccessControlForFeatures = None
    _useStandardizedQueries = None
    _templates = None
    _indexes = None
    _hasStaticData = None
    _supportsRollbackOnFailureParameter = None
    #----------------------------------------------------------------------
    def __init__(self, url,
                 username=None,
                 password=None,
                 token_url=None):
        """Constructor"""
        self._url = url
        self._token_url = token_url
        self._username = username
        self._password = password
        if not username is None and\
           not password is None:
            if not token_url is None:
                self._token = self.generate_token(tokenURL=token_url)[0]
            else:
                self._token = self.generate_token()[0]
        self.__init()
    #----------------------------------------------------------------------
    def __init(self):
        """ initializes the service """
        params = {
            "f" : "json",
        }
        if self._token is not None:
            params['token'] = self._token
        json_dict = self._do_get(self._url, params)
        attributes = [attr for attr in dir(self)
                      if not attr.startswith('__') and \
                      not attr.startswith('_')]
        for k,v in json_dict.iteritems():
            if k in attributes:
                setattr(self, "_"+ k, json_dict[k])
        self._parentLayer = featureservice.FeatureService(
            url=os.path.dirname(self._url),
            token_url=self._token_url,
            username=self._username,
            password=self._password)
    #----------------------------------------------------------------------
    @property
    def supportsRollbackOnFailureParameter(self):
        """ returns if rollback on failure supported """
        if self._supportsRollbackOnFailureParameter is None:
            self.__init()
        return self._supportsRollbackOnFailureParameter
    #----------------------------------------------------------------------
    @property
    def hasStaticData(self):
        """boolean T/F if static data is present """
        if self._hasStaticData is None:
            self.__init()
        return self._hasStaticData
    #----------------------------------------------------------------------
    @property
    def indexes(self):
        """gets the indexes"""
        if self._indexes is None:
            self.__init()
        return self._indexes
    #----------------------------------------------------------------------
    @property
    def templates(self):
        """ gets the template """
        if self._templates is None:
            self.__init()
        return self._templates
    #----------------------------------------------------------------------
    @property
    def allowGeometryUpdates(self):
        """ returns boolean if geometry updates are allowed """
        if self._allowGeometryUpdates is None:
            self.__init()
        return self._allowGeometryUpdates
    #----------------------------------------------------------------------
    @property
    def globalIdField(self):
        """ returns the global id field """
        if self._globalIdField is None:
            self.__init()
        return self._globalIdField

    #----------------------------------------------------------------------
    @property
    def objectIdField(self):
        if self._objectIdField is None:
            self.__init()
        return self._objectIdField
    #----------------------------------------------------------------------
    @property
    def currentVersion(self):
        """ returns the current version """
        if self._currentVersion is None:
            self.__init()
        return self._currentVersion
    #----------------------------------------------------------------------
    @property
    def id(self):
        """ returns the id """
        if self._id is None:
            self.__init()
        return self._id
    #----------------------------------------------------------------------
    @property
    def name(self):
        """ returns the name """
        if self._name is None:
            self.__init()
        return self._name
    #----------------------------------------------------------------------
    @property
    def type(self):
        """ returns the type """
        if self._type is None:
            self.__init()
        return self._type
    #----------------------------------------------------------------------
    @property
    def description(self):
        """ returns the layer's description """
        if self._description is None:
            self.__init()
        return self._description
    #----------------------------------------------------------------------
    @property
    def definitionExpression(self):
        """returns the definitionExpression"""
        if self._definitionExpression is None:
            self.__init()
        return self._definitionExpression
    #----------------------------------------------------------------------
    @property
    def geometryType(self):
        """returns the geometry type"""
        if self._geometryType is None:
            self.__init()
        return self._geometryType
    #----------------------------------------------------------------------
    @property
    def hasZ(self):
        """ returns if it has a Z value or not """
        if self._hasZ is None:
            self.__init()
        return self._hasZ
    #----------------------------------------------------------------------
    @property
    def hasM(self):
        """ returns if it has a m value or not """
        if self._hasM is None:
            self.__init()
        return self._hasM
    #----------------------------------------------------------------------
    @property
    def copyrightText(self):
        """ returns the copyright text """
        if self._copyrightText is None:
            self.__init()
        return self._copyrightText
    #----------------------------------------------------------------------
    @property
    def parentLayer(self):
        """ returns information about the parent """
        if self._parentLayer is None:
            self.__init()
        return self._parentLayer
    #----------------------------------------------------------------------
    @property
    def subLayers(self):
        """ returns sublayers for layer """
        if self._subLayers is None:
            self.__init()
        return self._subLayers
    #----------------------------------------------------------------------
    @property
    def minScale(self):
        """ minimum scale layer will show """
        if self._minScale is None:
            self.__init()
        return self._minScale
    @property
    def maxScale(self):
        """ sets the max scale """
        if self._maxScale is None:
            self.__init()
        return self._maxScale
    @property
    def effectiveMinScale(self):
        if self._effectiveMinScale is None:
            self.__init()
        return self._effectiveMinScale
    @property
    def effectiveMaxScale(self):
        if self._effectiveMaxScale is None:
            self.__init()
        return self._effectiveMaxScale
    @property
    def defaultVisibility(self):
        if self._defaultVisibility is None:
            self.__init()
        return self._defaultVisibility
    @property
    def extent(self):
        if self._extent is None:
            self.__init()
        return self._extent
    @property
    def timeInfo(self):
        if self._timeInfo is None:
            self.__init()
        return self._timeInfo
    @property
    def drawingInfo(self):
        if self._drawingInfo is None:
            self.__init()
        return self._drawingInfo
    @property
    def hasAttachments(self):
        if self._hasAttachments is None:
            self.__init()
        return self._hasAttachments
    @property
    def htmlPopupType(self):
        if self._htmlPopupType is None:
            self.__init()
        return self._htmlPopupType
    @property
    def displayField(self):
        if self._displayField is None:
            self.__init()
        return self._displayField
    @property
    def typeIdField(self):
        if self._typeIdField is None:
            self.__init()
        return self._typeIdField
    @property
    def fields(self):
        if self._fields is None:
            self.__init()
        return self._fields
    @property
    def types(self):
        if self._types is None:
            self.__init()
        return self._types
    @property
    def relationships(self):
        if self._relationships is None:
            self.__init()
        return self._relationships
    @property
    def maxRecordCount(self):
        if self._maxRecordCount is None:
            self.__init()
        return self._maxRecordCount
    @property
    def canModifyLayer(self):
        if self._canModifyLayer is None:
            self.__init()
        return self._canModifyLayer
    @property
    def supportsStatistics(self):
        if self._supportsStatistics is None:
            self.__init()
        return self._supportsStatistics
    @property
    def supportsAdvancedQueries(self):
        if self._supportsAdvancedQueries is None:
            self.__init()
        return self._supportsAdvancedQueries
    @property
    def hasLabels(self):
        if self._hasLabels is None:
            self.__init()
        return self._hasLabels
    @property
    def canScaleSymbols(self):
        if self._canScaleSymbols is None:
            self.__init()
        return self._canScaleSymbols
    @property
    def capabilities(self):
        if self._capabilities is None:
            self.__init()
        return self._capabilities
    @property
    def supportedQueryFormats(self):
        if self._supportedQueryFormats is None:
            self.__init()
        return self._supportedQueryFormats
    @property
    def isDataVersioned(self):
        if self._isDataVersioned is None:
            self.__init()
        return self._isDataVersioned
    @property
    def ownershipBasedAccessControlForFeatures(self):
        if self._ownershipBasedAccessControlForFeatures is None:
            self.__init()
        return self._ownershipBasedAccessControlForFeatures
    @property
    def useStandardizedQueries(self):
        if self._useStandardizedQueries is None:
            self.__init()
        return self._useStandardizedQueries
    #----------------------------------------------------------------------
    def addAttachment(self, oid, file_path):
        """ Adds an attachment to a feature service
            Input:
              oid - string - OBJECTID value to add attachment to
              file_path - string - path to file
            Output:
              JSON Repsonse
        """
        if self.hasAttachments == True:
            attachURL = self._url + "/%s/addAttachment" % oid
            params = {'f':'json'}
            if not self._token is None:
                params['token'] = self._token
            content = open(file_path, 'rb').read()
            parsed = urlparse.urlparse(attachURL)

            res = self._post_multipart(host=parsed.hostname,
                                       selector=parsed.path,
                                       filename=os.path.basename(file_path),
                                       filetype=mimetypes.guess_type(file_path)[0],
                                       content=content,
                                       fields=params)
            return self._unicode_convert(json.loads(res))
        else:
            return "Attachments are not supported for this feature service."
    #----------------------------------------------------------------------
    def deleteAttachment(self, oid, attachment_id):
        """ removes an attachment from a feature service feature
            Input:
              oid - integer or string - id of feature
              attachment_id - integer - id of attachment to erase
            Output:
               JSON response
        """
        url = self._url + "/%s/deleteAttachments" % oid
        params = {
            "f":"json",
            "attachmentIds" : "%s" % attachment_id
        }
        if not self._token is None:
            params['token'] = self._token
        return self._do_post(url, params)
    #----------------------------------------------------------------------
    def updateAttachment(self, oid, attachment_id, file_path):
        """ updates an existing attachment with a new file
            Inputs:
               oid - string/integer - Unique record ID
               attachment_id - integer - Unique attachment identifier
               file_path - string - path to new attachment
            Output:
               JSON response
        """
        url = self._url + "/%s/updateAttachment" % oid
        params = {
            "f":"json",
            "attachmentId" : "%s" % attachment_id
        }
        if not self._token is None:
            params['token'] = self._token
        parsed = urlparse.urlparse(url)
        content = open(file_path, 'rb').read()
        res = self._post_multipart(host=parsed.hostname,
                                   selector=parsed.path,
                                   filename=os.path.basename(file_path).split('.')[0],
                                   filetype=mimetypes.guess_type(file_path)[0],
                                   content=content,
                                   fields=params)
        return self._unicode_convert(json.loads(res))
    #----------------------------------------------------------------------
    def listAttachments(self, oid):
        """ list attachements for a given OBJECT ID """
        url = self._url + "/%s/attachments" % oid
        params = {
            "f":"json"
        }
        if not self._token is None:
            params['token'] = self._token
        return self._do_get(url, params)
    #----------------------------------------------------------------------
    def create_fc_template(self, out_path, out_name):
        """creates a featureclass template on local disk"""
        fields = self.fields
        objectIdField = self.objectIdField
        geomType = self.geometryType
        wkid = self.parentLayer.spatialReference['wkid']
        return common.create_feature_class(out_path,
                                           out_name,
                                           geomType,
                                           wkid,
                                           fields,
                                           objectIdField)

    #----------------------------------------------------------------------
    def query(self,
              where="1=1",
              out_fields="*",
              timeFilter=None,
              geometryFilter=None,
              returnGeometry=True,
              returnIDsOnly=False,
              returnCountOnly=False,
              returnFeatureClass=False,
              out_fc=None):
        """ queries a feature service based on a sql statement
            Inputs:
               where - the selection sql statement
               out_fields - the attribute fields to return
               timeFilter - a TimeFilter object where either the start time
                            or start and end time are defined to limit the
                            search results for a given time.  The values in
                            the timeFilter should be as UTC timestampes in
                            milliseconds.  No checking occurs to see if they
                            are in the right format.
               geometryFilter - a GeometryFilter object to parse down a given
                               query by another spatial dataset.
               returnGeometry - true means a geometry will be returned, else just the attributes
               returnIDsOnly - false is default.  True means only OBJECTIDs will be returned
               returnCountOnly - if True, then an integer is returned only based on the sql statement
               returnFeatureClass - Default False. If true, query will be returned as feature class
               out_fc - only valid if returnFeatureClass is set to True. Output location of query.
            Output:
               A list of Feature Objects (default) or a path to the output featureclass if
               returnFeatureClass is set to True.
         """
        params = {"f": "json",
                  "where": where,
                  "outFields": out_fields,
                  "returnGeometry" : returnGeometry,
                  "returnIdsOnly" : returnIDsOnly,
                  "returnCountOnly" : returnCountOnly,
                  }
        if not self._token is None:
            params["token"] = self._token
        if not timeFilter is None and \
           isinstance(timeFilter, filters.TimeFilter):
            params['time'] = timeFilter.filter
        if not geometryFilter is None and \
           isinstance(geometryFilter, filters.GeometryFilter):
            gf = geometryFilter.filter
            params['geometry'] = gf['geometry']
            params['geometryType'] = gf['geometryType']
            params['spatialRelationship'] = gf['spatialRel']
            params['inSR'] = gf['inSR']
        fURL = self._url + "/query"
        results = self._do_get(fURL, params)
        if not returnCountOnly and not returnIDsOnly:
            feats = []
            for res in results['features']:
                feats.append(common.Feature(res))
            if returnFeatureClass:
                out_fc, field_names = common.create_feature_class(out_path=os.path.dirname(out_fc),
                                                     out_name=os.path.basename(out_fc),
                                                 geom_type=self.geometryType,
                                                 wkid=self.parentLayer.spatialReference['wkid'],
                                                 fields=self.fields,
                                                 objectIdField=self.objectIdField)
                out_fc = common.insert_rows(out_fc, feats, field_names)
                return out_fc
            else:
                return feats
        else:
            return results
        return
    #----------------------------------------------------------------------
    def _chunks(self, l, n):
        """ Yield n successive chunks from l.
        """
        newn = int(1.0 * len(l) / n + 0.5)
        for i in xrange(0, n-1):
            yield l[i*newn:i*newn+newn]
        yield l[n*newn-newn:]
    #----------------------------------------------------------------------
    def get_local_copy(self, out_path, includeAttachments=False):
        """ exports the whole feature service to a feature class
            Input:
               out_path - path to where the data will be placed
               includeAttachments - default False. If sync is not supported
                                    then the paramter is ignored.
            Output:
               path to exported feature class or fgdb (as list)
        """
        if self.hasAttachments and \
           self.parentLayer.syncEnabled:
            return self.parentLayer.createReplica(replicaName="fgdb_dump",
                                                  layers="%s" % self.id,
                                                  returnAsFeatureClass=True,
                                                  returnAttachments=includeAttachments,
                                                  out_path=out_path)[0]
        elif self.hasAttachments == False and \
             self.parentLayer.syncEnabled:
            return self.parentLayer.createReplica(replicaName="fgdb_dump",
                                                  layers="%s" % self.id,
                                                  returnAsFeatureClass=True,
                                                  out_path=out_path)[0]
        else:
            result_features = []
            res = self.query(returnIDsOnly=True)
            OIDS = res['objectIds']
            OIDS.sort()
            OIDField = res['objectIdFieldName']
            count = len(OIDS)
            if count <= self.maxRecordCount:
                bins = 1
            else:
                bins = count / self.maxRecordCount
                v = count % self.maxRecordCount
                if v > 0:
                    bins += 1
            chunks = self._chunks(OIDS, bins)
            for chunk in chunks:
                chunk.sort()
                sql = "%s >= %s and %s <= %s" % (OIDField, chunk[0],
                                                 OIDField, chunk[len(chunk) -1])
                print sql
                result_features += self.query(where=sql)
            fc, fields = self.create_fc_template(out_path=os.path.dirname(out_path),
                                         out_name=os.path.basename(out_path)
                                         )
            return common.insert_rows(fc, result_features, fields)
    #----------------------------------------------------------------------
    def deleteFeatures(self, sql='1=1',objectIDs=''):
        """ removes 1:n features based on a sql statement
            Input:
              sql - string - where clause used to delete features
            Output:
               Number of features removed
        """
        dURL = self._url + "/deleteFeatures"
        params = {
            "f": "json",
            "where": sql,
            "objectIds": objectIDs
        }
        if not self._token is None:
            params['token'] = self._token
        result = self._do_post(url=dURL, param_dict=params)

        self.__init()
        return result
    #----------------------------------------------------------------------
    def addFeatures(self, fc, attachmentTable=None,
                    nameField="ATT_NAME", blobField="DATA",
                    contentTypeField="CONTENT_TYPE",
                    rel_object_field="REL_OBJECTID"):
        """ adds a feature to the feature service
           Inputs:
              fc - string - path to feature class data to add.
              attachmentTable - string - (optional) path to attachment table
              nameField - string - (optional) name of file field in attachment table
              blobField - string - (optional) name field containing blob data
              contentTypeField - string - (optional) name of field containing content type
              rel_object_field - string - (optional) name of field with OID of feature class
           Output:
              boolean, add results message as list of dictionaries

        """
        #try:
        messages = []
        if attachmentTable is None:
            #messages = []
            count = 0
            bins = 1
            uURL = self._url + "/addFeatures"
            max_chunk = 250
            js = self._unicode_convert(
                common.featureclass_to_json(fc))
            js = js['features']
            if len(js) <= max_chunk:
                bins = 1
            else:
                bins = int(len(js)/max_chunk)
                if len(js) % max_chunk > 0:
                    bins += 1
            chunks = self._chunks(l=js, n=bins)
            for chunk in chunks:
                params = {

                    "f" : 'json',
                    "features"  : json.dumps(chunk)
                }
                if not self._token is None:
                    params['token'] = self._token
                result = self._do_post(url=uURL, param_dict=params)
                messages.append(result)
                del params
                del result
            return True, messages
        else:
            oid_field = common.get_OID_field(fc)
            OIDs = common.get_records_with_attachments(attachment_table=attachmentTable)
            fl = common.create_feature_layer(fc, "%s not in ( %s )" % (oid_field, ",".join(OIDs)))
            val, msgs = self.addFeatures(fl)
            messages.append(msgs)
            del fl
            for oid in OIDs:
                fl = common.create_feature_layer(fc, "%s = %s" % (oid_field, oid), name="layer%s" % oid)
                val, msgs = self.addFeatures(fl)
                for result in msgs[0]['addResults']:
                    oid_fs = result['objectId']
                    sends = common.get_attachment_data(attachmentTable, sql="%s = %s" % (rel_object_field, oid))
                    for s in sends:
                        messages.append(self.addAttachment(oid_fs, s['blob']))
                        del s
                    del sends
                    del result
                messages.append(msgs)
                del fl
                del oid
            del OIDs
            return True, messages
########################################################################
class TableLayer(FeatureLayer):
    """Table object is exactly like FeatureLayer object"""
    pass

