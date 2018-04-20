def foo(i)
    print(i)
    i = i + 1
    if i < 10
         x = foo(i)
    end
    return
end

main
a = 1
y = foo(a)
