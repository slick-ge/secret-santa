curl -X POST -H Content-Type: application/json -d {"Name":"Mikheli","Surname":"Shubitidze","email":"misho@example.com"} http://localhost:5000/store_data
curl -X POST -H Content-Type: application/json -d {"Name":"Aleksandre","Surname":"Ghvineria","email":"misho@example.com"} http://localhost:5000/store_data
curl -X POST -H Content-Type: application/json -d {"Name":"Dachi","Surname":"Arghutashvili","email":"misho@example.com"} http://localhost:5000/store_data
curl -X POST -H Content-Type: application/json -d {"Name":"Endelika","Surname":"Mtsariashvili","email":"misho@example.com"} http://localhost:5000/store_data
curl -X POST -H Content-Type: application/json -d {"Name":"Lana","Surname":"Janezashvili","email":"misho@example.com"} http://localhost:5000/store_data
curl -X POST -H Content-Type: application/json -d {"Name":"Natali","Surname":"Jeiranashvili","email":"misho@example.com"} http://localhost:5000/store_data


db.createUser({ user: "santaapp", pwd: "test", roles: [{ role: "readWrite", db: "secret-santa" }] } )

mongosh "mongodb://10.10.10.29:27017" -u root -p example




docker run --rm -it rtsp/mongosh bash


