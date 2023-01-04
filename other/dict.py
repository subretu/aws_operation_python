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
before_index = 0

for index, row in df.iterrows():
    for alarm in row["alarm"].split(","):
        alarm_unit = MASTER.get(alarm)
        if (alarm_unit not in dict_alarm.keys()) and (
            alarm_unit not in dict_time.keys()
        ):
            # 最初に各keyを定義し値を設定していく
            dict_alarm[alarm_unit] = {}
            dict_time[alarm_unit] = {}

            dict_alarm[alarm_unit] = set()
            dict_time[alarm_unit] = 0

            dict_alarm[alarm_unit].add(alarm)
            dict_time[alarm_unit] = row["time_msec"]
        # alarmが単一の場合
        elif len(row["alarm"].split(",")) == 1:
            dict_alarm[alarm_unit].add(row["alarm"])
            dict_time[alarm_unit] = dict_time[alarm_unit] + row["time_msec"]
        else:
            # keyに重複がなければ値を変更する
            dict_alarm[alarm_unit].add(alarm)
            if alarm_unit not in dict_time.keys() or index != before_index:
                dict_time[alarm_unit] = dict_time[alarm_unit] + row["time_msec"]
        before_index = index


# 値の降順でソートし、dictを再作成
dict_time2 = dict(sorted(dict_time.items(), key=lambda x: x[1], reverse=True))
