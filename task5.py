from __future__ import annotations

import numpy as np
import pandas as pd

test_case = 1
test_cases = [
    [
        pd.DataFrame({
            "action_id": [10, 10, 10, 10, 11, 11, 11],
            "Mn": [1.0, 1.1, 2.5, 2.5, 0.2, 0.3, 1.0],
            "timestamp": ["11:30", "11:35", "12:00", "12:05", "23:00", "23:30", "00:10"]}),
        pd.DataFrame({
            "action_id": [10, 10, 11],
            "Mn": [500, 100, 400],
            "timestamp": ["11:45", "12:00", "23:55"]}),
        pd.DataFrame({
            "action_id": [10, 11],
            "Mn_add": [600, 400],
            "Mn_befor": [1.1, 0.3],
            "Mn_after": [2.5, 1.0],
            "timestamp": ["11:45", "23:55"]})
    ],
    [
        pd.DataFrame({
            "action_id": [10, 10, 10, 10, 11, 11, 11],
            "Mn": [1.0, 1.1, 2.5, 2.6, 0.2, 0.3, 1.0],
            "timestamp": ["11:30", "11:35", "12:00", "12:05", "23:00", "23:30", "00:10"]
        }),
        pd.DataFrame({
            "action_id": [10, 10, 11],
            "Mn": [100, 100, 400],
            "timestamp": ["11:45", "12:00", "23:55"]
        }),
        pd.DataFrame({
            "action_id": [10, 11],
            "Mn_add": [200, 400],
            "Mn_befor": [1.1, 0.3],
            "Mn_after": [2.6, 1.0],
            "timestamp": ["11:45", "23:55"]
        })
    ],
    [
        pd.DataFrame({
            "action_id": [10, 11],
            "Mn": [2.6, 0.2],
            "timestamp": ["12:05", "23:00"]
        }),
        pd.DataFrame({
            "action_id": [10, 10, 11],
            "Mn": [100, 100, 400],
            "timestamp": ["11:45", "12:00", "23:55"]
        }),
        pd.DataFrame({
            "action_id": [10, 11],
            "Mn_add": [200, 400],
            "Mn_befor": [np.nan, 0.2],
            "Mn_after": [2.6, np.nan],
            "timestamp": ["11:45", "23:55"]
        })
    ]

]
chem, addings, result = test_cases[test_case]


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

    chem_["timestamp"] = ("1970-01-01T" + chem_["timestamp"]).astype("datetime64[ns]")
    addings_["timestamp"] = ("1970-01-01T" + addings_["timestamp"]).astype("datetime64[ns]")

    result_ = pd.DataFrame({"action_id": [],
                            "Mn_add": [],
                            "Mn_befor": [],
                            "Mn_after": [],
                            "timestamp": []})

    # chem_['timestamp'] = pd.to_datetime(chem_['timestamp'], format='%H:%M', dayfirst=True)
    # addings_['timestamp'] = pd.to_datetime(addings_['timestamp'], format='%H:%M', dayfirst=True)
    flag_of_new_day = pd.to_datetime("00:00", format='%H:%M', dayfirst=True).hour

    i = 1
    for index in chem_.index:
        if chem_.at[index, 'timestamp'].hour == flag_of_new_day:
            chem_.at[index, 'timestamp'] += pd.Timedelta(days=i)
            i += 1

    time_flag = 0
    for action in addings_.action_id.unique():
        mn_add = int(addings_[addings_.action_id == action].Mn.sum())

        first_adding_time = addings_[addings_.action_id == action].timestamp.min()
        last_adding_time = addings_[addings_.action_id == action].timestamp.max()

        time_before = chem_.loc[chem_['timestamp'] < first_adding_time].timestamp.max()
        time_after = chem_.loc[chem_['timestamp'] > last_adding_time].timestamp.min()

        mn_before = chem_.loc[chem_['timestamp'] == time_before].Mn
        mn_after = chem_.loc[chem_['timestamp'] == time_after].Mn

        if len(mn_before.index) == 0:
            mn_before = np.nan
        else:
            mn_before = mn_before.values[0]
        if len(mn_after.index) == 0:
            mn_after = np.nan
        else:
            mn_after = mn_after.values[0]
        # print("\n\nfirst adding time: ", first_adding_time)
        # print("last adding time: ", last_adding_time)
        #
        # print("\n\ntime_before: ", time_before)
        # print("time_after: ", time_after)
        #
        # print("\n\nmn_before: ", mn_before)
        # print("mn_after: ", mn_after)

        # np_array = np.asarray([action, mn_add, mn_before.values[0], mn_after.values[0],
        #                        addings_.timestamp.iloc[time_flag].strftime('%H:%M')], dtype=object)

        result_.loc[len(result_.index)] = [action, mn_add, mn_before, mn_after,
                                           addings_.timestamp.iloc[time_flag].strftime('%H:%M')]

        time_flag -= 1

    return result_

print("Chem:\n", chem, "\n\n---------------------\n\n")
print("Addings:\n", addings, "\n\n---------------------\n\n")
print("Result:\n", result, "\n\n---------------------\n\n")

# assert (str(result) == str(solution(chem, addings)))
print("My output:\n", solution(chem, addings))
