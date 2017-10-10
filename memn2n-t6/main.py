import os

import pprint
import tensorflow as tf
import numpy as np
import json
from data import read_data, pad_data, depad_data
from model import MemN2N

pp = pprint.PrettyPrinter()

flags = tf.app.flags

flags.DEFINE_integer("edim", 20, "internal state dimension [20]")
flags.DEFINE_integer("nhop", 3, "number of hops [3]")
flags.DEFINE_integer("mem_size", 100, "maximum number of sentences that can be encoded into memory [50]")
flags.DEFINE_integer("batch_size", 32, "batch size to use during training [32]")
flags.DEFINE_integer("nepoch", 100, "number of epoch to use during training [100]")
flags.DEFINE_integer("anneal_epoch", 25, "anneal the learning rate every <anneal_epoch> epochs [25]")
flags.DEFINE_integer("babi_task", 1, "index of bAbI task for the network to learn [1]")
flags.DEFINE_float("init_lr", 0.01, "initial learning rate [0.01]")
flags.DEFINE_float("anneal_rate", 0.5, "learning rate annealing rate [0.5]")
flags.DEFINE_float("init_mean", 0., "weight initialization mean [0.]")
flags.DEFINE_float("init_std", 0.1, "weight initialization std [0.1]")
flags.DEFINE_float("max_grad_norm", 40, "clip gradients to this norm [40]")
flags.DEFINE_string("data_dir", "./bAbI/en-valid", "dataset directory [./bAbI/en_valid]")
flags.DEFINE_string("checkpoint_dir", "./checkpoints", "checkpoint directory [./checkpoints]")
flags.DEFINE_boolean("lin_start", True, "True for linear start training, False for otherwise [False]")
flags.DEFINE_boolean("is_test", False, "True for testing, False for training [False]")
flags.DEFINE_boolean("show_progress", False, "print progress [False]")
flags.DEFINE_boolean("D_layer", True, "True for adding D_layer")

FLAGS = flags.FLAGS


