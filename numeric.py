import time
import csv
import matplotlib.pyplot as plt


def PolygonArea(x, y):
    A = 0.0
    n = len(x)
    for i in range(n):
        j = (i+1)%n
        A += x[i] * y[j]
        A -= x[j] * y[i]
    A = abs(A)/2
    return A


def findMax(p):
    skip = 0
    maxima = []
    for i in range(len(p)-4):
        if p[i] <= p[i+1] and p[i+1] >= p[i+2] and p[i+1] > 900:
            if skip > 0:
                skip -= 1
                continue
            #print(str(i+1) + " " + str(p[i+1]))
            maxima.append(i+1)
            skip = 4
        else:
            skip = 0 if skip == 0 else skip - 1 
    return maxima


def read_druck_volumen_from_file(filename):
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header_row = next(reader)


        #for index, column_header in enumerate(header_row):
        #    print(index, column_header)
            
        
        druck = []
        vol = []
        
        

        for row in reader:
            druck += [float(row[2])]
            vol += [float(row[4].replace(',', '.'))]
    
    return druck, vol

def CalcAreaTimeSeries(p, V):
    maxima = findMax(p)
    
    Areas = []
    for i in range(len(maxima)-1):
        Areas.append(PolygonArea(p[maxima[i]:maxima[i+1]], V[maxima[i]:maxima[i+1]] ))
    print(Areas)
                







druck_un, vol_un = read_druck_volumen_from_file('unbelastet.csv')
druck_be, vol_be = read_druck_volumen_from_file('belastet.csv')


plt.title("Stirlingmotor unbelastet")
plt.plot(druck_un)
plt.plot(vol_un)
plt.legend(["Druck", "Volumen"])
plt.savefig("graphics/graphs_unbelastet.png")
plt.close()


plt.title("Stirlingmotor belastet")
plt.plot(druck_be)
plt.plot(vol_be)
plt.legend(["Druck", "Volumen"])
plt.savefig("graphics/graphs_belastet.png")
plt.close()
    

# pV Diagramm
plt.title("pV Diagramm")
plt.plot(vol_un, druck_un)
plt.plot(vol_be, druck_be)
plt.legend(["unbelastet", "belastet"])
plt.savefig("graphics/pV.png")
plt.close()


# Flaechen
CalcAreaTimeSeries(druck_un, vol_un)
CalcAreaTimeSeries(druck_be, vol_be)
