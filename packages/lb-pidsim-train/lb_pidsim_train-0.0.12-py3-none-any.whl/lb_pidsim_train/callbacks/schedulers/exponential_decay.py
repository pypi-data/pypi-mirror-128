#from __future__ import annotations


def exponential_decay (lr0, step = 1):
  """short description
  
  Parameters
  ----------
  lr0 : ...
    ...

  step : ...
    ...
  """
  def exponential_decay_func (epoch):
    return lr0 * 0.1**(epoch / step)
  return exponential_decay_func
