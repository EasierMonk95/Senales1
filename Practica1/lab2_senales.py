#Laboratorio 2 Correlacion
import scipy.io.wavfile
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats

print("Presiona 1 para la correlacion entre señales\nPresiona 2 para radar")
print("Presiona 3 para correlacion Pearson y Spearman")
entry = int(input("Respuesta: "))

if(entry == 1):

        #Llamamos el archivo .wav con el que se trabajara
        #Y se procede a seguir con la guia
        #La ubicacion del archivo se cambian \ por / 
        fs,x = scipy.io.wavfile.read('audio.wav')
        t = np.arange(0, len(x)/fs, 1.0/fs)
        
        x=x/float(np.max(np.abs(x))) 
        #Es necesario sacar la amplitud maxima de la señal debido a problemas con la correlacion
        #Maximo del valor absoluto de x

        
        decision = int(input("Para graficar en un segmento con voz presiona 1\nPara un segmento sordo presiona 2: "))
        
        if(decision == 1):
            #Almacenar fragmento de la señal en otra variable
            #Determino los rangos a fraccionar
            inicio = 1.6
            fin = 2.0
            seg1 = int(inicio*fs) #Deben ser enteros debido a errores de integracion
            seg2 = int(fin*fs) #Al multiplicarlo por fs, da el valor que necesito para la señal
            segment = x[seg1:seg2] #Valores de x en el rango dado (enteros)
            t2 = np.arange(0, len(segment)/fs , 1.0/fs)
            
    
        
            #Ahora se implementara la autocorrelación
        
            corr = np.correlate(segment, segment,"full")/fs
            #correlacion = np.correlate(x,segment,'full')
            #Parametros: a,v array like , mode {valid,same,full}
            t_c = np.arange(-len(segment)/fs, len(segment)/fs- 1.0/fs, 1.0/fs)
            #El segmento va viajando en el tiempo por tanto se toma desde -su longitud hasta su longitud
        
        
            
            plt.subplot(3,1,1) #Parametros del subplot (Numrow,NumCol,NumFigure)
            plt.plot(t,x)
            plt.grid()
            plt.gcf().set_size_inches((15, 15)) #Aumenta la visibilidad de la señal
                                                #Con mayor resolucion
            plt.subplot(3,1,2)
            plt.plot(t2,segment,'r')
            plt.grid()
            plt.gcf().set_size_inches((15, 15))
            
            plt.subplot(3,1,3)
            plt.plot(t_c,corr)
            plt.grid()
            plt.gcf().set_size_inches((15, 15))
            
        
        elif(decision == 2):
            #Implementando la correlacion con un segmento sordo
            inicio2 = 4.0
            fin2 = 4.3
            seg1_sordo = int(inicio2*fs)
            seg2_sordo = int(fin2*fs)
            segment2 = x[seg1_sordo:seg2_sordo]
            t3 = np.arange(0, len(segment2)/fs , 1.0/fs)
            
            #plt.plot(t2,segment2)
            
            #Crear una señal aleatoria con np.random.normal
            #Ahora le ingresamos ruido a la señal
            Ruido = np.random.normal(0,0.3,len(segment2))
            segment2+=Ruido

            
            corr2 = np.correlate(segment2, segment2,"full")/fs
            t_c2 = np.arange(-len(segment2)/fs, len(segment2)/fs- 1.0/fs, 1.0/fs)
            
            plt.subplot(3,1,1) #Parametros del subplot (Numrow,NumCol,NumFigure)
            plt.plot(t,x)
            plt.grid()
            plt.gcf().set_size_inches((15, 15))
            
            plt.subplot(3,1,2)
            plt.plot(t3,segment2)
            plt.grid()
            plt.gcf().set_size_inches((15, 15))
            
            plt.subplot(3,1,3)
            plt.plot(t_c2,corr2)
            plt.grid()
            plt.gcf().set_size_inches((15, 15))
            
        else: print("\nOpcion no valida")
       
    
