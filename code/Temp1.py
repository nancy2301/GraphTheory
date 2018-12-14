import pandas as pd
import copy


class travelPath(object):

    def __init__(self):
        # initialize variables to store paths, their distance and distance group
        self.route_info = self.getRouteInfo()
        self.OregonPorts = ["PDX", "RDM", "EUG", "MFR"]
        self.MontanaPorts = ["BIL", "BZN", "GTF", "FCA", "MSO", "HLN"]
        self.FinalPath = []
        self.distanceGroup = []
        self.distance = []

    def getRouteInfo(self):
        # read December 2017 Flights csv and store them in Pandas data frame flights
        flights = pd.read_csv('../raw_data/December 2017 Flights.csv',sep=',')

        # filter the data by [DistanceGroup < 8] and name it as flights1 data frame
        flights1 = flights[flights['DISTANCE_GROUP'] < 8]

        # select data from Origin, Dest, Distance_Group, Distance columns and store it in flights2 data frame
        flights2 = flights1[['ORIGIN', 'DEST', 'DISTANCE_GROUP', 'DISTANCE']]

        # drop duplicates from flights2 data frame and store it in flights3 data frame
        flights3 = flights2.drop_duplicates()

        # store the data in a dictionary with Origin as keys and Dest, Distance_Group and Distance as its values
        # storing the data in a dictionary will enable the retrieval of the elements of a dictionary by its key
        # time complexity of the retrieval will be O(1)
        dict = {}
        for origin in flights3['ORIGIN'].values.tolist():
            if origin in dict:
                continue
            flights4 = flights3[flights3['ORIGIN'] == origin]
            flights5 = flights4[['DEST', 'DISTANCE_GROUP', 'DISTANCE']]
            dict[origin] = list(flights5.itertuples(index=False, name='destinationInfo'))

        return dict

    # use depth - first search algorithm to find all the paths between Oregon and Montana
    def visitPort(self, source, current_DG, visited_Ports, existing_Path, destinationPort, totalDistance):

        route_list = self.route_info[source]
        for destinationInfo in route_list:
            # if destination_Group > = 8 then discard the route
            if (current_DG + destinationInfo.DISTANCE_GROUP) >= 8:
                continue

            # if DEST is in visited ports then discard the route
            if destinationInfo.DEST in visited_Ports:
                continue

            # calculate total distance of the path
            totalDistance = totalDistance + destinationInfo.DISTANCE

            # calculate total Distance_Group of the path
            current_DG = current_DG + destinationInfo.DISTANCE_GROUP

            # append the visited source and destination to existing_Path
            existing_Path.append((source, destinationInfo.DEST))

            # if DEST is in destinationPorts append the existing path to the final path
            # calculate total Distance_Group and total Distance of the path and store them
            if destinationInfo.DEST in destinationPort:
                self.FinalPath.append(copy.deepcopy(existing_Path))
                self.distanceGroup.append(current_DG)
                self.distance.append(totalDistance)

            # append ports visited to the visited_Ports
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

def getAllFlightsOregonMontana():
    path = travelPath()
    for i in range(0, len(path.OregonPorts)):
        path.get_info_for_source(path.OregonPorts[i], path.MontanaPorts)

    for i in range(0, len(path.MontanaPorts)):
        path.get_info_for_source(path.MontanaPorts[i], path.OregonPorts)

    ans = []
    for i in range(0, len(path.FinalPath)):
        ans.append([i+1, path.FinalPath[i], path.distance[i], path.distanceGroup[i]])
    all_flights = pd.DataFrame(ans, columns=['S.No','PATH','DISTANCE','DISTANCE GROUP'])
    return all_flights

def getPathsMedfordMissoula(source, destination):
    # initialize variable
    minimum = float('inf')
    shortestPath = []
    maximum = 0
    longestPath = []
    maximum_network_length = 0
    longestConnection = []
    
    # calculate and store all paths between Oregon and Montana from PART 1
    paths = getAllFlightsOregonMontana()
    ans = []
    
    # from paths find all paths from MFR to MSO
    for index, row in paths.iterrows():
        #print(row[1][-1])
        if row[1][0][0] in source :
            if row[1][-1][-1] in destination:
                # if source is MFR and destination is MSO , append it to ans
                ans.append([row[1], row[2], row[3]])
                
                # Get the maximum distance and path with maximum distance
                if row[2] > maximum:
                    longestPath = copy.deepcopy(row[1])
                    maximum = row[2]
                    
                # Get the minimum distance and path with minimum distance
                if row[2] < minimum:
                    shortestPath = copy.deepcopy(row[1])
                    minimum = row[2]
                    
                # Get the maximum network length and path with maximum network
                if len(row[1]) > maximum_network_length:
                    longestConnection = copy.deepcopy(row[1])
                    maximum_network_length = len(row[1])
    flights_M2M = pd.DataFrame(ans, columns=['PATH','DISTANCE','DISTANCE GROUP'])
    finalResult = ["All the paths between MFR and MSO are : ",flights_M2M, "Longest path is : ", longestPath, "Maximum distance is : ", maximum, "Shortest path is : ",shortestPath, "Minimum distance is : ", minimum, "Path with maximum network is : ",longestConnection, "Length of maximum network is : ",maximum_network_length]
    return finalResult

def main():
    print(getAllFlightsOregonMontana())
    for ans in getPathsMedfordMissoula("MFR", "MSO"):
       print(ans)

main()

