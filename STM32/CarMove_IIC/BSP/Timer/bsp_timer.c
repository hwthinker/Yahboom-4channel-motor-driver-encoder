#include "bsp_timer.h"


static u16 stop_time = 0;//�ӳ�ʱ��  delay time



//��ʱ��6���ӳ� 10ms���ӳ� �˷�����delay׼ȷ
//Timer 6 has a delay of 10ms. This method is more accurate than delay
void delay_time(u16 time)
{
	stop_time = time;
	while(stop_time);//���� Wait
}

//�ӳ�1s  Unit second
void my_delay(u16 s)//s
{
	for(int i = 0;i<s;i++)
	{
		delay_time(100);
	}
}


/**************************************************************************
Function function: TIM3 initialization, timed for 10 milliseconds
Entrance parameters: None
Return value: None
�������ܣ�TIM3��ʼ������ʱ10����
��ڲ�������
����  ֵ����
**************************************************************************/
void TIM3_Init(void)
{
	TIM_TimeBaseInitTypeDef TIM_TimeBaseStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM3, ENABLE); //ʹ�ܶ�ʱ����ʱ��  Enable the clock of the timer
	TIM_TimeBaseStructure.TIM_Prescaler = 7199;			 // Ԥ��Ƶ��  Prescaler
	TIM_TimeBaseStructure.TIM_Period = 99;				 //�趨�������Զ���װֵ  Set the automatic reset value of the counter
	TIM_TimeBaseInit(TIM3, &TIM_TimeBaseStructure);
	TIM_ClearFlag(TIM3, TIM_FLAG_Update);                //���TIM�ĸ��±�־λ Clear the update flag of TIM
	TIM_ITConfig(TIM3, TIM_IT_Update, ENABLE);

	//�ж����ȼ�NVIC����
	NVIC_InitStructure.NVIC_IRQChannel = TIM3_IRQn;			  //TIM6�ж�	TIM6 interrupt
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 4; //��ռ���ȼ�4��	Preempts priority level 4
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 2;		  //�����ȼ�2��	From priority level 2
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			  //IRQͨ����ʹ��	IRQ channel is enabled
	NVIC_Init(&NVIC_InitStructure);							  //��ʼ��NVIC�Ĵ���	Initializes NVIC registers

	TIM_Cmd(TIM3, ENABLE);
}


// TIM3�ж� //TIM3 Interrupt service
void TIM3_IRQHandler(void)
{
	if (TIM_GetITStatus(TIM3, TIM_IT_Update) != RESET) //���TIM�����жϷ������	Check whether TIM update interrupt occurs
	{
		TIM_ClearITPendingBit(TIM3, TIM_IT_Update);    //���TIMx�����жϱ�־	Clear TIMx update interrupt flag

		times++;
		
		if(stop_time>0)
		{
			stop_time --;
		}
	}
}

