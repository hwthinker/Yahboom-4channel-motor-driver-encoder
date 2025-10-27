#include "bsp_motor_usart.h"


//������ڳ�ʼ��	Motor serial port initialization
void Motor_Usart_init (void)
{
	GPIO_InitTypeDef GPIO_InitStructure;
	USART_InitTypeDef USART_InitStructure;
	NVIC_InitTypeDef NVIC_InitStructure;
	// �򿪴���GPIO��ʱ��	Turn on the serial GPIO clock
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_GPIOA, ENABLE);

	// �򿪴��������ʱ��	Enable the clock of the serial port peripheral
	RCC_APB1PeriphClockCmd(RCC_APB1Periph_USART2, ENABLE);

	// ��USART Tx��GPIO����Ϊ���츴��ģʽ		Configure the GPIO of USART Tx to push-pull multiplexing mode
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_2;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF_PP;
	GPIO_InitStructure.GPIO_Speed = GPIO_Speed_50MHz;
	GPIO_Init(GPIOA, &GPIO_InitStructure);

	// ��USART Rx��GPIO����Ϊ��������ģʽ		Configure the GPIO of USART Rx to floating input mode
	GPIO_InitStructure.GPIO_Pin = GPIO_Pin_3;
	GPIO_InitStructure.GPIO_Mode = GPIO_Mode_IN_FLOATING;
	GPIO_Init(GPIOA, &GPIO_InitStructure);

	//Usart2 NVIC ����	Usart2 NVIC Configuration
	NVIC_InitStructure.NVIC_IRQChannel = USART2_IRQn;
	NVIC_InitStructure.NVIC_IRQChannelPreemptionPriority = 1; //��ռ���ȼ�	Preemption priority
	NVIC_InitStructure.NVIC_IRQChannelSubPriority = 2;		  //�����ȼ�		Subpriority
	NVIC_InitStructure.NVIC_IRQChannelCmd = ENABLE;			  //IRQͨ��ʹ��	IRQ channel enable
	NVIC_Init(&NVIC_InitStructure);							  //����ָ���Ĳ�����ʼ��NVIC�Ĵ���	Initializes the NVIC registers according to the specified parameters

	
	// ���ò�����	Configuring the baud rate
	USART_InitStructure.USART_BaudRate = 115200;
	// ���� �������ֳ�	Configuration Pin Data Word Length
	USART_InitStructure.USART_WordLength = USART_WordLength_8b;
	// ����ֹͣλ	Configuring stop bits
	USART_InitStructure.USART_StopBits = USART_StopBits_1;
	// ����У��λ	Configuring the check digit
	USART_InitStructure.USART_Parity = USART_Parity_No;
	// ����Ӳ��������	Configuring Hardware Flow Control
	USART_InitStructure.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
	// ���ù���ģʽ���շ�һ��		Configure the working mode, send and receive together
	USART_InitStructure.USART_Mode = USART_Mode_Rx | USART_Mode_Tx;

	// ��ɴ��ڵĳ�ʼ������	Complete the initial configuration of the serial port
	USART_Init(USART2, &USART_InitStructure);

	//�������ڽ����ж�	Enable serial port receive interrupt
	USART_ITConfig(USART2, USART_IT_RXNE, ENABLE);
	// ʹ�ܴ���	Enable the serial port
	USART_Cmd(USART2, ENABLE);

}



/************************************************
�������� �� Send_Motor_U8		Function name: Send_Motor_U8
��    �� �� UART2����һ���ַ�	Function: UART2 sends a character
��    �� �� Data --- ����		Parameter: Data --- data
�� �� ֵ �� ��					Return value: None
*************************************************/
void Send_Motor_U8(uint8_t Data)
{
	while (USART_GetFlagStatus(USART2, USART_FLAG_TXE) == RESET)
		;
	USART_SendData(USART2, Data);
}

/************************************************
�������� �� Send_Motor_ArrayU8	Function name: Send_Motor_ArrayU8
��    �� �� ����1����N���ַ�		Function: Serial port 1 sends N characters
��    �� �� pData ---- �ַ���	Parameter: pData ---- string
            Length --- ����		Length --- length
�� �� ֵ �� ��					Return value: None
*************************************************/
void Send_Motor_ArrayU8(uint8_t *pData, uint16_t Length)
{
	while (Length--)
	{
		Send_Motor_U8(*pData);
		pData++;
	}
}


/*  �����жϽ��մ��� */
/* Serial port interrupt reception processing */
void USART2_IRQHandler(void)
{
	uint8_t Rx2_Temp = 0;
	/* �����ݻ�����ж�λ */
	/*Reading data will clear the interrupt bit*/
	while (USART_GetFlagStatus(USART2, USART_FLAG_RXNE) == RESET);
	
	Rx2_Temp = USART_ReceiveData(USART2);
	
	//����	deal with
	Deal_Control_Rxtemp(Rx2_Temp);

}






