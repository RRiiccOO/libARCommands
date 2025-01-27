'''
    Copyright (C) 2014 Parrot SA

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in
      the documentation and/or other materials provided with the 
      distribution.
    * Neither the name of Parrot nor the names
      of its contributors may be used to endorse or promote products
      derived from this software without specific prior written
      permission.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
    OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED 
    AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
    OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.
'''
import sys
import os
import re

MYDIR=os.path.abspath(os.path.dirname(sys.argv[0]))
if '' == MYDIR:
    MYDIR=os.getcwd()

sys.path.append('%(MYDIR)s/../../ARSDKBuildUtils/Utils/Python' % locals())

from ARFuncs import *
from ARCommandsParser import *

LIB_NAME = 'libARCommands'
LIB_MODULE = LIB_NAME.replace ('lib', '')

#################################
# CONFIGURATION :               #
#################################
# Setup XML and C/HFiles Names  #
# Public header names must be   #
# LIB_NAME + '/fileName.h'      #
#################################

SDK_PACKAGE_ROOT='com.parrot.arsdk.'
JNI_PACKAGE_NAME=SDK_PACKAGE_ROOT + LIB_MODULE.lower ()
JNI_PACKAGE_DIR = JNI_PACKAGE_NAME.replace ('.', '/')

# Default project name
DEFAULTPROJECTNAME='common'

#Name of the output public header containing id enums
COMMANDSID_HFILE_NAME=LIB_NAME + '/ARCOMMANDS_Ids.h'

#Name of the output public header containing typedefs
COMMANDSTYPES_HFILE_NAME=LIB_NAME + '/ARCOMMANDS_Types.h'

#Name of the output public header containing encoder helpers
COMMANDSGEN_HFILE_NAME=LIB_NAME + '/ARCOMMANDS_Generator.h'

#Name of the output public header containing decoder helpers
COMMANDSDEC_HFILE_NAME=LIB_NAME + '/ARCOMMANDS_Decoder.h'

#Name of the output public header containing filter helpers
COMMANDSFIL_HFILE_NAME=LIB_NAME + '/ARCOMMANDS_Filter.h'

#Name of the output internal header containing reader/writer functions prototypes
COMMANDSRW_HFILE_NAME='ARCOMMANDS_ReadWrite.h'

#Name of the output C file containing reader/writer functions
COMMANDSRW_CFILE_NAME='ARCOMMANDS_ReadWrite.c'

#Name of the output C file containing encoder helpers
COMMANDSGEN_CFILE_NAME='ARCOMMANDS_Generator.c'

#Name of the output C file containing decoder helpers
COMMANDSDEC_CFILE_NAME='ARCOMMANDS_Decoder.c'

#Name of the output C file containing filter helpers
COMMANDSFIL_CFILE_NAME='ARCOMMANDS_Filter.c'

#Name of the output C/H common testbench file
TB_CFILE_NAME='autoTest.c'
TB_HFILE_NAME='autoTest.h'
#Tag for tb ARSAL_PRINT calls
TB_TAG='AutoTest'

#Name of the linux entry point file for autotest
TB_LIN_CFILE_NAME='autoTest_linux.c'

#Name of the JNI C File
JNI_CFILE_NAME='ARCOMMANDS_JNI.c'
JNI_FILTER_CFILE_NAME='ARCOMMANDS_JNIFilter.c'

#Name of the JNI JAVA File
JNI_JFILE_NAME='ARCommand.java'
JNIClassName, _ = os.path.splitext (JNI_JFILE_NAME)
JNI_FILTER_JFILE_NAME='ARCommandsFilter.java'
JNIFilterClassName, _ = os.path.splitext (JNI_FILTER_JFILE_NAME)

#Name of the JNI JAVA Interfaces files (DO NOT MODIFY)
JAVA_INTERFACES_FILES_NAME=JNIClassName + '*Listener.java'
JAVA_ENUM_FILES_NAME=JNIClassName.upper() + '*_ENUM.java'

#Relative path of SOURCE dir
SRC_DIR=MYDIR + '/../gen/Sources/'

#Relative path of INCLUDES dir
INC_DIR=MYDIR + '/../gen/Includes/'

#Relative path of TESTBENCH dir
TB__DIR=MYDIR + '/../gen/TestBench/'

#Relative path of unix-like (Linux / os-x) TESTBENCH dir
LIN_TB_DIR=TB__DIR + 'linux/'

#Relative path of multiplatform code for testbenches
COM_TB_DIR=TB__DIR + 'common/'

#Relative path of JNI dir
JNI_DIR=MYDIR + "/../gen/JNI/"

#Relative path of JNI/C dir
JNIC_DIR=JNI_DIR + 'c/'

#Relative path of JNI/Java dir
JNIJ_DIR=JNI_DIR + 'java/'
JNIJ_OUT_DIR=JNIJ_DIR + JNI_PACKAGE_DIR + '/'

##### END OF CONFIG #####

# Create array of generated files (so we can cleanup only our files)
GENERATED_FILES = []
COMMANDSID_HFILE=INC_DIR + COMMANDSID_HFILE_NAME
GENERATED_FILES.append (COMMANDSID_HFILE)
COMMANDSGEN_HFILE=INC_DIR + COMMANDSGEN_HFILE_NAME
GENERATED_FILES.append (COMMANDSGEN_HFILE)
COMMANDSTYPES_HFILE=INC_DIR + COMMANDSTYPES_HFILE_NAME
GENERATED_FILES.append (COMMANDSTYPES_HFILE)
COMMANDSGEN_CFILE=SRC_DIR + COMMANDSGEN_CFILE_NAME
GENERATED_FILES.append (COMMANDSGEN_CFILE)
COMMANDSDEC_HFILE=INC_DIR + COMMANDSDEC_HFILE_NAME
GENERATED_FILES.append (COMMANDSDEC_HFILE)
COMMANDSDEC_CFILE=SRC_DIR + COMMANDSDEC_CFILE_NAME
GENERATED_FILES.append (COMMANDSDEC_CFILE)
COMMANDSFIL_HFILE=INC_DIR + COMMANDSFIL_HFILE_NAME
GENERATED_FILES.append (COMMANDSFIL_HFILE)
COMMANDSFIL_CFILE=SRC_DIR + COMMANDSFIL_CFILE_NAME
GENERATED_FILES.append (COMMANDSFIL_CFILE)
COMMANDSRW_HFILE=SRC_DIR + COMMANDSRW_HFILE_NAME
GENERATED_FILES.append (COMMANDSRW_HFILE)
COMMANDSRW_CFILE=SRC_DIR + COMMANDSRW_CFILE_NAME
GENERATED_FILES.append (COMMANDSRW_CFILE)
TB_CFILE=COM_TB_DIR + TB_CFILE_NAME
GENERATED_FILES.append (TB_CFILE)
TB_HFILE=COM_TB_DIR + TB_HFILE_NAME
GENERATED_FILES.append (TB_HFILE)
TB_LIN_CFILE=LIN_TB_DIR + TB_LIN_CFILE_NAME
GENERATED_FILES.append (TB_LIN_CFILE)
JNI_CFILE=JNIC_DIR + JNI_CFILE_NAME
GENERATED_FILES.append (JNI_CFILE)
JNI_FILTER_CFILE=JNIC_DIR + JNI_FILTER_CFILE_NAME
GENERATED_FILES.append (JNI_FILTER_CFILE)
JNI_JFILE=JNIJ_OUT_DIR + JNI_JFILE_NAME
GENERATED_FILES.append (JNI_JFILE)
JNI_FILTER_JFILE=JNIJ_OUT_DIR + JNI_FILTER_JFILE_NAME
GENERATED_FILES.append (JNI_FILTER_JFILE)
JAVA_INTERFACES_FILES=JNIJ_OUT_DIR + JAVA_INTERFACES_FILES_NAME
JAVA_ENUM_FILES=JNIJ_OUT_DIR + JAVA_ENUM_FILES_NAME

# Create names for #ifndef _XXX_ statements in .h files
COMMANDSID_DEFINE='_' + COMMANDSID_HFILE_NAME.upper ().replace ('/', '_').replace ('.', '_') + '_'
COMMANDSDEC_DEFINE='_' + COMMANDSDEC_HFILE_NAME.upper ().replace ('/', '_').replace ('.', '_') + '_'
COMMANDSGEN_DEFINE='_' + COMMANDSGEN_HFILE_NAME.upper ().replace ('/', '_').replace ('.', '_') + '_'
COMMANDSTYPES_DEFINE='_' + COMMANDSTYPES_HFILE_NAME.upper ().replace ('/', '_').replace ('.', '_') + '_'
COMMANDSRW_DEFINE='_' + COMMANDSRW_HFILE_NAME.upper ().replace ('/', '_').replace ('.', '_') + '_'
COMMANDSFIL_DEFINE='_' + COMMANDSFIL_HFILE_NAME.upper ().replace ('/', '_').replace ('.', '_') + '_'
TB_DEFINE='_' + TB_HFILE_NAME.upper ().replace ('/', '_').replace ('.', '_') + '_'

# Submodules names
ID_SUBMODULE='ID'
GEN_SUBMODULE='Generator'
DEC_SUBMODULE='Decoder'
FIL_SUBMODULE='Filter'
RW_SUBMODULE='ReadWrite'
TB_SUBMODULE='Testbench'
JNI_SUBMODULE='JNI'
JNI_FILTER_SUBMODULE='JNI_FILTER'

#Type conversion from XML Defined types to many other types
# XML Defined types
XMLTYPES = ['u8',       'i8',
            'u16',      'i16',
            'u32',      'i32',
            'u64',      'i64',
            'float',    'double',
            'string']
# Equivalent C types
CTYPES   = ['uint8_t',  'int8_t',
            'uint16_t', 'int16_t',
            'uint32_t', 'int32_t',
            'uint64_t', 'int64_t',
            'float',    'double',
            'char *']
# Equivalent C types with const char *
CTYPES_WC = ['uint8_t',  'int8_t',
            'uint16_t', 'int16_t',
            'uint32_t', 'int32_t',
            'uint64_t', 'int64_t',
            'float',    'double',
            'const char *']
# Equivalent size for the Generator internal functions
SZETYPES = ['U8',       'U8',
            'U16',      'U16',
            'U32',      'U32',
            'U64',      'U64',
            'Float',    'Double',
            'String']
# Equivalent calls for the Decoder internal functions
CREADERS = [ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read8FromBuffer'),     ' (int8_t)' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read8FromBuffer'),
            ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read16FromBuffer'),    ' (int16_t)' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read16FromBuffer'),
            ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read32FromBuffer'),    ' (int32_t)' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read32FromBuffer'),
            ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read64FromBuffer'),    ' (int64_t)' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read64FromBuffer'),
            ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'ReadFloatFromBuffer'), ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'ReadDoubleFromBuffer'),
            ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'ReadStringFromBuffer')]

# Equivalent calls for the Decoder print internal functions
CPRINTERS = [ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU8'),    ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI8'),
             ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU16'),   ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI16'),
             ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU32'),   ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI32'),
             ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU64'),   ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI64'),
             ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintFloat'), ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintDouble'),
             ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintString')]

# Equivalent JAVA Types
# No unsigned types in java, so use signed types everywhere
JAVATYPES = ['byte',    'byte',
             'short',   'short',
             'int',     'int',
             'long',    'long',
             'float',   'double',
             'String']
# Equivalent JNI Signatures
JAVASIG   = ['B',        'B',
             'S',        'S',
             'I',        'I',
             'J',        'J',
             'F',        'D',
             'Ljava/lang/String;']
# Equivalent JNI types
JNITYPES  = ['jbyte',    'jbyte',
             'jshort',   'jshort',
             'jint',     'jint',
             'jlong',    'jlong',
             'jfloat',   'jdouble',
             'jstring']
# JNI UnsignedToSigned casts
JNIUTSCASTS = ['(jbyte)', '',
               '(jshort)', '',
               '(jint)', '',
               '(jlong)', '',
               '', '',
               '']

