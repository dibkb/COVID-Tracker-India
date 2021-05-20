import requests
from datetime import datetime


class stateData():
    def __init__(self):
        self.url = 'https://api.rootnet.in/covid19-in/stats/lates'
        self.json = requests.get(self.url).json()

#         Time Details

    def getTimeObject(self):
        updateObject = self.json['lastOriginUpdate']
        updateObject = datetime.fromisoformat(updateObject[:-1])
        updateObject.strftime('%Y-%m-%d %H:%M:%S')
        return updateObject
    def getUpdateTime(self):
        updateTime = self.getTimeObject().strftime('%I:%M %p')
        return updateTime
    def getUpdateDate(self):
        updateDate= self.getTimeObject().strftime('%d %b %Y')
        return updateDate
    
#     Total Indian Stats

    def totalDataObject(self):
        dataObject = self.json['data']['summary']
        return dataObject
    def totalIndianCases(self):
        casesIndian = str(self.totalDataObject()['confirmedCasesIndian'])[:3]
        return float(casesIndian[:2] + "." + casesIndian[1:])
    def totalIndianDeaths(self):
        deathsIndian = str(self.totalDataObject()['deaths'])[:3]
        return int(deathsIndian)
    def totalIndianRecovered(self):
        casesIndian = str(self.totalDataObject()['discharged'])[:3]
        return float(casesIndian[:2] + "." + casesIndian[1:])

#     State Details
    def getStatesData(self):
        states = self.json['data']['regional']
        sortedStates = sorted(states,key=lambda i: (i['totalConfirmed'], i['confirmedCasesIndian'], 
                    i['confirmedCasesForeign'], i['deaths'], i['deaths'], i['loc']))[::-1]
        return sortedStates  

    def getFinalStatesData(self):
        import locale
        locale.setlocale(locale.LC_ALL, 'en_IN')
        locale.format_string("%d", 1255000, grouping=True)
        states =  self.getStatesData()
        for state in states:
            state['active'] =   state['totalConfirmed'] -(state['discharged'] + state['deaths'])
            state['deathRatio'] = round((state['deaths'] / state['totalConfirmed'])*100,2)
            
#     convert to indian value system 

            state['totalConfirmed'] =  locale.format_string("%d", state['totalConfirmed'], grouping=True)
            state['discharged'] =  locale.format_string("%d", state['discharged'], grouping=True)
            state['deaths'] =  locale.format_string("%d", state['deaths'], grouping=True) 
            state['active'] = locale.format_string("%d", state['active'], grouping=True)
        return states  
                
class districtData():
    
    def __init__(self,district):
        self.url = 'https://api.covid19india.org/state_district_wise.json'
        self.json = requests.get(self.url).json()
        self.district = district
        
#   Get District Data

    def getDistrict(self):
        for state in self.json:
            for district in self.json[state]['districtData']:
                if district == self.district:
                    dist_data = self.json[state]['districtData'][self.district]
                    state_name = state
 
        return dist_data,state_name
    def getStateData(self,state_name):
        for state in self.json:
            if state == state_name:
                return self.json[state]['districtData']
        
    
#   Get District Stats

    def totalDistrictCases(self):
        return self.getDistrict()[0]['confirmed']
    def totalDistrictActive(self):
        return self.getDistrict()[0]['active']
    def totalDistrictrecovered(self):
        return self.getDistrict()[0]['recovered']
    def totalDistrictDeaths(self):
        return self.getDistrict()[0]['deceased']

# District data of State

class districtDataState():
    
    def __init__(self,state):
        self.url = 'https://api.covid19india.org/state_district_wise.json'
        self.json = requests.get(self.url).json()
        self.state = state
        
    def getStateData(self):       
        return self.json[self.state]['districtData']

# class allData():
#     def __init__(self):
#         self.url = 'https://api.covid19india.org/state_district_wise.json'
#         self.json = requests.get(self.url).json()
    
#     def getAllDistrictData(self):       
#          return self.json

        

