#include <avr/io.h>

void spiSlaveEnable (void){
  DDRB |= (1 << PB0);
  DDRB |= (1 << 4); // Set MISO as output. MOSI, SCK and SS are set to inputs
  SPCR |= (1 << SPE); // Set device as SPI slave just by enabling SPIz
}

void pwmEnable(){
  DDRD |= (1 << PD6) | (1 << PD5)| (1 << PD3); // Set PB1 (OCR0) to an input
  DDRB |= ( 1 << PB1);

  // Setup PWM for pins D5 and D6 || Timer 0
  TCCR0A |= 0b10000011;
  TCCR0A |= (1 << COM0A1) | (1 << COM0A0)|(1 << COM0B1) | (1 << COM0B0);
  TCCR0B |= (1 << CS02) | (1 << CS00); // Divide the timer period by 1024
  
  // Setup PWM for pin D3 || Timer 2
  TCCR2A |= 0b10000011;
  TCCR2A |= (1 << COM2B1) | (1 << COM2B0)|(1 << COM2A1) | (1 << COM2A0);
  TCCR2B |= (1 << CS22) | (1 << CS20); // Divide the timer period by 1024
  // Setup PWM for pin D9 || Timer 1
  
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

void forward(){
  // Since D9 uses timer it seems its a bit wonky and doesn't work like the other ADCs and wont turn off properly
  // To solve this we are turning of it's PWM and setting a LOW on it to turn it off
  TCCR1A = 0b10000000;
  OCR2B = 20;   // D3 100% = 0
  DDRD &= ~(1 << PB1);
}

void backward(){
  // D9 or PB1 has it's pwm reconnected here in order to fix the Timer 1 issue
  // D3 100% = 0
  TCCR1A |= 0b10000011;
  TCCR1A |= (1 << COM1A1) | (1 << COM1A0);
  OCR2B = 254;  // D3 100% = 0 | 0% = 254
  OCR1A = 0;
}

void left(){
  OCR0A = 0; // D5
  OCR0B = 254; //D6
}

void right(){ 
  OCR0A = 254; // D5
  OCR0B = 0;  // D6
}

//TODO this is not working correctly
void stopOperation(){
  OCR0A = 254;
  OCR0B = 0;
  OCR2B = 254;
  OCR1A = 0;
}

int main(){
  spiSlaveEnable();
  pwmEnable();
  hBridgeSetup();
  while(true){
   uint8_t response = spiTranciever(0x02);
   switch(response){
    // GO PAT
    case 1:
    break;
   }
  }
}
