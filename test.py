# coding:utf8

bin=str(input('输入二进制数：'))
count = 0
for i in range(0,len(bin)):
    if bin[i] == str(1):
        sum=2**(len(bin)-i-1)
        count=count+sum
print count
