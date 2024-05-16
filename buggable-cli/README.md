#### Ejemplo de archivo JSON con anomalias
```
{
  "123": {
    "id": "123",
    "target": "mixtank2",
    "variable": "_max_capacity",
    "duration": 10,
    "variance": 4,
    "wander_factor": 0,
    "type": "noise",
    "deployment_time": "2023-08-29 13:21:23",
    "ready": true
  },
  "dkiqk": {
    "id": "dkiqk",
    "target": "conveyorbelt1",
    "variable": "_speed",
    "duration": 5,
    "variance": 0,
    "wander_factor": 1.2,
    "type": "wander",
    "value": 1,
    "deployment_time": "2023-08-29 12:26:23",
    "ready": true,
    "periodicity": 10
  }
}
```