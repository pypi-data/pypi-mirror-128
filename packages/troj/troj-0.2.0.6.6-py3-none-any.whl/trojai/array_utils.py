import numpy as np
import copy


def true_min_pert(labels, preds, original, perturbation, losses, norm=np.inf):
    '''
    Finds the smallest perturbation which flips the label. If no perturbation is found, sets the minimum to 0.5 (since
    the image will become entirely grey at such a perturbation).

    :param original_ims: Original inputs
    :param outs_array: Adversarial examples
    :param losses: Adversarial losses
    :param preds: Predictions on Adversarial Examples
    :param norm: the L^p norm to use.
    :return: minimum perturbation, the loss for the perturbation, and the prediction
    '''


    tile_list = [original for i in range(perturbation.shape[1])]
    tiled = np.stack(tile_list)
    # swap the first and second axis
    tiled = np.swapaxes(tiled, 0, 1)
    if tiled.shape[1] != 1:
        assert tiled[0, 0, 0, 0, 0] == tiled[0, 1, 0, 0, 0]

    # reshape outputs and original images to collection of vectors
    flattened_shape = (
        perturbation.shape[0],
        perturbation.shape[1],
        perturbation.shape[2] * perturbation.shape[3] * perturbation.shape[4],
    )
    flattened_outs = np.reshape(perturbation, flattened_shape)
    flattened_original = np.reshape(tiled, flattened_shape)

    # subtract the original from the perturbed to get the perturbation vector
    perturbations = flattened_outs - flattened_original
    perturbation_norms = np.linalg.norm(perturbations, norm, axis=2)

    tiled_labels = [labels for i in range(preds.shape[1])]
    tiled_labels = np.stack(tiled_labels)
    # swap the first and second axis
    tiled_labels = np.swapaxes(tiled_labels, 0, 1)
    #If the label isn't flipped, set min pert to 0.5
    perturbation_norms[tiled_labels==np.argmax(preds, axis=2)] = 0.5
    min_per_sample_idx = np.argmin(perturbation_norms, axis=1)

    min_pert_losses = []
    min_pert_preds = []
    min_pert_outs = []
    for idx in range(len(min_per_sample_idx)):
        min_pert_outs.append(perturbation[idx, min_per_sample_idx[idx]])
        min_pert_losses.append(losses[idx, min_per_sample_idx[idx]])
        min_pert_preds.append(preds[idx, min_per_sample_idx[idx]])

    min_pert_outs = np.asarray(min_pert_outs)
    min_pert_preds = np.asarray(min_pert_preds)
    min_pert_losses = np.asarray(min_pert_losses)
    return min_pert_outs, min_pert_preds, min_pert_losses


def compute_Lp_distance(x1, x2, p=np.inf):
    '''
    compute Lp distance of a collection of images against another collection.

    :param x1: image collection 1
    :param x2: image collection 2
    :param p: p norm
    :return: tensor of distances
    '''
    x1 = np.reshape(x1, (x1.shape[0], -1))
    x2 = np.reshape(x2, (x2.shape[0], -1))
    difference_vect = x1 - x2
    lp_distance = np.linalg.norm(difference_vect, p, axis=1)
    return lp_distance
