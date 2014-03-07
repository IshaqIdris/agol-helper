"""
   Base Class from which AGOL function inherit from.
"""
import urllib
import urllib2
import requests
import json
import Utilities
import httplib.
class BaseAGOLClass(object):
    _token = None
    _username = None
    _password = None    
    def generate_token(self):
        """ generates a token for a feature service """
        token = Utilities.getToken(username=self._username,
                                   password = self._password,
                                   referer='https://www.arcgis.com')[0]
        self._token = token
        return token
    @property
    def username(self):
        """ returns the user name """
        return self._username
    @username.setter
    def username(self, value):
        """ sets the username """
        self._username = value
    @property
    def password(self):
        """ getter for password """
        return "***"
    @password.setter
    def password(self, value):
        """ sets the username's password """
        self._password = value
    #----------------------------------------------------------------------
    def _do_post(self, url, param_dict):
        """ performs the POST operation and returns dictionary result """
        request = urllib2.Request(url, urllib.urlencode(param_dict))
        result = urllib2.urlopen(request).read()
        jres = json.loads(result)
        return self._unicode_convert(jres) 
    #----------------------------------------------------------------------
    def _do_get(self, url, param_dict, header={}):
        """ performs a get operation """
        url = url + "?%s" % urllib.urlencode(param_dict)
        request = urllib2.Request(url, headers=header)
        result = urllib2.urlopen(request).read()
        jres = json.loads(result)
        return self._unicode_convert(jres)
    #----------------------------------------------------------------------
    def _do_post_file(self, url, params, file_path):
        """ allows a user to POST a file to server """
        base_url = "{}/content/users/{}/addItem".format(url, 
                                                        self._username)
        filesUp = {"file": open(file_path, 'rb')}
        url = base_url + "?%s" % urllib.urlencode(params)
        response = requests.post(url, files=filesUp)
        vals = json.loads(response.text)
        return self._unicode_convert(vals)
    #----------------------------------------------------------------------
    def _post_multipart(self, host, selector, 
                        filename, filetype, 
                        content, fields):
        """ performs a multi-post to AGOL or AGS 
            Inputs:
               host - string - root url (no http:// or https://)
                   ex: www.arcgis.com
               selector - string - everything after the host
                   ex: /PWJUSsdoJDp7SgLj/arcgis/rest/services/GridIndexFeatures/FeatureServer/0/1/addAttachment
               filename - string - name file will be called on server
               filetype - string - mimetype of data uploading
               content - binary data - derived from open(<file>, 'rb').read()
               fields - dictionary - additional parameters like token and format information
            Output:
               JSON response as dictionary
        """
        body = ''
        for field in fields.keys():
            body += '------------ThIs_Is_tHe_bouNdaRY_$\r\nContent-Disposition: form-data; name="' + field + '"\r\n\r\n' + fields[field] + '\r\n'
        body += '------------ThIs_Is_tHe_bouNdaRY_$\r\nContent-Disposition: form-data; name="file"; filename="'
        body += filename + '"\r\nContent-Type: ' + filetype + '\r\n\r\n'
        body = body.encode('utf-8')
        body += content + '\r\n------------ThIs_Is_tHe_bouNdaRY_$--\r\n'
        h = httplib.HTTP(host)
        h.putrequest('POST', selector)
        h.putheader('content-type', 'multipart/form-data; boundary=----------ThIs_Is_tHe_bouNdaRY_$')
        h.putheader('content-length', str(len(body)))
        h.endheaders()
        h.send(body)
        errcode, errmsg, headers = h.getreply()
        return h.file.read()
    #----------------------------------------------------------------------    
    def _unicode_convert(self, obj):
        """ converts unicode to anscii """
        if isinstance(obj, dict):
            return {self._unicode_convert(key): self._unicode_convert(value) for key, value in obj.iteritems()}
        elif isinstance(obj, list):
            return [self._unicode_convert(element) for element in obj]
        elif isinstance(obj, unicode):
            return obj.encode('utf-8')
        else:
            return obj        
        