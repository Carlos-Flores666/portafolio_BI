# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 10:28:36 2019

@author: BI
"""

server = '52.170.44.37' 
database = 'BIGeography' 
username = 'PointerCol01' 
password = 'PointerCol01' 

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()


cursor.execute("""
select ruta, origen, destino
from Mapping_Tools.work.distancias_SQL_02
where distancia = (
select min(distancia )
from Mapping_Tools.work.distancias_SQL_02
where origen = '620124811'
and origen != destino
and destino in (select client_reference
  from  Mapping_Tools.work.temp_task 
  where fecha = '2019-10-25'
  and ruta = 'RAC034'))
and origen = '620124811'
""")


row = cursor.fetchall()
count = 1
while row != []:
    count = count + 1
    
    for i in row:
    
        print(i[0],i[1],i[2])
        
        cursor.execute("""
        insert into Mapping_Tools.work.ruta_optima values(   
    '"""+str(i[0])+"""'
    ,'"""+str(i[2])+"""'
    ,"""+str(count)+"""
    )                    
        """)
        cursor.commit()
        cursor.execute("""
                       
        
        select ruta, origen, destino
    from Mapping_Tools.work.distancias_SQL_02
    where distancia = (
    select min(distancia )
    from Mapping_Tools.work.distancias_SQL_02
    where origen = '"""+str(i[2])+"""'
    and origen != destino
    and destino in (select client_reference
      from  Mapping_Tools.work.temp_task 
      where fecha = '2019-10-25'
      and ruta = 'RAC034')
    and destino not in( select client_reference
  from  Mapping_Tools.work.ruta_optima))
    and origen = '"""+str(i[2])+"""'       

   
        """)
        row = cursor.fetchall()
        
        
