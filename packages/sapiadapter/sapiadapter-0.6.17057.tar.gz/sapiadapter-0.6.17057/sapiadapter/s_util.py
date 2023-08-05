
#####################################################################
#
# s_util.py
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

import os
import sys
import time
import json
import pickle
import uuid
import hashlib
import base64
import shutil
import gzip
import inspect

from subprocess import Popen, PIPE

from pathlib import Path
from traceback import format_exception

from . import s_log , s_config , s_net , s_db

#####################################################################

class NumpyEncoder( json.JSONEncoder ) :

    def default( self , obj ) :
        return  json.JSONEncoder.default( self , obj )
        #if isinstance( obj , numpy.integer ) :
        #    return int( obj )
        #elif isinstance( obj, numpy.floating ) :
        #    return float( obj)
        #elif isinstance( obj, numpy.ndarray ) :
        #    return obj.tolist( )
        #return json.JSONEncoder.default( self , obj )

def json_encode( data ) :
    return json.dumps( data , cls = NumpyEncoder )

#####################################################################

def pickle_load( fn ) :
    if( os.path.isfile( fn ) ) :
        s_log.write_msg( "FOUND " + fn )
        with open( fn , "rb" ) as f :
            return( pickle.load( f ) )
    else :
        return None
        
def pickle_save( datakey , data ) :
    f = open( "local_" + datakey + ".pkl" , "wb" )
    pickle.dump( run_response , f )
    f.close( )


 
def pathnotallowed( p ) :

    #s_log.write( p )

    p1 = os.path.normpath(p)
    #s_log.write( p1 )

    p2 = os.path.realpath(p1)
    #s_log.write( p2 )

    base_dir = s_config.get_key( "/config/cwd" , "/tmp")

    path_test = ( Path( base_dir ) / p2 ).resolve( ) 

    s_log.write(str(Path(base_dir).resolve()))
    s_log.write(str(path_test.parent))

    if( str( path_test.parent ).startswith( base_dir ) ) :
        return( False )

    s_log.write("pathnotallowed "+p)
    s_log.write(str(Path(base_dir).resolve()))
    s_log.write(str(path_test.parent))

    return( True )


def uhash( prefix = "" ) :
    return( prefix + hashlib.sha256( str( uuid.uuid4( ) ).encode( "utf-8" )  ).hexdigest( ) )

def hash( str , prefix = "" ) :
    return( prefix + hashlib.sha256( str ).hexdigest( ) )

def base64_decode( str ) :
    m = base64.b64decode( str ).decode( "utf-8" )
    return( m )


def is_ip( address ) :
    if( not address ) : return( False )
    return( not address.split( "." )[ -1 ].isalpha( ) )
    

def uptime( ) :
    return( time.time( ) - s_config.get_key( "/config/init/time" ) )


def uptime_lap( ) :

    tn = time.time( )

    tlp = s_config.get_key( "/config/init/time_lap" )  

    tl = tn - tlp 

    s_config.set_key( "/config/init/time_lap" , tn )

    return( tl )


def printexit( msg ) :
    print( msg )
    sys.exit( )


def printexception( e = False ) :
    if e:
        print( "EXCEPTION" + str( e ) )
    etype , value, tb = sys.exc_info( )
    info , error = format_exception( etype , value , tb )[ -2: ]
    print( f'Exception in:\n{info}\n{error}' )


heartbeat_last = 0
def heartbeat( t = 60 ) :
    global heartbeat_last
    time.sleep( 0.01 )
    if( uptime( ) - heartbeat_last ) < t : return( False )
    s_log.write( "@" )
    heartbeat_last = uptime( )
    return( True )

def ready( ) :

    # FIXME TODO move this out to function
    config = s_config.get_config( )
    if "/config/init/path_time" in config :
        cd = config[ "/config/cwd" ]
        cip = config[ "/config/init/path" ]
        cipt = config[ "/config/init/path_time" ]

        cfp=cip
        if not os.path.isabs(cip):
            cfp = cd + "/" + cip

        if os.path.isfile( cfp ) :

            cipt2 = os.path.getmtime( cfp )
            if( os.path.getmtime( cfp ) != cipt ) :
                s_config.setup( )
                s_db.setup( )
                s_log.write( "RELOADED " )
                #s_log.write( "CONFIG RELOADED " + cfp + str( cipt ) )

    ####################################################################

    if( not s_config.isready( ) ) :
        return( False )

    if( not s_net.check_connectivity( ) ) :
        return( False )

    return( True )