def main(_):
    word2idx = {}
    cand2idx = {}
    max_words = 0
    max_sentences = 0

    if not os.path.exists(FLAGS.checkpoint_dir):
        os.makedirs(FLAGS.checkpoint_dir)

    train_stories, train_questions, max_words, max_sentences = read_data('dstc/out_task4_train85.json', word2idx, cand2idx, max_words, max_sentences, test_flag=False)
    valid_stories, valid_questions, max_words, max_sentences = read_data('dstc/out_task4_valid15.json', word2idx, cand2idx, max_words, max_sentences, test_flag=False)
    test_stories, test_questions, max_words, max_sentences = read_data('dstc/out_dialog-task4INFOS-kb2_atmosphere_restrictions-distr0.5-tst1000.json', word2idx, cand2idx, max_words, max_sentences, test_flag=True)

    pad_data(train_stories, train_questions, max_words, max_sentences, test_flag=False)
    pad_data(valid_stories, valid_questions, max_words, max_sentences, test_flag=False)
    pad_data(test_stories, test_questions, max_words, max_sentences, test_flag=True)

    idx2word = dict(zip(word2idx.values(), word2idx.keys()))
    idx2cand = dict(zip(cand2idx.values(), cand2idx.keys()))
    FLAGS.nwords = len(word2idx)
    FLAGS.ncands = len(cand2idx)
    FLAGS.max_words = max_words
    FLAGS.max_sentences = max_sentences

    pp.pprint(flags.FLAGS.__flags)

    with tf.Session() as sess:
        model = MemN2N(FLAGS, sess)
        model.build_model()

        if FLAGS.is_test:
            model.run(valid_stories, valid_questions, test_stories, test_questions, idx2cand, answer_flag = False)
        else:
            model.run(train_stories, train_questions, valid_stories, valid_questions, idx2cand, answer_flag = True)

        prediction_test_valid = 0

        if prediction_test_valid == 1:
            predictions, target = model.predict(valid_stories, valid_questions)

            correct_num = 0
            #print(len(valid_questions))
            for i in range(len(valid_questions)):
                index = i
                #depad_data(valid_stories, valid_questions)

                #question = valid_questions[index]['question']
                answer = valid_questions[index]['answer']['utterance']
                cand = valid_questions[index]['cand']
                #story_index = valid_questions[index]['story_index']
                #sentence_index = valid_questions[index]['sentence_index']

                #story = valid_stories[story_index][:sentence_index + 1]

                #story = [list(map(idx2word.get, sentence)) for sentence in story]
                #question = list(map(idx2word.get, question))
                #prediction = idx2cand[np.argmax(predictions[index])]
                pred_sorted = np.argsort(predictions[index][-FLAGS.ncands:])
                pred_sorted = pred_sorted[::-1]
                cand_list = []
                prediction = None
                for c in cand:
                    cand_list.append(idx2cand.get(c['utterance']))
                for pred in pred_sorted:
                    if idx2cand[pred] in cand_list:
                        prediction = idx2cand[pred]
                        break
                answer = idx2cand.get(answer)

                #print('Story:')
                #pp.pprint(story)
                #print('\nQuestion:')
                #pp.pprint(question)
                #print('\nPrediction:')
                #pp.pprint(prediction)
                #print('\nAnswer:')
                #pp.pprint(answer)
                #print('\ncandidates')
                #pp.pprint(cand_list)
                #print('\nCorrect:')
                #pp.pprint(prediction == answer)
                if prediction == answer:
                    correct_num += 1
            print('case: '+str(len(valid_questions))+ '  correct_num: '+ str(correct_num))
            print('acc - ' + str(correct_num/len(valid_questions)*100))
        else:
            predictions, target = model.predict(test_stories, test_questions)

            correct_num = 0
            #print(len(valid_questions))
            responses = []
            for i in range(len(test_questions)):
                index = i
                dict_answer_current = {}
                dict_answer_current['dialog_id'] = test_questions[index]['dialog_id']
                candidate_rank = []
                #depad_data(valid_stories, valid_questions)

                #question = valid_questions[index]['question']
                #answer = test_questions[index]['answer']['utterance']
                cand = test_questions[index]['cand']
                #story_index = valid_questions[index]['story_index']
                #sentence_index = valid_questions[index]['sentence_index']

                #story = valid_stories[story_index][:sentence_index + 1]

                #story = [list(map(idx2word.get, sentence)) for sentence in story]
                #question = list(map(idx2word.get, question))
                #prediction = idx2cand[np.argmax(predictions[index])]
                pred_sorted = np.argsort(predictions[index][-FLAGS.ncands:])
                pred_sorted = pred_sorted[::-1]
                cand_list = []
                prediction = None
                for c in cand:
                    cand_list.append(idx2cand.get(c['utterance']))
                crank = 1
                flag = 0
                for pred in pred_sorted:
                    if idx2cand[pred] in cand_list:
                        if flag == 0:
                            prediction = idx2cand[pred]
                            flag = 1
                        for c in cand:
                            if c['utterance'] == pred:
                                #print(idx2cand.get(c['utterance']))
                                candidate_rank.append({"candidate_id": c['candidate_id'], "rank": crank})
                                crank = crank + 1
                                if crank == 11:
                                    break
                        if crank == 11:
                            break
                dict_answer_current['lst_candidate_id'] = candidate_rank
                responses.append(dict_answer_current)
                #answer = idx2cand.get(answer)

                #print('Story:')
                #pp.pprint(story)
                #print('\nQuestion:')
                #pp.pprint(question)
                #print('\nPrediction:')
                #pp.pprint(prediction)
                #print('\nAnswer:')
                #pp.pprint(answer)
                #print('\ncandidates')
                #pp.pprint(cand_list)
                #print('\nCorrect:')
                #pp.pprint(prediction == answer)
                #if prediction == answer:
                #    correct_num += 1
            fdout = open("dialog-task4INFOS-kb2_atmosphere_restrictions-distr0.5-tst1000.answer.json", "w")
            json.dump(responses, fdout)
            fdout.close()
            #print('case: '+str(len(test_questions))+ '  correct_num: '+ str(correct_num))
            #print('acc - ' + str(correct_num/len(test_questions)*100))


if __name__ == '__main__':
    tf.app.run()
