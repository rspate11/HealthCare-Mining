from django.core.management.base import BaseCommand, CommandError
import os
import json
from collections import defaultdict

class Command(BaseCommand):
    help = "merges the replies and the thread files"
    def handle(self, *args, **options):
        # parse the diabetes_threads.json

        f1 = open('threads/diabetes_ThreadsTyped.json')
        f2 = open('threads/diabetes_RepliesTyped.json')

        threadsData = json.load(f1)
        repliesData = json.load(f2)

        data        = []
        for l1 in threadsData:
            temp               = {}
            temp["title"]      = l1["title"]
            if l1["Type1"] is True:
                temp["type1"] = "yes"
            else:
                temp["type1"] = "no"

            if l1["Type2"] is True:
                temp["type2"] = "yes"
            else:
                temp["type2"] = "no"
            temp["body"] = l1["threadBody"]
            temp["replies"]  = []
            for l2 in repliesData:
                if temp["title"] == l2["threadId"]:
                    temp["replies"].append(l2['replyText'])
            data.append(temp)
        # with open("threadsRepliesMerged.json", "w") as f:
        #     json.dumps(data)
        f = open("threadsRepliesMerged.json", "w")
        json.dump(data, f)

        ####### this doesn't create a valid json add , and []
