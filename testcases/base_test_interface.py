from abc import ABC, abstractmethod

class BaseTestInterface(ABC):
  @abstractmethod
  def setup_class(self):
    self.headers = {}

  def set_headers(self, datas:dict):
    for k,v in datas.items():
      self.headers.update({k:v})
  
  def clear_headers(self):
    self.headers.clear()