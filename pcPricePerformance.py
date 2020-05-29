from pcpartpicker import API
import json
import os
import csv
import re
from datetime import datetime

# rm ulCPU.json ulGPU.json
# scrapy crawl ulCPU -o ulCPU.json
# scrapy crawl ulGPU -o ulGPU.json

os.chdir(os.path.dirname(os.path.realpath(__file__)))
print(os.path.abspath("."))

mode = "both"

cpuBlacklists = re.compile(r'i[3-9]-[2-7]|i[3-9]-\d{3}$|FX-|1300X|1400|1500X|2400G')
gpuBlacklists = re.compile(r'Quadro|GT |HD |GTX [3-9]|R[5-9]|Titan|GTX 10|RX 4')

api = API()
date = datetime.today().strftime('%Y-%m-%d')

if mode != "gpu":
    try:
        os.remove('ulCPU.json')
    except OSError:
        pass

    os.system('scrapy crawl ulCPU -o ulCPU.json')

    cpu_data = api.retrieve("cpu")
    pcppCPUs = {}
    print(len(cpu_data["cpu"]), "pcpartpicker cpus")
#    print(cpu_data["cpu"][0])
    for cpu in cpu_data["cpu"]:
        if not cpu.price.amount.is_zero() and not cpuBlacklists.search(cpu.model):
            model = cpu.model
            if "Core i" in model:
                model += " "
            if model in pcppCPUs:
                pcppCPUs[model]["price"] = min(pcppCPUs[model]["price"], cpu.price.amount)
            else:
                pcppCPUs[model] = {"cores":cpu.cores, "price":cpu.price.amount, "brand":cpu.brand}
    print(len(pcppCPUs), "pcpartpicker cpus with prices")

    ulCPUs = json.load(open(os.path.join(os.path.dirname(__file__), 'ulCPU.json'), "rb" ))

    matches = {}
    for model in pcppCPUs:
        for ulCPU in ulCPUs:
            if (model.lower() in ulCPU["model"].lower() or ulCPU["model"].lower() in model.lower()) and ulCPU["performance"] > 0:
                modelShort = model.replace("Core ","")\
                .replace("Ryzen 3 ","")\
                .replace("Ryzen 5 ","")\
                .replace("Ryzen 7 ","")\
                .replace("Ryzen 9 ","")
                matches[modelShort] = {**pcppCPUs[model], **ulCPU}
#                print(model, matches[model])
    print(len(matches), "matches")

    with open(os.path.join(os.path.dirname(__file__), 'cpus-'+date+'.csv'), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Model","Price","Performance","Brand","Popularity","Cores"])
        for model in matches:
            spamwriter.writerow([model, str(matches[model]["price"]), matches[model]["performance"], matches[model]["brand"], matches[model]["popularity"], matches[model]["cores"]])

if mode != "cpu":
    try:
        os.remove('ulGPU.json')
    except OSError:
        pass

    os.system('scrapy crawl ulGPU -o ulGPU.json')

    gpu_data = api.retrieve("video-card")
    pcppGPUs = {}
    print(len(gpu_data["video-card"]), "pcpartpicker gpus")
    for gpu in gpu_data["video-card"]:
        if not gpu.price.amount.is_zero() and not gpuBlacklists.search(gpu.chipset):
            model = gpu.chipset
            if model in pcppGPUs:
                pcppGPUs[model]["price"] = min(pcppGPUs[model]["price"], gpu.price.amount)
            else:
                pcppGPUs[model] = {"price":gpu.price.amount}
    print(len(pcppGPUs), "pcpartpicker gpus with prices")

    ulGPUs = json.load(open(os.path.join(os.path.dirname(__file__), 'ulGPU.json'), "rb" ))

    matches = {}
    for model in pcppGPUs:
        for ulGPU in ulGPUs:
            if (model.lower() in ulGPU["model"].lower() or ulGPU["model"].lower() in model.lower()) and ulGPU["performance"] > 0 and "2048SP" not in ulGPU["model"]:
                if ("Radeon VII" not in model):
                    modelShort = model.replace("Radeon ","").replace("GeForce ","")
                else:
                    modelShort = model
                matches[modelShort] = {**pcppGPUs[model], **ulGPU}
                if "NVIDIA" in ulGPU["model"]:
                    matches[modelShort]["brand"] = "Nvidia"
                elif any(x in ulGPU["model"] for x in ["AMD","ATI"]):
                    matches[modelShort]["brand"] = "AMD"
    print(len(matches), "matches")

    with open(os.path.join(os.path.dirname(__file__), 'gpus-'+date+'.csv'), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Model","Price","Performance","Brand","Popularity"])
        for model in matches:
            spamwriter.writerow([model, str(matches[model]["price"]), matches[model]["performance"], matches[model]["brand"], matches[model]["popularity"]])