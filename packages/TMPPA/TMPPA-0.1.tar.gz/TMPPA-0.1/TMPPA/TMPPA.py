# -*- coding: utf-8 -*-
__maintainer__ = "Proyecto de Grado"
__copyright__ = "Copyright 2021"
__version__ = "0.0.1"


try:
    from datetime import datetime, timedelta
    import pandas as pd
    import os
    import glob
    import numpy as np
    from pathlib import Path as p
    import os.path as path2
except Exception as exc:
    
    print( 'Module(s) {} are missing.:'.format(str(exc)))
    

    
    
class superclase(object):
    def __init__(self,gfile= None):    
        self.path = os.path.abspath(os.path.join(__file__, '..','..','..'))
        self.gfile = gfile
        self.path_data = None     
        self.data = None
        self.name_dataset = ''
        self.file_path_process =''
        self.file_path_process_csv =''
        self.status = False
        self.all_data = pd.DataFrame()
        self.data_jobs =''
        self.data_expl = pd.DataFrame()
        self.data_vars = pd.DataFrame()
        self.file_name =''
        self.listFicheros = []
        self.listcolumns =[]
        self.listregistros= []
        self.versiones = []
        self.version = None
        self.resumeMetadatos = None
        self.listnames = None
        self.columnsAtenciones = None
        self.ColumnasLaboratorios = None
        self.dfgrupoPaciente = None
        self.listLab = None
        self.base = pd.DataFrame()
        self.dataprueba = None
        self.incluirMicro = 0
        self.lower_peso = None
        self.upper_peso = None
        self.lower_talla = None
        self.upper_talla = None
        self.dictlaboRenames = None
        self.listLaborat = None
        self.tests = 0

        
    def addlist(self):
        self.versiones.append(self.version)
        self.listFicheros.append(self.gfile)
        self.listcolumns.append(self.data.shape[0])
        self.listregistros.append(self.data.shape[1])  
        
    def createdf(self):
        self.resumeMetadatos = pd.DataFrame()
        self.resumeMetadatos['Version'] = self.versiones
        self.resumeMetadatos['Ficheros'] = self.listFicheros
        self.resumeMetadatos['columns'] = self.listregistros
        self.resumeMetadatos['registros'] = self.listcolumns
        
    def validationAtenciones(self,X):        
        '''EL peso no puede ser menor a cero o mayor a 250
           La talla no puede ser menor a cero o mayor a 2.3
           El TAS Y EL TAD  no puede ser menor a cero o mayor a 200'''
        if X['PESO'] <=0 or X['TALLA'] <=0  or X['TAS '] <=0   or X['TAD '] <=0 or np.isnan(X['TAD ']) or np.isnan(X['TAS ']) or np.isnan(X['PESO']) or np.isnan(X['TALLA']):
            return 1
        elif X['PESO'] >= 250:
            return 1
        elif X['TALLA'] >= 2.3:
            return 1        
        elif X['TAS '] > 145:
            return 1    
        elif X['TAS '] < 55:
            return 1 
        elif X['TAD '] > 145:
            return 1 
        elif X['TAD '] < 55:
            return 1 
        elif (2021 - X['FECHA NACIMIENTO'].year) >= 103:
            return 1
        elif X['PESO'] < self.lower_peso:
            return 1
        elif X['PESO'] > self.upper_peso:
            return 1
        elif X['TALLA'] < self.lower_talla:
            return 1
        elif X['TALLA'] > self.upper_talla:
            return 1    
        else:
            return 0
        
    def comp_entero(self,variable):
        '''Retorna un booleano que confirma un tipo de dato entero.'''
        try:
            float(variable)
            return True
        except:
            return False    

    def validationLaboratorios(self,X):        
        '''EL peso no puede ser menor a cero o mayor a 250
           La talla no puede ser menor a cero o mayor a 2.3
           El TAS Y EL TAD  no puede ser menor a cero o mayor a 200'''

        if X['NOM_ITEM'] == "Creatinina":     

            if X['RESULT'] <=0 or np.isnan(X['RESULT']):
                return 1
            elif X['RESULT'] >= 6:
                return 1
            else:
                return 0
        else:
            return 0
        
        if X['NOM_ITEM'] == "Microalbuminuria":     

            if X['RESULT'] <=0 or np.isnan(X['RESULT']):
                return 1
            elif X['RESULT'] >= 100:
                return 1
            else:
                return 0
        else:
            return 0
    
    def show_error(ex):
        '''
        Captura el tipo de error, su description y localización.

        Parameters
        ----------
        ex : Object
            Exception generada por el sistema.

        Returns
        -------
        None.

        '''
        if str(ex)[1:4] == '401':
            print('No se establecio conexión con Api de Kaggle')
        else:    
            trace = []
            tb = ex.__traceback__
            while tb is not None:
                trace.append({
                              "filename": tb.tb_frame.f_code.co_filename,
                              "name": tb.tb_frame.f_code.co_name,
                              "lineno": tb.tb_lineno
                              })

                tb = tb.tb_next

            print('{}Something went wrong:'.format(os.linesep))
            print('---type:{}'.format(str(type(ex).__name__)))
            print('---message:{}'.format(str(type(ex))))
            print('---trace:{}'.format(str(trace)))        
        logging.debug(ex)
    pass


