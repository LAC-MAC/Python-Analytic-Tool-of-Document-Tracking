import re
import numpy as np
import pandas as pd

class Browsers:

    def __init__(self):
        self.chrome = "^*(Chrome\/)(([0-9]+\.*)+)( Safari\/)(([0-9]+\.*)+).*"
        self.safari = "^(?!.*(?:Chrome|Edge)).*Safari\/([0-9]+\.*)+"
        self.opera = ".*(?:Chrome).*(OPR)\/([0-9]+\.*)+"
        self.edge = "^.*((Edge.*)\/([0-9]+\.*)+|(Edg.*)\/([0-9]+\.*)+)"
        self.firefox = "^.*(Firefox\/)(([0-9]+\.*)+)"


    def setBrowsers(self, data):
        # get country attribute
        userAgentStrings = data["visitor_useragent"]
        # turn it an array
        arrUAS = userAgentStrings.to_numpy()

        df = pd.DataFrame()

        opera = 0
        edge = 0
        safari = 0
        firefox = 0
        dalvik = 0
        chrome = 0
        for i in arrUAS:
            if re.search("(?=.*Chrome/)(?=.*Safari/)(?=.*OPR/)", i) or re.search("(Opera)", i):
                opera = opera + 1
            elif re.search("(?=.*Chrome/)(?=.*Safari/)(?=.*Edg/)", i):
                edge = edge + 1
            elif re.search("(?=.*AppleWebKit/)(?=.*Chrome/)(?=.*Safari/)", i):
                chrome = chrome + 1
            elif re.search("(?=.*AppleWebKit/)(?=.*Safari/)", i):
                safari = safari +1
            elif re.search("(?=.*Firefox/)", i):
                firefox = firefox + 1
            elif re.search("(Dalvik/)", i):
                dalvik = dalvik + 1

        data = {'Occurences':[opera,chrome, safari, firefox, edge, dalvik]}
        df = pd.DataFrame(data, index =['Opera','Chrome','Safari','Firefox','Edge', 'Dalvik'] )
        return df
      



