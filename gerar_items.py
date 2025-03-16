import pandas as pd

# Dicionário com categorias e seus respectivos itens
items_por_categoria = {
    'Hortifruti': [
        ('Abacate', 'un'), ('Abacaxi', 'un'), ('Abóbora', 'kg'), ('Abobrinha', 'kg'),
        ('Acelga', 'un'), ('Agrião', 'maço'), ('Alface', 'un'), ('Alho', 'kg'),
        ('Banana Prata', 'kg'), ('Banana Nanica', 'kg'), ('Batata Doce', 'kg'),
        ('Berinjela', 'kg'), ('Beterraba', 'kg'), ('Brócolis', 'un'), ('Cebola', 'kg'),
        ('Cenoura', 'kg'), ('Chuchu', 'kg'), ('Couve', 'maço'), ('Espinafre', 'maço'),
        ('Gengibre', 'kg'), ('Inhame', 'kg'), ('Laranja', 'kg'), ('Limão', 'kg'),
        ('Maçã', 'kg'), ('Mamão', 'un'), ('Manga', 'kg'), ('Melancia', 'kg'),
        ('Morango', 'cx'), ('Pepino', 'kg'), ('Pêra', 'kg'), ('Pimentão', 'kg'),
        ('Repolho', 'un'), ('Rúcula', 'maço'), ('Tomate', 'kg'), ('Uva', 'kg'),
        # Novos itens Hortifruti
        ('Kiwi', 'kg'), ('Goiaba', 'kg'), ('Jabuticaba', 'kg'), ('Ameixa', 'kg'),
        ('Rabanete', 'maço'), ('Nabo', 'kg'), ('Vagem', 'kg'), ('Quiabo', 'kg'),
        ('Couve-Flor', 'un'), ('Alface Roxa', 'un'), ('Alface Americana', 'un'),
        ('Batata Inglesa', 'kg'), ('Aipim', 'kg'), ('Jiló', 'kg'), ('Maxixe', 'kg')
    ],
    'Carnes': [
        ('Alcatra', 'kg'), ('Bacon', 'kg'), ('Carne Moída', 'kg'), ('Costela Bovina', 'kg'),
        ('Coxa de Frango', 'kg'), ('Filé de Frango', 'kg'), ('Filé Mignon', 'kg'),
        ('Linguiça', 'kg'), ('Lombo Suíno', 'kg'), ('Patinho', 'kg'), ('Peito de Frango', 'kg'),
        ('Picanha', 'kg'), ('Presunto', 'kg'), ('Salsicha', 'kg'), ('Sardinha', 'kg'),
        # Novos itens Carnes
        ('Contra Filé', 'kg'), ('Cupim', 'kg'), ('Lagarto', 'kg'), ('Maminha', 'kg'),
        ('Músculo', 'kg'), ('Acém', 'kg'), ('Costela Suína', 'kg'), ('Pernil', 'kg'),
        ('Mortadela', 'kg'), ('Salame', 'kg'), ('Peito de Peru', 'kg'), ('Asa de Frango', 'kg')
    ],
    'Laticínios': [
        ('Iogurte Natural', 'un'), ('Leite Integral', 'L'), ('Leite Desnatado', 'L'),
        ('Manteiga', 'kg'), ('Margarina', 'kg'), ('Mussarela', 'kg'), ('Queijo Minas', 'kg'),
        ('Queijo Prato', 'kg'), ('Requeijão', 'un'), ('Cream Cheese', 'un'),
        ('Leite Condensado', 'un'), ('Creme de Leite', 'un'), ('Leite em Pó', 'kg'),
        # Novos itens Laticínios
        ('Iogurte Grego', 'un'), ('Leite Semi-Desnatado', 'L'), ('Queijo Provolone', 'kg'),
        ('Queijo Gorgonzola', 'kg'), ('Ricota', 'kg'), ('Cottage', 'un'), ('Nata', 'un'),
        ('Leite Fermentado', 'un'), ('Bebida Láctea', 'L'), ('Queijo Ralado', 'kg')
    ],
    'Mercearia': [
        ('Arroz', 'kg'), ('Feijão Preto', 'kg'), ('Feijão Carioca', 'kg'),
        ('Macarrão', 'kg'), ('Farinha de Trigo', 'kg'), ('Açúcar', 'kg'),
        ('Café', 'kg'), ('Sal', 'kg'), ('Óleo de Soja', 'un'), ('Azeite', 'un'),
        ('Vinagre', 'un'), ('Molho de Tomate', 'un'), ('Extrato de Tomate', 'un'),
        ('Milho em Conserva', 'un'), ('Ervilha em Conserva', 'un'), ('Atum', 'un'),
        ('Sardinha em Lata', 'un'), ('Temperos Diversos', 'un'), ('Maionese', 'un'),
        ('Mostarda', 'un'), ('Ketchup', 'un'),
        # Novos itens Mercearia
        ('Granola', 'kg'), ('Aveia', 'kg'), ('Farinha de Mandioca', 'kg'),
        ('Farinha de Milho', 'kg'), ('Amendoim', 'kg'), ('Castanha de Caju', 'kg'),
        ('Mel', 'un'), ('Geléia', 'un'), ('Achocolatado', 'kg'), ('Cereais', 'un')
    ],
    'Padaria': [
        ('Pão Francês', 'kg'), ('Pão de Forma', 'un'), ('Pão Integral', 'un'),
        ('Bolo', 'un'), ('Biscoito Água e Sal', 'un'), ('Biscoito Recheado', 'un'),
        ('Torrada', 'un'), ('Pão de Queijo', 'kg'), ('Croissant', 'un'),
        # Novos itens Padaria
        ('Pão Australiano', 'un'), ('Pão Sírio', 'un'), ('Sonho', 'un'),
        ('Rosca Doce', 'un'), ('Brioche', 'un'), ('Baguete', 'un'),
        ('Pão de Hambúrguer', 'pc'), ('Pão de Hot Dog', 'pc'), ('Bolo de Chocolate', 'un')
    ],
    'Bebidas': [
        ('Água Mineral', 'un'), ('Refrigerante Cola', 'L'), ('Refrigerante Guaraná', 'L'),
        ('Suco de Laranja', 'L'), ('Suco de Uva', 'L'), ('Cerveja', 'un'),
        ('Vinho Tinto', 'un'), ('Água de Coco', 'L'), ('Chá Mate', 'L'),
        # Novos itens Bebidas
        ('Energético', 'un'), ('Tônica', 'L'), ('Suco de Maracujá', 'L'),
        ('Suco de Pêssego', 'L'), ('Vinho Branco', 'un'), ('Vodka', 'un'),
        ('Whisky', 'un'), ('Champagne', 'un'), ('Suco de Caju', 'L')
    ],
    'Limpeza': [
        ('Água Sanitária', 'L'), ('Detergente', 'un'), ('Sabão em Pó', 'kg'),
        ('Amaciante', 'L'), ('Desinfetante', 'L'), ('Papel Higiênico', 'pc'),
        ('Papel Toalha', 'pc'), ('Saco de Lixo', 'pc'), ('Esponja', 'un'),
        ('Lustra Móveis', 'un'), ('Limpa Vidros', 'un'), ('Sabão em Barra', 'un'),
        # Novos itens Limpeza
        ('Alvejante', 'L'), ('Multiuso', 'un'), ('Cera Líquida', 'L'),
        ('Sabão de Coco', 'un'), ('Limpa Alumínio', 'un'), ('Amaciante Concentrado', 'L'),
        ('Desengordurante', 'un'), ('Inseticida', 'un'), ('Luva de Borracha', 'par')
    ],
    'Higiene': [
        ('Sabonete', 'un'), ('Shampoo', 'un'), ('Condicionador', 'un'),
        ('Creme Dental', 'un'), ('Escova de Dentes', 'un'), ('Fio Dental', 'un'),
        ('Desodorante', 'un'), ('Absorvente', 'pc'), ('Lenço de Papel', 'pc'),
        ('Algodão', 'pc'), ('Cotonete', 'pc'), ('Álcool em Gel', 'un'),
        # Novos itens Higiene
        ('Creme de Barbear', 'un'), ('Aparelho de Barbear', 'un'), ('Protetor Solar', 'un'),
        ('Hidratante', 'un'), ('Xampu Anti-Caspa', 'un'), ('Condicionador Anti-Frizz', 'un'),
        ('Escova de Cabelo', 'un'), ('Pente', 'un'), ('Sabonete Líquido', 'un')
    ]
}

# Criar lista de itens
items = []
for categoria, produtos in items_por_categoria.items():
    for produto, unidade in produtos:
        items.append({
            'Categoria': categoria,
            'Item': produto,
            'Quantidade': 1,  # quantidade padrão
            'Unidade': unidade,
            'Comprado': False
        })

# Criar DataFrame e salvar CSV
df = pd.DataFrame(items)
df.to_csv('compras.csv', index=False)

print(f"Arquivo CSV gerado com {len(df)} itens!")