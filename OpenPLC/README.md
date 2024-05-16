## Build

Use this command to build the **openplc-docker** image:

```console
foo@bar:~$ docker build -t openplc:v3 --build-arg init_files=</PATH/TO/INIT_FILES> .
```

**(!!!) </PATH/TO/INIT_FILES> folder must contain**:

- A ST (Structured Text) file with the programming of the PLC named **script.st** 
- A /devices/ folder containing the .cfg files of the devices (slaves) that will connect to the PLC.

Here is an example of a device config (.cfg) file:

```c
## Structure of a sample device config file
name="PythonWaterTankSlave"
slave_id=1
protocol="TCP"
address="127.0.0.1"
IP_Port=502
Discrete_Inputs_Start=0
Discrete_Inputs_Size=8
Coils_Start=0
Coils_Size=8
Input_Registers_Start=0
Input_Registers_Size=8
Holding_Registers_Read_Start=0
Holding_Registers_Read_Size=8
Holding_Registers_Start=0
Holding_Registers_Size=8
```
## Run


Docker run:

```console
foo@bar:~$ docker run -it --rm --privileged -p 8080:8080 -p 502:502 openplc:v3
```

