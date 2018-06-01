/*
 * CNETLCMHDL.h
 *
 *  Created on: 13.08.2016
 *      Author: pi
 */

#ifndef CNETLCMHDL_H_
#define CNETLCMHDL_H_

#include <stdio.h>

#include <lcm/lcm-cpp.hpp>			// include der library
#include "lcm-cmulti/exlcm/lcm_cmulti.hpp"
#include "CMULTI.h"
#include <cstdint>
#include <iostream>

using namespace std;

extern CMULTI cnet;
extern lcm::LCM cnet_lcm;

extern exlcm::cmulti_command_t cmulti_command;

class CNET_LCM_HDL
{
public:
//	CNET_LCM_HDL();
	virtual ~CNET_LCM_HDL();

	void handle_cnet_command(const lcm::ReceiveBuffer *rbuf, const std::string &chan, const exlcm::cmulti_command_t* msg)
	{
		cout << "Folgendes Kommando erhalten: " << msg->command << endl;
		cmulti_command = *msg;
	}
};

#endif /* CNETLCMHDL_H_ */
