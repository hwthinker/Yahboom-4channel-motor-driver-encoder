#include "AllHeader.h"

#define UPLOAD_DATA 2  //1:�����ܵı��������� 2:����ʵʱ�ı�����
					   //1: Receive total encoder data 2: Receive real-time encoder
                       
#define MOTOR_TYPE 2   //1:520��� 2:310��� 3:��������TT��� 4:TTֱ�����ٵ�� 5:L��520���
                       //1:520 motor 2:310 motor 3:speed code disc TT motor 4:TT DC reduction motor 5:L type 520 motor

uint8_t times = 0;

void Car_Move(void)
{
	static uint8_t state = 0;
	switch(state)
	{
		case 0:
		control_speed(300,300,300,300);//ǰ�� Forward
		break;
		
		case 1:
		control_speed(-300,-300,-300,-300);//���� Back
		break;
		
		case 2:
		control_speed(300,300,-600,-600);//����	Rotate right
		break;
		
		case 3:
		control_speed(-600,-600,300,300);//����	Rotate left
		break;
		
		case 4:
		control_speed(0,0,0,0);//ͣ��	Stop
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
		control_pwm(1500,1500,1500,1500);//ǰ�� Forward
		break;
		
		case 1:
		control_pwm(-1500,-1500,-1500,-1500);//���� Back
		break;
		
		case 2:
		control_pwm(1200,1200,-1500,-1500);//����	Rotate right
		break;
		
		case 3:
		control_pwm(-1500,-1500,1200,1200);//����	Rotate left
		break;
		
		case 4:
		control_pwm(0,0,0,0);//ͣ��	Stop
		break;
	}
	state++;
	if(state>4)state=0;
}


int main(void)
{	
	bsp_init();
	
	TIM3_Init();
	
	//���ģ��iicͨ�ų�ʼ��	Motor module iic communication initialization
	IIC_Motor_Init();
	printf("pelase wait...\r\n");
    control_pwm(0,0,0,0);
    delay_ms(100);

	
    #if MOTOR_TYPE == 1
	Set_motor_type(1);//���õ������	Configure motor type
	delay_ms(100);
	Set_Pluse_Phase(30);//���ü��ٱ� �����ֲ�ó�	Configure the reduction ratio. Check the motor manual to find out
	delay_ms(100);
	Set_Pluse_line(11);//���ôŻ��� �����ֲ�ó�	Configure the magnetic ring wire. Check the motor manual to get the result.
	delay_ms(100);
	Set_Wheel_dis(67.00);//��������ֱ��,�����ó�		Configure the wheel diameter and measure it
	delay_ms(100);
	Set_motor_deadzone(1900);//���õ������,ʵ��ó�	Configure the motor dead zone, and the experiment shows
	delay_ms(100);
    
    #elif MOTOR_TYPE == 2
    Set_motor_type(2);
	delay_ms(100);
	Set_Pluse_Phase(20);
	delay_ms(100);
	Set_Pluse_line(13);
	delay_ms(100);
	Set_Wheel_dis(48.00);
	delay_ms(100);
	Set_motor_deadzone(1600);
	delay_ms(100);
    
    #elif MOTOR_TYPE == 3
    Set_motor_type(3);
	delay_ms(100);
	Set_Pluse_Phase(45);
	delay_ms(100);
	Set_Pluse_line(13);
	delay_ms(100);
	Set_Wheel_dis(68.00);
	delay_ms(100);
	Set_motor_deadzone(1250);
	delay_ms(100);
    
    #elif MOTOR_TYPE == 4
    Set_motor_type(4);
	delay_ms(100);
	Set_Pluse_Phase(48);
	delay_ms(100);
	Set_motor_deadzone(1000);
	delay_ms(100);
    
    #elif MOTOR_TYPE == 5
    Set_motor_type(1);
	delay_ms(100);
	Set_Pluse_Phase(40);
	delay_ms(100);
	Set_Pluse_line(11);
	delay_ms(100);
	Set_Wheel_dis(67.00);
	delay_ms(100);
	Set_motor_deadzone(1900);
	delay_ms(100);
    #endif

	while(1)
	{
		if(times>=250)//��ʱ��ÿ10ms�ۼ�һ�Σ����ﵽ250�Σ���2.5���ʱ��ת��һ��С����״̬	The timer accumulates every 100ms, and when it reaches 25 times, that is, every 2.5 seconds, the state of the car is changed.
		{
            #if MOTOR_TYPE == 4
            Car_Move_PWM();
            #else
			Car_Move();
            #endif
			times = 0;
		}

		#if UPLOAD_DATA == 1
		Read_ALL_Enconder();
		printf("M1:%d\t M2:%d\t M3:%d\t M4:%d\t \r\n",Encoder_Now[0],Encoder_Now[1],Encoder_Now[2],Encoder_Now[3]);
		#elif UPLOAD_DATA == 2
		Read_10_Enconder();
		printf("M1:%d\t M2:%d\t M3:%d\t M4:%d\t \r\n",Encoder_Offset[0],Encoder_Offset[1],Encoder_Offset[2],Encoder_Offset[3]);
		#endif
	}
	
}

