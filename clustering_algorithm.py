################################################################################
# Usage: python clustering_algorithm.py 3 10 simple_data.txt clusters.txt      #
#   where   k = 3 (number of clusters)                                         #
#           max_iter = 10 (maximum iterations)                                 #
#           'simple_data.txt' is the tab-delimited data file to be worked with #
#           'clusters.txt' is the file to be created with cluster information  #
################################################################################


import sys
import random
import math


#################################
# Main Class, Business Domain   #
#################################

class Clusters:
    #########################################################
    # Initialize class variables                            #
    #   how to send over command line args????????????????  #
    #########################################################
    def __init__(self, arr):
        self.args = []
        # self.k = int(sys.argv[1])  # Number of clusters
        self.k = int(arr[0])
        # self.max_iter = int(sys.argv[2])  # Maximum times the program should loop through before giving up
        self.max_iter = int(arr[1])
        # self.points_file_handle = open(sys.argv[3], "r")  # Opens dataset for reading
        self.points_file_handle = open(arr[2], "r")
        # self.outfile_handle = open(sys.argv[4], "w")  # Creates and opens a text file for writing
        self.outfile_handle = open(arr[3], "w")
        self.write_to_outfile()
        self.x_coordinates = []
        self.y_coordinates = []
        self.center_id = []
        self.x_center = []
        self.y_center = []
        # Gonna write a function that will compare the two for me...
        self.closest_point = []
        self.new_closest_point = []
        self.fill_x_y_coordinate_lists()
        self.x_min, self.x_max, self.y_min, self.y_max = self.get_ranges()
        self.check = False
        self.validate_and_go()
        self.new_center_id = []
        self.new_x_center = []
        self.new_y_center = []

    #################################################
    # Write to outfile                              #
    #   may be able to make this more streamlined?  #
    #################################################
    def write_to_outfile(self):
        self.outfile_handle.write("X\tY\tCluster\n")  # Make a header for the outfile

    #################################################
    # Calculate the closest points to each cluster  #
    #################################################
    def calc_closest_points(self):
        # closest_point = []
        for i in range(0, len(self.x_coordinates)):
            closest_distance = 1000000000
            for center in range(0, len(self.center_id)):
                # distance = sqrt((x-x)^2 + (y-y)^2)
                distance = math.sqrt(
                    ((self.x_coordinates[i] - self.x_center[center]) ** 2) + ((self.y_coordinates[i] - self.y_center[center]) ** 2))
                if (distance < closest_distance):
                    closest_distance = distance
                    closest_center = center + 1
            self.closest_point.append(closest_center)
        return self.closest_point

    def new_calc_closest_points(self):
        # closest_point = []
        for i in range(0, len(self.x_coordinates)):
            closest_distance = 1000000000
            for center in range(0, len(self.center_id)):
                # distance = sqrt((x-x)^2 + (y-y)^2)
                distance = math.sqrt(
                    ((self.x_coordinates[i] - self.x_center[center]) ** 2) + ((self.y_coordinates[i] - self.y_center[center]) ** 2))
                if (distance < closest_distance):
                    closest_distance = distance
                    closest_center = center + 1
            self.new_closest_point.append(closest_center)
        # return self.closest_point

    #############################################
    # Get randomly generated starting points    #
    #   make a utility function???              #
    #############################################
    def random_starting_points(self):
        # center_id = []
        # x_center = []
        # y_center = []
        for i in range(0, self.k):
            x = random.uniform(self.x_min, self.x_max)
            y = random.uniform(self.y_min, self.y_max)
            self.center_id.append(i + 1)
            self.x_center.append(x)
            self.y_center.append(y)
        # return center_id, x_center, y_center

    ###############################
    # Fill x, y coordinate arrays #
    ###############################
    def fill_x_y_coordinate_lists(self):
        # self.x_coordinates = []
        # self.y_coordinates = []
        for rawline in self.points_file_handle:
            line = rawline.rstrip()
            x_value, y_value = line.split("\t")
            self.x_coordinates.append(float(x_value))
            self.y_coordinates.append(float(y_value))

    ########################################################
    # Get min and max values from x and y coordinate lists #
    #   make a utility function????                        #
    ########################################################
    def get_ranges(self):
        self.x_min = self.x_coordinates[0]
        self.x_max = self.x_coordinates[0]
        self.y_min = self.y_coordinates[0]
        self.y_max = self.y_coordinates[0]
        for i in range(0, len(self.x_coordinates)):
            if self.x_min > self.x_coordinates[i]:
                self.x_min = self.x_coordinates[i]
            if self.x_max < self.x_coordinates[i]:
                self.x_max = self.x_coordinates[i]
        for i in range(0, len(self.y_coordinates)):
            if self.y_min > self.y_coordinates[i]:
                self.y_min = self.y_coordinates[i]
            if self.y_max < self.y_coordinates[i]:
                self.y_max = self.y_coordinates[i]
        return self.x_min, self.x_max, self.y_min, self.y_max

    #################
    # Run this shit #
    #################
    def validate_and_go(self):
        while (self.check == False):
            self.random_starting_points()
            self.calc_closest_points()
            self.divide_by_zero()

    #####################################################
    # Check if points have associated cluster, I think? #
    #####################################################
    def divide_by_zero(self):
        # check = True
        total = 0
        for i in range(0, self.k):
            for x in range(0, len(self.closest_point)):
                if (self.closest_point[x] == i + 1):
                    total = total + 1
            if (total == 0):
                self.check = False
                break                           ######### WILL THIS BE AN ISSUE????
        self.check = True

    ###################################################################
    # Find average of points in a cluster and find new cluster center #
    ###################################################################
    def recalculate_cluster_center(self):
        for i in range(0, self.k):
            total = 0
            sum_of_x = 0
            sum_of_y = 0
            for x in range(0, len(self.x_coordinates)):
                if (self.closest_point[x] == i + 1):
                    total = total + 1
                    sum_of_x = sum_of_x + self.x_coordinates[x]
                    sum_of_y = sum_of_y + self.y_coordinates[x]
            if (total == 0):
                print("Please re-run program; clusters have been encountered with 0 associated points.")
                print(len(self.center_id))
                quit()
            avg_x = sum_of_x / total
            avg_y = sum_of_y / total
            self.new_x_center.append(avg_x)
            self.new_y_center.append(avg_y)
            self.new_center_id.append(i+1)

    def compare(self):
        self.new_calc_closest_points()
        comparisons = 1
        if (self.closest_point == self.new_closest_point):
            for item in range(0, len(self.closest_point)):
                self.outfile_handle.write(
                    f"{self.x_coordinates[item]}\t{self.y_coordinates[item]}\t{self.closest_point[item]}\n")
        # If not, repeat recalculation of centers and reassignation of points until lists are the same twice in a row, or we run out of iterations
        else:
            while (self.closest_point != self.new_closest_point):
                if (comparisons < self.max_iter):
                    self.closest_point = self.new_closest_point
                    # new_center_id, new_x_center, new_y_center = recalculate_cluster_center(k, x_coordinates, y_coordinates, closest_point, center_id)
                    self.recalculate_cluster_center()
                    # new_closest_point = calc_closest_points(x_coordinates, y_coordinates, new_x_center, new_y_center, new_center_id)
                    self.new_calc_closest_points()
                    comparisons = comparisons + 1
                    if (self.closest_point == self.new_closest_point):
                        for item in range(0, len(self.closest_point)):
                            self.outfile_handle.write(
                                f"{self.x_coordinates[item]}\t{self.y_coordinates[item]}\t{self.closest_point[item]}\n")
                else:
                    for item in range(0, len(self.new_closest_point)):
                        self.outfile_handle.write(
                            f"{self.x_coordinates[item]}\t{self.y_coordinates[item]}\t{self.new_closest_point[item]}\n")
                    print("The maximum number of iterations has been reached without convergence.")
                    break

























