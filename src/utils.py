import requests
import os
from stix2 import Environment, FileSystemSource, FileSystemSink, Filter
from stix2 import Bundle
import json
import nanoid
import consts

from models.models import Investigation, InvestigateRequest, CreateInvestigation


# generating a new nanoid
def generate_nanoid():
    return nanoid.generate(consts.NANOID_CHARSET, consts.NANOID_LENGTH)

def create_investigation(data: CreateInvestigation):
    nano_id = generate_nanoid()
    file_path = f"./data/{nano_id}"
    try:
        URL = f"{consts.ENCODING_URL}/generate_sdo"
        print(data)
        data_to_send = {
            "type": data.type,
            "data": {
                "value": data.data["value"],
                "type": data.data["type"]
            }
        }
        response = requests.post(
            url=URL,
            json=data_to_send
        )
        root_node = json.loads(response.json())

        os.mkdir(file_path)
        stix_sink = FileSystemSink(file_path)
        env = Environment(sink=stix_sink)
        env.add([root_node])
        print(root_node)
        data = {
            "file_path": file_path,
            "root_node_id": root_node["id"]
        }
        return data
    except Exception as e:
        print(str(e))
        return None

def preform_investigation(investigate_request: InvestigateRequest):
    file_path = investigate_request.file_path
    URL = f"{consts.ENRICHMENT_URL}/analyze"
    try:
        response = requests.post(
            url=URL,
            json=investigate_request.enrichment
        )
        response.raise_for_status()
        data = response.json()
        stix_sink = FileSystemSink(file_path)
        env = Environment(sink=stix_sink)
        for analyzer in investigate_request.enrichment["selected_analyzers"]:            
            sdos = data[analyzer]
            for sdo in sdos:
                env.add([sdo])
        return True, None
    except Exception as e:
        print(str(e))
        return False, e

def display_investigation(investigation: Investigation):
    stix_source = FileSystemSource(investigation.file_path)
    env = Environment(source=stix_source)
    objects = []
    for stix in consts.stixs:
        object_filter = Filter('type', '=', stix)
        results = env.query(object_filter)
        if len(results) > 0:
            objects.extend(results)
    bundle = Bundle(objects=objects)
    return bundle.serialize()