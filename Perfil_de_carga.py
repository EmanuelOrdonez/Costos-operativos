#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np


class PerfilCarga:
    """
    Esta clase transforma de formato un perfil de carga en una sola columna y
    permite modificar la potencia máxima pico base, la cantidad de años de
    proyección y el crecimiento interanual.

    """

    def __init__(self, path):
        """
        Método constructor

        path: Ruta en donde se encuentra el perfil de carga en formato excel,
        respetando el formato base de ejemplo. UTILIZAR DOBLE BARRA INVERTIDA y
        DOBLE COMILLAS PARA LA DIRECCIÓN DE LA CARPETA.

        """
        self.path = str(path)

    def To_Array(self):
        """
        Transforma el perfil de carga en una columna con todos
        sus valores
        """
        df = pd.read_excel(self.path, sheet_name="Hoja1")
        a = []
        for i in range(df.shape[0]):
            a = np.concatenate((a, df.values[i]), axis=None)
        return a.T

    def To_excel_column(self):
        """
        Entrega el perfil de carga en una columna pero en formato excel
        """

        column = self.To_Array()
        column = pd.DataFrame(column)
        return column.to_excel("Columna_Perfil_de_Carga.xlsx")

    def Transform_base(self, Ppico_New):
        """
        Toma el perfil de carga en formato de columna y modifica todos los
        valores en base de un nuevo máximo de potencia.

        Ppico_new: Potencia pico máxima a la cual se va a adaptar [MVA].
        """
        column = self.To_Array()
        Ppico = max(column)
        NewBase = column*(Ppico_New/Ppico)
        return NewBase

    def To_excel_with_NewBase(self, Ppico_New):
        """
        Entrega el perfil de carga en una columna pero en formato excel
        """

        column = self.Transform_base(Ppico_New)
        column = pd.DataFrame(column)
        return column.to_excel("NuevaBase_Perfil_de_Carga.xlsx")

    def Crecimiento_Perfil(self, Años, Tasa, Ppico_New=1):
        """
        Función para crear una matriz de n columnas igual a la cantidad de
        años, en la cual cada columna es el perfil de carga pero afectado por
        el crecimiento interanual.

        Años: Cantidad de años a los que se quiere proyectar.
        Tasa: Tasa de crecimiento interanual supuesta para el perfil.
        """
        column = self.Transform_base(Ppico_New)
        h = np.atleast_2d(column)
        for i in range(Años):
            b = column*((1+(Tasa/100))**(i+1))
            b = np.atleast_2d(b)
            h = np.vstack((h, b))
        return h

    def To_excel_Crecimiento(self, Años, Tasa,  Ppico_New=1):
        """
        Entrega el perfil de carga año a año en formato excel
        """

        column = self.Crecimiento_Perfil(Años, Tasa, Ppico_New)
        column = column.T
        column = pd.DataFrame(column)
        return column.to_excel("Crecimiento_Perfil_de_Carga.xlsx")

    def Matriz_Probabilidad(self, Lim_Escenarios, Años, Tasa, Ppico_New=1):
        """
        Devuelve la matriz de probabilidades a traves de los años.

        Lim_escenarios: Array que posee los límites de cada escenario
        (pico, sub-pico, resto-pico, etc...)

        """
        self.escenarios = np.array(Lim_Escenarios)
        column = self.Crecimiento_Perfil(Años, Tasa, Ppico_New)
        r = np.zeros((column.shape[0], np.size(self.escenarios)+1))
        for t in range(Años+1):
            for i in range(np.size(self.escenarios)):
                b = 0
                for x in column[t]:
                    if x >= self.escenarios[i]:
                        b += 1
                r[t][i] = b
        p = np.sort(r)
        f = r-p
        for i in range(f.shape[0]):
            f[i][-1] = column.shape[1]+f[i][-1]
        return f.T/column.shape[1]

    def To_excel_Matriz_Probabilidad(self, Lim_Escenarios, Años,
                                     Tasa, Ppico_New=1):
        """
        Entrega el perfil de carga año a año en formato excel
        """

        column = self.Matriz_Probabilidad(
            Lim_Escenarios, Años, Tasa, Ppico_New)
        column = pd.DataFrame(column)
        return column.to_excel("Matriz_Probabilidad.xlsx")
