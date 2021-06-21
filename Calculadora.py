import PySimpleGUI as sg

#Design dos Botões da Calculadora
btNum: dict = {'size':(7,2), 'font':('Franklin Gothic Book',24), 'button_color':("black","#DDA0DD")}
btSimbolo: dict = {'size':(7,2), 'font':('Franklin Gothic Book',24), 'button_color':("black","#BA55D3")}
btIgual: dict = {'size':(15,2), 'font':('Franklin Gothic Book',24), 'button_color':("black","#30042E"), 'focus':(True)}

#Layout
layout: list = [
    #Input dos Valores
    [sg.Text('0.0000', size=(19,1), justification='right', background_color='black', text_color='white', 
        font=('Digital-7',48), relief='sunken', key="_DISPLAY_")],
    #Botões de Numeros, Operações, Limpeza de Valores e Resultado
    [sg.Button('C',**btSimbolo), sg.Button('CE',**btSimbolo), sg.Button('%',**btSimbolo), sg.Button("/",**btSimbolo)],
    [sg.Button('7',**btNum), sg.Button('8',**btNum), sg.Button('9',**btNum), sg.Button("*",**btSimbolo)],
    [sg.Button('4',**btNum), sg.Button('5',**btNum), sg.Button('6',**btNum), sg.Button("-",**btSimbolo)],
    [sg.Button('1',**btNum), sg.Button('2',**btNum), sg.Button('3',**btNum), sg.Button("+",**btSimbolo)],    
    [sg.Button('0',**btNum), sg.Button('.',**btNum), sg.Button('=',**btIgual, bind_return_key=True)]
]

#Parametros da Janela
window: object = sg.Window('Calculadora Python', layout=layout, background_color="#272533", size=(580, 610), return_keyboard_events=True)

#Parametros à Serem Recebidos
valor: dict = {'inteiro':[], 'decimal':[], 'pontoFlutuante':False, 'Num1':0.0, 'Num2':0.0, 'resultado':0.0, 'operador':''}

'-------------------------------------------Funções-------------------------------------------'

#Formatação para Ponto Flutuante
def formatar() -> float:
    return float(''.join(valor['inteiro']).replace(',','') + '.' + ''.join(valor['decimal']))

#Atualiza a Tela Conforme os Clicks
def atualizar(display_value: str):
    try:
        window['_DISPLAY_'].update(value='{:,.4f}'.format(display_value))
    except:
        window['_DISPLAY_'].update(value=display_value)

#Evento do Clique do Botão de Numero
def entrarNumero(event: str):
    global valor
    if valor['pontoFlutuante']:
        valor['decimal'].append(event)
    else:
        valor['inteiro'].append(event)
    atualizar(formatar())

#Limpar Valores (CE ou C ou ESC)
def limpar():
    global valor
    valor['inteiro'].clear()
    valor['decimal'].clear()
    valor['pontoFlutuante'] = False

#Operadores (+ / - *)
def operador(event: str):
    global valor
    valor['operador'] = event
    try:
        valor['Num1'] = formatar()
    except:
        valor['Num1'] = valor['resultado']
    limpar()

#Calcular (=)
def calcular():
    global valor
    try:
        #Primeiro Formatar Valores
        valor['Num2'] = formatar()
    except ValueError: 
        #Exceção para quando o igual é pressionado sem entrada de valores
        valor['Num1'] = valor['resultado']
    try:
        #Primeiro Valor + Operação + Segundo Valor
        valor['resultado'] = eval(str(valor['Num1']) + valor['operador'] + str(valor['Num2']))
        atualizar(valor['resultado'])
        limpar()   
    except: 
        #Exceção para quando tentar dividir um valor por zero
        atualizar("ERRO! DIV/0")
        limpar()

'---------------------------Loops de Evento Principal e Chamadas das Funções---------------------------'

while True:
    #Construir a Tela e Sair da Tela
    event, values = window.read()
    print(event)
    if event is None:
        break
    #Chamar as Funções
    if event in ['0','1','2','3','4','5','6','7','8','9']:
        entrarNumero(event)
    if event in ['Escape:27','C','CE']:
        limpar()
        atualizar(0.00)
        valor['resultado'] = 0.0
    if event in ['+','-','*','/']:
        operador(event)
    if event == '=':
        calcular()
    if event == '.':
        valor['pontoFlutuante'] = True
    if event == '%': #Ler no Readme as Informações para os calculos de porcentagem
        atualizar(valor['resultado'] /100.0)