class extraction(superclase):
    """
    Documentación de la clase Kaggle:
        lista de Funciones:
            validar_path: Valida que existe la ruta y retorna un booleano
            get_lst_files:Lista los archivos de un directorio según el tipo de extensión solicitada.
            get_slide:Recibe el dataframe y Toma X porcentaje de registros del conjunto de datos.
            names_archivos:Imprime en pantalla cada uno nombres de los archivos contenidos en lst_files.
            
    """
    
    def validar_path(self,pathh):
        '''
            Descripción: Valida que existe la ruta y retorna un booleano
            Parámetros función: None
            Parámetros de Objeto: self.path
            Returns: None
        '''
        if path2.exists(pathh):
            return True
        else:
            return False
        
    def get_lst_files(self):
        '''
            Descripción: Lista los archivos de un directorio según el tipo de extensión solicitada.
            Parámetros función: None
            Parámetros de Objeto: self.path, self.ext
            Returns: No tiene un return pero carga el parámetro de objeto self.lst_files      
        '''

        
        
        self.listnames = []
        if self.ext is not None:
            self.lst_files = [f for f in glob.glob(str(self.path_data)+'/**'+ str(self.ext.lower()))] #/**/*., recursive=False
            for x in self.lst_files:
                self.listnames.append(os.path.basename(x))
            return self.listnames
        else:
            print('Falta determinar la extensión de los archivos, self.ext')




    def names_archivos(self):
        '''
        Descripción: Imprime en pantalla cada uno nombres de los archivos contenidos en lst_files.
        Parámetros función: x es el número de filas que se deben mostrar
        Parámetros de Objeto: self.lst_files
        Returns: None

        '''
        try:
            names_files = []
            print('Nombres de Archivos con la Extensión solicitada')
            for f in self.lst_files:
                child = os.path.splitext(os.path.basename(f))[0]
                names_files.append(child)
                print(child) 
            return names_files            
                              
        except Exception as exc:
            self.show_error(exc)
            
    def check_used_space(self,path):
        try:
            self.check_path(path)
            if self.dir_exist:
                total_size = 0

                #use the walk() method to navigate through directory tree
                for dirpath, dirnames, filenames in os.walk(path):
                    for i in filenames:

                        #use join to concatenate all the components of path
                        f = os.path.join(dirpath, i)

                        #use getsize to generate size in bytes and add it to the total size
                        total_size += os.path.getsize(f)

                self.bytes = total_size
                total_size = self.formatSize()
                print('Espacio usado por el destino: {}'.format(total_size))
            else:
                print('{}No es posible calcular el espacio utilizado.'.format(os.linesep))
                print('El directorio {} no existe.'.format(path))
        
        except Exception as exc:
            self.show_error(exc)
            
            
    def check_path(self,path_check):
        '''
        Valida que exista el path

        Returns
        -------
        None.

        '''
        self.dir_exist = os.path.exists(path_check)            
        
            
    def check_free_space(self,path_data):
        try:
            self.bytes = shutil.disk_usage(str(path_data))[2]
            free_space = self.formatSize()
            print('Espacio libre en disco: {}'.format(free_space))
        
        except Exception as exc:
            self.show_error(exc)
        
    def formatSize(self):
        try:
            bytes = float(self.bytes)
            kb = bytes / 1024
        except:
            return "Error"
        if kb >= 1024:
            M = kb / 1024
            if M >= 1024:
                G = M / 1024
                return "%.2fG" % (G)
            else:
                return "%.2fM" % (M)
        elif kb == 0:
            return 'Folder vacio'
        else:
            return "%.2fkb" % (kb)
      
    def resumen_data_all(self):
        '''
        Descripción: Construye un detallado con el nombnre de los archivos,cantidad de registros,nombre de campos y grupos de archivos que se pueden unir de todos los archivos dentro de un fichero asigando con anterioridad 
        Parámetros función: 
        Parámetros de Objeto: 
        Returns: 
        '''
        files = self.get_lst_files()

        df = pd.DataFrame()
        df_var = pd.DataFrame()
        nombres = []
        No_Registros = []
        No_Variables =[]
        Gr_Variable = []
        Gr_Variables = []
        Gr_Tabla = []
        total_variables = []
        l_veces = []
        l_variables = []

        for  file in files: 
            
            nombres.append(os.path.basename(file))
            df_file = pd.read_csv(file)    #,index_col=False,skip_blank_lines=True
            if df_file.empty:
                No_Registros.append(0)      
                No_Variables.append(0)   
            else:
                df_file['Name_file'] = os.path.basename(file)
                No_Registros.append(df_file.shape[0])
                No_Variables.append(df_file.shape[1])
            variables = df_file.columns.tolist()
            Gr_Variable.append(variables)
            tipo_var = [t.name for t in df_file.dtypes.tolist()]
            for var in variables:  
                z = var + '-' +str(tipo_var[variables.index(var)])
                total_variables.append(z)

            Gr_Variables = [list(item) for item in set(tuple(row) for row in Gr_Variable)] 



        df['nombres'] = nombres
        df['No_Registros'] = No_Registros    
        df['No_Variables'] = No_Variables 
        df['variables'] = Gr_Variable

        for variable in df['variables']:
            Gr_Tabla.append(Gr_Variables.index(variable))

        df['Gr_Tabla'] = Gr_Tabla 
        df.to_excel("Exploration_General_blop.xlsx", sheet_name='Exp')  
        

        conjunto_variables = set(total_variables)   

        for var2 in conjunto_variables:
            x = total_variables.count(var2)
            l_variables.append(var2)
            l_veces.append(x)


        df_var['variables'] =  l_variables
        df_var['veces'] = l_veces   
        df_var.to_excel("Exploration_Variables_blop.xlsx", sheet_name='Exp')     
        print(df_var.sort_values('veces',ascending=False)) 

 


  
class transformation(superclase):
    """
        Documentación de la clase transformation:
            lista de Funciones:
                descomprimir:Descomprime el archivo dado un path y una ruta de descarga
                unir_csv:Dada una lista de ficheros realiza la unión de cvs  
                get_data_csv:evalúa si el archivo csv está vacío de lo contrario carga el parametro self data
            
        
    """  
    
    
    def consolidaMeta(self):
        if self.validar_path(self.file_path_process_csv) == True: 
            df  = pd.read_excel(self.file_path_process_csv,engine='openpyxl')
            df1  = df.append(self.resumeMetadatos,ignore_index=True)
            df1.to_excel(self.file_path_process_csv, index = False) 
        else:
            self.resumeMetadatos.to_excel(self.file_path_process_csv) 

    
    
    def consolidaCC(self):
        if self.validar_path(self.file_path_pacientes_csv) == True:              
            self.data_expl  = pd.read_excel(self.file_path_pacientes_csv,engine='openpyxl')
            self.data_expl  = self.data_expl.append(self.resumePacientes,ignore_index=True)
            self.data_expl.to_excel(self.file_path_pacientes_csv, index = False) 
        else:
            self.resumePacientes.to_excel(self.file_path_pacientes_csv, index = False)
            
            
    def descomprimir(self,File):
        '''
        Descomprime el archivo dado un path y una ruta de descarga        
        '''
        if File.find('.zip') < 0:
            File = str(File).replace('NGS/','') + '.zip'
            ruta_zip = self.path_data + '\ '.strip() + File            
        else:
            ruta_zip = File
        password = None
        existe_file = self.validar_path(ruta_zip)
        if existe_file == True:
            archivo_zip = zipfile.ZipFile(ruta_zip, "r")
            try:
                archivo_zip.extractall(pwd=password, path=self.path_data)
                os.remove(ruta_zip,"r")
            except:
                print('Fichero no Descomprimido')                
                pass
        else:
            print('Fichero no Existe')
            
    def unir_csv_all(self):
        '''
        Dada una lista de ficheros realiza la unión de cvs   
        '''
        
        try:            
            salesdata = pd.DataFrame()
            if self.ext is not None:
                for f in glob.glob(str(self.path_data)+'/**/*.'+ str(self.ext.lower()), recursive=True):
                    appenddata = pd.read_csv(f, header=None, sep=";")
                    salesdata = salesdata.append(appenddata,ignore_index=True)
                salesdata.to_csv('consolidado.csv', index = False)   

            else:
                self.status = False
                print('Falta determinar la extensión de los archivos, self.ext')
        except Exception as exc:
            self.show_error(exc)



    def unir_csv(self):
        '''
        Dada una lista de ficheros realiza la unión de cvs   
        '''        
        try:            
            self.all_data = self.all_data.append(self.data,ignore_index=True)
            self.all_data.to_csv('consolidado.csv', index = False)   
        except Exception as exc:
            self.show_error(exc)
            
            
    def save_cvs(self):
        self.data.to_csv(self.file_path_process_csv, index = False)
        


    def get_data_csv(self,path = None):
        '''
        Descripción: evalúa si el archivo csv está vacío de lo contrario carga el parametro self data
        Parámetros función: the_path,
        Parámetros de Objeto: None
        Returns: Carga el parámetro self.data con la muestra (no tiene return de forma literal)

        '''

#         try:
#         if path is None:
#             path = self.file_path_process        
        
#         try:
        df = pd.read_csv(path) #,skip_blank_lines=True,index_col=False
        return df

#         if df.empty:
#             print('Conjunto de Datos vacio')
#             self.status = False
#         else:
#             self.data = df
#         except:
#             self.data = pd.DataFrame()
            

