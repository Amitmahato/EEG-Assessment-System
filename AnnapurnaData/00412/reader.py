patient = open('ptFile.dat','rb')
print('fileopened')
while ord(patient.read(1))!= 77 :
    continue
s= patient.read(1)
print(s)
while ord(s)==32:
    s = patient.read(1)
    print(s)
    continue

print('0')
level = 0
pt_name = ''
count = 0
while level<2 and count<20:
    if ord(s)!=32:
        level = 0
    else:
        level+=1
    pt_name+= chr(ord(s))
    count+=1
    print(s)
    s= patient.read(1)
    print('.',end='')
print(pt_name)
