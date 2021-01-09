import datetime
import Truck
import Package

# def _get_packages():
#     for package in DataInput.Data.packages:
#         print('id:', package.getValue().get_id(), ', deadline:', package.getValue().get_deadline(), ', notes:',
#               package.getValue().get_notes(), ', delivery_status:', package.getValue().get_visited())


def fill_morning_list(package_time, package_notes):
    if isinstance(package_time, str):
        print(package_time)
        return False
    if package_time.hour < 11 and package_notes == '':
        return True
    else:
        return False

def fill_truck1_only_list(package_notes):
    if str(package_notes).lower().__contains__('truck 1'):
        return True
    else:
        return False

def fill_truck2_only_list(package_notes):
    if str(package_notes).lower().__contains__('truck 2'):
        return True
    else:
        return False

def fill_anytime_list(package_time, package_notes):
    if package_time == "EOD" and package_notes == '':
        return True
    else:
        return False

def fill_late_list(package_time, package_notes):
    if (package_time == "EOD" and str(package_notes).lower().__contains__('delayed')) or (package_time == "EOD" and str(package_notes).lower().__contains__('wrong address')):
        return True
    else:
        return False

def deal_with_aux_packages(package_notes):
    if str(package_notes).lower().__contains__('must be delivered with'):
        # get correlated packages from notes
        correlated_packages = str(package_notes).split(',')
        for s_index, s in enumerate(correlated_packages):
            correlated_packages[s_index] = int(''.join(letter for letter in correlated_packages[s_index] if letter.isdigit()))
        # find the most specific list
        return correlated_packages

def deal_with_correlated_packages(package_notes):
    if str(package_notes).lower().__contains__('must be delivered'):
        # get correlated packages from notes
        correlated_packages = str(package_notes).split(',')
        for s_index, s in enumerate(correlated_packages):
            correlated_packages[s_index] = int(''.join(letter for letter in correlated_packages[s_index] if letter.isdigit()))
        # find the most specific list
        return correlated_packages
    return None
