import os
from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import ValidationError
import init_db

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
DB_FILE_NAME = os.path.join(basedir, 'db.sqlite3')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+ DB_FILE_NAME

db = SQLAlchemy(app)
ma = Marshmallow(app)

class TranslationModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(255))
    foreign_word = db.Column(db.String(255))
    characters = db.Column(db.String(255))
    back_translation = db.Column(db.String(255))
    script_mandarin_translation = db.Column(db.String(255))
    script_english_translation = db.Column(db.String(255))
    context = db.Column(db.String(255))
    additional_info = db.Column(db.String(255))

    def __init__(self, id=None, category=None, foreign_word=None, characters=None, back_translation=None, script_mandarin_translation=None, script_english_translation=None, context=None, additional_info=None):
        self.id = id 
        self.category = category
        self.foreign_word = foreign_word
        self.characters = characters
        self.back_translation = back_translation
        self.script_mandarin_translation = script_mandarin_translation
        self.script_english_translation = script_english_translation
        self.context = context
        self.additional_info = additional_info
    
    def __repr__(self):
        return f'<TranslationModel {self.foreign_word} {self.category}>' 
    
class TranslationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TranslationModel 

translation_schema = TranslationSchema()
translations_schema = TranslationSchema(many=True)

@app.route("/")
@app.route('/api')
def index():
    base_url = request.base_url.replace('api','')
    return jsonify({'translation':f'{base_url}api/translation'})

@app.route('/api/translation', methods=['GET'])
def get_translations():
    all_translations = TranslationModel.query.all()
    return jsonify({
        'count': len(all_translations),
        'results': translations_schema.dump(all_translations)
    })

@app.route('/api/translation/<id>', methods=['GET'])
def get_translation(id): 
    translation = db.session.get(TranslationModel,id)
    if translation:
        return translation_schema.jsonify(translation)
    else:
        return 'Not Found', 404
    
@app.route("/api/translation", methods=['POST'])
def submit_translation():
    req_data = request.json

    if not 'secretkey' in req_data:
        return jsonify({
            'errorMessage': 'Invalid key. Please enter a valid key'
        }), 401
        
    try: 
        req_data.pop('secretkey') # remove secretkey. it's being passed in as a body param because idk how headers work yet
        result = translation_schema.load(req_data)
    except ValidationError as e:
        return f'bad request: {e.messages}', 400
    
    foreign_word = req_data['foreign_word']
    translation = TranslationModel(**result)
        
    existing = TranslationModel.query.filter(TranslationModel.foreign_word == foreign_word)
    if existing.count() > 0: 
        return jsonify({
            'errorMessage': f'Record with foreign_word \'{foreign_word}\' already exists'
        }), 400
        
    db.session.add(translation)
    db.session.commit()
    
    return jsonify({'message':'Translation successfully added'})

@app.route("/api/translation", methods=['PUT'])
def update_translation():
    req_data = request.json
    
    if not 'secretkey' in req_data: 
        return jsonify({
            'errorMessage': 'Invalid key. Please enter a valid key'
        }), 401
       
    if not 'id' in req_data: 
        return jsonify({
            'errorMessage': 'Id value was not provided. Please enter an id value to perform this request'
        }), 422
        
    try: 
        req_data.pop('secretkey') # remove secretkey. it's being passed in as a body param because idk how headers work yet
        result = translation_schema.load(req_data)
    except ValidationError as e:
        return f'bad request: {e.messages}'
    
    id = req_data.get('id', '')
    existing_translation = db.session.get(TranslationModel, id)
    if not existing_translation:
        return jsonify({
            'errorMessage': f'Record {id} not found. Unable to process this request'
        }), 400
        
    existing_translation.id = id 
    existing_translation.category = result['category']
    existing_translation.foreign_word = result['foreign_word']
    existing_translation.characters = result['characters']
    existing_translation.back_translation = result['back_translation']
    existing_translation.script_mandarin_translation = result['script_mandarin_translation']
    existing_translation.script_english_translation = result['script_english_translation']
    existing_translation.context = result['context']
    existing_translation.additional_info = result['additional_info']
    
    db.session.commit()
    return jsonify({'message':'Translation successfully updated'})

@app.route('/api/translation/<translation_id>', methods=['DELETE'])
def delete_translation(translation_id):
    existing_translation = db.session.get(TranslationModel, translation_id)
    
    if existing_translation is None: 
        return jsonify({
            'error_message': f'Record {translation_id} not found. Unable to process this request'
        }), 400
    
    db.session.delete(existing_translation)
    db.session.commit()

    return jsonify({'message':f'Translation {translation_id} successfully deleted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5173, debug=True) # debug