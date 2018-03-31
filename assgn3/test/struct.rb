name=[]
Struct.new("T",:a,:b,:c,:d,:e,:name,:f)

def f(x)
	x["a"]='a'
	x["b"]=47114711
	x["c"]='c'
	x["d"]=1234
	x["e"]=3.141592897932
	x["f"]='*'
	x["name"]="abc"
end

k=Struct::T.new('','','','','','','')
f(k)
