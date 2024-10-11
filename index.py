from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from config.dbformat import Dbformat
from dbinstances.estacoes_repository import EstacoesRepository
from dbinstances.corretivas_repository import CorretivasRepository

app = Flask(__name__)

cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/estacoesLayer', methods = ['GET'])
def get_GeojsonLayer():
    data = EstacoesRepository().select_estacoeslayer()

    geojson = Dbformat().db_format_to_geojson(dbformat=data, geometry='Geometria')
    print(geojson)
    return geojson, 200, {'Content-Type': 'application/json'}

@app.route('/corretivaslayer', methods = ['GET'])
def get_corretivas_layer():
    data = CorretivasRepository().select_corretivas_layer()

    geojson = Dbformat().db_format_to_geojson(dbformat=data, geometry = 'Geometria')

    return geojson, 200, {'Content-Type': 'application/json'}

@app.route('/insertCorretiva', methods = ['POST'])
def insert_corretiva():
    data = request.json
    print(data)
    insert_data = CorretivasRepository().insert_corretiva(data['estacao_id'], **data['params'])

    return jsonify(data)

@app.route('/removeCorretiva', methods = ['POST'])
def remove_corretiva():
    data = request.json
     
    remove_data = CorretivasRepository().remove_corretiva(data['corretiva_id'])

    return jsonify(data)

@app.route('/updateCorretiva', methods = ['POST'])
def update_corretiva():
    data = request.json
    print(data)
    update_data = CorretivasRepository().update_corretiva(data['corretiva_id'], **data['params'])

    return jsonify(data)

if __name__ == "__main__":
	app.run(debug=True)