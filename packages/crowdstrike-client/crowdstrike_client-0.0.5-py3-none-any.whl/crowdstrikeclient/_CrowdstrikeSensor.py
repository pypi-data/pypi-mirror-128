import json

# Sensor 
def SensorsQueriesInstallersCcid(self):
    '''sensors/queries/installers/ccid/v1'''
    return json.loads(self.GetAPI("sensors/queries/installers/ccid/v1"))
