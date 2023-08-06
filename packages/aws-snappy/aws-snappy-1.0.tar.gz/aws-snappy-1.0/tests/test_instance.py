import json
import snappy.utils.constants as Consts
from snappy.instance import Instance

class TestInstance:

    # Uncomment to perform snapshot test
    # def test_snap_root_NormalValues(self):
    #     # Arrange
    #     instance_json = json.load(open("tests/test_data/test_data_instance_for_snapshot_02.json"))
    #     tags_specifications = [{
    #         "Key": "CreatorName",
    #         "Value": "mervin.hemaraju@checkout.com"
    #     }]

    #     # Act
    #     instance = Instance(instance_json)
    #     snapshot = instance.snap_root(tags_specifications=tags_specifications)
    #     print(f"test_snap_root_NormalValues: {snapshot}")

    #     assert False
    
    # Uncomment to perform snapshot test
    # def test_snap_root_NoTagsSpecifications1Of2(self):
    #     # Arrange
    #     instance_json = json.load(open("tests/test_data/test_data_instance_for_snapshot_01.json"))
    #     tags_specifications = None

    #     # Act
    #     instance = Instance(instance_json)
    #     snapshot = instance.snap_root(tags_specifications=tags_specifications)
    #     print(f"test_snap_root_NoTagsSpecifications1Of2: {snapshot}")

    #     assert False
    
    # Uncomment to perform snapshot test
    # def test_snap_root_NoTagsSpecifications2Of2(self):
    #     # Arrange
    #     instance_json = json.load(open("tests/test_data/test_data_instance_for_snapshot_03.json"))
    #     tags_specifications = []

    #     # Act
    #     instance = Instance(instance_json)
    #     snapshot = instance.snap_root(tags_specifications=tags_specifications)
    #     print(f"test_snap_root_NoTagsSpecifications2Of2: {snapshot}")

    #     assert False

    def test_load_instance_NoTagsDefined(self):
        # Arrange
        instance_json = json.load(open("tests/test_data/test_data_instance_no_tags.json"))
        expected_id = "i-009ced0eee26e121d"
        expected_private_ip = "172.31.255.20"
        expected_root_volume = "vol-0ab3909a5663e3a0c"
        expected_volumes = ["vol-0ab3909a5663e3a0c", "vol-0f3e69129f69e362f", "vol-0b4faf065769820dd", "vol-01f7d821d55743bfc"]
        expected_name = None

        # Act
        instance = Instance(instance_json)
        result_private_ip = instance.private_ip
        result_root_volume = instance.root_volume
        result_volumes = instance.volumes
        result_name = instance.name
        result_id = instance.id

        assert result_private_ip == expected_private_ip
        assert result_root_volume == expected_root_volume
        assert result_volumes == expected_volumes
        assert result_name == expected_name
        assert result_id == expected_id

    def test_load_instance_NoNameTagDefined(self):
        # Arrange
        instance_json = json.load(open("tests/test_data/test_data_instance_no_name.json"))
        expected_id = "i-009ced0eee26e121d"
        expected_private_ip = "172.31.255.20"
        expected_root_volume = "vol-0ab3909a5663e3a0c"
        expected_volumes = ["vol-0ab3909a5663e3a0c", "vol-0f3e69129f69e362f", "vol-0b4faf065769820dd", "vol-01f7d821d55743bfc"]
        expected_name = None

        # Act
        instance = Instance(instance_json)
        result_private_ip = instance.private_ip
        result_root_volume = instance.root_volume
        result_volumes = instance.volumes
        result_name = instance.name
        result_id = instance.id

        assert result_private_ip == expected_private_ip
        assert result_root_volume == expected_root_volume
        assert result_volumes == expected_volumes
        assert result_name == expected_name
        assert result_id == expected_id

    def test_load_instance_NoPrivateIpDefined(self):
        # Arrange
        instance_json = json.load(open("tests/test_data/test_data_instance_no_ip.json"))
        expected_id = "i-009ced0eee26e121d"
        expected_private_ip = None
        expected_root_volume = "vol-0ab3909a5663e3a0c"
        expected_volumes = ["vol-0ab3909a5663e3a0c", "vol-0f3e69129f69e362f", "vol-0b4faf065769820dd", "vol-01f7d821d55743bfc"]
        expected_name = "win_jump_pub_01"

        # Act
        instance = Instance(instance_json)
        result_private_ip = instance.private_ip
        result_root_volume = instance.root_volume
        result_volumes = instance.volumes
        result_name = instance.name
        result_id = instance.id

        assert result_private_ip == expected_private_ip
        assert result_root_volume == expected_root_volume
        assert result_volumes == expected_volumes
        assert result_name == expected_name
        assert result_id == expected_id

    def test_load_instance_NoVolumesDefined(self):
        # Arrange
        instance_json = json.load(open("tests/test_data/test_data_instance_no_volumes.json"))
        expected_result = "The instance 172.31.255.20 does not have any volumes."

        # Act
        try:
            instance = Instance(instance_json)
            result = "Failed"
        except Exception as e:
            result = str(e)

        assert expected_result == result

    def test_load_instance_NoRootVolumeDefined(self):
        # Arrange
        instance_json = json.load(open("tests/test_data/test_data_instance_no_root_volume.json"))
        expected_id = "i-009ced0eee26e121d"
        expected_private_ip =  "172.31.255.20"
        expected_root_volume = None
        expected_volumes = ["vol-0f3e69129f69e362f", "vol-0b4faf065769820dd", "vol-01f7d821d55743bfc"]
        expected_name = "win_jump_pub_01"

        # Act
        instance = Instance(instance_json)
        result_private_ip = instance.private_ip
        result_root_volume = instance.root_volume
        result_volumes = instance.volumes
        result_name = instance.name
        result_id = instance.id

        assert result_private_ip == expected_private_ip
        assert result_root_volume == expected_root_volume
        assert result_volumes == expected_volumes
        assert result_name == expected_name
        assert result_id == expected_id

    def test_load_instance_AllAttributesPresent(self):
        # Arrange
        instance_json = json.load(open("tests/test_data/test_data_instance_all_attributes.json"))
        expected_id = "i-009ced0eee26e121d"
        expected_private_ip = "172.31.255.20"
        expected_root_volume = "vol-0ab3909a5663e3a0c"
        expected_volumes = ["vol-0ab3909a5663e3a0c", "vol-0f3e69129f69e362f", "vol-0b4faf065769820dd", "vol-01f7d821d55743bfc"]
        expected_name = "win_jump_pub_01"

        # Act
        instance = Instance(instance_json)
        result_private_ip = instance.private_ip
        result_root_volume = instance.root_volume
        result_volumes = instance.volumes
        result_name = instance.name
        result_id = instance.id

        assert result_private_ip == expected_private_ip
        assert result_root_volume == expected_root_volume
        assert result_volumes == expected_volumes
        assert result_name == expected_name
        assert result_id == expected_id

    def test_snap_root_NoRootVolumeDefined(self):
        # Arrange
        instance_json = json.load(open("tests/test_data/test_data_instance_no_root_volume.json"))
        expected_result = Consts.EXCEPTION_MESSAGE_ROOT_VOLUME_NOT_FOUND

        # Act
        try:
            instance = Instance(instance_json)
            result = instance.snap_root([])
        except Exception as e:
            result = str(e)

        assert expected_result == result