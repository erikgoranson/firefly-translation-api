from flask import Flask, request, jsonify
import os
import db
from models import Translation

app = Flask(__name__)

DB_FILE_NAME = 'translations.db'

# create the database if needed and seed the table
if not os.path.isfile(DB_FILE_NAME):
    db.connect()

# route for landing page
@app.route("/")
@app.route('/api')
def index():
    base_url = request.base_url.replace('api','')
    return jsonify({'translation':f'{base_url}api/translation'})

@app.route('/api/translation', methods=['GET'])
def get_translation():
    trs = [t.serialize() for t in db.get_all()]
    return jsonify({
        'results': trs, 
        'status': '200',
        'count': len(trs)
    })

@app.route('/api/translation/<id>', methods=['GET'])
def get_translation_by_id(id):
    tr = db.get_by_id(id)
    if tr:
        return tr.serialize()
    else:
        return 'Not Found'
    
@app.route("/api/translation", methods=['POST'])
def submit_translation():
    req_data = request.json

    if not 'secretkey' in req_data:
        return jsonify({
            'errorMessage': 'Invalid key. Please enter a valid key'
        })# , 422 # status
        
    category = req_data['category']
    foreign_word = req_data['foreign_word']
    characters = req_data['characters']
    back_translation = req_data['back_translation']
    script_mandarin_translation = req_data['script_mandarin_translation']
    script_english_translation = req_data['script_english_translation']
    context = req_data['context']
    additional_info = req_data['additional_info']
    
    translation = Translation(None, category, foreign_word, characters, back_translation, script_mandarin_translation, script_english_translation, context, additional_info)
    
    existing = db.get_by_foreign_word(foreign_word)
    
    if existing is not None: 
        return jsonify({
            'errorMessage': f'Record with foreign_word \'{foreign_word}\' already exists'
        }), 400
    
    db.insert(translation)
    return jsonify({'message':'Translation successfully added', 'translation': translation.serialize()})
    
@app.route("/api/translation", methods=['PUT'])
def update_translation():
    req_data = request.json
    
    if not 'secretkey' in req_data: 
        # if not allowed, exit
        return jsonify({
            'errorMessage': 'Invalid key. Please enter a valid key'
        })# , 422 # status
       
    if not 'id' in req_data: 
        return jsonify({
            'errorMessage': 'Id value was not provided. Please enter an id value to perform this request'
        })# , 422 # status 
        
    id = req_data['id']
    category = req_data['category']
    foreign_word = req_data['foreign_word']
    characters = req_data['characters']
    back_translation = req_data['back_translation']
    script_mandarin_translation = req_data['script_mandarin_translation']
    script_english_translation = req_data['script_english_translation']
    context = req_data['context']
    additional_info = req_data['additional_info']
    
    translation = Translation(id, category, foreign_word, characters, back_translation, script_mandarin_translation, script_english_translation, context, additional_info)
    
    existing_record = db.get_by_id(id)
    
    if existing_record is None: 
        return jsonify({
            'errorMessage': f'Record {id} not found. Unable to process this request'
        }), 400
        
    db.update(translation)
    return jsonify({'message':'Translation successfully updated', 'original_translation': existing_record.serialize(), 'updated_translation':translation.serialize()})

@app.route('/api/translation/<id>', methods=['DELETE'])
def delete_translation(id):
    existing_record = db.get_by_id(id)
    
    if existing_record is None: 
        return jsonify({
            'errorMessage': f'Record {id} not found. Unable to process this request'
        }), 400
        
    db.delete(id)
    return jsonify({'message':f'Translation {id} successfully deleted'})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5173, debug=True) # debug