#include "AllHeader.h"

#define UPLOAD_DATA 2  //0:���������� 1:�����ܵı��������� 2:����ʵʱ�ı����� 3:���յ����ǰ�ٶ� mm/s
					   //0: Do not receive data 1: Receive total encoder data 2: Receive real-time encoder 3: Receive current motor speed mm/s

#define MOTOR_TYPE 2   //1:520��� 2:310��� 3:��������TT��� 4:TTֱ�����ٵ�� 5:L��520���
                       //1:520 motor 2:310 motor 3:speed code disc TT motor 4:TT DC reduction motor 5:L type 520 motor

uint8_t times = 0;

void Car_Move(void)
{
	static uint8_t state = 0;
	switch(state)
	{
		case 0:
			Contrl_Speed(400,400,400,400);
		break;
		case 1:
			Contrl_Speed(-400,-400,-400,-400);
		break;
		case 2:
			Contrl_Speed(400,400,-600,-600);
		break;
		case 3:
			Contrl_Speed(-600,-600,400,400);
		break;
		case 4:
			Contrl_Speed(0,0,0,0);
		break;
	}
	state++;
	if(state>4)state=0;
}

void Car_Move_PWM(void)
{
	static uint8_t state = 0;
	switch(state)
	{
		case 0:
		Contrl_Pwm(1500,1500,1500,1500);//ǰ�� Forward
		break;
		
		case 1:
		Contrl_Pwm(-1500,-1500,-1500,-1500);//���� Back
		break;
		
		case 2:
		Contrl_Pwm(1200,1200,-1500,-1500);//����	Rotate right
		break;
		
		case 3:
		Contrl_Pwm(-1500,-1500,1200,1200);//����	Rotate left
		break;
		
		case 4:
		Contrl_Pwm(0,0,0,0);//ͣ��	Stop
		break;
	}
	state++;
	if(state>4)state=0;
}

int main(void)
{	
	bsp_init();
	TIM3_Init();
	
	printf("pelase wait...\r\n");
	Contrl_Pwm(0,0,0,0);
    delay_ms(100);

	//�͵��ģ�鴮��ͨ��	Serial communication with motor module
	Motor_Usart_init();
	//�ȹر��ϱ�	Close the report first
	send_upload_data(false,false,false);delay_ms(10);
	
    #if MOTOR_TYPE == 1
	send_motor_type(1);//���õ������	Configure motor type
	delay_ms(100);
	send_pulse_phase(30);//���ü��ٱ� �����ֲ�ó�	Configure the reduction ratio. Check the motor manual to find out
	delay_ms(100);
	send_pulse_line(11);//���ôŻ��� �����ֲ�ó�	Configure the magnetic ring wire. Check the motor manual to get the result.
	delay_ms(100);
	send_wheel_diameter(67.00);//��������ֱ��,�����ó�		Configure the wheel diameter and measure it
	delay_ms(100);
	send_motor_deadzone(1900);//���õ������,ʵ��ó�	Configure the motor dead zone, and the experiment shows
	delay_ms(100);
    
    #elif MOTOR_TYPE == 2
    send_motor_type(2);
	delay_ms(100);
	send_pulse_phase(20);
	delay_ms(100);
	send_pulse_line(13);
	delay_ms(100);
	send_wheel_diameter(48.00);
	delay_ms(100);
	send_motor_deadzone(1600);
	delay_ms(100);
    
    #elif MOTOR_TYPE == 3
    send_motor_type(3);
	delay_ms(100);
	send_pulse_phase(45);
	delay_ms(100);
	send_pulse_line(13);
	delay_ms(100);
	send_wheel_diameter(68.00);
	delay_ms(100);
	send_motor_deadzone(1250);
	delay_ms(100);
    
    #elif MOTOR_TYPE == 4
    send_motor_type(4);
	delay_ms(100);
	send_pulse_phase(48);
	delay_ms(100);
	send_motor_deadzone(1000);
	delay_ms(100);
    
    #elif MOTOR_TYPE == 5
    send_motor_type(1);
	delay_ms(100);
	send_pulse_phase(40);
	delay_ms(100);
	send_pulse_line(11);
	delay_ms(100);
	send_wheel_diameter(67.00);
	delay_ms(100);
	send_motor_deadzone(1900);
	delay_ms(100);
    #endif
	
	//�����ģ�鷢����Ҫ�ϱ�������	Send the data that needs to be reported to the motor module
	#if UPLOAD_DATA == 1
	send_upload_data(true,false,false);delay_ms(10);
	#elif UPLOAD_DATA == 2
	send_upload_data(false,true,false);delay_ms(10);
	#elif UPLOAD_DATA == 3
	send_upload_data(false,false,true);delay_ms(10);
	#endif
	while(1)
	{
		if(times>=250)
		{
			#if MOTOR_TYPE == 4
            Car_Move_PWM();
            #else
			Car_Move();
            #endif
			times = 0;
		}
		if(g_recv_flag == 1)
		{
			g_recv_flag = 0;
			
			#if UPLOAD_DATA == 1
				Deal_data_real();
				printf("M1:%d,M2:%d,M3:%d,M4:%d\r\n",Encoder_Now[0],Encoder_Now[1],Encoder_Now[2],Encoder_Now[3]);
			#elif UPLOAD_DATA == 2
				Deal_data_real();
				printf("M1:%d,M2:%d,M3:%d,M4:%d\r\n",Encoder_Offset[0],Encoder_Offset[1],Encoder_Offset[2],Encoder_Offset[3]);
			#elif UPLOAD_DATA == 3
				Deal_data_real();
				printf("M1:%.2f,M2:%.2f,M3:%.2f,M4:%.2f\r\n",g_Speed[0],g_Speed[1],g_Speed[2],g_Speed[3]);
			#endif
		}
	}
}

