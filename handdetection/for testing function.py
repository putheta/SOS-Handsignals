a = [123,23,41,1,200,300]
min = 0
max = 0

for i in a :
    if i > max :
        max = i
    if i< max :
        min = i
    
print(min,max)