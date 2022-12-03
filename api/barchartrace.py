# Importing required libraries

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.animation as animation
from IPython.display import HTML

year=2018
fig, ax = plt.subplots(figsize=(15, 16))

def draw_barchart(year):
    animator = animation.FuncAnimation
    df= pd.read_csv("./input/provinces.csv",encoding='latin1')
    dff = df[df['year'].eq(year)].sort_values(by='population', ascending=True).tail(20)

    colors = dict(zip(
        ['Marmara Region','Aegean Region','Mediterranean Region','Central Anatolia Region','Black Sea Region','Eastern Anatolia Region','Southeast Anatolia Region'],
        ['#adb0ff', '#ffb3ff', '#90d595', '#e48381', '#aafbff', '#f7bb5f', '#eafb50']
    ))

    group_lk = df.set_index('province')['region'].to_dict()


    ax.barh(dff['province'], dff['population'], color=[colors[group_lk[x]] for x in dff['province']])
    dx = dff['population'].max() / 200
    for i, (value, name) in enumerate(zip(dff['population'], dff['province'])):
        ax.text(value-dx, i,     name,           size=14, weight=800, ha='right', va='bottom')
        ax.text(value-dx, i-.25, group_lk[name], size=8, color='#444444', ha='right', va='baseline')
        ax.text(value+dx, i,     f'{value:,.0f}',  size=14, ha='left',  va='center')
    # ... polished styles
    ax.text(1, 0.4, year, transform=ax.transAxes, color='#777777', size=46, ha='right', weight=500)
    ax.text(0, 1.06, 'Population', transform=ax.transAxes, size=12, color='#777777')
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:,.0f}'))
    ax.xaxis.set_ticks_position('top')
    ax.tick_params(axis='x', colors='#777777', labelsize=12)
    ax.set_yticks([])
    ax.margins(0, 0.01)
    ax.grid(which='major', axis='x', linestyle='-')
    ax.set_axisbelow(True)
    ax.text(0, 1.12, 'The most populous provinces in Turkey from 2007 to 2018',
            transform=ax.transAxes, size=24, weight=600, ha='left')
    ax.text(1, 0, 'by Can Iban', transform=ax.transAxes, ha='right',
            color='#777777', bbox=dict(facecolor='white', alpha=0.8, edgecolor='white'))
    plt.box(False)
    
 

def renderHtml():
    animator = animation.FuncAnimation(fig, draw_barchart, frames=range(2007, 2018))
    return HTML(animator.to_jshtml())

renderHtml()