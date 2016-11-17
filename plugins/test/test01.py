

def test():
    
    t = (0, 255, 0)
    l = [0, 255, 0]
    assert tuple(l) == t
    assert list(t) == l