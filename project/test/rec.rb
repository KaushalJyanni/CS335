def foo(a)
    print(a)
    a= a + 1
    if a < 10
        foo(a) 
    end
    return
end
main
c=5
foo(c)

