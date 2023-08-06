from art import estimators
import tensorflow as tf
import numpy as np


"""
TODO: This is our new base class, it inherits from art estimators. 
We'll have a class for major frameworks that will inherit this class

"""


class TrojClassifier(object):
    def get_classifier_meta(self):
        return {
            "model": str(self._model),
            "model_name": str(self._model.__class__.__name__),
            "input_shape": str(self._input_shape),
            "num_classes": str(self.nb_classes),
            "loss_func": str(self._loss),
            "channels_first": str(self._channels_first),
        }


class TensorFlowV1TrojClassifier(object):
    def __init__(self, *args):
        super(TrojClassifier, self).__init__(*args)


class TrojKerasClassifier(estimators.classification.KerasClassifier, TrojClassifier):
    import tensorflow as tf
    import tensorflow.keras.losses

    tf.compat.v1.disable_eager_execution()

    def ComputeLoss(
        self, x, y, return_preds=True, reduction=tf.keras.losses.Reduction.NONE
    ):
        print("loss fn")
        print(self.model.loss)
        print(self)
        old_reduction = self.model.loss_functions[0]._get_reduction()
        self.model.loss_functions[0].reduction = reduction
        preds = self.predict(x)
        # hard_labels = np.argmax(preds, axis=1)
        # hard_labels_dtype = 'float32'
        # y = y.astype(hard_labels_dtype)
        loss_val = self.model.loss_functions[0](y, preds)
        self._loss.reduction = old_reduction
        # tf.compat.v1.enable_eager_execution()
        if return_preds:

            return loss_val.eval(session=tf.compat.v1.Session()), preds
        else:
            return loss_val.numpy()


class TrojPytorchClassifier(
    estimators.classification.PyTorchClassifier, TrojClassifier
):
    def ComputeLoss(self, x, y, return_preds=True, reduction="none"):
        import torch

        old_reduction = self._loss.reduction
        self._loss.reduction = reduction
        preds = torch.tensor(self.predict(x))
        y = torch.tensor(y)
        loss_val = self._loss(preds, y)
        self._loss.reduction = old_reduction
        if return_preds:
            return loss_val.numpy(), preds.numpy()
        else:
            return loss_val.numpy()
