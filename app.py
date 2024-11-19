import flet as ft
import pandas as pd

# Inicialize as variáveis `caminho_arquivo` e `nome_arquivo_saida` com valores padrão
caminho_arquivo = ft.Text(value="")  # Inicialização com valor padrão vazio
nome_arquivo_saida = ft.Text(value="")  # Inicialização com valor padrão vazio
# Inicializa o campo de status com uma mensagem vazia
status = ft.Text(value="")


def planilha_assembleia(arquivo, nome_arquivo, page):
    try:
        # Lê o arquivo Excel
        dados_brutos = pd.read_excel(arquivo)

        # Verifica se a coluna 'CPF' existe
        if 'CPF' in dados_brutos.columns:
            # Cria a coluna 'LOGIN' preenchendo com zeros à esquerda para CPFs com menos de 11 dígitos
            dados_brutos['LOGIN'] = dados_brutos['CPF'].astype(
                str).str.zfill(11)

        # Verifica se a coluna 'DATAS DE NASCIMENTO' existe
        if 'DATAS DE NASCIMENTO' in dados_brutos.columns:
            # Cria a coluna 'SENHA' removendo as barras da coluna 'DATAS DE NASCIMENTO'
            dados_brutos['SENHA'] = dados_brutos['DATAS DE NASCIMENTO'].astype(
                str).str.replace('/', '', regex=False).str.zfill(8)

        if 'MATRICULA' in dados_brutos.columns:
            dados_brutos['MATRICULA 1'] = dados_brutos['MATRICULA'].astype(
                str).str[:4]

        # Mostra o DataFrame com as novas colunas
        print(dados_brutos.head(5))
        dados_brutos.to_csv(f'{nome_arquivo}.csv', sep=';', index=False)
        print('Planilha foi gerada.')

        # Exibe a mensagem de sucesso na interface gráfica
        status.value = f"Sucesso! Planilha '{nome_arquivo}.csv' foi gerada."
        status.color = "green"  # Cor verde para sucesso
        page.update()

    except Exception as e:
        # Exibe a mensagem de erro na interface gráfica
        status.value = f"Erro: {str(e)}"
        status.color = "red"  # Cor vermelha para erro
        page.update()


def main(page: ft.Page):
    # Definir um tamanho fixo para a página
    page.window_width = 500
    page.window_height = 350
    page.padding = 20

    # Função para selecionar um arquivo
    def selecionar_arquivo(e):
        if e.files and len(e.files) > 0:
            # Apenas define o valor se e.files não for None
            caminho_arquivo.value = e.files[0].path
            page.update()

    # Função a ser executada ao clicar no botão de processar
    def processar_click(e):
        # Verifique se as variáveis não são None antes de acessar seus atributos
        if caminho_arquivo.value and nome_arquivo_saida.value:
            # Chama a função que processa o arquivo
            planilha_assembleia(caminho_arquivo.value,
                                nome_arquivo_saida.value, page)
        else:
            status.value = "Por favor, selecione um arquivo e insira um nome de saída."
            status.color = "orange"  # Cor laranja para orientação
            page.update()

    # Adiciona o seletor de arquivo
    file_picker = ft.FilePicker(on_result=selecionar_arquivo)
    page.overlay.append(file_picker)

    # Cria o campo de texto para inserir o nome do arquivo de saída
    campo_nome_arquivo_saida = ft.TextField(
        label="Nome do Arquivo de Saída",
        on_change=lambda e: setattr(
            nome_arquivo_saida, 'value', e.control.value or "")
    )

    # Botão para abrir o seletor de arquivo
    botao_selecionar = ft.ElevatedButton(
        text="Selecionar Arquivo",
        on_click=lambda e: file_picker.pick_files()
    )

    # Botão para processar
    botao_processar = ft.ElevatedButton(
        text="Processar",
        on_click=processar_click
    )

    # Adiciona os controles na página
    page.add(
        botao_selecionar,
        campo_nome_arquivo_saida,
        botao_processar,
        status  # Exibe a mensagem de status (sucesso ou erro)
    )


# Execute a aplicação
ft.app(target=main)