#         except Exception as exc:
#             self.show_error(exc)

    def get_data_Excel(self,path= None,name_sheet=None,lista=None):
        
#         if path is None:
#             path = self.file_path_process       
        
        self.data =  pd.read_excel(self.path_data,engine='openpyxl') #,usecols=lista,engine='openpyxl', sheet_name=name_sheet,index_col=False
#         if df.empty:
#             print('Conjunto de Datos vacio')
#             self.status = False
#         else:
#             self.data = df
    
    
    
            
    def remove_column(self,lstcolumns):
        if self.data.empty:
            pass
        else:         
            self.data = self.data[self.data.columns[~self.data.columns.isin(lstcolumns)]] 
        
    
    def change_column_to_date(self,lstcolumns):
        if self.data.empty:
            pass
        else:            
            for col in lstcolumns:
                self.data[col] = pd.to_datetime(self.data[col])
          
            
    def filter_by_year(self,col,initial_year,final_year):
        if self.data.empty:
            pass
        else: 
            new_data = (pd.DatetimeIndex(self.data[col]).year >= initial_year) & (pd.DatetimeIndex(self.data[col]).year <= final_year)
            self.data = self.data.loc[new_data]
        
    
    def split_column(self,sb,nf,expandf,col,list_new_columns):
        try:
            if self.data.empty:
                print('Dataframe vacio')
            else:
                if expandf is True:
                    df_split = self.data[col].str.split(sb,n=nf,expand=expandf)
                    df_split.columns = list_new_columns
                    self.data = pd.concat([self.data, df_split], axis=1)
                else:
                    self.data[list_new_columns] = self.data[col].str.split(sb)
        except:
            pass
        
        
    def remove_duplicates_by_column(self,list_columns= None):
        if self.data.empty:
            pass
        else:        
            if list_columns is None:
                self.data.drop_duplicates(list_columns)        
            else:
                self.data.drop_duplicates(subset=list_columns,keep='last',inplace=True)

        
    def count_item_by_row(self,col_new,col):
        try:
            if self.data.empty:
                print('dataframe vacio, no es posible efectuar el proceso de contar elementos')
            else:
                self.data[col_new] =  self.data[col].apply(lambda x : len(x))
        except:
            pass
        
    def remove_file(self):
        os.remove(self.file_path_process)
        os.remove(self.file_path_process_csv)
        
    def filters_regex(self,fregex=False,col=None,str_filter=None):
        try:
            if fregex is False:
                new_data = self.data_jobs[(self.data_jobs[col] == str_filter)]
            else:
                new_data = self.data_jobs[self.data_jobs[col].str.contains(str_filter, regex=True, case=False)]
            return new_data 
        except:
            new_data = pd.DataFrame()            
            return new_data 
        
    def perfil_pandas(self):
        '''
        Descripción: Crea un archivo .Html en la misma ruta con el perfil de datos procesado por pandas profiling.
        Parámetros función: 
        Parámetros de Objeto: self.get_lst_files()
        Returns: None
        '''

        child = os.path.splitext(os.path.basename(self.file_path_process))[0]
        name_file = "Pandas Profiling Report " + child.replace('.csv','').replace('.zip','')        
        profile = ProfileReport(self.data, 
                                title=name_file, 
                                explorative=True,
                                minimal=True)
        profile.to_file(name_file + ".html")
        
        
    def convert_to_zip(self): 
        zip= zipfile.ZipFile(self.file_path_process, 'w', mode)
        zip.write(self.file_path_process_csv)
        zip.close()
        print('All files zipped successfully!')
        


        
    def consiladargrupospacientes(self): 
        self.get_data_Excel(self.path_data)
        test_list = self.data['id_pacientes'].unique()
        def split_list(lst, n):  
            for i in range(0, len(lst), n): 
                yield lst[i:i + n]
        listPacientes = list(split_list(test_list, self.CantPacientesporGrupo))
        dictGroup = {}
        dictGroup['grupos'] = listPacientes
        dfgrupoPaciente = pd.DataFrame(dictGroup).reset_index()
        dfgrupoPaciente['Id_Grupo'] =  dfgrupoPaciente['index']
        self.dfgrupoPaciente = dfgrupoPaciente.drop(['index'], axis=1)   
        
        
    def GeneraConsolidadoGrupoPacientesAtenciones(self):
        dfatencionesPacientes = pd.DataFrame()
        n = 0
        for pacientes in self.dfgrupoPaciente['grupos']:
            self.listFicheros = []
            self.listcolumns =[]
            self.listregistros= []
            self.versiones = []
            for file in self.listnames:                
                self.gfile = file
                self.path_data = str(p(self.path) / 'Output' / 'AtencionesIntegros' /self.gfile)  #Fichero de File de atenciones a Procesar 
                self.data = self.get_data_csv(self.path_data) # Realiza la lectura del fichero a procesar
                df1 = self.data[self.data['NUMERO DOCUMENTO'].isin(pacientes)]
                if dfatencionesPacientes.empty:   
                    dfatencionesPacientes = df1
                else:
                    dfatencionesPacientes = dfatencionesPacientes.append(df1,ignore_index=True)    
            dfatencionesPacientes['FECHA CONTROL (O DE ATENCION)'] =  pd.to_datetime(dfatencionesPacientes['FECHA CONTROL (O DE ATENCION)'])
            dfatencionesPacientes['FECHA_CONTROL'] = dfatencionesPacientes["FECHA CONTROL (O DE ATENCION)"].apply(lambda x : x.replace(day=1))
            dfatencionesPacientes['ANHO_NACIMIENTO'] =  pd.DatetimeIndex(dfatencionesPacientes['FECHA NACIMIENTO']).year
            dfatencionesPacientes['EDAD_TA'] = (pd.DatetimeIndex(dfatencionesPacientes['FECHA TAS']) -  pd.DatetimeIndex(dfatencionesPacientes['FECHA NACIMIENTO']))/np.timedelta64(365, 'D') # edad al momento de la toma de la tensión
            dfatencionesPacientes.sort_values(['NUMERO DOCUMENTO','FECHA_CONTROL' ], ascending=[True, True], inplace=True)
            dfatencionesPacientes.rename(columns={"NUMERO DOCUMENTO":"id_paciente","TAS ":'TAS','TAD ':'TAD'}, inplace=True)
            df1 = dfatencionesPacientes.drop_duplicates(['id_paciente','FECHA_CONTROL'], keep='last')#Elimina Duplicados varias citas en un mismo mes
            
            self.data = df1[['id_paciente','ANHO_NACIMIENTO','PESO','GENERO','FECHA_CONTROL','EDAD_TA','TALLA','TAS','TAD']]
            if self.tests == 1:
                name = 'Atenciones Grupo T' + str(n) + '.csv'
            else:    
                name = 'Atenciones Grupo ' + str(n) + '.csv'
            self.file_path_process_csv = str(p(self.path) / 'Output' /'Atenciones' / name)
            self.save_cvs()
            dfatencionesPacientes = pd.DataFrame()
            n = n+1
            self.version = 3        
            self.gfile = self.gfile # 
            self.addlist() # realiza la recolección de Metadatos
            self.createdf() # Guarda Metadatos en un dataset  
            self.file_path_process_csv = str(p(self.path) / 'Output'/ "resumenMetaDatos.xlsx")  
        self.consolidaMeta()  
        
        
    def calculate_lab(self,X,c3,c1,c2):
        if X[c3] >0:
            return  X[c3]
        elif X[c1] >0 and X['dif Month -1'] == 1 and X['dif Year -1'] == 0 :
            return X[c1]
        elif X[c2] >0 and X['dif Month +1'] == 1 and X['dif Year +1'] == 0 :
            return X[c2]
        
        
    def GeneraConsolidadoGrupoPacientesLaboratorios(self):
        dfatencionesPacientes = pd.DataFrame()
        
        n = 0
        for pacientes in self.dfgrupoPaciente['grupos']:
        #     print(len(pacientes))
            self.listFicheros = []
            self.listcolumns =[]
            self.listregistros= []
            self.versiones = []
            for file in self.listnames:
                self.gfile = file
                self.path_data = str(p(self.path) / 'Output' /'LaboratoriosIntegros' /self.gfile)  #Fichero de File de atenciones a Procesar 
                self.data = pd.read_csv(self.path_data,sep=',') # Realiza la lectura del fichero a procesar
                self.data['COD_PACI'] = self.data['COD_PACI'].str.replace('.','').str.replace('}','').str.replace('+','').str.replace('|','').str.replace('*','').str.replace('/','').astype(float)
                df1 = self.data[self.data['COD_PACI'].isin(pacientes)]
                if dfatencionesPacientes.empty:   
                    dfatencionesPacientes = df1
                else:
                    dfatencionesPacientes = dfatencionesPacientes.append(df1,ignore_index=True)     
            dfatencionesPacientes['FH_TOMA_MUESTRA'] = pd.to_datetime(dfatencionesPacientes['FH_TOMA_MUESTRA'],format="%Y-%m-%d %H:%M:%S").apply(lambda x : x.replace(hour=0,minute=0,second=0)) 
            dfatencionesPacientes['FECHA_CONTROL'] = dfatencionesPacientes["FH_TOMA_MUESTRA"].apply(lambda x : x.replace(day=1))        
            dfatencionesPacientes.sort_values(['COD_PACI','FECHA_CONTROL' ], ascending=[True, True], inplace=True)
            if df1.empty:
                self.data = dfatencionesPacientes  
                dfr =  pd.DataFrame(self.data.pivot_table(index=['COD_PACI','FECHA_CONTROL'], columns='cod_exam', values=['RESULT'],aggfunc=np.sum).to_records())
                self.data = dfr.rename(columns=self.dictlaboRenames)
            else:
                df1 = dfatencionesPacientes.drop_duplicates(['COD_PACI','FECHA_CONTROL','COD_ITEM'], keep='last')
                dfr =  pd.DataFrame(df1.pivot_table(index=['COD_PACI','FECHA_CONTROL'], columns='cod_exam', values=['RESULT'],aggfunc=np.sum).to_records())
                self.data = dfr.rename(columns=self.dictlaboRenames)

            if self.tests == 1:
                nameAnt = 'Atenciones Grupo T' + str(n) + '.csv'
            else:    
                nameAnt = 'Atenciones Grupo ' + str(n) + '.csv'
            self.path_data_atenciones = str(p(self.path) / 'Output' /'Atenciones' / nameAnt)
            
            atenciones = pd.read_csv(self.path_data_atenciones)          
            Atenciones = atenciones[['id_paciente','FECHA_CONTROL']]   
            Atenciones['FECHA_CONTROL'] =  pd.to_datetime(Atenciones['FECHA_CONTROL'])
            df1 = Atenciones.merge(self.data,how='outer')
            listpacientes  = df1['id_paciente'].unique()
            dfatenconsolidado = pd.DataFrame()
            for patient in listpacientes:
                
                df = df1[(df1['id_paciente'] == patient)] 
                
                df.sort_values(['FECHA_CONTROL','id_paciente'], ascending=[False,True], inplace=True)
                df['FECHA_CONTROL'] =  pd.to_datetime(df['FECHA_CONTROL'])
                df['Year'] = df['FECHA_CONTROL'].dt.year 
                df['Month'] = df['FECHA_CONTROL'].dt.month 
                df['Month -1'] =df['Month'].shift(periods=-1)
                df['Month +1'] =df['Month'].shift(periods=+1) 
                df['dif Month -1'] = abs(df['Month'] - df['Month -1'])
                df['dif Month +1'] = abs(df['Month'] - df['Month +1'])  
                #------------------------------------------------------------------
                df.sort_values(['FECHA_CONTROL','id_paciente'], ascending=[False,True], inplace=True)
                df['Year -1'] =df['Year'].shift(periods=-1)
                df['Year +1'] =df['Year'].shift(periods=+1) 
                df['dif Year -1'] = abs(df['Year'] - df['Year -1'])
                df['dif Year +1'] = abs(df['Year'] - df['Year +1'])  

                for lab in self.listLaborat:
                    c1 = lab + ' -1'
                    c2 = lab + ' +1'
                    c3 = lab #+ '_ORIGINAL'
                    c4 = lab + '_ORIGINAL'
                    if lab in df.columns.to_list():
                        df.sort_values(['FECHA_CONTROL','id_paciente'], ascending=[False,True], inplace=True)
                        df[c1] =df[c3].shift(periods=-1)
                        df[c2] =df[c3].shift(periods=+1)
                        col_list = [c3,c1,c2]
                        df['Validationtemp'] = df[col_list].sum(axis=1)
                        df.reset_index(drop=True)
                        df[c4] = df.apply(lambda x : self.calculate_lab(x,c3,c1,c2), axis=1)                       
                        
                if dfatenconsolidado.empty:   
                    dfatenconsolidado = df
                else:
                    dfatenconsolidado = dfatenconsolidado.append(df,ignore_index=True)
                    
            self.data = dfatenconsolidado[['id_paciente','FECHA_CONTROL','ALB_ORIGINAL','COL_ORIGINAL','CREA_ORIGINAL','CREAOR_ORIGINAL','GLICOS_ORIGINAL','HDL_ORIGINAL','LDL_ORIGINAL'
                                           ,'MICROA_ORIGINAL','PTH_ORIGINAL']]
            
            if self.tests == 1: 
                name = 'Laboratorio Grupo T' + str(n) + '.csv'
            else:    
                name = 'Laboratorio Grupo ' + str(n) + '.csv'
            self.file_path_process_csv = str(p(self.path) / 'Output' /'Laboratorios' / name)
            self.save_cvs()
            dfatencionesPacientes = pd.DataFrame()
            n = n+1
            self.version = 3        
            self.gfile = self.gfile # 
            self.addlist() # realiza la recolección de Metadatos
            self.createdf() # Guarda Metadatos en un dataset  
            self.file_path_process_csv = str(p(self.path) / 'Output'/ "resumenMetaDatos.xlsx")  
        self.consolidaMeta()         
        
    def GeneraConsolidadoGrupoPacientesInfGeneral(self):
        dfatencionesPacientes = pd.DataFrame()
        n = 0
        for pacientes in self.dfgrupoPaciente['grupos']:
        #     print(len(pacientes))
            self.listFicheros = []
            self.listcolumns =[]
            self.listregistros= []
            self.versiones = []
            for file in self.listnames:
                self.gfile = file
                self.path_data = str(p(self.path) / 'Output' /'InformeGeneralIntegros' /self.gfile)  #Fichero de File de atenciones a Procesar 
                self.data = pd.read_csv(self.path_data,sep=',') # Realiza la lectura del fichero a procesar
                self.data['id_paciente'] = self.data['# Documento'].astype(float)
                df1 = self.data[self.data['id_paciente'].isin(pacientes)]
                if dfatencionesPacientes.empty:   
                    dfatencionesPacientes = df1
                else:
                    dfatencionesPacientes = dfatencionesPacientes.append(df1,ignore_index=True)    
            dfatencionesPacientes.sort_values(['id_paciente'], ascending=[True], inplace=True)
            if df1.empty:
                self.data = dfatencionesPacientes.drop_duplicates(['id_paciente'], keep='last')        
            else:
                df1 = dfatencionesPacientes.drop_duplicates(['id_paciente'], keep='last')
                self.data = df1
            self.data.rename(columns={"Hipertensión":"Hypertension"}, inplace=True)
            self.data.drop(['# Documento', 'Validacion_tmp'], axis = 'columns', inplace=True)
            if self.tests == 1:
                name = 'InfGeneral Grupo T' + str(n) + '.csv'
            else:    
                name = 'InfGeneral Grupo ' + str(n) + '.csv'
            self.file_path_process_csv = str(p(self.path) / 'Output' /'InformeGeneral' / name)
            self.save_cvs()
            dfatencionesPacientes = pd.DataFrame()
            n = n+1
            self.version = 3        
            self.gfile = self.gfile # 
            self.addlist() # realiza la recolección de Metadatos
            self.createdf() # Guarda Metadatos en un dataset  
            self.file_path_process_csv = str(p(self.path) / 'Output'/ "resumenMetaDatos.xlsx")  
        self.consolidaMeta()
                
        

    def limpiarDatasetLaboratorios(self):
        for file in self.listnames:    
            self.listFicheros = []
            self.listcolumns =[]
            self.listregistros= []
            self.versiones = []
            self.gfile = file
            self.path_data = str(p(self.path) / 'Dataset' /'Laboratorios'/self.gfile) #Fichero de File de atenciones a Procesar 
            self.file_path_process_csv =str(p(self.path) / 'Output'/'LaboratoriosIntegros' /self.gfile).replace('xlsx','csv')  #Fichero de File despues de procesar calidad e integridad
            self.get_data_Excel(self.path_data) # Realiza la lectura del fichero a procesar
            self.version = 1
            self.addlist() # realiza la recolección de Metadatos
            dflab= self.data[self.ColumnasLaboratorios] # filtra las columnas de interes
            self.data = dflab[dflab['COD_ITEM'].isin(self.listLab)]
            self.data['RESULT'] = self.data['RESULT'].str.replace(',','.')            
            self.data['Validacion_tmp'] = self.data['RESULT'].apply(lambda x : self.comp_entero(x))
            self.data= self.data[self.data['Validacion_tmp'] == True] #
            self.data['RESULT'] = self.data['RESULT'].astype(float)            
            self.data['Check'] = self.data.apply(lambda x : self.validationLaboratorios(x), axis=1) # selecciona los registros que cumplen con los parametros de calidad
            self.data= self.data[self.data['Check'] == 0] # filtra los registros que cumplen con los parametros de calidad
            self.save_cvs() # Guarda el dataset despues de procesar calidad e integridad
            self.version = 2 
            self.gfile = self.gfile # 
            self.addlist() # realiza la recolección de Metadatos
            self.createdf() # Guarda Metadatos en un dataset 
            self.file_path_process_csv = str(p(self.path) / 'Output' /"resumenMetaDatos.xlsx")  
            self.consolidaMeta() # si ya existe un dataset anterior lo une con el que se esta procesando.     
            
            
            
    def limpiarDatasetInformeGeneral(self):
        for file in self.listnames:    
            self.listFicheros = []
            self.listcolumns =[]
            self.listregistros= []
            self.versiones = []
            self.gfile = file
            self.path_data = str(p(self.path) / 'Dataset' /'Informe general'/self.gfile) #Fichero de File de atenciones a Procesar 
            self.file_path_process_csv =str(p(self.path) / 'Output'/'InformeGeneralIntegros' /self.gfile).replace('xlsx','csv')  #Fichero de File despues de procesar calidad e integridad
            self.get_data_Excel(self.path_data) # Realiza la lectura del fichero a procesar
            self.version = 1
            self.addlist() # realiza la recolección de Metadatos
            dflab= self.data[self.ColumnasInformeGeneral]#.fillna(0) # filtra las columnas de interes
