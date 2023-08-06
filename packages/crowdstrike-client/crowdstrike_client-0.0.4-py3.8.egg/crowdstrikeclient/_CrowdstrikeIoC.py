import json

# Ioc
def IndicatorsQueriesDevices(self, payload):
    '''/indicators/queries/devices/v1'''
    return json.loads(self.GetAPI("indicators/queries/devices/v1?"+payload))

