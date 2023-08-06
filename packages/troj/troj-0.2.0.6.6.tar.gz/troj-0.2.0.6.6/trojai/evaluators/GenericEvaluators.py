import torch
import numpy as np
import pandas as pd


def dict_tensors_to_list(tensor_dict):
    '''
    Converts any Pytorch tensors in a dictionary into lists.
    :param tensor_dict: A dictionary which contains tensors.
    :return: A dictionary where tensors have been converted to lists.
    '''
    new_dict = {}
    for key in list(tensor_dict.keys()):
        key_vals = tensor_dict[key]
        if isinstance(key_vals, torch.Tensor):
            key_vals = key_vals.detach().cpu().numpy().tolist()
        new_dict[key] = key_vals
    return new_dict


def get_perts(sample, adversarial):
    '''
    Gets adversarial perturbations on samples for generic mdoels.
    :param sample: A sample.
    :param adversarial: A perturbed sample.
    :return: A dictionary containing the $L^\infty$-norm and the $L^2$ norm.
    '''
    if isinstance(sample, torch.Tensor):
        sample = sample.detach().cpu().numpy()
        adversarial = adversarial.detach().cpu().numpy()
    reshaped = np.reshape(sample-adversarial, -1)
    linf_diff = np.linalg.norm(reshaped, np.inf)
    l2_diff = np.linalg.norm(reshaped, 2)
    linf_diff = linf_diff.tolist()
    return {'l2_pert':l2_diff, 'linf_pert':linf_diff}


def generic_output_parser(preds, adv_preds, loss_dicts, samples, adversarial_samples):
    '''
    A generic parser for generating results from generic models.
    :param preds: A batch of predictions.
    :param adv_preds: A batch of adversarial predictions.
    :param loss_dicts: A list of loss dictionaries.
    :param samples: A batch of samples.
    :param adversarial_samples: A batch of adversarial samples.
    :return: A list of dictionaries which contains the concatenated information from the predictions,
     adversarial predictions, the losses, and the perturbation in both the $L^2$ and $L^\infty$-norm.
    '''
    dict_list = []
    for idx in range(len(preds)):
        sample_preds = dict_tensors_to_list(preds[idx]),
        sample_adv_preds = dict_tensors_to_list(adv_preds[idx])
        pert = get_perts(samples[idx], adversarial_samples[idx])
        parsed_dict = {**sample_preds[0], **sample_adv_preds, **loss_dicts[idx], **pert}
        dict_list.append(parsed_dict)
    return dict_list


class GenericAttackCallback:
    def __init__(self, attack, use_preds=True, output_parser=generic_output_parser):
        '''
        A class used for making the callbacks to run evaluations.
        :param attack: A generic attack instance.
        :param use_preds: Whether to use the labels or the model predictions for performing the attacks.
        :param output_parser: An output parsing function.
        '''
        self.attack = attack
        self.model = attack.model
        self.use_preds = use_preds
        #output parser is an optional argument which takes in the original predictions, the adversarial predictions
        #the loss dictionaries, the samples, and the adversarial samples
        self.output_parser = output_parser


    def run_on_batch(self, data, target, index, **parser_kwargs):
        '''
        Runs the callback on a batch from a generic batch iterator.
        :param data: Input data, which is a list containing datapoints (i.e Pytorch tensors).
        :param target: The annotations for the samples. This is a list of dictionaries, where the dictionaries contain the targets.
        :param index: The indices of the datapoints in the dataframe.
        :param parser_kwargs: Any keyword arguments to be passed to the parsing function.
        :return: A dictionary containing dataframe column names as keys, where the values are lists which contain the row
        values. i.e {'loss':[0.1, 0.77], 'predictions':[0,0]}
        '''
        preds = self.model.predict(data)
        if self.use_preds:
            target = preds
        adversarial_x, loss_dicts = self.attack.generate(data, target)
        adversarial_preds = self.model.predict(adversarial_x)
        parsed = self.output_parser(preds, adversarial_preds, loss_dicts, data, adversarial_x, **parser_kwargs)
        transpose_parsed = pd.DataFrame(parsed).to_dict(orient="list")
        return transpose_parsed, index