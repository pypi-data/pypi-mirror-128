import json

def DetectsQueriesDetects(self, query):
    '''detects/queries/detects/v1'''
    return json.loads(self.GetAPI("detects/queries/detects/v1?"+query))

def DetectsEntitiesSummariesGET(self, detects_ids):
    '''detects/entities/summaries/GET/v1'''
    return json.loads(self.PostAPI("detects/entities/summaries/GET/v1", ({"ids": detects_ids}) ))

def DetectsEntitiesDetects(self, ids, status, assigned_to_uuid, comment="CrowdStrike-Client"):
    '''detects/entities/detects/v2'''
    Param = {
        "ids": ids,
        "status": status,
        "assigned_to_uuid": assigned_to_uuid,
        "comment": comment
    }
    return json.loads(self.PatchAPI("detects/entities/detects/v2", Param))