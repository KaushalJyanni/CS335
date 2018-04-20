class a
    x = 5
    y = 6
    def foo(q)
        z =q +2
        return z
    end
endclass

f = newclass a
g = newclass a
g.y = 1
p = 3
f.x = 2
f.y = f.x 
f.x = f.foo(g.y)
print(f.x)
v=f.foo(g.y)
f.y = f.foo(v)
print(f.y)
