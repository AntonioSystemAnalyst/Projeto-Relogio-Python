import math
import time
import json
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.font import BOLD
from matplotlib.pyplot import fill
from numpy import append

# ----------------------------------------- #
# esse bloco aqui configura a janela
root = tk.Tk()
root.title("Relógio GMT")
root.geometry("455x560+400+30")
root.configure(background='#808080')
root.resizable(False, False)
# ----------------------------------------- #
# lista para carregar as cidades
cidades = [] 
# lista para carregar os fusos horarios
fuso    = [] 
# lista para carregar cada região
regiao  = [] 
# lista para carregar objetos do tipo create_line
textnumber = []

# number é a lista de número do relógio, que vai mudar conforme os cliques em left e right
number  = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

# star recebe a posição inicial de cada um dos asteriscos que forma a coroa
stars=[54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 
36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53]

# vetores incrementais para a primeira ver que será carregado
h=iter(['12','1','2','3','4','5','6','7','8','9','10','11'])
v=iter(['24','1','2','3','4','5','6','7','8','9','10','11','12', '13','14','15','16','17','18',
'19','20','21','22','23'])

# para configurar os espaços dos riscos na coroa fixa
x,y=220,260
x1,y1,x2,y2=x,y,x,10 

# para configura a dimensão de cada item 
r1=130 # dial lines for one minute 
r2=100 # for hour numbers  after the lines 
r3=120 # four GMT
r4=145 # for hour numbers  after the lines GMT
r5=160 # for coroa
rs= 80 # length of second needle 
rm= 80 # length of minute needle
rh= 60 # lenght of hour needle
rgmt = 90 # lenght of hour GMT

# pega os dados do relógio do pc, e transforma eles em angulos
in_degree = 0
in_degree_s=int(time.strftime('%S'))*6 # local second 
in_degree_m=int(time.strftime('%M'))*6 # local minutes  
in_degree_h=int(time.strftime('%I'))*30 # 12 hour format 
in_degree_GMT =  in_degree_h + 90

# variavel para controlar os botões de left e right
controle_Coroa = 1
# variavel para texto do fuso horario
TxtFuso = "Sao_Paulo"
# ------------------------------------------------ #
# esse bloco pega os dados do arquivo j.son e passa eles para as listas (cidades, fuso e regiao)
try:
    f = open ("dados/localtime.json", "r")
    data = json.load(f)
    for c in data['cities']:
        cidades.append (c['city'])
        fuso.append (c['offset'])
        regiao.append (c['region'])
    f.close() 
except Exception as e:
    print (e)
    print ("No localtime file available")
# ------------------------------------------------ #
# essa função pega a cidade que foi escolhida e posiciona o ponteiro vermelho no fuso horario dela
# @autor Antonio
def Func_Fuso ():
    global in_degree_GMT,Mgmt
    cmb = root.combo_mat.get()  # pega o nome da cidade
    qtd = len(cidades) # pega a quantidade de de elementos da lista de cidades     
    for i in range(0, qtd): 
        if (cmb == cidades[i]): # o mesmo indice da lista de cidades é referente ao seu fuso na lista de fuso 
            F = fuso[i]  # por isso usamos o mesmo i para por o fuso em F

    if (F > 0 or F == -3): # se o fuso for maior que zero ou igual a -3
        if (F == -3): # no caso de ser -3, F fica com o valor de 90 graus é que o mesmo que 3 horas (1 hora é igual a 30 graus)
            F = 90
        else:
            F = (F+3) * 30 # no caso de ser maior que zero, somamos ele com +3 (fuso de São Paulo/Rio de Janeiro) e multiplicamos por 30
        in_degree_GMT= in_degree_h+F  #s somamos ao valor em graus que esta nas horas
        in_radian = math.radians(in_degree_GMT) # passamos para radianos 
        c1.delete(Mgmt) # deletamos o ponteiro anterior
        x2=x+rgmt*math.sin(in_radian) # fazemos novas coordenadas
        y2=y-rgmt*math.cos(in_radian) 
        Mgmt=c1.create_line(x,y,x2,y2,width=2,fill='Red', arrow='last') # criamos o novo ponteiro com as novas coordenadas 
        if(in_degree_GMT>360): # caso seja maior que 360 graus.. tiramos 360 e ficamos com o resto
            in_degree_GMT=in_degree_GMT-360
        if(in_degree_GMT==360): # se for igual a 360 graus.. passamos o angulo para 0
             in_degree_GMT=0

    else:
        F = (F+3) * 30 * -1   # caso seja um fuso negativo é preciso somar e multiplicar por -1.. o restante é igual o de cima
        in_degree_GMT= in_degree_h-F # ai tiramos o resultado F doq ja estava
        in_radian = math.radians(in_degree_GMT) 
        c1.delete(Mgmt)
        x2=x+rgmt*math.sin(in_radian)
        y2=y-rgmt*math.cos(in_radian) 
        Mgmt=c1.create_line(x,y,x2,y2,width=2,fill='Red', arrow='last')
        if(in_degree_GMT>360):
            in_degree_GMT=in_degree_GMT-360
        if(in_degree_GMT==360):
             in_degree_GMT=0
 # ------------------------------------------------ #
 # esse bloco construi os elementos da janela
