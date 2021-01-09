import datetime
import time
from itertools import chain

import Route
from DeliveryInfo import merge
import RuleSet
import DataInput



def add_correlated_packages(list1, dict1):
    vals = list(dict1.values())
    keys = list(dict1.keys())
    for row_index, rows in enumerate(vals):
        for col_index, val in enumerate(rows):
            for elem in list1:
                elem_id = elem.getValue().get_id()
                if elem_id == val:
                    result = [True, keys[row_index]]
                    return result
    return [False, None]



if __name__ == '__main__':

    class Main:
        START_TIME = datetime.datetime.strptime('08:00:00', '%I:%M:%S')
        DELAYED_START_TIME = datetime.datetime.strptime('09:05:00', '%I:%M:%S')
        start_id = 15
        hub = 'Western Governors University 4001 South 700 East, Salt Lake City, UT 84107'
        curr_time = datetime.datetime
        total_miles = 0
        curr_miles = 0

        loc_dis_list = DataInput.Data.distances
        truck_1 = {}
        truck_2 = {}
        packages_for_truck1 = []
        packages_for_truck2 = []
        morning_packages = []
        any_time_packages = []
        all_package_list = [[]]
        late_run_only_list = []
        aux_packages = []
        correlated_packages = {}
        packages = DataInput.Data.packages
        route = Route
        deliveries = {}

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
                # pass
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

        # Further filter the aux list to deal with special cases
        for i, p in enumerate(aux_packages):
            notes = p.getValue().get_notes()
            p_id = p.getValue().get_id()
            results = RuleSet.deal_with_aux_packages(notes)
            if results is not None:
                correlated_packages[p_id] = results
                aux_packages[i] = None

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


        for key, v in correlated_packages.items():
            packages.find(v[0]).getValue().get_deadline()
            if RuleSet.fill_morning_list(packages.find(v[0]).getValue().get_deadline(), packages.find(v[0]).getValue().get_notes()) or RuleSet.fill_morning_list(packages.find(v[1]).getValue().get_deadline(), packages.find(v[1]).getValue().get_notes()):
                morning_packages.append(packages.find(v[0]))
                morning_packages.append(packages.find(v[1]))
                morning_packages.append(packages.find(key))
            elif RuleSet.fill_late_list(packages.find(v[0]).getValue().get_deadline(), packages.find(v[0]).getValue().get_notes()) or RuleSet.fill_late_list(packages.find(v[1]).getValue().get_deadline(), packages.find(v[1]).getValue().get_notes()):
                late_run_only_list.append(packages.find(v[0]))
                late_run_only_list.append(packages.find(v[1]))
                late_run_only_list.append(packages.find(key))
            elif RuleSet.fill_anytime_list(packages.find(v[0]).getValue().get_deadline(), packages.find(v[0]).getValue().get_notes()) or RuleSet.fill_anytime_list( packages.find(v[1]).getValue().get_deadline(), packages.find(v[1]).getValue().get_notes()):
                any_time_packages.append(packages.find(v[0]))
                any_time_packages.append(packages.find(v[1]))
                any_time_packages.append(packages.find(key))


        # start_id = min(morning_packages, key=lambda x: x.getValue().get_deadline()).getValue().get_id()
        morning_packages = Route.change_to_dict(morning_packages)
        packages_for_truck1 = Route.change_to_dict(packages_for_truck1)
        packages_for_truck2 = Route.change_to_dict(packages_for_truck2)
        any_time_packages = Route.change_to_dict(any_time_packages)
        late_run_only_list = Route.change_to_dict(late_run_only_list)
        aux_packages = Route.change_to_dict(aux_packages)

        morning_packages_keys = list(morning_packages.keys())
        packages_for_truck2_keys = list(packages_for_truck2.keys())
        any_time_packages_keys = list(any_time_packages.keys())
        late_run_only_list_keys = list(late_run_only_list.keys())



        print(packages_for_truck1)
        print(len(packages_for_truck2))
        print(morning_packages)
        print(len(any_time_packages))
        print(len(late_run_only_list))
        print(len(aux_packages))
        print(loc_dis_list)

        ######################################  V2 #####################################

        # fill morning run truck1
        earliest = []
        for k, v in morning_packages.items():
            if isinstance(v.get_deadline(), datetime.datetime):
                if v.get_deadline().hour < 10:
                    truck_1[k] = v
                    earliest.append(k)

        morning_run_truck1 = Route.get_packages_for_morning_route_with_earliest(hub, earliest, morning_packages, any_time_packages, loc_dis_list, [False, None], [False, None])
        for key in morning_run_truck1:
            if key in morning_packages_keys:
                morning_packages.pop(key)
            if key in any_time_packages_keys:
                any_time_packages.pop(key)

        # [miles, datetime, visited, deliveries
        # print(morning_run_truck1)
        truck1_deliveries = Route.new_run_route(morning_run_truck1, packages, START_TIME, loc_dis_list, [True, 'Truck 1'], [False,'Truck 2'])
        print(total_miles)
        total_miles = total_miles + truck1_deliveries[0]
        print('total miles:', total_miles, 'packages delivered:', len(truck1_deliveries[3]), 'double check:', truck1_deliveries[2])
        ######################
        # fill morning(delayed) run truck2

        morning_run_truck2 = Route.get_packages_for_morning_route_with_earliest(hub, [], aux_packages, packages_for_truck2, loc_dis_list, [False, None], [True, any_time_packages])
        # print('morn run t2:', morning_run_truck2)
        for key in morning_run_truck2:
            if key in any_time_packages_keys:
                any_time_packages.pop(key)
            if key in packages_for_truck2_keys:
                packages_for_truck2.pop(key)

        truck2_deliveries = Route.new_run_route(morning_run_truck2, packages, DELAYED_START_TIME, loc_dis_list, [False, 'Truck 1'], [True,'Truck 2'])
        # print(truck2_deliveries)
        total_miles = total_miles + truck2_deliveries[0]
        print('total miles:', total_miles, 'packages delivered:', len(truck2_deliveries[3]), 'double check:', truck2_deliveries[2])
        #################################
        # truck 2 second run
        # add return miles
        curr_time = truck2_deliveries[1]
        return_miles = Route.get_dist_from_to(loc_dis_list, packages.find(morning_run_truck2[-1]).getValue().get_distances(), hub)
        print(return_miles)
        total_miles = total_miles + return_miles
        print(total_miles)
        # add return time
        curr_time = curr_time + datetime.timedelta(minutes=(return_miles / 18) * 60)

        afternoon_run_truck2 = Route.get_packages_for_morning_route_with_earliest(hub, [], late_run_only_list, any_time_packages , loc_dis_list, [False, None], [False, None])

        # print('afternoon run t2:', afternoon_run_truck2)
        for key in afternoon_run_truck2:
            if key in any_time_packages_keys:
                any_time_packages.pop(key)
            if key in late_run_only_list_keys:
                late_run_only_list.pop(key)

        truck2_afternoon_deliveries = Route.new_run_route(afternoon_run_truck2, packages, curr_time, loc_dis_list,
                                                [False, 'Truck 1'], [True, 'Truck 2'])
        # print(truck2_afternoon_deliveries)
        total_miles = total_miles + truck2_afternoon_deliveries[0]
        print('total miles:', total_miles, 'packages delivered:', len(truck2_afternoon_deliveries[3]), 'double check:', truck2_afternoon_deliveries[2])
        ############################################################
        print()

        # merge all deliveries into one big dictionary
        deliveries = merge(truck1_deliveries[3], truck2_deliveries[3], truck2_afternoon_deliveries[3])
        print(len(deliveries), deliveries)
        # Complete but if I want to optimize it some more - choose from all packages while building route and base the
        # ruleset from that individual choice. Such as. are there still morning packages? get the next closest one from
        # one of those. if not is there any that needs



            # print(p_time)
            # early package.no notes
            # LoadTruck.fill_morning_list(package_time, package_notes)
            # truck 1 only
            # LoadTruck.fill_truck1_only_list(package_notes)
            # truck 2 only
            # LoadTruck.fill_truck2_only_list(package_notes)
            # any time.no notes
            # LoadTruck.fill_anytime_list(package_time, package_notes)
            # late.no notes
            # LoadTruck.fill_late_list(package_time, package_notes)

            #

        # print(DataInput.Data.list_of_distances)

# TODO load the truck