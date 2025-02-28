# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:38:07 2020

@author: BI
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:10:10 2020

@author: BI
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 11:42:18 2020

@author: BI
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 10:23:52 2020

@author: BI
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 20 14:32:09 2020

@author: BI
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 19 09:35:17 2020

@author: BI
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 12 13:01:39 2020

@author: BI
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:57:08 2019

@author: BI
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 10:28:36 2019

@author: BI
"""
import pyodbc

server = 
database = 
username = 
password = 

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor2 = cnxn.cursor()

cursor.execute("""

select top 1 EventId_origen
from
(
SELECT  
      EventId_origen
      ,count(EventId_destino) cluster_size
      
  FROM [Mapping_Tools].[Staging].[Jammer_distancias]

  where distancia <= 100 
  and EventId_origen != EventId_destino
  --and distancia != 0
  group by EventId_origen 
  ) a
  where cluster_size >= 2
  and EventId_origen not in ( select Eventid from [Mapping_Tools].[work].[clusters_Jammer_100])
  and EventId_origen not in ( select centro from [Mapping_Tools].[work].[clusters_Jammer_100])
 

""")

row = cursor.fetchall()

cursor2.execute("""  select max(cast(cluster_id as int))
    FROM [Mapping_Tools].[work].[clusters_Jammer_100]""")
row2 = cursor2.fetchall()

count = 1
#for i in row2:
   
  
    #count = i[0]
while row != []:
    cursor.execute("""

select top 1 EventId_origen
from
(
SELECT  
      EventId_origen
      ,count(EventId_destino) cluster_size
      
  FROM [Mapping_Tools].[Staging].[Jammer_distancias]

  where distancia <= 100 
  and EventId_origen != EventId_destino
  --and distancia != 0
  group by EventId_origen 
  ) a
  where cluster_size >= 2
  and EventId_origen not in ( select Eventid from [Mapping_Tools].[work].[clusters_Jammer_100])
  and EventId_origen not in ( select centro from [Mapping_Tools].[work].[clusters_Jammer_100])
 
""")


    row = cursor.fetchall()
    
    
    for i in row:
    
        print(i[0])
        count = count + 1
        
        cursor.execute("""
                       insert into [Mapping_Tools].[work].[clusters_Jammer_100]
        select """+str(count)+""" cluster_id, EventId_origen centro, EventId_destino id
  FROM [Mapping_Tools].[Staging].[Jammer_distancias]
  where distancia <= 100
  and EventId_origen = '"""+str(i[0])+"""'
  and EventId_origen != EventId_destino
        """)
        cursor.commit()
        
       
        
        
