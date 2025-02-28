# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 23:06:00 2022

@author: Carlos Israel Flores Vega
"""

from PIL import Image, ImageDraw
import cv2



import psycopg2

conn = psycopg2.connect(host= "localhost",
                        database="", 
                        user="", 
                        password="")
cursor1 = conn.cursor()

palabras = input('Escriba las palabras que desea buscar (máximo 2 separadas por un espacio): ')

palabras = palabras.split(' ')

    ####DOS PALABRAS
if len(palabras) > 1:
    
    palabra1 = palabras[0]
    palabra2 = palabras[1]

    cursor1.execute("""
                    select  pa.volumen, imagen, palabra, id_palabra, fecha_ini, fecha_fin
                    from public.ocr_palabras pa
                    inner join public.catalogo_libros lib on pa.volumen = lib.volumen
    where upper(palabra) like '%"""+palabra1.upper()+"""%' and imagen in (select imagen 
    												from public.ocr_palabras where upper(palabra) like '"""+palabra2.upper()+"""'  )
    order by volumen, imagen
    """)
    result = cursor1.fetchall()

    count = 0
    for i in result:
        count = count + 1
        
        
        volumen = i[0]
        imagen = i[1]
        fecha_ini = i[4]
        fecha_fin = i[5]
        
        print(count,'volumen: ',volumen,'fecha:', fecha_ini, ' a ', fecha_fin, 'imagen: ',imagen )
    
    
    print(count, 'Coincidencias encontradas.')
        
    abrir = input('Seleccione el número de imagen que desea ver: ')
    
    count_2 = 0
    for i in result:
        count_2 = count_2 + 1
        
        
        volumen = str(i[0])
        imagen = i[1]
        
        if count_2 == int(abrir):
            
            
            ##############ABRE LA IMAGEN SELECCIONADA##########
            cv = cv2.imread("C:/Users/carlo/Downloads/sociedades_mineras/VOL. "+volumen+" SM/VOL. "+volumen+" SM/"+imagen)
            img = Image.open("C:/Users/carlo/Downloads/sociedades_mineras/VOL. "+volumen+" SM/VOL. "+volumen+" SM/"+imagen)
            
            for palabra in palabras:
                
                largo = len(palabra)
            
                ####VERIFIACION UNICIDAD ID BOX
            
            
                texto2 = ("""select id_box
                from (
                select *, concat(split_part(charcter,' ',1)""")
                
                countxx = 1
                while countxx < largo:
                    texto2 = texto2 + ",lead(split_part(charcter,' ',1),"+str(countxx)+") over (order by id_box) "
                    countxx = countxx + 1
                    
                texto2 = texto2 + (""") palabra
                from public.ocr_boxes where imagen = '"""+imagen+"""' ) box where palabra = '"""+palabra.upper()+"""'""")
                
                
                cursor1.execute(texto2)
                
                veri = cursor1.fetchall()
                
                if len(veri) > 1:
                    for j in veri:
                        cursor1.execute("""
                                        select  split_part(charcter, ' ', 2) x1,
                split_part(charcter, ' ', 3) y1,
                split_part(charcter, ' ', 4) x2,
                split_part(charcter, ' ', 5) y2, volumen from public.ocr_boxes where id_box between """+str(j[0])+"""  and  + """+str(j[0])+"""+"""+str(largo))
                
                        coordenadas = cursor1.fetchall()
                
                        x1 = int(coordenadas[0][0])
                        y1 = int(coordenadas[0][1])
                        x2 = int(coordenadas[largo-1][2])
                        y2 = int(coordenadas[largo-1][3])
                
                
                        size = cv.shape
                
                        y_size = size[0]
                        
                        draw = ImageDraw.Draw(img)
                        
                        draw.rectangle((x1, y_size-y1, x2, y_size-y2),  outline=(255,0, 0))
                        
                    
                
                #####
                
                else:
        
                    countxx = 1
                    
                    texto = ("""select  split_part(charcter, ' ', 2) x1,
                    split_part(charcter, ' ', 3) y1,
                    split_part(charcter, ' ', 4) x2,
                    split_part(charcter, ' ', 5) y2, volumen from public.ocr_boxes where id_box between (select id_box
                    from (
                    select *, concat(split_part(charcter,' ',1)""")
                    
                    while countxx < largo:
                        texto = texto + ",lead(split_part(charcter,' ',1),"+str(countxx)+") over (order by id_box) "
                        countxx = countxx + 1
                        
                    texto = texto + (""") palabra
                    from public.ocr_boxes where imagen = '"""+imagen+"""' ) box where palabra = '"""+palabra.upper()+"""'
                    ) and (select id_box
                    from (
                    select *, concat(split_part(charcter,' ',1)""")
                                     
                    
                                     
                    countxx = 1
                    
                    while countxx < largo:
                        texto = texto + ",lead(split_part(charcter,' ',1),"+str(countxx)+") over (order by id_box) "
                        countxx = countxx + 1
                        
                    query = texto + (""") palabra
                    from public.ocr_boxes where imagen = '"""+imagen+"""' ) box where palabra = '"""+palabra.upper()+"""'
                    ) + """+str(countxx-1))
                    
                  
                    cursor1.execute(query)
                    
                    coordenadas = cursor1.fetchall()
                    
                    x1 = int(coordenadas[0][0])
                    y1 = int(coordenadas[0][1])
                    x2 = int(coordenadas[largo-1][2])
                    y2 = int(coordenadas[largo-1][3])
                    
                    
                    size = cv.shape
            
                    y_size = size[0]
                    
                    draw = ImageDraw.Draw(img)
                    
                    draw.rectangle((x1, y_size-y1, x2, y_size-y2),  outline=(255,0, 0))
                    
                
    
else:
    palabra = palabras[0]
    ####UNA PALABRA
    cursor1.execute("""
                    select  pa.volumen, imagen, palabra, id_palabra, fecha_ini, fecha_fin
                    from public.ocr_palabras pa
                    inner join public.catalogo_libros lib on pa.volumen = lib.volumen
    where upper(palabra) like '"""+palabra.upper()+"""' order by volumen, imagen
    """)
    
    result = cursor1.fetchall()
    
    count = 0
    for i in result:
        count = count + 1
        
        
        volumen = i[0]
        imagen = i[1]
        fecha_ini = i[4]
        fecha_fin = i[5]
    
        
        print(count,'volumen: ',volumen,'fecha:', fecha_ini, ' a ', fecha_fin, 'imagen: ',imagen )
    
    
    print(count, 'Coincidencias encontradas.')
        
    abrir = input('Seleccione el número de imagen que desea ver: ')
    
    count_2 = 0
    for i in result:
        count_2 = count_2 + 1
        
        
        volumen = str(i[0])
        imagen = i[1]
        
        if count_2 == int(abrir):
            
            largo = len(palabra)
            
            ##########ABRE LA IMAGEN SELECCIONADA ###########
            cv = cv2.imread("C:/Users/carlo/Downloads/sociedades_mineras/VOL. "+volumen+" SM/VOL. "+volumen+" SM/"+imagen)
            img = Image.open("C:/Users/carlo/Downloads/sociedades_mineras/VOL. "+volumen+" SM/VOL. "+volumen+" SM/"+imagen)
    
            
            ####VERIFIACION UNICIDAD ID BOX
            
            
            texto2 = ("""select id_box
            from (
            select *, concat(split_part(charcter,' ',1)""")
            
            countxx = 1
            while countxx < largo:
                texto2 = texto2 + ",lead(split_part(charcter,' ',1),"+str(countxx)+") over (order by id_box) "
                countxx = countxx + 1
                
            texto2 = texto2 + (""") palabra
            from public.ocr_boxes where imagen = '"""+imagen+"""' ) box where palabra = '"""+palabra.upper()+"""'""")
            
            
            cursor1.execute(texto2)
            
            veri = cursor1.fetchall()
            
            if len(veri) > 1:
                for j in veri:
                    cursor1.execute("""
                                    select  split_part(charcter, ' ', 2) x1,
            split_part(charcter, ' ', 3) y1,
            split_part(charcter, ' ', 4) x2,
            split_part(charcter, ' ', 5) y2, volumen from public.ocr_boxes where id_box between """+str(j[0])+"""  and  + """+str(j[0])+"""+"""+str(largo) )
            
                    coordenadas = cursor1.fetchall()
            
                    x1 = int(coordenadas[0][0])
                    y1 = int(coordenadas[0][1])
                    x2 = int(coordenadas[largo-1][2])
                    y2 = int(coordenadas[largo-1][3])
            
            
                    size = cv.shape
            
                    y_size = size[0]
                    
                    draw = ImageDraw.Draw(img)
                    
                    draw.rectangle((x1, y_size-y1, x2, y_size-y2),  outline=(255,0, 0))
                    
                
            
            #####
            
            else:
    
                countxx = 1
                
                texto = ("""select  split_part(charcter, ' ', 2) x1,
                split_part(charcter, ' ', 3) y1,
                split_part(charcter, ' ', 4) x2,
                split_part(charcter, ' ', 5) y2, volumen from public.ocr_boxes where id_box between (select id_box
                from (
                select *, concat(split_part(charcter,' ',1)""")
                
                while countxx < largo:
                    texto = texto + ",lead(split_part(charcter,' ',1),"+str(countxx)+") over (order by id_box) "
                    countxx = countxx + 1
                    
                texto = texto + (""") palabra
                from public.ocr_boxes where imagen = '"""+imagen+"""' ) box where palabra = '"""+palabra.upper()+"""'
                ) and (select id_box
                from (
                select *, concat(split_part(charcter,' ',1)""")
                                 
                
                                 
                countxx = 1
                
                while countxx < largo:
                    texto = texto + ",lead(split_part(charcter,' ',1),"+str(countxx)+") over (order by id_box) "
                    countxx = countxx + 1
                    
                query = texto + (""") palabra
                from public.ocr_boxes where imagen = '"""+imagen+"""' ) box where palabra = '"""+palabra.upper()+"""'
                ) + """+str(countxx-1))
                
              
                cursor1.execute(query)
                
                coordenadas = cursor1.fetchall()
                
                x1 = int(coordenadas[0][0])
                y1 = int(coordenadas[0][1])
                x2 = int(coordenadas[largo-1][2])
                y2 = int(coordenadas[largo-1][3])
                
                
                size = cv.shape
        
                y_size = size[0]
                
                draw = ImageDraw.Draw(img)
                
                draw.rectangle((x1, y_size-y1, x2, y_size-y2),  outline=(255,0, 0))
                
                
###########   img es la imagen resultado  ############            
img.show()
