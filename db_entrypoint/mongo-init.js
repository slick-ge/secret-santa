var username = process.env.MONGO_INITDB_USERNAME || 'defaultuser';
var password = process.env.MONGO_INITDB_PASSWORD || 'defaultpassword';
db = db.getSiblingDB('secret-santa');
db.createUser({
    user: username,
    pwd: password,
  roles: [{ role: 'readWrite', db: 'secret-santa' }]
});
