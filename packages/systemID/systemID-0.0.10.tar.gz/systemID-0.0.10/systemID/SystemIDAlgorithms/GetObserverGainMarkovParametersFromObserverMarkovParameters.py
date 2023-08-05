"""
Author: Damien GUEHO
Copyright: Copyright (C) 2021 Damien GUEHO
License: Public Domain
Version: 20
Date: November 2021
Python: 3.7.7
"""


import numpy as np


def getObserverGainMarkovParametersFromObserverMarkovParameters(observer_markov_parameters, **kwargs):

    # Dimensions
    output_dimension, input_dimension = observer_markov_parameters[0].shape

    # Number of observer Markov parameters
    number_observer_markov_parameters = len(observer_markov_parameters)
    number_of_parameters = min(kwargs.get('number_of_parameters', number_observer_markov_parameters), number_observer_markov_parameters)

    # Extract hk1 and hk2
    hk1 = ['NaN']
    hk2 = ['NaN']
    for i in range(1, min(number_observer_markov_parameters, number_of_parameters)):
        hk1.append(observer_markov_parameters[i][:, 0:input_dimension])
        hk2.append(-observer_markov_parameters[i][:, input_dimension:output_dimension + input_dimension])

    # First observer Markov parameter
    observer_gain_markov_parameters = ['NaN', hk2[1]]

    # Get hk
    for i in range(2, number_of_parameters):
        if i < number_observer_markov_parameters:
            hk = hk2[i]
            for j in range(1, i):
                hk = hk - np.matmul(hk2[j], observer_gain_markov_parameters[i - j])
            observer_gain_markov_parameters.append(hk)
        else:
            hk = np.zeros([output_dimension, output_dimension])
            for j in range(1, number_observer_markov_parameters):
                hk = hk - np.matmul(hk2[j], observer_gain_markov_parameters[i - j])
            observer_gain_markov_parameters.append(hk)

    return observer_gain_markov_parameters
