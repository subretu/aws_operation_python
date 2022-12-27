import pandas as pd

MASTER = {
    "A": "unitA",
    "B": "unitB",
    "C": "unitC",
    "D": "unitD",
    "E": "unitE",
    "F": "unitF",
}

df = pd.read_csv("./sample.csv")

dict_alarm = {}
dict_time = {}

for index, row in df.iterrows():
    if len(row["alarm"].split(",")) > 1:
        for alarm in row["alarm"].split(","):
            if (MASTER.get(alarm) not in dict_alarm.keys()) and (
                MASTER.get(alarm) not in dict_time.keys()
            ):
                dict_alarm[MASTER.get(alarm)] = {}
                dict_time[MASTER.get(alarm)] = {}

                dict_alarm[MASTER.get(alarm)] = set()
                dict_time[MASTER.get(alarm)] = 0

                dict_alarm[MASTER.get(alarm)].add(alarm)
                dict_time[MASTER.get(alarm)] = row["time_msec"]
            else:
                dict_alarm[MASTER.get(alarm)].add(alarm)
                if MASTER.get(alarm) not in dict_time.keys():
                    dict_time[MASTER.get(alarm)] = (
                        dict_time[MASTER.get(alarm)] + row["time_msec"]
                    )
    else:
        if (MASTER.get(row["alarm"]) not in dict_alarm.keys()) and (
            MASTER.get(row["alarm"]) not in dict_time.keys()
        ):
            dict_alarm[MASTER.get(row["alarm"])] = {}
            dict_time[MASTER.get(row["alarm"])] = {}

            dict_alarm[MASTER.get(row["alarm"])] = set()
            dict_time[MASTER.get(row["alarm"])] = 0

            dict_alarm[MASTER.get(row["alarm"])].add(row["alarm"])
            dict_time[MASTER.get(row["alarm"])] = row["time_msec"]
        else:
            dict_alarm[MASTER.get(row["alarm"])].add(row["alarm"])
            dict_time[MASTER.get(row["alarm"])] = (
                dict_time[MASTER.get(row["alarm"])] + row["time_msec"]
            )

# 値の降順でソートし、dictを再作成
dict_time2 = dict(sorted(dict_time.items(), key=lambda x: x[1], reverse=True))
