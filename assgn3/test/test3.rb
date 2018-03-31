def surround(before, after, *items)
    print "yolo!!! empty function"
end
surround('[', ']', 'this', 'that', 'the other')

print "\n"

surround('<', '>', 'Snakes', 'Turtles', 'Snails', 'Salamanders', 'Slugs','Newts')

print "\n"

def boffo(a, b, c, d)
    print "a = #{a} b = #{b}, c = #{c}, d = #{d}\n"
end
a1 = ['snack', 'fast', 'junk', 'pizza']
a2 = [4, 9]

boffo(*a1)
boffo(*b, a1, &c, d)