#             print(dflab.columns)
            self.data = dflab
            self.data['Validacion_tmp'] = self.data['Hipertensión'].apply(lambda x : self.comp_entero(x))
            self.data= self.data[self.data['Validacion_tmp'] == True] #
            self.save_cvs() # Guarda el dataset despues de procesar calidad e integridad
            self.version = 2 
            self.gfile = self.gfile # 
            self.addlist() # realiza la recolección de Metadatos
            self.createdf() # Guarda Metadatos en un dataset 
            self.file_path_process_csv = str(p(self.path) / 'Output' /"resumenMetaDatos.xlsx")  
            self.consolidaMeta() # si ya existe un dataset anterior lo une con el que se esta procesando.       
        
    def limpiarDatasetAtenciones(self):
        """1-Realiza una copia de los ficheros originales seleccionando los registros que cumplen con los parametros de calidad 
           2-Realiza la recolección de id_pacientes,si ya existe un dataset anterior lo une con el que se esta procesando. """
        for file in self.listnames:
#             print(file)
            self.listFicheros = []
            self.listcolumns =[]
            self.listregistros= []
            self.versiones = []
            self.gfile = file
            self.path_data = str(p(self.path) / 'Dataset' /'Atenciones'/self.gfile) #Fichero de File de atenciones a Procesar 
            self.file_path_process_csv =str(p(self.path) / 'Output' / 'AtencionesIntegros' /self.gfile).replace('xlsx','csv')  #Fichero de File despues de procesar calidad e integridad
            self.get_data_Excel(self.path_data) # Realiza la lectura del fichero a procesar
            self.version = 1
            self.addlist() # realiza la recolección de Metadatos
            self.data = self.data[self.columnsAtenciones] # filtra las columnas de interes
            self.data['Check'] = self.data.apply(lambda x : self.validationAtenciones(x), axis=1) # selecciona los registros que cumplen con los parametros de calidad
            self.data= self.data[self.data['Check'] == 0] # filtra los registros que cumplen con los parametros de calidad
            self.save_cvs() # Guarda el dataset despues de procesar calidad e integridad
            self.resumePacientes = pd.DataFrame(self.data['NUMERO DOCUMENTO'].unique(),columns=['id_pacientes']) # realiza la recolección de id_pacientes
            self.file_path_pacientes_csv = str(p(self.path) / 'Output' /'pacientes.xlsx')  
            self.consolidaCC() # si ya existe un dataset anterior lo une con el que se esta procesando.
            self.version = 2 
            self.gfile = self.gfile # 
            self.addlist() # realiza la recolección de Metadatos
            self.createdf() # Guarda Metadatos en un dataset 
            self.file_path_process_csv = str(p(self.path) / 'Output' /"resumenMetaDatos.xlsx")  
            self.consolidaMeta() # si ya existe un dataset anterior lo une con el que se esta procesando. 
            print('Proceso completo Para ', file)
            

        
        

    def crearDatasetbase(self):
        for n in range(0,self.dfgrupoPaciente.shape[0]):
