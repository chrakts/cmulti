TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
    cmultiServer.cpp \
    argparse.c \
    CNETLCMHDL.cpp \
    CMULTI.cpp

HEADERS += \
    argparse.h \
    argparse.h \
    checksum.h \
    CNETLCMHDL.h \
    lcm-cnet/exlcm/cnet_answer_t.hpp \
    lcm-cnet/exlcm/cnet_command_t.hpp \
    lcm-cnet/exlcm/cnet_constants_t.hpp \
    lcm-cnet/exlcm/cnet_crc_constants_t.hpp \
    lcm-cnet/exlcm/lcm_cnet.hpp \
    CMULTI.h \
    lcm-cmulti/exlcm/cmulti_answer_t.hpp \
    lcm-cmulti/exlcm/cmulti_command_t.hpp \
    lcm-cmulti/exlcm/cmulti_constants_t.hpp \
    lcm-cmulti/exlcm/cmulti_crc_constants_t.hpp \
    lcm-cmulti/exlcm/lcm_cmulti.hpp

DISTFILES += \
    libcrc.a \
    lcm-cmulti/cmulti.lcm

unix|win32: LIBS += -lcrc

unix|win32: LIBS += -llcm

unix|win32: LIBS += -lserial

unix|win32: LIBS += -lstdc++
