#!/bin/bash

###### MODIFYING OPENPLC DATABASE ######

# Remove all existing programs
echo "Removing Existent Programs"
SQL_REMOVE_PROGRAM="DELETE FROM Programs"
sqlite3 /OpenPLC_v3/webserver/openplc.db "$SQL_REMOVE_PROGRAM"

# Remove all existing slave devices
echo "Removing Existent Salves"
SQL_REMOVE_DEVICE="DELETE FROM Slave_dev"
sqlite3 /OpenPLC_v3/webserver/openplc.db "$SQL_REMOVE_DEVICE"

# Add new program as "script.st"
echo "Loading scripts"
SQL_PROGRAM="INSERT INTO Programs (Name, Description, File, Date_upload) VALUES ('Program Name', 'Desc', 'script.st', strftime('%s', 'now'));"
sqlite3 /OpenPLC_v3/webserver/openplc.db "$SQL_PROGRAM"



echo "Loading devices"
devices_path="/OpenPLC_v3/scripts/config/devices" # Path where devide configurations are stored
# add new slave device. modify and copy this line if need to add more slaves
for file in $(find "$devices_path" -type f -name "*.cfg"); do
    echo "Processing $file"
    . $file
    SQL_DEVICE="INSERT INTO Slave_dev (dev_name, dev_type, slave_id, ip_address, ip_port, di_start, di_size, coil_start, coil_size, ir_start, ir_size, hr_read_start, hr_read_size, hr_write_start, hr_write_size, baud_rate, parity, data_bits, stop_bits, pause) VALUES ('$name', '$protocol', $slave_id, '$address', $IP_Port, $Discrete_Inputs_Start, $Discrete_Inputs_Size, $Coils_Start, $Coils_Size, $Input_Registers_Start, $Input_Registers_Size, $Holding_Registers_Read_Start, $Holding_Registers_Read_Size, $Holding_Registers_Start, $Holding_Registers_Size, $baud_rate, '$parity', $data_bits, $stop_bits, $pause);"

    sqlite3 /OpenPLC_v3/webserver/openplc.db "$SQL_DEVICE"
done

# enable openplc start run mode. Comment out if not requried.
SQL_Start_run_mode="UPDATE Settings SET Value = 'true' WHERE Key = 'Start_run_mode';"
sqlite3 /OpenPLC_v3/webserver/openplc.db "$SQL_Start_run_mode"

# set active program
echo "script.st" > /OpenPLC_v3/webserver/active_program
cp /OpenPLC_v3/scripts/config/script.st /OpenPLC_v3/webserver/st_files

# compile new program for the first time
cd /OpenPLC_v3/webserver/scripts
echo "Compiling scripts.st"
./compile_program.sh script.st

# generate mbconfig.cfg
cd /OpenPLC_v3/webserver/
echo "Generating mbconfig.cfg"
python2.7 -c 'import webserver; webserver.generate_mbconfig()'

# start openplc webserver
cd /OpenPLC_v3
echo "Starting server"
./start_openplc.sh

wait