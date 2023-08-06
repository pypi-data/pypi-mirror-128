import json

def UsersQueriesUser_uuids_by_cid(self):
    '''/users/queries/user-uuids-by-cid/v1'''
    return json.loads(self.GetAPI("/users/queries/user-uuids-by-cid/v1"))

def UsersEntitiesUsers(self, ids):
    '''/users/entities/users/v1'''
    if type(ids) is list:
        Param = ""
        for ids in ids:
            Param += "ids="+ids+"&" 
    else:
        Param = "ids="+ids
    return json.loads(self.GetAPI("/users/entities/users/v1?"+Param))