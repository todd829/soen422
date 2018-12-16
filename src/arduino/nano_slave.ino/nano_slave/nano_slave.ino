#define BAUD 9600
#include <avr/io.h>
#include <util/setbaud.h>
#include <util/delay.h>

void spiSlaveEnable (void){
  DDRB |= (1 << PB0);
  DDRB |= (1 << 4); // Set MISO as output. MOSI, SCK and SS are set to inputs
  SPCR |= (1 << SPE); // Set device as SPI slave just by enabling SPIz
}

void pwmEnable(){
  DDRD |= (1 << PD6) | (1 << PD5)| (1 << PD3); // Set PB1 (OCR0) to an input
  DDRB |= ( 1 << PB1);
  TCCR0A |= 0b10000011;
  TCCR0A |= (1 << COM0A1) | (1 << COM0A0)|(1 << COM0B1) | (1 << COM0B0);
  TCCR0B |= (1 << CS02) | (1 << CS00); // Divide the timer period by 1024
  // Setup PWM for pin D3
  TCCR2A |= 0b10000011;
  TCCR2A |= (1 << COM2B1) | (1 << COM2B0)|(1 << COM2A1) | (1 << COM2A0);
  TCCR2B |= (1 << CS22) | (1 << CS20); // Divide the timer period by 1024
  // Setup PWM for pin D9
  TCCR1A |= 0b10000011;
  TCCR1A |= (1 << COM1A1) | (1 << COM1A0);
  TCCR1B |= (1 << CS12) | (1 << CS10); // Divide the timer period by 1024
}

uint8_t spiTranciever (uint8_t spi_data)
{
  SPDR = spi_data; // Load byte to be shifted out
  while (! (SPSR & (1 << SPIF))); // Wait until interrupt flag is asserted. IF is asserted when transmission is complete
    PORTB |=  (1 << PB0);
    return (SPDR);
}

void hBridgeSetup(){
  DDRD |= (1 << PD4) | (1 << PD5);
  PORTD |= (1 << PD4); // 1,2 Enable
  PORTD &= ~(1 << PD5);
}

int main(){
  //spiSlaveEnable();
  pwmEnable();
  //hBridgeSetup();
  DDRB |= (1 << PD3)|(1 << PB1);
  PORTD &= ~(1 << PD3);
  //PORTD &= ~(1 << PB1);
  OCR0A = 250;
  OCR0B = 250;
  OCR2B = 250;
  OCR1A = 250;
  while(true){
   uint8_t response = spiTranciever(0x02);

  }
}
