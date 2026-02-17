class emailFields:
  def __init__(self):
    self.data = {}
    self.errors = []
    self.finalKey = None
    self.final = []
  
  def __getitem__(self, key:str) -> str:
    return self.data[key]
  
  def __setitem__(self, key:str, value:str | list[str]):
    if key == "errors":
      self.errors.append(value)
    elif key == self.finalKey:
      self.final.append(value)
    else:
      self.data[key] = value
  
  def setFinal(self, key:str):
    self.finalKey = key
  
  def __contains__(self, key:str) -> bool:
    if key == "errors": return True
    if key == self.finalKey: return True
    return key in self.data