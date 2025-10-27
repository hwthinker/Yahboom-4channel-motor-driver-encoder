#include "uart_module.h"

#define BUF_SIZE (1024)         // ���ͻ�������С | Tx buffer size
#define RD_BUF_SIZE (BUF_SIZE)  // ���ջ�������С | Rx buffer size

QueueHandle_t uart_queue;// UART�¼����о�� | UART event queue handle

// ͨ�����ڷ���һ������ 
int Send_Motor_ArrayU8(uint8_t* data, uint16_t len)
{
    const int txBytes = uart_write_bytes(UART_NUM_1, data, len);
    return txBytes;
}

// ͨ�����ڷ���һ���ֽ� 
int Send_Motor_U8(uint8_t data)
{
    uint8_t data1 = data;// ������ʱ���������ڴ�������� | Avoid memory alignment issues
    const int txBytes = uart_write_bytes(UART_NUM_1, &data1, 1);
    return txBytes;
}

void uart1_init() {
    // UART�������� | UART parameter configuration
    uart_config_t uart_config = {
        .baud_rate = UART_BAUD,                 // �����ʣ�115200 | Common baud rate: 115200
        .data_bits = UART_DATA_8_BITS,          // 8λ����λ | 8 data bits
        .parity    = UART_PARITY_DISABLE,       // ��У��λ | No parity
        .stop_bits = UART_STOP_BITS_1,          // 1λֹͣλ | 1 stop bit
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,  // ����Ӳ������ | Disable hardware flow control
        .source_clk = UART_SCLK_APB,            // ʹ��APBʱ��Դ | Use APB clock source
    };

    uart_param_config(UART_NUM_1, &uart_config);// Ӧ�����ò��� | Apply configuration
    uart_set_pin(UART_NUM_1, UART1_TX_PIN, UART1_RX_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);// ����GPIO���� | Set GPIO pins
    uart_driver_install(UART_NUM_1, 2048, 2048, 50, &uart_queue, 0);// ��װUART���� | Install UART driver
}

//UART���ݴ������� | Task: UART Data Processing
void UART_Process_Task(void *pvParameters) {
    uart_event_t event;// UART�¼��ṹ�� | UART event structure
    uint8_t* dtmp = (uint8_t*) malloc(RD_BUF_SIZE);// ������ʱ������ | Allocate temp buffer
    while(1)
    {// �ȴ������¼�������ʽ��| Wait for queue event (blocking)
        if (xQueueReceive(uart_queue, (void *)&event, (TickType_t)portMAX_DELAY)) {
            switch (event.type) 
            {
                case UART_DATA:// ���ݵ����¼� | Data received event
                    int len = uart_read_bytes(UART_NUM_1, dtmp, event.size, portMAX_DELAY);// ��ȡUART���� | Read UART data
                    for (int i = 0; i < len; i++) {// ���ֽڴ������� | Process data byte by byte
                        Deal_Control_Rxtemp(dtmp[i]);
                    }
                    break;
                case UART_BUFFER_FULL:// ������������ | Buffer full handling
                    uart_flush_input(UART_NUM_1);// ������뻺���� | Clear input buffer
                    xQueueReset(uart_queue);    // �����¼����� | Reset event queue
                    break;
                case UART_FIFO_OVF:// FIFO������� | FIFO overflow handling
                    uart_flush_input(UART_NUM_1);// ���Ӳ��FIFO | Clear hardware FIFO
                    xQueueReset(uart_queue);    // �����¼����� | Reset event queue
                    break;
                default:
                    break;
            }
        }
    }
    free(dtmp);// �ͷ��ڴ� | Free memory
    dtmp = NULL;// ����Ұָ�� | Prevent dangling pointer
    vTaskDelete(NULL);// ɾ����ǰ���� | Delete current task
}
