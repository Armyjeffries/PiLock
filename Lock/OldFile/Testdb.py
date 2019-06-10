import shelve

db = shelve.open('cardid')
idnumberdb = db['Card UID']
print idnumberdb
print db
db.close()
