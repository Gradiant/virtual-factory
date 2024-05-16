PROGRAM flamingmoes
  VAR
    put_valve_status AT %QX100.0 : BOOL;
    valve_status AT %QX100.1 : BOOL;
    put_valve_status_int AT %QW100 : BOOL;
    valve_status_int AT %QW101 : BOOL;



  END_VAR

    put_valve_status := put_valve_status;
    valve_status := valve_status;
    put_valve_status_int := put_valve_status_int;
    valve_status_int := valve_status_int;


END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#200ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : flamingmoes;
  END_RESOURCE
END_CONFIGURATION
