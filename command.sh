curl -X POST -H Content-Type: application/json -d {"Name":"John","Surname":"Doe","email":"john@example.com"} http://localhost:5000/store_data



db.createUser({ user: "santaapp", pwd: "test", roles: [{ role: "readWrite", db: "secret-santa" }] } )


mongosh "mongodb://10.10.10.29:27017" -u root -p example




docker run --rm -it rtsp/mongosh bash


