import json




f2 = open("taskall_train85.json", "r")
f3 = open("taskall_valid15.json", "r")


json_data = json.load(f2)
json_data2 = json.load(f3)

f2_data =[]
f3_data =[]

for idx, story in enumerate(json_data):
    for ut in story['utterances']:
        tmp = ut.lower().split()
        for u in tmp:
            f2_data.append(u)
    for ut in story['candidates']:
        tmp = ut['utterance'].lower().split()
        for u in tmp:
            f2_data.append(u)
    tmp = story['answer']['utterance'].lower().split()
    for u in tmp:
        f2_data.append(u)


for idx, story in enumerate(json_data2):
    for ut in story['utterances']:
        tmp = ut.lower().split()
        for u in tmp:
            f3_data.append(u)
    for ut in story['candidates']:
        tmp = ut['utterance'].lower().split()
        for u in tmp:
            f3_data.append(u)
    tmp = story['answer']['utterance'].lower().split()
    for u in tmp:
        f3_data.append(u)

final = list(set(f2_data) - set(f3_data))

print(len(final))



f2.close()
f3.close()
