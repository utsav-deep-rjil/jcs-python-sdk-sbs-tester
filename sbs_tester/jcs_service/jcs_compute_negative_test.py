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
from urllib2 import HTTPError

import basic_test
from sbs_tester.common import utils


class JCSComputeNegativeTest(unittest.TestCase):
        
    def setUp(self):
        utils.created_volume_ids = []
        utils.created_snapshot_ids = []
        self.jcs = JCSComputeClient()

    
    def create_negative_sized_volume_test(self):
        
        request = CreateVolumeRequest()
        request.size = -10
        basic_test.create_volume_test(self, request)
    
        
    def test_negative_cases(self):
        
        #***************** describe volumes: list of random strings passed as volume IDs *******************
        
        request = DescribeVolumesRequest()
        request.volume_ids = ["list", "of", "random", "strings"]
        
        self.assertRaises(HTTPError, basic_test.describe_volumes_test, self, request)
        
        #***************** describe volumes: negative max_results ******************************************
        
        request = DescribeVolumesRequest()
        
        request.max_results = -1
        
        self.assertRaises(HTTPError, basic_test.describe_volumes_test, self, request)
        
        
        
        
        #***************** describe snapshots: list of random strings passed as snapshot IDs *******************
        
        request = DescribeSnapshotsRequest()
        request.snapshot_ids = ["list", "of", "random", "strings"]
        
        self.assertRaises(HTTPError, basic_test.describe_snapshots_test, self, request)
        
        #**************describe snapshots: negative max_results**************************
#         
#         request = DescribeSnapshotsRequest()
#         response = basic_test.describe_snapshots_test(self, request)
#          
#         print(response.xml)
#         expected_snapshots = response.snapshots
#         request.max_results = -3
#          
#         response = basic_test.describe_snapshots_test(self, request)
#         actual_snapshots = response.snapshots
#          
#         print(response.xml)
#         print(utils.list_to_str(actual_snapshots))
#         print(utils.list_to_str(expected_snapshots))
#          
#         self.assertListEqual(actual_snapshots, expected_snapshots, "Describe snapshots negative test 2: negative  max_results")
        
         
         
        #*****************create volume with negative size*******************
         
        self.assertRaises(ValueError,self.create_negative_sized_volume_test)
         
         
        #*****************create volume*******************
        request = CreateVolumeRequest()
        request.size = 20
        response = basic_test.create_volume_test(self, request)
        volume_id = response.volume.volume_id
         
           
        #*****************create snapshot*******************
           
        request = CreateSnapshotRequest()
        request.volume_id = volume_id
        response = basic_test.create_snapshot_test(self, request)
        snapshot_id = response.snapshot.snapshot_id
         
         
        #****************create volume with snapshot_id and size < snapshot.volume_size*******************
         
         
        request = CreateVolumeRequest()
        request.size = 10
        request.snapshot_id = snapshot_id
         
        self.assertRaises(HTTPError, basic_test.create_volume_test,self, request)
         
         
        #****************create volume with random string as snapshot ID*******************
         
        request = CreateVolumeRequest()
        request.snapshot_id = "random string"
         
        self.assertRaises(HTTPError, basic_test.create_volume_test,self, request)
         
        #****************create snapshot with random string as volume ID*******************
         
         
        request = CreateSnapshotRequest()
        request.volume_id = "random string"
         
        self.assertRaises(HTTPError, basic_test.create_snapshot_test,self, request)
         
         
        #******************delete same volume twice*******************
         
        request = DeleteVolumeRequest()
        request.volume_id = volume_id
        basic_test.delete_volume_test(self, request)
        self.assertRaises(HTTPError, basic_test.delete_volume_test,self, request)
         
         
        #****************delete volume: random string as volume_id*********************
         
        request.volume_id = "any random string as volume_id"
        self.assertRaises(HTTPError, basic_test.delete_volume_test,self, request)
         
         
        #******************delete same snapshot twice*******************
         
        request = DeleteSnapshotRequest()
        request.snapshot_id = snapshot_id
        basic_test.delete_snapshot_test(self, request)
        self.assertRaises(HTTPError, basic_test.delete_snapshot_test,self, request)
         
         
        #******************delete snapshot: random string as snapshot_id*******************
         
        request.snapshot_id = "any random string as snapshot_id"
        self.assertRaises(HTTPError, basic_test.delete_snapshot_test,self, request)
         
         
        
        
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



