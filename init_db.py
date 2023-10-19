from datetime import date
from app import db, app, DB_FILE_NAME, TranslationModel
import os
from seed import translations

with app.app_context():
    if not os.path.isfile(DB_FILE_NAME):
        db.drop_all()
        db.create_all()
        
        for i in translations:
            translation = TranslationModel(**i) 
            db.session.add(translation)
        db.session.commit()