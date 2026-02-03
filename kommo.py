import pandas as pd
import json
import numpy as np
from decimal import Decimal

# Caminho do arquivo
caminho = r"C:\Users\Alisson\jurisgrouted\Planilha kommo.xlsx"

# Ler o Excel
df = pd.read_excel(caminho)

# Mapeamento direto de simplificação
mapeamento = {
    'ID': 'id',
    'Tipo': 'tipo',
    'Nome': 'nome',
    'Primeiro nome': 'primeiro_nome',
    'Sobrenome': 'sobrenome',
    'Empresa': 'empresa',
    'Data de criação': 'data_criacao',
    'Criado por': 'criado_por',
    'Modificado em': 'modificado_em',
    'Modificado por': 'modificado_por',
    'Tags': 'tags',
    'Próxima tarefa': 'proxima_tarefa',
    'Usuário responsável': 'usuario_responsavel',
    'Leads': 'leads',
    'Posição (contato)': 'posicao',
    'Email comercial': 'email_comercial',
    'Email pessoal': 'email_pessoal',
    'Outro email': 'outro_email',
    'Telefone comercial': 'telefone_comercial',
    'Tel. direto com.': 'telefone_direto',
    'Celular': 'celular',
    'Faz': 'faz',
    'Telefone residencial': 'telefone_residencial',
    'Outro telefone': 'outro_telefone',
    'Endereço (Empresa)': 'endereco_empresa',
    'Site (Empresa)': 'site_empresa',
    'Nota 1': 'nota_1',
    'Nota 2': 'nota_2',
    'Nota 3': 'nota_3',
    'Nota 4': 'nota_4',
    'Nota 5': 'nota_5'
}

# Renomear colunas
df = df.rename(columns=mapeamento)

# Função personalizada para converter DataFrame para lista de dicionários
def dataframe_para_json_safe(df):
    """
    Converte DataFrame para lista de dicionários, garantindo que NaN vire None
    """
    resultado = []
    
    for _, row in df.iterrows():
        registro = {}
        for col in df.columns:
            valor = row[col]
            
            # Converter NaN/NaT para None
            if pd.isna(valor):
                registro[col] = None
            # Converter outros tipos que podem causar problemas
            elif isinstance(valor, (np.integer, np.floating)):
                registro[col] = float(valor) if np.isreal(valor) else None
            elif isinstance(valor, pd.Timestamp):
                registro[col] = valor.isoformat()
            else:
                registro[col] = valor
        
        resultado.append(registro)
    
    return resultado

# Converter para lista de dicionários com tratamento seguro
resultado = dataframe_para_json_safe(df)

# Salvar em arquivo JSON
caminho_json = r"C:\Users\Alisson\jurisgrouted\dados_convertidos.json"
with open(caminho_json, 'w', encoding='utf-8') as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)

print(f"✅ Conversão concluída! {len(resultado)} registros convertidos.")
print(f"📁 Arquivo salvo em: {caminho_json}")

# Gerar exemplo do JSON
print("\n📋 Exemplo do JSON gerado (primeiro registro):")
if resultado:
    exemplo = json.dumps(resultado[0], ensure_ascii=False, indent=2)
    print(exemplo)

# Validar que não há NaN
print("\n🔍 Validando que não há NaN no resultado...")
tem_nan = False
for i, item in enumerate(resultado[:10]):  # Verificar apenas os 10 primeiros
    for key, value in item.items():
        if value is not None and isinstance(value, float) and np.isnan(value):
            print(f"  ❌ Ainda há NaN no registro {i}, campo '{key}': {value}")
            tem_nan = True

if not tem_nan:
    print("  ✅ Nenhum NaN encontrado nos primeiros 10 registros!")