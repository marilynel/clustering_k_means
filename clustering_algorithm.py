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
    def __init__(self):
        self.x_coordinates = []
        self.y_coordinates = []
        self.center_id = []
        self.x_center = []
        self.y_center = []
        self.closest_point = []
        self.new_closest_point = []
        self.check = False
        self.new_center_id = []
        self.new_x_center = []
        self.new_y_center = []

    ################################
    # initialize values with input #
    ################################
    def read_input(self, argv):
        self.k = int(argv[0])
        self.max_iter = int(argv[1])
        self.points_file_handle = open(argv[2], "r")
        self.outfile_handle = open(argv[3], "w")
        self.header_to_outfile()
        self.fill_x_y_coordinate_lists()
        # self.x_min, self.x_max, self.y_min, self.y_max = self.get_ranges()
        self.validate_and_go()

    #################################################
    # Write to outfile                              #
    #   may be able to make this more streamlined?  #
    #################################################
    def header_to_outfile(self):
        self.outfile_handle.write("X\tY\tCluster\n")  # Make a header for the outfile

    #################################################
    # Calculate the closest points to each cluster  #
    #################################################
    def calc_closest_points(self):
        for i in range(0, len(self.x_coordinates)):
            closest_distance = 1000000000
            closest_center = 0
            for center in range(0, len(self.center_id)):
                distance = math.sqrt(
                    ((self.x_coordinates[i] - self.x_center[center]) ** 2) + ((self.y_coordinates[i] - self.y_center[center]) ** 2))
                if (distance < closest_distance):
                    closest_distance = distance
                    closest_center = center + 1
            self.closest_point.append(closest_center)

    def new_calc_closest_points(self):
        self.new_closest_point = []
        for i in range(0, len(self.x_coordinates)):
            closest_distance = 1000000000
            closest_center = 0
            for center in range(0, len(self.center_id)):
                # distance = sqrt((x-x)^2 + (y-y)^2)
                distance = math.sqrt(
                    ((self.x_coordinates[i] - self.x_center[center]) ** 2) + ((self.y_coordinates[i] - self.y_center[center]) ** 2))
                if (distance < closest_distance):
                    closest_distance = distance
                    closest_center = center + 1
            self.new_closest_point.append(closest_center)

    #############################################
    # Get randomly generated starting points    #
    #   make a utility function???              #
    #############################################
    def random_starting_points(self):
        for i in range(0, self.k):
            x = random.uniform(self.x_min, self.x_max)
            y = random.uniform(self.y_min, self.y_max)
            self.center_id.append(i + 1)
            self.x_center.append(x)
            self.y_center.append(y)

    ###############################
    # Fill x, y coordinate arrays #
    ###############################
    def fill_x_y_coordinate_lists(self):
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
            # self.random_starting_points()
            self.get_starting_points()
            self.calc_closest_points()
            self.divide_by_zero()

    #####################################################
    # Check if points have associated cluster, I think? #
    #####################################################
    def divide_by_zero(self):
        for i in range(0, self.k):
            total = 0
            for x in range(0, len(self.closest_point)):             # [1,1,3,2,3,3,1,2,3,3,2,3]
                if (self.closest_point[x] == i + 1):
                    total = total + 1
            if (total == 0):
                self.check = False
                break
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
                print(self.center_id)
                print(self.closest_point)
                print("Please re-run program; clusters have been encountered with 0 associated points.")
                quit()
            avg_x = sum_of_x / total
            avg_y = sum_of_y / total
            self.new_x_center.append(avg_x)
            self.new_y_center.append(avg_y)
            self.new_y_center.append(avg_y)
            self.new_center_id.append(i+1)

    def compare(self):
        self.recalculate_cluster_center()
        self.new_calc_closest_points()
        comparisons = 1
        if (self.closest_point == self.new_closest_point):
            self.write_to_file()
        else:
            while (self.closest_point != self.new_closest_point):
                if (comparisons < self.max_iter):
                    self.not_converged_action()
                    comparisons = comparisons + 1
                else:
                    self.write_to_file()
                    print("The maximum number of iterations has been reached without convergence.")
                    break

    def not_converged_action(self):
        self.closest_point = self.new_closest_point
        self.x_center = self.new_x_center
        self.y_center = self.new_y_center
        self.new_x_center = []
        self.new_y_center = []
        self.recalculate_cluster_center()
        self.new_calc_closest_points()
        if (self.closest_point == self.new_closest_point):
            self.write_to_file()

    ######################################################
    # Write points and associated cluster center to file #
    ######################################################
    def write_to_file(self):
        for item in range(0, len(self.x_center)):
            self.outfile_handle.write(f"Cluster {item} coordinates: {self.new_x_center[item]}, {self.new_y_center[item]}\n")
        for item in range(0, len(self.closest_point)):
            self.outfile_handle.write(
                f"{self.x_coordinates[item]}\t{self.y_coordinates[item]}\t{self.closest_point[item]}\n")

# get points from starting set using min and max x and y values?
# business domain
    def get_starting_points(self):
        self.x_center.append(self.x_coordinates[0])
        self.y_center.append(self.y_coordinates[0])
        remaining_x = self.x_coordinates.copy()
        remaining_y = self.y_coordinates.copy()
        remaining_x.remove(self.x_coordinates[0])
        remaining_y.remove(self.y_coordinates[0])

        for i in range(self.k-1):
            distances = []
            for j in range(len(remaining_x)):
                distance = math.sqrt(((remaining_x[j] - self.x_center[0]) ** 2) + ((remaining_y[j] - self.y_center[0]) ** 2))
                for l in range(len(self.x_center)):
                    next_distance = math.sqrt(((remaining_x[j] - self.x_center[l]) ** 2) + ((remaining_y[j] - self.y_center[l]) **2))
                    distance = min(distance, next_distance)
                distances.append(distance)

            # find the largest of those minimum distances
            a = 0
            min_distance = distances[0]
            for j in range(len(distances)):
                if (distances[j] > min_distance):
                    a = j
                    min_distance = distances[j]
            # self.init_centers.append((remaining_x[a], remaining_y[a]))
            self.x_center.append(remaining_x[a])
            self.y_center.append(remaining_y[a])
            remaining_x.remove(remaining_x[a])
            remaining_y.remove(remaining_y[a])
        for i in range(self.k):
            self.center_id.append(i+1)
        # print(self.x_center)
        # print(self.y_center)












def main():

    myclusters = Clusters()
    myclusters.read_input(sys.argv[1:])
    myclusters.compare()

    # and this
    # myclusters.write_output()

main()
