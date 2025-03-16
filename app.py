from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from fpdf import FPDF
import os
from datetime import datetime

app = Flask(__name__)

# Configurar caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'compras.csv')
PDF_PATH = os.path.join(BASE_DIR, 'lista_compras.pdf')

@app.route('/')
def index():
    df = pd.read_csv(CSV_PATH)
    # Ordena o DataFrame por categoria e item e reseta o índice
    df = df.sort_values(['Categoria', 'Item']).reset_index(drop=True)
    categorias = sorted(df['Categoria'].unique())
    items = df.to_dict('records')
    return render_template('index.html', items=items, categorias=categorias)

@app.route('/gerar-lista', methods=['POST'])
def gerar_lista():
    try:
        dados_recebidos = request.json
        print(f"Dados recebidos: {dados_recebidos}")  # Debug
        
        # Lê o CSV e ordena da mesma forma que na rota index
        df = pd.read_csv(CSV_PATH)
        df = df.sort_values(['Categoria', 'Item']).reset_index(drop=True)
        
        itens_selecionados = []
        for item in dados_recebidos:
            idx = int(item['index'])
            print(f"Processando índice: {idx}")  # Debug
            if 0 <= idx < len(df):
                item_atual = df.iloc[idx]
                print(f"Item encontrado: {item_atual['Item']}")  # Debug
                
                item_dict = {
                    'Item': str(item_atual['Item']),
                    'Categoria': str(item_atual['Categoria']),
                    'Quantidade': int(item['quantidade']),
                    'Unidade': str(item_atual['Unidade'])
                }
                itens_selecionados.append(item_dict)
        
        if not itens_selecionados:
            return jsonify({"error": "Nenhum item selecionado"}), 400
            
        # Gera PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Lista de Compras', 0, 1, 'C')
        pdf.ln(10)
        
        # Agrupa itens por categoria
        df_itens = pd.DataFrame(itens_selecionados)
        categorias = df_itens['Categoria'].unique()
        
        for categoria in sorted(categorias):
            itens_categoria = df_itens[df_itens['Categoria'] == categoria]
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, f'{categoria}:', 0, 1)
            pdf.set_font('Arial', '', 12)
            
            for _, item in itens_categoria.iterrows():
                texto = f"- {item['Item']}: {item['Quantidade']} {item['Unidade']}"
                pdf.cell(0, 8, texto, 0, 1)
            pdf.ln(5)
        
        # Salva o PDF
        pdf_name = f'lista_compras_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        pdf_path = os.path.join(BASE_DIR, pdf_name)
        pdf.output(pdf_path)
        
        return jsonify({"message": "PDF gerado com sucesso!", "path": pdf_name})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download-pdf/<path:filename>')
def download_pdf(filename):
    try:
        return send_file(
            os.path.join(BASE_DIR, filename),
            as_attachment=True
        )
    except Exception as e:
        return str(e), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)