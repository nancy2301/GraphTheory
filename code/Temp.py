import pandas as pd
import copy


class travelPath(object):

    def __init__(self):
        self.route_info = self.getRouteInfo()
        self.OregonPorts = ["PDX", "RDM", "EUG", "MFR"]
        self.MontanaPorts = ["BIL", "BZN", "GTF", "FCA", "MSO", "HLN"]
        self.FinalPath = []
        self.distanceGroup = []
        self.distance = []
        self.shortestPath = []
        self.longestPath = []
        self.longestConnection = []
        self.minimum = float('inf')
        self.maximum = 0
        self.maximum_network_length = 0

    def getRouteInfo(self):
        flights = pd.read_csv('/Users/nancyjain/Documents/nancy/SeattleUniversity/1/DiscreteMathematics/project/December 2017 Flights.csv',sep=',')
        flights1 = flights[flights['DISTANCE_GROUP'] < 8]
        flights2 = flights1[['ORIGIN', 'DEST', 'DISTANCE_GROUP', 'DISTANCE']]
        flights3 = flights2.drop_duplicates()

        dict = {}
        for origin in flights3['ORIGIN'].values.tolist():
            if origin in dict:
                continue
            flights4 = flights3[flights3['ORIGIN'] == origin]
            flights5 = flights4[['DEST', 'DISTANCE_GROUP', 'DISTANCE']]
            dict[origin] = list(flights5.itertuples(index=False, name='destinationInfo'))

        return dict

    def visitPort(self, source, current_DG, visited_Ports, existing_Path, destinationPort, totalDistance):

        route_list = self.route_info[source]
        for destinationInfo in route_list:
            if (current_DG + destinationInfo.DISTANCE_GROUP) >= 8:
                continue

            if destinationInfo.DEST in visited_Ports:
                continue

            totalDistance = totalDistance + destinationInfo.DISTANCE
            current_DG = current_DG + destinationInfo.DISTANCE_GROUP
            existing_Path.append((source, destinationInfo.DEST))

            if destinationInfo.DEST in destinationPort:
                self.FinalPath.append(copy.deepcopy(existing_Path))
                self.distanceGroup.append(current_DG)
                self.distance.append(totalDistance)
                if totalDistance > self.maximum :
                    self.longestPath = copy.deepcopy(existing_Path)
                    self.maximum = totalDistance
                if totalDistance < self.minimum :
                    self.shortestPath = copy.deepcopy(existing_Path)
                    self.minimum = totalDistance
                if len(existing_Path) > self.maximum_network_length:
                    self.longestConnection = copy.deepcopy(existing_Path)
                    self.maximum_network_length = len(existing_Path)

            visited_Ports.append(destinationInfo.DEST)
            self.visitPort(destinationInfo.DEST, current_DG, visited_Ports, existing_Path,
                           destinationPort, totalDistance)
            current_DG = current_DG - destinationInfo.DISTANCE_GROUP
            totalDistance = totalDistance - destinationInfo.DISTANCE
            existing_Path.pop()
            visited_Ports.pop()

    def get_info_for_source(self, sourcePort, destinationPorts):
        visited_Ports = []
        existing_Path = []
        visited_Ports.append(sourcePort)
        self.visitPort(sourcePort, 0, visited_Ports, existing_Path, destinationPorts, 0)


def main1():
    path = travelPath()
    for i in range(0, len(path.OregonPorts)):
        path.get_info_for_source(path.OregonPorts[i], path.MontanaPorts)

    for i in range(0, len(path.MontanaPorts)):
        path.get_info_for_source(path.MontanaPorts[i], path.OregonPorts)
        
    for i in range(0, len(path.FinalPath)):
        print(i+1, path.FinalPath[i], path.distance[i], path.distanceGroup[i])



def main2():
    path = travelPath()
    path.get_info_for_source("MFR", ["MSO"])
    print(path.FinalPath)
    print(path.minimum)
    print(path.shortestPath)
    print(path.maximum)
    print(path.longestPath)
    print(path.maximum_network_length)
    print(path.longestConnection)

main1()
#main2()