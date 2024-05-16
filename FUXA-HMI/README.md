## Build

Use this command to build the **fuxa:latest** image:

```console
foo@bar:~$ docker build -t fuxa:latest .
```
## Run

Docker run:

```console
foo@bar:~$ docker run --name HMI -d -p 1881:1881 fuxa:latest
```

## Access

[Link text Here](http://localhost:1881/)

## POST command to upload an already created FUXA project stored as a JSON config file

```console
curl -X POST -H "Content-Type: application/json" --data-binary "@fuxa-project.json" http://localhost:1881/api/project
```