####################################################################

def gen_workingdirectory( ) :
    work_dir = wd = s_config.get_key( "sys/workspacedir" ) + "/" + uhash( "WOK" )
    return( work_dir )

####################################################################

def proc_setup( ) :

    work_dir = gen_workingdirectory( )

    # FIXME TODO should be coming from config
    shutil.copytree( "/data/app/" , work_dir , ignore = shutil.ignore_patterns( ".git*" ) )

    os.chdir( work_dir )
    #print(os.getcwd())

    s_config.set_key( "sys/work_dir" , work_dir ) 

    # BEFORE WE ADD DEFAULT INPUT/OUTPUT FILE!!!
    proc_trackcurrentfiles( )

    ################
    #default_inputs =  s_db.meta_getdefault( )
    #s_db.files_set_defaultdata( default_inputs )
    s_db.files_defmeta_write( )
    ################

    s_db.setup( ) 

def proc_trackcurrentfiles( ) :

    procfiles = { }
    for dirpath , dirs, files in os.walk( "." ) :  
        for filename in files :
            fname = os.path.join( dirpath , filename )
            #fname=os.path.abspath(fname)
            #print(fname)
            procfiles[ fname ] = True
            #if( not s_db.files_create( fname ) ) :
            #    s_log.write( "ERROR files_create " + fname )
            #with open(fname) as myfile:
            #print(myfile.read())

    s_config.set_key( "sys/procfiles" , procfiles ) 

def proc_run( ) :

    pargs = ""

    # FIXME TODO filename should be coming from config
    process = Popen( [ "bash" , "_sapiserver_entrypoint_.sh" , pargs ] , stdout = PIPE , stderr = PIPE )

    stdout , stderr = process.communicate( )

    #print(os.getcwd())

    if stdout :
        stdout = str( stdout , "utf-8" )
        if( stdout.strip( ) != "" ) :
            s_db.stdio_create( 1 , stdout )
    if stderr :
        stderr = str( stderr , "utf-8" )
        if( stderr.strip( ) != "" ) :
            s_db.stdio_create( 2 , stderr )

def proc_storage( ) :

    procfiles = s_config.get_key( "sys/procfiles" ) 

    for dirpath , dirs, files in os.walk( "." ) :  
        for filename in files :
            fname = os.path.join( dirpath , filename )
            #fname=os.path.abspath(fname)
            #print(fname)
            if fname in procfiles : continue
            #print(fname)


            file_extension = Path( fname ).suffix

            # FIXME TODO extensions (list of) should be coming from config
            if(file_extension==".pyc"): continue

            if( not s_db.files_create( fname ) ) :
                s_log.write( "ERROR files_create " + fname )
            #with open(fname) as myfile:
            #print(myfile.read())

def proc_teardown( ) :
    # FIXME TODO check a config/token flag to decide if to keep/delete work dir 
    shutil.rmtree( s_config.get_key( "sys/work_dir" )  )

    os.chdir( s_config.get_key( "/config/cwd" ) )

####################################################################

def compress( d ) :
    blob = gzip.compress( d )
    return( blob )

def decompress( d ) :
    blob = gzip.decompress( d )
    return( blob )


def parent_path( ) :

    for teil in inspect.stack():
        # skip system calls
        if teil[1].startswith("<"):
            continue
        if teil[1].upper().startswith(sys.exec_prefix.upper()):
            continue
        trc = teil[1]
        
    # trc contains highest level calling script name
    # check if we have been compiled
    if getattr(sys, 'frozen', False):
        scriptdir, scriptname = os.path.split(sys.executable)
        return {"dir": scriptdir,
                "name": scriptname,
                "source": trc}

    # from here on, we are in the interpreted case
    scriptdir, trc = os.path.split(trc)
    # if trc did not contain directory information,
    # the current working directory is what we need
    if not scriptdir:
        scriptdir = os.getcwd()

    scr_dict ={"name": trc,
               "source": trc,
               "dir": scriptdir}

    #s_log.write(scr_dict)

    return scr_dict["dir"]
    



