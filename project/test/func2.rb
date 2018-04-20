def bar(z)
    print(z)
    return
end

def foo(x,y)
    i = x + 5
    i = i*y
    return i
end

main
a = 7
c = 9
b = foo(a,c)
d = bar(b)
print(d)
e = foo(5,6)
f = bar(e)
print(f)
foo(2,3)
