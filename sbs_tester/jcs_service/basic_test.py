
from jcs_sbs_sdk.model.snapshot import Snapshot
from jcs_sbs_sdk.model.volume import Volume
from time import sleep

from sbs_tester.common import utils


    
def describe_volumes_test(utest, request):
    if request is None:
        return
    
    response = utest.jcs.describe_volumes(request)
    utest.assertIsNotNone(response)
    utest.assertIsNotNone(response.volumes)
    utest.assertIsInstance(response.volumes, list, "Describe volumes test 1: volumes must be a list")
    
    for volume in response.volumes:
        utest.assertIsInstance(volume, Volume, "Describe volumes test 1: volumes must be list of Volume objects")
        if request.detail == True:
            utest.assertIsNotNone(volume.attachments, "Describe volumes test 3: with detail: attachments")
            utest.assertIsNotNone(volume.create_time, "Describe volumes test 3: with detail: create_time")
            utest.assertIsNotNone(volume.size, "Describe volumes test 3: with detail: size")
            utest.assertIsNotNone(volume.encrypted, "Describe volumes test 3: with detail: encrypted")
    
    if isinstance(request.volume_ids, list) and len(request.volume_ids)>0:
        volume_ids_str = "#".join(request.volume_ids)
        for volume in response.volumes:
            utest.assertIn(volume.volume_id, volume_ids_str, "Describe volumes varargs test 1: by volume_id: volume_ids")
    
    return response


def describe_snapshots_test(utest, request):
    if request is None:
        return
    
    response = utest.jcs.describe_snapshots(request)
    utest.assertIsNotNone(response)
    utest.assertIsNotNone(response.snapshots)
    utest.assertIsInstance(response.snapshots, list, "Describe snapshots test 1: snapshots must be a list")
    
    for snapshot in response.snapshots:
        utest.assertIsInstance(snapshot, Snapshot, "Describe snapshots test 1: snapshots must be list of snapshot objects")
        if request.detail == True:
            utest.assertIsNotNone(snapshot.start_time, "Describe snapshots test 3: with detail: create_time")
            utest.assertIsNotNone(snapshot.volume_size, "Describe snapshots test 3: with detail: size")
            utest.assertIsNotNone(snapshot.encrypted, "Describe snapshots test 3: with detail: encrypted")
    
    if isinstance(request.snapshot_ids, list) and len(request.snapshot_ids)>0:
        snapshot_ids_str = "#".join(request.snapshot_ids)
        for snapshot in response.snapshots:
            utest.assertIn(snapshot.snapshot_id, snapshot_ids_str, "Describe snapshots varargs test 1: by snapshot_id: snapshot_ids")
    
    return response


def create_volume_test(utest, request):
    if request is None:
        return
    
    initial_volume_count = utils.get_volumes_count()
    
    response = utest.jcs.create_volume(request)
    volume_id = response.volume.volume_id
    utils.print_request_response(request, response, msg="create volume")
    utils.created_volume_ids.append(volume_id)
    
    final_volume_count = utils.get_volumes_count()
    
    utest.assertEqual(initial_volume_count, final_volume_count - 1, "Create volume basic test: volume count")
    utest.assertIsNotNone(response)
    utest.assertIsNotNone(response.volume)
    
    while utils.get_volume_status(volume_id) != "available":
        sleep(10)
    
    return response


def create_snapshot_test(utest, request):
    if request is None:
        return
    
    initial_snpshot_count = utils.get_snapshots_count()
    
    response = utest.jcs.create_snapshot(request)
    snapshot_id = response.snapshot.snapshot_id
    utils.print_request_response(request, response, msg="create snapshot")
    
    final_snapshot_count = utils.get_snapshots_count()
    
    utest.assertEqual(initial_snpshot_count, final_snapshot_count - 1, "Create snapshot basic test: snapshot count")
    utest.assertIsNotNone(response)
    utest.assertIsNotNone(response.snapshot)
    utest.assertEqual(request.volume_id, response.snapshot.volume_id, "Create snapshot basic test: source volume id")
    
    utils.created_snapshot_ids.append(response.snapshot.snapshot_id)
    
    snapshot_status = utils.get_snapshot_status(snapshot_id)
    while snapshot_status != "completed" and snapshot_status != "error":
        sleep(20)
        snapshot_status = utils.get_snapshot_status(snapshot_id)
        
    return response


def delete_volume_test(utest, request):
    if request is None:
        return
    
    initial_volume_count = utils.get_volumes_count()
    
    response = utest.jcs.delete_volume(request)
    utils.print_request_response(request, response, msg="delete volume")
    
    
    while utils.get_volume_status(request.volume_id) == "deleting":
        sleep(10)
    
    final_volume_count = utils.get_volumes_count()
    
    utest.assertEqual(initial_volume_count, final_volume_count + 1, "Delete volume basic test: volume count")
    utest.assertIsNotNone(response)
    utest.assert_(response.deleted, "Delete volume basic test: return value")
    
    return response


def delete_snapshot_test(utest, request):
    if request is None:
        return
    
    initial_snpshot_count = utils.get_snapshots_count()
    
    response = utest.jcs.delete_snapshot(request)
    utils.print_request_response(request, response, msg="delete snapshot")
    
    while utils.get_snapshot_status(request.snapshot_id) == "deleting":
        sleep(60)
    
    final_snapshot_count = utils.get_snapshots_count()
    
    utest.assertEqual(initial_snpshot_count, final_snapshot_count + 1, "Delete snapshot basic test: snapshot count")
    utest.assertIsNotNone(response)
    utest.assert_(response.deleted, "Delete snapshot basic test: return value")
    
    return response




