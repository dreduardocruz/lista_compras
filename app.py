from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
from fpdf import FPDF
import os
import tempfile
from datetime import datetime

app = Flask(__name__)

# Configurar caminhos absolutos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, 'compras.csv')
PDF_PATH = os.path.join(BASE_DIR, 'lista_compras.pdf')

# Load items from CSV
# Fix the load_items function to use CSV_PATH
def load_items():
    df = pd.read_csv(CSV_PATH)
    return df.sort_values(['Categoria', 'Item']).reset_index(drop=True).to_dict('records')

@app.route('/')
def index():
    items = load_items()
    categorias = sorted(set(item['Categoria'] for item in items))
    return render_template('index.html', items=items, categorias=categorias)

@app.route('/gerar-lista', methods=['POST'])
def gerar_lista():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400

        items = load_items()

        class PDF(FPDF):
            def __init__(self):
                super().__init__()
                # Define colors for each category
                self.category_colors = {
                    'Hortifruti': (230, 255, 230),  # Light green
                    'Carnes': (255, 230, 230),      # Light red
                    'Laticínios': (255, 255, 230),  # Light yellow
                    'Mercearia': (255, 240, 220),   # Light orange
                    'Padaria': (255, 235, 205),     # Light brown
                    'Bebidas': (230, 230, 255),     # Light blue
                    'Limpeza': (240, 255, 255),     # Light cyan
                    'Higiene': (255, 230, 255)      # Light purple
                }

        pdf = PDF()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, 'Lista de Compras', 0, 1, 'C')
        
        current_category = None
        for item in sorted(data, key=lambda x: items[int(x['index'])]['Categoria']):
            index = int(item['index'])
            quantidade = item['quantidade']
            item_info = items[index]
            
            if current_category != item_info['Categoria']:
                current_category = item_info['Categoria']
                pdf.set_font('Arial', 'B', 14)
                pdf.ln(5)
                # Set background color for category
                pdf.set_fill_color(*pdf.category_colors.get(current_category, (255, 255, 255)))
                pdf.cell(0, 10, current_category, 0, 1, 'L', True)
                pdf.set_font('Arial', '', 12)
            
            pdf.cell(0, 10, f"- {item_info['Item']}: {quantidade} {item_info['Unidade']}", 0, 1)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_pdf:
            pdf.output(temp_pdf.name, 'F')
            return send_file(
                temp_pdf.name,
                as_attachment=True,
                download_name=f'lista_compras_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf',
                mimetype='application/pdf'
            )

    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
    app.run(debug=True, host='0.0.0.0', port=8080)