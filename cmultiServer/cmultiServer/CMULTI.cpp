/*
 * CMULTI.cpp
 *
 *  Created on: 12.08.2016
 *      Author: pi
 */

#include "CMULTI.h"
#include "checksum.h"

/*
CMULTI::CMULTI() {
	// TODO Auto-generated constructor stub

}

CMULTI::~CMULTI() {
	// TODO Auto-generated destructor stub
}

*/

extern exlcm::cmulti_crc_constants_t cmulti_crc_constants_t;
extern exlcm::cmulti_constants_t cmulti_constants;


uint8_t CMULTI::Get_Command(char *command, uint8_t length, uint16_t timeout)
{
#define SLEEP_TIME		20000.0
int maxcycles,cycles=0,num_data=0;

	maxcycles = (uint16_t)(((double)timeout) / (SLEEP_TIME/1000000) );
	while(this->IsDataAvailable()==false)
	{
		usleep(SLEEP_TIME);
		cycles++;
		if(cycles > maxcycles)
			return( false );
	}
	while( 1 )
	{
		if( (num_data >= length) | (cycles > maxcycles) )
		{
//			cout << "Length: " << std::to_string(num_data) << " cycles: " << std::to_string(cycles) << endl;
			cout << "Length: "  << " cycles: "  << endl;
			command[length-1]= 0;
			cout << command << endl;
			return( false );
		}
		if( this->IsDataAvailable() )
		{
			command[num_data] = this->ReadByte(10);
//			cout << "<" << to_string(command[num_data]) << ">" << endl;
			if(command[num_data]!=0)
				num_data++;
		}
		else
		{
			sleep(SLEEP_TIME);
			cycles++;
		}
		if(num_data > 1)
		{
			if(  (command[num_data-2] == '<') & (command[num_data-1] == '\\')  )
			{
				command[num_data] = 0;
				return( true );
			}
		}

	}
	return( true );
}

uint8_t CMULTI::Get_Answer(char *answer, uint8_t length, uint16_t timeout)
{
#define SLEEP_TIME		20000.0
uint16_t maxcycles,cycles=0,num_data=0;

	maxcycles = (uint16_t)(((double)timeout) / (SLEEP_TIME/1000000) );
	while(this->IsDataAvailable()==false)
	{
		usleep(SLEEP_TIME);
		cycles++;
		if(cycles > maxcycles)
			return( false );
	}
	while( 1 )
	{
		if( (num_data >= length) | (cycles > maxcycles) )
		{
//			cout << "Length: " << to_string(num_data) << " cycles: " << to_string(cycles) << endl;
			answer[length-1]= 0;
			cout << answer << endl;
			return( false );
		}
		if( this->IsDataAvailable() )
		{
			cout << "Wait for answer" << endl;
			answer[num_data] = this->ReadByte(10000);		// war 10
//			cout << "<" << to_string(command[num_data]) << ">" << endl;
			if(answer[num_data]!=0)
				num_data++;
		}
		else
		{
			sleep(SLEEP_TIME);
			cycles++;
		}
		if(num_data > 1)
		{
			if(   ( (answer[num_data-2] == '.') | (answer[num_data-2] == '!') ) & (answer[num_data-1] == '>' )   )
			{
				answer[num_data] = 0;
				return( true );
			}
		}

	}
	return( true );
}

uint8_t CMULTI::Get_Command(string & command, uint16_t timeout)
{
#define SLEEP_TIME		20000.0
uint16_t maxcycles,cycles=0;
unsigned int start,ende;
char one_char;

	command.clear();
	maxcycles = (uint16_t)(((double)timeout) / (SLEEP_TIME/1000000) );
	while(this->IsDataAvailable()==false)
	{
		usleep(SLEEP_TIME);
		cycles++;
		if(cycles > maxcycles)
			return( false );
	}
	while( 1 )
	{
		if( (cycles > maxcycles) | (command.length()>1024) )
			return( false );
		if( this->IsDataAvailable() )
		{
			one_char = this->ReadByte(10);
			if( one_char != 0)
				command += one_char;
		}
		else
		{
			usleep(SLEEP_TIME);
			cycles++;
		}
		if(command.length() > 1)
		{
			ende = command.rfind("<\\",command.npos);
			start = command.rfind("\\>",command.npos);
			if(  ende < command.npos  )
			{
				if( start < command.npos )
				{
					command = command.substr(start+2,command.length()-4-start);
					return( true );
				}
				else
				{
					return( false );
				}
			}
		}

	}
	return( true );
}