def xmlToC (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return AREnumName (LIB_MODULE, proj.name + '_' + cl.name, cmd.name + '_' + arg.name);
    xmlIndex = XMLTYPES.index (arg.type)
    return CTYPES [xmlIndex]

def xmlToCwithConst (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return AREnumName (LIB_MODULE, proj.name + '_' + cl.name, cmd.name + '_' + arg.name);
    xmlIndex = XMLTYPES.index (arg.type)
    return CTYPES_WC [xmlIndex]

def xmlToSize (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return 'U32';
    xmlIndex = XMLTYPES.index (arg.type)
    return SZETYPES [xmlIndex]

def xmlToReader (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return '(' + AREnumName (LIB_MODULE, proj.name + '_' + cl.name, cmd.name + '_' + arg.name) + ')' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read32FromBuffer')
    xmlIndex = XMLTYPES.index (arg.type)
    return CREADERS [xmlIndex]

def xmlToPrinter (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return '(' + AREnumName (LIB_MODULE, proj.name + '_' + cl.name, cmd.name + '_' + arg.name) + ')' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI32')
    xmlIndex = XMLTYPES.index (arg.type)
    return CPRINTERS [xmlIndex]

def xmlToJava (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return ARJavaEnumType (LIB_MODULE, proj.name + '_' + cl.name, cmd.name + '_' + arg.name)
    xmlIndex = XMLTYPES.index (arg.type)
    return JAVATYPES [xmlIndex]

def jniEnumClassName (proj, cl, cmd, arg):
    if arg.type != 'enum':
        return ''
    return JNI_PACKAGE_DIR + '/' + ARJavaEnumType (LIB_MODULE, proj.name + '_' + cl.name, cmd.name + '_' + arg.name)

def xmlToJavaSig (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return 'L' + jniEnumClassName (proj, cl, cmd, arg) + ';'
    xmlIndex = XMLTYPES.index (arg.type)
    return JAVASIG [xmlIndex]

def xmlToJni (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return 'jobject'
    xmlIndex = XMLTYPES.index (arg.type)
    return JNITYPES [xmlIndex]

def xmlToJniCast (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return '(jobject)'
    xmlIndex = XMLTYPES.index (arg.type)
    return JNIUTSCASTS [xmlIndex]

# Sample args for testbench
SAMPLEARGS = ['42',              '-42',
              '4200',            '-4200',
              '420000',          '-420000',
              '420102030405ULL', '-420102030405LL',
              '42.125',          '-42.000001',
              '"Test string with spaces"']
# Formatter for printf
PRINTFF    = ['%u',   '%d',
              '%u',   '%d',
              '%u',   '%d',
              '%llu', '%lld',
              '%f',   '%f',
              '%s']

def xmlToSample (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return '(' + AREnumName (LIB_MODULE, proj.name + '_' + cl.name, cmd.name + '_' + arg.name) + ')0';
    xmlIndex = XMLTYPES.index (arg.type)
    return SAMPLEARGS [xmlIndex]

def xmlToPrintf (proj, cl, cmd, arg):
    if 'enum' == arg.type:
        return '%d';
    xmlIndex = XMLTYPES.index (arg.type)
    return PRINTFF [xmlIndex]

LICENCE_HEADER='''/*
    Copyright (C) 2014 Parrot SA
    
    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met:
    * Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.
    * Neither the name of Parrot nor the names
    of its contributors may be used to endorse or promote products
    derived from this software without specific prior written
    permission.
    
    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
    LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
    FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
    COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
    INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
    BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
    OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
    AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
    OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGE.
*/
'''

noGen = False
genDebug = False
genTreeFilename = None
projects = [DEFAULTPROJECTNAME]
args = sys.argv
args.pop (0)
while len(args) > 0:
    a = args.pop (0)
    #################################
    # If "-fname" is passed as an   #
    # argument, just output the     #
    # name of the generated files   #
    #################################
    if a == "-fname":
        for fil in GENERATED_FILES:
            ARPrint (fil + ' ', True)
        ARPrint (JAVA_INTERFACES_FILES + ' ', True)
        ARPrint (JAVA_ENUM_FILES, True)
        ARPrint ('')
        EXIT (0)
    #################################
    # If "-dname" is passed as an   #
    # argument, just output the     #
    # name of the generated dirs    #
    #################################
    elif a == "-dname":
        ARPrint (SRC_DIR, True)
        ARPrint (INC_DIR + LIB_NAME, True)
        ARPrint (INC_DIR, True)
        ARPrint (LIN_TB_DIR, True)
        ARPrint (COM_TB_DIR, True)
        ARPrint (TB__DIR, True)
        ARPrint (JNIJ_OUT_DIR, True)
        ARPrint (JNIJ_DIR, True)
        ARPrint (JNIC_DIR, True)
        ARPrint (JNI_DIR)
        EXIT (0)
    #################################
    # If "-nogen" is passed as an   #
    # argument, don't generate any  #
    # file                          #
    #################################
    elif a == "-nogen":
        noGen=True
    #################################
    # If -projectname is specified, #
    # use its value to set the      #
    # project name instead of the   #
    # default one.                  #
    #################################
    elif a == "-projects":
        projectsList = args.pop(0)
        for project in projectsList.split(','):
            projects.append (project)
    #################################
    # If -debug-cmds is specified   #
    # and set to 'yes', generate    #
    # commands for _debug.xml files.#
    #################################
    elif a == "-debug-cmds":
        val = args.pop(0)
        if val == 'yes':
            genDebug = True
    #################################
    # If -gen-tree is specified,    #
    # generate a C structs tree     #
    # dump of Xml tree.             #
    #################################
    elif a == "-gen-tree":
        genTreeFilename = args.pop(0)
    elif a != "":
        print("Invalid parameter %s." %(a))

if not os.path.exists (SRC_DIR):
    os.makedirs (SRC_DIR)
if not os.path.exists (INC_DIR):
    os.makedirs (INC_DIR)
if not os.path.exists (INC_DIR + LIB_NAME):
    os.makedirs (INC_DIR + LIB_NAME)
if not os.path.exists (TB__DIR):
    os.makedirs (TB__DIR)
if not os.path.exists (LIN_TB_DIR):
    os.makedirs (LIN_TB_DIR)
if not os.path.exists (COM_TB_DIR):
    os.makedirs (COM_TB_DIR)
if not os.path.exists (JNI_DIR):
    os.makedirs (JNI_DIR)
if not os.path.exists (JNIC_DIR):
    os.makedirs (JNIC_DIR)
if not os.path.exists (JNIJ_OUT_DIR):
    os.makedirs (JNIJ_OUT_DIR)


#################################
# 1ST PART :                    #
#################################
# Read XML file to local arrays #
# of commands / classes         #
#################################

allProjects = parseAllProjects(projects, '%(MYDIR)s/..' % locals(), genDebug)

# Check all
err = ''
for proj in allProjects:
    err = err + proj.check ()
if len (err) > 0:
    ARPrint ('Your XML Files contain errors:', True)
    ARPrint (err)
    EXIT (1)

if noGen: # called with "-nogen"
    ARPrint ('Commands parsed:')
    for proj in allProjects:
        ARPrint ('Project ' + proj.name)
        ARPrint ('/*')
        for comment in proj.comments:
            ARPrint (' * ' + comment)
        ARPrint (' */')
        for cl in proj.classes:
            ARPrint ('-> ' + cl.name)
            ARPrint ('   /* ')
            for comment in cl.comments:
                ARPrint ('    * ' + comment)
            ARPrint ('    */')
            for cmd in cl.cmds:
                ARPrint (' --> ' + cmd.name)
                ARPrint ('     buffer:  ' + ARCommandBuffer.toString(cmd.buf))
                ARPrint ('     timeout: ' + ARCommandTimeoutPolicy.toString(cmd.timeout))
                ARPrint ('     list:    ' + ARCommandListType.toString(cmd.listtype))
                ARPrint ('     /* ')
                for comment in cmd.comments:
                    ARPrint ('      * ' + comment)
                ARPrint ('      */')
                for arg in cmd.args:
                    ARPrint ('   (' + arg.type + ' ' + arg.name + ')')
                    ARPrint ('    /* ')
                    for comment in arg.comments:
                        ARPrint ('     * ' + comment)
                    ARPrint ('     */')
                    for enum in arg.enums:
                        ARPrint ('   (typedef enum ' + enum.name + ')')
                        ARPrint ('    /* ')
                        for comment in enum.comments:
                            ARPrint ('     * ' + comment)
                        ARPrint ('     */')

    EXIT (0)


#################################
# 2ND PART :                    #
#################################
# Write private H files         #
#################################

hfile = open (COMMANDSID_HFILE, 'w')

hfile.write (LICENCE_HEADER)
hfile.write ('/********************************************\n')
hfile.write (' *            AUTOGENERATED FILE            *\n')
hfile.write (' *             DO NOT MODIFY IT             *\n')
hfile.write (' *                                          *\n')
hfile.write (' * To add new commands :                    *\n')
hfile.write (' *  - Modify ../Xml/commands.xml file       *\n')
hfile.write (' *  - Re-run generateCommandsList.py script *\n')
hfile.write (' *                                          *\n')
hfile.write (' ********************************************/\n')
hfile.write ('\n')
hfile.write ('#ifndef ' + COMMANDSID_DEFINE + '\n')
hfile.write ('#define ' + COMMANDSID_DEFINE + ' (1)\n')
hfile.write ('\n')
hfile.write ('// ARSDK_NO_ENUM_PREPROCESS //\n')
hfile.write ('typedef enum {\n')
for proj in allProjects:
    ENAME='PROJECT'
    hfile.write ('    ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, ENAME, proj.name) + ' = ' + proj.ident + ',\n')
hfile.write ('} ' + AREnumName (LIB_MODULE, ID_SUBMODULE, ENAME) + ';\n')
hfile.write ('\n')
hfile.write ('\n')
for proj in allProjects:
    if proj.classes:
        ENAME=proj.name + '_CLASS'
        hfile.write ('typedef enum {\n')
        for cl in proj.classes:
            hfile.write ('    ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, ENAME, cl.name) + ' = ' + cl.ident + ',\n')
        hfile.write ('} ' + AREnumName (LIB_MODULE, ID_SUBMODULE, ENAME) + ';\n')
        hfile.write ('\n')
hfile.write ('\n')
hfile.write ('\n')
for proj in allProjects:
    for cl in proj.classes:
        hfile.write ('typedef enum {\n')
        ENAME=proj.name + '_' + cl.name + '_CMD'
        first = True
        for cmd in cl.cmds:
            if first:
                hfile.write ('    ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, ENAME, cmd.name) + ' = 0,\n')
                first = False
            else:
                hfile.write ('    ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, ENAME, cmd.name) + ',\n')
        hfile.write ('    ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, ENAME, 'MAX') + ',\n')
        hfile.write ('} ' + AREnumName (LIB_MODULE, ID_SUBMODULE, ENAME) + ';\n')
        hfile.write ('\n')
    hfile.write ('\n')

hfile.write ('\n')
hfile.write ('#endif /* ' + COMMANDSID_DEFINE + ' */\n')

hfile.close ()

hfile = open(COMMANDSRW_HFILE, 'w')

hfile.write ('/********************************************\n')
hfile.write (' *            AUTOGENERATED FILE            *\n')
hfile.write (' *             DO NOT MODIFY IT             *\n')
hfile.write (' *                                          *\n')
hfile.write (' * To add new commands :                    *\n')
hfile.write (' *  - Modify ../Xml/commands.xml file       *\n')
hfile.write (' *  - Re-run generateCommandsList.py script *\n')
hfile.write (' *                                          *\n')
hfile.write (' ********************************************/\n')
hfile.write ('\n')
hfile.write ('#ifndef ' + COMMANDSRW_DEFINE + '\n')
hfile.write ('#define ' + COMMANDSRW_DEFINE + ' (1)\n')
hfile.write ('\n')
hfile.write ('#include <inttypes.h>\n')
hfile.write ('#include <string.h>\n')
hfile.write ('#include <stdlib.h>\n')
hfile.write ('\n')
hfile.write ('// ------- //\n')
hfile.write ('// WRITERS //\n')
hfile.write ('// ------- //\n')
hfile.write ('\n')
if hasArgOfType['u8'] or hasArgOfType['i8']:
    hfile.write ('// Add an 8 bit value to the buffer\n')
    hfile.write ('// Returns -1 if the buffer is not big enough\n')
    hfile.write ('// Returns the new offset in the buffer on success\n')
    hfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU8ToBuffer') + ' (uint8_t *buffer, uint8_t newVal, int32_t oldOffset, int32_t buffCap);\n')
    hfile.write ('\n')
if hasArgOfType['u16'] or hasArgOfType['i16']:
    hfile.write ('// Add a 16 bit value to the buffer\n')
    hfile.write ('// Returns -1 if the buffer is not big enough\n')
    hfile.write ('// Returns the new offset in the buffer on success\n')
    hfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU16ToBuffer') + ' (uint8_t *buffer, uint16_t newVal, int32_t oldOffset, int32_t buffCap);\n')
    hfile.write ('\n')
if hasArgOfType['u32'] or hasArgOfType['i32'] or hasArgOfType['float'] or hasArgOfType['enum']:
    hfile.write ('// Add a 32 bit value to the buffer\n')
    hfile.write ('// Returns -1 if the buffer is not big enough\n')
    hfile.write ('// Returns the new offset in the buffer on success\n')
    hfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU32ToBuffer') + ' (uint8_t *buffer, uint32_t newVal, int32_t oldOffset, int32_t buffCap);\n')
    hfile.write ('\n')
if hasArgOfType['u64'] or hasArgOfType['i64'] or hasArgOfType['double']:
    hfile.write ('// Add a 64 bit value to the buffer\n')
    hfile.write ('// Returns -1 if the buffer is not big enough\n')
    hfile.write ('// Returns the new offset in the buffer on success\n')
    hfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU64ToBuffer') + ' (uint8_t *buffer, uint64_t newVal, int32_t oldOffset, int32_t buffCap);\n')
    hfile.write ('\n')
if hasArgOfType['string']:
    hfile.write ('// Add a NULL Terminated String to the buffer\n')
    hfile.write ('// Returns -1 if the buffer is not big enough\n')
    hfile.write ('// Returns the new offset in the buffer on success\n')
    hfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddStringToBuffer') + ' (uint8_t *buffer, const char *newVal, int32_t oldOffset, int32_t buffCap);\n')
    hfile.write ('\n')
if hasArgOfType['float']:
    hfile.write ('// Add a float to the buffer\n')
    hfile.write ('// Returns -1 if the buffer is not big enough\n')
    hfile.write ('// Returns the new offset in the buffer on success\n')
    hfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddFloatToBuffer') + ' (uint8_t *buffer, float newVal, int32_t oldOffset, int32_t buffCap);\n')
    hfile.write ('\n')
if hasArgOfType['double']:
    hfile.write ('// Add a double to the buffer\n')
    hfile.write ('// Returns -1 if the buffer is not big enough\n')
    hfile.write ('// Returns the new offset in the buffer on success\n')
    hfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddDoubleToBuffer') + ' (uint8_t *buffer, double newVal, int32_t oldOffset, int32_t buffCap);\n')
    hfile.write ('\n')
hfile.write ('// ------- //\n')
hfile.write ('// READERS //\n')
hfile.write ('// ------- //\n')
hfile.write ('\n')
if hasArgOfType['u8'] or hasArgOfType['i8']:
    hfile.write ('// Read an 8 bit value from the buffer\n')
    hfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    hfile.write ('uint8_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read8FromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error);\n')
    hfile.write ('\n')
if hasArgOfType['u16'] or hasArgOfType['i16']:
    hfile.write ('// Read a 16 bit value from the buffer\n')
    hfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    hfile.write ('uint16_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read16FromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error);\n')
    hfile.write ('\n')
if hasArgOfType['u32'] or hasArgOfType['i32'] or hasArgOfType['enum']:
    hfile.write ('// Read a 32 bit value from the buffer\n')
    hfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    hfile.write ('uint32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read32FromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error);\n')
    hfile.write ('\n')
if hasArgOfType['u64'] or hasArgOfType['i64']:
    hfile.write ('// Read a 64 bit value from the buffer\n')
    hfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    hfile.write ('uint64_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read64FromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error);\n')
    hfile.write ('\n')
if hasArgOfType['float']:
    hfile.write ('// Read a float value from the buffer\n')
    hfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    hfile.write ('float ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'ReadFloatFromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error);\n')
    hfile.write ('\n')
if hasArgOfType['double']:
    hfile.write ('// Read a double value from the buffer\n')
    hfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    hfile.write ('double ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'ReadDoubleFromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error);\n')
    hfile.write ('\n')
if hasArgOfType['string']:
    hfile.write ('// Read a string value from the buffer\n')
    hfile.write ('// On error, return NULL and set *error to 1, else set *error to 0\n')
    hfile.write ('char* ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'ReadStringFromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error);\n')
    hfile.write ('\n')
hfile.write ('// -------- //\n')
hfile.write ('// TOSTRING //\n')
hfile.write ('// -------- //\n')
hfile.write ('\n')
if (hasArgOfType['u8']  or hasArgOfType['i8'] or
    hasArgOfType['u16'] or hasArgOfType['i16'] or
    hasArgOfType['u32'] or hasArgOfType['i32'] or
    hasArgOfType['u64'] or hasArgOfType['i64'] or
    hasArgOfType['float'] or hasArgOfType['double'] or
    hasArgOfType['string'] or hasArgOfType['enum']):
    hfile.write ('// Write a string in a buffer\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (const char *stringToWrite, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['u8']:
    hfile.write ('// Write a string in a buffer from an uint8_t arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU8') + ' (const char *name, uint8_t arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['i8']:
    hfile.write ('// Write a string in a buffer from an int8_t arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI8') + ' (const char *name, int8_t arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['u16']:
    hfile.write ('// Write a string in a buffer from an uint16_t arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU16') + ' (const char *name, uint16_t arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['i16']:
    hfile.write ('// Write a string in a buffer from an int16_t arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI16') + ' (const char *name, int16_t arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['u32']:
    hfile.write ('// Write a string in a buffer from an uint32_t arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU32') + ' (const char *name, uint32_t arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['i32'] or hasArgOfType['enum']:
    hfile.write ('// Write a string in a buffer from an int32_t arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI32') + ' (const char *name, int32_t arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['u64']:
    hfile.write ('// Write a string in a buffer from an uint64_t arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU64') + ' (const char *name, uint64_t arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['i64']:
    hfile.write ('// Write a string in a buffer from an int64_t arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI64') + ' (const char *name, int64_t arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['float']:
    hfile.write ('// Write a string in a buffer from float arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintFloat') + ' (const char *name, float arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['double']:
    hfile.write ('// Write a string in a buffer from a double arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintDouble') + ' (const char *name, double arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
if hasArgOfType['string']:
    hfile.write ('// Write a string in a buffer from a string arg\n')
    hfile.write ('// On error, return -1, else return offset in string\n')
    hfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintString') + ' (const char *name, char *arg, char *output, int outputLen, int outputOffset);\n')
    hfile.write ('\n')
  

hfile.write ('\n')
hfile.write ('#endif /* ' + COMMANDSRW_DEFINE + ' */\n')

hfile.close ()


#################################
# 3RD PART :                    #
#################################
# Generate private ReadWrite C  #
# file                          #
#################################

cfile = open (COMMANDSRW_CFILE, 'w')

cfile.write (LICENCE_HEADER)
cfile.write ('/********************************************\n')
cfile.write (' *            AUTOGENERATED FILE            *\n')
cfile.write (' *             DO NOT MODIFY IT             *\n')
cfile.write (' *                                          *\n')
cfile.write (' * To add new commands :                    *\n')
cfile.write (' *  - Modify ../Xml/commands.xml file       *\n')
cfile.write (' *  - Re-run generateCommandsList.py script *\n')
cfile.write (' *                                          *\n')
cfile.write (' ********************************************/\n')
cfile.write ('#include <config.h>\n')
cfile.write ('#include <stdio.h>\n')
cfile.write ('#include "' + COMMANDSRW_HFILE_NAME + '"\n')
cfile.write ('#include <libARSAL/ARSAL_Endianness.h>\n')
cfile.write ('\n')
cfile.write ('// ------- //\n')
cfile.write ('// WRITERS //\n')
cfile.write ('// ------- //\n')
cfile.write ('\n')
if hasArgOfType['u8'] or hasArgOfType['i8']:
    cfile.write ('// Add an 8 bit value to the buffer\n')
    cfile.write ('// Returns -1 if the buffer is not big enough\n')
    cfile.write ('// Returns the new offset in the buffer on success\n')
    cfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU8ToBuffer') + ' (uint8_t *buffer, uint8_t newVal, int32_t oldOffset, int32_t buffCap)\n')
    cfile.write ('{\n')
    cfile.write ('    int32_t retVal = 0;\n')
    cfile.write ('    if (buffCap < (oldOffset + sizeof (newVal)))\n')
    cfile.write ('    {\n')
    cfile.write ('        retVal = -1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        uint8_t *buffptr = &(buffer [oldOffset]);\n')
    cfile.write ('        uint8_t localVal = newVal;\n')
    cfile.write ('        memcpy (buffptr, &localVal, sizeof (localVal));\n')
    cfile.write ('        retVal = oldOffset + sizeof (localVal);\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['u16'] or hasArgOfType['i16']:
    cfile.write ('// Add a 16 bit value to the buffer\n')
    cfile.write ('// Returns -1 if the buffer is not big enough\n')
    cfile.write ('// Returns the new offset in the buffer on success\n')
    cfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU16ToBuffer') + ' (uint8_t *buffer, uint16_t newVal, int32_t oldOffset, int32_t buffCap)\n')
    cfile.write ('{\n')
    cfile.write ('    int32_t retVal = 0;\n')
    cfile.write ('    if (buffCap < (oldOffset + sizeof (newVal)))\n')
    cfile.write ('    {\n')
    cfile.write ('        retVal = -1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        uint16_t *buffptr = (uint16_t *)& (buffer [oldOffset]);\n')
    cfile.write ('        uint16_t localVal = htods (newVal);\n')
    cfile.write ('        memcpy (buffptr, &localVal, sizeof (localVal));\n')
    cfile.write ('        retVal = oldOffset + sizeof (localVal);\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['u32'] or hasArgOfType['i32'] or hasArgOfType['float'] or hasArgOfType['enum']:
    cfile.write ('// Add a 32 bit value to the buffer\n')
    cfile.write ('// Returns -1 if the buffer is not big enough\n')
    cfile.write ('// Returns the new offset in the buffer on success\n')
    cfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU32ToBuffer') + ' (uint8_t *buffer, uint32_t newVal, int32_t oldOffset, int32_t buffCap)\n')
    cfile.write ('{\n')
    cfile.write ('    int32_t retVal = 0;\n')
    cfile.write ('    if (buffCap < (oldOffset + sizeof (newVal)))\n')
    cfile.write ('    {\n')
    cfile.write ('        retVal = -1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        uint32_t *buffptr = (uint32_t *)& (buffer [oldOffset]);\n')
    cfile.write ('        uint32_t localVal = htodl (newVal);\n')
    cfile.write ('        memcpy (buffptr, &localVal, sizeof (localVal));\n')
    cfile.write ('        retVal = oldOffset + sizeof (localVal);\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['u64'] or hasArgOfType['i64'] or hasArgOfType['double']:
    cfile.write ('// Add a 64 bit value to the buffer\n')
    cfile.write ('// Returns -1 if the buffer is not big enough\n')
    cfile.write ('// Returns the new offset in the buffer on success\n')
    cfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU64ToBuffer') + ' (uint8_t *buffer, uint64_t newVal, int32_t oldOffset, int32_t buffCap)\n')
    cfile.write ('{\n')
    cfile.write ('    int32_t retVal = 0;\n')
    cfile.write ('    if (buffCap < (oldOffset + sizeof (newVal)))\n')
    cfile.write ('    {\n')
    cfile.write ('        retVal = -1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        uint64_t *buffptr = (uint64_t *)& (buffer [oldOffset]);\n')
    cfile.write ('        uint64_t localVal = htodll (newVal);\n')
    cfile.write ('        memcpy (buffptr, &localVal, sizeof (localVal));\n')
    cfile.write ('        retVal = oldOffset + sizeof (localVal);\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['string']:
    cfile.write ('// Add a NULL Terminated String to the buffer\n')
    cfile.write ('// Returns -1 if the buffer is not big enough\n')
    cfile.write ('// Returns the new offset in the buffer on success\n')
    cfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddStringToBuffer') + ' (uint8_t *buffer, const char *newVal, int32_t oldOffset, int32_t buffCap)\n')
    cfile.write ('{\n')
    cfile.write ('    int32_t retVal = 0;\n')
    cfile.write ('    if (buffCap < (oldOffset + strlen (newVal) + 1))\n')
    cfile.write ('    {\n')
    cfile.write ('        retVal = -1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        char *buffptr = (char *)& (buffer [oldOffset]);\n')
    cfile.write ('        strcpy (buffptr, newVal);\n')
    cfile.write ('        retVal = oldOffset + strlen (newVal) + 1;\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['float']:
    cfile.write ('// Add a float to the buffer\n')
    cfile.write ('// Returns -1 if the buffer is not big enough\n')
    cfile.write ('// Returns the new offset in the buffer on success\n')
    cfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddFloatToBuffer') + ' (uint8_t *buffer, float newVal, int32_t oldOffset, int32_t buffCap)\n')
    cfile.write ('{\n')
    cfile.write ('    return ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU32ToBuffer') + ' (buffer, * (uint32_t *)&newVal, oldOffset, buffCap);\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['double']:
    cfile.write ('// Add a double to the buffer\n')
    cfile.write ('// Returns -1 if the buffer is not big enough\n')
    cfile.write ('// Returns the new offset in the buffer on success\n')
    cfile.write ('int32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddDoubleToBuffer') + ' (uint8_t *buffer, double newVal, int32_t oldOffset, int32_t buffCap)\n')
    cfile.write ('{\n')
    cfile.write ('    return ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU64ToBuffer') + ' (buffer, * (uint64_t *)&newVal, oldOffset, buffCap);\n')
    cfile.write ('}\n')
    cfile.write ('\n')
cfile.write ('// ------- //\n')
cfile.write ('// READERS //\n')
cfile.write ('// ------- //\n')
cfile.write ('\n')
if hasArgOfType['u8'] or hasArgOfType['i8']:
    cfile.write ('// Read an 8 bit value from the buffer\n')
    cfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    cfile.write ('uint8_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read8FromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    uint8_t retVal = 0;\n')
    cfile.write ('    int newOffset = *offset + sizeof (uint8_t);\n')
    cfile.write ('    if (newOffset > capacity)\n')
    cfile.write ('    {\n')
    cfile.write ('        *error = 1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        retVal = buffer [*offset];\n')
    cfile.write ('        *offset = newOffset;\n')
    cfile.write ('        *error = 0;\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['u16'] or hasArgOfType['i16']:
    cfile.write ('// Read a 16 bit value from the buffer\n')
    cfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    cfile.write ('uint16_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read16FromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    uint16_t retVal = 0;\n')
    cfile.write ('    uint8_t *buffAddr = &buffer[*offset];\n')
    cfile.write ('    int newOffset = *offset + sizeof (uint16_t);\n')
    cfile.write ('    if (newOffset > capacity)\n')
    cfile.write ('    {\n')
    cfile.write ('        *error = 1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        memcpy (&retVal, buffAddr, sizeof (uint16_t));\n')
    cfile.write ('        retVal = dtohs (retVal);\n')
    cfile.write ('        *offset = newOffset;\n')
    cfile.write ('        *error = 0;\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['u32'] or hasArgOfType['i32'] or hasArgOfType['enum']:
    cfile.write ('// Read a 32 bit value from the buffer\n')
    cfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    cfile.write ('uint32_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read32FromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    uint32_t retVal = 0;\n')
    cfile.write ('    uint8_t *buffAddr = &buffer[*offset];\n')
    cfile.write ('    int newOffset = *offset + sizeof (uint32_t);\n')
    cfile.write ('    if (newOffset > capacity)\n')
    cfile.write ('    {\n')
    cfile.write ('        *error = 1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        memcpy (&retVal, buffAddr, sizeof (uint32_t));\n')
    cfile.write ('        retVal = dtohl (retVal);\n')
    cfile.write ('        *offset = newOffset;\n')
    cfile.write ('        *error = 0;\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['u64'] or hasArgOfType['i64']:
    cfile.write ('// Read a 64 bit value from the buffer\n')
    cfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    cfile.write ('uint64_t ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read64FromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    uint64_t retVal = 0;\n')
    cfile.write ('    uint8_t *buffAddr = &buffer[*offset];\n')
    cfile.write ('    int newOffset = *offset + sizeof (uint64_t);\n')
    cfile.write ('    if (newOffset > capacity)\n')
    cfile.write ('    {\n')
    cfile.write ('        *error = 1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        memcpy (&retVal, buffAddr, sizeof (uint64_t));\n')
    cfile.write ('        retVal = dtohll (retVal);\n')
    cfile.write ('        *offset = newOffset;\n')
    cfile.write ('        *error = 0;\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['float']:
    cfile.write ('// Read a float value from the buffer\n')
    cfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    cfile.write ('float ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'ReadFloatFromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    float retVal = 0;\n')
    cfile.write ('    uint8_t *buffAddr = &buffer[*offset];\n')
    cfile.write ('    int newOffset = *offset + sizeof (float);\n')
    cfile.write ('    if (newOffset > capacity)\n')
    cfile.write ('    {\n')
    cfile.write ('        *error = 1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        memcpy (&retVal, buffAddr, sizeof (float));\n')
    cfile.write ('        retVal = dtohf (retVal);\n')
    cfile.write ('        *offset = newOffset;\n')
    cfile.write ('        *error = 0;\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['double']:
    cfile.write ('// Read a double value from the buffer\n')
    cfile.write ('// On error, return zero and set *error to 1, else set *error to 0\n')
    cfile.write ('double ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'ReadDoubleFromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    double retVal = 0;\n')
    cfile.write ('    uint8_t *buffAddr = &buffer[*offset];\n')
    cfile.write ('    int newOffset = *offset + sizeof (double);\n')
    cfile.write ('    if (newOffset > capacity)\n')
    cfile.write ('    {\n')
    cfile.write ('        *error = 1;\n')
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        memcpy (&retVal, buffAddr, sizeof (double));\n')
    cfile.write ('        retVal = dtohd (retVal);\n')
    cfile.write ('        *offset = newOffset;\n')
    cfile.write ('        *error = 0;\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['string']:
    cfile.write ('// Read a string value from the buffer\n')
    cfile.write ('// On error, return NULL and set *error to 1, else set *error to 0\n')
    cfile.write ('char* ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'ReadStringFromBuffer') + ' (uint8_t *buffer, int32_t capacity, int32_t *offset, int32_t *error)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    char *retVal = NULL;\n')
    cfile.write ('    char *buffAddr = (char *)&buffer[*offset];\n')
    cfile.write ('    int newOffset = *offset;\n')
    cfile.write ('    while ((newOffset < capacity) && (\'\\0\' != (char) buffer [newOffset]))\n')
    cfile.write ('    {\n')
    cfile.write ('        newOffset += sizeof (char);\n');
    cfile.write ('    }\n')
    cfile.write ('    if (newOffset >= capacity)\n')
    cfile.write ('    {\n')
    cfile.write ('        *error = 1;\n');
    cfile.write ('    }\n')
    cfile.write ('    else\n')
    cfile.write ('    {\n')
    cfile.write ('        retVal = buffAddr;\n')
    cfile.write ('        *offset = newOffset + 1;\n')
    cfile.write ('        *error = 0;\n')
    cfile.write ('    }\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
cfile.write ('// -------- //\n')
cfile.write ('// TOSTRING //\n')
cfile.write ('// -------- //\n')
cfile.write ('\n')
if (hasArgOfType['u8']  or hasArgOfType['i8'] or
    hasArgOfType['u16'] or hasArgOfType['i16'] or
    hasArgOfType['u32'] or hasArgOfType['i32'] or
    hasArgOfType['u64'] or hasArgOfType['i64'] or
    hasArgOfType['float'] or hasArgOfType['double'] or
    hasArgOfType['string'] or hasArgOfType['enum']):
    cfile.write ('// Write a string in a buffer\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (const char *stringToWrite, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int retVal = -1;\n')
    cfile.write ('    int capacity = outputLen - outputOffset - 1;\n')
    cfile.write ('    int len = strlen (stringToWrite);\n')
    cfile.write ('    if (capacity >= len)\n')
    cfile.write ('    {\n')
    cfile.write ('        strncat (output, stringToWrite, len);\n')
    cfile.write ('        retVal = outputOffset + len;\n')
    cfile.write ('    } // No else --> If capacity is not enough, keep retVal to -1\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['u8']:
    cfile.write ('// Write a string in a buffer from an uint8_t arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU8') + ' (const char *name, uint8_t arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int capacity, len;\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    int retVal = -1;\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        capacity = outputLen - offset - 1;\n')
    cfile.write ('#if HAVE_DECL_PRIU8\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%" PRIu8, arg);\n')
    cfile.write ('#else\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%u", arg);\n')
    cfile.write ('#endif\n')
    cfile.write ('        if (len >= capacity)\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = -1;\n')
    cfile.write ('        }\n')
    cfile.write ('        else\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = offset + len;\n')
    cfile.write ('        }\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['i8']:
    cfile.write ('// Write a string in a buffer from an int8_t arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI8') + ' (const char *name, int8_t arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int capacity, len;\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    int retVal = -1;\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        capacity = outputLen - offset - 1;\n')
    cfile.write ('#if HAVE_DECL_PRII8\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%" PRIi8, arg);\n')
    cfile.write ('#else\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%d", arg);\n')
    cfile.write ('#endif\n')
    cfile.write ('        if (len >= capacity)\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = -1;\n')
    cfile.write ('        }\n')
    cfile.write ('        else\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = offset + len;\n')
    cfile.write ('        }\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['u16']:
    cfile.write ('// Write a string in a buffer from an uint16_t arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU16') + ' (const char *name, uint16_t arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int capacity, len;\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    int retVal = -1;\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        capacity = outputLen - offset - 1;\n')
    cfile.write ('#if HAVE_DECL_PRIU16\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%" PRIu16, arg);\n')
    cfile.write ('#else\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%u", arg);\n')
    cfile.write ('#endif\n')
    cfile.write ('        if (len >= capacity)\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = -1;\n')
    cfile.write ('        }\n')
    cfile.write ('        else\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = offset + len;\n')
    cfile.write ('        }\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['i16']:
    cfile.write ('// Write a string in a buffer from an int16_t arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI16') + ' (const char *name, int16_t arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int capacity, len;\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    int retVal = offset;\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        capacity = outputLen - offset - 1;\n')
    cfile.write ('#if HAVE_DECL_PRII16\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%" PRIi16, arg);\n')
    cfile.write ('#else\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%d", arg);\n')
    cfile.write ('#endif\n')
    cfile.write ('        if (len >= capacity)\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = -1;\n')
    cfile.write ('        }\n')
    cfile.write ('        else\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = offset + len;\n')
    cfile.write ('        }\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['u32']:
    cfile.write ('// Write a string in a buffer from an uint32_t arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU32') + ' (const char *name, uint32_t arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int capacity, len;\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    int retVal = offset;\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        capacity = outputLen - offset - 1;\n')
    cfile.write ('#if HAVE_DECL_PRIU32\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%" PRIu32, arg);\n')
    cfile.write ('#else\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%u", arg);\n')
    cfile.write ('#endif\n')
    cfile.write ('        if (len >= capacity)\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = -1;\n')
    cfile.write ('        }\n')
    cfile.write ('        else\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = offset + len;\n')
    cfile.write ('        }\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['i32'] or hasArgOfType['enum']:
    cfile.write ('// Write a string in a buffer from an int32_t arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI32') + ' (const char *name, int32_t arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int capacity, len;\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    int retVal = offset;\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        capacity = outputLen - offset - 1;\n')
    cfile.write ('#if HAVE_DECL_PRII32\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%" PRIi32, arg);\n')
    cfile.write ('#else\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%d", arg);\n')
    cfile.write ('#endif\n')
    cfile.write ('        if (len >= capacity)\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = -1;\n')
    cfile.write ('        }\n')
    cfile.write ('        else\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = offset + len;\n')
    cfile.write ('        }\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['u64']:
    cfile.write ('// Write a string in a buffer from an uint64_t arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintU64') + ' (const char *name, uint64_t arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int capacity, len;\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    int retVal = offset;\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        capacity = outputLen - offset - 1;\n')
    cfile.write ('#if HAVE_DECL_PRIU64\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%" PRIu64, arg);\n')
    cfile.write ('#else\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%llu", arg);\n')
    cfile.write ('#endif\n')
    cfile.write ('        if (len >= capacity)\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = -1;\n')
    cfile.write ('        }\n')
    cfile.write ('        else\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = offset + len;\n')
    cfile.write ('        }\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['i64']:
    cfile.write ('// Write a string in a buffer from an int64_t arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintI64') + ' (const char *name, int64_t arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int capacity, len;\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    int retVal = offset;\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        capacity = outputLen - offset - 1;\n')
    cfile.write ('#if HAVE_DECL_PRII64\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%" PRIi64, arg);\n')
    cfile.write ('#else\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%lld", arg);\n')
    cfile.write ('#endif\n')
    cfile.write ('        if (len >= capacity)\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = -1;\n')
    cfile.write ('        }\n')
    cfile.write ('        else\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = offset + len;\n')
    cfile.write ('        }\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['float']:
    cfile.write ('// Write a string in a buffer from float arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintFloat') + ' (const char *name, float arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int capacity, len;\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    int retVal = offset;\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        capacity = outputLen - offset - 1;\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%f", arg);\n')
    cfile.write ('        if (len >= capacity)\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = -1;\n')
    cfile.write ('        }\n')
    cfile.write ('        else\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = offset + len;\n')
    cfile.write ('        }\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['double']:
    cfile.write ('// Write a string in a buffer from a double arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintDouble') + ' (const char *name, double arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int capacity, len;\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    int retVal = offset;\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        capacity = outputLen - offset - 1;\n')
    cfile.write ('        len = snprintf (& output [offset], capacity, "%f", arg);\n')
    cfile.write ('        if (len >= capacity)\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = -1;\n')
    cfile.write ('        }\n')
    cfile.write ('        else\n')
    cfile.write ('        {\n')
    cfile.write ('            retVal = offset + len;\n')
    cfile.write ('        }\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return retVal;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
if hasArgOfType['string']:
    cfile.write ('// Write a string in a buffer from a string arg\n')
    cfile.write ('// On error, return -1, else return offset in string\n')
    cfile.write ('int ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'PrintString') + ' (const char *name, char *arg, char *output, int outputLen, int outputOffset)\n')
    cfile.write ('{\n')
    cfile.write ('    // We don\'t check args because this function is only called by autogenerated code\n')
    cfile.write ('    int offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (name, output, outputLen, outputOffset);\n')
    cfile.write ('    if (offset >= 0)\n')
    cfile.write ('    {\n')
    cfile.write ('        offset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' (arg, output, outputLen, offset);\n')
    cfile.write ('    } // No else --> Do nothing if the previous WriteString failed\n')
    cfile.write ('    return offset;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
cfile.close ()

#################################
# 4TH PART :                    #
#################################
# Generate public Types H file  #
#################################

hfile = open (COMMANDSTYPES_HFILE, 'w')

hfile.write ('/**\n')
hfile.write (' * @file ' + COMMANDSTYPES_HFILE_NAME + '\n')
hfile.write (' * @brief libARCommands types header.\n')
hfile.write (' * This file contains all types declarations needed to use commands\n')
hfile.write (' * @note Autogenerated file\n')
hfile.write (' **/\n')
hfile.write ('#ifndef ' + COMMANDSTYPES_DEFINE + '\n')
hfile.write ('#define ' + COMMANDSTYPES_DEFINE + '\n')
hfile.write ('#include <inttypes.h>\n')
hfile.write ('\n')
hfile.write ('/**\n')
hfile.write (' * @brief Size of the ARCommands header.\n')
hfile.write (' * This is the minimum size of a zero-arg command.\n')
hfile.write (' * The size of a command is equal to this, plus the size\n')
hfile.write (' * of its arguments.\n')
hfile.write (' */\n')
hfile.write ('#define ' + ARMacroName (LIB_MODULE, 'HEADER', 'SIZE') + ' (4)\n')
hfile.write ('\n')

if genDebug:
    hfile.write ('/**\n')
    hfile.write (' * Defined only if the library includes debug commands\n')
    hfile.write (' */\n')
    hfile.write ('#define ' + ARMacroName (LIB_MODULE, 'HAS', 'DEBUG_COMMANDS') + ' (1)\n')
    hfile.write ('\n')

for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            for arg in cmd.args:
                if len(arg.enums) != 0:
                    hfile.write ('// Project ' + proj.name + '\n')
                    hfile.write ('// Class ' + cl.name + '\n')
                    hfile.write ('// Command ' + cmd.name + '\n')

                    submodules=proj.name.upper() + '_' + cl.name.upper()
                    macro_name=cmd.name.upper() + '_' + arg.name.upper();
                    hfile.write ('\n/**\n')
                    hfile.write (' * @brief ' + arg.comments[0] + '\n')
                    for comm in arg.comments[1:]:
                        hfile.write (' * ' + comm + '\n')
                    hfile.write (' */\n')
                    hfile.write ('typedef enum\n')
                    hfile.write ('{\n')
                    first = True
                    for enum in arg.enums:
                        if first:
                            hfile.write ('    ' + AREnumValue (LIB_MODULE, submodules, macro_name, enum.name) + ' = 0,    ///< ' + enum.comments[0] + '\n')
                            first = False
                        else:
                            hfile.write ('    ' + AREnumValue (LIB_MODULE, submodules, macro_name, enum.name) + ',    ///< ' + enum.comments[0] + '\n')
                    hfile.write ('    ' + AREnumValue (LIB_MODULE, submodules, macro_name, 'MAX') + '\n')
                    hfile.write ('} ' + AREnumName (LIB_MODULE, submodules, macro_name) + ';\n\n')
hfile.write ('\n')
hfile.write ('#endif /* ' + COMMANDSTYPES_DEFINE + ' */\n')

hfile.close ()

#################################
# 5TH PART :                    #
#################################
# Generate public coder H file  #
#################################

hfile = open (COMMANDSGEN_HFILE, 'w')

hfile.write (LICENCE_HEADER)
hfile.write ('/**\n')
hfile.write (' * @file ' + COMMANDSGEN_HFILE_NAME + '\n')
hfile.write (' * @brief libARCommands generator header.\n')
hfile.write (' * This file contains all declarations needed to generate commands\n')
hfile.write (' * @note Autogenerated file\n')
hfile.write (' **/\n')
hfile.write ('#ifndef ' + COMMANDSGEN_DEFINE + '\n')
hfile.write ('#define ' + COMMANDSGEN_DEFINE + '\n')
hfile.write ('#include <' + COMMANDSTYPES_HFILE_NAME + '>\n')
hfile.write ('#include <inttypes.h>\n')
hfile.write ('\n')
hfile.write ('\n')
hfile.write ('/**\n')
hfile.write (' * @brief Error codes for ' + ARFunctionName (LIB_MODULE, GEN_SUBMODULE, 'GenerateClassCommand') + ' functions\n')
hfile.write (' */\n')
GEN_ERR_ENAME='ERROR'
hfile.write ('typedef enum {\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'OK') + ' = 0, ///< No error occured\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'BAD_ARGS') + ', ///< At least one of the arguments is invalid\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'NOT_ENOUGH_SPACE') + ', ///< The given output buffer was not large enough for the command\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'ERROR') + ', ///< Any other error\n')
hfile.write ('} ' +  AREnumName (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + ';\n')
hfile.write ('\n')
hfile.write ('\n')
for proj in allProjects:
    hfile.write ('// Project ' + proj.name + '\n\n')
    for cl in proj.classes:
        hfile.write ('// Command class ' + cl.name + '\n')
        for cmd in cl.cmds:
            hfile.write ('\n/**\n')
            hfile.write (' * @brief ' + cmd.comments[0] + '\n')
            for comm in cmd.comments[1:]:
                hfile.write (' * ' + comm + '\n')
            hfile.write (' * @warning A command is not NULL terminated and can contain NULL bytes.\n')
            hfile.write (' * @param buffer Pointer to the buffer in which the library should store the command\n')
            hfile.write (' * @param buffLen Size of the buffer\n')
            hfile.write (' * @param cmdLen Pointer to an integer that will hold the actual size of the command\n')
            for arg in cmd.args:
                for comm in arg.comments:
                    hfile.write (' * @param _' + arg.name + ' ' + comm + '\n')
            hfile.write (' * @return Error code (see ' + AREnumName (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + ')\n')
            hfile.write (' */\n')
            hfile.write (AREnumName (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + ' ' + ARFunctionName (LIB_MODULE, GEN_SUBMODULE, 'Generate' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name)) + ' (uint8_t *buffer, int32_t buffLen, int32_t *cmdLen')
            for arg in cmd.args:
                hfile.write (', ' + xmlToCwithConst (proj, cl, cmd, arg) + ' _' + arg.name)
            hfile.write (');\n')
        hfile.write ('\n')
    hfile.write ('\n')

hfile.write ('\n')
hfile.write ('#endif /* ' + COMMANDSGEN_DEFINE + ' */\n')

hfile.close ()

#################################
# 6TH PART :                    #
#################################
# Generate coder C part         #
#################################

cfile = open (COMMANDSGEN_CFILE, 'w')

cfile.write (LICENCE_HEADER)
cfile.write ('/********************************************\n')
cfile.write (' *            AUTOGENERATED FILE            *\n')
cfile.write (' *             DO NOT MODIFY IT             *\n')
cfile.write (' *                                          *\n')
cfile.write (' * To add new commands :                    *\n')
cfile.write (' *  - Modify ../Xml/commands.xml file       *\n')
cfile.write (' *  - Re-run generateCommandsList.py script *\n')
cfile.write (' *                                          *\n')
cfile.write (' ********************************************/\n')
cfile.write ('#include <config.h>\n')
cfile.write ('#include "' + COMMANDSRW_HFILE_NAME + '"\n')
cfile.write ('#include <' + COMMANDSTYPES_HFILE_NAME + '>\n')
cfile.write ('#include <' + COMMANDSGEN_HFILE_NAME + '>\n')
cfile.write ('#include <' + COMMANDSID_HFILE_NAME + '>\n')
cfile.write ('\n')

for proj in allProjects:
    cfile.write ('// Project ' + proj.name + '\n\n')
    for cl in proj.classes:
        cfile.write ('// Command class ' + cl.name + '\n')
        for cmd in cl.cmds:
            cfile.write (AREnumName (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + ' ' + ARFunctionName (LIB_MODULE, GEN_SUBMODULE, 'Generate' +  ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name)) + ' (uint8_t *buffer, int32_t buffLen, int32_t *cmdLen')
            for arg in cmd.args:
                cfile.write (', ' + xmlToCwithConst (proj, cl, cmd, arg) + ' _' + arg.name)
            cfile.write (')\n')
            cfile.write ('{\n')
            cfile.write ('    int32_t currIndexInBuffer = 0;\n')
            cfile.write ('    ' + AREnumName (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + ' retVal = ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'OK') + ';\n')
            cfile.write ('    if ((buffer == NULL) ||\n')
            cfile.write ('        (cmdLen == NULL))\n')
            cfile.write ('    {\n')
            cfile.write ('        return ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'BAD_ARGS') + ';\n')
            cfile.write ('    } // No else --> Args Check\n')
            hasStringArgs = False
            for arg in cmd.args:
                if arg.type == 'string':
                    hasStringArgs = True
                    break
            if hasStringArgs:
                cfile.write ('    // Test all String args (if any)\n')
                cfile.write ('    if (')
                first = True
                for arg in cmd.args:
                    if 'string' == arg.type:
                        if first:
                            first = False
                        else:
                            cfile.write ('        ')
                        cfile.write ('(_' + arg.name + ' == NULL) ||\n')
                cfile.write ('       (0))\n')
                cfile.write ('    {\n')
                cfile.write ('        return ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'BAD_ARGS') + ';\n')
                cfile.write ('    } // No else --> Args Check\n')
                cfile.write ('\n')
            cfile.write ('    // Write project header\n')
            cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'OK') + ')\n')
            cfile.write ('    {\n')
            cfile.write ('        currIndexInBuffer = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU8ToBuffer') + ' (buffer, ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, 'PROJECT', proj.name) + ', currIndexInBuffer, buffLen);\n')
            cfile.write ('        if (currIndexInBuffer == -1)\n')
            cfile.write ('        {\n')
            cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'NOT_ENOUGH_SPACE') + ';\n')
            cfile.write ('        } // No else --> Do not modify retVal if no issue was found\n')
            cfile.write ('    } // No else --> Processing block\n')
            cfile.write ('    // Write class header\n')
            cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'OK') + ')\n')
            cfile.write ('    {\n')
            cfile.write ('        currIndexInBuffer = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU8ToBuffer') + ' (buffer, ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_CLASS', cl.name) + ', currIndexInBuffer, buffLen);\n')
            cfile.write ('        if (currIndexInBuffer == -1)\n')
            cfile.write ('        {\n')
            cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'NOT_ENOUGH_SPACE') + ';\n')
            cfile.write ('        } // No else --> Do not modify retVal if no issue was found\n')
            cfile.write ('    } // No else --> Processing block\n')
            cfile.write ('    // Write id header\n')
            cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'OK') + ')\n')
            cfile.write ('    {\n')
            cfile.write ('        currIndexInBuffer = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'AddU16ToBuffer') + ' (buffer, ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_' + cl.name + '_CMD', cmd.name) + ', currIndexInBuffer, buffLen);\n')
            cfile.write ('        if (currIndexInBuffer == -1)\n')
            cfile.write ('        {\n')
            cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'NOT_ENOUGH_SPACE') + ';\n')
            cfile.write ('        } // No else --> Do not modify retVal if no issue was found\n')
            cfile.write ('    } // No else --> Processing block\n')
            for arg in cmd.args:
                cfile.write ('    // Write arg _' + arg.name + '\n')
                cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'OK') + ')\n')
                cfile.write ('    {\n')
                cfile.write ('        currIndexInBuffer = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Add' + xmlToSize (proj, cl, cmd, arg) + 'ToBuffer') + ' (buffer, _' + arg.name + ', currIndexInBuffer, buffLen);\n')
                cfile.write ('        if (currIndexInBuffer == -1)\n')
                cfile.write ('        {\n')
                cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'NOT_ENOUGH_SPACE') + ';\n')
                cfile.write ('        } // No else --> Do not modify retVal if no issue was found\n')
                cfile.write ('    } // No else --> Processing block\n')
            cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'OK') + ')\n')
            cfile.write ('    {\n')
            cfile.write ('        *cmdLen = currIndexInBuffer;\n')
            cfile.write ('    } // No else --> Do not set cmdLen if an error occured\n')
            cfile.write ('    return retVal;\n')
            cfile.write ('}\n\n')
        cfile.write ('\n')
    cfile.write ('\n')

cfile.write ('\n')
cfile.write ('// END GENERATED CODE\n')

cfile.close ()

#################################
# 7TH PART :                    #
#################################
# Generate public decoder H file#
#################################

hfile = open (COMMANDSDEC_HFILE, 'w')

hfile.write (LICENCE_HEADER)
hfile.write ('/**\n')
hfile.write (' * @file ' + COMMANDSDEC_HFILE_NAME + '\n')
hfile.write (' * @brief libARCommands decoder header.\n')
hfile.write (' * This file contains all declarations needed to decode commands\n')
hfile.write (' * @note Autogenerated file\n')
hfile.write (' **/\n')
hfile.write ('#ifndef ' + COMMANDSDEC_DEFINE + '\n')
hfile.write ('#define ' + COMMANDSDEC_DEFINE + '\n')
hfile.write ('#include <' + COMMANDSTYPES_HFILE_NAME + '>\n')
hfile.write ('#include <inttypes.h>\n')
hfile.write ('\n')
hfile.write ('\n')
hfile.write ('/**\n')
hfile.write (' * @brief Error codes for ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'DecodeBuffer') + ' function\n')
hfile.write (' */\n')
DEC_ERR_ENAME='ERROR'
hfile.write ('typedef enum {\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ' = 0, ///< No error occured\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NO_CALLBACK') + ', ///< No error, but no callback was set (so the call had no effect)\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'UNKNOWN_COMMAND') + ', ///< The command buffer contained an unknown command\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_DATA') + ', ///< The command buffer did not contain enough data for the specified command\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_SPACE') + ', ///< The string buffer was not big enough for the command description\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'ERROR') + ', ///< Any other error\n')
hfile.write ('} ' + AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + ';\n')
hfile.write ('\n/**\n')
hfile.write (' * @brief Decode a comand buffer\n')
hfile.write (' * On success, the callback set for the command will be called in the current thread.\n')
hfile.write (' * @param buffer the command buffer to decode\n')
hfile.write (' * @param buffLen the length of the command buffer\n')
hfile.write (' * @return ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ' on success, any error code otherwise\n')
hfile.write (' */\n')
hfile.write (AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + '\n')
hfile.write (ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'DecodeBuffer') + ' (uint8_t *buffer, int32_t buffLen);\n')
hfile.write ('\n')
hfile.write ('\n/**\n')
hfile.write (' * @brief Describe a comand buffer\n')
hfile.write (' * @param buffer the command buffer to decode\n')
hfile.write (' * @param buffLen the length of the command buffer\n')
hfile.write (' * @param resString the string pointer in which the description will be stored\n')
hfile.write (' * @param stringLen the length of the string pointer\n')
hfile.write (' * @return ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ' on success, any error code otherwise\n')
hfile.write (' */\n')
hfile.write (AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + '\n')
hfile.write (ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'DescribeBuffer') + ' (uint8_t *buffer, int32_t buffLen, char *resString, int32_t stringLen);\n')
hfile.write ('\n')
for proj in allProjects:
    hfile.write ('// Project ' + proj.name + '\n\n')
    for cl in proj.classes:
        hfile.write ('// Command class ' + cl.name + '\n')
        for cmd in cl.cmds:
            hfile.write ('\n/**\n')
            hfile.write (' * @brief callback type for the command ' + proj.name + '.' + cl.name + '.' + cmd.name + '\n')
            hfile.write (' */\n')
            hfile.write ('typedef void (*' + ARTypeName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Callback') + ') (')
            first = True
            for arg in cmd.args:
                if first:
                    first = False
                else:
                    hfile.write (', ')
                hfile.write (xmlToC (proj, cl, cmd, arg) + ' ' + arg.name)
            if not first:
                hfile.write (', ')
            hfile.write ('void *custom);\n')
            hfile.write ('/**\n')
            hfile.write (' * @brief callback setter for the command ' + proj.name + '.' + cl.name + '.' + cmd.name + '\n')
            hfile.write (' * @param callback new callback for the command ' + proj.name + '.' + cl.name + '.' + cmd.name + '\n')
            hfile.write (' * @param custom pointer that will be passed to all calls to the callback\n')
            hfile.write (' */\n')
            hfile.write ('void ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Callback') + ' (' + ARTypeName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Callback') + ' callback, void *custom);\n')
        hfile.write ('\n')
    hfile.write ('\n')

hfile.write ('#endif /* ' + COMMANDSDEC_DEFINE + ' */\n')

hfile.close ()

#################################
# 8TH PART :                    #
#################################
# Generate decoder C part       #
#################################

cfile = open (COMMANDSDEC_CFILE, 'w')

cfile.write (LICENCE_HEADER)
cfile.write ('/********************************************\n')
cfile.write (' *            AUTOGENERATED FILE            *\n')
cfile.write (' *             DO NOT MODIFY IT             *\n')
cfile.write (' *                                          *\n')
cfile.write (' * To add new commands :                    *\n')
cfile.write (' *  - Modify ../Xml/commands.xml file       *\n')
cfile.write (' *  - Re-run generateCommandsList.py script *\n')
cfile.write (' *                                          *\n')
cfile.write (' ********************************************/\n')
cfile.write ('#include <config.h>\n')
cfile.write ('#include <stdio.h>\n')
cfile.write ('#include "' + COMMANDSRW_HFILE_NAME + '"\n')
cfile.write ('#include <' + COMMANDSTYPES_HFILE_NAME + '>\n')
cfile.write ('#include <' + COMMANDSDEC_HFILE_NAME + '>\n')
cfile.write ('#include <' + COMMANDSID_HFILE_NAME + '>\n')
cfile.write ('#include <libARSAL/ARSAL_Mutex.h>\n')
cfile.write ('\n')
cfile.write ('// CALLBACK VARIABLES + SETTERS\n')
cfile.write ('\n')
cfile.write ('static ARSAL_Mutex_t ' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, 'mutex') + ';\n')
cfile.write ('static int ' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, 'isInit') + ' = 0;\n')
cfile.write ('int ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'Init') + ' (void)\n')
cfile.write ('{\n')
cfile.write ('    if ((' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, 'isInit') + ' == 0) &&\n')
cfile.write ('        (ARSAL_Mutex_Init (&' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, 'mutex') + ') == 0))\n')
cfile.write ('    {\n')
cfile.write ('        ' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, 'isInit') + ' = 1;\n')
cfile.write ('    } // No else --> Do nothing if already initialized\n')
cfile.write ('    return ' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, 'isInit') + ';\n')
cfile.write ('}\n')
cfile.write ('\n')
for proj in allProjects:
    cfile.write ('// Project ' + proj.name + '\n\n')
    for cl in proj.classes:
        cfile.write ('// Command class ' + cl.name + '\n')
        for cmd in cl.cmds:
            cfile.write ('static ' + ARTypeName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Callback') + ' ' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Cb') + ' = NULL;\n')
            cfile.write ('static void *' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Custom') + ' = NULL;\n')
            cfile.write ('void ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Callback') + ' (' + ARTypeName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Callback') + ' callback, void *custom)\n')
            cfile.write ('{\n')
            cfile.write ('    if (' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'Init') + ' () == 1)\n')
            cfile.write ('    {\n')
            cfile.write ('        ARSAL_Mutex_Lock (&' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, 'mutex') + ');\n')
            cfile.write ('        ' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Cb') + ' = callback;\n')
            cfile.write ('        ' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Custom') + ' = custom;\n')
            cfile.write ('        ARSAL_Mutex_Unlock (&' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, 'mutex') + ');\n')
            cfile.write ('    } // No else --> do nothing if library can not be initialized\n')
            cfile.write ('}\n')
        cfile.write ('\n')
    cfile.write ('\n')

cfile.write ('// DECODER ENTRY POINT\n')
cfile.write (AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + '\n')
cfile.write (ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'DecodeBuffer') + ' (uint8_t *buffer, int32_t buffLen)\n')
cfile.write ('{\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, ID_SUBMODULE, 'PROJECT') + ' commandProject = -1;\n')
cfile.write ('    int commandClass = -1;\n')
cfile.write ('    int commandId = -1;\n')
cfile.write ('    int32_t error = 0;\n')
cfile.write ('    int32_t offset = 0;\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + ' retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ';\n')
cfile.write ('    if (NULL == buffer)\n')
cfile.write ('    {\n')
cfile.write ('        retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'ERROR') + ';\n')
cfile.write ('    } // No else --> Arg check\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        if (' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'Init') + ' () == 0)\n')
cfile.write ('        {\n')
cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'ERROR') + ';\n')
cfile.write ('        } // No else --> keep retVal to OK if init went fine\n')
cfile.write ('    } // No else --> Processing block\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        commandProject = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read8FromBuffer') + ' (buffer, buffLen, &offset, &error);\n')
cfile.write ('        if (error == 1)\n')
cfile.write ('        {\n')
cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_DATA') + ';\n')
cfile.write ('        } // No else --> Do not modify retVal if read went fine\n')
cfile.write ('    } // No else --> Processing block\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        commandClass = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read8FromBuffer') + ' (buffer, buffLen, &offset, &error);\n')
cfile.write ('        if (error == 1)\n')
cfile.write ('        {\n')
cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_DATA') + ';\n')
cfile.write ('        } // No else --> Do not modify retVal if read went fine\n')
cfile.write ('    } // No else --> Processing block\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        commandId = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read16FromBuffer') + ' (buffer, buffLen, &offset, &error);\n')
cfile.write ('        if (error == 1)\n')
cfile.write ('        {\n')
cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_DATA') + ';\n')
cfile.write ('        } // No else --> Do not modify retVal if read went fine\n')
cfile.write ('    } // No else --> Processing block\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        switch (commandProject)\n')
cfile.write ('        {\n')
for proj in allProjects:
    cfile.write ('        case ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, 'PROJECT', proj.name) + ':\n')
    cfile.write ('        {\n')
    cfile.write ('            switch (commandClass)\n')
    cfile.write ('            {\n')
    for cl in proj.classes:
        cfile.write ('            case ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_CLASS', cl.name) + ':\n')
        cfile.write ('            {\n')
        cfile.write ('                switch (commandId)\n')
        cfile.write ('                {\n')
        for cmd in cl.cmds:
            cfile.write ('                case ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_' + cl.name + '_CMD', cmd.name) + ':\n')
            cfile.write ('                {\n')
            CBNAME = ARGlobalName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Cb')
            CBCUSTOMNAME = ARGlobalName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Custom')
            cfile.write ('                    ARSAL_Mutex_Lock (&' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, 'mutex') + ');\n')
            cfile.write ('                    if (' + CBNAME + ' != NULL)\n')
            cfile.write ('                    {\n')
            for arg in cmd.args:
                if 'string' == arg.type:
                    cfile.write ('                        ' + xmlToC (proj, cl, cmd, arg) + ' _' + arg.name + ' = NULL;\n')
                else:
                    cfile.write ('                        ' + xmlToC (proj, cl, cmd, arg) + ' _' + arg.name + ';\n')
            for arg in cmd.args:
                cfile.write ('                        if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
                cfile.write ('                        {\n')
                cfile.write ('                            _' + arg.name + ' = ' + xmlToReader (proj, cl, cmd, arg) + ' (buffer, buffLen, &offset, &error);\n')
                cfile.write ('                            if (error == 1)\n')
                cfile.write ('                            {\n')
                cfile.write ('                                retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_DATA') + ';\n')
                cfile.write ('                            } // No else --> Do not modify retVal if read went fine\n')
                cfile.write ('                        } // No else --> Processing block\n')
            cfile.write ('                        if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
            cfile.write ('                        {\n')
            cfile.write ('                            ' + CBNAME + ' (')
            first = True
            for arg in cmd.args:
                if first:
                    first = False
                else:
                    cfile.write (', ')
                cfile.write ('_' + arg.name)
            if not first:
                cfile.write (', ')
            cfile.write (CBCUSTOMNAME + ');\n')
            cfile.write ('                        } // No else --> Processing block\n')
            cfile.write ('                    }\n')
            cfile.write ('                    else\n')
            cfile.write ('                    {\n')
            cfile.write ('                        retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NO_CALLBACK') + ';\n')
            cfile.write ('                    }\n')
            cfile.write ('                    ARSAL_Mutex_Unlock (&' + ARGlobalName (LIB_MODULE, DEC_SUBMODULE, 'mutex') + ');\n')
            cfile.write ('                }\n')
            cfile.write ('                break; /* ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_' + cl.name + '_CMD', cmd.name) + ' */\n')
        cfile.write ('                default:\n')
        cfile.write ('                    retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'UNKNOWN_COMMAND') + ';\n')
        cfile.write ('                    break;\n')
        cfile.write ('                }\n')
        cfile.write ('            }\n')
        cfile.write ('            break; /* ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_CLASS', cl.name) + ' */\n')
    cfile.write ('            default:\n')
    cfile.write ('                retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'UNKNOWN_COMMAND') + ';\n')
    cfile.write ('                break;\n')
    cfile.write ('            }\n')
    cfile.write ('        }\n')
    cfile.write ('        break; /* ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, 'PROJECT', proj.name) + ' */\n')

cfile.write ('        default:\n')
cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'UNKNOWN_COMMAND') + ';\n')
cfile.write ('            break;\n')
cfile.write ('        }\n')
cfile.write ('    } // No else --> Processing block\n')
cfile.write ('    return retVal;\n')
cfile.write ('}\n')
cfile.write ('\n')
cfile.write (AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + '\n')
cfile.write (ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'DescribeBuffer') + ' (uint8_t *buffer, int32_t buffLen, char *resString, int32_t stringLen)\n')
cfile.write ('{\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, ID_SUBMODULE, 'PROJECT') + ' commandProject = -1;\n')
cfile.write ('    int commandClass = -1;\n')
cfile.write ('    int commandId = -1;\n')
cfile.write ('    int32_t offset = 0;\n')
cfile.write ('    int32_t error = 0;\n')
cfile.write ('    int strOffset = 0;\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + ' retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ';\n')
cfile.write ('    if ((NULL == buffer) || (NULL == resString))\n')
cfile.write ('    {\n')
cfile.write ('        retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'ERROR') + ';\n')
cfile.write ('    } // No else --> Arg check\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        if (' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'Init') + ' () == 0)\n')
cfile.write ('        {\n')
cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'ERROR') + ';\n')
cfile.write ('        } // No else --> keep retVal to OK if init went fine\n')
cfile.write ('    } // No else --> Processing block\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        commandProject = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read8FromBuffer') + ' (buffer, buffLen, &offset, &error);\n')
cfile.write ('        if (error == 1)\n')
cfile.write ('        {\n')
cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_DATA') + ';\n')
cfile.write ('        } // No else --> Do not modify retVal if read went fine\n')
cfile.write ('    } // No else --> Processing block\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        commandClass = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read8FromBuffer') + ' (buffer, buffLen, &offset, &error);\n')
cfile.write ('        if (error == 1)\n')
cfile.write ('        {\n')
cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_DATA') + ';\n')
cfile.write ('        } // No else --> Do not modify retVal if read went fine\n')
cfile.write ('    } // No else --> Processing block\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        commandId = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read16FromBuffer') + ' (buffer, buffLen, &offset, &error);\n')
cfile.write ('        if (error == 1)\n')
cfile.write ('        {\n')
cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_DATA') + ';\n')
cfile.write ('        } // No else --> Do not modify retVal if read went fine\n')
cfile.write ('    } // No else --> Processing block\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ' && stringLen > 0)\n')
cfile.write ('    {\n')
cfile.write ('        resString[0] = \'\\0\';\n')
cfile.write ('    }\n')
cfile.write ('    else\n')
cfile.write ('    {\n')
cfile.write ('        retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'ERROR') + ';\n')
cfile.write ('    }\n')
cfile.write ('\n')
cfile.write ('    if (retVal == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        switch (commandProject)\n')
cfile.write ('        {\n')
for proj in allProjects:
    cfile.write ('        case ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, 'PROJECT', proj.name) + ':\n')
    cfile.write ('        {\n')
    cfile.write ('            switch (commandClass)\n')
    cfile.write ('            {\n')
    for cl in proj.classes:
        cfile.write ('            case ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_CLASS', cl.name) + ':\n')
        cfile.write ('            {\n')
        cfile.write ('                switch (commandId)\n')
        cfile.write ('                {\n')
        for cmd in cl.cmds:
            cfile.write ('                case ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_' + cl.name + '_CMD', cmd.name) + ':\n')
            cfile.write ('                {\n')
            cfile.write ('                    strOffset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' ("' + proj.name + '.' + cl.name + '.' + cmd.name + ':", resString, stringLen, strOffset) ;\n')
            for arg in cmd.args:
                cfile.write ('                    if (strOffset > 0)\n')
                cfile.write ('                    {\n')
                cfile.write ('                        ' + xmlToC (proj, cl, cmd, arg) + ' arg = ' + xmlToReader (proj, cl, cmd, arg) + ' (buffer, buffLen, &offset, &error);\n')
                cfile.write ('                        if (error == 0)\n')
                cfile.write ('                        {\n')
                cfile.write ('                            strOffset = ' + xmlToPrinter (proj, cl, cmd, arg) + ' (" | ' + arg.name + ' -> ", arg, resString, stringLen, strOffset);\n')
                cfile.write ('                        }\n')
                cfile.write ('                        else\n')
                cfile.write ('                        {\n')
                cfile.write ('                            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_DATA') + ';\n')
                cfile.write ('                        }\n')
                cfile.write ('                    } // No else --> If first print failed, the next if will set the error code\n')
            cfile.write ('                    if (strOffset < 0)\n')
            cfile.write ('                    {\n')
            cfile.write ('                        retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'NOT_ENOUGH_SPACE') + ';\n')
            cfile.write ('                    } // No else --> Do not modify retVal if no error occured\n')
            cfile.write ('                }\n')
            cfile.write ('                break; /* ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_' + cl.name + '_CMD', cmd.name) + ' */\n')
        cfile.write ('                default:\n')
        cfile.write ('                    strOffset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' ("' + proj.name + '.' + cl.name + '.UNKNOWN -> Unknown command", resString, stringLen, strOffset);\n')
        cfile.write ('                    retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'UNKNOWN_COMMAND') + ';\n')
        cfile.write ('                    break;\n')
        cfile.write ('                }\n')
        cfile.write ('            }\n')
        cfile.write ('            break; /* ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_CLASS', cl.name) + ' */\n')
    cfile.write ('            default:\n')
    cfile.write ('                strOffset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' ("' + proj.name + '.UNKNOWN -> Unknown command", resString, stringLen, strOffset);\n')
    cfile.write ('                retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'UNKNOWN_COMMAND') + ';\n')
    cfile.write ('                break;\n')
    cfile.write ('            }\n')
    cfile.write ('        }\n')
    cfile.write ('        break; /* ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, 'PROJECT', proj.name) + ' */\n')

cfile.write ('        default:\n')
cfile.write ('            strOffset = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'WriteString') + ' ("UNKNOWN -> Unknown command", resString, stringLen, strOffset);\n')
cfile.write ('            retVal = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'UNKNOWN_COMMAND') + ';\n')
cfile.write ('            break;\n')
cfile.write ('        }\n')
cfile.write ('    } // No else --> Processing block\n')
cfile.write ('    return retVal;\n')
cfile.write ('}\n')
cfile.write ('\n')


cfile.write ('// END GENERATED CODE\n')

cfile.close ()



#################################
# 9TH PART :                    #
#################################
# Generate filter h file        #
#################################

FIL_STATUS_ENAME='STATUS'
FIL_ERROR_ENAME='ERROR'

hfile = open (COMMANDSFIL_HFILE, 'w')

hfile.write (LICENCE_HEADER)
hfile.write ('/**\n')
hfile.write (' * @file ' + COMMANDSFIL_HFILE_NAME + '\n')
hfile.write (' * @brief libARCommands filter header.\n')
hfile.write (' * This file contains all declarations needed to create and use a commands filter\n')
hfile.write (' * @note Autogenerated file\n')
hfile.write (' **/\n')
hfile.write ('#ifndef ' + COMMANDSFIL_DEFINE + '\n')
hfile.write ('#define ' + COMMANDSFIL_DEFINE + '\n')
hfile.write ('#include <' + COMMANDSTYPES_HFILE_NAME + '>\n')
hfile.write ('#include <inttypes.h>\n')
hfile.write ('\n')
hfile.write ('/**\n')
hfile.write (' * @brief Error code for ARCOMMANDS_Filter functions.\n')
hfile.write (' */\n')
hfile.write ('typedef enum {\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ' = 0, ///< No error.\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'ALLOC') + ', ///< Memory allocation error.\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_STATUS') + ', ///< The given status is not a valid status.\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_FILTER') + ', ///< The given filter is not a valid filter.\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_BUFFER') + ', ///< The given buffer is not a valid buffer.\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OTHER') + ', ///< Any other error.\n')
hfile.write ('} ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ';\n')
hfile.write ('\n')
hfile.write ('/**\n')
hfile.write (' * @brief Status code for ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'FilterCommand') + ' function\n')
hfile.write (' */\n')
hfile.write ('typedef enum {\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ' = 0, ///< The command should pass the filter\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ', ///< The command should not pass the filter\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'UNKNOWN') + ', ///< Unknown command. The command was possibly added in a newer version of libARCommands, or is an invalid command.\n')
hfile.write ('    ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ERROR') + ', ///< The filtering of the command failed.\n')
hfile.write ('} ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ';\n')
hfile.write ('\n')
hfile.write ('/**\n')
hfile.write (' * @brief ARCOMMANDS_Filter object holder\n')
hfile.write (' */\n')
hfile.write ('typedef struct ARCOMMANDS_Filter_t ARCOMMANDS_Filter_t;\n')
hfile.write ('\n')
hfile.write ('/**\n')
hfile.write (' * @brief Creates a new ARCOMMANDS_Filter_t\n')
hfile.write (' * @param defaultBehavior The default behavior of the filter (must be either ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ' or ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ').\n')
hfile.write (' * @param error Optionnal pointer which will hold the error code.\n')
hfile.write (' * @warning This function allocates memory.\n')
hfile.write (' * @note The memory must be freed by a call to ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'DeleteFilter') + '.\n')
hfile.write (' * @return A new ARCOMMANDS_Filter_t instance. NULL in case of error.\n')
hfile.write (' */\n')
hfile.write ('ARCOMMANDS_Filter_t* ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'NewFilter') + ' (' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' defaultBehavior, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' *error);\n')
hfile.write ('\n')
hfile.write ('/**\n')
hfile.write (' * @brief Deletes an ARCOMMANDS_Filter_t\n')
hfile.write (' * @param filter The filter to delete.\n')
hfile.write (' */\n')
hfile.write ('void ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'DeleteFilter') + ' (ARCOMMANDS_Filter_t **filter);\n')
hfile.write ('\n')
hfile.write ('/**\n')
hfile.write (' * @brief Filter an ARCommand\n')
hfile.write (' * @param filter The ARCOMMANDS_Filter_t to use for filtering.\n')
hfile.write (' * @param buffer The ARCommand buffer.\n')
hfile.write (' * @param len The ARCommand buffer length.\n')
hfile.write (' * @param error Optionnal pointer which will hold the error code.\n')
hfile.write (' * @return An ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' status code\n')
hfile.write (' */\n')
hfile.write (AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'FilterCommand') + ' (ARCOMMANDS_Filter_t *filter, uint8_t *buffer, uint32_t len, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' *error);\n')
hfile.write ('\n')
hfile.write ('\n')
hfile.write ('// Filter ON/OFF functions')
hfile.write ('\n')
for proj in allProjects:
    hfile.write ('// Project ' + proj.name + '\n')
    hfile.write ('\n')
    
    hfile.write ('/**\n')
    hfile.write (' * @brief Sets the filter behavior for all commands ' + proj.name + '.XXX.XXX.\n')
    hfile.write (' * @param filter The filter to be modified.\n')
    hfile.write (' * @param behavior The behavior to use for the commands (must be either ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ' or ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ').\n')
    hfile.write (' * @return An ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' enum.\n')
    hfile.write (' */\n')
    hfile.write (AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' ARCOMMANDS_Filter_Set' + ARCapitalize (proj.name) + 'Behavior (ARCOMMANDS_Filter_t *filter, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' behavior);\n')
    hfile.write ('\n')
        
    for cl in proj.classes:
        hfile.write ('// Command class ' + cl.name + '\n')
        hfile.write ('\n')
        
        hfile.write ('/**\n')
        hfile.write (' * @brief Sets the filter behavior for all commands ' + proj.name + '.' + cl.name + '.XXX.\n')
        hfile.write (' * @param filter The filter to be modified.\n')
        hfile.write (' * @param behavior The behavior to use for the commands (must be either ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ' or ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ').\n')
        hfile.write (' * @return An ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' enum.\n')
        hfile.write (' */\n')
        hfile.write (AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' ARCOMMANDS_Filter_Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + 'Behavior (ARCOMMANDS_Filter_t *filter, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' behavior);\n')
        hfile.write ('\n')
        
        for cmd in cl.cmds:
            hfile.write ('/**\n')
            hfile.write (' * @brief Sets the filter behavior for the command ' + proj.name + '.' + cl.name + '.' + cmd.name + '.\n')
            hfile.write (' * @param filter The filter to be modified.\n')
            hfile.write (' * @param behavior The behavior to use for the command (must be either ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ' or ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ').\n')
            hfile.write (' * @return An ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' enum.\n')
            hfile.write (' */\n')
            hfile.write (AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' ARCOMMANDS_Filter_Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Behavior (ARCOMMANDS_Filter_t *filter, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' behavior);\n')
            hfile.write ('\n')
        hfile.write ('\n')
    hfile.write ('\n')


hfile.write ('#endif /* ' + COMMANDSFIL_DEFINE + ' */\n')

hfile.close ()

#################################
# 10TH PART :                   #
#################################
# Generate filter c file        #
#################################

cfile = open (COMMANDSFIL_CFILE, 'w')

cfile.write (LICENCE_HEADER)
cfile.write ('/********************************************\n')
cfile.write (' *            AUTOGENERATED FILE            *\n')
cfile.write (' *             DO NOT MODIFY IT             *\n')
cfile.write (' *                                          *\n')
cfile.write (' * To add new commands :                    *\n')
cfile.write (' *  - Modify ../Xml/commands.xml file       *\n')
cfile.write (' *  - Re-run generateCommandsList.py script *\n')
cfile.write (' *                                          *\n')
cfile.write (' ********************************************/\n')
cfile.write ('#include <config.h>\n')
cfile.write ('#include <stdlib.h>\n')
cfile.write ('#include "' + COMMANDSRW_HFILE_NAME + '"\n')
cfile.write ('#include <' + COMMANDSTYPES_HFILE_NAME + '>\n')
cfile.write ('#include <' + COMMANDSFIL_HFILE_NAME + '>\n')
cfile.write ('#include <' + COMMANDSID_HFILE_NAME + '>\n')
cfile.write ('\n')
cfile.write ('\n')
cfile.write ('// ARCOMMANDS_Filter_t structure definition\n')
cfile.write ('struct ARCOMMANDS_Filter_t\n')
cfile.write ('{\n')
for proj in allProjects:
    cfile.write ('    // Project ' + proj.name + '\n')
    for cl in proj.classes:
        cfile.write ('    // Class ' + cl.name + '\n')
        for cmd in cl.cmds:
            cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' Cmd' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Behavior;\n')
    cfile.write ('\n')
cfile.write ('};\n')
cfile.write ('\n')
cfile.write ('\n')
cfile.write ('// Constructor\n')
cfile.write ('ARCOMMANDS_Filter_t* ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'NewFilter') + ' (' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' defaultBehavior, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' *error)\n')
cfile.write ('{\n')
cfile.write ('    ARCOMMANDS_Filter_t *retFilter = NULL;\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' localError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ';\n')
cfile.write ('    if ((defaultBehavior != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ') &&\n')
cfile.write ('        (defaultBehavior != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + '))\n')
cfile.write ('    {\n')
cfile.write ('        localError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_STATUS') + ';\n')
cfile.write ('    } // No else : Args check\n')
cfile.write ('\n')
cfile.write ('    if (localError == ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        retFilter = malloc (sizeof (struct ARCOMMANDS_Filter_t));\n')
cfile.write ('        if (retFilter == NULL)\n')
cfile.write ('        {\n')
cfile.write ('            localError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'ALLOC') + ';\n')
cfile.write ('        } // No else : Error processing.\n')
cfile.write ('    } // No else : Processing block\n')
cfile.write ('\n')
cfile.write ('    // Setup default behavior\n')
cfile.write ('    if (localError == ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
for proj in allProjects:
    cfile.write ('        // Projects ' + proj.name + '\n')
    for cl in proj.classes:
        cfile.write ('        // Class ' + cl.name + '\n')
        for cmd in cl.cmds:
            cfile.write ('        retFilter->Cmd' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Behavior = defaultBehavior;\n')
cfile.write ('    } // No else : Processing block\n')
cfile.write ('\n')
cfile.write ('    if (localError != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        if (retFilter != NULL)\n')
cfile.write ('        {\n')
cfile.write ('            ARCOMMANDS_Filter_DeleteFilter (&retFilter);\n')
cfile.write ('        } // No else : Nothing to do if the pointer is already NULL\n')
cfile.write ('    } // No else : Only do cleanup if an error occured\n')
cfile.write ('\n')
cfile.write ('    if (error != NULL)\n')
cfile.write ('    {\n')
cfile.write ('        *error = localError;\n')
cfile.write ('    } // No else : Set error only if pointer is not NULL\n')
cfile.write ('    return retFilter;\n')
cfile.write ('}\n')
cfile.write ('\n')
cfile.write ('void ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'DeleteFilter') + ' (ARCOMMANDS_Filter_t **filter)\n')
cfile.write ('{\n')
cfile.write ('    if ((filter != NULL) &&\n')
cfile.write ('        (*filter != NULL))\n')
cfile.write ('    {\n')
cfile.write ('        free (*filter);\n')
cfile.write ('        *filter = NULL;\n')
cfile.write ('    } // No else : No need to delete an invalid filter instance\n')
cfile.write ('}\n')
cfile.write ('\n')
cfile.write (AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'FilterCommand') + ' (ARCOMMANDS_Filter_t *filter, uint8_t *buffer, uint32_t len, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' *error)\n')
cfile.write ('{\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, ID_SUBMODULE, 'PROJECT') + ' commandProject = -1;\n')
cfile.write ('    int commandClass = -1;\n')
cfile.write ('    int commandId = -1;\n')
cfile.write ('    int32_t offset = 0;\n')
cfile.write ('    int32_t readError = 0;\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' localError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ';\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' retStatus = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'UNKNOWN') + ';\n')
cfile.write ('\n')
cfile.write ('    // Args check\n')
cfile.write ('    if (filter == NULL)\n')
cfile.write ('    {\n')
cfile.write ('        localError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_FILTER') + ';\n')
cfile.write ('    } // No else : Args check\n')
cfile.write ('\n')
cfile.write ('    if ((buffer == NULL) ||\n')
cfile.write ('        (len < 4))\n')
cfile.write ('    {\n')
cfile.write ('        localError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_BUFFER') + ';\n')
cfile.write ('    } // No else : Args check\n')
cfile.write ('\n')
cfile.write ('    if (localError == ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        commandProject = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read8FromBuffer') + ' (buffer, len, &offset, &readError);\n')
cfile.write ('        if (readError == 1)\n')
cfile.write ('        {\n')
cfile.write ('            localError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_BUFFER') + ';\n')
cfile.write ('        }\n')
cfile.write ('    } // No else : Processing block\n')
cfile.write ('\n')
cfile.write ('    if (localError == ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        commandClass = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read8FromBuffer') + ' (buffer, len, &offset, &readError);\n')
cfile.write ('        if (readError == 1)\n')
cfile.write ('        {\n')
cfile.write ('            localError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_BUFFER') + ';\n')
cfile.write ('        }\n')
cfile.write ('    } // No else : Processing block\n')
cfile.write ('\n')
cfile.write ('    if (localError == ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        commandId = ' + ARFunctionName (LIB_MODULE, RW_SUBMODULE, 'Read16FromBuffer') + ' (buffer, len, &offset, &readError);\n')
cfile.write ('        if (readError == 1)\n')
cfile.write ('        {\n')
cfile.write ('            localError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_BUFFER') + ';\n')
cfile.write ('        }\n')
cfile.write ('    } // No else : Processing block\n')
cfile.write ('\n')
cfile.write ('    if (localError == ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        switch (commandProject)\n')
cfile.write ('        {\n')
for proj in allProjects:
    cfile.write ('        case ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, 'PROJECT', proj.name) + ':\n')
    cfile.write ('        {\n')
    cfile.write ('            switch (commandClass)\n')
    cfile.write ('            {\n')
    for cl in proj.classes:
        cfile.write ('            case ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_CLASS', cl.name) + ':\n')
        cfile.write ('            {\n')
        cfile.write ('                switch (commandId)\n')
        cfile.write ('                {\n')
        for cmd in cl.cmds:
            cfile.write ('                case ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_' + cl.name + '_CMD', cmd.name) + ':\n')
            cfile.write ('                {\n')
            cfile.write ('                    retStatus = filter->Cmd' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Behavior;\n')
            cfile.write ('                }\n')
            cfile.write ('                break; /* ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_' + cl.name + '_CMD', cmd.name) + ' */\n')
        cfile.write ('                default:\n')
        cfile.write ('                    // Do nothing, the default answer is already UNKNOWN\n')
        cfile.write ('                    break;\n')
        cfile.write ('                }\n')
        cfile.write ('            }\n')
        cfile.write ('            break; /* ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, proj.name + '_CLASS', cl.name) + ' */\n')
    cfile.write ('            default:\n')
    cfile.write ('                // Do nothing, the default answer is already UNKNOWN\n')
    cfile.write ('                break;\n')
    cfile.write ('            }\n')
    cfile.write ('        }\n')
    cfile.write ('        break; /* ' + AREnumValue (LIB_MODULE, ID_SUBMODULE, 'PROJECT', proj.name) + ' */\n')

cfile.write ('        default:\n')
cfile.write ('            // Do nothing, the default answer is already UNKNOWN\n')
cfile.write ('            break;\n')
cfile.write ('        }\n')
cfile.write ('    }\n')
cfile.write ('\n')
cfile.write ('    if (localError != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        retStatus = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ERROR') + ';\n')
cfile.write ('    } // No else : Keep retStatus if no error occured\n')
cfile.write ('\n')
cfile.write ('    if (error != NULL)\n')
cfile.write ('    {\n')
cfile.write ('        *error = localError;\n')
cfile.write ('    } // No else : Set error only if pointer is not NULL\n')
cfile.write ('\n')
cfile.write ('    return retStatus;\n')
cfile.write ('}\n')
cfile.write ('\n')
cfile.write ('\n')
cfile.write ('// Filter ON/OFF functions')
cfile.write ('\n')
for proj in allProjects:
    cfile.write ('// Project ' + proj.name + '\n')
    cfile.write ('\n')

    cfile.write (AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' ARCOMMANDS_Filter_Set' + ARCapitalize (proj.name) + 'Behavior (ARCOMMANDS_Filter_t *filter, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' behavior)\n')
    cfile.write ('{\n')
    cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' retError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ';\n')
    cfile.write ('\n')
    cfile.write ('    if (filter == NULL)\n')
    cfile.write ('    {\n')
    cfile.write ('        retError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_FILTER') + ';\n')
    cfile.write ('    } // No else : Args check\n')
    cfile.write ('\n')
    cfile.write ('    if ((behavior != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ') &&\n')
    cfile.write ('        (behavior != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + '))\n')
    cfile.write ('    {\n')
    cfile.write ('        retError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_STATUS') + ';\n')
    cfile.write ('    } // No else : Arg check\n')
    cfile.write ('\n')
    cfile.write ('    if (retError == ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
    cfile.write ('    {\n')
    for cl in proj.classes:
        for cmd in cl.cmds:
            cfile.write ('        filter->Cmd' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Behavior = behavior;\n')
    cfile.write ('    }\n')
    cfile.write ('\n')
    cfile.write ('    return retError;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
    
    for cl in proj.classes:
        cfile.write ('// Command class ' + cl.name + '\n')
        cfile.write ('\n')
        cfile.write (AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' ARCOMMANDS_Filter_Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + 'Behavior (ARCOMMANDS_Filter_t *filter, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' behavior)\n')
        cfile.write ('{\n')
        cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' retError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ';\n')
        cfile.write ('\n')
        cfile.write ('    if (filter == NULL)\n')
        cfile.write ('    {\n')
        cfile.write ('        retError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_FILTER') + ';\n')
        cfile.write ('    } // No else : Args check\n')
        cfile.write ('\n')
        cfile.write ('    if ((behavior != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ') &&\n')
        cfile.write ('        (behavior != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + '))\n')
        cfile.write ('    {\n')
        cfile.write ('        retError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_STATUS') + ';\n')
        cfile.write ('    } // No else : Arg check\n')
        cfile.write ('\n')
        cfile.write ('    if (retError == ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
        cfile.write ('    {\n')
        for cmd in cl.cmds:
            cfile.write ('        filter->Cmd' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Behavior = behavior;\n')
        cfile.write ('    }\n')
        cfile.write ('\n')
        cfile.write ('    return retError;\n')
        cfile.write ('}\n')
        cfile.write ('\n')
    
    for cl in proj.classes:
        cfile.write ('// Command class ' + cl.name + '\n')
        cfile.write ('\n')
        for cmd in cl.cmds:
            cfile.write (AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' ARCOMMANDS_Filter_Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Behavior (ARCOMMANDS_Filter_t *filter, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' behavior)\n')
            cfile.write ('{\n')
            cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' retError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ';\n')
            cfile.write ('    if (filter == NULL)\n')
            cfile.write ('    {\n')
            cfile.write ('        retError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_FILTER') + ';\n')
            cfile.write ('    } // No else : Args check\n')
            cfile.write ('\n')
            cfile.write ('    if ((behavior != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ') &&\n')
            cfile.write ('        (behavior != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + '))\n')
            cfile.write ('    {\n')
            cfile.write ('        retError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'BAD_STATUS') + ';\n')
            cfile.write ('    } // No else : Arg check\n')
            cfile.write ('\n')
            cfile.write ('    if (retError == ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
            cfile.write ('    {\n')
            cfile.write ('        filter->Cmd' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Behavior = behavior;\n')
            cfile.write ('    }\n')
            cfile.write ('\n')
            cfile.write ('    return retError;\n')
            cfile.write ('}\n')
            cfile.write ('\n')
        cfile.write ('\n')
    cfile.write ('\n')

cfile.write ('// END GENERATED CODE\n')

cfile.close ()

#################################
# 11TH PART :                   #
#################################
# Generate C Testbench          #
#################################

def TB_CALL_VARNAME (proj, cls, cmd):
    return proj.name + ARCapitalize (cls.name) + ARCapitalize (cmd.name) + 'ShouldBeCalled'

def TB_CREATE_VARNAME (proj, cls, cmd):
    return 'int ' + TB_CALL_VARNAME (proj, cls, cmd) + ' = 0;'

cfile = open (TB_CFILE, 'w')

cfile.write (LICENCE_HEADER)
cfile.write ('/********************************************\n')
cfile.write (' *            AUTOGENERATED FILE            *\n')
cfile.write (' *             DO NOT MODIFY IT             *\n')
cfile.write (' *                                          *\n')
cfile.write (' * To add new commands :                    *\n')
cfile.write (' *  - Modify ../Xml/commands.xml file       *\n')
cfile.write (' *  - Re-run generateCommandsList.py script *\n')
cfile.write (' *                                          *\n')
cfile.write (' ********************************************/\n')
cfile.write ('#include <' + COMMANDSGEN_HFILE_NAME + '>\n')
cfile.write ('#include <' + COMMANDSDEC_HFILE_NAME + '>\n')
cfile.write ('#include <' + COMMANDSFIL_HFILE_NAME + '>\n')
cfile.write ('#include <libARSAL/ARSAL_Print.h>\n')
cfile.write ('#include <stdlib.h>\n')
cfile.write ('#include <string.h>\n')
cfile.write ('\n')
cfile.write ('int errcount;\n')
cfile.write ('char describeBuffer [1024] = {0};\n')
cfile.write ('\n')
for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            cfile.write (TB_CREATE_VARNAME (proj, cl, cmd) + '\n')
cfile.write ('\n')
for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            cfile.write ('void ' + ARFunctionName (LIB_MODULE, TB_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Cb') + ' (')
            first = True
            for arg in cmd.args:
                if first:
                    first = False
                else:
                    cfile.write (', ')
                cfile.write (xmlToC (proj, cl, cmd, arg) + ' ' + arg.name)
            if not first:
                cfile.write (', ')
            cfile.write ('void *custom)\n')
            cfile.write ('{\n')
            cfile.write ('    ARSAL_PRINT (ARSAL_PRINT_WARNING, "' + TB_TAG + '", "Callback for command ' + proj.name + '.' + cl.name + '.' + cmd.name + ' --> Custom PTR = %p", custom);\n')
            for arg in cmd.args:
                cfile.write ('    ARSAL_PRINT (ARSAL_PRINT_WARNING, "' + TB_TAG + '", "' + arg.name + ' value : <' + xmlToPrintf (proj, cl, cmd, arg) + '>", ' + arg.name + ');\n')
                if "string" == arg.type:
                    cfile.write ('    if (strcmp (' + xmlToSample (proj, cl, cmd, arg) + ', ' + arg.name + ') != 0)\n')
                else:
                    cfile.write ('    if (' + arg.name + ' != ' + xmlToSample (proj, cl, cmd, arg) + ')\n')
                cfile.write ('    {\n')
                if "string" == arg.type:
                    cfile.write ('        ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "BAD ARG VALUE !!! --> Expected <%s>", ' + xmlToSample (proj, cl, cmd, arg) + ');\n')
                else:
                    cfile.write ('        ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "BAD ARG VALUE !!! --> Expected <' + xmlToSample (proj, cl, cmd, arg) + '>");\n')
                cfile.write ('        errcount++ ;\n')
                cfile.write ('    }\n')
            cfile.write ('    if (' + TB_CALL_VARNAME (proj, cl, cmd) + ' == 0)\n')
            cfile.write ('    {\n')
            cfile.write ('        ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "BAD CALLBACK !!! --> This callback should not have been called for this command");\n')
            cfile.write ('        errcount++ ;\n')
            cfile.write ('    }\n')
            cfile.write ('}\n')
        cfile.write ('\n')
    cfile.write ('\n')

cfile.write ('\n')
cfile.write ('void ' + ARFunctionName (LIB_MODULE, TB_SUBMODULE, 'initCb') + ' (void)\n')
cfile.write ('{\n')
cfile.write ('    intptr_t cbCustom = 0;\n')
for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            cfile.write ('    ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Callback') + ' ((' + ARTypeName (LIB_MODULE, DEC_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Callback') + ') ' + ARFunctionName (LIB_MODULE, TB_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Cb') + ', (void *)cbCustom++ );\n')
cfile.write ('}\n')

cfile.write ('\n')
cfile.write ('\n')
cfile.write ('int ' + ARFunctionName (LIB_MODULE, TB_SUBMODULE, 'filterTest') + ' (uint8_t *buffer, uint32_t size, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' (*setter)(ARCOMMANDS_Filter_t *, ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + '))\n')
cfile.write ('{\n')
cfile.write ('    int errors = 0;\n')
cfile.write ('    ARCOMMANDS_Filter_t *testFilter = NULL;\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' filterError = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ';\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' filterStatus = ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'UNKNOWN') + ';\n')
cfile.write ('    // Default allow, set to block after\n')
cfile.write ('    testFilter = ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'NewFilter') + ' (' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ', &filterError);\n')
cfile.write ('    if (filterError != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "Error while creating allow filter : %d", filterError);\n')
cfile.write ('        errors++;\n')
cfile.write ('    }\n')
cfile.write ('    else\n')
cfile.write ('    {\n')
cfile.write ('        filterStatus = ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'FilterCommand') + ' (testFilter, buffer, size, &filterError);\n')
cfile.write ('        if ((filterStatus != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ') ||\n')
cfile.write ('            (filterError != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + '))\n')
cfile.write ('        {\n')
cfile.write ('            ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "Error while filtering : expected status %d / error %d, got status %d, error %d !", ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ', ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ', filterStatus, filterError);\n')
cfile.write ('            errors++;\n')
cfile.write ('        }\n')
cfile.write ('        // Change filter status\n')
cfile.write ('        filterError = setter (testFilter, ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ');\n')
cfile.write ('        if (filterError != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('        {\n')
cfile.write ('            ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "Error while setting filter state to blocked : %d", filterError);\n')
cfile.write ('            errors++;\n')
cfile.write ('        }\n')
cfile.write ('        else\n')
cfile.write ('        {\n')
cfile.write ('            filterStatus = ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'FilterCommand') + ' (testFilter, buffer, size, &filterError);\n')
cfile.write ('            if ((filterStatus != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ') ||\n')
cfile.write ('                (filterError != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + '))\n')
cfile.write ('            {\n')
cfile.write ('                ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "Error while filtering : expected status %d / error %d, got status %d, error %d !", ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ', ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ', filterStatus, filterError);\n')
cfile.write ('                errors++;\n')
cfile.write ('            }\n')
cfile.write ('        }\n')
cfile.write ('        ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'DeleteFilter') + ' (&testFilter);\n')
cfile.write ('    }\n')
cfile.write ('    // Default block, set to allow after\n')
cfile.write ('    testFilter = ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'NewFilter') + ' (' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ', &filterError);\n')
cfile.write ('    if (filterError != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "Error while creating block filter : %d", filterError);\n')
cfile.write ('        errors++;\n')
cfile.write ('    }\n')
cfile.write ('    else\n')
cfile.write ('    {\n')
cfile.write ('        filterStatus = ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'FilterCommand') + ' (testFilter, buffer, size, &filterError);\n')
cfile.write ('        if ((filterStatus != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ') ||\n')
cfile.write ('            (filterError != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + '))\n')
cfile.write ('        {\n')
cfile.write ('            ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "Error while filtering : expected status %d / error %d, got status %d, error %d !", ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'BLOCKED') + ', ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ', filterStatus, filterError);\n')
cfile.write ('            errors++;\n')
cfile.write ('        }\n')
cfile.write ('        // Change filter status\n')
cfile.write ('        filterError = setter (testFilter, ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ');\n')
cfile.write ('        if (filterError != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ')\n')
cfile.write ('        {\n')
cfile.write ('            ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "Error while setting filter state to allowed : %d", filterError);\n')
cfile.write ('            errors++;\n')
cfile.write ('        }\n')
cfile.write ('        else\n')
cfile.write ('        {\n')
cfile.write ('            filterStatus = ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'FilterCommand') + ' (testFilter, buffer, size, &filterError);\n')
cfile.write ('            if ((filterStatus != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ') ||\n')
cfile.write ('                (filterError != ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + '))\n')
cfile.write ('            {\n')
cfile.write ('                ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "Error while filtering : expected status %d / error %d, got status %d, error %d !", ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME, 'ALLOWED') + ', ' + AREnumValue (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME, 'OK') + ', filterStatus, filterError);\n')
cfile.write ('                errors++;\n')
cfile.write ('            }\n')
cfile.write ('        }\n')
cfile.write ('        ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'DeleteFilter') + ' (&testFilter);\n')
cfile.write ('    }\n')
cfile.write ('    return errors;\n')
cfile.write ('}\n')
cfile.write ('\n')
cfile.write ('int ' + ARFunctionName (LIB_MODULE, TB_SUBMODULE, 'autoTest') + ' ()\n')
cfile.write ('{\n')
cfile.write ('    int32_t buffSize = 128;\n')
cfile.write ('    uint8_t *buffer = malloc (buffSize * sizeof (uint8_t));\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + ' res = ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'OK') + ';\n')
cfile.write ('    int32_t resSize = 0;\n')
cfile.write ('    errcount = 0;\n')
cfile.write ('    ' + ARFunctionName (LIB_MODULE, TB_SUBMODULE, 'initCb') + ' ();\n')
for proj in allProjects:
    cfile.write ('    // Project ' + proj.name + '\n')
    for cl in proj.classes:
        cfile.write ('    // Command class ' + cl.name + '\n')
        for cmd in cl.cmds:
            cfile.write ('    res = ' + ARFunctionName (LIB_MODULE, GEN_SUBMODULE, 'Generate' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name)) + ' (buffer, buffSize, &resSize')
            for arg in cmd.args:
                cfile.write (', ' + xmlToSample (proj, cl, cmd, arg))
            cfile.write (');\n')
            cfile.write ('    if (res != ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'OK') + ')\n')
            cfile.write ('    {\n')
            cfile.write ('        ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "Error while generating command ' + ARCapitalize (proj.name) + '.' + ARCapitalize (cl.name) + '.' + ARCapitalize (cmd.name) + '\\n\\n");\n')
            cfile.write ('        errcount++ ;\n')
            cfile.write ('    }\n')
            cfile.write ('    else\n')
            cfile.write ('    {\n')
            cfile.write ('        ARSAL_PRINT (ARSAL_PRINT_WARNING, "' + TB_TAG + '", "Generating command ' + ARCapitalize (proj.name) + '.' + ARCapitalize (cl.name) + '.' + ARCapitalize (cmd.name) + ' succeded");\n')
            cfile.write ('        ' + AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + ' err;\n')
            cfile.write ('        err = ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'DescribeBuffer') + ' (buffer, resSize, describeBuffer, 1024);\n')
            cfile.write ('        if (err != ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
            cfile.write ('        {\n')
            cfile.write ('            ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "Error while describing buffer: %d", err);\n')
            cfile.write ('            errcount++ ;\n')
            cfile.write ('        }\n')
            cfile.write ('        else\n')
            cfile.write ('        {\n')
            cfile.write ('            ARSAL_PRINT (ARSAL_PRINT_WARNING, "' + TB_TAG + '", "%s", describeBuffer);\n')
            cfile.write ('        }\n')
            cfile.write ('        errcount += ' + ARFunctionName (LIB_MODULE, TB_SUBMODULE, 'filterTest') + ' (buffer, resSize, ARCOMMANDS_Filter_Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Behavior);\n')
            cfile.write ('        ' + TB_CALL_VARNAME (proj, cl, cmd) + ' = 1;\n')
            cfile.write ('        err = ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'DecodeBuffer') + ' (buffer, resSize);\n')
            cfile.write ('        ' + TB_CALL_VARNAME (proj, cl, cmd) + ' = 0;\n')
            cfile.write ('        ARSAL_PRINT (ARSAL_PRINT_WARNING, "' + TB_TAG + '", "Decode return value : %d\\n\\n", err);\n')
            cfile.write ('        if (err != ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
            cfile.write ('        {\n')
            cfile.write ('            errcount++ ;\n')
            cfile.write ('        }\n')
            cfile.write ('    }\n')
            cfile.write ('\n')
        cfile.write ('\n')
    cfile.write ('\n')

cfile.write ('    if (errcount == 0)\n')
cfile.write ('    {\n')
cfile.write ('        ARSAL_PRINT (ARSAL_PRINT_WARNING, "' + TB_TAG + '", "No errors !");\n')
cfile.write ('    }\n')
cfile.write ('    else\n')
cfile.write ('    {\n')
cfile.write ('        ARSAL_PRINT (ARSAL_PRINT_ERROR, "' + TB_TAG + '", "%d errors detected during autoTest", errcount);\n')
cfile.write ('    }\n')
cfile.write ('    if (buffer != NULL)\n')
cfile.write ('    {\n')
cfile.write ('        free (buffer);\n')
cfile.write ('    }\n')
cfile.write ('    return errcount;\n')
cfile.write ('}\n')

cfile.close ()

hfile = open (TB_HFILE, 'w')

hfile.write (LICENCE_HEADER)
hfile.write ('/********************************************\n')
hfile.write (' *            AUTOGENERATED FILE            *\n')
hfile.write (' *             DO NOT MODIFY IT             *\n')
hfile.write (' *                                          *\n')
hfile.write (' * To add new commands :                    *\n')
hfile.write (' *  - Modify ../Xml/commands.xml file       *\n')
hfile.write (' *  - Re-run generateCommandsList.py script *\n')
hfile.write (' *                                          *\n')
hfile.write (' ********************************************/\n')
hfile.write ('#ifndef ' + TB_DEFINE + '\n')
hfile.write ('#define ' + TB_DEFINE + ' (1)\n')
hfile.write ('\n')
hfile.write ('int ' + ARFunctionName (LIB_MODULE, TB_SUBMODULE, 'autoTest') + ' ();\n')
hfile.write ('\n')
hfile.write ('#endif /* ' + TB_DEFINE + ' */\n')

hfile.close ()

cfile = open (TB_LIN_CFILE, 'w')

cfile.write (LICENCE_HEADER)
cfile.write ('/********************************************\n')
cfile.write (' *            AUTOGENERATED FILE            *\n')
cfile.write (' *             DO NOT MODIFY IT             *\n')
cfile.write (' *                                          *\n')
cfile.write (' * To add new commands :                    *\n')
cfile.write (' *  - Modify ../Xml/commands.xml file       *\n')
cfile.write (' *  - Re-run generateCommandsList.py script *\n')
cfile.write (' *                                          *\n')
cfile.write (' ********************************************/\n')
cfile.write ('#include "' + TB_HFILE_NAME + '"\n')
cfile.write ('\n')
cfile.write ('int main (int argc, char *argv[])\n')
cfile.write ('{\n')
cfile.write ('    return ' + ARFunctionName (LIB_MODULE, TB_SUBMODULE, 'autoTest') + ' ();\n')
cfile.write ('}\n')

cfile.close ()

#################################
# 12TH PART :                   #
#################################
# Generate JNI C/Java code      #
#################################

def interfaceName (proj, cls, cmd):
    return JNIClassName + ARCapitalize (proj.name) + ARCapitalize (cls.name) + ARCapitalize (cmd.name) + 'Listener'
def interfaceVar (proj, cls, cmd):
    return '_' + interfaceName (proj,cls,cmd)
def javaCbName (proj, cls, cmd):
    return 'on' + ARCapitalize (proj.name) + ARCapitalize (cls.name) + ARCapitalize (cmd.name) + 'Update'

for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            jfile = open (JNIJ_OUT_DIR + interfaceName (proj,cl,cmd) + '.java', 'w')
            jfile.write (LICENCE_HEADER)
            jfile.write ('package ' + JNI_PACKAGE_NAME + ';\n')
            jfile.write ('\n')
            jfile.write ('/**\n')
            jfile.write (' * Interface for the command <code>' + ARCapitalize (cmd.name) + '</code> of class <code>' + ARCapitalize (cl.name) + '</code> in project <code>' + ARCapitalize (proj.name) + '</code> listener\n')
            jfile.write (' * @author Parrot (c) 2013\n')
            jfile.write (' */\n')
            jfile.write ('public interface ' + interfaceName (proj,cl,cmd) + ' {\n')
            jfile.write ('\n')
            jfile.write ('    /**\n')
            jfile.write ('     * Called when a command <code>' + ARCapitalize (cmd.name) + '</code> of class <code>' + ARCapitalize (cl.name) + '</code> in project <code>' + ARCapitalize (proj.name) + '</code> is decoded\n')
            for arg in cmd.args:
                for comm in arg.comments:
                    jfile.write ('     * @param _' + arg.name + ' ' + comm + '\n')
            jfile.write ('     */\n')
            jfile.write ('    void ' + javaCbName (proj,cl,cmd) + ' (')
            first = True
            for arg in cmd.args:
                if first:
                    first = False
                else:
                    jfile.write (', ')
                jfile.write (xmlToJava (proj, cl, cmd, arg) + ' ' + arg.name)
            jfile.write (');\n')
            jfile.write ('}\n')
            jfile.close ()

jfile = open (JNI_JFILE, 'w')

jfile.write (LICENCE_HEADER)
jfile.write ('package ' + JNI_PACKAGE_NAME + ';\n')
jfile.write ('\n')
jfile.write ('import ' + SDK_PACKAGE_ROOT + 'arsal.ARNativeData;\n')
jfile.write ('\n')
jfile.write ('/**\n')
jfile.write (' * Java representation of a C ' + JNIClassName + ' object.<br>\n')
jfile.write (' * This class holds either app-generated objects, that are to be sent\n')
jfile.write (' * to the device, or network-generated objects, that are to be decoded by\n')
jfile.write (' * the application.\n')
jfile.write (' * @author Parrot (c) 2013\n')
jfile.write (' */\n')
jfile.write ('public class ' + JNIClassName + ' extends ARNativeData {\n')
jfile.write ('\n')
jfile.write ('    public static final int ' + ARMacroName (LIB_MODULE, JNIClassName, 'HEADER_SIZE') + ' = 4;\n')
jfile.write ('    public static final boolean ' + ARMacroName (LIB_MODULE, JNIClassName, 'HAS_DEBUG_COMMANDS') + ' = ')
if genDebug:
    jfile.write ('true;\n')
else:
    jfile.write ('false;\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Creates a new, empty ' + JNIClassName + ' with the default size.<br>\n')
jfile.write ('     * This is a typical constructor for app-generated ' + JNIClassName + '.<br>\n')
jfile.write ('     * To optimize memory, the application can reuse an ' + JNIClassName + '\n')
jfile.write ('     * object after it was disposed.\n')
jfile.write ('     */\n')
jfile.write ('    public ' + JNIClassName + ' () {\n')
jfile.write ('        super ();\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Creates a new, empty ' + JNIClassName + ' with an user-specified size.<br>\n')
jfile.write ('     * This is a typical constructor for app-generated ' + JNIClassName + '.<br>\n')
jfile.write ('     * To optimize memory, the application can reuse an ' + JNIClassName + '\n')
jfile.write ('     * object after it was disposed.\n')
jfile.write ('     * @param capacity user specified capacity of the command buffer\n')
jfile.write ('     */\n')
jfile.write ('    public ' + JNIClassName + ' (int capacity) {\n')
jfile.write ('        super (capacity);\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Creates a new ' + JNIClassName + ' from another ARNativeData instance.<br>\n')
jfile.write ('     * This is a typical constructor for network-generated ' + JNIClassName + '.<br>\n')
jfile.write ('     * To optimize memory, the application can reuse an ' + JNIClassName + '\n')
jfile.write ('     * object after it was disposed.\n')
jfile.write ('     * @param oldData ARNativeData which contains original data\n')
jfile.write ('     */\n')
jfile.write ('    public ' + JNIClassName + ' (ARNativeData oldData) {\n')
jfile.write ('        super (oldData);\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Creates a new ' + JNIClassName + ' from a c pointer and size.<br>\n')
jfile.write ('     * To optimize memory, the application can reuse an ' + JNIClassName + '\n')
jfile.write ('     * object after it was disposed.\n')
jfile.write ('     * @param data The original data buffer to copy\n')
jfile.write ('     * @param dataSize The original data buffer size\n')
jfile.write ('     */\n')
jfile.write ('    public ' + JNIClassName + ' (long data, int dataSize) {\n')
jfile.write ('        super (data, dataSize);\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Creates a new ' + JNIClassName + ' from another ARNativeData, with a given minimum capacity.<br>\n')
jfile.write ('     * This is a typical constructor for network-generated ' + JNIClassName + '.<br>\n')
jfile.write ('     * To optimize memory, the application can reuse an ' + JNIClassName + '\n')
jfile.write ('     * object after it was disposed.\n')
jfile.write ('     * @param oldData ARNativeData which contains original data\n')
jfile.write ('     * @param capacity Minimum capacity of this object\n')
jfile.write ('     */\n')
jfile.write ('    public ' + JNIClassName + ' (ARNativeData oldData, int capacity) {\n')
jfile.write ('        super (oldData, capacity);\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Describe a ' + JNIClassName + '.<br>\n')
jfile.write ('     * @return A String describing the ' + JNIClassName + ', with arguments values included\n')
jfile.write ('     */\n')
jfile.write ('    public String toString () {\n')
jfile.write ('        return nativeToString (pointer, used);\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Try to describe an ARNativeData as if it was an ' + JNIClassName + '.<br>\n')
jfile.write ('     * @return A String describing the ARNativeData, if possible as an ' + JNIClassName + '.\n')
jfile.write ('     */\n')
jfile.write ('    public static String arNativeDataToARCommandString (ARNativeData data) {\n')
jfile.write ('        if (data == null) { return "null"; }\n')
jfile.write ('        String ret = nativeStaticToString(data.getData(), data.getDataSize());\n')
jfile.write ('        if (ret == null) { ret = data.toString(); }\n')
jfile.write ('        return ret;\n');
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Decodes the current ' + JNIClassName + ', calling commands listeners<br>\n')
jfile.write ('     * If a listener was set for the Class/Command contained within the ' + JNIClassName + ',\n')
jfile.write ('     * its <code>onClassCommandUpdate(...)</code> function will be called in the current thread.\n')
jfile.write ('     * @return An ' + ARJavaEnumType (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + ' error code\n')
jfile.write ('     */\n')
jfile.write ('    public ' + ARJavaEnumType (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + ' decode () {\n')
jfile.write ('        ' + ARJavaEnumType (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + ' err = ' + ARJavaEnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'ERROR') + ';\n')
jfile.write ('        if (!valid) {\n')
jfile.write ('            return err;\n')
jfile.write ('        }\n')
jfile.write ('        int errInt = nativeDecode (pointer, used);\n')
jfile.write ('        if (' + ARJavaEnumType (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + '.getFromValue (errInt) != null) {\n')
jfile.write ('            err = ' + ARJavaEnumType (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + '.getFromValue (errInt);\n')
jfile.write ('        }\n')
jfile.write ('        return err;\n')
jfile.write ('    }\n')
jfile.write ('\n')
for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            jfile.write ('    /**\n')
            jfile.write ('     * Set an ' + JNIClassName + ' to hold the command <code>' + ARCapitalize (cmd.name) + '</code> of class <code>' + ARCapitalize (cl.name) + '</code> in project <code>' + ARCapitalize (proj.name) + '</code><br>\n')
            jfile.write ('     * <br>\n')
            jfile.write ('     * Project ' + ARCapitalize (proj.name) + ' description:<br>\n')
            for comm in proj.comments:
                jfile.write ('     * ' + comm + '<br>\n')
            jfile.write ('     * <br>\n')
            jfile.write ('     * Class ' + ARCapitalize (cl.name) + ' description:<br>\n')
            for comm in cl.comments:
                jfile.write ('     * ' + comm + '<br>\n')
            jfile.write ('     * <br>\n')
            jfile.write ('     * Command ' + ARCapitalize (cmd.name) + ' description:<br>\n')
            for comm in cmd.comments:
                jfile.write ('     * ' + comm + '<br>\n')
            jfile.write ('     * <br>\n')
            jfile.write ('     * This function reuses the current ' + JNIClassName + ', replacing its content with a\n')
            jfile.write ('     * new command created from the current params\n')
            for arg in cmd.args:
                for comm in arg.comments:
                    jfile.write ('     * @param _' + arg.name + ' ' + comm + '\n')
            jfile.write ('     * @return An ' + ARJavaEnumType (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + ' error code.\n')
            jfile.write ('     */\n')
            jfile.write ('    public ' + ARJavaEnumType (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + ' set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + ' (')
            first = True
            for arg in cmd.args:
                if first:
                    first = False
                else:
                    jfile.write (', ')
                jfile.write (xmlToJava (proj, cl, cmd, arg) + ' ' + arg.name)
            jfile.write (') {\n')
            jfile.write ('        ' + ARJavaEnumType (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + ' err = ' + ARJavaEnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'ERROR') + ';\n')
            jfile.write ('        if (!valid) {\n')
            jfile.write ('            return err;\n')
            jfile.write ('        }\n')
            jfile.write ('        int errInt = nativeSet' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + ' (pointer, capacity')
            for arg in cmd.args:
                jfile.write (', ' + arg.name)
            jfile.write (');\n')
            jfile.write ('        if (' + ARJavaEnumType (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + '.getFromValue (errInt) != null) {\n')
            jfile.write ('            err = ' + ARJavaEnumType (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + '.getFromValue (errInt);\n')
            jfile.write ('        }\n')
            jfile.write ('        return err;\n')
            jfile.write ('    }\n')
            jfile.write ('\n')


for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            jfile.write ('    private static ' + interfaceName (proj,cl,cmd) + ' ' + interfaceVar (proj,cl,cmd) + ' = null;\n')
            jfile.write ('\n')
            jfile.write ('    /**\n')
            jfile.write ('     * Set the listener for the command <code>' + ARCapitalize (cmd.name) + '</code> of class <code>' + ARCapitalize (cl.name) + '</code> in project <code>' + ARCapitalize (proj.name) + '</code><br>\n')
            jfile.write ('     * Listeners are static to the class, and are not to be set on every object\n')
            jfile.write ('     * @param ' + interfaceVar (proj,cl,cmd) + '_PARAM New listener for the command\n')
            jfile.write ('     */\n')
            jfile.write ('    public static void set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Listener (' + interfaceName (proj,cl,cmd) + ' ' + interfaceVar (proj,cl,cmd) + '_PARAM) {\n')
            jfile.write ('        ' + interfaceVar (proj,cl,cmd) + ' = ' + interfaceVar (proj,cl,cmd) + '_PARAM;\n')
            jfile.write ('    }\n')
            jfile.write ('\n')
        jfile.write ('\n')
    jfile.write ('\n')
jfile.write ('\n')
jfile.write ('    private native String  nativeToString (long jpdata, int jdataSize);\n')
jfile.write ('    private static native String  nativeStaticToString (long jpdata, int jdataSize);\n')
jfile.write ('    private native int     nativeDecode (long jpdata, int jdataSize);\n')
jfile.write ('\n')
for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            jfile.write ('    private native int     nativeSet' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + ' (long pdata, int dataTotalLength')
            for arg in cmd.args:
                jfile.write (', ' + xmlToJava (proj, cl, cmd, arg) + ' ' + arg.name)
            jfile.write (');\n')
        jfile.write ('\n')
    jfile.write ('\n')
jfile.write ('}\n')

jfile.close ()

jfile = open (JNI_FILTER_JFILE, 'w')

jfile.write (LICENCE_HEADER)
jfile.write ('package ' + JNI_PACKAGE_NAME + ';\n')
jfile.write ('\n')
jfile.write ('import com.parrot.arsdk.arsal.ARSALPrint;\n')
jfile.write ('\n')
jfile.write ('/**\n')
jfile.write (' * Java implementation of a C ' + JNIFilterClassName + ' object.<br>\n')
jfile.write (' * @author Parrot (c) 2014\n')
jfile.write (' */\n')
jfile.write ('public class ' + JNIFilterClassName + '\n')
jfile.write ('{\n')
jfile.write ('    private long cFilter;\n')
jfile.write ('    private boolean valid;\n')
jfile.write ('    private static final String TAG = ' + JNIFilterClassName + '.class.getSimpleName();\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Creates a new ' + JNIFilterClassName + ' which allows all commands.\n')
jfile.write ('     */\n')
jfile.write ('    public ' + JNIFilterClassName + ' () {\n')
jfile.write ('        this(ARCOMMANDS_FILTER_STATUS_ENUM.ARCOMMANDS_FILTER_STATUS_ALLOWED);\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Creates a new ' + JNIFilterClassName + ' with the given default behavior.\n')
jfile.write ('     * @param behavior The default behavior of the filter.\n')
jfile.write ('     * @warning Only ALLOWED and BLOCK are allowed as default behavior. Providing any other value will create an invalid object.\n')
jfile.write ('     */\n')
jfile.write ('    public ' + JNIFilterClassName + ' (ARCOMMANDS_FILTER_STATUS_ENUM behavior) {\n')
jfile.write ('        this.cFilter = nativeNewFilter (behavior.getValue());\n')
jfile.write ('        this.valid = (this.cFilter != 0);\n')
jfile.write ('        if (! this.valid) {\n')
jfile.write ('            dispose();\n')
jfile.write ('        }\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Checks the object validity.\n')
jfile.write ('     * @return <code>true</code> if the object is valid<br><code>false</code> if the object is invalid.\n')
jfile.write ('     */\n')
jfile.write ('    public boolean isValid () {\n')
jfile.write ('        return valid;\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Marks a ' + JNIFilterClassName + ' as unused (so C-allocated memory can be freed)<br>\n')
jfile.write ('     * A disposed ' + JNIFilterClassName + ' is marked as invalid.\n')
jfile.write ('     */\n')
jfile.write ('    public void dispose () {\n')
jfile.write ('        if (valid) {\n')
jfile.write ('            nativeDeleteFilter (cFilter);\n')
jfile.write ('        }\n')
jfile.write ('        this.valid = false;\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Gets the native pointer for this filter\n')
jfile.write ('     * @return The pointer.\n')
jfile.write ('     */\n')
jfile.write ('    public long getFilter () {\n')
jfile.write ('        return cFilter;\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    protected void finalize () throws Throwable {\n')
jfile.write ('        try {\n')
jfile.write ('            if (valid) {\n')
jfile.write ('                ARSALPrint.e (TAG, this + ": Finalize error -> dispose () was not called !");\n')
jfile.write ('                dispose ();\n')
jfile.write ('            }\n')
jfile.write ('        }\n')
jfile.write ('        finally {\n')
jfile.write ('            super.finalize ();\n')
jfile.write ('        }\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    /**\n')
jfile.write ('     * Filters a command.<br>\n')
jfile.write ('     * This function returns the filter behavior for the given ' + JNIClassName + '.<br>\n')
jfile.write ('     * @param command The command to be filtered.\n')
jfile.write ('     * @return The filter status.\n')
jfile.write ('     */\n')
jfile.write ('    public ARCOMMANDS_FILTER_STATUS_ENUM filterCommand (' + JNIClassName + ' command) {\n')
jfile.write ('        if (! valid) { return ARCOMMANDS_FILTER_STATUS_ENUM.ARCOMMANDS_FILTER_STATUS_ERROR; }\n')
jfile.write ('        int cStatus = nativeFilterCommand (cFilter, command.getData(), command.getDataSize());\n')
jfile.write ('        return ARCOMMANDS_FILTER_STATUS_ENUM.getFromValue(cStatus);\n')
jfile.write ('    }\n')
jfile.write ('\n')
jfile.write ('    private native long nativeNewFilter (int behavior);\n')
jfile.write ('    private native void nativeDeleteFilter (long cFilter);\n')
jfile.write ('    private native int nativeFilterCommand (long cFilter, long command, int len);\n')
jfile.write ('\n')
for proj in allProjects:
    jfile.write ('    // Project ' + proj.name + '\n')
    jfile.write ('    // - Class ' + cl.name + '\n')
    jfile.write ('    private native int nativeSet' + ARCapitalize(proj.name) + 'Behavior (long cFilter, int behavior);\n')
    jfile.write ('    /**\n')
    jfile.write ('     * Sets the behavior for all commands ' + ARCapitalize(proj.name) + '.XXX.XXX.\n')
    jfile.write ('     * @param behavior The behavior to set.\n')
    jfile.write ('     * @return An ARCOMMANDS_FILTER_ERROR_ENUM value.\n')
    jfile.write ('     */\n')
    jfile.write ('    public ARCOMMANDS_FILTER_ERROR_ENUM set' + ARCapitalize(proj.name) + 'Behavior (ARCOMMANDS_FILTER_STATUS_ENUM behavior) {\n')
    jfile.write ('        if (! valid) { return ARCOMMANDS_FILTER_ERROR_ENUM.ARCOMMANDS_FILTER_ERROR_BAD_FILTER; }\n')
    jfile.write ('        int cErr = nativeSet' + ARCapitalize(proj.name) + 'Behavior (this.cFilter, behavior.getValue());\n')
    jfile.write ('        return ARCOMMANDS_FILTER_ERROR_ENUM.getFromValue(cErr);\n')
    jfile.write ('    }\n')
    jfile.write ('\n')
        
    for cl in proj.classes:
        jfile.write ('    // - Class ' + cl.name + '\n')
        jfile.write ('    private native int nativeSet' + ARCapitalize(proj.name) + ARCapitalize(cl.name)  + 'Behavior (long cFilter, int behavior);\n')
        jfile.write ('    /**\n')
        jfile.write ('     * Sets the behavior for all commands ' + ARCapitalize(proj.name) + '.' + ARCapitalize(cl.name) + '.XXX.\n')
        jfile.write ('     * @param behavior The behavior to set.\n')
        jfile.write ('     * @return An ARCOMMANDS_FILTER_ERROR_ENUM value.\n')
        jfile.write ('     */\n')
        jfile.write ('    public ARCOMMANDS_FILTER_ERROR_ENUM set' + ARCapitalize(proj.name) + ARCapitalize(cl.name)  + 'Behavior (ARCOMMANDS_FILTER_STATUS_ENUM behavior) {\n')
        jfile.write ('        if (! valid) { return ARCOMMANDS_FILTER_ERROR_ENUM.ARCOMMANDS_FILTER_ERROR_BAD_FILTER; }\n')
        jfile.write ('        int cErr = nativeSet' + ARCapitalize(proj.name) + ARCapitalize(cl.name) + 'Behavior (this.cFilter, behavior.getValue());\n')
        jfile.write ('        return ARCOMMANDS_FILTER_ERROR_ENUM.getFromValue(cErr);\n')
        jfile.write ('    }\n')
        jfile.write ('\n')
            
        for cmd in cl.cmds:
            jfile.write ('    private native int nativeSet' + ARCapitalize(proj.name) + ARCapitalize(cl.name) + ARCapitalize(cmd.name) + 'Behavior (long cFilter, int behavior);\n')
            jfile.write ('    /**\n')
            jfile.write ('     * Sets the behavior for the command ' + ARCapitalize(proj.name) + '.' + ARCapitalize(cl.name) + '.' + ARCapitalize(cmd.name) + '.\n')
            jfile.write ('     * @param behavior The behavior to set.\n')
            jfile.write ('     * @return An ARCOMMANDS_FILTER_ERROR_ENUM value.\n')
            jfile.write ('     */\n')
            jfile.write ('    public ARCOMMANDS_FILTER_ERROR_ENUM set' + ARCapitalize(proj.name) + ARCapitalize(cl.name) + ARCapitalize(cmd.name) + 'Behavior (ARCOMMANDS_FILTER_STATUS_ENUM behavior) {\n')
            jfile.write ('        if (! valid) { return ARCOMMANDS_FILTER_ERROR_ENUM.ARCOMMANDS_FILTER_ERROR_BAD_FILTER; }\n')
            jfile.write ('        int cErr = nativeSet' + ARCapitalize(proj.name) + ARCapitalize(cl.name) + ARCapitalize(cmd.name) + 'Behavior (this.cFilter, behavior.getValue());\n')
            jfile.write ('        return ARCOMMANDS_FILTER_ERROR_ENUM.getFromValue(cErr);\n')
            jfile.write ('    }\n')
            jfile.write ('\n')
        jfile.write ('\n')
    jfile.write ('\n')
jfile.write ('}\n')

jfile.close ()

cfile = open (JNI_CFILE, 'w')

JNI_FUNC_PREFIX='Java_' + JNI_PACKAGE_NAME.replace ('.', '_') + '_'
JNI_FIRST_ARGS='JNIEnv *env, jobject thizz'
JNI_FIRST_ARGS_STATIC='JNIEnv *env, jclass clazz'

cfile.write (LICENCE_HEADER)
cfile.write ('/********************************************\n')
cfile.write (' *            AUTOGENERATED FILE            *\n')
cfile.write (' *             DO NOT MODIFY IT             *\n')
cfile.write (' *                                          *\n')
cfile.write (' * To add new commands :                    *\n')
cfile.write (' *  - Modify ../../Xml/commands.xml file    *\n')
cfile.write (' *  - Re-run generateCommandsList.py script *\n')
cfile.write (' *                                          *\n')
cfile.write (' ********************************************/\n')
cfile.write ('#include <' + COMMANDSGEN_HFILE_NAME + '>\n')
cfile.write ('#include <' + COMMANDSDEC_HFILE_NAME + '>\n')
cfile.write ('#include <jni.h>\n')
cfile.write ('#include <stdlib.h>\n')
cfile.write ('\n')
cfile.write ('#define TOSTRING_STRING_SIZE (1024)\n')
cfile.write ('\n')
cfile.write ('static jfieldID g_dataSize_id = 0;\n')
cfile.write ('static JavaVM *g_vm = NULL;\n')
cfile.write ('\n')
cfile.write ('JNIEXPORT jstring JNICALL\n')
cfile.write (JNI_FUNC_PREFIX + JNIClassName + '_nativeToString (' + JNI_FIRST_ARGS + ', jlong jpdata, jint jdataSize)\n')
cfile.write ('{\n')
cfile.write ('    jstring ret = NULL;\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + ' err = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ';\n')
cfile.write ('    char *cstr = calloc (TOSTRING_STRING_SIZE, 1);\n')
cfile.write ('    if (cstr == NULL)\n')
cfile.write ('    {\n')
cfile.write ('        return ret;\n')
cfile.write ('    }\n')
cfile.write ('    err = ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'DescribeBuffer') + ' ((uint8_t *)(intptr_t)jpdata, jdataSize, cstr, TOSTRING_STRING_SIZE);\n')
cfile.write ('    if (err == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        ret = (*env)->NewStringUTF(env, cstr);\n')
cfile.write ('    }\n')
cfile.write ('    free (cstr);\n')
cfile.write ('    return ret;\n')
cfile.write ('}\n')
cfile.write ('JNIEXPORT jstring JNICALL\n')
cfile.write (JNI_FUNC_PREFIX + JNIClassName + '_nativeStaticToString (' + JNI_FIRST_ARGS_STATIC + ', jlong jpdata, jint jdataSize)\n')
cfile.write ('{\n')
cfile.write ('    jstring ret = NULL;\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + ' err = ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ';\n')
cfile.write ('    char *cstr = calloc (TOSTRING_STRING_SIZE, 1);\n')
cfile.write ('    if (cstr == NULL)\n')
cfile.write ('    {\n')
cfile.write ('        return ret;\n')
cfile.write ('    }\n')
cfile.write ('    err = ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'DescribeBuffer') + ' ((uint8_t *)(intptr_t)jpdata, jdataSize, cstr, TOSTRING_STRING_SIZE);\n')
cfile.write ('    if (err == ' + AREnumValue (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME, 'OK') + ')\n')
cfile.write ('    {\n')
cfile.write ('        ret = (*env)->NewStringUTF(env, cstr);\n')
cfile.write ('    }\n')
cfile.write ('    free (cstr);\n')
cfile.write ('    return ret;\n')
cfile.write ('}\n')
cfile.write ('\n')
cfile.write ('JNIEXPORT jint JNICALL\n')
cfile.write (JNI_FUNC_PREFIX + JNIClassName + '_nativeDecode (' + JNI_FIRST_ARGS + ', jlong jpdata, jint jdataSize)\n')
cfile.write ('{\n')
cfile.write ('    uint8_t *pdata = (uint8_t *) (intptr_t)jpdata;\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, DEC_SUBMODULE, DEC_ERR_ENAME) + ' err = ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'DecodeBuffer') + ' (pdata, jdataSize);\n')
cfile.write ('    return err;\n')
cfile.write ('}\n')
cfile.write ('\n')
for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            cfile.write ('JNIEXPORT jint JNICALL\n')
            cfile.write (JNI_FUNC_PREFIX + JNIClassName + '_nativeSet' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + ' (' + JNI_FIRST_ARGS + ', jlong c_pdata, jint dataLen')
            for arg in cmd.args:
                cfile.write (', ' + xmlToJni (proj, cl, cmd, arg) + ' ' + arg.name)
            cfile.write (')\n')
            cfile.write ('{\n')
            cfile.write ('    int32_t c_dataSize = 0;\n')
            cfile.write ('    ' + AREnumName (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME) + ' err = ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'ERROR') + ';\n');
            cfile.write ('    if (g_dataSize_id == 0)\n')
            cfile.write ('    {\n')
            cfile.write ('        jclass clz = (*env)->GetObjectClass (env, thizz);\n')
            cfile.write ('        if (clz != 0)\n')
            cfile.write ('        {\n')
            cfile.write ('            g_dataSize_id = (*env)->GetFieldID (env, clz, "used", "I");\n')
            cfile.write ('            (*env)->DeleteLocalRef (env, clz);\n')
            cfile.write ('        }\n')
            cfile.write ('        else\n')
            cfile.write ('        {\n')
            cfile.write ('            return err;\n')
            cfile.write ('        }\n')
            cfile.write ('    }\n')
            cfile.write ('\n')
            for arg in cmd.args:
                if 'string' == arg.type:
                    cfile.write ('    const char *c_' + arg.name + ' = (*env)->GetStringUTFChars (env, ' + arg.name + ', NULL);\n')
                elif 'enum' == arg.type:
                    cfile.write ('    jclass j_' + arg.name + '_class = (*env)->FindClass (env, "' + jniEnumClassName (proj, cl, cmd, arg) + '");\n')
                    cfile.write ('    jmethodID j_' + arg.name + '_mid = (*env)->GetMethodID (env, j_' + arg.name + '_class, "getValue", "()I");\n')
                    cfile.write ('    jint j_' + arg.name + '_enum = (*env)->CallIntMethod (env, ' + arg.name + ', j_' + arg.name + '_mid);\n')
            cfile.write ('    err = ' + ARFunctionName (LIB_MODULE, GEN_SUBMODULE, 'Generate' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name)) + ' ((uint8_t *) (intptr_t) c_pdata, dataLen, &c_dataSize')
            for arg in cmd.args:
                if 'string' == arg.type:
                    cfile.write (', c_' + arg.name)
                elif 'enum' == arg.type:
                    cfile.write (', j_' + arg.name + '_enum')
                else:
                    cfile.write (', (' + xmlToC (proj, cl, cmd, arg) + ')' + arg.name)
            cfile.write (');\n')
            for arg in cmd.args:
                if 'string' == arg.type:
                    cfile.write ('    (*env)->ReleaseStringUTFChars (env, ' + arg.name + ', c_' + arg.name + ');\n')
                elif 'enum' == arg.type:
                    cfile.write ('    (*env)->DeleteLocalRef (env, j_' + arg.name + '_class);\n')
            cfile.write ('    if (err == ' + AREnumValue (LIB_MODULE, GEN_SUBMODULE, GEN_ERR_ENAME, 'OK') + ')\n')
            cfile.write ('    {\n')
            cfile.write ('        (*env)->SetIntField (env, thizz, g_dataSize_id, (jint)c_dataSize);\n')
            cfile.write ('    }\n')
            cfile.write ('    return err;\n')
            cfile.write ('}\n')
            cfile.write ('\n')
        cfile.write ('\n')
    cfile.write ('\n')

def cCallbackName (proj,cls,cmd):
    return ARFunctionName (LIB_MODULE, JNI_SUBMODULE, ARCapitalize (proj.name) + ARCapitalize (cls.name) + ARCapitalize (cmd.name) + 'nativeCb')

for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            cfile.write ('void ' + cCallbackName (proj,cl,cmd) + ' (')
            for arg in cmd.args:
                cfile.write (xmlToC (proj, cl, cmd, arg) + ' ' + arg.name + ', ')
            cfile.write ('void *custom)\n')
            cfile.write ('{\n')
            cfile.write ('    jclass clazz = (jclass)custom;\n')
            cfile.write ('    jint res;\n')
            cfile.write ('    JNIEnv *env = NULL;\n')
            cfile.write ('    res = (*g_vm)->GetEnv (g_vm, (void **)&env, JNI_VERSION_1_6);\n')
            cfile.write ('    if (res < 0) { return; }\n')
            cfile.write ('    jfieldID delegate_fid = (*env)->GetStaticFieldID (env, clazz, "' + interfaceVar (proj,cl,cmd) + '", "L' + JNI_PACKAGE_NAME.replace ('.', '/') + '/' + interfaceName (proj,cl,cmd) + ';");\n')
            cfile.write ('    jobject delegate = (*env)->GetStaticObjectField (env, clazz, delegate_fid);\n')
            cfile.write ('    if (delegate == NULL) { return; }\n')
            cfile.write ('\n')
            cfile.write ('    jclass d_clazz = (*env)->GetObjectClass (env, delegate);\n')
            cfile.write ('    jmethodID d_methodid = (*env)->GetMethodID (env, d_clazz, "' + javaCbName (proj,cl,cmd) + '", "(')
            for arg in cmd.args:
                cfile.write ('' + xmlToJavaSig (proj, cl, cmd, arg))
            cfile.write (')V");\n')
            cfile.write ('    (*env)->DeleteLocalRef (env, d_clazz);\n')
            cfile.write ('    if (d_methodid != NULL)\n')
            cfile.write ('    {\n')
            for arg in cmd.args:
                if 'string' == arg.type:
                    cfile.write ('        jstring j_' + arg.name + ' = (*env)->NewStringUTF (env, ' + arg.name + ');\n')
                elif 'enum' == arg.type:
                    cfile.write ('        jclass j_' + arg.name + '_class = (*env)->FindClass (env, "' + jniEnumClassName (proj, cl, cmd, arg) + '");\n')
                    cfile.write ('        jmethodID j_' + arg.name + '_mid = (*env)->GetStaticMethodID (env, j_' + arg.name + '_class, "getFromValue", "(I)' + xmlToJavaSig(proj, cl, cmd, arg) + '");\n')
                    cfile.write ('        jobject j_' + arg.name + '_enum = (*env)->CallStaticObjectMethod (env, j_' + arg.name + '_class, j_' + arg.name + '_mid, ' + arg.name + ');\n')
            cfile.write ('        (*env)->CallVoidMethod (env, delegate, d_methodid')
            for arg in cmd.args:
                if 'string' == arg.type:
                    cfile.write (', j_' + arg.name)
                elif 'enum' == arg.type:
                    cfile.write (', j_' + arg.name + '_enum')
                else:
                    cfile.write (', ' + xmlToJniCast(proj, cl, cmd, arg) + arg.name)
            cfile.write (');\n')
            for arg in cmd.args:
                if 'string' == arg.type:
                    cfile.write ('        (*env)->DeleteLocalRef (env, j_' + arg.name + ');\n')
                elif 'enum' == arg.type:
                    cfile.write ('        (*env)->DeleteLocalRef (env, j_' + arg.name + '_class);\n')
                    cfile.write ('        (*env)->DeleteLocalRef (env, j_' + arg.name + '_enum);\n')
            cfile.write ('    }\n')
            cfile.write ('    (*env)->DeleteLocalRef (env, delegate);\n')
            cfile.write ('}\n')
            cfile.write ('\n')
        cfile.write ('\n')
    cfile.write ('\n')

cfile.write ('JNIEXPORT jint JNICALL\n')
cfile.write ('JNI_OnLoad (JavaVM *vm, void *reserved)\n')
cfile.write ('{\n')
cfile.write ('    g_vm = vm;\n')
cfile.write ('    JNIEnv *env = NULL;\n')
cfile.write ('    if ((*vm)->GetEnv (vm, (void **)&env, JNI_VERSION_1_6) != JNI_OK)\n')
cfile.write ('    {\n')
cfile.write ('        return -1;\n')
cfile.write ('    }\n')
cfile.write ('    jclass clazz = (*env)->FindClass (env, "' + JNI_PACKAGE_NAME.replace ('.', '/') + '/' + JNIClassName + '");\n')
cfile.write ('    if (clazz == NULL)\n')
cfile.write ('    {\n')
cfile.write ('        return -1;\n')
cfile.write ('    }\n')
cfile.write ('    jclass g_class = (*env)->NewGlobalRef (env, clazz);\n')
cfile.write ('    if (g_class == NULL)\n')
cfile.write ('    {\n')
cfile.write ('        return -1;\n')
cfile.write ('    }\n')
cfile.write ('\n')
for proj in allProjects:
    for cl in proj.classes:
        for cmd in cl.cmds:
            cfile.write ('    ' + ARFunctionName (LIB_MODULE, DEC_SUBMODULE, 'Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Callback') + ' (' + cCallbackName (proj,cl,cmd) + ', (void *)g_class);\n')
        cfile.write ('\n')
    cfile.write ('\n')
cfile.write ('\n')
cfile.write ('    return JNI_VERSION_1_6;\n')
cfile.write ('}\n')
cfile.write ('/* END OF GENERAED CODE */\n')

cfile.close ()

cfile = open (JNI_FILTER_CFILE, 'w')

cfile.write (LICENCE_HEADER)
cfile.write ('/********************************************\n')
cfile.write (' *            AUTOGENERATED FILE            *\n')
cfile.write (' *             DO NOT MODIFY IT             *\n')
cfile.write (' *                                          *\n')
cfile.write (' * To add new commands :                    *\n')
cfile.write (' *  - Modify ../../Xml/commands.xml file    *\n')
cfile.write (' *  - Re-run generateCommandsList.py script *\n')
cfile.write (' *                                          *\n')
cfile.write (' ********************************************/\n')
cfile.write ('#include <' + COMMANDSFIL_HFILE_NAME + '>\n')
cfile.write ('#include <jni.h>\n')
cfile.write ('#include <stdlib.h>\n')
cfile.write ('\n')
cfile.write ('JNIEXPORT jlong JNICALL\n')
cfile.write (JNI_FUNC_PREFIX + JNIFilterClassName + '_nativeNewFilter(' + JNI_FIRST_ARGS + ', jint behavior)\n')
cfile.write ('{\n')
cfile.write ('    ARCOMMANDS_Filter_t *filter = ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'NewFilter') + ' (behavior, NULL);\n')
cfile.write ('    return (jlong)(intptr_t)filter;\n')
cfile.write ('}\n')
cfile.write ('\n')
cfile.write ('JNIEXPORT void JNICALL\n')
cfile.write (JNI_FUNC_PREFIX + JNIFilterClassName + '_nativeDeleteFilter(' + JNI_FIRST_ARGS + ', jlong cFilter)\n')
cfile.write ('{\n')
cfile.write ('    ARCOMMANDS_Filter_t *filter = (ARCOMMANDS_Filter_t *)(intptr_t)cFilter;\n')
cfile.write ('    ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'DeleteFilter') + ' (&filter);\n')
cfile.write ('}\n')
cfile.write ('\n')
cfile.write ('JNIEXPORT jint JNICALL\n')
cfile.write (JNI_FUNC_PREFIX + JNIFilterClassName + '_nativeFilterCommand(' + JNI_FIRST_ARGS + ', jlong cFilter, jlong cCommand, jint len)\n')
cfile.write ('{\n')
cfile.write ('    ARCOMMANDS_Filter_t *filter = (ARCOMMANDS_Filter_t *)(intptr_t)cFilter;\n')
cfile.write ('    uint8_t *command = (uint8_t *)(intptr_t)cCommand;\n')
cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_STATUS_ENAME) + ' status = ' + ARFunctionName (LIB_MODULE, FIL_SUBMODULE, 'FilterCommand') + ' (filter, command, len, NULL);\n')
cfile.write ('    return (jint)status;\n')
cfile.write ('}\n')
cfile.write ('\n')
for proj in allProjects:
    cfile.write ('    // Project ' + proj.name + '\n')
    cfile.write ('JNIEXPORT jint JNICALL\n')
    cfile.write (JNI_FUNC_PREFIX + JNIFilterClassName + '_nativeSet' + ARCapitalize(proj.name) + 'Behavior (' + JNI_FIRST_ARGS + ', jlong cFilter, jint behavior)\n')
    cfile.write ('{\n')
    cfile.write ('    ARCOMMANDS_Filter_t *filter = (ARCOMMANDS_Filter_t *)(intptr_t)cFilter;\n')
    cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' err = ARCOMMANDS_Filter_Set' + ARCapitalize (proj.name) + 'Behavior (filter, behavior);\n')
    cfile.write ('    return (jint)err;\n')
    cfile.write ('}\n')
    cfile.write ('\n')
    for cl in proj.classes:
        cfile.write ('    // - Class ' + cl.name + '\n')
        cfile.write ('JNIEXPORT jint JNICALL\n')
        cfile.write (JNI_FUNC_PREFIX + JNIFilterClassName + '_nativeSet' + ARCapitalize(proj.name) + ARCapitalize(cl.name) + 'Behavior (' + JNI_FIRST_ARGS + ', jlong cFilter, jint behavior)\n')
        cfile.write ('{\n')
        cfile.write ('    ARCOMMANDS_Filter_t *filter = (ARCOMMANDS_Filter_t *)(intptr_t)cFilter;\n')
        cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' err = ARCOMMANDS_Filter_Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + 'Behavior (filter, behavior);\n')
        cfile.write ('    return (jint)err;\n')
        cfile.write ('}\n')
        cfile.write ('\n')
        for cmd in cl.cmds:
            cfile.write ('JNIEXPORT jint JNICALL\n')
            cfile.write (JNI_FUNC_PREFIX + JNIFilterClassName + '_nativeSet' + ARCapitalize(proj.name) + ARCapitalize(cl.name) + ARCapitalize(cmd.name) + 'Behavior (' + JNI_FIRST_ARGS + ', jlong cFilter, jint behavior)\n')
            cfile.write ('{\n')
            cfile.write ('    ARCOMMANDS_Filter_t *filter = (ARCOMMANDS_Filter_t *)(intptr_t)cFilter;\n')
            cfile.write ('    ' + AREnumName (LIB_MODULE, FIL_SUBMODULE, FIL_ERROR_ENAME) + ' err = ARCOMMANDS_Filter_Set' + ARCapitalize (proj.name) + ARCapitalize (cl.name) + ARCapitalize (cmd.name) + 'Behavior (filter, behavior);\n')
            cfile.write ('    return (jint)err;\n')
            cfile.write ('}\n')
            cfile.write ('\n')
        cfile.write ('\n')
    cfile.write ('\n')
cfile.write ('/* END OF GENERAED CODE */\n')

##################################
# 13TH PART :                    #
##################################
# Dump command tree as C structs #
##################################

def dump_enum_table(proj, cl, cmd, arg):
    table = 'static struct arsdk_enum %s_%s_%s_%s_enum_tab[] = {\n' % (proj.name, cl.name, cmd.name, arg.name)
    value = 0
    for enum in arg.enums:
        comment = enum.comments[0] if len(enum.comments) > 0 else ''
        table += '  {\n'
        table += '    .name = "%s",\n' % enum.name
        table += '    .value = %s,\n' % AREnumValue(LIB_MODULE,
                                                    proj.name.upper() + '_' +
                                                    cl.name.upper(),
                                                    cmd.name.upper() + '_' +
                                                    arg.name.upper(), enum.name)
        table += '    .comment = "%s"\n' % comment.replace('"', '\\"')
        table += '  },\n'
        value += 1
    table = table + '};\n'
    return table if len(arg.enums) > 0 else ''

def dump_arg_table(proj, cl, cmd):
    table = 'static struct arsdk_arg %s_%s_%s_arg_tab[] = {\n' % (proj.name,
                                                                  cl.name,
                                                                  cmd.name)
    for arg in cmd.args:
        comment = arg.comments[0] if len(arg.comments) > 0 else ''
        if len(arg.enums) > 0:
            enums = '%s_%s_%s_%s_enum_tab' % (proj.name,
                                              cl.name,
                                              cmd.name,
                                              arg.name)
            nenums = 'ARRAY_SIZE(%s)' % enums
        else:
            enums = 'NULL'
            nenums = '0'
        table += '  {\n'
        table += '    .name = "%s",\n' % arg.name
        table += '    .type = ARSDK_ARG_TYPE_%s,\n' % arg.type.upper()
        table += '    .enums = %s,\n' % enums
        table += '    .nenums = %s,\n' % nenums
        table += '    .comment = "%s"\n' % comment.replace('"', '\\"')
        table += '  },\n'
    table = table + '};\n'
    return table if len(cmd.args) > 0 else ''

def dump_cmd_table(proj, cl):
    table = 'static struct arsdk_cmd %s_%s_cmd_tab[] = {\n' % (proj.name,
                                                               cl.name)
    for cmd in cl.cmds:
        comment = cmd.comments[0] if len(cmd.comments) > 0 else ''
        if len(cmd.args) > 0:
            args = '%s_%s_%s_arg_tab' % (proj.name, cl.name, cmd.name)
            nargs = 'ARRAY_SIZE(%s)' % args
        else:
            args = 'NULL'
            nargs = '0'
        table += '  {\n'
        table += '    .name = "%s",\n' % cmd.name
        table += '    .id = %s,\n' % AREnumValue(LIB_MODULE,
                                                 ID_SUBMODULE,
                                                 proj.name + '_' + cl.name +
                                                 '_CMD', cmd.name)
        # ignore fields, .buf, .timeout, .listtype (are they used at all ?)
        table += '    .args = %s,\n' % args
        table += '    .nargs = %s,\n' % nargs
        table += '    .comment = "%s"\n' % comment.replace('"', '\\"')
        table += '  },\n'
    table = table + '};\n'
    return table if len(cl.cmds) > 0 else ''

def dump_class_table(proj):
    table = 'static struct arsdk_class %s_class_tab[] = {\n' % proj.name
    for cl in proj.classes:
        comment = cl.comments[0] if len(cl.comments) > 0 else ''
        if len(cl.cmds) > 0:
            cmds = proj.name + '_' + cl.name + '_cmd_tab'
            ncmds = 'ARRAY_SIZE(%s)' % cmds
        else:
            cmds = 'NULL'
            ncmds = '0'
        table += '  {\n'
        table += '    .name = "%s",\n' % cl.name
        table += '    .ident = %s,\n' % AREnumValue(LIB_MODULE,
                                                    ID_SUBMODULE,
                                                    proj.name + '_CLASS',
                                                    cl.name)
        table += '    .cmds = %s,\n' % cmds
        table += '    .ncmds = %s,\n' % ncmds
        table += '    .comment = "%s"\n' % comment.replace('"', '\\"')
        table += '  },\n'
    table = table + '};\n'
    return table if len(proj.classes) > 0 else ''

def dump_project_table(projects):
    table = 'static struct arsdk_project arsdk_projects[] = {\n'
    for proj in projects:
        comment = proj.comments[0] if len(proj.comments) > 0 else ''
        if len(proj.classes) > 0:
            classes = proj.name + '_class_tab'
            nclasses = 'ARRAY_SIZE(%s)' % classes
        else:
            classes = 'NULL'
            nclasses = '0'
        table += '  {\n'
        table += '    .name = "%s",\n' % proj.name
        table += '    .ident = %s,\n' % AREnumValue(LIB_MODULE,
                                                    ID_SUBMODULE,
                                                    'PROJECT',
                                                    proj.name)
        table += '    .classes = %s,\n' % classes
        table += '    .nclasses = %s,\n' % nclasses
        table += '    .comment = "%s"\n' % comment.replace('"', '\\"')
        table += '  },\n'
    table = table + '};\n'
    table += 'static const unsigned int arsdk_nprojects = '
    table += 'ARRAY_SIZE(arsdk_projects);\n'
    return table if len(projects) > 0 else ''

def dump_tree_header(filename):
    hfile = open (filename, 'w')
    hfile.write (LICENCE_HEADER)
    hfile.write ('/********************************************\n')
    hfile.write (' *            AUTOGENERATED FILE            *\n')
    hfile.write (' *             DO NOT MODIFY                *\n')
    hfile.write (' ********************************************/\n')
    hfile.write ('\n')
    hfile.write ('#define ARRAY_SIZE(_t) (sizeof(_t)/sizeof((_t)[0]))\n')
    hfile.write ('\n')
    hfile.write ('/**\n')
    hfile.write (' * @brief libARCommands Tree dump.\n')
    hfile.write (' * @note Autogenerated file\n')
    hfile.write (' **/\n')
    hfile.write ('#ifndef _ARSDK_ARCOMMANDS_TREE_H\n')
    hfile.write ('#define _ARSDK_ARCOMMANDS_TREE_H\n')
    hfile.write ('#include <inttypes.h>\n')
    hfile.write ('#include <stdlib.h>\n')
    hfile.write ('#include <' + COMMANDSTYPES_HFILE_NAME + '>\n')
    hfile.write ('#include <' + COMMANDSID_HFILE_NAME + '>\n')
    hfile.write ('\n')
    hfile.write ('\n')
    hfile.write('enum arsdk_arg_type {\n')
    hfile.write('    ARSDK_ARG_TYPE_ENUM,\n')
    hfile.write('    ARSDK_ARG_TYPE_U8,\n')
    hfile.write('    ARSDK_ARG_TYPE_I8,\n')
    hfile.write('    ARSDK_ARG_TYPE_U16,\n')
    hfile.write('    ARSDK_ARG_TYPE_I16,\n')
    hfile.write('    ARSDK_ARG_TYPE_U32,\n')
    hfile.write('    ARSDK_ARG_TYPE_I32,\n')
    hfile.write('    ARSDK_ARG_TYPE_U64,\n')
    hfile.write('    ARSDK_ARG_TYPE_I64,\n')
    hfile.write('    ARSDK_ARG_TYPE_FLOAT,\n')
    hfile.write('    ARSDK_ARG_TYPE_DOUBLE,\n')
    hfile.write('    ARSDK_ARG_TYPE_STRING,\n')
    hfile.write('};\n')
    hfile.write ('\n')
    hfile.write ('struct arsdk_enum {\n')
    hfile.write ('    const char               *name;\n')
    hfile.write ('    unsigned int              value;\n')
    hfile.write ('    const char               *comment;\n')
    hfile.write ('};\n')
    hfile.write ('\n')
    hfile.write ('struct arsdk_arg {\n')
    hfile.write ('    const char               *name;\n')
    hfile.write ('    enum arsdk_arg_type       type;\n')
    hfile.write ('    struct arsdk_enum        *enums;\n')
    hfile.write ('    unsigned int              nenums;\n')
    hfile.write ('    const char               *comment;\n')
    hfile.write ('    void                     *priv;\n')
    hfile.write ('};\n')
    hfile.write ('\n')
    hfile.write ('struct arsdk_cmd {\n')
    hfile.write ('    const char               *name;\n')
    hfile.write ('    unsigned int              id;\n')
    hfile.write ('    struct arsdk_arg         *args;\n')
    hfile.write ('    unsigned int              nargs;\n')
    hfile.write ('    const char               *comment;\n')
    hfile.write ('    void                     *priv;\n')
    hfile.write ('};\n')
    hfile.write ('\n')
    hfile.write ('struct arsdk_class {\n')
    hfile.write ('    const char               *name;\n')
    hfile.write ('    unsigned int              ident;\n')
    hfile.write ('    struct arsdk_cmd         *cmds;\n')
    hfile.write ('    unsigned int              ncmds;\n')
    hfile.write ('    const char               *comment;\n')
    hfile.write ('    void                     *priv;\n')
    hfile.write ('};\n')
    hfile.write ('\n')
    hfile.write ('struct arsdk_project {\n')
    hfile.write ('    const char               *name;\n')
    hfile.write ('    eARCOMMANDS_ID_PROJECT    ident;\n')
    hfile.write ('    struct arsdk_class       *classes;\n')
    hfile.write ('    unsigned int              nclasses;\n')
    hfile.write ('    const char               *comment;\n')
    hfile.write ('    void                     *priv;\n')
    hfile.write ('};\n')
    hfile.write ('\n')

    # walk XML tree and dump C structures
    for proj in allProjects:
        for cl in proj.classes:
            for cmd in cl.cmds:
                for arg in cmd.args:
                    hfile.write(dump_enum_table(proj, cl, cmd, arg))
                hfile.write(dump_arg_table(proj, cl, cmd))
            hfile.write(dump_cmd_table(proj, cl))
        hfile.write(dump_class_table(proj))
    hfile.write(dump_project_table(allProjects))

    hfile.write ('#endif /* _ARSDK_ARCOMMANDS_TREE_H */\n')
    hfile.close ()

if genTreeFilename:
    dump_tree_header(genTreeFilename)
