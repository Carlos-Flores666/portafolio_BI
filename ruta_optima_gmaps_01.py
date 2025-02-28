# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 11:10:15 2019

@author: BI
"""

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
select ruta, cliente_origen, cliente_destino, valor
from (
SELECT [ruta]
      ,[cliente_origen]
      ,[cliente_destino]
      ,--avg([segundos]) valor
      avg([metros]) valor
  FROM  [Mapping_Tools].[work].[distance_gmaps]
  group by ruta, cliente_origen, cliente_destino) a
   where valor = (
select min( metros )
from [Mapping_Tools].[work].[distance_gmaps]
where cliente_origen = '620124811'
and cliente_origen != cliente_destino
and cliente_destino in (select client_reference
  from  Mapping_Tools.work.temp_task 
  where fecha = '2019-10-25'
  and ruta = 'RAC034'))
and cliente_origen = '620124811'
  
""")



row = cursor.fetchall()
count = 1
while row != []:
    count = count + 1
    
    for i in row:
    
        print(i[0],i[1],i[2])
        
        cursor.execute("""
        insert into Mapping_Tools.work.ruta_optima_gmaps_dist values(   
    '"""+str(i[0])+"""'
    ,'"""+str(i[2])+"""'
    ,"""+str(count)+"""
    )                    
        """)
        cursor.commit()
        cursor.execute("""
       select ruta, cliente_origen, cliente_destino, valor
from (
SELECT [ruta]
      ,[cliente_origen]
      ,[cliente_destino]
      ,--avg([segundos]) valor
      avg([metros]) valor
  FROM  [Mapping_Tools].[work].[distance_gmaps]
  group by ruta, cliente_origen, cliente_destino) a
   where valor = (
select min( metros )
from [Mapping_Tools].[work].[distance_gmaps]
where cliente_origen = '"""+str(i[2])+"""'
and cliente_origen != cliente_destino
and cliente_destino in (select client_reference
  from  Mapping_Tools.work.temp_task 
  where fecha = '2019-10-25'
  and ruta = 'RAC034')
and cliente_destino not in( select client_reference
  from  Mapping_Tools.work.ruta_optima_gmaps_dist))
and cliente_origen = '"""+str(i[2])+"""'
        """)
        
      
        row = cursor.fetchall()
        
        
