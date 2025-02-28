# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 18:23:46 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 13:37:21 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 15:29:27 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 31 14:39:28 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 29 16:50:25 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 24 17:51:46 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 16 17:58:46 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 16:00:11 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:51:38 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 16:48:15 2023

@author: carlo
"""


# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 11:58:19 2023

@author: carlo
"""

import psycopg2
import busca_actos_02 as busca_actos
from colorama import Fore, Back, Style
from PIL import Image

import networkx as nx
import matplotlib.pyplot as plt


conn = psycopg2.connect(host= "localhost",
                        database="base_ficticia", 
                        user="postgres", 
                        password="postgresql")
conn.autocommit = True
cursor1 = conn.cursor()


        


G = nx.DiGraph()
node_pos = {}

lvl_down = 0
lvl_up = 0

titulo = input('escriba un número de título: ')

cursor1.execute("""
                select fecha_registro
from public.concesiones
        where numero_titulo =  """+str(titulo))
        
fecha = cursor1.fetchall()[0][0]

titulo_n = str(titulo) +"""
"""+str(fecha)

G.add_node(str(titulo_n))
node_pos[str(titulo_n)] = (0,0)
color_map = []
e_labels = {}

x = 1
y = 2


def traza(titulo, lvl_down, node_pos, G):
    
    
    
    
    cursor1.execute("""
        select c.numero_titulo,  fecha_registro, superficie, descripcion, e.id_tipo_evento, nombre_lote
        from public.concesiones c
    	inner join public.eventos e on c.id_evento = e.id_evento
    	inner join public.catalogo_tipo_evento te on e.id_tipo_evento = te.id_tipo_evento
        inner join public.nombre_lotes nl on c.numero_titulo = nl.numero_titulo
        where c.numero_titulo =  """+ str(titulo))
    
    first_tit = cursor1.fetchall()
    
    
    
    cursor1.execute("""
                    select c.numero_titulo
                from comprobacion.comprobacion_lotes_sustituidos ls
                inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
                where c.numero_titulo = '"""+str(titulo)+"""'
                    """)
    relation = cursor1.fetchall()
    
    if len(relation) < 1:
        tipo = 0 
    
    if len(relation) > 1 :
        tipo = 2
        
    if len(relation) == 1:
        
        cursor1.execute("""
                        select ls.numero_titulo, c.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where c.numero_titulo = '"""+str(titulo)+"""'
                                    """)
        d = cursor1.fetchall()[0][0]
       
        
        cursor1.execute("""
                        select ls.numero_titulo
                from comprobacion.comprobacion_lotes_sustituidos ls
                inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
                where ls.numero_titulo = '"""+str(d)+"""'
                        """)
        dd = cursor1.fetchall()
        
        
        
        
        if len(dd) > 1:
            tipo = 3
            
        if len(dd) == 1:
            tipo = 1
        
        
    
    

    if tipo == 3:
        lvl_down = lvl_down - x
        print(Fore.YELLOW + ' TÍTULO '+str(titulo)+ ' ES UNA DIVISION')
        
        cursor1.execute("""
            select  c.numero_titulo, ls.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where c.numero_titulo = '"""+str(titulo)+"""'
           order by ls.numero_titulo desc
           """)
        
        deri = cursor1.fetchall()
        
        ante = deri[0][1]
        
        cursor1.execute("""
                select  cast(fecha as date)
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
        where c.numero_titulo =  '"""+str(ante)+"""'""")
        
        fe = cursor1.fetchall()
        if len(fe) > 0:
            
            ante_nn = str(ante) +'\n'+str(fe[0][0])
        else:
            ante_nn = str(ante)
            
        cursor1.execute("""
                select  cast(fecha as date)
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
        where c.numero_titulo =  '"""+str(titulo)+"""'""")
        
        fec = cursor1.fetchall()
       
        titulo_nn = str(titulo)+'\n'+str(fec[0][0])

        G.add_node(str(ante_nn))
        G.add_edge(str(ante_nn), str(titulo_nn))
        act = busca_actos.r_actos(ante)
        if len(act) > 0:
            e_labels[(str(ante_nn), str(titulo_nn))] = act
        
        
        
        
        cursor1.execute("""
            select  c.numero_titulo, ls.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where ls.numero_titulo = '"""+str(ante)+"""'
           order by ls.numero_titulo desc
         """)
         
        derideri = cursor1.fetchall()
        
        nodos = 0
        for i in derideri:
            
            cursor1.execute("""
                select numero_titulo, fecha, superficie, cc.nombre, nombre_lote
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
    inner join catalogos.clase_concesion cc on c.id_clase_concesion = cc.id_clase_concesion
        where c.numero_titulo =  '"""+str(i[0])+"""'""")
            resul = cursor1.fetchall()
            print(Fore.WHITE + 'numero_titulo | fecha_registro | superficie' )
            print(resul)
            print(Fore.CYAN)
            busca_actos.busca_actos(i[0])
            
            
            if str(i[0]) == str(titulo):
                continue
            else:
                if len(resul) > 0:
            
                    ante_n = str(i[0]) +'\n'+str(resul[0][1])
                else:
                    ante_n = str(i[0])
                    
                nodos = nodos - y
                G.add_node(ante_n)
                G.add_edge(str(ante_nn), str(ante_n))
                act = busca_actos.r_actos(ante)
                if len(act) > 0:
                    e_labels[(str(ante_nn), ante_n)] = act
                    
                node_pos[ante_n] = (lvl_down + 1, nodos)
        
        node_pos[str(ante_nn)] = (lvl_down, nodos/2)
        
        print('Los anteriores títulos sustituyen a: ')
        cursor1.execute("""
                select numero_titulo, fecha, superficie, cc.nombre, nombre_lote
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
    inner join catalogos.clase_concesion cc on c.id_clase_concesion = cc.id_clase_concesion
        where c.numero_titulo =  '"""+str(ante)+"""'""")
        
        anterior = cursor1.fetchall()
        print('numero_titulo | fecha_registro | superficie | nombre del lote' )
        print(anterior)
        
        traza(ante, lvl_down, node_pos, G)
          
    if tipo == 0:
        print(Fore.YELLOW +' TÍTULO '+str(titulo) )
        print(Fore.WHITE +'numero_titulo | fecha_registro | superficie | nombre del lote' )
        print(first_tit)    
        print('El título '+ str(titulo) +' no sustituye algún título')
        print(Fore.CYAN)
        busca_actos.busca_actos(titulo)
        
    if tipo == 1:
        lvl_down = lvl_down - x
        print(Fore.YELLOW +'EL TÍTULO '+str(titulo))
        print(Fore.WHITE +'numero_titulo | fecha_registro | superficie | nombre del lote' )
        cursor1.execute("""
             select  c.numero_titulo, ls.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where c.numero_titulo = '"""+str(titulo)+"""'
           order by ls.numero_titulo desc
           """)
           
        deri = cursor1.fetchall()
        print(first_tit)
        print(Fore.CYAN)
        busca_actos.busca_actos(titulo)
        nodos = 0
        for i in deri:
            
            cursor1.execute("""
                               select numero_titulo, fecha, superficie, cc.nombre, nombre_lote
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
    inner join catalogos.clase_concesion cc on c.id_clase_concesion = cc.id_clase_concesion
        where c.numero_titulo =  '"""+str(i[1])+"""'""")
            resul = cursor1.fetchall()
          
            print(Fore.WHITE +'El anterior título sustituye a: ')
            print('numero_titulo | fecha_registro | superficie | nombre del lote' )
            print(resul)
            print(Fore.CYAN)
            busca_actos.busca_actos(i[1])
            
            if len(resul) > 0:
                ante_n = str(i[1]) +'\n'+str(resul[0][1])
            else:
                ante_n = str(i[1])
            
            
            cursor1.execute("""
                select  cast(fecha as date)
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
        where c.numero_titulo =  '"""+str(titulo)+"""'""")
        
            fec = cursor1.fetchall()
           
            titulo_nn = str(titulo)+'\n'+str(fec[0][0])
                
            nodos = nodos - y
            G.add_node(ante_n)
            G.add_edge(ante_n, str(titulo_nn) )
            act = busca_actos.r_actos(i[1])
            if len(act) > 0:
                e_labels[(ante_n, str(titulo_nn))] = act
            
            if len(node_pos[str(titulo_nn)]) > 0:
                node_pos[ante_n] = (lvl_down, (node_pos[str(titulo_nn)][1]) )
            else:
                node_pos[ante_n] = (lvl_down, nodos)
            traza(i[1], lvl_down, node_pos, G)
    
    if tipo == 2:
        lvl_down = lvl_down - x
        print(Fore.YELLOW +'EL TÍTULO '+str(titulo)+ ' ES UNA UNIFICACION')
        cursor1.execute("""
            select  c.numero_titulo, ls.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where c.numero_titulo = '"""+str(titulo)+"""'
           order by ls.numero_titulo desc
           """)
           
        deri = cursor1.fetchall()
        print(Fore.WHITE +'numero_titulo | fecha_registro | superficie | nombre del lote' )
        print(first_tit)
        print(Fore.CYAN)
        busca_actos.busca_actos(titulo)
        print('El anterior título sustituye a: ')
        nodos = 0
        for i in deri:
            
            cursor1.execute("""
                                select numero_titulo, fecha, superficie, cc.nombre, nombre_lote
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
    inner join catalogos.clase_concesion cc on c.id_clase_concesion = cc.id_clase_concesion
        where c.numero_titulo =  '"""+str(i[1])+"""'""")
            resul = cursor1.fetchall()
            print(Fore.WHITE +'numero_titulo | fecha_registro | superficie | nombre del lote' )
            print(resul)
            print(Fore.CYAN)
            busca_actos.busca_actos(i[1])
            print('a su vez:')
            
            if len(resul) > 0:
                ante_n = str(i[1]) +'\n'+str(resul[0][1])
            else:
                ante_n = str(i[1])
            
            nodos = nodos - y
            G.add_node(ante_n)
            G.add_edge(ante_n, str(titulo_n) )
            act = busca_actos.r_actos(i[1])
            if len(act) > 0:
                e_labels[(ante_n, str(titulo_n))] = act
                
            node_pos[ante_n] = (lvl_down, nodos)
        
            traza(i[1], lvl_down, node_pos, G)
            
    if tipo == 4:
        lvl_down = lvl_down - x
        print(Fore.YELLOW +'EXPLOTACION')
        cursor1.execute("""
            select  c.numero_titulo, ls.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where c.numero_titulo = '"""+str(titulo)+"""'
           order by ls.numero_titulo desc
           """)
           
        deri = cursor1.fetchall()
        print(Fore.WHITE +'numero_titulo | fecha_registro | superficie' )
        print(first_tit)
        print(Fore.CYAN)
        busca_actos.busca_actos(titulo)
        nodos = 0
        for i in deri:
           
            cursor1.execute("""
                               select numero_titulo, fecha, superficie, cc.nombre, nombre_lote
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
    inner join catalogos.clase_concesion cc on c.id_clase_concesion = cc.id_clase_concesion
        where c.numero_titulo =  '"""+str(i[1])+"""'""")
            resul = cursor1.fetchall()
          
            print('El anterior título sustituye a: ')
            print(Fore.WHITE +'numero_titulo | fecha_registro | superficie' )
            print(resul)
            print(Fore.CYAN)
            
            if len(resul) > 0:
                ante_n = str(i[1]) +'\n'+str(resul[0][1])
            else:
                ante_n = str(i[1])
            
            nodos = nodos - y
            G.add_node(ante_n)
            G.add_edge(ante_n, str(titulo_n) )
            act = busca_actos.r_actos(i[1])
            if len(act) > 0:
                e_labels[(ante_n, str(titulo_n))] = act
                
            if len(node_pos[str(titulo_n)]) > 0:
                node_pos[ante_n] = (lvl_down, (node_pos[str(titulo_n)][1]) )
            else:
                node_pos[ante_n] = (lvl_down, nodos)
            
            busca_actos.busca_actos(i[1])
            
    #nx.draw(G, node_pos, with_labels = True, font_color = 'white', node_shape='s')
    
    return G, node_pos
            
            
            
