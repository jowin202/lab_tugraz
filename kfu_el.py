from math import sqrt
import matplotlib.pyplot as plt

#as found in german wikipedia
def orthogonal_regression(x,y):
	xd = sum(x)/len(x)
	yd = sum(y)/len(y)
	sx = sum([(a-xd)**2 for a in x])/(len(x)-1)
	sy = sum([(b-yd)**2 for b in y])/(len(y)-1)
	sxy = sum( [ (x[i] - xd)*(y[i]-yd) for i in range(len(x))] )/(len(x)-1)
	beta1 = (sy-sx + sqrt( (sy-sx)**2 + 4*sxy**2))/(2*sxy)
	beta0 = yd - beta1 * xd
	return beta0, beta1
	
def calc_emodul(L, beta, I):
    return L**3/(48.0 * beta/100.0 * I) #in m/N

def calc_emodul_deviation(L, delta_L, beta, I, delta_I, delta_beta):
    #in m/N
    res = L**2 / (48.0 * beta/100.0 * I) * (3 * delta_L + L * delta_beta/(beta/100.0) + L * delta_I/I)
    return res


def calc_delta_beta(F, h):
    delta_h = 1/10 # in cm
    delta_F = 0.01
    beta_max = (h[-1] - h[1] + 2 * delta_h)/(F[-1] - F[1] - 2 *delta_F)
    beta_min = (h[-1] - h[1] - 2 * delta_h)/(F[-1] - F[1] + 2 *delta_F)
    return (beta_max - beta_min)/100 # convert to m/N .






g = 9.81
m = [0.5 * i for i in range(0,11)]

F = [g*x for x in m]


#gemessene Daten
h1 = [0,0.2,0.4,0.6,0.8,1.0,1.1,1.4,1.5,1.8,1.9]
h2 = [0,1.1,1.5,2.2,3.3,3.7,4.4,5,6.2,7,7.3]
    

beta0_1, beta1_1 = orthogonal_regression(F,h1) #stab 
beta0_2, beta1_2 = orthogonal_regression(F,h2) #brett
    






# for the drawing of the line
x = [0,50]
y1 = [beta0_1, beta0_1 + 50*beta1_1] #stab
y2 = [beta0_2, beta0_2 + 50*beta1_2] #brett


print("Regression:")
print("h_1 = " + str(round(beta0_1,4)) + " cm + " + str(round(beta1_1,4)) + " cm/N * F ") #stab
print("h_2 = " + str(round(beta0_2,4)) + " cm + " + str(round(beta1_2,4)) + " cm/N * F " ) #brett



plt.title("Holzstab")
plt.scatter(F,h1)
plt.plot(x,y1)
plt.xlabel("Kraft / N")
plt.ylabel("Auslenkung / cm")
#plt.show()
plt.savefig("regression1.png")
plt.close()

plt.title("Holzbrett")
plt.scatter(F,h2)
plt.plot(x,y2)
plt.xlabel("Kraft / N")
plt.ylabel("Auslenkung / cm")
#plt.show()
plt.savefig("regression2.png")
plt.close()



L = 0.50
delta_L = 1/1000 #global
h_stab = 8/1000
h_brett = 3/1000
b_stab = 24/1000
b_brett = 87/1000

delta_b = 1/1000 # 1mm
delta_h = 1/1000

Iy_stab = b_stab * h_stab ** 3/12.0
Iy_brett = b_brett * h_brett ** 3/12.0

Delta_Iy_stab = ( delta_b * h_stab**3 + 3*b_stab*h_stab**2 * delta_h )/12.0
Delta_Iy_brett = ( delta_b * h_brett**3 + 3*b_brett*h_brett**2 * delta_h)/12.0


print("I Holzstab: " + str(Iy_stab) + " +- " + str(Delta_Iy_stab))
print("I Holzbrett: " + str(Iy_brett) + " +- " + str(Delta_Iy_brett))



delta_beta_1 = calc_delta_beta(F, h1)
delta_beta_2 = calc_delta_beta(F, h2)


e_stab = calc_emodul(L, beta1_1, Iy_stab)
e_brett = calc_emodul(L, beta1_2, Iy_brett)

e_stab_dev = calc_emodul_deviation(L,delta_L,beta1_1,Iy_stab,Delta_Iy_stab,delta_beta_1)
e_brett_dev = calc_emodul_deviation(L,delta_L,beta1_2,Iy_brett,Delta_Iy_brett,delta_beta_2)


print("Holzstab: " + str(e_stab) + " +- " + str(e_stab_dev))
print("Holzbrett: " + str(e_brett) + " +- " + str(e_brett_dev))
