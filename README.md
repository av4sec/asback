## avasec simple python backend

### installation

1. docker build -t asback .
2. docker run -p 8080:8080 asback

### test

* curl http://localhost:8080/api/role
* curl http://localhost:8080/api/role/1
* curl -H "Content-Type: application/json" -X POST -d '{"extid":"42","charid":"role_42","name":"Role 42"}' http://localhost:8080/api/role
* curl -H "Content-Type: application/json" -X PUT -d '{"name":"Role number one"}' http://localhost:8080/api/role/1
* curl -X DELETE http://localhost:8080/api/role/3
