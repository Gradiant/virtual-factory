# Dockerized ICS Lab

## Description of the project

This repo aims to develop and deploy a virtualized ICS network on which to perform cybersecurity tests and as a data generation/capture source. The network will consist of:

- HMI (FUXA): Human Machine Interface, used to monitor and control the industrial process. It provides a graphical user interface for the operator to interact with the system.

- PLCs (OpenPLC): Programmable Logic Controllers, used to control the industrial process. They execute the control logic and communicate with the HMI and end devices.

- End devices (simulated in Python 3 and deployed through Docker containers): These are the physical devices connected to the PLCs, such as sensors, actuators, etc. They provide input and receive output from the PLCs. They are simulated in Python 3 and deployed through Docker containers for ease of use and portability.

- Attacker nodes (Kali Linux + Python3 + Docker): These are nodes that simulate malicious actors attempting to gain unauthorized access to the ICS network and disrupt its normal operation. These nodes can be used to test the security measures implemented in the ICS network and evaluate their effectiveness.

- Sniffer nodes: nodes to capture de traffic in order to study and detect the cyberattacks

## Demo description
- Flaming Moe's
In this demo, the goal is to represents an industrial factory who make flaming Moe's drink.
The process mix different drinks, in order to put the final mixture in a bottle

![flaming moes fuxa interface.PNG](images%2Fflaming%20moes%20fuxa%20interface.PNG)

## Start DEMO Flaming Moe's

```
docker-compose up
```

## UI
- Openplc interface: http://localhost:8080  (openplc:openplc)
- Fuxa interface: http://localhost:1881

## Simulators configuration

Each simulator has its configuration file that will tell it how it should connect and how it should act.

- **simulator_connector_client** -> This is a communication between simulators, so that they can pass data from their internal state and that they can simulate something real, such as the flow of water.
current supported connectors: 
  - mqtt

- **industrial_connector_client** -> It is the industrial protocol connection through which we want to connect, here the corresponding values that would be sent by this type of protocol will be sent.
current supported connectors: 
  - modbus

- **simulator_names**: -> list of simulator names, although it is a list, my advice is to use one, otherwise they will share an IP address and it is not so realistic.

- **for simulator_name in simulator names**: -> we must inform the following fields
- type: 
  - tank
  - tap
  - valve
  - pipe
  - drain
- **inputs**: -> list of names of other simulators that are connected to the input of this simulator
- **outputs**: -> list of names of other simulators that are connected to the output of this simulator
- **mapper_industry_properties**: -> this mapper will help transform simulator code variables into industrial protocol variables/registers. The mapper is needed to read and write, where each variable will have its correspondence with the chosen protocol.
  - if modbus: -> We must put the corresponding register number in map, and the type in type: (coil, register, uregister)->(boolean, int16, uint16) respectively.
  
    - **valve**: -> open-> variable that indicates when it should be opened or closed, it uses two registers, one to show the status and another to modify it.    
    - **tank**: heat_cool_level: variable that indicates when it should be heated, coll down or stay the same temperture.
      - temp: current temperture
      - max_temp: maximum temperature admitted
      - min_temp: minimum temperature admitted
      - pressure: current pressure
      - max_pressure: maximum presión admitted
      - min_pressure: minimum pressure admitted
      - capacity: current capacity
      - max_capacity: maximum capacidad admitted
      - min_capacity: minimum capacity admitted
      - 
- **buggable**: Indicates whether a bug controlled by the buggable-cli can be caused

- **configuration variables of each simulator**:
  - tap: 
    - output_level -> number of units that we want the output flow to be.
  - valve:
    - output_level -> number of units that we want the output flow to be.
  - tank: 
    - output_level -> number of units that we want the output flow to be.
    - temp: temperature at which the simulation starts
    - max_temp: maximum temperature admitted
    - min_temp: minimum temperature admitted
    - pressure: pressure at which the simulation starts
    - max_pressure: maximum presión admitted
    - min_pressure: minimum pressure admitted
    - capacity: capacity at which the simulation starts
    - max_capacity: maximum capacidad admitted
    - min_capacity: minimum capacity admitted


# Class Architecture

![Arch.PNG](images%2FArch.png)
