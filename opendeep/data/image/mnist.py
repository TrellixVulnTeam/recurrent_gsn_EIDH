'''
Object for the MNIST handwritten digit dataset
'''
__authors__ = "Markus Beissinger"
__copyright__ = "Copyright 2015, Vitruvian Science"
__credits__ = ["Markus Beissinger"]
__license__ = "Apache"
__maintainer__ = "OpenDeep"
__email__ = "dev@opendeep.org"

# standard libraries
import logging
import cPickle
import gzip
import numpy
# internal imports
import opendeep.data.dataset as datasets
from opendeep.data.dataset import Dataset
import opendeep.utils.file_ops as files
from opendeep.utils.nnet import make_shared_variables

log = logging.getLogger(__name__)

class MNIST(Dataset):
    '''
    Object for the MNIST handwritten digit dataset. Pickled file provided by Montreal's LISA lab into train, valid, and test sets.
    '''
    def __init__(self, binary=False, filename='mnist.pkl.gz', source='http://www.iro.umontreal.ca/~lisa/deep/data/mnist/mnist.pkl.gz'):
        # instantiate the Dataset class to install the dataset from the url
        log.info('Loading MNIST with binary=%s', str(binary))
        super(self.__class__, self).__init__(filename, source)
        # self.dataset_location now contains the os path to the dataset file
        # self.file_type tells how to load the dataset
        # load the dataset into memory
        if self.file_type is files.GZ:
            (train_X, train_Y), (valid_X, valid_Y), (test_X, test_Y) = cPickle.load(gzip.open(self.dataset_location, 'rb'))
        else:
            (train_X, train_Y), (valid_X, valid_Y), (test_X, test_Y) = cPickle.load(open(self.dataset_location, 'r'))

        # make optional binary
        if binary:
            _binary_cutoff = 0.5
            log.debug('Making MNIST X values binary with cutoff %s', str(_binary_cutoff))
            train_X = (train_X > _binary_cutoff).astype('float32')
            valid_X = (valid_X > _binary_cutoff).astype('float32')
            test_X  = (test_X > _binary_cutoff).astype('float32')

        log.debug('Concatenating train and valid sets together...')
        train_X = numpy.concatenate((train_X, valid_X))
        train_Y = numpy.concatenate((train_Y, valid_Y))

        self._train_shape = train_X.shape
        self._valid_shape = valid_X.shape
        self._test_shape  = test_X.shape
        log.debug('Train shape is: %s', str(self._train_shape))
        log.debug('Valid shape is: %s', str(self._valid_shape))
        log.debug('Test shape is: %s', str(self._test_shape))
        # transfer the datasets into theano shared variables
        log.debug('Loading MNIST into theano shared variables')
        (self.train_X, self.train_Y,
         self.valid_X, self.valid_Y,
         self.test_X, self.test_Y) = make_shared_variables((train_X, train_Y, valid_X, valid_Y, test_X, test_Y), borrow=True)


    def getDataByIndices(self, indices, subset):
        '''
        This method is used by an iterator to return data values at given indices.
        :param indices: either integer or list of integers
        The index (or indices) of values to return
        :param subset: integer
        The integer representing the subset of the data to consider dataset.(TRAIN, VALID, or TEST)
        :return: array
        The dataset values at the index (indices)
        '''
        if subset is datasets.TRAIN:
            return self.train_X.get_value(borrow=True)[indices]
        elif subset is datasets.VALID and hasattr(self, 'valid_X') and self.valid_X:
            return self.valid_X.get_value(borrow=True)[indices]
        elif subset is datasets.TEST and hasattr(self, 'test_X') and self.test_X:
            return self.test_X.get_value(borrow=True)[indices]
        else:
            return None

    def getLabelsByIndices(self, indices, subset):
        '''
        This method is used by an iterator to return data label values at given indices.
        :param indices: either integer or list of integers
        The index (or indices) of values to return
        :param subset: integer
        The integer representing the subset of the data to consider dataset.(TRAIN, VALID, or TEST)
        :return: array
        The dataset labels at the index (indices)
        '''
        if subset is datasets.TRAIN and hasattr(self, 'train_Y') and self.train_Y:
            return self.train_Y.get_value(borrow=True)[indices]
        elif subset is datasets.VALID and hasattr(self, 'valid_Y') and self.valid_Y:
            return self.valid_Y.get_value(borrow=True)[indices]
        elif subset is datasets.TEST and hasattr(self, 'test_Y') and self.test_Y:
            return self.test_Y.get_value(borrow=True)[indices]
        else:
            return None