#             print('Grupo '+ str(n))
            if self.tests == 1:
                nameInf = 'InfGeneral Grupo T' + str(n) + '.csv'
                nameAnt = 'Atenciones Grupo T' + str(n) + '.csv'
                namelab = 'Laboratorio Grupo T' + str(n) + '.csv'
            else:    
                nameInf = 'InfGeneral Grupo ' + str(n) + '.csv'
                nameAnt = 'Atenciones Grupo ' + str(n) + '.csv'
                namelab = 'Laboratorio Grupo ' + str(n) + '.csv'
            self.path_data_InfGeneral = str(p(self.path) / 'Output' /'InformeGeneral' / nameInf)
            self.path_data_atenciones = str(p(self.path) / 'Output' /'Atenciones' / nameAnt)
            self.path_data_laboratorio = str(p(self.path) / 'Output' /'Laboratorios' / namelab)    
            laboratorio = pd.read_csv(self.path_data_laboratorio)
            atenciones = pd.read_csv(self.path_data_atenciones)    
            InfGeneral = pd.read_csv(self.path_data_InfGeneral).drop_duplicates()  
            laboratorio['FECHA_CONTROL'] =  pd.to_datetime(laboratorio['FECHA_CONTROL'],format="%Y-%m-%d %H:%M:%S").apply(lambda x : x.replace(hour=0,minute=0,second=0))
            atenciones['FECHA_CONTROL'] =  pd.to_datetime(atenciones['FECHA_CONTROL'],format="%Y-%m-%d %H:%M:%S")
            atenciones['GENERO'] = atenciones['GENERO'].replace('MASCULINO',1).replace('FEMENINO',0)    
            datoscompl = atenciones[['id_paciente','ANHO_NACIMIENTO','GENERO']].drop_duplicates()
            atenciones.drop(['ANHO_NACIMIENTO','GENERO'], axis = 'columns', inplace=True)    
            dfe1 = atenciones.merge(laboratorio,how='outer',on=['id_paciente','FECHA_CONTROL'])
            dfe2 = datoscompl.merge(InfGeneral)#.fillna(0)
            dfe = dfe2.merge(dfe1,how='outer')#.fillna(0) 
            dfe  = dfe[(dfe['FECHA_CONTROL'] != 0)] 
            dfe['FECHA_CONTROL'] =  pd.to_datetime(dfe['FECHA_CONTROL'])
            
            
            
