import theano
import theano.tensor as T
import theano.ifelse as ifelse
import numpy as np
import pdb
import math

import intm
import ac
import acr

if __name__ == '__main__':
  template = theano.shared(np.float32(np.array([[0.22, 0.44, 0.22],
                                                [0.66, 0.88, 0.66],
                                                [0.11, 0.33, 0.11]])), name='template')

  ack = ac.AC(None, template=template, activation=None)
  acker = acr.ACR(ack, theano.shared(10, name='image_size'))
  iGeoPose = (intm.getINTMMatrix(1, None, theano.shared(np.float32(np.array([[1,-3,-3,1,1,0,0*math.pi/2]]))))[0][0],
              intm.getINTMMatrix(1, None, theano.shared(np.float32(np.array([[1,-3,-3,1,1,0,0*math.pi/2]]))))[1][0])
  render = acker.render(iGeoPose[0], iGeoPose[1])
  print render.eval()

  print T.grad(T.sum(render), acker.template).eval()
  pdb.set_trace()

















