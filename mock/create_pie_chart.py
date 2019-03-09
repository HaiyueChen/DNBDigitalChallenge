import matplotlib.pyplot as plt
import numpy as np

def pie_chart(amounts=[6000.00, 3200.00, 15000.00, 2000.00, 0.00, 2000.00, 100.00]):
    categories = "Mat og drikke", "Bil og transport","Bolig og fritidsbolig","Ferige og fritid",  "Sparing","Øvrige utgifter","Ikke kategorisert"
    colors = ['#f44242', '#f48641','#f4d041','#caf441','#41f44f','#41dff4','#f44176']

    plt.pie(amounts, labels=categories, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig('./pie.png')

pie_chart()
