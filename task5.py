from __future__ import annotations

import numpy as np
import pandas as pd


chem = pd.DataFrame({
    "action_id": [10, 10, 10, 10, 11, 11, 11],
    "Mn": [1.0, 1.1, 2.5, 2.5, 0.2, 0.3, 1.0],
    "timestamp": [
        "11:30",
        "11:35",
        "12:00",
        "12:05",
        "23:00",
        "23:30",
        "00:10"]})
addings = pd.DataFrame({
    "action_id": [10, 10, 11],
    "Mn": [500, 100, 400],
    "timestamp": [
        "11:45",
        "12:00",
        "23:55"]})

result = pd.DataFrame({
    "action_id": [10, 11],
    "Mn_add": [600, 400],
    "Mn_befor": [1.1, 0.3],
    "Mn_after": [2.5, 1.0],
    "timestamp": [
        "11:45",
        "23:55"]})


def solution(chem_, addings_):
    """
    Написати програму що поверне змерджений датафрейм відповідно до прикладу:
    "action_id" - ід процесу
    "Mn_add" - маса внесеного
    "Mn_befor" - хім аналіз до внесення
    "Mn_after" - хім аналіз відразу після внесення
    "timestamp" - початок внесення речовини
    """
    # turning on the time machine
    chem_ = chem_.astype({"timestamp": "str"})
    addings_ = addings_.astype({"timestamp": "str"})

    result_ = pd.DataFrame({"action_id": [],
                            "Mn_add": [],
                            "Mn_befor": [],
                            "Mn_after": [],
                            "timestamp": []})

    chem_['timestamp'] = pd.to_datetime(chem_['timestamp'], format='%H:%M', dayfirst=True)
    addings_['timestamp'] = pd.to_datetime(addings_['timestamp'], format='%H:%M', dayfirst=True)
    flag_of_new_day = pd.to_datetime("00:00", format='%H:%M', dayfirst=True).hour
    # print("\n\n\n--------IM HERE--------\n\n\n", flag_of_new_day)

    # united_timestamps = (
    #     pd.concat((chem_['timestamp'], addings_['timestamp']), ignore_index=True).sort_values(ignore_index=True))
    # print("\n\n\n--------IM HERE--------\n\n\n", united_timestamps)
    # i = 1
    # for index in addings_.index:
    #     # print("Timestamp before:\n", addings_.at[index, 'timestamp'])
    #     addings_.at[index, 'timestamp'] += pd.DateOffset(day=i)
    #     i += 1
    # i = 1
    # for index in chem_.index:
    #     # print("Timestamp before:\n", addings_.at[index, 'timestamp'])
    #     chem_.at[index, 'timestamp'] += pd.DateOffset(day=i)
    #     i += 1
    #     # print("\nTimestamp after:\n", addings_.at[index, 'timestamp'])
    # # df['new_charge_date'] = pd.to_datetime(df['charge_date']).apply(pd.DateOffset(3))
    i = 2

    for index in chem_.index:
        if chem_.at[index, 'timestamp'].hour == flag_of_new_day:
            chem_.at[index, 'timestamp'] += pd.DateOffset(day=i)
            i += 1

    time_flag = 0
    for action in addings_.action_id.unique():
        mn_add = addings_[addings_.action_id == action].Mn.sum()

        first_adding_time = addings_[addings_.action_id == action].timestamp.min()
        last_adding_time = addings_[addings_.action_id == action].timestamp.max()

        time_before = chem_.loc[chem_['timestamp'] < first_adding_time].timestamp.max()
        time_after = chem_.loc[chem_['timestamp'] > last_adding_time].timestamp.min()

        mn_before = chem_.loc[chem_['timestamp'] == time_before].Mn
        mn_after = chem_.loc[chem_['timestamp'] == time_after].Mn

        # print("\n\nfirst adding time: ", first_adding_time)
        # print("last adding time: ", last_adding_time)
        #
        # print("\n\ntime_before: ", time_before)
        # print("time_after: ", time_after)
        #
        # print("\n\nmn_before: ", mn_before)
        # print("mn_after: ", mn_after)

        np_array = np.asarray([action, mn_add, mn_before.values[0], mn_after.values[0],
                               addings_.timestamp.iloc[time_flag].strftime('%H:%M')], dtype=object)
        result_.loc[len(result_.index)] = np_array

        time_flag -= 1

    return result_


# chem['timestamp'] = pd.to_datetime(chem['timestamp'], format='%H:%M')
# a = pd.to_datetime(addings['timestamp'], format='%H:%M')
# print(chem.loc[chem['timestamp'] < a, 'Mn'].max())


print("Chem:\n", chem, "\n\n---------------------\n\n")
print("Addings:\n", addings, "\n\n---------------------\n\n")
print("Result:\n", result, "\n\n---------------------\n\n")

# print(addings["action_id"].unique()[1])

# print(addings[addings.action_id == 10].timestamp.min())
#
# first_adding_time = addings[addings.action_id == 10].timestamp.min()
# last_adding_time = addings[addings.action_id == 10].timestamp.max()
# time_before = chem.loc[chem['timestamp'] < first_adding_time].timestamp.max()
# time_after = chem.loc[chem['timestamp'] > last_adding_time].timestamp.min()
# mn_before = chem.loc[chem['timestamp'] == time_before].Mn
# mn_after = chem.loc[chem['timestamp'] == time_after].Mn
#
# print(mn_after.apply(pd.to_numeric, errors='coerce'))

print(solution(chem, addings).head())