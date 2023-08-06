import torch
from PIL import Image
import torchvision.transforms.functional as TVF
import torchvision.transforms as transforms
import numpy as np
import torch.nn as nn


class GenericFGSM:
    def __init__(self, model, epsilon, alpha, num_iter, loss_kwarg_dict={}):
        '''
        :param model: an instance of a model.
        :param epsilon: Maximum allowable perturbation.
        :param alpha: Step size
        :param num_iter: Number of steps
        '''
        #TODO allow user to pick certain losses from the model loss dictionary to maximize.
        assert hasattr(model, 'compute_loss')
        assert hasattr(model, 'predict')
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.num_iter = num_iter
        self.loss_kwarg_dict = loss_kwarg_dict

    def generate(self, X, Y, return_examples=True):
        '''
        :param X: A list of images (Pytorch tensors) to attack.
        :param Y: A list of image annotation dictionaries.
        :param return_examples: If true, returns the examples, else just returns the perturbations.
        :param return_losses: Whether or not to return the list of loss dictionaries (each dictionary contains the initial
        loss and final loss)
        :returns: A list of either adversarial examples or just the perturbations, along with the losses if return_losses=True
        '''
        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            x = X[idx]
            y = Y[idx]
            check_val = list(y.values())
            if len(check_val)>0:
                losses = {}
                init_loss = self.model.compute_loss([x], [y], grad=False)
                losses["initial_loss"] = init_loss.item()
                delta = torch.nn.init.normal_(torch.zeros_like(x, requires_grad=True), mean=0, std=0.001)
                for t in range(self.num_iter):
                    inp = [x + delta]
                    loss = self.model.compute_loss(inp, [y], grad=True, **self.loss_kwarg_dict)
                    loss.backward(retain_graph=True)
                    delta.data = (delta + x.shape[0] * self.alpha * delta.grad.data).clamp(-self.epsilon, self.epsilon)
                    delta.grad.zero_()
                losses["final_loss"] = loss.item()
                if return_examples:
                    adv_X.append(x + delta.detach())
                else:
                    adv_X.append(delta.detach())
                loss_dicts.append(losses)
        return adv_X, loss_dicts


class MomentumPGD:
    def __init__(self, model, epsilon, alpha, beta, num_iter, loss_kwarg_dict={}):
        '''
        PGD with momentum.
        :param model: an instance of a generic model.
        :param epsilon: Maximum allowable perturbation.
        :param alpha: Step size
        :param num_iter: Number of steps
        '''
        #TODO allow user to pick certain losses from the model loss dictionary to maximize.
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.beta = beta
        self.num_iter = num_iter
        self.loss_kwarg_dict = loss_kwarg_dict

    def generate(self, X, Y, return_examples=True):
        '''
        :param X: A list of images (Pytorch tensors) to attack.
        :param Y: A list of image annotation dictionaries.
        :param return_examples: If true, returns the examples, else just returns the perturbations.
        :param return_losses: Whether or not to return the list of loss dictionaries (each dictionary contains the initial
        loss and final loss)
        :returns: A list of either adversarial examples or just the perturbations, along with the losses if return_losses=True
        '''
        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            x = X[idx]
            y = Y[idx]
            check_val = list(y.values())
            if len(check_val)>0:
                losses = {}
                init_loss = self.model.compute_loss([x], [y], grad=False)
                losses["initial_loss"] = init_loss.item()
                delta = torch.nn.init.normal_(torch.zeros_like(x, requires_grad=True), mean=0, std=0.001)
                prev_delta = 0
                for t in range(self.num_iter):
                    inp = [x + delta]
                    loss = self.model.compute_loss(inp, [y], grad=True, **self.loss_kwarg_dict)
                    loss.backward()
                    delta.data = (self.beta*(delta + x.shape[0] * self.alpha * delta.grad.data)+(1-self.beta)*prev_delta).clamp(-self.epsilon, self.epsilon)
                    prev_delta = delta.grad.data
                    delta.grad.zero_()
                losses["final_loss"] = loss.item()
                if return_examples:
                    adv_X.append(x + delta.detach())
                else:
                    adv_X.append(delta.detach())
                loss_dicts.append(losses)
        return adv_X, loss_dicts


class AdaptivePGD:
    def __init__(self, model, epsilon, alpha, beta, reduction_thresh, reduction_rate, num_iter, loss_kwarg_dict={}):
        '''
        PGD with momentum and adaptive step size.

        :param model: an instance of a PytorchObjectDetector object.
        :param epsilon: Maximum allowable perturbation.
        :param alpha: Step size
        :param num_iter: Number of steps
        '''
        # TODO allow user to pick certain losses from the model loss dictionary to maximize.
        self.model = model
        self.epsilon = epsilon
        self.alpha = alpha
        self.beta = beta
        self.reduction_thresh = reduction_thresh
        self.reduction_rate = reduction_rate
        self.num_iter = num_iter
        self.loss_kwarg_dict = loss_kwarg_dict

    def generate(self, X, Y, return_examples=True):
        '''
        :param X: A list of images (Pytorch tensors) to attack.
        :param Y: A list of image annotation dictionaries.
        :param return_examples: If true, returns the examples, else just returns the perturbations.
        :param return_losses: Whether or not to return the list of loss dictionaries (each dictionary contains the initial
        loss and final loss)
        :returns: A list of either adversarial examples or just the perturbations, along with the losses if return_losses=True
        '''
        adv_X = []
        loss_dicts = []
        for idx in range(len(X)):
            x = X[idx]
            y = Y[idx]
            check_val = list(y.values())
            if len(check_val) > 0:
                losses = {}
                init_loss = self.model.compute_loss([x], [y], grad=False)
                prev_loss = init_loss
                reduct = 1
                losses["initial_loss"] = init_loss.item()
                delta = torch.nn.init.normal_(torch.zeros_like(x, requires_grad=True), mean=0, std=0.001)
                prev_delta = 0
                for t in range(self.num_iter):
                    inp = [x + delta]
                    loss = self.model.compute_loss(inp, [y], grad=True, **self.loss_kwarg_dict)
                    loss.backward()
                    delta.data = (self.beta * (delta + x.shape[0] * (self.alpha / reduct) * delta.grad.data) + (
                                1 - self.beta) * prev_delta).clamp(-self.epsilon, self.epsilon)
                    prev_delta = delta.grad.data
                    cur_loss = loss.item()
                    if cur_loss - prev_loss < self.reduction_thresh:
                        reduct = reduct * self.reduction_rate
                    delta.grad.zero_()
                losses["final_loss"] = loss.item()
                if return_examples:
                    adv_X.append(x + delta.detach())
                else:
                    adv_X.append(delta.detach())
                loss_dicts.append(losses)
        return adv_X, loss_dicts
