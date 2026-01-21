s=' '+input()+' '
i=0
s1=''
word=""
while i <len(s)-1:
    if s[i]==' ':
        i+=1
        if s[i] in 'aeiouAEIOU':
            while s[i] != ' ':
                word=s[i]+word
                i+=1
        else:
            while s[i] != ' ':
                word=word+s[i]
                i+=1
        s1+=word+' '
        word=""
print(s1)

c=0
for ch in s:
    if ord(ch) not in range(ord('a'), ord('z')+1) and ord(ch) not in range(ord('0'), ord('9')+1) and ord(ch) not in range(ord('A'), ord('Z')+1):
        c+=1
print(c)
s2=''
for ch in s:
    if 65<=ord(ch)<=90:
        ch=chr(ord(ch)+32)
    if ord(ch)-2<97:
        s2+=chr(122-(99-ord(ch)))
    elif 97<=ord(ch)-2<=122:
        s2+=chr(ord(ch)-2)
    else:
        s2+=ch
print(s2)




