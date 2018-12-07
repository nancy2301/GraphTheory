import pandas as pd
import copy


class travelPath(object):

    def __init__(self):
        self.route_info = self.getRouteInfo()
        self.OregonPorts = ["PDX", "RDM", "EUG", "MFR"]
        self.MontanaPorts = ["BIL", "BZN", "GTF", "FCA", "MSO", "HLN"]
        self.FinalPath = []
        self.minimum = float('inf')
        self.maximum = 0
        self.maximum_network_length = 0

    def getRouteInfo(self):
        flights = pd.read_csv(
            '/Users/nancyjain/Documents/nancy/SeattleUniversity/1/DiscreetMathematics/project/December 2017 Flights.csv',
            sep=',')
        flights1 = flights[flights['DISTANCE_GROUP'] < 8]
        flights2 = flights1[['ORIGIN', 'DEST', 'DISTANCE_GROUP', 'DISTANCE']]
        flights3 = flights2.drop_duplicates()

        dict = {}
        count = 0
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

            if destinationInfo.DEST in destinationPort:
                temp = (source, destinationInfo.DEST)
                existing_Path.append(temp)
                self.FinalPath.append(copy.deepcopy(existing_Path))
                self.maximum = max(self.maximum, totalDistance)
                self.minimum = min(self.minimum, totalDistance)
                self.maximum_network_length = max(self.maximum_network_length, len(existing_Path))
                existing_Path.pop()
                continue

            current_DG = current_DG + destinationInfo.DISTANCE_GROUP
            totalDistance = totalDistance + destinationInfo.DISTANCE
            existing_Path.append((source, destinationInfo.DEST))
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

    for list in path.FinalPath:
        print (list)


def main2():
    path = travelPath()
    path.get_info_for_source("MFR", ["MSO"])
    print (path.FinalPath)
    print (path.minimum)
    print (path.maximum)
    network = []
    for i in range(0, len(path.FinalPath)):
        if path.maximum_network_length == len(path.FinalPath[i]):
            network.append(path.FinalPath[i])
    print (network)

main1()
#main2()