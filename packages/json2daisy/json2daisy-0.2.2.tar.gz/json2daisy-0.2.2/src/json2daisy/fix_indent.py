
import sys
import os

with open (sys.argv[1], 'r') as file:
  data = [line for line in file]

outname = 'unindent_' + os.path.basename(sys.argv[1])
outname = os.path.join(os.path.dirname(sys.argv[1]), outname)

with open(outname, 'w') as file:
  for line in data:
    outstring = ''
    for i in range(len(line)):
      if line[i] == '\t':
        outstring += ' '*2
      else:
        outstring += line[i:]
        break
    file.write(outstring)
    
  
