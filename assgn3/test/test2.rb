for i in (1..10)
    rno = rand(100) + 1
    msg = case rno
        when 42 then "The ultimate result."
        when 1..10 then "Way too small."
        when 11..15,19,27 then "Sorry, too small"
        when 80..99 then "Way to large"
        when 100 then
                print "TOPS\n"
                "Really way too large"
        else "Just wrong"
    end
    print "Result: ", rno, ": ", msg, "\n"
end