elif(entry == 2):
    
    #Lo primero es crear el pulso de la señal x(n)
    n=1000 #Cantidad de puntos
    rango = np.linspace(-10,10,n) #Crea un vector de 1000 puntos de -10 a 10 en cantidades iguales
    #numpy.zeros crea un array de ceros
    pulse = np.zeros(n)
    pulse[500:550] = 1 #Se asignan los valores de 1 en un rango de 500 a 550
    
    '''
    plt.plot(rango,pulse,'r')
    plt.xlabel("Tiempo")
    plt.ylabel("Amplitud")
    plt.grid()
    '''
    
    #Calculamos el ciclo de dureza del pulso
    duty_C = sum(pulse)*100/n #5% de la señal
    print("El ciclo de dureza de la señal es ",duty_C, end="%")

    #Ahora atenuamos la señal al 50%
    pulse_at = pulse/2
    
    
    move_t = np.roll(pulse_at, 200)
    
    #plt.plot(rango, move_t)
    
    #Una vez hecho, se hace una afectacion en el canal con relacion al ruido
    #Se genera ruido Gausiano
    desvi = 0
    boolie= False
    while(boolie == False):
        desvi = int(input("Para una desviacion de 0.3 presiona 1\nPara una desviacion de 0.7 presiona 2\nRespuesta: ")) 
        if(desvi == 1):
            Gauss_Noise = np.random.normal(0,0.3,n) #Inicio, escala, tamaño
            boolie=True
        elif(desvi == 2):
            Gauss_Noise = np.random.normal(0,0.7,n)
            boolie=True
        else: 
            print("Valor no permitido")
            boolie=False
    
    move_t+=Gauss_Noise
    
    corr = np.correlate(pulse, move_t,"same")
    plt.plot(rango,corr)
    
    
elif(entry == 3):
    print("Correlacion pearson y spearman")
    #Leemos el archivo de excel utilizando la libreria pandas
    df = pd.read_excel("DatosCorrelacion.xlsx")
    #print(df)
    #Creamos un vector columna para cada uno
    edad = df["Edad"].values
    N_calculo = df["Nota calculo"].values
    N_informatica = df["Nota informatica"].values
    
    '''
    print(edad)
    print(N_calculo)
    print(N_informatica)
    '''
    
    plt.subplot(2,1,1)
    plt.xlabel("Nota informatica")
    plt.ylabel("Nota calculo")
    plt.scatter(N_informatica,N_calculo)
    plt.grid()
   
    
    plt.subplot(2,1,2)
    plt.xlabel("Edad")
    plt.ylabel("Nota calculo")
    plt.scatter(edad,N_calculo)
    plt.tight_layout()
    plt.grid()
    plt.gcf().set_size_inches((8, 8))
    
    '''
    En la primera grafica de nota_calculo vs nota_informatica se puede apreciar
    que hay demasiada similutud de notas, es decir que los estudiantes que tienen
    buenas notas en calculo, tienen notas muy similares en informatica
    
    En la segunda grafica de edad vs Nota_calculo no tienen una correlacion clara
    por lo que se puede afirmar que no hay mucha similitud entre estas 
    '''
    
    corr1_pearson = stats.pearsonr(N_calculo, N_informatica).statistic
    corr1_spearman = stats.spearmanr(N_calculo, N_informatica).correlation
    corr2_pearson = stats.pearsonr(edad, N_calculo).statistic
    corr2_spearman = stats.spearmanr(edad, N_calculo).correlation
    
    print("Coeficiente de correlacion Pearson entre Nota informatica y Nota calculo\n",corr1_pearson)
    print("Coeficiente de correlacion Spearman entre Nota informatica y Nota calculo\n",corr1_spearman)
    print("Coeficiente de correlacion Pearson entre edad y Nota calculo \n",corr2_pearson)
    print("Coeficiente de correlacion Spearman entre edad y Nota calculo\n",corr2_spearman)
    
    '''
    Como se evidencio en las partes anteriores del laboratorio la correlacion
    mientras mas similar sea entre dos señales debe tender a 1 y como se evidencia
    en la correlacion de pearson y spearman de Nota de informatica y Nota calculo
    es muy cercano a 1, por lo que hay demasiada similutud entre ambas funciones
    Mientras que al evidenciar la correlacion entre edad y Notas calculo es muy diferente
    a 1 por lo que no hay casi similitud
    '''
    
    '''
    Comparandolo con el iterario anterior se puede concluir que si concuerda la 
    respuesta anterior con la actual debido a los resultados obtenidos
    '''