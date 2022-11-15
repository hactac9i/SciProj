import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd

data = open(r'C:\Users\...\spec.txt', encoding = 'utf-8')

name = input('Введите имя исследуемого образца: ')
data_list = []
for line in data:
    data_list.append(line.split())


del  data_list[0:11]

for i in range(len(data_list)):
    for j in range(3):
        data_list[i][j] = data_list[i][j].replace(',','')
        data_list[i][j] = float(data_list[i][j])


df = pd.DataFrame(data_list)
header_columns = ['WL(nm)', 'Abs', 'T%']
df = pd.DataFrame(df.values[1:], columns=header_columns)
print(df.reset_index(drop=True))
df.to_csv('output.csv', index=False, sep=';')
data.close()

#простая визуализация
import matplotlib.pyplot as plt
import numpy as np

x = np.array(df['WL(nm)'])
y = np.array(df['Abs'])

#сглаживание
from scipy.signal import savgol_filter
y_filtered = savgol_filter(y, 99, 5)

for i in range(len(df['Abs'])):
    df['Abs'][i] = y_filtered[i]

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel('WL(nm)',fontsize = 15,    #  размер шрифта
              color = 'black')    #  цвет шрифта
              #  параметры области с текстом

ax.set_ylabel('Abs', fontsize = 15,    #  размер шрифта
              color = 'black')    #  цвет шрифта

ax.grid(color = 'blue',    #  цвет линий
        linewidth = 0.1,    #  толщина
        linestyle = '--')    #  начертание
ax.set_title(f'Электронный спектр поглощения {name}')
plt.show()
fig.savefig(f'saved_figure-100dpi{name}200_1100.png', dpi = 100)

df_MB = df[df['WL(nm)'] > 450]
max_WL = df_MB.loc[df_MB['Abs'].idxmax(), 'WL(nm)']
max_Abs = max(df_MB['Abs'])
print(max_Abs)
print(max_WL)

x = np.array(df_MB['WL(nm)'])
y = np.array(df_MB['Abs'])
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel('WL(nm)',fontsize = 15,    #  размер шрифта
              color = 'black')    #  цвет шрифта
              #  параметры области с текстом

ax.set_ylabel('Abs', fontsize = 15,    #  размер шрифта
              color = 'black')    #  цвет шрифта

ax.grid(color = 'blue',    #  цвет линий
        linewidth = 0.1,    #  толщина
        linestyle = '--')    #  начертание
ax.set_title(f'Электронный спектр поглощения {name}')

ax.text((max_WL+50), (max_Abs-0.5), f'WL(nm) = {max_WL} \n Abs = {round(max_Abs,3)}',
        fontsize = 10)

plt.show()
fig.savefig(f'saved_figure-100dpi{name}450_900.png', dpi = 100)

