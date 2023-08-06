from . import TrojEpsilon
import numpy as np
# import pandas as pd
from . import array_utils
from . import attack_utils
from . import ODAttack
import torch
from . import TrojClassifier

class GenericRobustnessEvaluator:
    def __init__(
        self,
        classifier,
        attack,
        attack_name,
        attkwargs,
        use_model_preds=False
    ):
        '''
        The simple robustness evaluator class. Should be used to form a baseline.

        :param classifier: TrojClassifier/ART Classifier instance
        :param attack: undecalred ART evasion class
        :param attack_name: Name for logging
        :param **attkwargs: keyword arguments for attack.
        '''
        self.atk_meta = attkwargs
        self.classifier = classifier
        self.attacker = TrojEpsilon.LpAttack(
            self.classifier, attack, use_model_preds, **attkwargs)
        self.atk_meta['name'] = attack_name

    def attack(self, data, target, index, device=None):
        '''
        Runs the attack.

        :param data: Input data
        :param target: Target labels
        :param index: Index of samples in dataframe
        :param device: If using Pytorch, one can specify the device.
        :return: A dictionary containing the minimum perturbation, the loss, adversarial loss, prediction, and adversarial
        prediction for each sample, along with a list of indices for the logging function.
        '''

        # send data and target to cpu, convert to numpy
        data = np.ascontiguousarray(data.astype(np.float32))
        test_loss, preds = self.classifier.ComputeLoss(data, target)
        preds = np.argmax(preds, axis=1)
        adv_x, adv_preds, adv_loss = self.attacker.generate(data, target)
        # adv_loss, adv_preds = self.classifier.ComputeLoss(adv_x, target)
        perturbation = array_utils.compute_Lp_distance(data, adv_x)
        adv_pred = np.argmax(adv_preds, axis=1)
        # generate the adversarial image using the data numpy array and label numpy array
        out_dict = {
            "Linf_perts": perturbation,
            "Loss": test_loss,
            "Adversarial_Loss": adv_loss,
            "prediction": preds,
            "Adversarial_prediction": adv_pred,
        }
        return (out_dict, index)

class BasicRobustnessEvaluator:
    def __init__(
        self,
        classifier,
        eps_steps=0.01,
        batch_size=128,
        norm=np.inf,
        use_model_preds=False,
    ):
        '''
        The simple robustness evaluator class. Should be used to form a baseline.

        :param classifier: TrojClassifier/ART Classifier instance
        :param eps_steps: Epsilon step size for the attack. Smaller values are more precise but slower.
        :param batch_size: Number of images in a batch.
        :param norm: The p norm (can be int or np.inf)
        :param use_model_preds: Whether or not to use true labels or model predictions
        '''
        self.atk_meta = {'attack_name':'fgsm', "eps_steps": str(eps_steps),
             "batch_size":str(batch_size), "norm": str(norm),  "use_model_preds": str(use_model_preds)}
        self.classifier = classifier
        self.attacker = TrojEpsilon.TrojEpsAttack(
            self.classifier,
            eps_steps=eps_steps,
            batch_size=batch_size,
            norm=norm,
            use_model_preds=use_model_preds,
        )

    def attack(self, data, target, index, device=None):
        '''
        Runs the attack.

        :param data: Input data
        :param target: Target labels
        :param index: Index of samples in dataframe
        :param device: If using Pytorch, one can specify the device.
        :return: A dictionary containing the minimum perturbation, the loss, adversarial loss, prediction, and adversarial
        prediction for each sample, along with a list of indices for the logging function.
        '''

        # send data and target to cpu, convert to numpy
        data = np.ascontiguousarray(data.astype(np.float32))
        test_loss, preds = self.classifier.ComputeLoss(data, target)
        preds = np.argmax(preds, axis=1)
        adv_x, adv_preds, adv_loss = self.attacker.generate(data, target)
        # adv_loss, adv_preds = self.classifier.ComputeLoss(adv_x, target)
        perturbation = array_utils.compute_Lp_distance(data, adv_x)
        adv_pred = np.argmax(adv_preds, axis=1)
        # generate the adversarial image using the data numpy array and label numpy array
        out_dict = {
            "Linf_perts": perturbation,
            "Loss": test_loss,
            "Adversarial_Loss": adv_loss,
            "prediction": preds,
            "Adversarial_prediction": adv_pred,
        }
        return (out_dict, index)


