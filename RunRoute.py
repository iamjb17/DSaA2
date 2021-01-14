import datetime
import Route
from DeliveryInfo import merge
import RuleSet
import DataInput


# O(n^3) dominates this method
def run_route():
    # Start time for the business to open and delivery trucks leave the hub
    START_TIME = datetime.datetime.strptime('08:00:00', '%I:%M:%S')
    # Start time for truck waiting on delayed packages to reduce the number of return trips
    DELAYED_START_TIME = datetime.datetime.strptime('09:05:00', '%I:%M:%S')
    # Permanent location of the hub
    hub = 'Western Governors University 4001 South 700 East, Salt Lake City, UT 84107'
    curr_time = datetime.datetime
    total_miles = 0
    curr_miles = 0
    time_of_update = datetime.datetime.strptime('10:20:00', '%I:%M:%S')

    loc_dis_list = DataInput.Data.distances
    truck_1 = {}
    truck_2 = {}
    packages_for_truck1 = []
    packages_for_truck2 = []
    morning_packages = []
    any_time_packages = []
    late_run_only_list = []
    aux_packages = []
    correlated_packages = {}
    packages = DataInput.Data.packages
    deliveries = {}

    # O(2n)
    # Send packages through the rule set and put them in their respective list
    for package in packages:
        package_time = package.getValue().get_deadline()
        package_notes = package.getValue().get_notes()
        if isinstance(package_time, str):
            if RuleSet.fill_truck1_only_list(package_notes):
                packages_for_truck1.append(package)
            elif RuleSet.fill_truck2_only_list(package_notes):
                packages_for_truck2.append(package)
            elif RuleSet.fill_anytime_list(package_time, package_notes):
                any_time_packages.append(package)
            elif RuleSet.fill_late_list(package_time, package_notes):
                late_run_only_list.append(package)
            else:
                aux_packages.append(package)
        elif isinstance(package_time, datetime.time):
            if RuleSet.fill_morning_list(package_time, package_notes):
                morning_packages.append(package)
            elif RuleSet.fill_truck1_only_list(package_notes):
                packages_for_truck1.append(package)
            elif RuleSet.fill_truck2_only_list(package_notes):
                packages_for_truck2.append(package)
            elif RuleSet.fill_late_list(package_time, package_notes):
                late_run_only_list.append(package)
            else:
                aux_packages.append(package)

    # O(n^2)
    # Further filter the aux list to deal with special cases/notes
    for i, p in enumerate(aux_packages):
        notes = p.getValue().get_notes()
        p_id = p.getValue().get_id()
        results = RuleSet.deal_with_aux_packages(notes)
        if results is not None:
            correlated_packages[p_id] = results
            aux_packages[i] = None

    # O(n^3)
    # remove any package correlated with another package from all list
    for key, v in correlated_packages.items():
        for val1 in v:
            for index, elem in enumerate(packages_for_truck1):
                if elem.getValue().get_id() == val1:
                    packages_for_truck1.pop(index)
            for index, elem in enumerate(packages_for_truck2):
                if elem.getValue().get_id() == val1:
                    packages_for_truck2.pop(index)
            for index, elem in enumerate(morning_packages):
                if elem.getValue().get_id() == val1:
                    morning_packages.pop(index)
            for index, elem in enumerate(late_run_only_list):
                if elem.getValue().get_id() == val1:
                    late_run_only_list.pop(index)
            for index, elem in enumerate(any_time_packages):
                if elem.getValue().get_id() == val1:
                    any_time_packages.pop(index)

    # O(n)
    # put all correlated packages that need to be delivered together in the same list to go into the same truck. the list depends on priority of the delivery deadline and/or notes
    for key, v in correlated_packages.items():
        packages.find(v[0]).getValue().get_deadline()
        if RuleSet.fill_morning_list(packages.find(v[0]).getValue().get_deadline(),
                                     packages.find(v[0]).getValue().get_notes()) or RuleSet.fill_morning_list(
            packages.find(v[1]).getValue().get_deadline(), packages.find(v[1]).getValue().get_notes()):
            morning_packages.append(packages.find(v[0]))
            morning_packages.append(packages.find(v[1]))
            morning_packages.append(packages.find(key))
        elif RuleSet.fill_late_list(packages.find(v[0]).getValue().get_deadline(),
                                    packages.find(v[0]).getValue().get_notes()) or RuleSet.fill_late_list(
            packages.find(v[1]).getValue().get_deadline(), packages.find(v[1]).getValue().get_notes()):
            late_run_only_list.append(packages.find(v[0]))
            late_run_only_list.append(packages.find(v[1]))
            late_run_only_list.append(packages.find(key))
        elif RuleSet.fill_anytime_list(packages.find(v[0]).getValue().get_deadline(),
                                       packages.find(v[0]).getValue().get_notes()) or RuleSet.fill_anytime_list(
            packages.find(v[1]).getValue().get_deadline(), packages.find(v[1]).getValue().get_notes()):
            any_time_packages.append(packages.find(v[0]))
            any_time_packages.append(packages.find(v[1]))
            any_time_packages.append(packages.find(key))

    # O(n^2)
    # change each list of packages to dict structure for better searching and sorting
    morning_packages = Route.change_to_dict(morning_packages)
    packages_for_truck1 = Route.change_to_dict(packages_for_truck1)
    packages_for_truck2 = Route.change_to_dict(packages_for_truck2)
    any_time_packages = Route.change_to_dict(any_time_packages)
    late_run_only_list = Route.change_to_dict(late_run_only_list)
    aux_packages = Route.change_to_dict(aux_packages)

    # O(n)
    # keep a list of all package ids and what dict the package is in for referencing multiple times
    morning_packages_keys = list(morning_packages.keys())
    packages_for_truck2_keys = list(packages_for_truck2.keys())
    any_time_packages_keys = list(any_time_packages.keys())
    late_run_only_list_keys = list(late_run_only_list.keys())

    # print(packages_for_truck1)
    # print(len(packages_for_truck2))
    # print(morning_packages)
    # print(len(any_time_packages))
    # print(len(late_run_only_list))
    # print(len(aux_packages))
    # print(loc_dis_list)

    ######################################  V2 #####################################

    # fill morning run truck1 with packages from list based on greedy route

    # O(n)
    # since this is the first truck and packages to go out, get the packages that needs to be delivered first
    earliest = []
    for k, v in morning_packages.items():
        if isinstance(v.get_deadline(), datetime.datetime):
            if v.get_deadline().hour < 10:
                truck_1[k] = v
                earliest.append(k)

    # O(n^2)
    # The route of truck 1s morning run. Based on greedy algorithm
    morning_run_truck1 = Route.get_packages_for_morning_route_with_earliest(hub, earliest, morning_packages,
                                                                            any_time_packages, loc_dis_list,
                                                                            [False, None], [False, None])
    # O(n^2)
    # If a package id is in the route of truck 1s morning run delete packaged from its container list
    for key in morning_run_truck1:
        if key in morning_packages_keys:
            morning_packages.pop(key)
        if key in any_time_packages_keys:
            any_time_packages.pop(key)

    # O(3n)
    # Runs the route and collects delivery data then returns that data [miles, datetime, visited, deliveries obj]
    truck1_deliveries = Route.new_run_route(morning_run_truck1, packages, START_TIME, loc_dis_list,
                                            [True, 'Truck 1'], [False, 'Truck 2'], deliveries)
    total_miles = total_miles + truck1_deliveries[0]
    # print('total miles:', total_miles, 'packages delivered:', len(truck1_deliveries[3]), 'double check:',
    #       truck1_deliveries[2])

    ######################
    # fill morning run truck2 with packages from list based on greedy route

    # O(n^2)
    # The route of truck 2s morning run. Based on greedy algorithm
    morning_run_truck2 = Route.get_packages_for_morning_route_with_earliest(hub, [], aux_packages,
                                                                            packages_for_truck2, loc_dis_list,
                                                                            [False, None],
                                                                            [True, any_time_packages])
    # O(n^2)
    # If a package id is in the route of truck 2s morning run delete packaged from its container list
    for key in morning_run_truck2:
        if key in any_time_packages_keys:
            any_time_packages.pop(key)
        if key in packages_for_truck2_keys:
            packages_for_truck2.pop(key)

    # O(3n)
    # Runs the route and collects delivery data then returns that data [miles, datetime, visited, deliveries obj]
    truck2_deliveries = Route.new_run_route(morning_run_truck2, packages, DELAYED_START_TIME, loc_dis_list,
                                            [False, 'Truck 1'], [True, 'Truck 2'], deliveries)
    total_miles = total_miles + truck2_deliveries[0]
    # print('total miles:', total_miles, 'packages delivered:', len(truck2_deliveries[3]), 'double check:',
    #       truck2_deliveries[2])

    #################################
    # truck 2 second run in the afternoon

    # get the time truck 2 last delivered its last package
    curr_time = truck2_deliveries[1]

    # add miles from return trip back to hub from last package location
    return_miles = Route.get_dist_from_to(loc_dis_list,
                                          packages.find(morning_run_truck2[-1]).getValue().get_distances(), hub)
    total_miles = total_miles + return_miles

    # add time it took for the truck to go back to hub
    curr_time = curr_time + datetime.timedelta(minutes=(return_miles / 18) * 60)
    load_2_start_time = curr_time

    # 410 S State St., Salt Lake City, UT 84111 / Third District Juvenile Court 410 S State St
    update_package_after_init(packages.find(9), ['410 S State St.', 'Salt Lake City', 'UT', '84111',
                                                 'Third District Juvenile Court 410 S State St'], curr_time,
                              late_run_only_list, time_of_update)

    # O(n^2)
    # The route of truck 2s afternoon run. Based on greedy algorithm
    afternoon_run_truck2 = Route.get_packages_for_morning_route_with_earliest(hub, [], late_run_only_list,
                                                                              any_time_packages, loc_dis_list,
                                                                              [False, None], [False, None])

    # O(n^2)
    # If a package id is in the route of truck 2s afternoon run delete packaged from its container list
    for key in afternoon_run_truck2:
        if key in any_time_packages_keys:
            any_time_packages.pop(key)
        if key in late_run_only_list_keys:
            late_run_only_list.pop(key)

    # O(3n)
    # Runs the route and collects delivery data then returns that data [miles, datetime, visited, deliveries obj]
    truck2_afternoon_deliveries = Route.new_run_route(afternoon_run_truck2, packages, curr_time, loc_dis_list,
                                                      [False, 'Truck 1'], [True, 'Truck 2'], deliveries)
    total_miles = total_miles + truck2_afternoon_deliveries[0]
    curr_time = truck2_afternoon_deliveries[1]
    # print('total miles:', total_miles, 'packages delivered:', len(truck2_afternoon_deliveries[3]), 'double check:',
    #       truck2_afternoon_deliveries[2])
    ############################################################

    # O(n)
    # merge all deliveries into one big dictionary
    deliveries = merge(truck1_deliveries[3], truck2_deliveries[3], truck2_afternoon_deliveries[3])
    # print('truck 1 morning miles:', truck1_deliveries[0], 'truck 2 morning miles:', truck2_deliveries[0], 'truck 2 afternoon miles:', truck2_afternoon_deliveries[0])
    return [deliveries, total_miles, curr_time, load_2_start_time.time(), morning_run_truck1, morning_run_truck2,
            afternoon_run_truck2, START_TIME.time(), DELAYED_START_TIME.time()]


# O(1)
# Update package that needs updating with new data
def update_package_after_init(package_to_update, update_info, curr_time, where_package_is_stored, time_of_update):
    if curr_time > time_of_update:
        package_to_update.getValue().set_delivery_city(update_info[1])
        package_to_update.getValue().set_delivery_address(update_info[0])
        package_to_update.getValue().set_delivery_state(update_info[2])
        package_to_update.getValue().set_delivery_distances(update_info[4])
        package_to_update.getValue().set_delivery_zip(update_info[3])
