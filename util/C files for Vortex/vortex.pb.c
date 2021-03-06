/* Automatically generated nanopb constant definitions */
/* Generated by nanopb-0.3.2 at Sun Mar 22 23:16:59 2015. */

#include "vortex.pb.h"

#if PB_PROTO_HEADER_VERSION != 30
#error Regenerate this file with the current version of nanopb generator.
#endif

const command_data_CommandType command_data_command_default = command_data_CommandType_STOP;


const pb_field_t sensor_data_fields[4] = {
    PB_FIELD(  1, UINT32  , REPEATED, CALLBACK, FIRST, sensor_data, ir_data_array, ir_data_array, 0),
    PB_FIELD(  2, UINT32  , REPEATED, CALLBACK, OTHER, sensor_data, sonar_data_array, ir_data_array, 0),
    PB_FIELD(  3, UINT32  , OPTIONAL, STATIC  , OTHER, sensor_data, timestamp, sonar_data_array, 0),
    PB_LAST_FIELD
};

const pb_field_t command_data_fields[3] = {
    PB_FIELD(  1, ENUM    , OPTIONAL, STATIC  , FIRST, command_data, command, command, &command_data_command_default),
    PB_FIELD(  2, INT32   , REPEATED, CALLBACK, OTHER, command_data, args, command, 0),
    PB_LAST_FIELD
};


