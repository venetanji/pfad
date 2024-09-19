import matplotlib.pyplot as plt
import csv
import matplotlib

matplotlib.rcParams['font.family'] = 'Microsoft YaHei'
data = []

with open('latest_1min_temperature_sc.csv', newline='', encoding='utf-8') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

    next(spamreader)

    for row in spamreader:
    
        if not row:
            continue
        
        location = row[1] 
        temperature = float(row[2]) 
        
        data.append((location, temperature))
        
        print(data)
        


fig, ax = plt.subplots(figsize=(10, 6))

locations, temperatures =([record[0] for record in data], [float(record[1]) for record in data])

ax.bar(locations, temperatures, color='green')

ax.set_title('香港各地点一分钟温度', fontsize=16)
ax.set_xlabel('地点', fontsize=3)
ax.set_ylabel('温度 (°C)', fontsize=14)

ax.set_xticklabels(locations, rotation=45, ha='right', fontsize=12)

plt.tight_layout()

plt.show()
