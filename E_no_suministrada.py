import numpy as np
from Perfil_de_carga import PerfilCarga
from matplotlib import (use, is_interactive)
import matplotlib.pyplot as plt

use('Qt5Agg')


class Energías(PerfilCarga):
    """
    Esta clase se encarga de calcular las energías que se encuentran
    en la operación de un sistema de potencia.
    Energía no suministradas, ya sea por probabilididad de falla, por
    sobrecarga del sistema.
    Energía por generación distribuida.
    Energía por pérdidas.
    En esta clase se deben utilizar la mayoría de los valores obtenidos con
    un software que permita el estudio de sistemas de potencia.
    """

    def __init__(self, Param_DNA_red_n, DNA_red_n_1, Tasa_de_fallas,
                 Long_cond_n_1,path):
        """
        Se toman todos los valores necesarios para calcular los distintos
        tipos de energías.

        Param_DNA_red_n: Son los parámetros de la función lineal o cuadrática
        que delimita la DNA en red n a través de los años.
        DNA_red_n_1: Matriz de demanda no abastecida segun lugar de falla y
        escenario presentado a la hora de la falla. En las columnas van los
        escenarios y las filas representan cada falla. La primer columna
        representa al escenario con menor demanda y la última el de mayor.
        Tasa_de_fallas: Diccionario en el cual se tienen las tasas de
        fallas de las líneas segun el tipo y de transformadores.
        Long_cond_n_1: long de los conductores en los cuales se presentaron
        DNA en alguno de los escenarios.
        path: Ruta en donde se encuentra el perfil de carga en formato excel,
        respetando el formato base de ejemplo. UTILIZAR DOBLE BARRA INVERTIDA y
        DOBLE COMILLAS PARA LA DIRECCIÓN DE LA CARPETA.
        """
        PerfilCarga.__init__(self, path)
        self.param_red_n = Param_DNA_red_n
        self.DNA_n_1 = np.array(DNA_red_n_1)
        self.Tasa_fallas = Tasa_de_fallas
        self.Long_cond_n_1 = Long_cond_n_1

        Horas_fallas = np.zeros(len(self.Long_cond_n_1))
        for i in range(len(self.Long_cond_n_1)):
            for x in list(self.Tasa_fallas.keys()):
                if self.Long_cond_n_1[i][0] == x:
                    Horas_fallas_num = self.Long_cond_n_1[i][1]*self.Tasa_fallas[self.Long_cond_n_1[i][0]][0]*self.Tasa_fallas[self.Long_cond_n_1[i][0]][1]/100
                    Horas_fallas[i] = Horas_fallas_num

        self.Horas_fallas = Horas_fallas

    def ENS_n_1(self, Lim_Escenarios,Años,Tasa,Ppico_New):
        Probabilidad = self.Matriz_Probabilidad(Lim_Escenarios, Años, Tasa, Ppico_New).T
        Aux = np.zeros(self.DNA_n_1.shape)
        for i in range(Lim_Escenarios.size):
            Aux[i] = self.DNA_n_1[i]*self.Horas_fallas[i]
        Aux2 = np.zeros([Probabilidad.shape[0],self.DNA_n_1.shape[0]])
        for i in range(Probabilidad.shape[0]):
            for x in range(Aux.shape[0]):
                Aux2[i][x]=Aux[x].dot(np.flip(Probabilidad[i]))
        self.ENS_n_1 = Aux2
        return Aux2

    def ENS_n_1_TotalAño(self, Lim_Escenarios,Años,Tasa,Ppico_New):
        
        Aux2 = self.ENS_n_1(self, Lim_Escenarios,Años,Tasa,Ppico_New)
        Aux3 = np.zeros(Aux2.shape[0])
        for i in range(Aux2.shape[0]):
            Aux3[i] = Aux2[i].sum()

        return Aux3

    def Plot_ENS_n_1(self, Lim_Escenarios,Años,Tasa,Ppico_New):

        Aux2 = self.ENS_n_1(Lim_Escenarios,Años,Tasa,Ppico_New)
        Abs_Años = [0 for i in range(Años)]
        for i in range(Años):
            A = str(i)
            B = "Año " + A
            Abs_Años[i] = B
        indice = np.arange(len(Abs_Años))
        Aux2 = Aux2.T
        x=1
        for i in range(Aux2.shape[0]):
            if i==0:
                plt.bar(indice,Aux2[i])
            if i!=0:
                while x==i:
                    plt.bar(indice,Aux2[i],bottom=Aux2[x])
                    x+=1
        
        plt.legend()
        plt.show()









