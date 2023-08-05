from itertools import zip_longest

list1 = [1, 8, 19, 26, 31, 42]

list2=[6, 11, 24, 29, 35, 37, 39, 44]

start_bug = []
end_bug = []
bug=[(x, y) for x, y in zip_longest(list1, list2, fillvalue=-1) ]
print(bug)
for i in bug:
    if i[0] > i[1]:
        start_bug.append(i[0])
    elif i[0] == -1:
        end_bug.append(i[1])

couple=[]
for i in start_bug:
    for j in end_bug:
        if i < j:
            couple.append((i,j))

print(couple)

no_bug=[(x, y) for x, y in zip_longest(list1, list2, fillvalue=-1) if x != -1 and x < y]
no_bug= no_bug+list(couple)
print(no_bug)
