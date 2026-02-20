generalEmailFields = ["subject", "sender", "id", "errors"]

class emailFields:
  def __init__(self):
    self.data:dict[str,str] = {}
    self.errors:list[str] = []
    self.finalKey: str | None = None
    self.final: list[str] = []
    self.iterIndex = 0
  
  def fromString(self, string: str, id:str) -> "emailFields":
    self.data = {}
    self.errors = []
    self.finalKey = None
    self.final = []
    self.iterIndex = 0
    self.data["id"] = id
    for line in string.split("\n"):
      key, value = line.split(": ", 1)
      self.data[key.strip().lower()] = value.replace("%\\n", "\n").strip()
    return self
  
  def __getitem__(self, key:str) -> str:
    if key.startswith("errors"):
      key,index = key.split("_",1)
      if("_" in key):
        if int(index) > -1:
          return self.errors[int(index)]
        else:
          return self.errors[0]
      else:
          return "\n".join(self.final)
    elif self.finalKey is not None and key.startswith(self.finalKey):
      if "_" in key:
        key,index = key.split("_",1)
        if int(index) > -1:
          return self.final[int(index)]
        else:
          return self.final[0]
      else:
        return "\n".join(self.final)
    return self.data[key]
  
  def __setitem__(self, key:str, value:str):
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
      self.iterIndex += 1
      return key
    
    elif self.iterIndex < len(self.data) + len(self.errors):
      key = self.iterIndex - len(self.data) - 1
      self.iterIndex += 1
      return "errors_" + str(key)
    
    elif self.finalKey is not None and self.iterIndex < len(self.data) + len(self.errors) + len(self.final):
      key = self.iterIndex - len(self.data) - len(self.errors) - 1
      self.iterIndex += 1
      return self.finalKey + "_" + str(key)
    
    else:
      raise StopIteration
  
  def __str__(self) -> str:
    string = ""
    for key in self.data:
      if key == "id":
        continue
      string += key + ": " + self[key].replace("\n", "%\\n") + "\n"
    for i, e in enumerate(self.errors):
      string += "errors_{}: ".format(i) + e.replace("\n", "%\\n") + "\n"
    if self.finalKey is not None:
      for i, f in enumerate(self.final):
        string += self.finalKey + "_{}: ".format(i) + f.replace("\n", "%\\n") + "\n"
    return string
