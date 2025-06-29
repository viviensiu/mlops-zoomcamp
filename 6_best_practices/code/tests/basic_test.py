# Comparison of naming convention for Testing to detect test cases 
def unit_test_1():
    # not detected by Testing
    x = 2
    y = 1
    assert x == y

def test_1():
    # detected by Testing 
    x = 2
    y = 1
    assert x == y