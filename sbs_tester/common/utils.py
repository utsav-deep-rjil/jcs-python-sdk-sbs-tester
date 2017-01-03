from jcs_sbs_sdk.model.describe_snapshots_request import DescribeSnapshotsRequest
from jcs_sbs_sdk.model.describe_volumes_request import DescribeVolumesRequest
from jcs_sbs_sdk.service.jcs_compute_client import JCSComputeClient
import json
from urllib2 import HTTPError


created_volume_ids = []
created_snapshot_ids = []

jcs = JCSComputeClient()
def get_volume_status(volume_id):
    describe_volume_request = DescribeVolumesRequest()
    describe_volume_request.volume_ids = [volume_id]
    try:
        response = jcs.describe_volumes(describe_volume_request)
        print("Volume status: " + response.volumes[0].status)
        return response.volumes[0].status
    except HTTPError as e:
        print(e)
        return "Not Found"

def get_snapshot_status(snapshot_id):
    describe_snapshot_request = DescribeSnapshotsRequest()
    describe_snapshot_request.snapshot_ids = [snapshot_id]
    try:
        response = jcs.describe_snapshots(describe_snapshot_request)
        print("Snapshot status: " + response.snapshots[0].status)
        return response.snapshots[0].status
    except HTTPError as e:
        print(e)
        return "Not Found"
    

def get_volumes_count():
    describe_volume_request = DescribeVolumesRequest()
    response = jcs.describe_volumes(describe_volume_request)
    return len(response.volumes)

def get_snapshots_count():
    describe_snapshot_request = DescribeSnapshotsRequest()
    response = jcs.describe_snapshots(describe_snapshot_request)
    return len(response.snapshots)




def print_json(inp_str):
    # print(inp_str)
    parsed = json.loads(str(inp_str))
    print json.dumps(parsed, indent=4)

def print_request_response(request, response,msg=None):
    if msg is not None:
        print("\n************* %s ******************"%(msg))
    print("\nRequest object in JSON is:")
    print_json(request)
    print("\nAPI response XML is:")
    print(response.xml)
    print("\nSDK Response object in JSON is:")
    print_json(response)


def list_to_str(inp_list):
    ret = []
    for item in inp_list:
        ret.append(str(item))
    return '[%s]' % ','.join(ret)
    
    
    