#################################################
# Function: get_ranges()                        #
# Description: Find mins and maxes in data set  #
# Parameters: x_coordinates[], y_coordinates[]  #
# Returns: x_min, x_max, y_min, y_max           #
#################################################
# utility
# def get_ranges(x_coordinates, y_coordinates):
#   x_min = x_coordinates[0]
#   x_max = x_coordinates[0]
#   y_min = y_coordinates[0]
#   y_max = y_coordinates[0]
#   for i in range(0, len(x_coordinates)):
#       if x_min > x_coordinates[i]:
#           x_min = x_coordinates[i]
#       if x_max < x_coordinates[i]:
#           x_max = x_coordinates[i]
#   for i in range(0, len(y_coordinates)):
#       if y_min > y_coordinates[i]:
#           y_min = y_coordinates[i]
#       if y_max < y_coordinates[i]:
#           y_max = y_coordinates[i]
#   return x_min, x_max, y_min, y_max

# get points from starting set using min and max x and y values?
# business domain
def get_starting_points(k, x_coordinates, y_coordinates):
    # for each point, measure the distance to every other point
    avg_dist_list = []
    for j in range(0, len(x_coordinates)):
        total_distance = 0
        # compare one point to every other point
        for i in range(0, len(x_coordinates)):
            distance = math.sqrt(((x_coordinates[j] - x_coordinates[i]) ** 2) + ((y_coordinates[j] - y_coordinates[i]) ** 2))
            total_distance = total_distance + distance
        avg_distance = total_distance / len(x_coordinates)
        avg_dist_list.append(avg_distance)
    # avg_dist_list now contains, in order, the average distance of each point to every other point

    # make a list of starter points and add in the points furthest away from all the others
    start_pts_x = []
    start_pts_y = []
    temp_distance = avg_dist_list[0]
    # temp_index = 0
    used_indices = []
    start_id = []
    for j in range(0, k):
        start_id.append(j+1)
        for i in range(0, len(avg_dist_list)):
            if ((temp_distance < avg_dist_list[i]) and (i not in used_indices)):
                temp_distance = avg_dist_list[i]
                temp_index = i
        start_pts_x.append(x_coordinates[temp_index])
        start_pts_y.append(y_coordinates[temp_index])
        used_indices.append(temp_index)
    # should end up with two lists of length k of x and y coordinates of the furthest out points in the dataset

    return start_id, start_pts_x, start_pts_y





