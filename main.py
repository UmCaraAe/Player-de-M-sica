from tkinter import * 
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import pygame
import time
from mutagen.mp3 import MP3

janela = Tk()
janela.title("Player de Música")
janela.geometry("500x350")
janela.configure(background="#201b2c")
janela.resizable(width=False, height=False)
# janela.attributes("-alpha", 0.9)
janela.iconbitmap(default="C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/Login/img/favicon.ico")

#Inicia o mixer do pygame
pygame.mixer.init()

def duracao():
    #Pega o tempo de música atual e transforma em segundos
    duracao_atual = pygame.mixer.music.get_pos() / 1000
    
    # des_label.config(text=f'Slider: {int(controle_deslizante.get())} and Song Pos: {int(duracao_atual)}')
    
    conve_duracao_atual = time.strftime('%M:%S', time.gmtime(duracao_atual))
    
    musica_atual = playlist.curselection()
    
    #Pegando a próxima música da playlist
    musica = playlist.get(ACTIVE)
    
    #adicionando o diretorio e mp3 da música do titulo
    musica = f'C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/playlist/{musica}.mp3'
    #Faz a leitura da música atual e exibe o tempo decorrido na tela com a biblioteca mutagen.mp3
    musica_mut = MP3(musica)
    global tempo_musica
    tempo_musica = musica_mut.info.length
    #Converte para o formato de tempo
    conve_tempo_musica = time.strftime('%M:%S', time.gmtime(tempo_musica))
    
    
    #Soma mais 1 segundo
    duracao_atual +=1
    
    if int(controle_deslizante.get()) == int(tempo_musica):
        barra_de_status.config(text=f'Tempo decorrido: {conve_tempo_musica} de  {conve_tempo_musica} ')
    
    elif pausado:
        pass
    
    elif int(controle_deslizante.get()) == int(duracao_atual):
        #Atualizar a posição do slider
        posicao_deslizante = int(tempo_musica)
        controle_deslizante.config(to=posicao_deslizante, value=int(duracao_atual))
    else:
        #Caso o slider não se mova
        posicao_deslizante = int(tempo_musica)
        controle_deslizante.config(to=posicao_deslizante, value=int(controle_deslizante.get()))
        
        conve_duracao_atual = time.strftime('%M:%S', time.gmtime(int(controle_deslizante.get())))
        
        barra_de_status.config(text=f'Tempo decorrido: {conve_duracao_atual} de  {conve_tempo_musica} ') 

        prox_tempo = int(controle_deslizante.get()) + 1
        controle_deslizante.config(value=prox_tempo)
    
    barra_de_status.after(1000, duracao)
        
    #Mostra a duração da música na tela

def deslizar(x):
    # des_label.config(text=f'{int(controle_deslizante.get())} de {tempo_musica}')
    musica = playlist.get(ACTIVE)
    musica = f'C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/playlist/{musica}.mp3'
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(loops=0, start=int(controle_deslizante.get()))


#define a função para tocar a música
def play():
    musica = playlist.get(ACTIVE)
    musica = f'C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/playlist/{musica}.mp3'
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(loops=0)
    # tocar_btn.place(x=10000)
    # pausar_btn.grid(column=1)
    duracao()
    
    # des_label = int(tempo_musica)
    # controle_deslizante.config(to=des_label, value=0)

    #Pega o volume atual e mostra na tela
    volume_atual = pygame.mixer.music.get_volume()
    volume_atual = volume_atual * 100
    # des_label.config(text=volume_atual * 100)
    
    #Muda a imagem do volume
    if int(volume_atual) < 1:
        volume_meter.config(image=vol0)
    elif int(volume_atual) > 0 and int(volume_atual) <= 25:
        volume_meter.config(image=vol1)
    elif int(volume_atual) >= 25 and int(volume_atual) <= 50:
        volume_meter.config(image=vol2)
    elif int(volume_atual) >= 50 and int(volume_atual) <= 75:
        volume_meter.config(image=vol3)
    elif int(volume_atual) >=75 and int(volume_atual) <= 100:
        volume_meter.config(image=vol4)
global pausado
pausado = False

