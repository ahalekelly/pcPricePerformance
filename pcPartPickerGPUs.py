from pcpartpicker import API
import json
import os
import csv

api = API()
cpu_data = api.retrieve("gpu")
pcppCPUs = {}
print(len(cpu_data["cpu"]), "pcpartpicker cpus")
print(cpu_data["cpu"][0])
for cpu in cpu_data["cpu"]:
    if not cpu.price.amount.is_zero():
        model = cpu.model
        if "Core i" in model:
            model += " "
        if model in pcppCPUs:
            pcppCPUs[model]["price"] = min(pcppCPUs[model]["price"], cpu.price.amount)
        else:
            pcppCPUs[model] = {"cores":cpu.cores, "price":cpu.price.amount, "brand":cpu.brand}
print(len(pcppCPUs), "pcpartpicker cpus after dedup")

ulCPUs = json.load(open(os.path.join(os.path.dirname(__file__), 'ulCPU.json'), "rb" ))

matches = {}
for model in pcppCPUs:
    for ulCPU in ulCPUs:
        if model in ulCPU["model"]:
            matches[model] = {**pcppCPUs[model], **ulCPU}
            print(model, matches[model])
print(len(matches), "matches")

with open(os.path.join(os.path.dirname(__file__), 'cpus.csv'), 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(["Model","Price","Performance","Brand","Popularity","Cores"])
    for model in matches:
        spamwriter.writerow([model, str(matches[model]["price"]), matches[model]["performance"], matches[model]["brand"], matches[model]["popularity"], matches[model]["cores"]])