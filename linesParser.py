s = 'DCL a DEFAULT 100;a - 91 == 4 + 5;'
openbrace = 0
pos = []

x = 0

for i in s:
    if i == '{':
        openbrace += 1
    elif i == '}':
        openbrace -= 1
    elif i == ';' and openbrace == 0:
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
