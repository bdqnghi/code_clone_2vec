import matplotlib.pyplot as plt


a=[[0.024,0.839],[0.0723,0.581],[0.224,0.634],[0.2523,0.571],[0.524,1.234],[0.423,1.171],[0.301,1.234],[0.23,1.1],[0.17,0.85],[0.21,0.9],[0.1111,0.3232],[0.15442,0.3455],[0.51,0.8],[0.56,0.7],[0.4,0.6],[0.44,0.54]]
a_1 = [[0.014,0.439],[0.0223,0.211],[0.42,0.739],[0.43,0.881],[0.344,0.469],[0.2323,0.781]]
a.extend(a_1)
label = ["dictionary(C#)","map(Java)","lock(C#)","synchronized(Java)","readonly(C#)","final(Java)","public (C#)"," public (Java)"," private (C#)"," private (Java)"," double (C#)"," double (Java)"," if (C#)"," if (Java)"," for (C#)"," for (Java)"]
label_1 = ["java.io.OutputStream.write(byte)(Java)","Sharpen.OutputStream.Write(int)(C#)","java.util.concurrent.atomic.AtomicInteger.getAndAdd(int)(Java)","Sharpen.AtomicInteger.GetAndAdd(int)(C#)","java.io.DataInputStream.read(byte)(Java)","System.IO.BinaryReader.Read(char,int,int)(C#)"]
label.extend(label_1)
colors = list()
for l in label:
	print l
	if "C#" in l:
		colors.append("r")
	else:
		colors.append("b")

print colors
plt.scatter(*zip(*a), marker='o', c=colors)


print zip(label,*zip(*a))
for label, x, y in zip(label,*zip(*a)):
	color = "blue"
	if "C#" in label:
		color = "red"
	
	plt.annotate(label,xy=(x,y),xytext=(0,0),textcoords="offset points",color=color)



plt.show()


# a=[[0.2,0.839],[0.21,0.75],[0.25,0.90],[0.12,0.656],[0.132,0.724],[0.3,0.79],[0.11,0.91],[0.22332,0.8722],[0.44,0.683]]
# label = ("call(C#)","call(Java)", "dictonary(C#)","pair(C#)","entry(C#)","map(Java)","entry(Java)","pair(C#)","pair(java)")


# colors = list()
# for l in label:
# 	print l

# 	if "decl_stmt" in l:
# 		colors.append("red")
# 	else:
# 		# if "C#" in l:
# 		# 	colors.append("r")
# 		# else:
# 		colors.append("blue")

# print colors
# plt.scatter(*zip(*a),c=colors, marker='o')


# print zip(label,*zip(*a))
# for label, x, y in zip(label,*zip(*a)):
# 	color = "blue"
# 	if "call" in label:
# 		color = "red"
	# else:
	# 	if "C#" in label:
	# 		color = "red"
		
	

# 	plt.annotate(label,xy=(x,y),xytext=(0,0),textcoords="offset points",color=color)



# plt.show()