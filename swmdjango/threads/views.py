from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from collections import defaultdict

import json
import pandas
import numpy
import csv
import os
import nltk


dirname = os.path.dirname(__file__)


def getFileName(filename):
    return os.path.abspath(os.path.join(dirname, '../..', 'data/' + filename))


def getRelatedSymptoms(symptom=None):
    ############################### comment till here if symSym.txt exists
    filename = getFileName('diabetes_30pages.json')
    with open(filename, 'r') as f:
        data = json.load(f)

    filename = getFileName('diabetes_replies.json')
    with open(filename, 'r') as f1:
        replies = json.load(f1)

    replyText = " "
    for i in range (0, len(data)):
        try:
            datastring = (str(data[i]['title']).strip("[]").strip("''") + " " + str(data[i]['tags']).strip("[]").strip("''")+ " " +str(data[i]['threadBody']).strip("[]").strip("''"))
            id = str(data[i]['title']).strip("[]").strip("''")

            for j in range (0, len(replies)):
                try:
                    reply = (str(replies[j]['threadId']).strip("[]").strip("''") )

                    if  reply == id:
                          replyText = replyText + " " + (str(replies[j]['replyText']).strip("[]").strip("''"))
                except:
                    continue

            file.write(datastring + "" + replyText + "\n")

        except:
            continue

    filename = getFileName('symptoms.txt')
    symptomFile = open(filename)
    lines = symptomFile.readlines()
    syms = []
    for line in lines:
        syms.append(line[:-1])

    length = len(syms)
    fh = open("myfile.txt")
    lines = fh.readlines()
    finalCount = list()
    for i in range(0,len(syms)):
        count = list()
        for j in range(0, len(lines)):
            if syms[i] in lines[j]:
                count.append(1)
            else:
                count.append(0)
        finalCount.append(count)

    symEnc = numpy.array(finalCount)
    encSym = numpy.transpose(symEnc)

    symSym = numpy.matmul(symEnc,encSym)

    I = pandas.Index(syms, name="rows")
    C = pandas.Index(syms, name="columns")

    file1 = open("output.txt", "w")
    df = pandas.DataFrame(symSym,index=I, columns=C)
    for i in range(0, length):
        df = df.sort_values(by = syms[i], axis=1,ascending= False)
        file1.write(syms[i] + str(df.columns.values.tolist()) + "\n")
    df.to_csv("symSym.csv")
    ############################### comment till here if symSym.txt exists

    filename = getFileName('symSym.csv')
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        allSymptoms = []
        relatedSymptoms = []
        for i1, row in enumerate(csv_reader):
            if symptom is None:
                return row[1:]

            if i1 == 0:
                allSymptoms = row
            if row[0] == symptom or nltk.edit_distance(row[0], symptom) < 10:
                for i2, r in enumerate(row):
                    if r != '0' and i2 != 0:
                        relatedSymptoms.append(allSymptoms[i2])
        return relatedSymptoms


class GetThreads(APIView):
    def post(self, request, format=None):
        querySymptom = request.data.get('symptom')

        relatedSymptoms = getRelatedSymptoms(querySymptom)

        if querySymptom is "":
            relatedSymptoms = getRelatedSymptoms()

        data = {
            "related_symptoms": relatedSymptoms
        }

        if querySymptom not in relatedSymptoms:
            relatedSymptoms.insert(0, querySymptom)

        # parse the diabetes_threads.json
        filename = getFileName("threadsRepliesMerged.json")
        f1 = open(filename)

        threadsData = json.load(f1)

        # return all threads
        # if querySymptom is None:
        #     return Response(symptomsData, status=status.HTTP_200_OK)

        repliesDict = defaultdict(list)
        threads     = defaultdict(list)

        data["threads"] = {}
        for relatedSymptom in relatedSymptoms:
            data["threads"][relatedSymptom] = []
            for l1 in threadsData:
                if relatedSymptom in l1["title"] or relatedSymptom in l1["body"]:
                    data["threads"][relatedSymptom].append(l1)
                else:
                    for text in l1["replies"]:
                        if relatedSymptom in text:
                            data["threads"][relatedSymptom].append(l1)
                            break

        return Response(data, status=status.HTTP_200_OK)
