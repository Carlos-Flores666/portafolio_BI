# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 13:02:54 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 13:37:48 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 23 16:34:10 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Tue May 16 18:03:02 2023

@author: carlo
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 11 16:57:02 2023

@author: carlo
"""

import psycopg2



conn = psycopg2.connect(host= "",
                        database="", 
                        user="", 
                        password="")

conn2 = psycopg2.connect(host= "",
                        database="", 
                        user="", 
                        password="")

conn.autocommit = True
conn2.autocommit = True
cursor1 = conn.cursor()
cursor2 = conn2.cursor()



def busca_actos(titulo):
    #REVISADO CON DOS OPCIONES
    cursor1.execute("""
                    select numero_titulo, 
    case when id_tipo_persona = 1 then 'PERSONA FÍSICA'
    when id_tipo_persona = 2 then 'PERSONA MORAL' end,
    nombre_titular, t.primer_apellido, t.segundo_apellido, porcentaje_participacion, fecha_expedicion
    from dgm.concesion c
    inner join comprobacion.comprobacion_titulares t on c.id_concesion = t.id_concesion
    where numero_titulo = '"""+str(titulo)+"""'""")

    '''cursor1.execute("""
                    select numero_titulo, 
    case when id_tipo_persona = 1 then 'PERSONA FÍSICA'
    when id_tipo_persona = 2 then 'PERSONA MORAL' end,
    nombre_titular, t.primer_apellido, t.segundo_apellido, porcentaje_participacion, fecha
    from dgm.concesion c 
    inner join comprobacion.comprobacion_generales g on c.id_concesion = g.id_concesion
    inner join comprobacion.comprobacion_titulares t on c.id_concesion = t.id_concesion
    where numero_titulo = '"""+str(titulo)+"""'""")
    '''
    
    titulares_origen = cursor1.fetchall()
    print('TITULARES ORIGINARIOS:')
    
    print('TÍTULO | TIPO PERSONA | NOMBRE | PRIMER APELLIDO | SEGUNDO APELLIDO | PORCENTAJE DE TITULARIDAD | FECHA REGISTRO')
    
    for i in titulares_origen:
        print(i)
    #REVISADO
    cursor2.execute("""
                   select row_number() over(order by fecha_registro), *
                   from (select distinct numero_titulo, ta.nombre, fecha_registro
    from actos.actos_captura a
    inner join actos.actos_registrador r on a.id_actos_captura = r.id_acto_captura
    inner join actos.actos_partes pa on a.id_actos_captura = pa.id_actos_captura
    inner join actos.actos_titulos p on pa.id_acto_parte = p.id_acto_parte
    inner join catalogos.tipo_acto ta on a.id_tipo_acto = ta.id_tipo_acto
    where numero_titulo = '"""+str(titulo)+"""') a
    order by fecha_registro
                    """)
                    
    actos = cursor2.fetchall()
    
    if len(actos) == 0:
        print('NO SE ENCONTRARON ACTOS CONTRATOS O CONVENIOS RELACIONADOS CON EL TÍTULO ')
    
    else:
        print('ACTOS CONTRATOS Y CONVENIOS RELACIONADOS:')
        
        print('ORDEN | TÍTULO | TIPO DE ACTO | FECHA DEL ACTO ')
        
        for i in actos:
            print(i)
        #REVISADO    
        cursor2.execute("""
                        select id_acto
                        from (select distinct a.id_acto, fecha_registro
                        from actos.actos_captura a
                        inner join actos.actos_registrador r on a.id_acto_captura = r.id_acto_captura
                        inner join actos.actos_partes pa on a.id_actos_captura = pa.id_actos_captura
                        inner join actos.actos_titulos p on pa.id_acto_parte = p.id_acto_parte
                        where numero_titulo = '"""+str(titulo)+"""') a
                        order by fecha_registro
                        """)
        id_actos = cursor2.fetchall()
                        
        
        
        for j in id_actos:
            
            id_acto = j[0]
            
            cursor2.execute("""
                            select pv.numero_titulo,tp.nombre, pa.nombre, pa.primer_apellido, pa.segundo_apellido,
                        pa.afectacion, fecha_registro
                        from actos.actos_titulos pv
                        inner join actos.actos_partes ap on ap.id_acto_parte = pv.id_acto_parte
                        inner join actos.actos_captura ac on ac.id_acto_captura = ap.id_acto_captura
                        inner join actos.actos_titular pa on pv.id_acto_parte = pa.id_acto_parte
                        inner join actos.actos_registrador r on r.id_acto_captura = ac.id_acto_captura
                        inner join catalogos.tipo_parte tp on tp.id_tipo_parte = pa.id_tipo_parte
                        where ac.id_acto_captura in  ("""+str(id_acto)+""") and numero_titulo = '"""+str(titulo)+"""'
                        order by fecha_registro
                            """)
                            
            detalle_acto = cursor2.fetchall()
            
            #print('ORDEN | TÍTULO | TIPO DE ACTO | FECHA DEL ACTO ')
            #print(actos[int(select_acto)-1])
            
            print('             CEDENTE             |            CESIONARIO            |     PORCENTAJE CEDIDO   |  FECHA DEL ACTO')
            
            for i in detalle_acto:
                
                print(i)

       
    
def r_actos(titulo):

    
    cursor2.execute("""
                   select nombre, cast(fecha_registro as date)
                   from (select distinct numero_titulo, ta.nombre, fecha_registro, ta.id_tipo_acto
    from actos.actos_captura a
    inner join actos.actos_registrador r on a.id_acto_captura = r.id_acto_captura
    inner join actos.actos_partes pa on a.id_actos_captura = pa.id_actos_captura
    inner join actos.actos_titulos p on pa.id_acto_parte = p.id_acto_parte
    inner join catalogos.tipo_acto ta on a.id_tipo_acto = ta.id_tipo_acto
    where numero_titulo = '"""+str(titulo)+"""') a
    where a.id_tipo_acto in (150
,195
,102
,103
,105
,145
,146
,147
,153
,154
,3
,106
,107
,108
,111
,113
,179
,184
,192
,200
,201
,212
,214
,218
,241
,157
,159
,161
,163
,173
,243
,244
,245
,249
,4
,5
,6
,124
,2
,8
,24
,27
,29
,30
,33
,36
,37
,38
,39
,40
,41
,42
,52
,55
,89
,93
,117
,119
,120
,122
,128
,143
,144
,10
,23 )
    order by fecha_registro
                    """)
                    
    actos = cursor2.fetchall()
    
    act = ''
    count=0
    for i in actos:
        count = count + 1
        if count < len(actos):
            act = act + str(i[0])+' '+str(i[1])+ """
            """
        if count == len(actos):
            act = act + str(i[0])+' '+str(i[1])
    
    
    return act