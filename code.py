import qrcode
import os
from rich.console import Console

console = Console()

class PredefinedColors():
    VERMELHO = (255, 0, 0)
    VERDE = (0, 255, 0)
    AZUL = (0, 0, 255)
    PRETO = (0, 0, 0)
    BRANCO = (255, 255, 255)
    AMARELO = (255, 255, 0)
    ROXO = (102, 30, 102)
    
# inclusão dos dados    
def inclusion(data_list):
    for inclus in range(1, 10):
        while True:
            data = console.input(f'Digite o Conteudo {inclus} (ou digite [bold bright_cyan]"F"[/bold bright_cyan] para finalizar): ')
            if data == ' ':
            	console.print("Erro, por favor insira algo válido.", style="Bold red")
            else:
                break
        if data.lower() == 'f':
            break
        data_list.append(data)
        total = 9 - inclus
        if inclus != 9:
        	console.print(f'Você tem mais {total}', style="italic black on white")

# confere o valor no formato rgb
def Check_value_input_rgb(color):
    try:
        color_list = color.split(',')
        if len(color_list) != 3:
            return False
        for component in color_list:
            if not (0 <= int(component) <= 255):
                return False
        return True
    except ValueError:
        return False

# gerador do qrcode
def generate_qr():
    data_list = []
    inclusion(data_list)
    
    address = input('Caminho para Salvar: ')
    name = input('Nome do Arquivo: ')
    extension = '.' + input("tipo de arquivo: ")

    address = address.replace('\\', '/')
    if not address.endswith('/'):
        address += '/'

    all_data = '\n'.join(data_list)

    full_address = address + name + extension

    color_method = console.input('Escolha o método de seleção de cor ([magenta][1]RGB[/magenta] ou [yellow][2]Predefinido)[/yellow]: ')
    while color_method not in ['1', '2']:
        color_method = console.input('Escolha o método de seleção de cor ([magenta][1]RGB[/magenta] ou [yellow][2]Predefinido)[/yellow]: ')

    if color_method == '1':
        while True:
            fill_color = input('Cor de preenchimento [blue](ex: 255, 0, 0)[/blue]: ')
            if Check_value_input_rgb(fill_color):
                fill_color = tuple(map(int, fill_color.split(',')))
                break
            else:
                print("Formato de cor inválido. Por favor, insira no formato correto.")

        while True:
            back_color = input('Cor de fundo RGB [blue](ex: 0, 0, 0)[/blue]: ')
            if Check_value_input_rgb(back_color):
                back_color = tuple(map(int, back_color.split(',')))
                break
            else:
                console.print("Formato de cor inválido. Por favor, insira no formato correto.", style="bold red")

    elif color_method == '2':
        print("Cores predefinidas disponíveis:")
        console.print("1 - [bright_red]Vermelho[/bright_red]")
        console.print("2 - [bright_green]Verde[/bright_green]")
        console.print("3 - [bright_blue]Azul[/bright_blue]")
        console.print("4 - [black on white]Preto[/black on white]")
        console.print("5 - [white on black]Branco[/white on black]")
        console.print("6 - [bright_yellow]Amarelo[/bright_yellow]")
        console.print("7 - [bright_magenta]Roxo[/bright_magenta]")

        print('Selecione uma das cores acima')
        fill_color_choice = input('Escolha a cor de preenchimento: ')
        back_color_choice = input('Escolha a cor do fundo: ')

        predefined_colors = {
            '1': PredefinedColors.VERMELHO,
            '2': PredefinedColors.VERDE,
            '3': PredefinedColors.AZUL,
            '4': PredefinedColors.PRETO,
            '5': PredefinedColors.BRANCO,
            '6': PredefinedColors.AMARELO,
            '7': PredefinedColors.ROXO
        }

        if fill_color_choice in predefined_colors:
            fill_color = predefined_colors[fill_color_choice]
        else:
            console.print('Opção inválida para cor de preenchimento. Usando cor padrão.', style="bold red")
            fill_color = (0, 0, 0)

        if back_color_choice in predefined_colors:
            back_color = predefined_colors[back_color_choice]
        else:
            console.print('Opção inválida para cor de fundo. Usando cor padrão.', style="bold red")
            back_color = (255, 255, 255)

    qr = qrcode.QRCode(version=1, 
                       box_size=10, 
                       border=5,
                       error_correction=qrcode.constants.ERROR_CORRECT_L)

    qr.add_data(all_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color= fill_color, back_color= back_color)

    img.save(full_address)

    console.print(f'QrCode gerado no caminho {address}', style="rgb(252,186,3)")
    return address

# chamada para abrir o explorer
def explorer(address):
    open_dir = console.input('Deseja abrir o local do arquivo [bold green][s][/bold green] ou [bold red][n][/bold red]? ')
    if open_dir.lower() == 's':
        os.startfile(address)

while True:
    address = generate_qr()
    explorer(str(address))

    repeat = input('Deseja gerar outro QrCode? [s] ou [n]: ')
    if repeat.lower() != 's':
        break
    console.clear() # limpa o terminal para uma nova geração
