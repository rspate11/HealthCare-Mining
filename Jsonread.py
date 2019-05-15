import json
import pandas
import numpy

with open('diabetes_30pages.json','r') as f:
     data = json.load(f)
     # print (data)
with open('diabetes_replies.json', 'r') as f1:
    replies = json.load(f1)

file = open("myfile.txt", "w")
reply = ""
datastring = ""
replyText =" "
for i in range (0, len(data)):
    try:
        # print(data[i]['symptom'])
        datastring = (str(data[i]['title']).strip("[]").strip("''") +" "+ str(data[i]['tags']).strip("[]").strip("''")+ " " +str(data[i]['threadBody']).strip("[]").strip("''"))
        id = str(data[i]['title']).strip("[]").strip("''")

        for j in range (0, len(replies)):
            try:
                reply = (str(replies[j]['threadId']).strip("[]").strip("''") )

                # print (reply)
                # print (id)
                if  reply == id:
                      replyText = replyText + " " + (str(replies[j]['replyText']).strip("[]").strip("''"))
            except:
                continue

        file.write(datastring + "" + replyText + "\n")
        # print( datastring + "" + replyText)

    except:
        continue

symptomFile = open("symptoms.txt")
lines = symptomFile.readlines()
syms = []
for line in lines:
    syms.append(line[:-1])
    # for word in line.split():
    #     syms.append(word)

print(syms)

length= len(syms)
fh = open("myfile.txt")
lines = fh.readlines()
# print(lines)
finalCount = list()
for i in range(0,len(syms)):
    count = list()
    for j in range(0,len(lines)):
        if syms[i] in lines[j]:
            count.append(1)
        else:
            count.append(0)
    finalCount.append(count)

symEnc = numpy.array(finalCount)
print(symEnc)
encSym = numpy.transpose(symEnc)

symSym = numpy.matmul(symEnc,encSym)
print(symSym)

I = pandas.Index(syms, name="rows")
C = pandas.Index(syms, name="columns")

file1 = open("output.txt", "w")
df = pandas.DataFrame(symSym,index=I, columns=C)
print(df)
for i in range(0, length):
    df = df.sort_values(by = syms[i], axis=1,ascending= False)
    file1.write(syms[i] + str(df.columns.values.tolist()) + "\n")
print(df)
df.to_csv("symSym.csv")