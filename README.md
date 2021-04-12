# Nearest Driver Web Service
This is a Web Service challenge that uses the driverLocationsApi and the Azure Maps Route API to get the closest driver using longitude and latitude.

API for the nearest driver web service should match the webServiceApi.yaml OpenAPI file.
Also the service is deployed using Docker, therefore, host must download Docker to easily follow the Docker deployment. Benefit of web service being in a container is that it is extremely small in size.

Project structure:
```
.
├── docker-compose.yaml
├── app
    ├── Dockerfile
    ├── requirements.txt
    └── app.py

```

[_docker-compose.yaml_](docker-compose.yaml)
```
services: 
  web: 
    build: app 
    ports: 
      - '5000:5000'
```


## Deploy with docker-compose

```
$ docker-compose up -d
Creating network "kevin-challenge_default" with the default driver
Building web
[+] Building 11.1s (11/11) FINISHED                                                                                                                                                                                 
 => [internal] load build definition from Dockerfile                                                                                                                                                           0.0s
 => => transferring dockerfile: 217B                                                                                                                                                                           0.0s
 => [internal] load .dockerignore                      
```
## Expected result

Listing containers must show one container running and the port mapping as below:
```
$ docker ps
CONTAINER ID   IMAGE                 COMMAND            CREATED         STATUS         PORTS                      NAMES
025663d275b3   kevin-challenge_web   "python3 app.py"   4 seconds ago   Up 3 seconds   0.0.0.0:5000->5000/tcp     kevin-challenge_web_1
```

## Tests

- After the application starts, navigate to `http://localhost:5000` in your web browser or run:
```
    $ curl localhost:5000 
    This is dispatch closest driver web service
```

- example API test with terminal: 
```
    $ curl -X 'POST' 'http://127.0.0.1:5000/api/dispatch-closest-driver?lon=-80.79554578876035&lat=35.57102321926562' -H 'accept: application/json'  -d ''
    {
        "distance": 94641, 
        "driverId": "cdda0837-327d-4fa6-a64e-e0821ed19fbf"
    }
```
- same example API test with using Postman (return same as above):
    - Make sure it is a **POST** and paste in:
        - **http://127.0.0.1:5000/api/dispatch-closest-driver?lon=-80.79554578876035&lat=35.57102321926562**
    
## Stop and remove the containers
```
$ docker-compose down
```