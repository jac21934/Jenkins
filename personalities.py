import random
import numpy

# The basic d20
class D20:
  def __init__(self):
    self.name = "d20"
  
  def roll(self):
    return random.randint(1, 20)

  def flavor(self):
    return None

# The ultimate die, but it has performance anxiety
class SuperProdigy(D20):
  def __init__(self):
    self.name = "superprodigy"
  
  def roll(self):
    self.last_value = random.randint(1, 20)
    return self.last_value

  def flavor(self):
    if (self.last_value < 10):
      return "The die felt too much pressure"
    elif (self.last_value > 15):
      return "The die felt relaxed"
    else:
      return ""

# Always rolls exactly +/- 2 from whatever you were holding it as
class Blorp(D20):
  def __init__(self):
    self.name = "blorp"
  
  def roll(self):
    held_value = random.randint(1, 20)
    if held_value < 3:
      self.last_value = held_value + 2
    elif held_value > 18:
      self.last_value = held_value  -2
    elif bool(random.getrandbits(1)):
      self.last_value = held_value + 2
    else:
      self.last_value = held_value - 2
    self.held_value = held_value
    return self.last_value

  def flavor(self):
    return f"You were holding {self.held_value}"

# The ultimate die - reliably rolls very high
class Diamond(D20):
  def __init__(self):
    self.name = "diamond"

  def roll(self):
    return random.randint(12, 20)

# Solidly rolls high, but not too high
class Fresh(D20):
  def __init__(self):
    self.name = "fresh"
    #          1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20
    weights = [0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 4, 4, 3, 2, 1, 0, 0, 0]
    self.dist = [i / sum(weights) for i in weights]
  
  def roll(self):
    retVal = 1 + numpy.random.choice(20, 1, p=self.dist)
    return retVal

# Reliably rolls low
class LowNSlow(D20):
  def __init__(self):
    self.name = "low&slow"
    #          1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20
    weights = [1, 2, 3, 4, 4, 4, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.dist = [i / sum(weights) for i in weights]

  def roll(self):
    retVal = 1 + numpy.random.choice(20, 1, p=self.dist)
    return retVal

# Distribution changes over time
class Shy(D20):
  def __init__(self):
    self.name = "shy"
    #          1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20
    weights = [1, 3, 5, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    self.direction = "up"
    self.dist = [i / sum(weights) for i in weights]

  def roll(self):
    value = 1 + numpy.random.choice(20, 1, p=self.dist)
    # Mutate the distribution either up or down
    if self.direction == "up":
      self.dist.insert(0, self.dist.pop())
    else:
      self.dist.remove(0)
      self.dist.append(0)
    
    # Swap direction if necessary
    if self.dist[-1] > 0:
      self.direction = "down"
    if self.dist[0] > 0:
      self.direction = "up"
  
    return value
  
  def flavor(self):
    if self.dist.index(max(self.dist)) > 10 and self.direction == "up":
      return "Die is feeling good and getting luckier"
    elif self.dist.index(max(self.dist)) > 10 and self.direction == "down":
      return "Die is feeling good but getting unluckier"
    elif self.dist.index(max(self.dist)) <= 10 and self.direction == "up":
      return "Die is feeling bad but getting luckier"
    elif self.dist.index(max(self.dist)) <= 10 and self.direction == "down":
      return "Die is feeling bad and getting unluckier"