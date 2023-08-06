import json

# Intel
def MalqueryEntitiesMetadata(self, ids):
    '''/malquery/entities/metadata/v1'''
    Param = ""
    for ids in ids:
        Param += "ids="+ids+"&"    
    return json.loads(self.GetAPI("devices/entities/devices/v1?"+Param))