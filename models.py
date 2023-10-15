
class Translation:
  def __init__(self, id, category, foreign_word, characters, back_translation, script_mandarin_translation, script_english_translation, context, additional_info):
    
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
    return '<id {}>'.format(self.id) 

  def serialize(self):
    return {
      'id': self.id,
      'category': self.category,
      'foreign_word': self.foreign_word,
      'characters': self.characters,
      'back_translation':self.back_translation,
      'script_mandarin_translation':self.script_mandarin_translation,
      'script_english_translation':self.script_english_translation,
      'context':self.context,
      'additional_info':self.additional_info,
    }