#             def calculate_lab(X,c3,c1,c2):
#                 if X[c3] >0:
#                     return  X[c3]
#                 elif X[c1]  >0:
#                     return X[c1]
#                 elif X[c2]  >0:
#                     return X[c2]
            
#             for lab in self.listLaborat:
#                 c1 = lab + ' -1'
#                 c2 = lab + ' +1'
#                 c3 = lab + '_ORIGINAL'
#                 if lab in dfe.columns.to_list():
#                     dfe.sort_values(['FECHA_CONTROL','id_paciente'], ascending=[False,True], inplace=True)
#                     dfe[c1] =dfe[c3].shift(periods=-1)
#                     dfe[c2] =dfe[c3].shift(periods=+1)
#                     col_list = [c3,c1,c2]
#                     dfe['Validationtemp'] = dfe[col_list].sum(axis=1)                   
#                     dfe.reset_index(drop=True)
#                     dfe[lab] = dfe.apply(lambda x : calculate_lab(x,c3,c1,c2), axis=1)  
            

            def calculate_TFG(X):
                if X['GENERO'] == 1:
                    return ((140-X['EDAD_TA'])*X['PESO'])/(72*X['CREA_ORIGINAL']) if X['CREA_ORIGINAL'] != 0 else 0
                else:
                    return (((140-X['EDAD_TA'])*X['PESO'])/(72*X['CREA_ORIGINAL'])*0.85) if X['CREA_ORIGINAL'] != 0 else 0
#             print(dfe.columns)    
            dfe['TGF'] = dfe.apply(lambda x : calculate_TFG(x), axis=1)#.fillna(0)  

            def calculateEstadio(X):
                if X['TGF'] >= 90:
                    return 1
                elif X['TGF'] >= 60 and X['TGF'] < 90:
                    return 2    
                elif X['TGF'] >= 30 and X['TGF'] < 60:
                    return 3     
                elif X['TGF'] >= 15 and X['TGF'] < 30:
                    return 4     
                elif X['TGF'] < 15:
                    return 5     

            dfe['ESTADIO'] = dfe.apply(lambda x : calculateEstadio(x), axis=1)
            dfe.sort_values(['FECHA_CONTROL','id_paciente'], ascending=[False,True], inplace=True)
            self.data  = dfe[(dfe['TGF'] > 0)]            
#             self.data.drop(['CREA_ORIGINAL','MICROA_ORIGINAL','CREA -1','CREA +1','Validationtemp','MICROA -1','MICROA +1'], axis = 'columns', inplace=True)
            if self.tests == 1:
                name = 'base Grupo T' + str(n) + '.csv'
            else:
                name = 'base Grupo ' + str(n) + '.csv'
            self.file_path_process_csv = str(p(self.path) / 'Output' /'DatasetBase' / name)
            self.save_cvs()
            
    def resumenpacientes(self):
