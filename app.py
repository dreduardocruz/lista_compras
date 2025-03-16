from flask import Flask, render_template, request, jsonify, send_file
from lista_pdf import gerar_pdf
import pandas as pd
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
    # Ordena o DataFrame por nome por padrão
    df = df.sort_values('Item')
    categorias = sorted(df['Categoria'].unique())
    items = df.to_dict('records')
    return render_template('index.html', items=items, categorias=categorias)

@app.route('/gerar-lista', methods=['POST'])
def gerar_lista():
    try:
        itens_selecionados = request.json
        print(f"Dados recebidos: {itens_selecionados}")
        
        if not itens_selecionados:
            return jsonify({"error": "Nenhum item selecionado"}), 400
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_name = f'lista_compras_{timestamp}.pdf'
        pdf_path = os.path.join(BASE_DIR, pdf_name)
        
        global PDF_PATH
        PDF_PATH = pdf_path
        
        gerar_pdf(itens_selecionados, pdf_path)
        return jsonify({
            "message": "PDF gerado com sucesso!",
            "path": pdf_path
        })
    except Exception as e:
        print(f"Erro na geração do PDF: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Nova rota para download do PDF
@app.route('/download-pdf')
def download_pdf():
    try:
        return send_file(PDF_PATH, as_attachment=True)
    except Exception as e:
        return jsonify({"error": "PDF não encontrado"}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)