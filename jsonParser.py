import json
from collections import defaultdict
import functools
from nltk.util import ngrams
import re



def printTitles(titles):
    for title in titles:
        print("title:", title)
        print("tags:", titles[title]["tags"])
        print("numberOfReplies:", titles[title]["numberOfReplies"])
        print("threadBody:", titles[title]["threadBody"])
        if titles[title]["numberOfReplies"] > 0:
            print("replyText:", titles[title]["replyText"])
            print("length(replyText):", len(titles[title]["replyText"]))
        print("\n\n")
    return


def cleanText(dirtyText):
    return [x for x in map(functools.partial(re.sub, r'[^a-zA-Z0-9\\s\\t\\n\\r]', ' '), replyText)]

def populateThreadTitles(lines, titles):
    for line in lines:
        # each line is a string is of the form
        # {
        #     'title': ['Meal Replacements for Type II'],
        #     'tags': ['Type 2 Diabetes'],
        #     'numberOfReplies': 4,
        #     'threadBody': ['\r\n\t\t\t    Is it a good idea to use meal replacement shakes for breakfast and lunch if you are type II?', '\r\n\t\t\t']
        # },
        # except the last line, so remove the trailing "," to make every string a valid json
        if line[-1] == ",":
            line = line[:-1]
        jsonLine = json.loads(line)

        # get all the discussion threads
        if "title" in jsonLine:
            title           = jsonLine["title"][0]
            # temp = map(functools.partial(re.sub, r'[^a-zA-Z0-9\\s\\t\\n\\r]', ' '), replyText)
            # replyText = []
            # for k in temp:
            #     replyText.append(k)
            replyText = cleanText(dirtyText)
            tags            = jsonLine["tags"]
            numberOfReplies = jsonLine["numberOfReplies"]
            threadBody      = jsonLine["threadBody"]

            titles[title]["tags"]            = jsonLine["tags"]
            titles[title]["numberOfReplies"] = jsonLine["numberOfReplies"]
            titles[title]["threadBody"]     = jsonLine["threadBody"]
    return titles


def populateReplies(lines, titles):
    for line in lines:
        if line[-1] == ",":
            line = line[:-1]
        jsonLine = json.loads(line)

        # get all the discussion threads
        if "threadId" in jsonLine:
            threadId  = jsonLine["threadId"][0]
            replyText = jsonLine["replyText"]
            temp      = map(functools.partial(re.sub, r'[^a-zA-Z0-9\\s\\t\\n\\r]', ' '), replyText)
            replyText = []
            for k in temp:
                replyText.append(k)
            if threadId not in titles:
                print(threadId, "not in threads!!")
                exit(1)
            if "replyText" not in titles[threadId]:
                titles[threadId]["replyText"] = []
            titles[threadId]["replyText"].extend(replyText)
    return titles


def mapTitlesToId(titles, idToTitleMap, titleToIdMap):
    counter = 0
    for key in titles:
        counter += 1
        idToTitleMap[counter] = key
        titleToIdMap[key] = counter
    return


def mapSentenceToTitleId(titles, sentenceToTitleIdMap, titleToIdMap):
    for title in titles:
        idx = titleToIdMap[title]
        sentenceToTitleIdMap[title] = idx
        for s in titles[title]["threadBody"]:
            sentenceToTitleIdMap[s] = idx
        if "replyText" in titles[title]:
            for s in titles[title]["replyText"]:
                sentenceToTitleIdMap[s] = idx

with open('data/diabetes_30pages.json') as f:
    # ignore the first and last line as they are [, ] respectively
    lines = f.read().splitlines()[1:-1]

    # store the titles and the associated fields ie. tags, #replies, threadBody
    titles = defaultdict(defaultdict)

    populateThreadTitles(lines, titles)
    populateReplies(lines, titles)


    idToTitleMap         = {}
    titleToIdMap         = {}
    sentenceToTitleIdMap = {}
    mapTitlesToId(titles, idToTitleMap, titleToIdMap)
    mapSentenceToTitleId(titles, sentenceToTitleIdMap, titleToIdMap)
    print(sentenceToTitleIdMap)
    # printTitles(titles)

exit(0)
# build the feature set
for key in titles:
    threadBody = titles[key]["threadBody"]
    for s in threadBody:
        # 1. build the n-grams
        s      = s.lower()
        s      = re.sub(r'[^a-zA-Z0-9\\s\\t\\n\\r]', ' ', s)
        tokens = [token for token in s.split(" ") if token != ""]
        output = list(ngrams(tokens, 3))
        # print(output)
        # 6. morphological features

    replyText  = titles[key]["replyText"]

# 2. semantic features
# 3. position based features: NOT USED
# 4. user based features: NOT USED
# 5. tag based features: TODO