#############################################################################################################
# Function: starting_points()                                                                               #
# Description: Gets k-number of random points for initial cluster centers using random number generator.    #
# Parameters: k, x_min, x_max, y_min, y_max                                                                 #
# Returns: center_id[], x_center[], y_center[]                                                              #
#############################################################################################################
# utility
# def starting_points(k, x_min, x_max, y_min, y_max):
#   center_id = []
#   x_center = []
#   y_center = []
#   for i in range(0, k):
#       x = random.uniform(x_min, x_max)
#       y = random.uniform(y_min, y_max)
#       center_id.append(i+1)
#       x_center.append(x)
#       y_center.append(y)
#   return center_id, x_center, y_center


#####################################################################################
# Function: calc_closest_points()                                                   #
# Description: Assigns all points to the nearest cluster centers                    #
# Parameters: x_coordinates[], y_coordinates[], x_center[], y_center[], center_id[] #
# Returns: closest_point[]                                                          #
#####################################################################################
# business domain
# def calc_closest_points(x_coordinates, y_coordinates, x_center, y_center, center_id):
#   closest_point = []
#   for i in range(0, len(x_coordinates)):
#       closest_distance = 1000000000
#       for center in range(0, len(center_id)):
#           distance = sqrt((x-x)^2 + (y-y)^2)
#           distance = math.sqrt(((x_coordinates[i] - x_center[center]) ** 2) + ((y_coordinates[i] - y_center[center]) ** 2))
#           if (distance < closest_distance):
#               closest_distance = distance
#               closest_center = center + 1
#       closest_point.append(closest_center)
#   return closest_point


#################################################################################################################################################
# Function: divide_by_zero()                                                                                                                    #
# Description: Reroll for random cluster centers and recalculate closest points if there is a center that does not have points assigned to it   #
# Parameters: k, closest_point[]                                                                                                                #
# Returns: check (bool)                                                                                                                         #
#################################################################################################################################################
# utility
# def divide_by_zero(k, closest_point):
#   check = True
#   total = 0
#   for i in range(0, k):
#       for x in range(0, len(closest_point)):
#           if (closest_point[x] == i + 1):
#               total = total + 1
#       if (total == 0):
#           check = False
#           break
#   return check


