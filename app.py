'''
Application that selects a rgb color and 
sends via serial port to arduino by lighting the LED with the corresponding color
Author: Juliana Rosin
September/2019 
'''
from tkinter import *
import serial
import time

class Comm:
    def __init__(self):
        self.name_port = '/dev/ttyACM0'
        self.baud = 9600    

    def connect_port(self):
        self.port = serial.Serial(port=self.name_port, baudrate=self.baud,timeout=1)

    def write_port(self,frame):
        x = bytearray(frame,'utf-8')
        self.port.write(x)
    
    def disconnect_port(self):
        self.port.close()


class Application:
    def __init__(self,janela_pai):
        self.cl_janela_pai = janela_pai
        self.cl_obj_comm = Comm()
        self.cl_flag_comm = False
        self.show_layout_app() 

    def show_layout_app(self):
        ph_logo = PhotoImage(file='img/logo.png')
        lb_logo = Label(self.cl_janela_pai,image=ph_logo,borderwidth=0)
        lb_logo.imagem = ph_logo 
        lb_logo.place(x=0,y=0)
        
        lb_title = Label(self.cl_janela_pai,text='LED CONTROL RGB',bg='white').place(x=170,y=50)
        self.lb_color = Label(self.cl_janela_pai,width=8,bg='#FF0000',highlightthickness=2)
        self.lb_color.place(x=100,y=130)

        self.ent_color = Entry(self.cl_janela_pai,width=8)
        self.ent_color.place(x=170,y=130)
        self.ent_color.insert(END,'FF0000')

        self.bt_envia_color = Button(self.cl_janela_pai,width=2,text='send',command=self.command_bt_send_color)
        self.bt_envia_color.place(x=250,y=125)

        lb_arduino = Label(self.cl_janela_pai,text='Arduino',bg='white').place(x=170,y=170)

        self.bt_conn_arduino = Button(self.cl_janela_pai,width=2,text='OFF',command=self.command_bt_conect)
        self.bt_conn_arduino.place(x=250,y=165)

        self.lb_alert = Label(self.cl_janela_pai,text='',bg='white')
        self.lb_alert.place(x=170,y=200)
       
    def command_bt_conect(self):
        if self.bt_conn_arduino['text'] == 'OFF':
            try:
                self.cl_obj_comm.connect_port()
                self.bt_conn_arduino['text'] = 'ON'
                self.cl_flag_comm = True
            except:
                self.lb_alert['text'] = 'error connecting arduino'
        else:
            try:
                self.bt_conn_arduino['text'] = 'OFF'
                self.cl_obj_comm.disconnect_port()
                self.cl_flag_comm = False
            except:
                self.lb_alert['text'] = 'error disconnecting arduino'

    def command_bt_send_color(self):
        valor = self.ent_color.get()
        if valor != '' and len(valor)== 6:
            try:
                r,g,b = int(valor[0:2],16),int(valor[2:4],16),int(valor[4:6],16)
                self.lb_alert['text'] = ''
                self.lb_color['bg'] ='#'+valor
                if self.cl_flag_comm:
                    frame = str(r).zfill(3)+str(g).zfill(3)+str(b).zfill(3)
                    self.cl_obj_comm.write_port(frame)
            except:
                self.lb_alert['text'] = 'Invalid Value'
        else:
             self.lb_alert['text'] = 'Invalid Value'

    def disconnect_port_app(self):
        if self.cl_flag_comm:
            self.cl_obj_comm.disconnect_port()
  



if __name__ == "__main__":
    janela= Tk()
    janela.geometry('%dx%d+%d+%d' % (400,400,50,50))
    janela.configure(bg='white')
    janela.title('LED CONTROL RGB')
    janela.resizable(False, False)
    app = Application(janela)
    janela.mainloop()
    app.disconnect_port_app()