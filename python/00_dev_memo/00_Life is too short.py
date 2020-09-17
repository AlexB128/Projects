text = "Life is too short. Python is easy."

dic = {}
for c in text:
    dic[c] = dic[c] + 1 if c in dic else 1

print(dic)

dic = {}
for c in text.split(' '):
    dic[c] = dic[c] + 1 if c in dic else 1

print(dic)
