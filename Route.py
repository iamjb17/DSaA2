import DeliveryInfo
import datetime
import random


# helper method that changes a list into a dict
def change_to_dict(list_to_change):
    new_dict = dict()
    for elem_index, elem in enumerate(list_to_change):
        if elem is not None and elem.getKey() not in list_to_change:
            new_dict[elem.getKey()] = elem.getValue()
    return new_dict


# calculate the distance from one location to another using the full location distance data
def get_dist_from_to(loc_dis_dict, from_here, to_there):
    dist = loc_dis_dict.get(from_here).get(to_there)
    return dist


# takes 1 location and gets the next closest location by distance using the full location distance data
def get_next_closest_loc(loc_dis_dict1, truck_load1, start_id1, visited1, switch_list):
    if switch_list[0]:
        list_to_switch_to = switch_list[1]
        for k, v in loc_dis_dict1.get(truck_load1.get(start_id1).get_distances()).items():
            if v != 0.0:
                for k1, v1 in list_to_switch_to.items():
                    if v1.get_id() not in visited1:
                        if k == v1.get_distances():
                            result = [v1.get_distances(), v1.get_id()]
                            return result
    else:
        for k, v in loc_dis_dict1.get(truck_load1.get(start_id1).get_distances()).items():
            if v != 0.0:
                for k1, v1 in truck_load1.items():
                    if v1.get_id() not in visited1:
                        if k == v1.get_distances():
                            result = [v1.get_distances(), v1.get_id()]
                            return result


# runs a look ahead function with some randomness added. returns a dict of locations and distances tested
def get_start_id_test_avg(keys, packages, loc_dis_list):
    test_list = {}
    for k in keys:
        # print('start key:',k)
        tested = []
        miles = 0.0
        tested.append(k)
        for i in range(int(len(keys))):
            choice = random.choice(keys)
            # print('to key:',choice)
            inner_test_list = []
            if choice not in tested:
                # print('miles before:', miles)
                miles = miles + get_dist_from_to(loc_dis_list, packages.get(k).get_distances(),
                                                 packages.get(choice).get_distances())
                # print('miles after:', miles)
                tested.append(choice)
            else:
                i -= 1
        tested.clear()
        test_list[k] = miles
    return test_list


# runs the route of the given trucks package data returns delivery information
def new_run_route(route, packages, curr_time, loc_dis_list, truck1, truck2, deliveries):
    global enroute, delivered
    deliveries = deliveries
    visited = []
    miles = 0
    loaded_on_time = curr_time

    if truck1[0] is True:
        enroute = truck1[1] + ': enroute'
        delivered = truck1[1] + ': delivered'
    elif truck2[0] is True:
        enroute = truck2[1] + ': enroute'
        delivered = truck2[1] + ': delivered'

    for pac in packages:
        pac.getValue().set_delivery_status('delivered')

    for value in route:
        deliveries[value] = DeliveryInfo.DeliveryInfo(value, enroute, None, loaded_on_time, False)

    for index, value in enumerate(route):
        if not index + 1 > len(route) - 1:
            miles_dif = get_dist_from_to(loc_dis_list, packages.find(route[index]).getValue().get_distances(),
                                         packages.find(route[index + 1]).getValue().get_distances())
            miles = miles + miles_dif
            curr_time = curr_time + datetime.timedelta(minutes=(miles_dif / 18) * 60)
            deliveries[route[index]] = DeliveryInfo.DeliveryInfo(route[index], delivered, curr_time, loaded_on_time,
                                                                 True)
            visited.append(route[index])
        deliveries[route[index]] = DeliveryInfo.DeliveryInfo(route[index], delivered, curr_time, loaded_on_time, True)
        visited.append(route[index])

    visited.append(route[len(route) - 1])
    return [miles, curr_time, visited, deliveries]


