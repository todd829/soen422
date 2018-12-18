#include <avr/io.h>

void spiSlaveEnable (void){
  DDRB |= (1 << PB0);
  DDRB |= (1 << 4); // Set MISO as output. MOSI, SCK and SS are set to inputs
  SPCR |= (1 << SPE); // Set device as SPI slave just by enabling SPIz
}

void pwmEnable(){
  DDRD |= (1 << PD6) | (1 << PD5)| (1 << PD3) | (1 << PD7) | (1 << PD2); // Set PB1 (OCR0) to an input
  DDRB |= ( 1 << PB1);

  // Setup PWM for pins D5 and D6 || Timer 0
  TCCR0A |= 0b10000011;
  TCCR0A |= (1 << COM0A1) | (1 << COM0A0)|(1 << COM0B1) | (1 << COM0B0);
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
  PORTD &= ~(1 << PD5);
}

void backward(){
  // Since D9 uses timer it seems its a bit wonky and doesn't work like the other ADCs and wont turn off properly
  // To solve this we are turning of it's PWM and setting a LOW on it to turn it off
  DDRD |= (1 << PD3);
  DDRB &= ~(1 << PB1);
}

void forward(){
  // D9 or PB1 has it's pwm reconnected here in order to fix the Timer 1 issue
  // D3 100% = 0
  DDRB |= (1 << PB1);
  DDRD &= ~(1 << PD3);
}

void left(){
  OCR0A = 0; // D5
  OCR0B = 254; //D6
}

void right(){ 
  OCR0A = 254; // D5
  OCR0B = 0;  // D6
}

void high(){
  PORTD |= (1 << PD7);
  PORTD &= ~(1 << PD2);
}

void low(){
  PORTD |= (1 << PD2);
  PORTD &= ~(1 << PD7);
}

//TODO this is not working correctly
void stopOperation(){
  DDRB &= ~(1 << PB1);
  DDRD &= ~(1 << PD3);
  OCR0A = 0; // D5
  OCR0B = 0; //D6
  PORTD &= ~(1 << PD7) & ~(1 << PD2);
}

int main(){
  spiSlaveEnable();
  pwmEnable();
  hBridgeSetup();
  while(true){
   uint8_t response = spiTranciever(0x02);
   switch(response){
    case 1:
    forward();
    break;

    case 2:
    backward();
    break;

    case 3:
    left();
    break;

    case 4:
    right();
    break;

    case 5:
    high();
    break;

    case 6:
    low();
    break;

    default:
    stopOperation();
    break;
   }
  }
}
