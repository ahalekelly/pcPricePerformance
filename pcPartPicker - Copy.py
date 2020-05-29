from pcpartpicker import API
import json
import os

api = API()
cpu_data = api.retrieve("cpu")
pcppCPUs = []
print(len(cpu_data["cpu"]), "pcpartpicker cpus")
for cpu in cpu_data["cpu"]:
    if not cpu.price.amount.is_zero():
        if len(pcppCPUs) is 0 or (cpu.model != pcppCPUs[-1]["model"] and cpu.model+" " != pcppCPUs[-1]["model"]):
            pcppCPUs.append({"model":cpu.model, "cores":cpu.cores, "price":cpu.price.amount})
            if "Core i" in pcppCPUs[-1]["model"]:
                pcppCPUs[-1]["model"] += " "
        else: # duplicate model
#            print(pcppCPUs[-1]["model"], pcppCPUs[-1]["price"], cpu.price.amount)
            if cpu.cores != pcppCPUs[-1]["cores"]:
                print("Duplicate model with different core counts!")
                print(pcppCPUs[-1]["model"], pcppCPUs[-1]["cores"], cpu.cores)
            pcppCPUs[-1]["price"] = min(pcppCPUs[-1]["price"], cpu.price.amount)
print(len(pcppCPUs), "pcpartpicker cpus after dedup")

ulCPUs = json.load(open(os.path.join(os.path.dirname(__file__), 'ulCPU.json'), "rb" ))

matches = 0
for cpu in pcppCPUs:
    for ulCPU in ulCPUs:
        if cpu["model"] in ulCPU["model"]:
#            print(cpu["model"], "-", ulCPU["model"])
            matches += 1
print(matches, "matches")