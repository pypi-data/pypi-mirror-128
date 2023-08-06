
#####################################################################
#
# sapiadapter.py
#
# Project   : SAPIADAPTER
# Author(s) : Zafar Iqbal < zaf@sparc.space >
# Copyright : (C) 2021 SPARC PC < https://sparc.space/ >
#
# All rights reserved. No warranty, explicit or implicit, provided.
# SPARC PC is and remains the owner of all titles, rights
# and interests in the Software.
#
#####################################################################

from . import s_log , s_config , s_net , s_util , s_db , s_cleanup

#####################################################################

#s_log.write( "    ####    ####    ####    ####\n" )

#####################################################################

s_config.setup( )
s_db.setup( )

#s_log.write( s_config.get_key( "/config/version" ) ) 

#####################################################################


def isready( ) :

    if( not s_util.ready( ) ) :
        s_log.write( "ERROR False ready" )
        return( False )

    s_log.write( "OK" )
    return( True )

#####################################################################

def config_load_from_file( cp ) :
    return( s_config.load_from_file( cp ) )

def ready( ) :
    return( s_util.ready( ) )

def prexit( msg ) :
    s_util.printexit( msg )

def defdata( ) :
    return( s_db.files_defdata_get( ) )

def defmeta( ) :
    return( s_db.files_defmeta_get( ) )

def uptime( ) :
    return( s_util.uptime( ) )
def uptime_lap( ) :
    return( s_util.uptime_lap( ) )

def heartbeat( t = 60 ) :
    return( s_util.heartbeat( t ) )

def server( ) :

    s_log.write( "SERVER STARTED" )

    while True :


        s_log.write("SERVER LOOP")

        heartbeat( )

        #####################################################

        try :
            flag_jobget = s_net.job_get( )
        except Exception as e :
            s_util.printexception( )
            #continue
            prexit( "EXCEPTION job_get" )
            #sys.exit( 99 )

        #####################################################
        
        if flag_jobget == False :

            s_log.write( "ERROR False job_get" )
            continue
            #sapi.prexit( "False job_get" )

        if flag_jobget == None :
            continue

        #####################################################

        defmeta = s_db.files_defmeta_get( )
        if( "_ping_5800b137d" in defmeta ) :
            #print(defmeta["_ping_5800b137d"])
            t1 = defmeta[ "_ping_5800b137d" ]
            s_db.setup( )
            defdata=[ "_ping_5800b137d" ] 
            defmeta = {
                "_ping_5800b137d" : "." + t1
            }
            s_db.files_defdata_set( defdata )
            s_db.files_defmeta_set( defmeta)
            s_net.job_set( )
            s_log.write( "OK PINGPONG" )
            continue

        #####################################################

        if( not s_util.proc_setup( ) ) :
            continue

        #####################################################

        s_util.proc_run( )

        #####################################################

        s_util.proc_storage( )
        s_util.proc_teardown( )

        #####################################################

        s_net.job_set( )

        #####################################################

        s_log.write( "OK" )




#####################################################################

# DATA
# TIMEOUT
def run( meta_inputs = { } , wait_timeout = 60 ) :

    if( not ready( ) ) :
        s_log.write( "NOT READY" )
        return( False )

    if( not meta_inputs ) :
        #s_log.write( "false meta_inputs " )
        #return( False )
        meta_inputs["module"] = "sparc1/test_read_metadata_odi/entrypoint1"


    if( not isinstance( meta_inputs , ( dict ) ) ) :
        s_log.write( "false meta_inputs dict" )
        return( False )

    #####################################################################

    s_db.setup( )

    #####################################################################

    f = s_db.files_defmeta_set( meta_inputs ) 

    if( not f ) :
        s_log.write( "false meta_add " )
        return( False )

    #####################################################################

    if not s_net.job_request( ) :
        s_log.write( "false job_request" )
        return( False )

    #####################################################################

    jid = s_config.get_key( "jid" )

    if( jid == False ) :
        s_log.write( "false job_request jid" )
        return( False )

    #####################################################################

    jr = s_net.job_responsewait( jid , wait_timeout )

    if( jr == False ) :
        s_log.write( "false job_wait" )
        return( False )

    if( jr == None ) :
        s_log.write( "none job_wait" )
        return( None )

    #####################################################################

    if( s_db.stdio_has_stderr( ) ) :
        s_log.write( "ERROR stdio_has_stderr " + s_db.stdio_get_stderr( ) )
        return( None )

    #####################################################################

    dd = defdata( )
    if( dd==False ) : return(True)
    return(dd)
