import pytest
from snappy.snappy import Snappy

class TestSnappy:
    
    # Uncomment to perform snapshot test
    # def test_snappy_snap_roots(self):
        
    #     # Arrange
    #     instances = ["172.31.255.50", "172.31.255.20"]
    #     tags_specifications = [{
    #         "Key": "CreatorName",
    #         "Value": "mervin.hemaraju@checkout.com"
    #     }]
        
    #     # Act
    #     try:
    #         snappy = Snappy(instances)
            
    #         snapshots = snappy.snap_roots(tags_specifications)
            
    #         print(f"test_snappy_snap_roots: {snapshots}")
            
    #     except Exception as e:
    #         result = str(e)
            
    #         print(f"test_snappy_snap_roots: {result}")
            
    #     # Assert
    #     assert False
            
    testdata = [
        
        #### -> Testing for Mixed hostnames and ip addresses
        (["172.31.255.50", "172.31.255.20"], "Passed", 2),
        (["172.31.255.50", "172.31.255.20", "lin_jump_pub_01"], "Passed", 3),
        (["win_ad_01", "win_jump_pub_01", "lin_jump_pub_01"], "Passed", 3),
        (["172.31.255.50", "10.0.0.0"], "The following instances could not be retrieved: ['10.0.0.0']", 0),
        (["win_jump_pub_01", "winlin_jump_pub_01"], "The following instances could not be retrieved: ['winlin_jump_pub_01']", 0),
        (["win_jump_pub_01", "172.31.255.50", "winlin_jump_pub_01"], "The following instances could not be retrieved: ['winlin_jump_pub_01']", 0),
        (["win_jump_pub_01", "10.0.0.0", "winlin_jump_pub_01"], "The following instances could not be retrieved: ['10.0.0.0', 'winlin_jump_pub_01']", 0),
        (["172.31.255.30", "172.31.255.50", "winlin_jump_pub_01"], "The following instances could not be retrieved: ['winlin_jump_pub_01']", 0),
        (["win_jump_pub_01", "10.0.0.0"], "The following instances could not be retrieved: ['10.0.0.0']", 0),
        
        #### -> Testing for Duplicates
        (["172.31.255.50", "172.31.255.50", "172.31.255.20"], "Passed", 2),
        (["172.31.255.50", "172.31.255.50", "172.31.255.50"], "Passed", 1),
        (["lin_jump_pub_01", "172.31.255.30", "172.31.255.30"], "Passed", 1),
        (["lin_jump_pub_01", "172.31.255.30", "172.31.255.20"], "Passed", 2),
    ]
    @pytest.mark.parametrize("test_data,expected_result,expected_size", testdata)
    def test_snappy_initialization(self,test_data,expected_result,expected_size):
        # Arrange
        
        # Act
        try:
            snappy = Snappy(test_data)
            result = "Passed"
        except Exception as e:
            result = str(e)
            
        # Assert
        assert result == expected_result
        
        if result == "Passed":                
            assert len(snappy.instances) == expected_size
        