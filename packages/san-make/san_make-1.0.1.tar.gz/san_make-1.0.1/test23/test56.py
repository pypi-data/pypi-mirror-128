import pytest,os

o=os.path.dirname(__file__)
print(o)
pytest.main(['-v','--html=o/12.html','D:/python test/test23/'])
