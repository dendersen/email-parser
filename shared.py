generalEmailFields = ["subject", "sender", "id", "errors"]

class emailFields:
  def __init__(self):
    self.data = {}
    self.errors = []
    self.finalKey: str | None = None
    self.final = []
    self.iterIndex = 0
  
  def fromString(self, string: str) -> "emailFields":
    self.data = {}
    self.errors = []
    self.finalKey = None
    self.final = []
    self.iterIndex = 0
    for line in string.split("\n"):
      key, value = line.split(": ", 1)
      self.data[key.strip().lower()] = value.replace("%\\n", "\n").strip()
    return self
  
  def __getitem__(self, key:str) -> str:
    if key.startswith("errors"):
      key,index = key.split("_")
      if not index is None:
        return self.errors[int(index)]
      else:
        return self.errors[0]
    elif key == self.finalKey:
      key,index = key.split("_")
      if not index is None:
        return self.final[int(index)]
      else:
        return self.final[0]
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
  
  def __iter__(self):
    self.iterIndex = 0
    return self
  
  def __next__(self) -> str:
    if self.iterIndex < len(self.data):
      key = list(self.data.keys())[self.iterIndex]
      value = self.data[key]
      self.iterIndex += 1
      return key
    
    elif self.iterIndex < len(self.data) + len(self.errors):
      error = self.errors[self.iterIndex - len(self.data)]
      self.iterIndex += 1
      return "errors_" + str(self.iterIndex - len(self.data) - 1)
    
    elif self.finalKey is not None and self.iterIndex < len(self.data) + len(self.errors) + len(self.final):
      final = self.final[self.iterIndex - len(self.data) - len(self.errors)]
      self.iterIndex += 1
      return self.finalKey + "_" + str(self.iterIndex - len(self.data) - len(self.errors) - 1)
    
    else:
      raise StopIteration
  
  def __str__(self) -> str:
    string = ""
    for key in self:
      string += key + ": " + self[key].replace("\n", "%\\n") + "\n"
    return string