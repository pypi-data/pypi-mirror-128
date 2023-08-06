import numpy as np
import pandas as pd
from trojai.evaluators.NLP_utils import *
from trojai.data import log_to_dataframe
from textattack import AttackArgs, Attacker



class BaseNLPEvaluator:
    def __init__(self, model, dataset, attack_dict, attack_args, class_lookup=None, stats_func=None, include_original=False,
                 include_wmd = True):
        '''

        :param model:
        :param dataset:
        :param attack_dict:
        :param attack_args:
        :param class_lookup: Either None or a dictionary of the form {class_name:class_id} or {class_id:class_name}.
        :param stats_func:
        :param include_original:
        :param include_wmd:
        '''
        self.model = model
        self.dataset = dataset
        self.attack_dict = attack_dict
        self.attack_args = attack_args
        self.attackers = self.build_attackers()
        #stats_func returns a dictionary of statistics built from a result.
        self.stats_func = stats_func
        self.include_original = include_original
        if include_wmd==True:
            self.wmd = NLPMetrics.WordMoverDistance('word2vec-google-news-300')
        else:
            self.wmd = None

        if class_lookup is not None:
            if type(list(class_lookup.values())[0])!=str:
                class_lookup = {y: x for x, y in class_lookup.items()}
            self.class_lookup = class_lookup
        else:
            self.class_lookup = None

    def build_attackers(self):
        '''
        Initializes attackers to be run.
        '''
        attacker_dict = {}
        for attack in self.attack_dict.keys():
            attacker = Attacker(self.attack_dict[attack], self.dataset, self.attack_args)
            attacker_dict[attack] = attacker
        return attacker_dict

    def run(self, df=None):
        #TODO add verbose flag for progress tracking
        if df is not None:
            for attacker in self.attackers.keys():
                results_iterable = self.attackers[attacker].attack_dataset()
                for result_idx in range(len(results_iterable)):
                    result = results_iterable[result_idx]
                    parsed = parse_result(result, result_idx, self.class_lookup, self.stats_func, self.include_original, wmd=self.wmd, attack = attacker)
                    df = log_to_dataframe(df, result_idx, parsed)
        else:
            dict_list = []
            for attacker in self.attackers.keys():
                results_iterable = self.attackers[attacker].attack_dataset()
                for result_idx in range(len(results_iterable)):
                    result = results_iterable[result_idx]
                    parsed = parse_result(result, result_idx, self.class_lookup, self.stats_func, self.include_original, wmd=self.wmd, attack = attacker)
                    dict_list.append(parsed)
            df = pd.DataFrame(dict_list)
        return df
