import myutils

def test_testfunction():
    assert myutils.arbitraryTestFunc(5) == True 
    assert myutils.arbitraryTestFunc(1) == False 
def testIPwithIP():
    assert myutils.isIP('1.1.1.1') == True
    assert myutils.isIP('2001:db8::') == True
    assert myutils.isIP('255.255.255.255') == True
    assert myutils.isIP('255.255.255.256') == False
def test_answerstring():
    assert myutils.isIP('asd') == False
def test_answerint():
    assert myutils.isIP(2) == False
def test_DNSlookup():
    hostname,result, ip_address = myutils.resolve_dns('test.huehue.nl') 
    assert ip_address == '1.1.1.1'
