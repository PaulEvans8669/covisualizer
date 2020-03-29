class Country:
    maxCases = 0
    maxDeaths = 0

    def __init__(self, json_data):
        name = json_data['country']
        province = json_data['province']
        self.__prepare(name, province)

        cases = json_data['timeline']['cases']
        for c in cases:
            val = cases[c]
            if val == 0:
                val = -1
            self.addCase(c, val)
            Country.maxCases = max(Country.maxCases, val)

        deaths = json_data['timeline']['deaths']
        for d in deaths:
            val = cases[d]
            if val == 0:
                val = -1
            self.addDeath(d, val)
            Country.maxDeaths = max(Country.maxDeaths, val)

        self.lat = 0
        self.lon = 0

    def __prepare(self, name, province):
        self.name = name
        self.province = province
        self.cases = dict()
        self.deaths = dict()

    def addCase(self, date, val):
        self.cases[date] = val

    def addDeath(self, date, val):
        self.deaths[date] = val
