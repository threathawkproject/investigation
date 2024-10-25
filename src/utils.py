import requests
import os
from stix2 import Environment, FileSystemSource, FileSystemSink, Filter
from stix2 import Bundle
import json
import nanoid
import consts

from models.models import Investigation, InvestigateRequest, CreateInvestigation, SaveInvestigation


# generating a new nanoid
def generate_nanoid():
    return nanoid.generate(consts.NANOID_CHARSET, consts.NANOID_LENGTH)

def check_by_type_and_id(env, stix_id, type):
    by_type = Filter('type', '=', type)
    by_id = Filter('id', '=', stix_id)
    stix_obj = env.query([
        by_type,
        by_id
    ])
    print(stix_obj)
    if len(stix_obj) > 0:
        return True
    return False


def create_investigation(data: CreateInvestigation):
    nano_id = generate_nanoid()
    file_path = f"./data/{nano_id}"
    try:
        ENCODING_URL = os.getenv('ENCODING_URL', default="http://localhost:8001")
        URL = f"{ENCODING_URL}/generate_sdo"
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

        print(type(root_node))
        print(root_node)

        os.mkdir(file_path)
        stix_sink = FileSystemSink(file_path, allow_custom=True, bundlify=True)
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
    ENRICHMENT_URL = os.getenv('ENRICHMENT_URL', default="http://localhost:8000")
    URL = f"{ENRICHMENT_URL}/analyze"
    try:
        response = requests.post(
            url=URL,
            json=investigate_request.enrichment
        )
        response.raise_for_status()
        data = response.json()
        stix_sink = FileSystemSink(file_path, allow_custom=True, bundlify=True)
        stix_source = FileSystemSource(file_path, allow_custom=True)
        env = Environment(source=stix_source,sink=stix_sink)
        for analyzer in investigate_request.enrichment["selected_analyzers"]:            
            sdos = data[analyzer]
            for sdo in sdos:
                stix_obj = json.loads(sdo)
                if stix_obj["type"] != "relationship":
                    print(f"id: {stix_obj['id']} || type: {stix_obj['type']}")
                    exists = check_by_type_and_id(env, stix_obj["id"], stix_obj["type"])
                    if not exists:
                        env.add([sdo])
                else:
                    env.add([sdo])
        return True, None
    except Exception as e:
        print(str(e))
        return False, e

def display_investigation(investigation: Investigation):
    stix_source = FileSystemSource(investigation.file_path, allow_custom=True)
    env = Environment(source=stix_source)
    objects = []
    for stix in consts.stix_types:
        object_filter = Filter('type', '=', stix)
        results = env.query(object_filter)
        if len(results) > 0:
            objects.extend(results)
    bundle = Bundle(objects=objects, allow_custom=True)
    return bundle.serialize()


def save_investigation(client, investigation_data):
    pass
