import json
import random
import pickle
import numpy as np
from py4j.java_gateway import JavaGateway
import tensorflow
import tflearn
from tensorflow.python.framework import ops
from tensorflow.python.keras.models import load_model

with open("intents.json") as file:
    data = json.load(file)

gateway = JavaGateway()  # connect to the JVM
mytest = gateway.entry_point
try:
    with open("data.pickle", "rb") as f:
        words, classes, training, output = pickle.load(f)
except:
    words = []
    documents = []
    docs_x = []
    docs_y = []

    classes = []
    for intent in data["intents"]:
        Tag = intent["tag"]
        classes.append(Tag)
        for patterns in intent["patterns"]:
            value = mytest.tokenize(patterns, Tag)
            docs_x.append(value)
            docs_y.append(intent["tag"])

    mytest.Analyze()
    words = mytest.getLem_Words()
    documents = mytest.get_pairs()

    words = sorted(list(set(words)))
    classes = sorted(classes)

    for doc in docs_x:
        for y in doc:
            if y == "?":
                doc.remove(y)

    training = []
    output = []

    out_empty = [0 for _ in range(len(classes))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [mytest.stemming(w) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[classes.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    with open("data.pickle", "wb") as f:
        pickle.dump((words, classes, training, output), f)

ops.reset_default_graph()
net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net, tensorboard_verbose=3)


model.fit(training, output, n_epoch=1000, batch_size=8, show_metric=True)
model.save("model.tflearn")



#
def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = mytest.sentence_tokenize(s)
    s_words = [mytest.stemming(word) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
    return np.array(bag)


# Model yüklemesi sıkıntıda her seferinde yeniden kurmak gerekiyor
# Yanlış kelime yazılması için düzeltme uygula
def chat(inp1):
    inp = inp1
    if inp.lower() == "quit":
        quit()

    results = model.predict([bag_of_words(inp, words)])
    results_index = np.argmax(results)
    tag = classes[results_index]

    for tg in data["intents"]:
        if tg["tag"] == tag:
            responses = tg['responses']
    return random.choice(responses)

