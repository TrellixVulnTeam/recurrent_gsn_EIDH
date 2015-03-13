'''
.. module: denoising_autoencoder

A Denoising Autoencoder is a special case of Generative Stochastic Networks. It is used as a basic,
unsupervised, generative building block for feedforward networks.

'Generalized Denoising Auto-Encoders as Generative Models'
Yoshua Bengio, Li Yao, Guillaume Alain, Pascal Vincent
http://papers.nips.cc/paper/5023-generalized-denoising-auto-encoders-as-generative-models.pdf
'''
__authors__ = "Markus Beissinger"
__copyright__ = "Copyright 2015, Vitruvian Science"
__credits__ = ["Markus Beissinger"]
__license__ = "Apache"
__maintainer__ = "OpenDeep"
__email__ = "dev@opendeep.org"

# standard libraries
import logging
# third party libraries
import theano.sandbox.rng_mrg as RNG_MRG
# internal references
import opendeep.log.logger as logger
from opendeep.models.model import Model
from opendeep.models.multi_layer.generative_stochastic_network import GSN
from opendeep.data.standard_datasets.image.mnist import MNIST
from opendeep.optimization.adadelta import AdaDelta

log = logging.getLogger(__name__)

class DAE(GSN):
    '''
    Class for creating a new Denoising Autoencoder (DAE)
    This is a special case of a GSN with only one hidden layer
    '''
    # Default values to use for some DAE parameters
    _defaults = {# gsn parameters
                "walkbacks": 1,
                "hidden_size": 1500,
                "visible_activation": 'sigmoid',
                "hidden_activation": 'tanh',
                "input_sampling": True,
                "MRG": RNG_MRG.MRG_RandomStreams(1),
                # train param
                "cost_function": 'binary_crossentropy',
                # noise parameters
                "noise_annealing": 1.0, #no noise schedule by default
                "add_noise": True,
                "noiseless_h1": True,
                "hidden_add_noise_sigma": 2,
                "input_salt_and_pepper": 0.4,
                # data parameters
                "output_path": 'outputs/dae/',
                "is_image": True,
                "vis_init": False}

    def __init__(self, config=None, defaults=_defaults, inputs_hook=None, hiddens_hook=None, dataset=None):
        # init Model
        # force the model to have one layer - DAE is a specific GSN with a single hidden layer
        defaults['layers'] = 1
        if config:
            config['layers'] = 1
        super(DAE, self).__init__(config=config, defaults=defaults, inputs_hook=inputs_hook, hiddens_hook=hiddens_hook, dataset=dataset)


class StackedDAE(Model):
    '''
    A stacked Denoising Autoencoder stacks multiple layers of DAE's
    '''
    def __init__(self):
        super(StackedDAE, self).__init__()
        log.error("StackedDAE not implemented yet!")
        raise NotImplementedError("StackedDAE not implemented yet!")


###############################################
# MAIN METHOD FOR RUNNING DEFAULT DAE EXAMPLE #
###############################################
def main():
    ########################################
    # Initialization things with arguments #
    ########################################
    logger.config_root_logger()
    log.info("Creating a new DAE")

    mnist = MNIST()
    config = {"output_path": '../../../outputs/dae/mnist/'}
    dae = DAE(config=config, dataset=mnist)

    # # Load initial weights and biases from file
    # params_to_load = 'dae_params.pkl'
    # dae.load_params(params_to_load)

    optimizer = AdaDelta(dae, mnist)
    optimizer.train()


if __name__ == '__main__':
    main()