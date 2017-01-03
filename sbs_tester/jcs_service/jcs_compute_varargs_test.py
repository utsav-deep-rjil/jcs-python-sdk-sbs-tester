from jcs_sbs_sdk.model.create_snapshot_request import CreateSnapshotRequest
from jcs_sbs_sdk.model.create_volume_request import CreateVolumeRequest
from jcs_sbs_sdk.model.delete_snapshot_request import DeleteSnapshotRequest
from jcs_sbs_sdk.model.delete_volume_request import DeleteVolumeRequest
from jcs_sbs_sdk.model.describe_snapshots_request import DescribeSnapshotsRequest
from jcs_sbs_sdk.model.describe_volumes_request import DescribeVolumesRequest
from jcs_sbs_sdk.model.snapshot import Snapshot
from jcs_sbs_sdk.model.volume import Volume
from jcs_sbs_sdk.service.jcs_compute_client import JCSComputeClient
from time import sleep
import unittest

from sbs_tester.common import utils

import basic_test

class JCSComputeVarArgsTest(unittest.TestCase):
        
    def setUp(self):
        utils.created_volume_ids = []
        utils.created_snapshot_ids = []
        self.jcs = JCSComputeClient()


    
    def test_variable_arguments(self):
        
        
     
        #*****************create volume*******************
         
        request = CreateVolumeRequest()
        request.size = 10
        request.encrypted = True
         
        response = basic_test.create_volume_test(self, request)
        self.assertEqual(request.size, response.volume.size, "Create volume varargs test 1: volume size")
        self.assertEqual(request.encrypted, response.volume.encrypted, "Create volume varargs test 1: encryption")
         
         
        volume_id = response.volume.volume_id
         
           
        #*****************create snapshot*******************
           
        request = CreateSnapshotRequest()
        request.volume_id = volume_id
        response = basic_test.create_snapshot_test(self, request)
        snapshot_id = response.snapshot.snapshot_id
         
         
        #****************create volume with snapshot_id, size and encryption *******************
         
         
        request = CreateVolumeRequest()
        request.size = 20
        request.encrypted = True
        request.snapshot_id = snapshot_id
         
        response = basic_test.create_volume_test(self, request)
        self.assertEqual(request.size, response.volume.size, "Create volume varargs test 2: volume size")
        self.assertEqual(request.encrypted, response.volume.encrypted, "Create volume varargs test 2: encryption")
        self.assertEqual(request.snapshot_id, response.volume.snapshot_id, "Create volume varargs test 2: snapshot ID")
         
        request.volume_type = "standard"
        request.encrypted = False
         
        response = basic_test.create_volume_test(self, request)
        self.assertEqual(request.size, response.volume.size, "Create volume varargs test 3: volume size")
        # The source snapshot was encrypted so even if request.encrypted is False, created volume will be encrypted:
        self.assertEqual(True, response.volume.encrypted, "Create volume varargs test 3: encryption")
        self.assertEqual(request.snapshot_id, response.volume.snapshot_id, "Create volume varargs test 3: snapshot ID")
        self.assertEqual(request.volume_type, response.volume.volume_type, "Create volume varargs test 3: volume type")
         
         
        #***************** describe volumes *******************
        
        request = DescribeVolumesRequest()
        request.volume_ids = utils.created_volume_ids
        
        response = basic_test.describe_volumes_test(self, request)
        
        request = DescribeVolumesRequest()
        response = basic_test.describe_volumes_test(self, request)
        
        expected_volumes = response.volumes
        
        request.max_results = 5
        response = basic_test.describe_volumes_test(self, request)
        actual_volumes = response.volumes
        
        while len(response.volumes) > 0:
            request.next_token = response.volumes[-1].volume_id
            response = basic_test.describe_volumes_test(self, request)
            actual_volumes.extend(response.volumes)
        
        
        actual_volumes_str = utils.list_to_str(actual_volumes)
        expected_volumes_str = utils.list_to_str(expected_volumes)
        print(actual_volumes_str)
        print(expected_volumes_str)
        
        self.assertEqual(actual_volumes_str, expected_volumes_str, "Describe volumes varargs test 2: by max_results and next_token: final result")
        
        
        request = DescribeVolumesRequest()
        request.detail = True
        response = basic_test.describe_volumes_test(self, request)
        
        
        
        #******************** describe snapshots ********************
        
        request = DescribeSnapshotsRequest()
        request.snapshot_ids = utils.created_snapshot_ids
        
        response = basic_test.describe_snapshots_test(self, request)
        
        request = DescribeSnapshotsRequest()
        response = basic_test.describe_snapshots_test(self, request)
        
        expected_snapshots = response.snapshots
        
        request.max_results = 5
        response = basic_test.describe_snapshots_test(self, request)
        actual_snapshots = response.snapshots
        
        while len(response.snapshots) > 0:
            request.next_token = response.snapshots[-1].snapshot_id
            response = basic_test.describe_snapshots_test(self, request)
            actual_snapshots.extend(response.snapshots)
        
        
        actual_snapshots_str = utils.list_to_str(actual_snapshots)
        expected_snapshots_str = utils.list_to_str(expected_snapshots)
        
        print(actual_snapshots_str)
        print(expected_snapshots_str)
        
        
        self.assertEqual(actual_snapshots_str, expected_snapshots_str, "Describe snapshots varargs test 2: by max_results and next_token: final result")
        
        
        request = DescribeSnapshotsRequest()
        request.detail = True
        response = basic_test.describe_snapshots_test(self, request)
        
    
    def tearDown(self):
        for volume_id in utils.created_volume_ids:
            try:
                request = DeleteVolumeRequest()
                request.volume_id = volume_id
                basic_test.delete_volume_test(self, request)
            except Exception as e:
                print(e)
                continue
        
        for snapshot_id in utils.created_snapshot_ids:
            try:
                request = DeleteSnapshotRequest()
                request.snapshot_id = snapshot_id
                basic_test.delete_snapshot_test(self, request)
            except Exception as e:
                print(e)
                continue



