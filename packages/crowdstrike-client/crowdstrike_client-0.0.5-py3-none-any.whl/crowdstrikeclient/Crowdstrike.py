'''
Custom Crowdstrike library
--------------------------
Base Crowdstrike Class
Base API Requests Call
'''
import requests, json, datetime
from time import sleep
from base64 import b64encode

class CrowdStrike(object):
    def __init__(self, endpoint, clientid, secret, oauth_endpoint="https://api.crowdstrike.com/"):
        self.clientid = clientid
        self.secret = secret
        self.endpoint = endpoint # For API Requests
        self.oauth_endpoint = oauth_endpoint
        self.__jwt = self.__createtoken()
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer " + self.__jwt
        }
        
    # HOST
    from ._CrowdstrikeHost import DevicesQueriesDevices
    from ._CrowdstrikeHost import DevicesEntitiesDevices
    from ._CrowdstrikeHost import DevicesCombinedDevicesLoginhistory
    from ._CrowdstrikeHost import DevicesCombinedDevicesNetworkAddressHistory
    # SENSOR
    from ._CrowdstrikeSensor import SensorsQueriesInstallersCcid
    # MALQUERY
    from ._CrowdstrikeIntel import MalqueryEntitiesMetadata
    # IOC
    from ._CrowdstrikeIoC import IndicatorsQueriesDevices
    # Detects
    from ._CrowdstrikeDetects import DetectsQueriesDetects
    from ._CrowdstrikeDetects import DetectsEntitiesSummariesGET
    from ._CrowdstrikeDetects import DetectsEntitiesDetects
    # User Manegement
    from ._CrowdstrikeUserMenagement import UsersEntitiesUsers
    from ._CrowdstrikeUserMenagement import UsersQueriesUser_uuids_by_cid

    def GetToken(self):
        return self.__jwt

    def Close(self):
        self.__revoketoken()

    def GetAPI(self, path):
        '''Is public for custom requests'''
        req = requests.get(self.endpoint + path, headers=self.headers)
        if req.status_code == 403:
            print ("Forbidden, maybe Token or API have problem")
            exit(1)
        if req.status_code == 429 and "X-RateLimit-RetryAfter" in req.headers:
            self.__ratelimit(req.headers["X-RateLimit-RetryAfter"])
            self.GetAPI(path)
            return
        return req.text
    
    def PostAPI(self, path, payload):
        headers = self.headers
        headers.update({"Content-type": "application/json"})
        req = requests.post(self.endpoint + path, json=payload, headers=headers)
        if req.status_code == 403:
            print ("Forbidden, maybe Token or API have problem")
            exit(1)
        if req.status_code == 429 and "X-RateLimit-RetryAfter" in req.headers:
            self.__ratelimit(req.headers["X-RateLimit-RetryAfter"])
            self.PostAPI(payload)
            return
        return req.text

    def PatchAPI(self, path, payload):
        headers = self.headers
        headers.update({"Content-type": "application/json"})
        req = requests.patch(self.endpoint + path, json=payload, headers=headers)
        if req.status_code == 403:
            print ("Forbidden, maybe Token or API have problem")
            exit(1)
        if req.status_code == 429 and "X-RateLimit-RetryAfter" in req.headers:
            self.__ratelimit(req.headers["X-RateLimit-RetryAfter"])
            self.PostAPI(payload)
            return
        return req.text

    def __ratelimit(self, RetryAfter):
        RetryAfterTimestamp = int(RetryAfter)
        TimestampUTC = int(datetime.datetime.utcnow().strftime("%s"))
        print ("Reached the X-RateLimit-RetryAfter:\t" + str(RetryAfter))
        sleep(RetryAfterTimestamp - TimestampUTC)
        
    def __createtoken(self):
        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
            }
        payloads = {
            "client_id": self.clientid,
            "client_secret": self.secret
        }
        req = requests.post(self.oauth_endpoint + "oauth2/token", headers=headers, data=payloads)
        
        if req.status_code > 201:
            print ("HTTP ERROR:\t" + req.status_code + "\nMESSAGE:\t" + req.text)
            return
        
        resp_json = json.loads(req.text)
        if "access_token" in resp_json:
            return resp_json["access_token"]

    def __revoketoken(self):
        headers = {
            "Authorization": "Basic " + b64encode(str.encode(self.clientid+":"+self.secret)).decode(),
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
            }
        payloads = {
            "token": self.__jwt
        }
        req = requests.post(self.endpoint + "oauth2/revoke", headers=headers, data=payloads)
        if req.status_code == 200:
            self.__jwt = None

    def __custom_error(self, msg):
        return {
            "crowdstrikeclient" : {
                "error": msg
            }
        }