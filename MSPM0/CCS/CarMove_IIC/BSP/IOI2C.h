#ifndef __IOI2C_H
#define __IOI2C_H

#include "ti_msp_dl_config.h"
#include "stdint.h"
#include "delay.h"

#define u8 uint8_t

//IO��������	IO direction setting
#define SDA_IN()  { DL_GPIO_initDigitalInput(I2C_SDA_IOMUX); }
#define SDA_OUT() {                                                \
                        DL_GPIO_initDigitalOutput(I2C_SDA_IOMUX);    \
                        DL_GPIO_setPins(I2C_PORT, I2C_SDA_PIN);      \
                        DL_GPIO_enableOutput(I2C_PORT, I2C_SDA_PIN); \
                  }

//IO��������	 IO operation function
#define SCL(x)    ( (x) ? DL_GPIO_setPins(I2C_PORT,I2C_SCL_PIN) : DL_GPIO_clearPins(I2C_PORT,I2C_SCL_PIN) ) //SCL
#define SDA(x)    ( (x) ? DL_GPIO_setPins(I2C_PORT,I2C_SDA_PIN) : DL_GPIO_clearPins(I2C_PORT,I2C_SDA_PIN) ) //SDA	 
#define SDA_GET() ( ( ( DL_GPIO_readPins(I2C_PORT,I2C_SDA_PIN) & I2C_SDA_PIN ) > 0 ) ? 1 : 0 )  //����SDA	Input SDA


//IIC���в�������	IIC all operation functions
int IIC_Start(void);			//����IIC��ʼ�ź�	Send IIC start signal
void IIC_Stop(void);	  		//����IICֹͣ�ź�	Send IIC stop signal
void IIC_Send_Byte(u8 txd);		//IIC����һ���ֽ�	IIC sends a byte
u8 IIC_Read_Byte(void);			//IIC��ȡһ���ֽ�	IIC reads a byte
int IIC_Wait_Ack(void); 		//IIC�ȴ�ACK�ź�		IIC waits for ACK signal
void IIC_Ack(void);				//IIC����ACK�ź�		IIC sends ACK signal
void IIC_NAck(void);			//IIC������ACK�ź�	IIC does not send ACK signal


int i2cWrite(uint8_t addr, uint8_t reg, uint8_t len, uint8_t *data);
int i2cRead(uint8_t addr, uint8_t reg, uint8_t len, uint8_t *buf);

#endif
