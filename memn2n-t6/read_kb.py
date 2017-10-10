
import numpy as np
import json
import re
import pprint
import copy

class read_kb :
    def __init__(self):
        self.kb_keys_order = ['R_phone', 'R_address', 'R_name', 'R_location', 'R_price', 'R_rating', 'R_cuisine',
                         'R_atmosphere', 'R_restrictions', 'R_number']

        self.kb_dic = {}
        self.read_from_file("../data/dataset-E2E-goal-oriented-test-v1.0/extendedkb1.txt")
        self.read_from_file("../data/dataset-E2E-goal-oriented-test-v1.0/extendedkb2.txt")

    def read_from_file(self, kb_file):
        f = open(kb_file, 'r')
        kb_list = f.readlines()
        f.close()

        for kb in kb_list:
            kb_s = re.split("\s", kb.strip())

            if self.kb_dic.get('R_name') == None:
                self.kb_dic['R_name'] = set()
                self.kb_dic['R_name'].add(kb_s[1])
            else:
                self.kb_dic['R_name'].add(kb_s[1])

            if self.kb_dic.get(kb_s[2]) == None:
                self.kb_dic[kb_s[2]] = set()
                self.kb_dic[kb_s[2]].add(kb_s[3])
            else:
                self.kb_dic[kb_s[2]].add(kb_s[3])

    def convert_kb_match(self, utterance, type=0):
        for kb_key in self.kb_keys_order:
            for kb_value in self.kb_dic[kb_key]:
                if type == 0 :
                    utterance = utterance.replace(kb_value, '<' + kb_key + '>')
                elif type == 1 :
                    utterance = utterance.replace(kb_value, '<' + kb_key + '="' + kb_value + '">')
                elif type == 2 :
                    utterance = utterance.replace(kb_value, '<' + kb_key + '>' + kb_value + '</' + kb_key + '>')

        return utterance

if __name__ == '__main__':

    inputtaskfile = "../data/dataset-E2E-goal-oriented/dialog-task1API-kb1_atmosphere-distr0.5-trn10000.json"
    # inputtaskfile = "../data/dataset-E2E-goal-oriented/dialog-task2REFINE-kb1_atmosphere-distr0.5-trn10000.json"
    # inputtaskfile = "../data/dataset-E2E-goal-oriented/dialog-task3OPTIONS-kb1_atmosphere-distr0.5-trn10000.json"
    # inputtaskfile = "../data/dataset-E2E-goal-oriented/dialog-task4INFOS-kb1_atmosphere-distr0.5-trn10000.json"
    # inputtaskfile = "../data/dataset-E2E-goal-oriented/dialog-task5FULL-kb1_atmosphere-distr0.5-trn10000.json"

    read_kb = read_kb()

    fd = open(inputtaskfile, 'r')
    json_data = json.load(fd)
    fd.close()

    print("KB Key size :", len(read_kb.kb_dic))
    print("KB Keys :", read_kb.kb_dic.keys())
    print("KB Keys Order :", read_kb.kb_keys_order)

    utterance = "i'd like to book a table in a expensive price range with french cuisine for six people with a business atmosphere"
    print("utterance  :", utterance)
    print("utter_conv :", read_kb.convert_kb_match(utterance, 1))

    for idx, story in enumerate(json_data):
        # print("Story :")
        # pprint.pprint(story)
        # story['dialog_id']
        utterances = json.loads(read_kb.convert_kb_match(json.dumps(story['utterances'])))

        candidates = list()
        for candidate in story['candidates'] :
            candidate['utterance'] = read_kb.convert_kb_match(candidate['utterance'])
            candidates.append(candidate)

        json_data[idx]['utterances'] = utterances
        json_data[idx]['candidates'] = candidates

        # print("utterances :", utterances)
        # print("candidates :", candidates)

        if (story.get('answer') != None):
            story['answer']['candidate_id']
            json_data[idx]['answer']['utterance'] = read_kb.convert_kb_match(story['answer']['utterance'])

    with open("out_task1.json", "w") as f :
        f.write(json.dumps(json_data))


