import hashTable
import Package


# O(n^2)

# O(n^2)
# because the distance and location data is uniform(distance is correct both ways), fill the missing dat by the inverse of the data based on location
def fill_distance_list(d_list):
    for row_index, row in enumerate(d_list):
        for col_index, element in enumerate(row):
            if element != '':
                d_list[row_index][col_index] = float(d_list[row_index][col_index])
            if element == '':
                d_list[row_index][col_index] = float(d_list[col_index][row_index])
    return d_list


# O(n log n)
# this sorts the distances for/from each location from shortest to furthest away location
def sort_distances(d_list):
    for index, dict_elem in enumerate(d_list):
        d_list[index] = dict(sorted(dict_elem.items(), key=lambda curr: curr[1]))
    return d_list


# O(n)
# change 2 list to 1 dict and structuring the data in such a way that data from the data from one list is the value and data from the other list is the key
def change_from_list_to_dict(d_list, locations):
    for row_index, row in enumerate(d_list):
        ite = iter(row)
        ite2 = iter(locations)
        res_dict = dict(zip(ite2, ite))
        d_list[row_index] = res_dict
    return d_list


# Data class, handles(along with helper methods) data extraction, transformation, and loading
class Data:
    pac_index = 0
    dis_index = 0
    loc_index = 0
    add_dis_loc_index = 0
    add_dis = 0
    locations = []
    distances = {}
    packages = hashTable.HashTable(40)
    iterator = iter(locations)
    iterator2 = iter(packages)
    list_of_distances = [[]]

    # O(n)
    # opens a file and loads the data into a data structure
    with open('Resources/location_list.txt', 'r') as location_list:
        location_data = location_list.readlines()
    for line in location_data:
        locations.append(line.replace(',\n', ''))
    loc_index += 1

    # O(n)
    # opens a file and loads the data into a data structure
    with open('Resources/deliver_distances.txt', 'r') as distance_list:
        distance_data = distance_list.readlines()
    for line in distance_data:
        list_of_distances.insert(dis_index, line.replace('\n', '').split(','))
        dis_index += 1

    for line in distance_data:
        distances[locations[add_dis_loc_index]] = line.replace('\n', '')
        add_dis_loc_index += 1

    # O(n^2)
    # opens a file and loads the data into a data structure
    with open('Resources/package_information.txt', 'r') as package_list:
        header = package_list.readline()
        package_data = package_list.readlines()
    for line in package_data:
        line_list = line.replace('\n', '').split(',')
        if len(line_list) > 9:
            line_list[7:-1] = [','.join(line_list[7:-1])]
        index_of_location = 0

        for index, loc in enumerate(locations):
            if loc.__contains__(line_list[1]):
                index_of_location = index

        # create new package object from the ingested data and insert package obj into hash table data structure
        new_package = Package.Package(line_list[0], line_list[1], line_list[2], line_list[3], line_list[4],
                                      line_list[5], line_list[6], line_list[7], locations[index_of_location])
        packages.insert(int(line_list[0]), new_package)
        pac_index += 1

    list_of_distances = fill_distance_list(list_of_distances)
    list_of_distances = change_from_list_to_dict(list_of_distances, locations)
    list_of_distances = sort_distances(list_of_distances)
    list_of_distances.pop(len(list_of_distances) - 1)

    # O(n)
    # merging list of locations into an already existing dict
    for k, v in distances.items():
        distances[k] = list_of_distances[add_dis]
        add_dis += 1