root.combo_mat = ttk.Combobox(root, values=cidades, state='readonly')
root.combo_mat.grid(column=0, row=1)
root.combo_mat.set(value="Sao_Paulo")
root.combo_mat.place(relx=0.675, rely=0.945, relheight=0.04, relwidth=0.21)
cmb = root.combo_mat.get()
root.lb_Fuso = Label(root, text='Fuso Horários - GMT', bg='#808080', fg='#000000', font="3")
root.lb_Fuso.place (rely=0.900, relx=0.275, relwidth=0.4, relheight=0.04)
root.lb_Fuso = Label(root, text='Coroa', bg='#808080', fg='#000000', font="3")
root.lb_Fuso.place (rely=0.900, relx=0.105, relwidth=0.1, relheight=0.04)
root.bt_Fuso = Button(root, text='Ativar Fuso', font='verdona-bold 8', bg='#808080', fg='#000000', command=lambda:Func_Fuso())
root.bt_Fuso.place(rely=0.945, relx=0.375, relwidth=0.2, relheight=0.04)
root.bt_Cora1 = Button(root, text='Left', font='verdona-bold 8', bg='#808080', fg='#000000', command=lambda:coroa(-1))
root.bt_Cora1.place(rely=0.945, relx=0.04, relwidth=0.12, relheight=0.04)
root.bt_Cora2 = Button(root, text='Right', font='verdona-bold 8', bg='#808080', fg='#000000', command=lambda:coroa(1))
root.bt_Cora2.place(rely=0.945, relx=0.160, relwidth=0.12, relheight=0.04)    
 # ------------------------------------------------ #
 # aqui subimos a imagem do relógio
img = tk.PhotoImage(file="image/relogio.png")
img = img.subsample(2,2)
 # aqui construimos um canvas e subimos a imagem nele
