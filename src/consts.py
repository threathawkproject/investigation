NANOID_CHARSET = "0123456789abcdefghij"
NANOID_LENGTH = 4
ENRICHMENT_URL = "http://localhost:8000"
ENCODING_URL = "http://localhost:8081"
stix_types = [
    "indicator",
    "attack-pattern",
    "location",
    "threat-actor",
    "malware",
    "tool",		
    "campaign",
    "relationship",
    "domain-name",
    "intrusion-set",
    "email"
]

investigation_types = [
    {
        "name": "Domain Name",
        "value": "domain",
        "type": "domain-name"
    },
    {
        "name": "Email Address",
        "value": "email",
        "type": "email-addr"
    },
    {
        "name": "MD5",
        "value": "md5",
        "type":  "indicator"
    },
    {
        "name": "SHA1",
        "value": "sha1",
        "type":  "indicator"
    },
    {
        "name": "SHA256",
        "value": "sha256",
        "type":  "indicator"
    },
    {
        "name": "IP address",
        "value": "ip",
        "type":  "indicator"
    },
    {
        "name": "URL",
        "value": "url",
        "type":  "indicator"
    },
    {
        "name": "Attack Pattern",
        "value": "attack-pattern",
        "type":  "attack-pattern"
    },
    {
        "name": "Threat Actor",
        "value": "threat-actor",
        "type":  "threat-actor"
    },
    {
        "name": "Malware",
        "value": "malware",
        "type":  "malware"
    },
    {
        "name": "Tool",
        "value": "tool",
        "type":  "tool",
    },
    {
        "name": "Campaign",
        "value": "campaign",
        "type":  "campaign"    
    },
    {
        "name": "Intrusion Set",
        "value": "intrusion-set",
        "type":  "intrusion-set"
    },
    {
        "name": "Location",
        "value": "location",
        "type":  "location"
    },

]