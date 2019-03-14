s = 'DCL a DEFAULT 100;a - 91 == 4 + 5; DESDE asd = 4 HASTA dsa HAGA QWERYT;YTREWQ FINDESDE; olakase'
openbrace = 0
pos = []



repita = []
mientras = []
i = 0
n = len(s)
while i < n:
    digit = s.find('REPITA', i)
    if not (digit in repita) and digit != -1:
        repita.append(digit)
    digit = s.find('MIENTRAS', i)
    if not (digit in mientras) and digit != -1:
        mientras.append(digit)
    i += 1
print(repita)
print(mientras)  
if len(repita) != len(mientras):
    print ("Wrong balance between REPITA's and MIENTRAS's")
i = 0
n = len(repita)
while i < n:
    if repita[i] > mientras[i]:
        print ("Wrong distribution of REPITA's and MIENTRAS's")
    i += 1
w = 0
inside_while = False



haga = []
findesde = []
y = 0
u = len(s)
while y < u:
    digit = s.find('HAGA', y)
    if not (digit in haga) and digit != -1:
        haga.append(digit)
    digit = s.find('FINDESDE', y)
    if not (digit in findesde) and digit != -1:
        findesde.append(digit)
    y += 1
print(haga)
print(findesde)  
if len(haga) != len(findesde):
    print ("Wrong balance between REPITA's and MIENTRAS's")
o = 0
p = len(haga)
while o < p:
    if haga[o] > findesde[o]:
        print ("Wrong distribution of REPITA's and MIENTRAS's")
    o += 1
l = 0
inside_do = False


x = 0
for i in s:
    if w < n:
        if x > repita[w]:
            inside_while = True
        if x > mientras[w]:
            inside_while = False
            w += 1
    if l < p:
        if x > haga[l]:
            inside_do = True
        if x > findesde[l]:
            inside_do = False
            l += 1
    if i == '{':
        openbrace += 1
    elif i == '}':
        openbrace -= 1
    elif i == ';' and openbrace == 0 and inside_while == False and inside_do == False:
        pos.append(x)
    x += 1

lista = []
n = len(pos)

y = 0

while y < n:
    if y == 0:
        lista.append(s[:pos[y]])
    else:
        lista.append(s[pos[y-1]+1:pos[y]])
    y += 1

lista.append(s[pos[-1]+1:])

if openbrace == 0:
    print(lista)
else:
    print("Bad distribution of brackets!")