c1 = tk.Canvas(root, width=455, height=499)
c1.create_image(690 // 3.07, 700 // 2.8, image=img)
c1.grid(row=0,column=0,padx=0,pady=0,columnspan=1)
 # ------------------------------------------------ #
 # essa função cria um ciruclo - importante pra criar o primeiro circulo de c1
 # @param x - valor inteiro para posição x  
 # @param y - valor inteiro para posição y
 # @param r - valor do raio do circulo
 # @return create_oval- uma figura oval do canvas com as dimensões passadas
def create_circle(x, y, r, canvasName): 
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    return canvasName.create_oval(x0, y0, x1, y1, width=10, outline='black', fill='black' )
create_circle(216, 260, 160, c1)
# criando o circulo c1
center=c1.create_oval(56,100,376,420,fill='black')
 # ------------------------------------------------ #
 # esse bloco cria os numeros e as coroas
in_degree = 0
for i in range(0,60):
    in_radian = math.radians(in_degree)
    if(i%5==0): 
        ratio=0.85
        t1=x+r2*math.sin(in_radian) 
        t2=x-r2*math.cos(in_radian) 
        c1.create_text(t1+3,t2+40,fill='White',font="Times 12  bold",text=next(h)) 
    else:
        ratio=0.9

    x1=x+ratio*r1*math.sin(in_radian)
    y1=y-ratio*r1*math.cos(in_radian)
    x2=x+r1*math.sin(in_radian)
    y2=y-r1*math.cos(in_radian)
    c1.create_line(x1,y1,x2,y2,width=1, fill='white') 
    in_degree=in_degree+6

in_degree = 0
for i in range(0,120):
    in_radian = math.radians(in_degree)
    if(i%5 == 0):
        t1=x+r4*math.sin(in_radian) 
        t2=x-r4*math.cos(in_radian) 
        textnumber.append(c1.create_text(t1+3,t2+40,fill='green',font="Times 8  bold",text=next(v))) 
    in_degree=in_degree+3

in_degree = 0
ax = 0
for i in range(0,360):
    in_radian = math.radians(in_degree)
    if(i%5 == 0):
        t1=x+r5*math.sin(in_radian) 
        t2=x-r5*math.cos(in_radian) 
        if (stars[ax]<36):
            c1.create_text(t1+3,t2+40,fill='red',font="Times 8  bold",text="*") 
        else:
            c1.create_text(t1+3,t2+40,fill='blue',font="Times 8  bold",text="*") 
        ax = ax  + 1
    in_degree=in_degree+1  
                  
# ------------------------------------------------------ #
# essa função muda a coroa conforme se clica em left e right
# @param valo - determina qual dos botões foram acionados
# @autor Antonio
def coroa (valor): 

    global controle_Coroa, number, v, textnumber, stars   
    indice_six = 0
    indice_star = 0

    if (valor > 0):
        if (controle_Coroa+1>23):
            controle_Coroa = 0
            ajusta_vetor_numeros (0)
        else:
            controle_Coroa = controle_Coroa + 1
            ajusta_vetor_numeros (controle_Coroa)
    else:
        if (controle_Coroa-1 < 0):
            controle_Coroa = 23
            ajusta_vetor_numeros (23)
        else:
            controle_Coroa = controle_Coroa - 1
            ajusta_vetor_numeros (controle_Coroa)

    for i in range (0, 24):
        if (number[i] == 6):
            indice_six = i
    
    if (indice_six>6):
        indice_star = (indice_six-6)*3+19
    else:
        indice_star = 19-(6-indice_six)*3 
    ajusta_vetor_stars(indice_star)

    in_degree = 0
    cont      = 0
    qtd = len(textnumber)
    for i in range(0, qtd):
         c1.delete(textnumber[i])
    for i in range(0,120):
        in_radian = math.radians(in_degree)
        if(i%5 == 0):
            t1=x+r4*math.sin(in_radian) 
            t2=x-r4*math.cos(in_radian) 
            textnumber[cont]=c1.create_text(t1+3,t2+40,fill='green',font="Times 8  bold",text=str(number[cont]))
            cont = cont + 1 
        in_degree=in_degree+3

    in_degree = 0
    ax = 0
    for i in range(0,360):
            in_radian = math.radians(in_degree)
            if(i%5 == 0):
                t1=x+r5*math.sin(in_radian) 
                t2=x-r5*math.cos(in_radian) 
                if (stars[ax]<36):
                    c1.create_text(t1+3,t2+40,fill='red',font="Times 8  bold",text="*") 
                else:
                    c1.create_text(t1+3,t2+40,fill='blue',font="Times 8  bold",text="*") 
                ax = ax  + 1
            in_degree=in_degree+1

# ------------------------------------------------------ #
# essa função reorganiza o vetor de numeros para mostra-la na janela
# @param indice - valor para realocar o vetor
# @autor Antonio
def ajusta_vetor_numeros (indice):
    global number, stars
    controle  = 0 
    cont = 1
    ax_indice = indice
    while (ax_indice<24):
        number[ax_indice] =  cont 
        ax_indice  =  ax_indice  + 1 
        cont = cont + 1
        controle = cont
    if (controle<24):
        cont = 0
        while (cont<indice):
            number[cont] = controle
            controle = controle + 1
            cont = cont + 1
    if (indice == 1):
        number[0] = 24

# ------------------------------------------------------ #
# essa função reorganiza o vetor de asteriscos para mostra-la na janela
# @param indice - valor para realocar o vetor
# @autor Antonio
def ajusta_vetor_stars (indice):
    global stars
    controle  = 0 
    cont = 1
    ax_indice = indice
    while (ax_indice<72):
        stars[ax_indice] =  cont 
        ax_indice  =  ax_indice  + 1 
        cont = cont + 1
        controle = cont
    if (controle<72):
        cont = 0
        while (cont<indice):
            stars[cont] = controle
            controle = controle + 1
            cont = cont + 1
    if (indice == 1):
        stars[0] = 72
# ------------------------------------------------------ #
# esse bloco constri e movimenta os ponteiros
in_radian = math.radians(in_degree_s) 
x2=x+rs*math.sin(in_radian)
y2=y-rs*math.cos(in_radian)
second=c1.create_line(x,y,x2,y2,fill='white',width=2)

def my_second():
    global in_degree_s,second
    in_radian = math.radians(in_degree_s)
    c1.delete(second)
    x2=x+rs*math.sin(in_radian) 
    y2=y-rs*math.cos(in_radian) 
    second=c1.create_line(x,y,x2,y2,arrow='last',fill='white',width=2)
    if(in_degree_s>=360): 
        in_degree_s=0
        my_minute()  
    in_degree_s=in_degree_s+6
    c1.after(1000,my_second) 

in_radian = math.radians(in_degree_m)
x2=x+rm*math.sin(in_radian)
y2=y-rm*math.cos(in_radian) 
minute=c1.create_line(x,y,x2,y2,width=2,fill='green', arrow='last')

def my_minute():
    global in_degree_m,minute
    in_degree_m=in_degree_m+6 
    in_radian = math.radians(in_degree_m) 
    c1.delete(minute) 
    x2=x+rm*math.sin(in_radian) 
    y2=y-rm*math.cos(in_radian)
    minute=c1.create_line(x,y,x2,y2,width=2,fill='green', arrow='last')
    my_hour() 
    if(in_degree_m>=360): 
        in_degree_m=0

in_degree_h=in_degree_h+(in_degree_m*0.0833333)          
in_radian = math.radians(in_degree_h)
x2=x+rh*math.sin(in_radian)
y2=y-rh*math.cos(in_radian)
hour=c1.create_line(x,y,x2,y2,width=2,fill='#a83e32', arrow='last')

def my_hour():
    global in_degree_h,hour
    in_degree_h=in_degree_h+0.5 
    in_radian = math.radians(in_degree_h) 
    c1.delete(hour)
    x2=x+rh*math.sin(in_radian)
    y2=y-rh*math.cos(in_radian) 
    hour=c1.create_line(x,y,x2,y2,width=2,fill='#a83e32', arrow='last')
    my_GMT()
    if(in_degree_h>=360):
        in_degree_h=0

in_degree_GMT=in_degree_GMT+(in_degree_m*0.0833333)          
in_radian = math.radians(in_degree_GMT)
x2=x+rgmt*math.sin(in_radian)
y2=y-rgmt*math.cos(in_radian)
Mgmt =c1.create_line(x,y,x2,y2,width=2,fill='red', arrow='last')

def my_GMT():
    global in_degree_GMT,Mgmt
    in_degree_GMT=in_degree_GMT+0.5 
    in_radian = math.radians(in_degree_GMT) 
    c1.delete(Mgmt)
    x2=x+rgmt*math.sin(in_radian)
    y2=y-rgmt*math.cos(in_radian) 
    Mgmt=c1.create_line(x,y,x2,y2,width=2,fill='Red', arrow='last')
    if(in_degree_GMT>=360):
        in_degree_GMT=0
# ------------------------------------------------------ #
my_second()
root.mainloop()






