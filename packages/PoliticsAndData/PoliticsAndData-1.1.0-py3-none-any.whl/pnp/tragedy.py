"""
Contains :py:class:`Tragedy`.
"""

import numpy as np
import pickle

rand = np.random.default_rng()


class Tragedy:
    """ """
    def __init__(self, loc="./"):
        self.file = f"{loc}weights.pkl"
        self.widths = []
        self.layers = [
            np.array([0.0]*width) for width in self.widths
        ]

        try:
            self.load()
        except IOError:
            self.init_weights(True)

    def load(self):
        """ """
        with open(self.file, "rb") as f:
            self.weights = pickle.load(f)

    def save(self):
        """ """
        with open(self.file, "wb") as f:
            pickle.dump(self.weights, f, pickle.HIGHEST_PROTOCOL)

    def init_weights(self, confirm=False):
        """

        :param confirm:  (Default value = False)

        """
        if confirm:
            self.weights = [
                rand.normal(
                    size=(self.widths[i], self.widths[i+1]),
                    loc=0,
                    scale=(2/(self.widths[i]+self.widths[i+1]))**(1/2)
                ) for i in range(0, len(self.widths)-1)
            ]
            self.save()

    def forward_prop(self):
        """ """
        for i in range(len(self.layers)):
            layer = self.layers[i]

    def back_prop(self, delta: np.ndarray):
        """

        :param delta: np.ndarray: 

        """
        for i in range(len(self.weights), -1):
            layer = self.layers[i]
            weights = self.weights[i]
