from replit import db

class Repository():
  def __init__(self): pass

  def save(self, user_id):
    db[str(user_id)] = str(user_id)

  def findAll(self):
    return db.keys()

  def reset(self):
    user_ids = self.findAll()
    for user_id in user_ids:
      del db[user_id]