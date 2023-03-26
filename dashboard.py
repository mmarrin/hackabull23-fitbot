import matplotlib.pyplot as plt
import json

temperatures = []
humidity = []
co = []
blood_pressure = []
heart_rate = []
sp = []

with open("data.json") as file:
    all_data = json.load(file)
    for reading in all_data:
        if reading["name"] == "temperature":
            temperatures.append(reading["value"])
        elif reading["name"] == "Humidity":
            humidity.append(reading["value"])
        elif reading["name"] == "CO2":
            co.append(reading["value"])
        elif reading["name"] == "Blood Pressure":
            blood_pressure.append(reading["value"])
        elif reading["name"] == "Heart Rate":
            heart_rate.append(reading["value"])
        elif reading["name"] == "SPO2":
            sp.append(reading["value"])

plt.style.use("seaborn-pastel")
fig, ax = plt.subplots()
ax.plot(list(range(len(temperatures))), [float(temperature) for temperature in temperatures], linewidth=3)
ax.set_title("Temperature", fontsize=24)
plt.show()

plt.style.use("seaborn-pastel")
fig, ax = plt.subplots()
ax.plot(list(range(len(humidity))), [float(humidity) for humidity in humidity], linewidth=3)
ax.set_title("Humidity", fontsize=24)
plt.show()

plt.style.use("seaborn-pastel")
fig, ax = plt.subplots()
ax.plot(list(range(len(co))), [float(co) for co in co], linewidth=3)
ax.set_title("Carbon Dioxide", fontsize=24)
plt.show()

plt.style.use("seaborn-pastel")
fig, ax = plt.subplots()
ax.plot(list(range(len(heart_rate))), [float(heart_rate) for heart_rate in heart_rate], linewidth=3)
ax.set_title("Heart Rate", fontsize=24)
plt.show()

plt.style.use("seaborn-pastel")
fig, ax = plt.subplots()
ax.plot(list(range(len(blood_pressure))), [float(blood_pressure) for blood_pressure in blood_pressure], linewidth=3)
ax.set_title("Blood Pressure", fontsize=24)
plt.show()

plt.style.use("seaborn-pastel")
fig, ax = plt.subplots()
ax.plot(list(range(len(sp))), [float(sp) for sp in sp], linewidth=3)
ax.set_title("SPO2", fontsize=24)
plt.show()