#define a função para pausar e despausar a música
def pause(esta_pausado):
    global pausado
    pausado = esta_pausado
    if pausado:
        pygame.mixer.music.unpause()
        pausado = False    
    else:
        pygame.mixer.music.pause()
        pausado = True

#Define a função de próxima música da playlist
def avancar_musica():
    barra_de_status.config(text='')
    controle_deslizante.config(value=0)
    
    prox_musica = playlist.curselection()
    prox_musica = prox_musica[0]+1
    #Pegando a próxima música da playlist
    musica = playlist.get(prox_musica)
    #adicionando o diretorio e mp3 da música do titulo
    musica = f'C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/playlist/{musica}.mp3'
    #Carregando e tocando a música
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(loops=0)
    
    #Removendo a barra de seleção da playlist
    playlist.selection_clear(0, END)
    
    #Ativando a barra de seleção da próxima música da playlist
    playlist.activate(prox_musica)
    playlist.selection_set(prox_musica, last=None)
    
def voltar_musica():
    #Faz com que ao voltar a música a barra de status e o slider voltem a posição inicial
    barra_de_status.config(text='')
    controle_deslizante.config(value=0)
    #Usa a mesma função da próxima música, mas no caso ao invés de avançar +1 música ela retrocede -1 música
    prox_musica = playlist.curselection()
    prox_musica = prox_musica[0]-1
    #Pegando a próxima música da playlist
    musica = playlist.get(prox_musica)
    #adicionando o diretorio e mp3 da música do titulo
    musica = f'C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/playlist/{musica}.mp3'
    #Carregando e tocando a música
    pygame.mixer.music.load(musica)
    pygame.mixer.music.play(loops=0)
    
    #Removendo a barra de seleção da playlist
    playlist.selection_clear(0, END)
    
    #Ativando a barra de seleção da próxima música da playlist
    playlist.activate(prox_musica)
    playlist.selection_set(prox_musica, last=None)
    
#Define a função de adicionar músicas
def add_musica():
    musica = filedialog.askopenfilename(initialdir='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/playlist/', title="Escolha uma Música", filetypes=(("mp3 Files", "*.mp3"), ))
    #Retira a informação do Diretorio e da extensão .mp3 da música
    musica = musica.replace("C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/playlist/", "")
    musica = musica.replace(".mp3", "")
    playlist.insert(END, musica)
    
#Define a função de adicionar várias músicas a playlist
def add_varias_musicas():
    musicas = filedialog.askopenfilenames(initialdir='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/playlist/', title="Escolha uma Música", filetypes=(("mp3 Files", "*.mp3"), ))
    
    for musica in musicas:
        musica = musica.replace("C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/playlist/", "")
        musica = musica.replace(".mp3", "")
        playlist.insert(END, musica)

#Define a função de remover a música selecionada 
def remover_musica():
    #Remove a música selecionada
    playlist.delete(ANCHOR)
    pygame.mixer.music.stop()

#Define a função de remover todas as músicas da playlist   
def remover_todas():
    #Remove todas as músicas 
    playlist.delete(0, END)
    pygame.mixer.music.stop()

#Define a função do volume
def volume(x):
    pygame.mixer.music.set_volume(volume_deslize.get())
    #Pega o volume atual e mostra na tela
    volume_atual = pygame.mixer.music.get_volume()
    volume_atual = volume_atual * 100
    # des_label.config(text=volume_atual * 100)
    
    #Muda a imagem do volume
    if int(volume_atual) < 1:
        volume_meter.config(image=vol0)
    elif int(volume_atual) > 0 and int(volume_atual) <= 25:
        volume_meter.config(image=vol1)
    elif int(volume_atual) >= 25 and int(volume_atual) <= 50:
        volume_meter.config(image=vol2)
    elif int(volume_atual) >= 50 and int(volume_atual) <= 75:
        volume_meter.config(image=vol3)
    elif int(volume_atual) >=75 and int(volume_atual) <= 100:
        volume_meter.config(image=vol4)

#Criando uma Master Frame
master_frame = Frame(janela, background="#201b2c")
master_frame.pack()

playlist = Listbox(master_frame, bg="#3b3154", fg="#00ff88", width=60, selectbackground="#201b2c", selectforeground="#00ff88")
playlist.grid(row=0, column=0)

