from fpdf import FPDF
import pandas as pd
from datetime import datetime

class ListaPDF(FPDF):
    def header(self):
        # Cabeçalho elegante
        self.set_font('Arial', 'B', 20)
        self.set_text_color(44, 62, 80)  # Azul escuro elegante
        self.cell(0, 20, 'Lista de Compras', 0, 1, 'C')
        
        # Data atual
        self.set_font('Arial', '', 10)
        self.set_text_color(128, 128, 128)  # Cinza
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.cell(0, 10, f'Gerado em: {data_atual}', 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def gerar_pdf(itens_selecionados, pdf_path='lista_compras.pdf'):
    df = pd.read_csv('compras.csv')
    pdf = ListaPDF()
    pdf.add_page()
    
    # Cores para alternar linhas
    cor_clara = (245, 247, 250)  # Cinza bem claro
    cor_header = (52, 73, 94)    # Azul escuro elegante
    
    # Cabeçalho da tabela
    pdf.set_fill_color(*cor_header)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font('Arial', 'B', 11)
    pdf.cell(70, 10, 'Item', 1, 0, 'C', True)
    pdf.cell(25, 10, 'Qtd', 1, 0, 'C', True)
    pdf.cell(25, 10, 'Unidade', 1, 0, 'C', True)
    pdf.cell(70, 10, 'Categoria', 1, 1, 'C', True)

    # Conteúdo agrupado por categoria
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', '', 10)
    linha_colorida = False

    categorias = {}
    
    # Organizar itens por categoria
    for item in itens_selecionados:
        try:
            if 'nome' in item:  # Item personalizado
                categoria = 'Outros'
                nome = item['nome']
                quantidade = item['quantidade']
                unidade = item.get('unidade', 'un')
            else:  # Item do CSV
                index = item['index']
                row = df.iloc[index]
                categoria = row['Categoria']
                nome = row['Item']
                quantidade = item['quantidade']
                unidade = row['Unidade']
            
            if categoria not in categorias:
                categorias[categoria] = []
            categorias[categoria].append((nome, quantidade, unidade))
        except Exception as e:
            print(f"Erro ao processar item: {str(e)}")

    # Imprimir itens organizados por categoria
    for categoria in sorted(categorias.keys()):
        # Título da categoria
        pdf.set_font('Arial', 'B', 12)
        pdf.set_text_color(52, 73, 94)
        pdf.ln(5)
        pdf.cell(0, 10, categoria, 0, 1, 'L')
        pdf.set_font('Arial', '', 10)
        
        for nome, quantidade, unidade in sorted(categorias[categoria]):
            # Alternar cores das linhas
            if linha_colorida:
                pdf.set_fill_color(*cor_clara)
            else:
                pdf.set_fill_color(255, 255, 255)
            
            pdf.set_text_color(0, 0, 0)
            pdf.cell(70, 8, str(nome), 1, 0, 'L', True)
            pdf.cell(25, 8, str(quantidade), 1, 0, 'C', True)
            pdf.cell(25, 8, str(unidade), 1, 0, 'C', True)
            pdf.cell(70, 8, str(categoria), 1, 1, 'L', True)
            
            linha_colorida = not linha_colorida

    pdf.output(pdf_path)
    return pdf_path