uint8_t CMULTI::Get_Answer(string & answer,int16_t crc, uint16_t timeout)
{
#define SLEEP_TIME		20000.0
uint16_t maxcycles,cycles=0;
char one_char;
size_t start;
	answer.clear();
	maxcycles = (uint16_t)(((double)timeout) / (SLEEP_TIME/1000) );
	while(this->IsDataAvailable()==false)
	{
		usleep(SLEEP_TIME);
		cycles++;
		if(cycles > maxcycles)
		{
      cout << "!!!!Timeout: "<<cycles << " von " << maxcycles << " erreicht" << endl;
			return( cmulti_constants.timeout );
		}
	}
	while( 1 )
	{
		if( (cycles > maxcycles) | (answer.length()>1024) )
		{
    	cout << "---->!!!!Timeout: " <<cycles << " von " << maxcycles << " erreicht" << endl;
			return( cmulti_constants.timeout );
		}
		if( this->IsDataAvailable() )
		{
			try
			{
//			  cout << "Read Character " << answer.length() << endl;
				one_char = this->ReadByte(timeout);
			}
			catch(...)
			{
				return( cmulti_constants.timeout  );
			}
			if( one_char != 0)
				answer += one_char;
		}
		else
		{
//			cout << "Sleep for " << SLEEP_TIME << " us" << endl;
			usleep(SLEEP_TIME);
			cycles++;
		}
		if(answer.length() > 1)
		{

			if(crc==cmulti_crc_constants_t.noCRC)
			{
				if(  (answer.rfind(".>",answer.npos) < answer.npos) | (answer.rfind("!>",answer.npos) < answer.npos)  )
				{
					start = answer.rfind("<",answer.npos);
					if( start < answer.npos )
					{
						answer = answer.substr(start+1,answer.length()-2-start);
						switch(*answer.rbegin())
						{
							case '.':
								return( cmulti_constants.answerTrue ) ;
							break;
							case '!':
								return( cmulti_constants.answerFalse ) ;
							break;
							default:
								return( cmulti_constants.answerWrong ) ;
							break;
						}
					}
					else
					{
						return( cmulti_constants.answerWrong );
					}
				}
			}
			else // with crc
			{
				size_t ende;
				string   answerCrc;
				ende = answer.rfind(">",answer.npos);
//				cout << "test 0" << endl;
				if( ende < answer.npos )
				{
					start = answer.rfind("<",answer.npos);
//					cout << "test 1 " << start << " " << ende << " " << answer.npos << endl;
					if( (start < answer.npos) && ( (answer[ende-5]=='.') || (answer[ende-5]=='!') ) )
					{
						answerCrc =  answer.substr(ende-4,4);
//						cout << "test 2" << endl;
						answer = answer.substr(start+1,answer.length()-6-start);
//						cout << "test 3" << endl;
						cout << "CRC: " << answerCrc << " Antwort: " << answer << endl;
						unsigned int crcInt,crc16;
						std::stringstream crcSS;
						crcSS << std::hex << answerCrc;
						crcSS >> crcInt;
						cout << "CRC: " << answerCrc << " = " << crcInt << " Antwort: " << answer << endl;
						crc16 = crc_xmodem( (const unsigned char*)  answer.c_str(),answer.length() );

						if(crc16==crcInt)
						{
							switch(*answer.rbegin())
							{
								case '.':
									return( cmulti_constants.answerTrue ) ;
								break;
								case '!':
									return( cmulti_constants.answerFalse ) ;
								break;
								default:
									return( cmulti_constants.answerWrong ) ;
								break;
							}
						}
						else
						{
							cout << "CRC-Fehler" << endl;
							return(cmulti_constants.crcError);
						}
					}
					else
					{
						cout << "answer wrong" << endl;
						return( cmulti_constants.answerWrong );
					}
				}
			}
		}

	}
}


uint8_t CMULTI::Send_Command(exlcm::cmulti_command_t *command)
{
	if(this->IsOpen())
	{
		cout << "Target:" << command->target << endl;
		cout << "Source:" << command->source << endl;
		cout << "Command:" << command->command << endl;
		if(command->crcType == cmulti_crc_constants_t.noCRC)
		{
			stringstream ss,s1,ll;
			string parameter;
			uint16_t length,plength;
			plength = command->parameter.length();
			if(plength>0)
			{
				plength++;
				parameter = command->parameter + "<";
			}

			length = command->command.length()+plength+7;
			ll << std::setfill('0') << std::setw(2) << std::hex << length;
			ss << "#" << ll.str() << "@" << command->target << command->source << command->command << parameter << "\r\n";
			this->Write( ss.str() );
			cout << ss.str() << endl;
			usleep(100000);
			this->Flush();
		}
		else
		{
			uint16_t crc16;
			stringstream ss,s1,ll;
			string parameter;
			uint16_t length,plength;
			plength = command->parameter.length();
			if(plength>0)
			{
				plength++;
				parameter = command->parameter + "<";
			}
			length = command->command.length()+plength+11;
			ll << std::setfill('0') << std::setw(2) << std::hex << length;
			s1 << "#" << ll.str() << "D" << command->target << command->source << command->command << parameter;
			crc16 = crc_xmodem((const unsigned char *)s1.str().c_str(), s1.tellp());
			ss << s1.str() << std::setfill('0') << std::setw(4) << std::hex << crc16 << "\r\n";
			this->Write( ss.str() );
			cout << ss.str() << endl;
			usleep(100000);
			this->Flush();
		}
		return(true);
	}
	else
		return(false);
}

uint8_t CMULTI::Flush()
{
char one_char;
	if(this->IsOpen())
	{
    while(this->IsDataAvailable()==true)
    {
      one_char = this->ReadByte(100);
    }
		return(true);
	}
	else
		return(false);
}