# creates the morning route with package that needs to be delivered first. takes in up to 5 different list to build route from
def get_packages_for_morning_route_with_earliest(hub, earliest, morning, any_time, loc_dist_list, truck1_only,
                                                 truck2_third_list):
    main_packages = morning
    secondary_packages = any_time
    curr_index = 0
    current = []
    truck = []
    loc_dist_list = loc_dist_list
    truck2 = truck2_third_list[0]
    truck2_third_list = truck2_third_list[1]

    # if there are packages that need to be delivered early put them at the front of the line
    if len(earliest) > 0:
        for index, value in enumerate(earliest):
            if len(truck) <= 16:
                truck.append(value)
                current.append(get_next_closest_loc(loc_dist_list, main_packages, truck[index], truck,
                                                    switch_list=[False, None]))
                truck.append(current[0][1])
        # print(truck1_only, truck2_third_list,truck, current)
        for i in range(len(main_packages)):
            if len(truck) <= 16:
                curr = current[curr_index][1]
                curr_val = get_next_closest_loc(loc_dist_list, main_packages, curr, truck,
                                                switch_list=[False, None])
                if curr_val is not None:
                    current.append(curr_val)
                    if current[curr_index + 1] is not None:
                        truck.append(current[curr_index + 1][1])
                        curr_index += 1

    # if no early packages need delivering create route from other data only
    else:
        driver = get_start_id_test_avg(list(main_packages.keys()), main_packages, loc_dist_list)
        first_key = min(driver, key=driver.get)
        if first_key is None:
            first_key = random.choice(list(main_packages.keys()))
        truck.append(first_key)
        current.append(get_next_closest_loc(loc_dist_list, main_packages, truck[0], truck, switch_list=[False, None]))
        truck.append(current[0][1])
        for i in range(len(main_packages)):
            if len(truck) <= 16:
                curr = current[curr_index][1]
                curr_val = get_next_closest_loc(loc_dist_list, main_packages, curr, truck,
                                                switch_list=[False, None])
                if curr_val is not None:
                    current.append(curr_val)
                    if current[curr_index + 1] is not None:
                        truck.append(current[curr_index + 1][1])
                        curr_index += 1

    # if the truck is full dont add anymore packages
    if len(truck) == 16:
        return truck
    curr_index = len(current) - 1

    curr = current[curr_index][1]
    curr_val = get_next_closest_loc(loc_dist_list, main_packages, curr, truck, switch_list=[True, secondary_packages])
    current.append(curr_val)
    truck.append(current[curr_index + 1][1])
    curr_index += 1

    for i in range(len(secondary_packages)):
        if len(truck) < 16:
            # print(len(truck), i)
            curr = current[curr_index][1]
            curr_val = get_next_closest_loc(loc_dist_list, secondary_packages, curr, truck, switch_list=[False, None])
            if curr_val is not None:
                current.append(curr_val)
                if current[curr_index + 1] is not None:
                    truck.append(current[curr_index + 1][1])
                    curr_index += 1

    if truck2 is True:
        if len(truck) == 16:
            return truck
        curr_index = len(current) - 1

        curr = current[curr_index][1]
        curr_val = get_next_closest_loc(loc_dist_list, secondary_packages, curr, truck,
                                        switch_list=[True, truck2_third_list])
        current.append(curr_val)
        truck.append(current[curr_index + 1][1])
        curr_index += 1

        for i in range(len(truck2_third_list)):
            if len(truck) < 16:
                # print(len(truck), i)
                curr = current[curr_index][1]
                curr_val = get_next_closest_loc(loc_dist_list, truck2_third_list, curr, truck,
                                                switch_list=[False, None])
                if curr_val is not None:
                    current.append(curr_val)
                    if current[curr_index + 1] is not None:
                        truck.append(current[curr_index + 1][1])
                        curr_index += 1

    return truck


# build the afternoon route can take 3 list including time sensitive packages
def get_all_packages_build_afternoon_route(hub, earliest, afternoon, any_time, loc_dist_list):
    afternoon_packages = afternoon
    any_time_packages = any_time
    curr_index = 0
    current = []
    truck = []
    loc_dist_list = loc_dist_list

    for index, value in enumerate(earliest):
        if len(truck) <= 16:
            truck.append(value)
            current.append(
                get_next_closest_loc(loc_dist_list, afternoon_packages, truck[index], truck, switch_list=[False, None]))
            truck.append(current[0][1])
    for i in range(len(afternoon_packages)):
        if len(truck) <= 16:
            curr = current[curr_index][1]
            curr_val = get_next_closest_loc(loc_dist_list, afternoon_packages, curr, truck, switch_list=[False, None])
            if curr_val is not None:
                current.append(curr_val)
                if current[curr_index + 1] is not None:
                    truck.append(current[curr_index + 1][1])
                    curr_index += 1
    if len(truck) == 16:
        return truck
    curr_index = len(current) - 1

    curr = current[curr_index][1]
    curr_val = get_next_closest_loc(loc_dist_list, afternoon_packages, curr, truck,
                                    switch_list=[True, any_time_packages])
    current.append(curr_val)
    truck.append(current[curr_index + 1][1])
    curr_index += 1

    for i in range(len(any_time_packages)):
        if len(truck) <= 16:
            curr = current[curr_index][1]
            curr_val = get_next_closest_loc(loc_dist_list, any_time_packages, curr, truck, switch_list=[False, None])
            if curr_val is not None:
                current.append(curr_val)
                if current[curr_index + 1] is not None:
                    truck.append(current[curr_index + 1][1])
                    curr_index += 1

    return truck
