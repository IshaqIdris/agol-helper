from agol import featureservice, layer
"""
   Updating a feature layer

"""
from agol import featureservice

if __name__ == "__main__":

  fURL = "http://services2.arcgis.com/PWJUSsdoJDp7SgLj/arcgis/rest/services/PublicOutages/FeatureServer/1"
    fl = layer.FeatureLayer(url=fURL,username="MikeSolutions",password='double1pa')
    result = fl.query(where="1=1",out_fields='NUMSERVED,NUMOUT')
    for res in result:
        res.set_value("NUMSERVED", 100)
        res.set_value("NUMOUT", 123)

    print fl.updateFeature(result)

