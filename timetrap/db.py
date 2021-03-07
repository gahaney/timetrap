import sqlite3

class db(object):
  _DB_FILE = 'timetrap.db'
  _SCHEMA = 'timetrap/schema.sql'

  def __enter__(self):
    return self

  def __init__(self):
    self.conn = sqlite3.connect(db._DB_FILE)
    self.cur = self.conn.cursor()

  def __del__(self):
    self.close()

  def __exit__(self, ext_type, exc_value, traceback):
    self.cur.close()
    if isinstance(exc_value, Exception):
        self.conn.rollback()
    else:
        self.conn.commit()
    self.conn.close()

  def close(self):
    self.conn.close()

  def init_db(self):
    with open(self._SCHEMA) as schema:
      self.conn.executescript(schema.read())

  def insert(self, ticket, comment):
    self.cur.execute("select * from time where stop is null")
    count = self.cur.fetchone()
    if count==None:
      self.cur.execute("INSERT INTO time (ticket, comment) VALUES (?, ?)", (ticket, comment))
    else:
      print("You must stop tracking your current ticket first")

  def show(self):
    self.cur.execute("select ticket, start, stop, comment from time")
    rows = self.cur.fetchall()
    return rows

  def stop(self):
    self.cur.execute("update time set stop = datetime(CURRENT_TIMESTAMP, 'localtime') where stop is null")
    rows = self.cur.fetchall()
