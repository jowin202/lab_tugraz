import time
import csv
import matplotlib.pyplot as plt
from statistics import mean
from math import pi


def PolygonArea(x, y):
    A = 0.0
    n = len(x)
    for i in range(n):
        j = (i+1)%n
        A += x[i] * y[j]
        A -= x[j] * y[i]
    A = abs(A)/2
    A *= 0.0001 # change unit to 1 Joule
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




def read_freq_from_file(filename):
    with open(filename) as csv_file:
        reader = csv.reader(csv_file, delimiter=';')
        header_row = next(reader)


        #for index, column_header in enumerate(header_row):
        #    print(index, column_header)
            
        
        freq = []
        freq2 = []
        
        
        count = 0
        for row in reader:
            if row[5] != '':
                freq += [float(row[1].replace(',', '.'))]
                freq2 += [float(row[5].replace(',', '.'))]
            count += 1
            if count == 30:
                break
    
    return freq,freq2



def CalcAreaTimeSeries(p, V):
    maxima = findMax(p)
    
    Areas = []
    for i in range(len(maxima)-1):
        Areas.append(PolygonArea(p[maxima[i]:maxima[i+1]], V[maxima[i]:maxima[i+1]] ))
    return Areas


def CalcCycleTimeSeries(p, V):
    maxima = findMax(p)
    
    result = []
    for i in range(len(maxima)-1):
        result.append(maxima[i+1]-maxima[i])
    return result

def analyzeAreas(Areas):
    mw = mean(Areas)
    print("Mittelwert: " + str(mw))
    print("Spannweite: " + str(max(Areas) - min(Areas)))





druck_un, vol_un = read_druck_volumen_from_file('unbelastet.csv')
druck_be, vol_be = read_druck_volumen_from_file('belastet.csv')


plt.title("Stirlingmotor unbelastet")
plt.plot(druck_un)
plt.plot(vol_un)
plt.legend(["Druck", "Volumen"])
plt.xlabel("Zeit / ms")
plt.ylabel("Druck / hPa bzw. Volumen / cm3")
plt.savefig("graphics/graphs_unbelastet.png")
plt.close()


plt.title("Stirlingmotor belastet")
plt.plot(druck_be)
plt.plot(vol_be)
plt.legend(["Druck", "Volumen"])
plt.xlabel("Zeit / ms")
plt.ylabel("Druck / hPa bzw. Volumen / cm3") 
plt.savefig("graphics/graphs_belastet.png")
plt.close()
    

# pV Diagramm
plt.title("pV Diagramm")
plt.plot(vol_un, druck_un)
plt.plot(vol_be, druck_be)
plt.xlabel("Volumen / cm3")
plt.ylabel("Druck / hPa bzw Volumen / cm3")
plt.legend(["unbelastet", "belastet"])
plt.savefig("graphics/pV.png")
plt.close()


# Flaechen
print("Unbelelastet: ")
area_un = CalcAreaTimeSeries(druck_un, vol_un)
analyzeAreas(area_un)
print("Belelastet: ")
area_be = CalcAreaTimeSeries(druck_be, vol_be)
analyzeAreas(area_be)


# doing a fancy latex output for copy & paste to script
print("Area per round: ")
for i in range(max(len(area_un), len(area_be))):
    print(str(i+1) + " & " + str(round(area_un[i],4) if i < len(area_un) else "") + " & " + str(round(area_be[i],4)) + " \\\\")

print("Zyklusdauern: ")
cycl_un = CalcCycleTimeSeries(druck_un, vol_un)
cycl_be = CalcCycleTimeSeries(druck_be, vol_be)

for i in range(max(len(cycl_un), len(cycl_be))):
    print(str(i+1) + " & " + str(cycl_un[i] if i < len(cycl_un) else "") + " & " + str(cycl_be[i]) + " \\\\")

print("\\hline")
print("Mittelwert: & " + str(mean(cycl_un)) + " & " + str(mean(cycl_be)) + " \\\\")
print("Spannweite: & " + str(max(cycl_un)-min(cycl_un)) + " & " + str(max(cycl_be)-min(cycl_be)) + " \\\\")


print("")
print("")

delta_t = max(max(cycl_un)-min(cycl_un), max(cycl_be)-min(cycl_be)) #spannweite
delta_t /= 1000 # in sekunden

spannweite_area_un = max(area_un) - min(area_un)
spannweite_area_be = max(area_be) - min(area_be)

mean_area_un = mean(area_un)
mean_area_be = mean(area_be)

mean_cycl_un = mean(cycl_un)/1000
mean_cycl_be = mean(cycl_be)/1000

print("Leistungsberechnung: ")
print("Leistung unbelastet: " + str(mean_area_un/mean_cycl_un))
print("Leistung belastet: " + str(mean_area_be/mean_cycl_be))
print("Leistung_unsicherheit unbelastet: " + str(spannweite_area_un/mean_cycl_un + mean_area_un/mean_cycl_un**2 * delta_t))
print("Leistung belastet: " + str(spannweite_area_be/mean_cycl_be + mean_area_be/mean_cycl_be**2 * delta_t))






print("")
print("")

print("Mit Wasser abtransportierte Leistung:")
rho_w = 998
c = 4186
T_un = 5
T_be = 6.1
dVpdt = 200.0/49 * 10**-6
Delta_Temp = 0.25
Delta_time = 0.1
Delta_Vol = 1.5*10**-6

V_W = 200*10**-6
t_W = 49

print("P unbelastet: " + str(rho_w * c * T_un * dVpdt))
print("P belastet: " + str(rho_w * c * T_be * dVpdt))


print("Unsicherheit unbelastet: " + str( rho_w * c * ( Delta_Temp *  V_W/t_W + T_un * Delta_Vol/t_W + T_un * V_W / t_W**2 * Delta_time  )))
print("Unsicherheit belastet: " + str( rho_w * c * ( Delta_Temp *  V_W/t_W  + T_be * Delta_Vol/t_W + T_be * V_W / t_W**2 * Delta_time  )))












#frequenzspektrum
freq_un,freq_un2 = read_freq_from_file("unbelastet.csv")
freq_be,freq_be2 = read_freq_from_file("belastet.csv")




plt.title("Frequenzspektrum")
plt.plot(freq_un, freq_un2)
plt.plot(freq_be, freq_be2)
plt.ylabel("Volumen / cm3")
plt.xlabel("Frequenz / Hz")
plt.legend(["unbelastet", "belastet"])
plt.savefig("graphics/freq.png")
plt.close()




print("")
print("")
print("")


print("Drehmoment:")
print("")

print("P mech: " + str(0.55 * 0.25 * 2*pi/mean_cycl_be))
print("Delta P mech: " + str( (0.05 * 0.25 + 0.55 * 0.001)/mean_cycl_be + 0.55*0.25/mean_cycl_be**2 * 0.002))
