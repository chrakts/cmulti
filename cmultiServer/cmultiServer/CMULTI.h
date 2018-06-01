/*
 * CNET.h
 *
 *  Created on: 12.08.2016
 *      Author: pi
 */

#ifndef CMULTI_H_
#define CMULTI_H_

#include <iostream>   // std::cout
#include <SerialStream.h>
#include <SerialPort.h>
#include <string>
#include <cstdint>
#include <cstring>
#include <iostream>
#include <iomanip>
#include <sstream>

#include <lcm/lcm-cpp.hpp>			// include der library
#include "lcm-cmulti/exlcm/lcm_cmulti.hpp"			// Sammelinclude fuer alle lcm-includes
#include "checksum.h"

using namespace std;
using namespace LibSerial;

class CMULTI: public SerialPort
{
	public:
		using SerialPort::SerialPort;

		~CMULTI()
		{
			this->Close();
		}
		uint8_t Get_Command(char *command, uint8_t length, uint16_t timeout);
		uint8_t Get_Answer(char *answer, uint8_t length, uint16_t timeout);
		uint8_t Get_Command(string & command, uint16_t timeout);
		uint8_t Get_Answer(string & answer,int16_t crc, uint16_t timeout);
		uint8_t Send_Command(exlcm::cmulti_command_t *command);
		uint8_t Flush();

};

#endif /* CNET_H_ */
