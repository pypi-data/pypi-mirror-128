import pytest
from snappy.utils.helper import retrieve_failed_instances, is_an_ip_address, organize_instances, remove_duplicate_instances


###########################
####### Test Models #######
###########################
class MyInstanceT:
    
    def __init__(self, private_ip, name) -> None:
        self.private_ip = private_ip
        self.name = name
        
class TestHelper:
        
    testdata = [
        (
            ["10.10.10.1", "10.10.10.2","10.10.10.3", "10.10.10.4"], 
            [MyInstanceT("10.10.10.1", "test1"), MyInstanceT("10.10.10.3", "test2")], 
            ["10.10.10.2", "10.10.10.4"]
        ),
        (
            ["test1", "test2","test3"], 
            [MyInstanceT("10.10.10.1", "test1"), MyInstanceT("10.10.10.3", "test2")], 
            ["test3"]
        ),
        (
            ["10.10.10.1", "10.10.10.2","test3", "10.10.10.4"], 
            [MyInstanceT("10.10.10.1", "test1"), MyInstanceT("10.10.10.3", "test3")], 
            ["10.10.10.2", "10.10.10.4"]
        ),
        (
            ["10.10.10.1", "10.10.10.2","test3", "test4"], 
            [MyInstanceT("10.10.10.1", "test1"), MyInstanceT("10.10.10.3", "test3")], 
            ["10.10.10.2", "test4"]
        ),
        (
            ["10.10.10.1", "10.10.10.2"], 
            [MyInstanceT("10.10.10.1", "test1"), MyInstanceT("10.10.10.2", "test3")], 
            []
        ),
        (
            ["test1", "test3"], 
            [MyInstanceT("10.10.10.1", "test1"), MyInstanceT("10.10.10.2", "test3")], 
            []
        ),
    ]
    @pytest.mark.parametrize("previous_instances,retrieved_instances,expected_result", testdata)
    def test_retrieve_failed_instances(self, previous_instances, retrieved_instances, expected_result):  
        # Arrange
        
        # Act
        result = retrieve_failed_instances(previous_instances, retrieved_instances)
        
        # Assert
        assert expected_result == result


    testdata = [
        ("1.1.1.1", True),
        ("10.10.10.10", True),
        ("1.10.100.255", True),
        ("255.255.255.255", True),
        ("255.255.255.256", False),
        ("255.255.256.255", False),
        ("255.256.255.255", False),
        ("256.255.255.255", False),
        ("192.168.100.", False),
        ("300.168.100.1", False),
        ("1.168.100.300", False),
        ("192.168..1", False),
        ("192..1.1", False),
        (".1.1.1", False),
        ("hello.168.100.1", False),
        ("t.r.s.a", False),
        ("100.1.1.1:20", False),
    ]
    @pytest.mark.parametrize("test_data,expected_result", testdata)
    def test_is_an_ip_address(self,test_data,expected_result):
        # Arrange

        # Act
        result = is_an_ip_address(test_data)

        # Assert
        assert result == expected_result
        
    
    testdata = [
        (["1.1.1.1", "server_1", "server_2", "2.2.2.2"], ["1.1.1.1","2.2.2.2"], ["server_1", "server_2"]),
        (["1.1.1.1", "2.2.2.2"], ["1.1.1.1","2.2.2.2"], []),
        (["server_1", "server_2"], [], ["server_1", "server_2"]),
        ([], [], []),
        (["1.1.1.1", "server_1", "server_2", "2.2.2.2", "3.3.3.3"], ["1.1.1.1","2.2.2.2", "3.3.3.3"], ["server_1", "server_2"]),
    ]
    @pytest.mark.parametrize("test_data,expected_ips,expected_hostnames", testdata)
    def test_organize_instances(self,test_data,expected_ips,expected_hostnames):
        # Arrange

        # Act
        result_ips, result_hostnames = organize_instances(test_data)

        # Assert
        assert expected_ips == result_ips
        assert expected_hostnames == result_hostnames
        
    testdata = [
        (
            [MyInstanceT("1.1.1.1", ""),MyInstanceT("1.1.1.2", ""),MyInstanceT("1.1.1.1", ""),MyInstanceT("1.1.1.2", "")], 
            [MyInstanceT("1.1.1.1", ""),MyInstanceT("1.1.1.2", "")]
        ),
        ([MyInstanceT("1.1.1.1", ""),MyInstanceT("1.1.1.2", ""),MyInstanceT("1.1.1.1", ""),MyInstanceT("1.1.1.2", ""),MyInstanceT("1.1.1.2", "")], [MyInstanceT("1.1.1.1", ""),MyInstanceT("1.1.1.2", "")]),
        ([MyInstanceT("1.1.1.1", ""),MyInstanceT("1.1.1.2", ""),MyInstanceT("1.1.1.2", ""),MyInstanceT("1.1.1.2", "")], [MyInstanceT("1.1.1.1", ""),MyInstanceT("1.1.1.2", "")]),
        ([MyInstanceT("1.1.1.2", ""),MyInstanceT("1.1.1.2", ""),MyInstanceT("1.1.1.2", "")], [MyInstanceT("1.1.1.2", "")]),
        ([MyInstanceT("1.1.1.1", ""),MyInstanceT("1.1.1.2", ""),MyInstanceT("1.1.1.3", "")], [MyInstanceT("1.1.1.1", ""),MyInstanceT("1.1.1.2", ""),MyInstanceT("1.1.1.3", "")]),
    ]
    @pytest.mark.parametrize("test_data,expected_result", testdata)
    def test_remove_duplicate_instances(self,test_data, expected_result):
        
        # Act
        result = remove_duplicate_instances(test_data)
        
        # Assert
        assert [r.private_ip for r in result] == [er.private_ip for er in expected_result]
        assert len(result) == len(expected_result)