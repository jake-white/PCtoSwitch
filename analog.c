// Simple analog to digitial conversion

#include <avr/io.h>
#include <avr/pgmspace.h>
#include <stdint.h>

#if defined(__AVR_AT90USB162__)
int16_t analogRead(uint8_t pin) { return 0; }  // no ADC on '162 chip
#else

int16_t analogRead(uint8_t pin)
{
	uint8_t low;

	DIDR0 |= 0x01;
	ADCSRA = (1<<ADEN) | (1<<ADPS2) | (1<<ADPS1) | (1<<ADPS0);
	ADMUX = 0x40;  // channel 0, ref=vcc
	ADCSRA |= (1<<ADSC);
	while (ADCSRA & (1<<ADSC)) ;
	low = ADCL;
	return (ADCH << 8) | low;
}

#endif