#Imagens dos Botões de Controle
voltar = PhotoImage(file='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/img/anterior.png')
avancar = PhotoImage(file='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/img/proximo.png')
tocar = PhotoImage(file='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/img/play.png')
pausar = PhotoImage(file='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/img/pause.png')
add_musica_img = PhotoImage(file='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/img/add.png')

#Imagens de Controle de Volume
global vol0
global vol1
global vol2
global vol3
global vol4
vol0 = PhotoImage(file='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/img/volume-mudo.png')
vol1 = PhotoImage(file='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/img/volume.png')
vol2 = PhotoImage(file='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/img/volume-baixo.png')
vol3 = PhotoImage(file='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/img/volume-medio.png')
vol4 = PhotoImage(file='C:/Users/Erick/Desktop/Meu Portifolio/assets/projetos/player de musica/img/volume-alto.png')

#Medidor de Volume
volume_meter = Label(master_frame, image=vol0, background='#201b2c')
volume_meter.grid(row=1, column=1, padx=10)

#Área de Controle
FrameControle = Frame(master_frame, bg="#201b2c")
FrameControle.grid(row=2, column=0, pady=20)

#Criando uma Label Frame de Volume
volume_frame = LabelFrame(master_frame, text="Volume", background="#201b2c", foreground="#00ff88", )
volume_frame.grid(row=0, column=1)

#Botões de Controle
voltar_btn = Button(FrameControle, image=voltar,borderwidth=0, bg="#201b2c", command=voltar_musica)
avancar_btn = Button(FrameControle, image=avancar,borderwidth=0, bg="#201b2c", command=avancar_musica)
tocar_btn = Button(FrameControle, image=tocar,borderwidth=0, bg="#201b2c", command=play)
pausar_btn = Button(FrameControle, image=pausar,borderwidth=0, bg="#201b2c", command=lambda: pause(pausado))

voltar_btn.grid(row=0, column=0, padx=10)
avancar_btn.grid(row=0, column=2, padx=10)
tocar_btn.grid(row=0, column=1, padx=10)
pausar_btn.grid(row=0, column=3, padx=10)

#Criando o Menu de Músicas
menu_TocaRaul = Menu(janela, bg="#201b2c")
janela.config(menu=menu_TocaRaul, bg="#201b2c")

#Adicionar Música
add_musica_menu = Menu(menu_TocaRaul, bg="#201b2c", background="#201b2c", foreground="#00ff88")
menu_TocaRaul.add_cascade(label="Adicionar Músicas", menu=add_musica_menu, background="#201b2c", foreground="#00ff88")
add_musica_menu.add_command(label="Adicione Uma Música a PlayList", command=add_musica, background="#201b2c", foreground="#00ff88")

#Adicionar várias músicas de uma vez
add_musica_menu.add_command(label="Adicione Várias Músicas a PlayList", command=add_varias_musicas, background="#201b2c", foreground="#00ff88")

#Deletar música da playlist
remove_musica_menu = Menu(menu_TocaRaul, background="#201b2c", foreground="#00ff88")
menu_TocaRaul.add_cascade(label="Remover Música", menu=remove_musica_menu, background='#201b2c', foreground='#00ff88')
remove_musica_menu.add_command(label="Remova uma Música da PlayList", background='#201b2c', foreground='#00ff88', command=remover_musica)
remove_musica_menu.add_command(label="Remova Todas as Músicas da PlayList", background='#201b2c', foreground='#00ff88', command=remover_todas)

#Criando barra de duração atual da música
barra_de_status =Label(janela, text='', bd=1, relief=GROOVE, anchor=E, background="#201b2c", foreground="#00ff88")
barra_de_status.pack(fill=X, side=BOTTOM, ipady=2)

#Criando um slider de posição do tempo da música
controle_deslizante = ttk.Scale(master_frame, from_=0, to=100, orient=HORIZONTAL, value=0, command=deslizar, length=360)
controle_deslizante.grid(row=1, column=0, pady=10)

#Criando um slider para controlar o volume
volume_deslize = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, command=volume, length=125)
volume_deslize.pack()

des_label = Label(janela, text='0', background="#201b2c", foreground="#00FF88")
des_label.pack(pady=10)

janela.mainloop()