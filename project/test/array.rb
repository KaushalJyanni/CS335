main
a=array.new(5)
d=1
a[0]=2
a[d]=3
a[2]=4
d=0
c=a[d]+a[2]
print(c)
for i in (0..4)
    a[i] = i + 1
end

for i in (0..4)
    x=a[i]
    print(x)
end
