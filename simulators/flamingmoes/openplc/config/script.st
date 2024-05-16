PROGRAM flamingmoes
  VAR
    put_tequila_valve_status AT %QX100.0 : BOOL;
    tequila_valve_status AT %QX100.1 : BOOL;
    put_peppermint_valve_status AT %QX100.2 : BOOL;
    peppermint_valve_status AT %QX100.3 : BOOL;
    put_mintcream_valve_status AT %QX100.4 : BOOL;
    mintcream_valve_status AT %QX100.5 : BOOL;
    put_brandy_valve_status AT %QX100.6 : BOOL;
    brandy_valve_status AT %QX100.7 : BOOL;
    put_gin_valve_status AT %QX101.0 : BOOL;
    gin_valve_status AT %QX101.1 : BOOL;
    put_coughsyrup_valve_status AT %QX101.2 : BOOL;
    coughsyrup_valve_status AT %QX101.3 : BOOL;
    put_mixtank1_valve_status AT %QX101.4 : BOOL;
    mixtank1_valve_status AT %QX101.5 : BOOL;
    put_mixtank2_valve_status AT %QX101.6 : BOOL;
    mixtank2_valve_status AT %QX101.7 : BOOL;
    put_recolector_valve_status AT %QX102.0 : BOOL;
    recolector_valve_status AT %QX102.1 : BOOL;
    put_dispenservalve1_status AT %QX102.2 : BOOL;
    dispenservalve1_status AT %QX102.3 : BOOL;
    put_dispenservalve2_status AT %QX102.4 : BOOL;
    dispenservalve2_status AT %QX102.5 : BOOL;
    put_dispenservalve3_status AT %QX102.6 : BOOL;
    dispenservalve3_status AT %QX102.7 : BOOL;
    manual_mode AT %QX199.7 : BOOL;

    mix_tank1_capacity AT %QW100 : UINT;
    mix_tank1_min_capacity AT %QW101 : UINT;
    mix_tank1_max_capacity AT %QW102 : UINT;
    mix_tank1_max_pressure AT %QW103 : UINT;
    mix_tank1_min_pressure AT %QW104 : UINT;
    mix_tank1_pressure AT %QW105 : UINT;
    mix_tank1_max_temp AT %QW106 : UINT;
    mix_tank1_min_temp AT %QW107 : INT;
    mix_tank1_temp AT %QW108 : INT;
    mix_tank1_heat_cool_level AT %QW109 : INT;

    mix_tank2_capacity AT %QW110 : UINT;
    mix_tank2_min_capacity AT %QW111 : UINT;
    mix_tank2_max_capacity AT %QW112 : UINT;
    mix_tank2_max_pressure AT %QW113 : UINT;
    mix_tank2_min_pressure AT %QW114 : UINT;
    mix_tank2_pressure AT %QW115 : UINT;
    mix_tank2_max_temp AT %QW116 : INT;
    mix_tank2_min_temp AT %QW117 : INT;
    mix_tank2_temp AT %QW118 : INT;
    mix_tank2_heat_cool_level AT %QW119 : INT;


    recolector_capacity AT %QW120 : UINT;
    recolector_min_capacity AT %QW121 : UINT;
    recolector_max_capacity AT %QW122 : UINT;
    recolector_max_pressure AT %QW123 : UINT;
    recolector_min_pressure AT %QW124 : UINT;
    recolector_pressure AT %QW125 : UINT;
    recolector_max_temp AT %QW126 : INT;
    recolector_min_temp AT %QW127 : INT;
    recolector_temp AT %QW128 : INT;
    recolector_heat_cool_level AT %QW129 : INT;

  END_VAR

    tequila_valve_status := tequila_valve_status;
    put_tequila_valve_status := put_tequila_valve_status;
    peppermint_valve_status := peppermint_valve_status;
    put_peppermint_valve_status := put_peppermint_valve_status;
    mintcream_valve_status := mintcream_valve_status;
    put_mintcream_valve_status := put_mintcream_valve_status;
    brandy_valve_status := brandy_valve_status;
    put_brandy_valve_status := put_brandy_valve_status;
    gin_valve_status := gin_valve_status;
    put_gin_valve_status := put_gin_valve_status;
    coughsyrup_valve_status := coughsyrup_valve_status;
    put_coughsyrup_valve_status := put_coughsyrup_valve_status;
    put_mixtank1_valve_status := put_mixtank1_valve_status;
    mixtank1_valve_status := mixtank1_valve_status;
    put_mixtank2_valve_status := put_mixtank2_valve_status;
    mixtank2_valve_status := mixtank2_valve_status;
    put_recolector_valve_status := put_recolector_valve_status;
    recolector_valve_status := recolector_valve_status;
    put_dispenservalve1_status := put_dispenservalve1_status;
    dispenservalve1_status := dispenservalve1_status;
    put_dispenservalve2_status := put_dispenservalve2_status;
    dispenservalve2_status := dispenservalve2_status;
    put_dispenservalve3_status := put_dispenservalve3_status;
    dispenservalve3_status := dispenservalve3_status;
    manual_mode := manual_mode;

    mix_tank1_capacity := mix_tank1_capacity;
    mix_tank1_min_capacity := mix_tank1_min_capacity;
    mix_tank1_max_capacity := mix_tank1_max_capacity;
    mix_tank1_max_pressure := mix_tank1_max_pressure;
    mix_tank1_min_pressure := mix_tank1_min_pressure;
    mix_tank1_pressure := mix_tank1_pressure;
    mix_tank1_max_temp := mix_tank1_max_temp;
    mix_tank1_min_temp := mix_tank1_min_temp;
    mix_tank1_temp := mix_tank1_temp;
    mix_tank1_heat_cool_level := mix_tank1_heat_cool_level;

    mix_tank2_capacity := mix_tank2_capacity;
    mix_tank2_min_capacity := mix_tank2_min_capacity;
    mix_tank2_max_capacity := mix_tank2_max_capacity;
    mix_tank2_max_pressure := mix_tank2_max_pressure;
    mix_tank2_min_pressure := mix_tank2_min_pressure;
    mix_tank2_pressure := mix_tank2_pressure;
    mix_tank2_max_temp := mix_tank2_max_temp;
    mix_tank2_min_temp := mix_tank2_min_temp;
    mix_tank2_temp := mix_tank2_temp;
    mix_tank2_heat_cool_level := mix_tank2_heat_cool_level;

    recolector_capacity := recolector_capacity;
    recolector_min_capacity := recolector_min_capacity;
    recolector_max_capacity := recolector_max_capacity;
    recolector_max_pressure := recolector_max_pressure;
    recolector_min_pressure := recolector_min_pressure;
    recolector_pressure := recolector_pressure;
    recolector_max_temp := recolector_max_temp;
    recolector_min_temp := recolector_min_temp;
    recolector_temp := recolector_temp;
    recolector_heat_cool_level := recolector_heat_cool_level;


END_PROGRAM


CONFIGURATION Config0

  RESOURCE Res0 ON PLC
    TASK task0(INTERVAL := T#200ms,PRIORITY := 0);
    PROGRAM instance0 WITH task0 : flamingmoes;
  END_RESOURCE
END_CONFIGURATION