def traza_ahead(titulo, lvl_up, node_pos, G):
    
    cursor1.execute("""
                    select ls.numero_titulo
                from comprobacion.comprobacion_lotes_sustituidos ls
                inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
                where ls.numero_titulo = '"""+str(titulo)+"""'
                    """)
    relation = cursor1.fetchall()
    
    if len(relation) < 1:
        tipo = 0 
    
    if len(relation) > 1 :
        tipo = 3
        
    if len(relation) == 1:
        
        cursor1.execute("""
                        select ls.numero_titulo, c.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where ls.numero_titulo = '"""+str(titulo)+"""'
                                    """)
        d = cursor1.fetchall()[0][1]
       
        
        cursor1.execute("""
                        select c.numero_titulo
                from comprobacion.comprobacion_lotes_sustituidos ls
                inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
                where c.numero_titulo = '"""+str(d)+"""'
                        """)
        dd = cursor1.fetchall()
        
        
        
        
        if len(dd) > 1:
            tipo = 2
            
        if len(dd) == 1:
            tipo = 1
        
        
    
    

    if tipo == 2:
        lvl_up = lvl_up + x
        print(Fore.YELLOW + ' TÍTULO '+str(titulo)+ ' SE UNIFICO CON LOS SIGUIENTES TITULOS')
        
        cursor1.execute("""
            select  c.numero_titulo, ls.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where ls.numero_titulo = '"""+str(titulo)+"""'
           order by ls.numero_titulo desc
           """)
        
        deri = cursor1.fetchall()
        
        ante = deri[0][0]
        
        cursor1.execute("""
                select  cast(fecha as date)
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
        where c.numero_titulo =  '"""+str(ante)+"""'""")
        
        fecha = cursor1.fetchall()[0][0]
        
        ante_n = str(titulo) +"""
        """+str(fecha)
        
        
        
        G.add_node(str(ante_n))
        G.add_edge(str(titulo_n), str(ante_n))
        act = busca_actos.r_actos(titulo)
        if len(act) > 0:
            e_labels[(str(titulo_n), str(ante_n))] = act
        
        cursor1.execute("""
            select  c.numero_titulo, ls.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where c.numero_titulo = '"""+str(ante)+"""'
           order by ls.numero_titulo desc
         """)
         
        derideri = cursor1.fetchall()
        nodos = 0
        for i in derideri:
            
            cursor1.execute("""
                select numero_titulo, fecha, superficie, cc.nombre, nombre_lote
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
    inner join catalogos.clase_concesion cc on c.id_clase_concesion = cc.id_clase_concesion
        where c.numero_titulo =  '"""+str(i[1])+"""'""")
            resul = cursor1.fetchall()
            print(Fore.WHITE + 'numero_titulo | fecha_registro | superficie' )
            print(resul)
            print(Fore.CYAN)
            busca_actos.busca_actos(i[1])
            
            if str(i[1]) == str(ante):
                continue
            else:
                if len(resul) > 0:
                    ante_n = str(i[1]) +'\n'+str(resul[0][1])
                else:
                    ante_n = str(i[1])
            
                nodos = nodos + y
                G.add_node(ante_n)
                G.add_edge(ante_n, str(ante))
                act = busca_actos.r_actos(i[1])
                if len(act) > 0:
                    e_labels[(ante_n, str(ante))] = act
                    
                node_pos[ante_n] = (lvl_up - 1, nodos)
           
        print('Los anteriores títulos fueron sustituidos por el título ' +str(ante))
        node_pos[str(ante)] = (lvl_up, nodos/2)
        
        traza_ahead(ante, lvl_up, node_pos, G)
          
    if tipo == 0:
        lvl_up = lvl_up + x
        print(Fore.YELLOW +' TÍTULO '+str(titulo) )
        print(Fore.WHITE +'numero_titulo | fecha_registro | superficie | nombre del lote' )   
        cursor1.execute("""
                               select numero_titulo, fecha, superficie, cc.nombre, nombre_lote
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
    inner join catalogos.clase_concesion cc on c.id_clase_concesion = cc.id_clase_concesion
        where c.numero_titulo =  '"""+str(titulo)+"""'""")
        resul = cursor1.fetchall()
        print(resul)
        print('El título ' + str(titulo) + ' no ha sido sustituido.')
        
        act = busca_actos.r_actos(titulo)
        if len(act) > 0:
            titulo_nn = str(titulo) +'\n'+str(resul[0][1])
            G.add_node('ULTREG')
            G.add_edge(str(titulo_nn), 'ULTREG' )
            e_labels[(str(titulo_nn), 'ULTREG')] = act
        
        node_pos['ULTREG'] = (lvl_up, node_pos[str(titulo_n)][1])
        
        
    if tipo == 1:
        lvl_up = lvl_up + x
        print(Fore.YELLOW +'TÍTULO '+str(titulo))
        print(Fore.WHITE +'numero_titulo | fecha_registro | superficie | nombre del lote' )
        cursor1.execute("""
             select  c.numero_titulo, ls.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where ls.numero_titulo = '"""+str(titulo)+"""'
           order by ls.numero_titulo desc
           """)
           
        deri = cursor1.fetchall()
        nodos = 0
        for i in deri:
            
            cursor1.execute("""
                               select numero_titulo, fecha, superficie, cc.nombre, nombre_lote
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
    inner join catalogos.clase_concesion cc on c.id_clase_concesion = cc.id_clase_concesion
        where c.numero_titulo =  '"""+str(i[0])+"""'""")
            resul = cursor1.fetchall()
          
            print(Fore.WHITE +'El título '+ str(titulo) +' fue sustituido por: ')
            print('numero_titulo | fecha_registro | superficie | nombre del lote' )
            print(resul)
            print(Fore.CYAN)
            busca_actos.busca_actos(i[0])
            
            if len(resul) > 0:
                ante_n = str(i[0]) +'\n'+str(resul[0][1])
            else:
                ante_n = str(i[0])
                
            cursor1.execute("""
                    select  cast(fecha as date)
        from comprobacion.comprobacion_concesion c
        inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
            where c.numero_titulo =  '"""+str(titulo)+"""'""")
            
            fec = cursor1.fetchall()
            
            titulo_nn = str(titulo)+'\n'+str(fec[0][0])
                
            nodos = nodos + y
            G.add_node(ante_n)
            G.add_edge(str(titulo_nn), ante_n )
            act = busca_actos.r_actos(titulo)
            if len(act) > 0:
                e_labels[(str(titulo_nn), ante_n)] = act
            
            node_pos[ante_n] = (lvl_up, node_pos[str(titulo_nn)][1])
            
            traza_ahead(i[0], lvl_up, node_pos, G)
    
    if tipo == 3:
        lvl_up = lvl_up + x
        print(Fore.YELLOW +'EL TÍTULO '+str(titulo)+ ' SE DIVIDIO')
        cursor1.execute("""
            select  c.numero_titulo, ls.numero_titulo
            from comprobacion.comprobacion_lotes_sustituidos ls
            inner join comprobacion.comprobacion_concesion c on ls.id_concesion = c.id_concesion
            where ls.numero_titulo = '"""+str(titulo)+"""'
           order by c.numero_titulo desc
           """)
           
        deri = cursor1.fetchall()
       
        
        
        print('El título '+ str(titulo) +' fue sustituido por: ')
        nodos = 0
        for i in deri:
            
            cursor1.execute("""
                                select numero_titulo, fecha, superficie, cc.nombre, nombre_lote
    from comprobacion.comprobacion_concesion c
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
    inner join catalogos.clase_concesion cc on c.id_clase_concesion = cc.id_clase_concesion
        where c.numero_titulo =  '"""+str(i[0])+"""'""")
            resul = cursor1.fetchall()
            print(Fore.WHITE +'numero_titulo | fecha_registro | superficie | nombre del lote' )
            print(resul)
            print(Fore.CYAN)
            busca_actos.busca_actos(i[0])
            print('a su vez:')
            
            if len(resul) > 0:
                ante_n = str(i[0]) +'\n'+str(resul[0][1])
            else:
                ante_n = str(i[0])
                
                
            cursor1.execute("""
                    select  cast(fecha as date)
        from comprobacion.comprobacion_concesion c
        inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
            where c.numero_titulo =  '"""+str(titulo)+"""'""")
            
            fec = cursor1.fetchall()
            
            titulo_nn = str(titulo)+'\n'+str(fec[0][0])
            
            nodos = nodos + y
            G.add_node(ante_n)
            G.add_edge(str(titulo_nn), ante_n)
            act = busca_actos.r_actos(titulo)
            if len(act) > 0:
                e_labels[(str(titulo_nn), ante_n)] = act
            node_pos[ante_n] = (lvl_up, nodos)
        
            traza_ahead(i[0], lvl_up, node_pos, G)
            
    
    return G, node_pos

traza(titulo, lvl_down, node_pos, G)
traza_ahead(titulo, lvl_up, node_pos, G)
    
for i in G:
    if i == titulo_n:
        color_map.append('#ff6200')
    else:
        color_map.append('#0380fc')


nx.draw(G, node_pos, node_color = color_map, with_labels = True,
        font_color = 'white', node_shape='o', node_size = 500, font_size = 4)


nx.draw_networkx_edge_labels(G, node_pos, edge_labels=e_labels, label_pos=0.5, font_size=4,
                             font_color='k', font_family='sans-serif', font_weight='normal',
                             alpha=None, bbox=None, horizontalalignment='center', 
                             verticalalignment='center', ax=None, rotate=True, clip_on=True)


plt.savefig("C:/Users/carlo/Documents/trazabilidad_02/graficas/simulador"+str(titulo)+".jpg", dpi=1000)  

img = Image.open("C:/Users/carlo/Documents/trazabilidad_02/graficas/simulador"+str(titulo)+".jpg")
img.show()
                
            
    
            
        
    