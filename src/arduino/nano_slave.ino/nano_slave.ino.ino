#define BAUD 9600
#include <avr/io.h>
#include <util/setbaud.h>
#include <util/delay.h>

void spiSlaveEnable (void){
  DDRB |= (1 << PB0);
  DDRB |= (1 << 4); // Set MISO as output. MOSI, SCK and SS are set to inputs
  SPCR |= (1 << SPE); // Set device as SPI slave just by enabling SPIz
  Serial.begin(9600);
}

void pwmEnable(){
  DDRD |= (1 << PD6); // Set PB1 (OCR0) to an input
  TCCR0A |= 0b10000011;
  TCCR0A |= (1 << COM0A1) | (1 << COM0A0);
  TCCR0B |= (1 << CS02) | (1 << CS00); // Divide the timer period by 1024
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
  PORTD &= ~(1 << 6);
}

int main(){
  spiSlaveEnable();
  pwmEnable();
  hBridgeSetup();
  while(true){
   uint8_t response = spiTranciever(0x02);
   Serial.println(response);
   OCR0A = response;
  }
}
