import json



f = open("dialog-task5FULL-kb1_atmosphere-distr0.5-trn10000.json", "r")
f_1 = open("dialog-task1API-kb1_atmosphere-distr0.5-trn10000.json", "r")
f_2 = open("dialog-task2REFINE-kb1_atmosphere-distr0.5-trn10000.json", "r")
f_3 = open("dialog-task3OPTIONS-kb1_atmosphere-distr0.5-trn10000.json", "r")
f_4 = open("dialog-task4INFOS-kb1_atmosphere-distr0.5-trn10000.json", "r")

f2 = open("taskall_train85.json", "w")
f2_1 = open("taskall_train_85_90.json", "w")
f2_2 = open("taskall_train_85_10.json", "w")
t1 = open("task1_train85.json", "w")
t2 = open("task2_train85.json", "w")
t3 = open("task3_train85.json", "w")
t4 = open("task4_train85.json", "w")
t5 = open("task5_train85.json", "w")


f3 = open("taskall_valid15.json", "w")

f3_1 = open("task1_valid15.json", "w")
f3_2 = open("task2_valid15.json", "w")
f3_3 = open("task3_valid15.json", "w")
f3_4 = open("task4_valid15.json", "w")
f3_5 = open("task5_valid15.json", "w")

json_data = json.load(f)

f2_data = []
f2_1d = []
f2_2d = []
f3_data = []
f3_1d = []
f3_2d = []
f3_3d = []
f3_4d = []
f3_5d = []
t1d = []
t2d = []
t3d = []
t4d = []
t5d = []

for idx, story in enumerate(json_data):
    if idx < 8500:
        f2_data.append(story)
        f2_1d.append(story)
        t5d.append(story)
        if idx >= 7650:
            f2_2d.append(story)
    else:
        f3_data.append(story)
        f3_5d.append(story)
json_data = json.load(f_1)
for idx, story in enumerate(json_data):
    if idx < 8500:
        f2_data.append(story)
        f2_1d.append(story)
        t1d.append(story)
        if idx >= 7650:
            f2_2d.append(story)
    else:
        f3_data.append(story)
        f3_1d.append(story)
json_data = json.load(f_2)
for idx, story in enumerate(json_data):
    if idx < 8500:
        f2_data.append(story)
        f2_1d.append(story)
        t2d.append(story)
        if idx >= 7650:
            f2_2d.append(story)
    else:
        f3_data.append(story)
        f3_2d.append(story)
json_data = json.load(f_3)
for idx, story in enumerate(json_data):
    if idx <8500:
        f2_data.append(story)
        f2_1d.append(story)
        t3d.append(story)
        if idx >= 7650:
            f2_2d.append(story)
    else:
        f3_data.append(story)
        f3_3d.append(story)
json_data = json.load(f_4)
for idx, story in enumerate(json_data):
    if idx < 8500:
        f2_data.append(story)
        f2_1d.append(story)
        t4d.append(story)
        if idx >= 7650:
            f2_2d.append(story)
    else:
        f3_data.append(story)
        f3_4d.append(story)


json.dump(f2_data, f2)
json.dump(f2_1d, f2_1)
json.dump(f2_2d, f2_2)
json.dump(f3_data, f3)
json.dump(f3_1d, f3_1)
json.dump(f3_2d, f3_2)
json.dump(f3_3d, f3_3)
json.dump(f3_4d, f3_4)
json.dump(f3_5d, f3_5)
json.dump(t1d, t1)
json.dump(t2d, t2)
json.dump(t3d, t3)
json.dump(t4d, t4)
json.dump(t5d, t5)


f.close()
f_1.close()
f_2.close()
f_3.close()
f_4.close()
f2.close()
f2_1.close()
f2_2.close()
f3.close()
f3_1.close()
f3_2.close()
f3_3.close()
f3_4.close()
f3_5.close()