#################################################################################
# Function: recalculate cluster center()                                        #
# Description: Fine average of points in a cluster and find new cluster center  #
# Parameters: k, x_coordinates[], y_coordinates[], closest_point[]              #
# Returns: new_center_id[], new_x_center[], new_y_center[]                      #
#################################################################################
# business domain
# def recalculate_cluster_center(k, x_coordinates, y_coordinates, closest_point, center_id):
#   new_center_id = []
#   new_x_center = []
#   new_y_center = []
#   for i in range(0, k):
#       total = 0
#       sum_of_x = 0
#       sum_of_y = 0
#       for x in range(0, len(x_coordinates)):
#           if (closest_point[x] == i + 1):
#               total = total + 1
#               sum_of_x = sum_of_x + x_coordinates[x]
#               sum_of_y = sum_of_y + y_coordinates[x]
#       if (total == 0):
#           print("Please re-run program; clusters have been encountered with 0 associated points.")
#           print(len(center_id))
#           quit()
#       avg_x = sum_of_x / total
#       avg_y = sum_of_y / total
#       new_x_center.append(avg_x)
#       new_y_center.append(avg_y)
#       new_center_id.append(i+1)
#   return new_center_id, new_x_center, new_y_center


 
# Assign command line arguments to variables in program
# sys.argv[] = k clusters, max iterations, input file name, output file name
def main():
    # k = int(sys.argv[1])                          # Number of clusters
    # max_iter = int(sys.argv[2])                   # Maximum times the program should loop through before giving up
    # points_file_handle = open(sys.argv[3], "r")   # Opens dataset for reading
    # outfile_handle = open(sys.argv[4], "w")       # Creates and opens a text file for writing
    # outfile_handle.write("X\tY\tCluster\n")       # Make a header for the outfile



    # NEW WITH CLASSES
    # arr = sys.argv[1:]
    myclusters = Clusters(sys.argv[1:])
    myclusters.compare()
    # END NEW



    # Read (x, y) coordinates from file and store as lists
    # MAKE A SEPARATE FUNCTION
    # x_coordinates = []
    # y_coordinates = []
    # for rawline in points_file_handle:
    #   line = rawline.rstrip()
    #   x_value, y_value = line.split("\t")
    #   x_coordinates.append(float(x_value))
    #   y_coordinates.append(float(y_value))


    # Find min and max range of datapoints
    # MAKE A SEPARATE FUNCION MAYBE?
    # x_min, x_max, y_min, y_max = get_ranges(x_coordinates, y_coordinates)
    # Generate random starter cluster centers
    # center_id, x_center, y_center = starting_points(k, x_min, x_max, y_min, y_max)
    # center_id, x_center, y_center = get_starting_points(k, x_coordinates, y_coordinates)
    # Assign datapoints to nearest random cluster centers
    # closest_point = calc_closest_points(x_coordinates, y_coordinates, x_center, y_center, center_id)
    # Check to see if all the cluster centers have datapoints assigned to them
    # check = divide_by_zero(k, closest_point)

    # To avoid a situation where some of the initial points are not useable, recalculate if there are centers with no points
    # MAKE A SEPARATE FUNCION MAYBE?
    # while (check == False):
    #   center_id, x_center, y_center = starting_points(k, x_min, x_max, y_min, y_max)
    #   center_id, x_center, y_center = get_starting_points(k, x_coordinates, y_coordinates)
    #   closest_point = calc_closest_points(x_coordinates, y_coordinates, x_center, y_center, center_id)
    #   check = divide_by_zero(k, closest_point)

    # Calculate a new cluster center from the points in their clusters
    # MAKE A SEPARATE FUNCION MAYBE?
    # new_center_id, new_x_center, new_y_center = recalculate_cluster_center(k, x_coordinates, y_coordinates, closest_point, center_id)
    # Reassign datapoints to new cluster centers
    # new_closest_point = calc_closest_points(x_coordinates, y_coordinates, new_x_center, new_y_center, new_center_id)



    # NEW WITH CLASSES
#   closest_point = newcluster.calc_closest_points()        # original closest points
#   newcluster.recalculate_cluster_center()                 # recalc cluster centers
#   new_closest_point = newcluster.calc_closest_points()    # new closest points
    # END NEW


    # May make the last bit classy too? unsure but this seemed to work ok


#   # If the lists of cluster center assignations are the same, we're done!
#   # MAKE A SEPARATE FUNCION MAYBE?
#   comparisons = 1
#   if (closest_point == new_closest_point):
#       for item in range(0, len(closest_point)):
#           newcluster.outfile_handle.write(f"{newcluster.x_coordinates[item]}\t{newcluster.y_coordinates[item]}\t{closest_point[item]}\n")
#   # If not, repeat recalculation of centers and reassignation of points until lists are the same twice in a row, or we run out of iterations
#   else:
#       while (closest_point != new_closest_point):
#           if (comparisons < newcluster.max_iter):
#               closest_point = new_closest_point
#               # new_center_id, new_x_center, new_y_center = recalculate_cluster_center(k, x_coordinates, y_coordinates, closest_point, center_id)
#               newcluster.recalculate_cluster_center()
#               # new_closest_point = calc_closest_points(x_coordinates, y_coordinates, new_x_center, new_y_center, new_center_id)
#               new_closest_point = newcluster.calc_closest_points()
#               comparisons = comparisons + 1
#                if (closest_point == new_closest_point):
#                    for item in range(0, len(closest_point)):
#                       newcluster.outfile_handle.write(f"{newcluster.x_coordinates[item]}\t{newcluster.y_coordinates[item]}\t{closest_point[item]}\n")
#            else:
#                for item in range(0, len(new_closest_point)):
#                    newcluster.outfile_handle.write(f"{newcluster.x_coordinates[item]}\t{newcluster.y_coordinates[item]}\t{new_closest_point[item]}\n")
#                print("The maximum number of iterations has been reached without convergence.")
#                break


main()
