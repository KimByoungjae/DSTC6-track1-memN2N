import json



f = open("dialog-task5FULL-kb1_atmosphere-distr0.5-trn10000.json", "r")

f2 = open("task5_train85.json", "w")
f3 = open("task5_valid15.json", "w")


json_data = json.load(f)

f2_data = []
f3_data = []

for idx, story in enumerate(json_data):
    if idx < 8500:
        f2_data.append(story)
    else:
        f3_data.append(story)

json.dump(f2_data, f2)
json.dump(f3_data, f3)





f.close()
f2.close()
f3.close()
