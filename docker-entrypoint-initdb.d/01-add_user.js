
const user = _getEnv("MONGODB_SMARTER_USER")
const pass = _getEnv("MONGODB_SMARTER_PASS")
const database = _getEnv("MONGO_INITDB_DATABASE")

db = db.getSiblingDB('admin')
db.createUser({user: user, pwd: pass, roles: [{role: "readWrite", db: database}]})
