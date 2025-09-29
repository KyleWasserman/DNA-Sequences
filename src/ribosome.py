import re
from functools import reduce

class Node:
  def __init__(self, codon, name):
    self.codon = codon
    self.name = name

def read_codons(codon_file):
  # This will open a file with a given path (codon_file)
  file = open(codon_file)
  global letters
  letters = []
  global names
  names = []
  global stored_dir
  stored_dir = {}
  global codon_dir
  codon_dir = {}

  # Iterates through a file, storing each line in the line variable
  for line in file:
    Regex = r"^(?P<name>[A-Za-z]+): (?P<acids>(([AUGC](\{\d+\})?)+(,\s)?)+(\s)*$)"
    matches = re.search(Regex, line)
    if matches == None:
      continue
    acid_list = re.split(r",\s", matches.group("acids"))
    name = matches.group("name")
    Regex2 = r"(([AUGC](\{(?P<number>\d+)\})?))"
    newList = []
    for item in acid_list:
      match2 = re.findall(Regex2, item)
      stri = ""
      times = 0
      for i in match2:
          match3 = re.search(Regex2, i[0])
          if match3.group("number") == None:
              times = 1
          else:
            times = int(match3.group("number"))
          for j in range(times):
            stri += str(i[0][0])
      newList.append(stri)
      stored_dir[stri] = name
      letters.append(stri)  
    codon_dir[name] = newList
    names.append(name)
  letters = sorted(letters, key=len)
  letters.reverse()  
    
  
  
    

def read_evals(eval_file):
  # This will open a file with a given path (eval_file)
  file = open(eval_file)
  global evals
  evals = {}
  # Iterates through a file, storing each line in the line variable
  for line in file:
    Regx = r"^(?P<name>[a-zA-z0-9]+):\s(?P<LR>L|R),\s(?P<place>PO|PR|I)(\s)*$"
    match = re.search(Regx, line)
    temp = []
    temp.append(match.group("LR"))
    temp.append(match.group("place"))
    evals[match.group("name")] = temp
    





def encode(sequence):
  meow = ""
  seq_list = re.split(r"\s", sequence)
  for name in seq_list:
    cluster = codon_dir.get(name)
    if cluster == None:
      continue
    max = ""
    for acid in cluster:
      if len(str(acid)) > len(max):
        max = str(acid)
    meow += max
  return meow

def decode(sequence):
  if len(sequence) < 1:
    return ""
  answer = ""  
  found = None
  while(len(sequence) > 0):
    found = None 
    for pattern in letters:
      Regex = "^" + pattern
      Match = re.search(Regex, sequence)
      if Match != None:
        found = pattern
        break
    if found == None:
      sequence = sequence.replace(sequence[0], "", 1)
      continue
    else :
      for i in range(len(found)):
        sequence = sequence.replace(sequence[0], "", 1)
      answer += stored_dir.get(found)
      answer += " "
  answer = answer.rstrip(" ")
  return answer

def decodeH(sequence):
  if len(sequence) < 1:
    return []
  answer = []  
  found = None
  while(len(sequence) > 0):
    found = None 
    for pattern in letters:
      Regex = "^" + pattern
      Match = re.search(Regex, sequence)
      if Match != None:
        found = pattern
        break
    if found == None:
      sequence = sequence.replace(sequence[0], "", 1)
      continue
    else :
      for i in range(len(found)):
        sequence = sequence.replace(sequence[0], "", 1)
      person = Node(found, stored_dir.get(found))
      answer.append(person)
  return answer






def operate(sequence,eval_name):
  if (len(sequence) < 1):
    return ""
  if evals.get(eval_name) == None:
    return None 
  answerL = []  
  answer = ""  
  if evals.get(eval_name)[0] == "R":
    temp = ""
    for i in sequence:
      temp = i + temp
    sequence = temp
  setting = evals.get(eval_name)[1]   
  directions = decodeH(sequence)
  started = False
  for direction in directions:
    if started == False:
      if direction.name == "START":
        started = True 
      continue
    else:
      if direction.name == "STOP":
        started = False
        continue
      if direction.name == "START":
        started = True
        continue  
      answerL.append(direction)
  if setting == "PO":
    answerL = PO(answerL)
  if setting == "PR":
    answerL.reverse()
    answerL = PO(answerL)
    answerL.reverse()
  if setting == "I":
    answerL.reverse()
    answerL = I(answerL)
    answerL.reverse()    
  for node in answerL:
    answer += node.codon
  return answer
      

def I(library):
  Going = True
  while Going == True:
    Going = False
    for i in range(len(library)):
      if library[i].name == "SWAP":
        if (i < 1) or (i > len(library) - 2):
          library.pop(i)
          Going = True
          break
        if library[i + 1].name == "DEL" or library[i+1].name == "SWAP":
          continue 
        if library[i + 1].name == "EXCHANGE":
          library.pop(i)
          Going = True
          break
        library[i-1], library[i+1] = library[i+1], library[i-1]
        library.pop(i)
        Going = True
        break  
      if library[i].name == "DEL":
        if i == 0:
          library.pop(i)
          Going = True
          break
        library.pop(i - 1)
        library.pop(i - 1)
        Going = True
        break
      if library[i].name == "EXCHANGE":
        if i == 0:
          library.pop(i)
          Going = True
          break
        if len(codon_dir.get(library[i-1].name)) < 2:
          library.pop(i)
          Going = True
          break
        library[i - 1] = swapcodon(library[i-1])    
        library.pop(i)
        Going = True
        break  
  return library   


def PO(library):
  Going = True
  while Going == True:
    Going = False
    for i in range(len(library)):
      if library[i].name == "SWAP":
        if (i < 2):
          library.pop(i)
          Going = True
          break
        library[i-2], library[i-1] = library[i-1], library[i-2]
        library.pop(i)
        Going = True
        break  
      if library[i].name == "DEL":
        if i == 0:
          library.pop(i)
          Going = True
          break
        library.pop(i - 1)
        library.pop(i - 1)
        Going = True
        break
      if library[i].name == "EXCHANGE":
        if i == 0:
          library.pop(i)
          Going = True
          break
        if len(codon_dir.get(library[i-1].name)) < 2:
          library.pop(i)
          Going = True
          break
        library[i - 1] = swapcodon(library[i-1])    
        library.pop(i)
        Going = True
        break  
  return library        

def swapcodon(node):
  for seq in codon_dir.get(node.name):
    if seq != node.codon:
      node.codon = seq
      return node
  return None    

              

