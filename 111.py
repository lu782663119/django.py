def age(n):
    if n == 1:
       c = 10
    else:
       c = age(n - 1) + 2
    return c
print ("第五个人的年龄是：",age(30))