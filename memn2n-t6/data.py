import os
import json
from collections import Counter


def read_data(fname, word2idx, cand2idx, max_words, max_sentences, test_flag):
    # stories[story_ind] = [[sentence1], [sentence2], ..., [sentenceN]]
    # questions[question_ind] = {'question': [question], 'answer': [answer], 'story_index': #, 'sentence_index': #}
    stories = dict()
    questions = dict()


    if len(word2idx) == 0:
        word2idx['<null>'] = 0


    if os.path.isfile(fname):
        with open(fname) as f:
            #lines = f.readlines()
            json_data = json.load(f)
    else:
        raise Exception("[!] Data {file} not found".format(file=fname))

    for story_idx, story in enumerate(json_data): #fix like dstc
        #add code like dstc
        dict_answer_current = {}
        dict_answer_current['dialog_id'] = story['dialog_id']


        # Determine whether the line indicates the start of a new story
        #if words[0] == '1':
        story_ind = story_idx
        sentence_ind = 0
        stories[story_ind] = []

        for utter_idx, utter in enumerate(story['utterances']):
            words = utter.split()
            max_words = max(max_words, len(words))

            # Determine whether the line is a question or not
            if utter_idx == len(story['utterances'])-1:
                is_question = True
                question_ind = len(questions)
                questions[question_ind] = {'question': [], 'answer': {}, 'cand': [], 'story_index': story_ind, 'dialog_id': story['dialog_id'], 'sentence_index': sentence_ind}

                for  c in story['candidates']:
                    word_tok = c['utterance'].split()
                    max_words = max(max_words, len(word_tok))
            else:
                is_question = False
                sentence_ind = len(stories[story_ind])

            # Parse and append the words to appropriate dictionary / Expand word2idx dictionary
            sentence_list = []
            for k in range(0, len(words)):
                w = words[k].lower()

                # Remove punctuation
                if ('.' in w) or ('?' in w):
                    w = w[:-1]

                # Add new word to dictionary
                if w not in word2idx:
                    word2idx[w] = len(word2idx)

                # Append sentence to story dict if not question
                if not is_question:
                    sentence_list.append(w)

                    if k == len(words)-1:
                        stories[story_ind].append(sentence_list)
                        break

                # Append sentence and answer to question dict if question
                else:
                    sentence_list.append(w)

                    #dstc answer cand
                    if k == len(words)-1:
                        for cand_idx, cand in enumerate(story['candidates']):
                            add_cand = cand['utterance']
                            if add_cand not in cand2idx:
                                cand2idx[add_cand] = len(cand2idx)

                            answer = cand['utterance']
                            answer_words = answer.lower().split()  #split or raw
                            #cand['utterance'] = answer_words
                            for answer_word in answer_words:
                                if answer_word not in word2idx:
                                    word2idx[answer_word] = len(word2idx)
                        questions[question_ind]['cand'] = story['candidates']
                        questions[question_ind]['question'].extend(sentence_list)
                        if test_flag == False:
                            questions[question_ind]['answer'] = story['answer']
                            questions[question_ind]['answer']['utterance'] = story['answer']['utterance']
                            break

                    #origin
                    #if '?' in words[k]:
                    #    answer = words[k + 1].lower()

                    #    if answer not in word2idx:
                    #        word2idx[answer] = len(word2idx)

                    #    questions[question_ind]['question'].extend(sentence_list)
                    #    questions[question_ind]['answer'].append(answer)
                    #    break

            # Update max_sentences
            max_sentences = max(max_sentences, sentence_ind+1)


    # Convert the words into indices
    for idx, context in stories.items():
        for i in range(len(context)):
            temp = list(map(word2idx.get, context[i]))
            context[i] = temp

    for idx, value in questions.items():
        temp1 = list(map(word2idx.get, value['question']))
        value['question'] = temp1

        if test_flag == False:
            #print(value['answer']['utterance'])
            temp2 = cand2idx.get(value['answer']['utterance'])
            value['answer']['utterance'] = temp2
            #print(temp2)
            #print(value['answer']['utterance'])

        for val in value['cand']:
            temp3 = cand2idx.get(val['utterance'])
            val['utterance'] = temp3

    return stories, questions, max_words, max_sentences


def pad_data(stories, questions, max_words, max_sentences, test_flag):

    # Pad the context into same size with '<null>'
    for idx, context in stories.items():
        for sentence in context:
            while len(sentence) < max_words:
                sentence.append(0)
        while len(context) < max_sentences:
            context.append([0] * max_words)

    # Pad the question into same size with '<null>'
    for idx, value in questions.items():
        while len(value['question']) < max_words:
            value['question'].append(0)

        # Pad the cands, answer into same size with '<null>'
        #if test_flag == False:
        #    while len(value['answer']['utterance']) < max_words:
        #        value['answer']['utterance'].append(0)
        #for c in value['cand']:
        #    while len(c['utterance']) < max_words:
        #        c['utterance'].append(0)


def depad_data(stories, questions):

    for idx, context in stories.items():
        for i in range(len(context)):
            if 0 in context[i]:
                if context[i][0] == 0:
                    temp = context[:i]
                    context = temp
                    break
                else:
                    index = context[i].index(0)
                    context[i] = context[i][:index]

    for idx, value in questions.items():
        if 0 in value['question']:
            index = value['question'].index(0)
            value['question'] = value['question'][:index]
            #for c in value['cand']:
            #    cand = c['utterance']
            #    for i in range(len(cand)):
            #        if 0 in cand:
            #            if cand[0] == 0:
            #                break
            #            else:
            #                index = cand.index(0)
            #                cand = cand[:index]

