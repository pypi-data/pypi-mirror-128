from trojai.metrics import NLPMetrics
import spacy
import numpy as np


def parse_result(result, idx, class_map=None, stats_func=None, include_original=False, wmd=None, **dict_kwargs):
    #TODO add optional input for calssification mapping
    '''
    set include_original to true if building the dataframe from the run, useful for instance when using a predefined dataset
    '''
    goal_map = {0:'Succeed', 1:'Fail', 2:'Skip', 3:'Skip'}
    unproc_original_result = result.original_result
    unproc_perturbed_result = result.perturbed_result

    original_text_object = unproc_original_result.attacked_text
    perturbed_text_object = unproc_perturbed_result.attacked_text

    original_id = idx
    original_sentence_length = original_text_object.num_words
    original_sentence = original_text_object.text
    perturbed_sentence = perturbed_text_object.text
    goal_status = goal_map[unproc_perturbed_result.goal_status]

    ground_truth = unproc_original_result.ground_truth_output
    original_pred = unproc_original_result.output
    perturbed_pred = unproc_perturbed_result.output
    original_probs = unproc_original_result.raw_output
    pert_probs = unproc_perturbed_result.raw_output
    num_query = unproc_perturbed_result.num_queries

    if class_map is not None:
        ground_truth = class_map[ground_truth]
        original_pred = class_map[original_pred]
        perturbed_pred = class_map[perturbed_pred]

    base_dict = {'perturbed_sentence':perturbed_sentence, 'goal_status':goal_status, 'num_queries':num_query, 'ground_truth':ground_truth,
                 'original_prediction':original_pred, 'perturbed_pred':perturbed_pred,
                 'probabilites':original_probs, 'perturbed_probabilites':pert_probs, 'sentence_length':original_sentence_length,
                 'dataset_id':original_id,}
    if stats_func != None:
        stats_dict = stats_func(result, wmd)
        base_dict = {**base_dict, **stats_dict, **dict_kwargs}
    if include_original:
        orig_dict = {'input_sentence':original_sentence}
        base_dict = {**orig_dict, **base_dict}
    return base_dict

class DefStatsFunc:
    def __init__(self, spacy_model_name = "en_core_web_sm"):
        self.nlp = spacy.load(spacy_model_name)

    def stats_func_default(self, result, wmd=None):



        out_dict = {}
        unproc_original_result = result.original_result
        unproc_perturbed_result = result.perturbed_result

        original_text_object = unproc_original_result.attacked_text
        perturbed_text_object = unproc_perturbed_result.attacked_text

        original_sentence = original_text_object.text
        perturbed_sentence = perturbed_text_object.text

        spcy_orig = self.nlp(original_sentence)
        spcy_pert = self.nlp(perturbed_sentence)

        num_stopwords = NLPMetrics.count_stopwords(original_sentence)
        num_nonstop = NLPMetrics.count_non_stopwords(original_sentence)
        out_dict['%_stopwords'] = num_stopwords
        out_dict['%_non-stopwords'] = num_nonstop

        percent_words_different, swapped = NLPMetrics.percent_swapped(original_sentence, perturbed_sentence)
        percent_nonstopwords_different, _ = NLPMetrics.percent_swapped(original_sentence, perturbed_sentence,
                                                                             remove_stop=True)
        swapped_lev = NLPMetrics.swapped_lev_dist(swapped)
        out_dict['%_changed_words'] = percent_words_different
        out_dict['%_changed_non-stopwords'] = percent_nonstopwords_different
        out_dict['swapped'] = swapped
        out_dict['swapped_levenshtein_distance'] = swapped_lev
        out_dict['mean_swapped_levenshtein_distance'] = np.mean(swapped_lev)
        out_dict['sentence_levenshtein_distance'] = NLPMetrics.levenshteinDistance(original_sentence, perturbed_sentence)

        original_tagged = NLPMetrics.tagger(spcy_orig)
        perturbed_tagged = NLPMetrics.tagger(spcy_pert)
        out_dict['original_tagged'] = original_tagged
        out_dict['perturbed_tagged'] = perturbed_tagged

        #orig_oovs = NLPMetrics.get_w2v_oov_words(spcy_orig)
        #pert_oovs = NLPMetrics.get_w2v_oov_words(spcy_pert)
        #out_dict['out_of_w2v_voc_inp_tokens'] = orig_oovs
        #out_dict['out_of_w2v_voc_pert_tokens'] = pert_oovs
        #out_dict['%_oov_inp'] = len(orig_oovs)/len(spcy_orig)
        #out_dict['%_oov_pert'] = len(pert_oovs)/len(spcy_pert)

        char_count = NLPMetrics.word_based_character_count(original_sentence)
        out_dict['word-based_character_count'] = char_count

        if wmd != None:
            dist = wmd.distance(original_sentence, perturbed_sentence)
            out_dict['Word_Mover_distance'] = dist
        return out_dict


