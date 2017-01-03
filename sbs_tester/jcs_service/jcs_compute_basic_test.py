from jcs_sbs_sdk.model.create_snapshot_request import CreateSnapshotRequest
from jcs_sbs_sdk.model.create_volume_request import CreateVolumeRequest
from jcs_sbs_sdk.model.delete_snapshot_request import DeleteSnapshotRequest
from jcs_sbs_sdk.model.delete_volume_request import DeleteVolumeRequest
from jcs_sbs_sdk.model.snapshot import Snapshot
from jcs_sbs_sdk.model.volume import Volume
from jcs_sbs_sdk.service.jcs_compute_client import JCSComputeClient
from time import sleep
import unittest

from sbs_tester.common import utils

import basic_test

class JCSComputeBasicTest(unittest.TestCase):
        
    def setUp(self):
        utils.created_volume_ids = []
        utils.created_snapshot_ids = []
        self.jcs = JCSComputeClient()
    
    def test_create_and_delete(self):
         
        #*****************create volume*******************
         
        request = CreateVolumeRequest()
        request.size = 10
         
        response = basic_test.create_volume_test(self,request)
        self.assertEqual(request.size, response.volume.size, "Create volume basic test: volume size")
         
        volume_id = response.volume.volume_id
         
           
        #*****************create snapshot*******************
           
        request = CreateSnapshotRequest()
        request.volume_id = volume_id
        response = basic_test.create_snapshot_test(self,request)
        snapshot_id = response.snapshot.snapshot_id
         
        #*****************delete volume*******************
           
        request = DeleteVolumeRequest()
        request.volume_id = volume_id
        response = basic_test.delete_volume_test(self,request)
 
        #"*****************delete snapshot*******************
           
        request = DeleteSnapshotRequest()
        request.snapshot_id = snapshot_id
        response = basic_test.delete_snapshot_test(self,request)
        pass
    
    
    def tearDown(self):
        for volume_id in utils.created_volume_ids:
            try:
                request = DeleteVolumeRequest()
                request.volume_id = volume_id
                basic_test.delete_volume_test(self,request)
            except Exception as e:
                print(e)
                continue
        
        for snapshot_id in utils.created_snapshot_ids:
            try:
                request = DeleteSnapshotRequest()
                request.snapshot_id = snapshot_id
                basic_test.delete_snapshot_test(self,request)
            except Exception as e:
                print(e)
                continue



