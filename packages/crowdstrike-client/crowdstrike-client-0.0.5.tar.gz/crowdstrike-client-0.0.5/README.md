# crowdstrike-client
CrowdStrike API Client Library (nonofficial)

### Install
```bash
pip install crowdstrike-client
```

### Usage
```python
from crowdstrikeclient import CrowdStrike

cs = CrowdStrike("ht://endpoint", "client", "secret")
print ("My JWT Token", cs.GetToken())
print ("My Ccid:", cs.SensorsQueriesInstallersCcid()
cs.Close()
```