#         self.ext = 'csv'
#         self.path_data = r"C:\Users\jguevara\Dropbox\ProyectoGrado\Output\DatasetBase"
#         self.get_lst_files()
#         from datetime import datetime, timedelta

        def calculateDifmonthpred(X):
            x = ((X["FECHA_CONTROL"] -  X["PREVIOUSDATEGENERIC_MODEL"]).days)/30    
            if X['DATE_MAX_GENERIC_MODEL'] == X["FECHA_CONTROL"]:
                return 10000
            elif x < 0:
                return abs(int(x)) +6
            else:
                return x +6

        def find_date():
            self.base["FECHA_CONTROL"] = pd.to_datetime(self.base["FECHA_CONTROL"],format="%Y-%m-%d %H:%M:%S")        
            DF_DATE_MAX_GENERIC_MODEL  = pd.DataFrame(self.base.groupby(['id_paciente']).agg({'FECHA_CONTROL': ['max']}).to_records()).rename(columns={"('FECHA_CONTROL', 'max')":"DATE_MAX_GENERIC_MODEL"})
            DF_DATE_MAX_GENERIC_MODEL["DATE_MAX_GENERIC_MODEL"] = pd.to_datetime(DF_DATE_MAX_GENERIC_MODEL["DATE_MAX_GENERIC_MODEL"],format="%Y-%m-%d %H:%M:%S")
            new_datetime = timedelta(days = 180)
            DF_DATE_MAX_GENERIC_MODEL['PREVIOUSDATEGENERIC_MODEL'] = (DF_DATE_MAX_GENERIC_MODEL["DATE_MAX_GENERIC_MODEL"] - new_datetime).apply(lambda x : x.replace(day=1))
            dfe = self.base.merge(DF_DATE_MAX_GENERIC_MODEL,on=['id_paciente'])
            dfe['DifmonthpredGeneric'] = dfe.apply(lambda x : calculateDifmonthpred(x), axis=1)  
            dfe1 = dfe.iloc[dfe.groupby('id_paciente').agg(max_ = ('DifmonthpredGeneric', lambda data: data.idxmin())).max_]
            dfe2 = dfe1[['id_paciente','FECHA_CONTROL']].rename(columns={'FECHA_CONTROL':'DATEENDPREDMAX'})
            self.base1 =  self.base.merge(dfe2,on=['id_paciente'])




        self.base = pd.DataFrame()  
        for file in  self.listnames:
            self.gfile = file
            self.path_data = str(p( self.path) / 'Output' /'DatasetBase' / self.gfile)  #Fichero de File de atenciones a Procesar 
            self.data = pd.read_csv( self.path_data,sep=',') # Realiza la lectura del fichero a procesar                  
            if  self.base.empty:   
                 self.base =  self.data
            else:
                 self.base =  self.base.append( self.data,ignore_index=True)

        if self.incluirMicro == 1:
            self.base = self.base[self.base['MICROA'].notnull()]  

        find_date()


        #         print(self.base.shape,'dimenciones Originales')

        #         print(self.base1.shape,'dimenciones 2')

        listavar = ['id_paciente','FECHA_CONTROL','PESO', 'EDAD_TA', 'TALLA', 'TAD','TAS', 'CREA_ORIGINAL', 'MICROA_ORIGINAL','TGF', 'ESTADIO','COL_ORIGINAL',
                          'HDL_ORIGINAL','LDL_ORIGINAL','CREAOR_ORIGINAL','PTH_ORIGINAL','ALB_ORIGINAL','GLICOS_ORIGINAL']
        listdel = []
        
        for x in listavar:
            if x not in self.base.columns:
                listdel.append(x) 
                
        def delete__by_values(lst, values):
            values_as_set = set(values)
            return [ x for x in lst if x not in values_as_set ]
        
        listavar = delete__by_values( listavar, listdel )

        dfbase = self.base[listavar]


        base  = pd.DataFrame(self.base1.groupby(['id_paciente','DATEENDPREDMAX','ANHO_NACIMIENTO', 'GENERO', 'Hypertension', 'Diabetes']).agg({'FECHA_CONTROL': ['min','max', 'count']}).to_records()).rename(columns={"('FECHA_CONTROL', 'min')":"DATE_MIN","('FECHA_CONTROL', 'max')":"DATE_MAX","('FECHA_CONTROL', 'count')":'No_Consultas'}) # resume fechas de inicio y fin y calcula los meses 
        #         print(base.shape,'dimenciones 3')
        data2 =  dfbase.rename(columns={'FECHA_CONTROL':'DATE_MIN','TAS':'TAS_INI','TAD':'TAD_INI','ESTADIO':'ESTADIO_INI',
                                                   'CREA_ORIGINAL':'CREA_INI','MICROA_ORIGINAL':'MICROA_INI','TGF':'TGF_INI','TALLA':'TALLA_INI','PESO':'PESO_INI','EDAD_TA':'EDAD_TA_INI',
                                       'COL_ORIGINAL':'COL_INI','HDL_ORIGINAL':'HDL_INI','LDL_ORIGINAL':'LDL_INI','CREAOR_ORIGINAL':'CREAOR_INI','PTH_ORIGINAL':'PTH_INI','ALB_ORIGINAL':'ALB_INI','GLICOS_ORIGINAL':'GLICOS_INI'})
        #         print(data2.shape,'dimenciones 4')
        data3 =  dfbase.rename(columns={'FECHA_CONTROL':"DATE_MAX",'TAS':'TAS_FIN','TAD':'TAD_FIN','ESTADIO':'ESTADIO_FIN',
                                                   'CREA_ORIGINAL':'CREA_FIN','MICROA_ORIGINAL':'MICROA_FIN','TGF':'TGF_FIN','TALLA':'TALLA_FIN','PESO':'PESO_FIN','EDAD_TA':'EDAD_TA_FIN',
                                       'COL_ORIGINAL':'COL_FIN','HDL_ORIGINAL':'HDL_FIN','LDL_ORIGINAL':'LDL_FIN','CREAOR_ORIGINAL':'CREAOR_FIN','PTH_ORIGINAL':'PTH_FIN','ALB_ORIGINAL':'ALB_FIN','GLICOS_ORIGINAL':'GLICOS_FIN'})
        #         print(data3.shape,'dimenciones 5')
        data4 =  dfbase.rename(columns={'FECHA_CONTROL':"DATEENDPREDMAX",'TAS':'TAS_FIN_PRED','TAD':'TAD_FIN_PRED','ESTADIO':'ESTADIO_FIN_PRED',
                                                   'CREA_ORIGINAL':'CREA_FIN_PRED','MICROA_ORIGINAL':'MICROA_FIN_PRED','TGF':'TGF_FIN_PRED','TALLA':'TALLA_FIN_PRED','PESO':'PESO_FIN_PRED','EDAD_TA':'EDAD_TA_FIN_PRED',
                                       'COL_ORIGINAL':'COL_FIN_PRED','HDL_ORIGINAL':'HDL_FIN_PRED','LDL_ORIGINAL':'LDL_FIN_PRED','CREAOR_ORIGINAL':'CREAOR_FIN_PRED','PTH_ORIGINAL':'PTH_FIN_PRED','ALB_ORIGINAL':'ALB_FIN_PRED','GLICOS_ORIGINAL':'GLICOS_FIN_PRED'})
        #         print(data4.shape,'dimenciones 5')

        df1 = base.merge(data2).drop_duplicates()
        #         print(df1.shape,'dimenciones 6')
        df2 = base.merge(data3).drop_duplicates()
        #         print(df2.shape,'dimenciones 7')
        df3 = base.merge(data4).drop_duplicates()
        #         print(df3.shape,'dimenciones 8')
        # # #--------------------------------------------------------------------------------------

        dfv2 = df1.merge(df2, on=['id_paciente','Diabetes','Hypertension','DATE_MIN','DATE_MAX','No_Consultas','GENERO','DATEENDPREDMAX','ANHO_NACIMIENTO'],how='outer')
        #         print(dfv2.shape,'dimenciones 8')
        dfv4 = dfv2.merge(df3, on=['id_paciente','Diabetes','Hypertension','DATE_MIN','DATE_MAX','No_Consultas','GENERO','DATEENDPREDMAX','ANHO_NACIMIENTO'],how='outer')
        #         print(dfv3.shape,'dimenciones 8')
        
        def find_error_dates(X):
            if X['DATE_MIN'] == X["DATE_MAX"]:
                return 1
            elif X['DATEENDPREDMAX'] == X["DATE_MAX"]:
                return 1
            elif X['DATEENDPREDMAX'] == X["DATE_MIN"]:
                return 1
            else:
                return 0

        dfv4['ValidationDates'] = dfv4.apply(lambda x : find_error_dates(x), axis=1) 
        Natenc = [1,2,3]
        estadios_analisis = [1,2,3,4]
        dfv3 = dfv4[~dfv4.ValidationDates.isin(Natenc) & dfv4.ESTADIO_INI.isin(estadios_analisis)]


        dfv3['DIF_TFG'] = dfv3['TGF_FIN'] - dfv3['TGF_INI'] 
        dfv3['DIF_TAD'] = dfv3['TAD_FIN'] - dfv3['TAD_INI']       
        dfv3['DIF_TAS'] = dfv3['TAS_FIN']  -  dfv3['TAS_INI'] 
        dfv3['DIF_CREA'] =  dfv3['CREA_FIN'] - dfv3['CREA_INI'] 
        dfv3['DIF_MICROA'] = dfv3['MICROA_FIN'] - dfv3['MICROA_INI'] 
        dfv3["DATE_MAX"] = pd.to_datetime(dfv3["DATE_MAX"],format="%Y-%m-%d %H:%M:%S")
        dfv3['DATE_MIN'] = pd.to_datetime(dfv3["DATE_MIN"],format="%Y-%m-%d %H:%M:%S")
        dfv3['DIF_FECHA'] =  abs(((dfv3["DATE_MAX"] -  dfv3["DATE_MIN"]).dt.days)/365)
        dfv3['MTAD'] = dfv3['DIF_TAD']/dfv3['DIF_FECHA']
        dfv3['MTAS'] = dfv3['DIF_TAS']/dfv3['DIF_FECHA']
        dfv3['MCREA'] = dfv3['DIF_CREA']/dfv3['DIF_FECHA']
        dfv3['MMICROA'] = dfv3['DIF_MICROA']/dfv3['DIF_FECHA']
        dfv3['MTFG'] = dfv3['DIF_TFG']/dfv3['DIF_FECHA']
        #--------------------------------------------------------------------------------
        dfv3['DIF_TFG_PRED'] = dfv3['TGF_FIN_PRED']  -  dfv3['TGF_INI'] 
        dfv3['DIF_TAD_PRED'] = dfv3['TAD_FIN_PRED']  - dfv3['TAD_INI']        
        dfv3['DIF_TAS_PRED'] =dfv3['TAS_FIN_PRED'] - dfv3['TAS_INI']  
        dfv3['DIF_CREA_PRED'] =dfv3['CREA_FIN_PRED'] -  dfv3['CREA_INI'] 
        dfv3['DIF_MICROA_PRED'] =  dfv3['MICROA_FIN_PRED'] - dfv3['MICROA_INI'] 
        dfv3["DATE_MAX_PRED"] = pd.to_datetime(dfv3["DATEENDPREDMAX"],format="%Y-%m-%d %H:%M:%S")
        dfv3['DATE_MIN'] = pd.to_datetime(dfv3["DATE_MIN"],format="%Y-%m-%d %H:%M:%S")
        dfv3['DIF_FECHA_PRED'] =  abs(((dfv3["DATE_MAX_PRED"] -  dfv3["DATE_MIN"]).dt.days)/365)
        dfv3['MTAD_PRED'] = dfv3['DIF_TAD_PRED']/dfv3['DIF_FECHA_PRED']
        
        dfv3['DIF_COL_PRED'] = dfv3['COL_FIN_PRED']  -  dfv3['COL_INI'] 
        dfv3['MCOL_PRED'] = dfv3['DIF_COL_PRED']/dfv3['DIF_FECHA_PRED']        
        dfv3['DIF_COL'] = dfv3['COL_FIN']  -  dfv3['COL_INI'] 
        dfv3['MCOL'] = dfv3['DIF_COL']/dfv3['DIF_FECHA']
        
        
        dfv3['DIF_LDL_PRED'] = dfv3['LDL_FIN_PRED']  -  dfv3['LDL_INI'] 
        dfv3['MLDL_PRED'] = dfv3['DIF_LDL_PRED']/dfv3['DIF_FECHA_PRED']
        dfv3['DIF_LDL'] = dfv3['LDL_FIN']  -  dfv3['LDL_INI'] 
        dfv3['MLDL'] = dfv3['DIF_LDL']/dfv3['DIF_FECHA']  

        dfv3['DIF_GLICOS_PRED'] = dfv3['GLICOS_FIN_PRED']  -  dfv3['GLICOS_INI'] 
        dfv3['MGLICOS_PRED'] = dfv3['DIF_GLICOS_PRED']/dfv3['DIF_FECHA_PRED']
        dfv3['DIF_GLICOS'] = dfv3['GLICOS_FIN']  -  dfv3['GLICOS_INI'] 
        dfv3['MGLICOS'] = dfv3['DIF_GLICOS']/dfv3['DIF_FECHA']  
        
        dfv3['DIF_HDL_PRED'] = dfv3['HDL_FIN_PRED']  -  dfv3['HDL_INI'] 
        dfv3['MHDL_PRED'] = dfv3['DIF_HDL_PRED']/dfv3['DIF_FECHA_PRED']
        dfv3['DIF_HDL'] = dfv3['HDL_FIN']  -  dfv3['HDL_INI'] 
        dfv3['MHDL'] = dfv3['DIF_HDL']/dfv3['DIF_FECHA']  
        
        
        dfv3['MTAS_PRED'] = dfv3['DIF_TAS_PRED']/dfv3['DIF_FECHA_PRED']
        dfv3['MCREA_PRED'] = dfv3['DIF_CREA_PRED']/dfv3['DIF_FECHA_PRED']
        dfv3['MMICROA_PRED'] = dfv3['DIF_MICROA_PRED']/dfv3['DIF_FECHA_PRED']


        dfv3['MTFG_PRED'] = dfv3['DIF_TFG_PRED']/dfv3['DIF_FECHA_PRED']


        dfv3['ESTADIOS'] =  dfv3['ESTADIO_INI'].astype(str)+ '-' + dfv3['ESTADIO_FIN'].astype(str)
        dfv3['IMC_INI'] = dfv3['PESO_INI'] / (dfv3['TALLA_INI'] * dfv3['TALLA_INI']) #(IMC = peso [kg]/ estatura [m2]).
        dfv3['IMC_FIN'] = dfv3['PESO_FIN'] / (dfv3['TALLA_FIN'] * dfv3['TALLA_FIN'])
        dfv3['IMC_FIN_PRED'] = dfv3['PESO_FIN_PRED'] / (dfv3['TALLA_FIN_PRED'] * dfv3['TALLA_FIN_PRED'])        
        dfv3['DIF_IMC_PRED'] = dfv3['IMC_FIN_PRED']  -  dfv3['IMC_INI'] 
        dfv3['MIMC_PRED'] = dfv3['DIF_IMC_PRED']/dfv3['DIF_FECHA_PRED']        
        dfv3['MonthDATE_MAX_DATE_PRED'] =  ((dfv3["DATE_MAX"] -  dfv3["DATE_MAX_PRED"]).dt.days)/30
        dfv3['MonthDATE_PRED_DATE_MIN'] =  ((dfv3["DATE_MAX_PRED"] -  dfv3["DATE_MIN"]).dt.days)/30


        def calculateProgresor(X):
            if X['MTFG'] <= -5:
                return 1
            else:
                return 0

        if not dfv3.empty: 
            dfv3['ProgresorRapido'] = dfv3.apply(lambda x : calculateProgresor(x), axis=1) 
        dfv3.drop(['DATEENDPREDMAX', 'No_Consultas','ValidationDates'], axis = 'columns', inplace=True)
        self.data = dfv3
        if self.tests == 1:
            self.file_path_process_csv = str(p( self.path) / 'Output' /'DatasetBaseGeneralT.csv')
        else:    
            self.file_path_process_csv = str(p( self.path) / 'Output' /'DatasetBaseGeneral.csv')
        self.save_cvs()
        print('fin') 

        
class claseGeneral(extraction,transformation):
    
    def log(self):
        print('log')
    

        
    

        


        
    
    
  
        
    
    
    
    
    
        
        
            
            
        