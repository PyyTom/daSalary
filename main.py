#!/usr/bin/env python3
import sqlite3,datetime,locale,os
locale.setlocale(locale.LC_ALL,'es_ES')
meses= {'ENERO':31, 'FEBRERO':28, 'MARZO':31, 'ABRIL':30, 'MAYO':31, 'JUNO':30, 'JULIO':31, 'AGOSTO':31, 'SEPTIEMBRE':30, 'OCTUBRE':31, 'NOVIEMBRE':30,'DICIEMBRE':31}
if os.path.isdir('ARCHIVO')==False:os.mkdir('ARCHIVO')
db=sqlite3.connect('ARCHIVO/'+str(datetime.datetime.today().year)+'.db')
if db.execute('select name from sqlite_master').fetchall()==[]:
    for mes in meses:
        db.execute('create table if not exists '+mes+'(DIA integer,HORAS float)')
        for dia in range(1,meses[mes]+1):
            db.execute('insert into '+mes+' values(?,?)',(dia,0.00,))
            db.commit()
from distutils.dir_util import copy_tree
copy_tree('ARCHIVO','/Users/tommylatorre/Desktop/ARCHIVO/SALARIO')
db.close()
from flet import *
def main(page:Page):
    def muestra(e):
        r_mensuales.controls,r_horas.controls,r_dias.controls,horas_anuales,anual,m=[],[],[],0.0,0,0
        for mes in meses:
            m+=1
            c_dias=Column([],scroll=ScrollMode.ALWAYS,width=110,height=500)
            db = sqlite3.connect('ARCHIVO/' + d_anos.value + '.db')
            horas=db.execute('select sum(HORAS) from '+mes).fetchone()[0]
            if horas<60:mensual=0
            else:
                horas_plus=horas-60
                mensual_plus=horas_plus*8
                mensual=475+mensual_plus
            for dia in db.execute('select * from ' + mes).fetchall():
                if dia[1]==0.0:color='white'
                else:color='green'
                dia_s=str(datetime.datetime(int(d_anos.value),int(m),int(dia[0])).strftime('%A'))[0:3]
                c_dias.controls.append(Container(bgcolor=color,content=TextButton(dia_s+str(dia[0])+' '+str(dia[1])+' h',on_click=lambda x,mes=mes,dia=dia[0],horas=dia[1]:edita(mes,dia,horas))))
            db.close()
            r_dias.controls.append(c_dias)
            r_horas.controls.append(Text(str(horas)+' HORAS',width=110,text_align=TextAlign.CENTER))
            r_mensuales.controls.append(Text(str(mensual) + ' €', width=110,text_align=TextAlign.CENTER))
            horas_anuales+=horas
            anual+=mensual
        t_anual.value=str(anual)+' €, '
        t_horas_anuales.value=str(horas_anuales)+' HORAS'
        page.update()
    def guarda(mes,dia,horas):
        if horas=='':dialog.title=Text('NO HAS PUESTO LAS HORAS')
        else:
            db=sqlite3.connect('ARCHIVO/'+d_anos.value+'.db')
            db.execute('update '+mes+' set HORAS=? where DIA=?',(horas,dia,))
            db.commit()
            db.close()
            dialog.title=Text('GUARDADO CON EXITO')
            t_horas.value=''
            r_edit.controls=[]
            muestra('')
        dialog.open=True
        page.update()
    def edita(mes,dia,horas):
        def cambia(e):
            if e==('-'):t_horas.value-=0.5
            else:t_horas.value+=0.5
            page.update()
        t_mes.value,t_dia.value,t_horas.value=mes,dia,horas
        r_edit.controls=[t_dia,t_mes,b_menos,t_horas,b_mas,b_guarda]
        b_menos.on_click,b_mas.on_click=lambda _:cambia('-'),lambda _:cambia('+')
        b_guarda.on_click=lambda _:guarda(t_mes.value,t_dia.value,t_horas.value)
        page.update()
    page.window.full_screen=True
    page.theme_mode=ThemeMode.LIGHT
    dialog=AlertDialog(title=Text())
    page.overlay.append(dialog)
    d_anos=Dropdown(options=[dropdown.Option(ano[:-3]) for ano in os.listdir('ARCHIVO')],on_change=muestra)
    t_anual,t_horas_anuales=Text(size=20),Text(size=20)
    t_dia,t_mes,t_horas,b_menos,b_mas,b_guarda=Text(size=30),Text(size=30),TextField(label='HORAS',width=75),ElevatedButton('-',width=50),ElevatedButton('+',width=50),ElevatedButton('GUARDA')
    r_dias,r_horas,r_mensuales,r_edit=Row(),Row(),Row(),Row(alignment=MainAxisAlignment.CENTER)
    page.add(Row([IconButton(icon=icons.EXIT_TO_APP_OUTLINED,icon_size=50,icon_color='red',on_click=lambda _:page.window.destroy())],alignment=MainAxisAlignment.END),
             Row([d_anos,t_anual,t_horas_anuales],alignment=MainAxisAlignment.CENTER),
             Divider(),
             Row([Text(mes,width=109,text_align=TextAlign.CENTER) for mes in meses]),
             r_dias,
             Divider(),
             r_horas,
             r_mensuales,
             Divider(),
             r_edit)
app(target=main,assets_dir='assets')