class BlackBoxODEvaluator:
    # different run form to classification
    def __init__(
        self,
        model,
        obj_class,
        loader,
        batch_iterator,
        df=None,
        device="cuda",
        iou_thresh=0.5,
        nms_thresh=0.05,
        return_nms=False,
        use_preds=False,
        verbose=True,
        **attkwargs
    ):
        '''
        The class used for evaluating the robustness of an object detection algorithm against the simple blackbox attack.

        :param model:  Pytorch Object detection model. That is, any model which outputs predictions as a dictionary
        containing the keys [boxes, labels, scores] where boxes are the bounding boxes for
        predicted objects in the form [x,y, x+w, y+h] where w,h are the width and height of the bounding box. Labels are the
        predicted labels, and scores are the confidence of prediction, where each value is of the correct Pytorch dtype.
        :param obj_class: The class to perform the attack on.
        :param loader: Dataloader
        :param batch_iterator: Troj OD batch iterator
        :param df: Dataframe
        :param device: Deprecated
        :param iou_thresh: IOU threshold for a positive detection of an object
        :param nms_thresh: Threshold used when applying NMS.
        :param return_nms: When saving predictions to dataframe, whether or not apply NMS to the predictions first.
        :param use_preds: Whether or not to use the true annotations or annotations predicted by the model. #TODO implement
        :param verbose: Whether or not print info during attack.
        :param return_prc: Whether or not to return the precision recall curve.
        :param attkwargs: Arguments for the evolutionary attack.
        '''
        self.model = model
        self.obj_class = obj_class
        self.loader = loader
        self.batch_iterator = batch_iterator
        self.df = df
        if self.df == None:
            self.df = loader.dataframe
        self.device = device
        self.iou_thresh = iou_thresh
        self.nms_thresh = nms_thresh
        self.return_nms = return_nms
        self.use_preds = use_preds
        self.attacker = ODAttack.EvoDAttack(self.model, self.obj_class, **attkwargs)
        self.verbose = verbose

    def _save_bbox_ims(self, image, target_box, fname, out_path=""):
        print(image)
        print(image.shape)
        print(target_box)
        import torchvision.transforms as transforms
        from PIL import Image 
        import PIL 
        import os
        arr = image
        im = transforms.ToPILImage()(arr)
        
        directory = './perts/'

        if not os.path.exists(directory):
            os.makedirs(directory)
        im.save("perts/"+fname)
        

    def run(self, num_samples, save_perts=False):
        '''
        #TODO add save perturbation option here.
        Run the black box robustness evaluation on a set number of samples.

        :param num_samples: number of samples containing the attack class to run attack on.
        :return: the dataframe and the ids of the attacked samples.
        '''
        # TODO: Should the dataset task checker be in here?
        tracker = 0
        attacked_ids = []
        batch_enum = enumerate(self.batch_iterator)

        while tracker < num_samples:
            batch_id, (ims, labs, ids) = next(batch_enum)

            if tracker > 0 and batch_id == 0:
                break

            for idx in range(len(labs)):
                sample_id = ids[idx]
                data_dict = {}
                if self.use_preds==False:
                    perturb, gt, preds = self.attacker.attack(ims[idx], labs[idx])
                else:
                    perturb, gt, preds = self.attacker.attack(ims[idx], None)
                #make sure we have a ground truth object
                if gt != None:
                    #Add the perturbation to the image
                    pert_im = ims[idx] + perturb.to(self.device)
                    #get predictions on perturbed image
                    pert_preds = self.model([pert_im])[0]
                    #Apply non-maximal suppression to predictions
                    nms_pert_preds = ODAttack.nms_pred_reduce(pert_preds, self.nms_thresh)
                    nms_preds = ODAttack.nms_pred_reduce(preds, self.nms_thresh)
                    #check to see if gt object has disappeared
                    flip = ODAttack.check_flip(nms_pert_preds, gt, self.obj_class, self.iou_thresh, self.nms_thresh)
                    #Get imagewise AP for class
                    troj_ap,_ = ODAttack.get_class_ap(self.obj_class, nms_preds, labs[idx], self.iou_thresh)
                    adv_troj_ap,_ = ODAttack.get_class_ap(self.obj_class, nms_pert_preds, labs[idx], self.iou_thresh)
                    # compute perturbation norm
                    pert_vec = perturb.view(-1)
                    linf_pert = torch.norm(pert_vec, p=np.inf)
                    tracker += 1
                    if self.return_nms==True:
                        orig_boxes, orig_labels, orig_scores = attack_utils.get_pred_data(nms_preds)
                        pert_boxes, pert_labels, pert_scores = attack_utils.get_pred_data(nms_pert_preds)
                    else:
                        orig_boxes, orig_labels, orig_scores = attack_utils.get_pred_data(preds)
                        pert_boxes, pert_labels, pert_scores = attack_utils.get_pred_data(pert_preds)
                    gt_boxes = gt['boxes'].detach().cpu().numpy()
                    data_dict = {
                            "flip": flip,
                            "TmAP": troj_ap.item(),
                            "Adv_TmAP": adv_troj_ap.item(),
                            "Linf": linf_pert.item(),}
                    '''
                            "iou_thresh":self.iou_thresh,
                            "nms_thresh":self.nms_thresh,
                            'pred_boxes':orig_boxes,
                            'pred_labels': orig_labels,
                            'pred_scores': orig_scores,
                            'adversarial_boxes': pert_boxes,
                            'adversarial_labels': pert_labels,
                            'adversarial_scores': pert_scores,
                            'gt_box':gt_boxes
                        
                        }
                    '''
                    self.df = attack_utils.log_to_dataframe(self.df, sample_id, data_dict)
                    attacked_ids.append(sample_id)
                    if save_perts:    
                        #TODO save perturbation
                        self._save_bbox_ims(pert_im, gt_boxes, self.df["file_name"][sample_id])
            return self.df, attacked_ids
