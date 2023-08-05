#from __future__ import annotations

from tensorflow.keras.callbacks import Callback


class PowerScheduler (Callback):
  def __init__ (self) -> None:
    super(PowerScheduler, self) . __init__()