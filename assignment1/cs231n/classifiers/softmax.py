import math
import numpy as np
from random import shuffle

def softmax_loss_naive(W, X, y, reg):
  """
  Softmax loss function, naive implementation (with loops)

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using explicit loops.     #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  # compute the loss and the gradient
  num_classes = W.shape[1]
  num_train = X.shape[0]
  loss = 0.0

  for i in xrange(num_train):
    scores = X[i].dot(W)
    probs = np.zeros(num_classes)
    logC = -np.max(scores)    # constant to improve numeric stability (-max scores[j])
    for j in xrange(num_classes):
      probs[j] = math.exp(scores[j] + logC) # unnormalized probability for class
    
    loss += -math.log(probs[y[i]] / np.sum(probs))
  
    probs /= np.sum(probs)   # Normalize the probabilities 
    probs[y[i]] -= 1.0       # gradient subtracts one from correct class
    dW += X[i].reshape(-1,1) * probs.T

  loss /= num_train

  loss += 0.5 * reg * np.sum(W * W)

  dW = dW/num_train + reg * W   # average gradient and add regularization

  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW


def softmax_loss_vectorized(W, X, y, reg):
  """
  Softmax loss function, vectorized version.

  Inputs and outputs are the same as softmax_loss_naive.
  """
  # Initialize the loss and gradient to zero.
  loss = 0.0
  dW = np.zeros_like(W)

  #############################################################################
  # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
  # Store the loss in loss and the gradient in dW. If you are not careful     #
  # here, it is easy to run into numeric instability. Don't forget the        #
  # regularization!                                                           #
  #############################################################################
  num_train = X.shape[0]
  scores = X.dot(W)  
  correct_class_scores = scores[np.arange(num_train), y[:num_train]]
  logC = -np.max(scores)  # for numerical stability when computing exponentials

  # Compute probabilities for each score given the input values and weights.
  probs = np.exp(scores + logC)
  probs = probs / np.sum(probs, axis=1).reshape(-1,1) # normalize probs

  # Compute loss from probabilities of the correct class scores.
  loss = np.sum(np.negative(np.log(probs[np.arange(num_train), y[:num_train]])))
  loss = loss/num_train + .5 * reg * np.sum(W * W)

  # Calculate the gradient.  First adjust probabilities for correct class.
  # Then calculate gradient as dot product of input values & probablities.
  # Then average and add regularization.
  probs[range(num_train), y] -= 1
  dW = (X.T).dot(probs)
  dW = dW/num_train + reg * W
  #############################################################################
  #                          END OF YOUR CODE                                 #
  #############################################################################

  return loss, dW
