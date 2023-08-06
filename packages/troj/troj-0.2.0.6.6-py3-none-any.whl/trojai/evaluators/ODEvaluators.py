from trojai.data import log_to_dataframe
from trojai.attacks.attack_utils import check_flip, get_class_ap, nms_pred_reduce
from trojai.metrics.metric_utils import get_pred_data
import trojai.estimators
import trojai.data
import trojai.attacks.attack_utils
import trojai.attacks.GradientBasedODAttacks
import trojai.evaluators
import torch
import numpy as np
from ..evaluators import RobustnessEvaluatorBase


#TODO document
class OD_FGSM_callback:
    def __init__(self, model, epsilon, alpha, num_iter):
        '''
        A callback to run FGSM on object detectors using the generic evaluator base class

        :param model: an instance of a PytorchObjectDetector object.
        :param epsilon: Maximum allowable perturbation.
        :param alpha: Step size
        :param num_iter: Number of steps
        '''
        self.attacker = trojai.attacks.GradientBasedODAttacks.FGSMObjectDetection(model, epsilon, alpha, num_iter)
        self.model = model
        self.keys = ['boxes', 'labels', 'scores']
        self.new_keys = ['pred_boxes', 'pred_labels', 'pred_scores']
        self.new_keys_adver = ['adversarial_boxes', 'adversarial_labels', 'adversarial_scores']

    def evaluate_batch(self, data, target, index):
        '''
        :param data: Input data.
        :param target: Targets to predict.
        :param index: Dataframe indices.
        :return: dataframe indices, and associated predictions.
        '''
        #returning losses works here since by default the attack operates on individual images
        adv_data, losses = self.attacker.generate(data, target)
        predictions = self.model.predict(data)
        formatted_adversarial_predictions = {}
        if len(adv_data)>0:
            adversarial_predictions = self.model.predict(adv_data)
            formatted_adversarial_predictions = trojai.estimators.PytorchObjectDetector.ODPredsFormatting(adversarial_predictions,
                                                                                                    self.keys,
                                                                                                    self.new_keys_adver)
        formatted_predictions = trojai.estimators.PytorchObjectDetector.ODPredsFormatting(predictions, self.keys,
                                                                                    self.new_keys)

        merged = {**formatted_predictions, **formatted_adversarial_predictions}
        return index, merged


class ODPredictionsCallback:
    def __init__(self, model, return_loss=False):
        '''
        A callback for simply making predictions on an object detection dataset.
        :param model: an instance of a PytorchObjectDetector object.
        :param return_loss: Method not yet implemented.
        '''
        #TODO option for logging individual loss components if we can get losses per sample
        self.model = model
        self.keys = ['boxes', 'labels', 'scores']
        self.new_keys = ['pred_boxes', 'pred_labels', 'pred_scores']
        self.return_loss = return_loss

    def evaluate_batch(self, data, target, index):
        '''
        :param data: Input data.
        :param target: Targets to predict.
        :param index: Dataframe indices.
        :return: dataframe indices, and associated predictions.
        '''
        #TODO add method for returning loss
        predictions  = self.model.predict(data)
        formatted_predictions = trojai.estimators.PytorchObjectDetector.ODPredsFormatting(predictions, self.keys,
                                                                                    self.new_keys)
        return formatted_predictions

def OD_vanilla_evaluator(model):
    '''
    Makes an evaluator for getting predictions on an object detection dataset.
    :param model: an instance of a PytorchObjectDetector object.
    :return: An evaluator object.
    '''
    call = ODPredictionsCallback(model)
    evaluator = RobustnessEvaluatorBase(None, [call.evaluate_batch], [{}])
    return evaluator

def OD_FGSM_evaluator(model, epsilon, alpha, num_iter):
    '''
    :param model: an instance of a PytorchObjectDetector object.
    :param epsilon: Maximum allowable perturbation.
    :param alpha: Step size
    :param num_iter: Number of steps
    :returns: Returns an evaluator object which runs the FGSM attack against an OD model.
    '''
    call = OD_FGSM_callback(model, epsilon, alpha, num_iter)
    evaluator = RobustnessEvaluatorBase(None, [call.evaluate_batch], [{}])
    return evaluator
