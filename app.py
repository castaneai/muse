import sqlite3
import bottle
import bottle_sqlite

app = bottle.Bottle()
app.install(bottle_sqlite.Plugin(dbfile="test.db"))


@app.get("/init")
def init(db):
    db.executescript(open("init.sql").read())
    return "init OK."


@app.get("/musics")
def get_musics(db):
    return db.execute("select * from musics left join artworks on musics.id = artworks.music_id").fetchall()


app.run(host="localhost", port=8080, debug=True)
