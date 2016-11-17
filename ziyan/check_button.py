
"""


"""


from PIL import Image


class StartButton(object):
    """ WEISS """
    
    def __init__(self, conf):
        """ init """
        self.conf = conf
        self.p1 = self.conf['p1']
        self.p2 = self.conf['p2']
        self.p3 = self.conf['p3']
        pass
        
    def check(self, fn):
        """ check running or not """

        im = Image.open(fn)
        #print im.size
        
        ### green
        rgb1 = im.getpixel(self.p1)
        
        ### white
        rgb2 = im.getpixel(self.p2)
        
        ###
        rgb3 = im.getpixel(self.p3)
        
        #assert rgb1 == self.conf['green']
        if rgb1 == self.conf['green']  and rgb3 == self.conf['p']:
            return True

        if rgb2 == self.conf['white'] and rgb3 == self.conf['p']:
            return False

        
if __name__ == '__main__':
    
    
    conf = {'p1':(39, 42), 'p2':(36, 46), 'p3':(20,11), "green":(0, 255, 0), "white":(255, 255, 255), "p":(198, 198, 198)}
    
    btn = StartButton(conf)
    
    print btn.check("1474421213.jpg")
    print btn.check("1474421223.jpg")
   