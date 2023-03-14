import json
from py4j.java_gateway import JavaGateway


with open("intents.json") as file:
    data = json.load(file)

gateway = JavaGateway()  # connect to the JVM
mytest = gateway.entry_point

mytest.Entity()