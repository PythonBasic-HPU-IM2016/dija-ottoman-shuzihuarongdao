temp=input()
try:
    if temp[-1] in ["f","F"]:
        c=(eval(temp[:-1])-32)/1.8
        print("{:.2f}C".format(c))
    elif temp[-1] in ["c","C"]:
        f = 1.8*eval(temp[:-1])+32
        print("{:.2f}F".format(f))
    else:
        print("输入错误，末位只能是'C','c','F','f'")
except NameError:
    print("试图访问的变量名不存在")
except SyntaxError:
    print("存在语法错误")
