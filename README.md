## avasec simple python backend

### installation

1. docker build -t asback .
2. docker run -p 8080:8080 asback

### test

* All Roles:      curl http://localhost:8080/api/role
* Specific Role:  curl http://localhost:8080/api/role/1
* Add new Role:   curl -X POST -H "Content-Type: application/json" -d '{"extid":"42","charid":"role_42","name":"Role 42"}' http://localhost:8080/api/role
* Update Role:    curl -X PUT  -H "Content-Type: application/json" -d '{"name":"Role number one"}' http://localhost:8080/api/role/1
* Delete Role:    curl -X DELETE http://localhost:8080/api/role/3
* Search Roles:   curl http://localhost:8080/api/role/search?q=12
* Acode:          same like role (no search yet)
* Role - Acode:   curl -H "Content-Type: application/json" -X POST -d '{"role_id":"100", "acode_id":"200"}' http://localhost:8080/api/role_acode
