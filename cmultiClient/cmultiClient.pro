TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

INCLUDEPATH += /home/chrak/repositories/cmulti/lcm-cmulti/exlcm

SOURCES += \
    cmultiClient/CMULTI.cpp \
    cmultiClient/CNETLCMHDL.cpp \
    cmultiClient/argparse.c \
    cmultiClient/cmultiClient.cpp

DISTFILES += \
    cmultiClient/libcrc.a \
    cmultiClient/lcm-cmulti/cmulti.lcm \
    ../lcm-cmulti/cmulti.lcm

HEADERS += \
    cmultiClient/argparse.h \
    cmultiClient/checksum.h \
    cmultiClient/CMULTI.h \
    cmultiClient/CNETLCMHDL.h \
    ../lcm-cmulti/exlcm/cmulti_answer_t.hpp \
    ../lcm-cmulti/exlcm/cmulti_command_t.hpp \
    ../lcm-cmulti/exlcm/cmulti_constants_t.hpp \
    ../lcm-cmulti/exlcm/cmulti_crc_constants_t.hpp \
    ../lcm-cmulti/exlcm/lcm_cmulti.hpp

unix|win32: LIBS += -lcrc

unix|win32: LIBS += -llcm

unix|win32: LIBS += -lserial

unix|win32: LIBS += -lstdc++
