def foo(a)
    a= a + 1
    print(a)
    if a < 5
        x=foo(a)
    end
    return
end

main
c=2
y=foo(c)

