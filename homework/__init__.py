import re
#1.
pattern = re.compile(r'\d+')
str1 = 'sadsd454sdf454fsd35435sdfsdf'
ans = ''.join(re.findall(pattern, str1))
print(ans)

#2.
pattern2 = re.compile(r'[A-Za-z]')
ans2 = result = ''.join(re.findall(pattern2, str1))
print(ans2)

#3.
str2 = matchstr = """_abc, abc, abc_1, 1_abc, abc$, @#!"""
pattern3 =  r"""(\b[a-zA-Z_]\w+\b)"""
ans3 = result = re.findall(pattern3, str2)
print(ans3)

#4.
pattern4 = '\w+\@\w+\.\w{3}'
str3 = 'asfdfsjgf@qq.com'
ans4 = re.sub(pattern4,'123123@126.com',str3)
print(ans4)