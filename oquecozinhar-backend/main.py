from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import pandas as pd
import os

dados = pd.read_csv(r'Arquivo_final.csv')
colunas = ['tipo', 'preparo', 'rendimento']

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    pass


@app.route('/obter-receita', methods=['POST'])
@cross_origin()
def obter_receita():
    parametros = request.get_json()
    parametros_input = [parametros[col] for col in colunas]

    # Filtrando receitas com mais ou menos de 30 minutos
    if parametros_input[1] == 'rookie':
        amostra1 = dados.loc[dados['PREPARO'] <= 30]
    elif parametros_input[1] == 'master':
        amostra1 = dados.loc[dados['PREPARO'] > 30]
    else:
        amostra1 = dados.loc[:]

    # Filtrando receitas por porções servidas
    if parametros_input[2] == 1:
        amostra2 = amostra1.loc[amostra1['RENDIMENTO'] == parametros_input[2]]
    elif parametros_input[2] == 2:
        amostra2 = amostra1.loc[amostra1['RENDIMENTO'] == parametros_input[2]]
    else:
        amostra2 = amostra1.loc[amostra1['RENDIMENTO'] >= parametros_input[2]]

    # Filtrando receitas Vegetarianas ou não
    if parametros_input[0] == 1:
        amostra3 = amostra2.loc[amostra2['TIPO'] == 'Vegetariana']
        amostra = amostra3.sample()
    else:
        amostra = amostra2.sample()

    link = str(amostra['LINK'].values[0])
    nome = str(amostra['RECEITA'].values[0])
    rendimento = str(amostra['RENDIMENTO'].values[0])
    preparo = str(int(amostra['PREPARO'].values[0]))

    return jsonify(nome=nome, link=link, rendimento=rendimento, preparo=preparo)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=port)
