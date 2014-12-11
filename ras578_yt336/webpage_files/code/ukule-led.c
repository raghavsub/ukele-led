#include "trtSettings.h"
#include "trtkernel_1284.c"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <avr/sleep.h>

// serial communication library
// Don't mess with the semaphores
#define SEM_RX_ISR_SIGNAL 1
#define SEM_STRING_DONE 2 // user hit <enter>
#include "trtUart.h"
#include "trtUart.c"
#include "chord_lookup_table.h"

#include <util/delay.h>
#include "WS2811.h"

#define BIT(B)           (0x01 << (uint8_t)(B))
#define SET_BIT_HI(V, B) (V) |= (uint8_t)BIT(B)
#define SET_BIT_LO(V, B) (V) &= (uint8_t)~BIT(B)

#define PAUSE  1000     // msec
#define DELAY    10	// msec
#define COUNT_INDEX  37
 
// Define the output function, using pin 0 on port a.
DEFINE_WS2811_FN(WS2811RGB, PORTA, 0)

// UART file descriptor
// putchar and getchar are in uart.c
FILE uart_str = FDEV_SETUP_STREAM(uart_putchar, uart_getchar, _FDEV_SETUP_RW);

// semaphore to protect shared variable
#define SEM_SHARED 3

// --- control LEDs from buttons and uart -------------------
// input arguments to each thread
// not actually used in this example
int args[2] ;

// song table containing chord indices at each time step
int song[1000];

// current indices into the song table and chord table
volatile int song_idx = 0;
volatile int chord_idx = 0;

// tempo of song
int bpm;

// time signature of song
int time_sig;

// current count-in value
int count;

// flag:
// 0 means nothing is happening
// 1 means we are in practice mode
// 2 means we are in play mode
char go = 0;

/* send the output signal to the RGB LEDs periodically */
void driveLED(void* args) {

	long rel;
	long dead;
	
	while (1) {

		// use RGB LED driver with current chord
        WS2811RGB(lookup_table[chord_idx], 16);

        rel = trtCurrentTime() + SECONDS2TICKS(0.01);
		dead = trtCurrentTime() + SECONDS2TICKS(0.01);
		trtSleepUntil(rel, dead);
	}
}

/* convert a song string (from USART) into a chord table */
void strToSong(char *str, int *song) {
	int song_idx = 0; 
	int str_idx = 0;
	while( str_idx < strlen( str ) ) {
		char buf[3];
		strncpy(buf, str + str_idx, 2);
		song[song_idx++] = atoi(buf);
		str_idx += 3;
	}

}

/* get the string from the USART */
void serialComm(void* args) {
	int val;
	char cmd[1000];

	while(1) {
		
        gets(cmd);
		trtWait(SEM_STRING_DONE);
	
        // don't interrupt the current song
		if (go != 2) {

            // practice mode
			if (cmd[0] == '1') {
				char buf1[3];
				strncpy(buf1, cmd + 2, 2);	
				chord_idx = atoi(buf1);
				go = 1;
				continue;
			}

            // play mode
			char buf2[4];
			strncpy(buf2, cmd + 2, 3);
			
			bpm = atoi(buf2);
			if (bpm < 60) {
				bpm = 60;
			}
			if (bpm > 240) {
				bpm = 240;
			}

            // convert bpm to timer period
			OCR3A = (62500 * 60) / bpm - 1;

			char buf3[2];
			strncpy(buf3, cmd + 6, 1);
			time_sig = atoi(buf3);
			if (time_sig < 1) {
				time_sig = 1;
			}

			count = 0;
			
			strToSong(cmd + 8, song);
			song_idx = 0;
			go = 2;
		}
	}
}

/* timer3 compare match ISR */
ISR (TIMER3_COMPA_vect) {
	if(go == 2) {
		if(count < time_sig) {
			chord_idx = COUNT_INDEX + count;
			count++;
		} else {
			chord_idx = song[song_idx];

            // end of song
			if(chord_idx == -1) {
				go = 0;
				chord_idx = 0;
			}
			song_idx++;
		}
	} else if (!go) {
		chord_idx = 0;
	}
}

/* MAIN */
int main(void) {

    // setup neopixel driver
    SET_BIT_HI(DDRA, 0);
    SET_BIT_LO(PORTA, 0);

    // setup timer 3
    TCCR3B = (1<<WGM32) + 0x04; // ctc, prescale by 256
    OCR3A = 10000; // 1 second (DEFAULT)
    TIMSK3= (1<<OCIE3A); // enable interrupt

    //init the UART -- trt_uart_init() is in trtUart.c
    trt_uart_init();
    stdout = stdin = stderr = &uart_str;
    fprintf(stdout,"\n\r TRT 9feb2009\n\r\n\r");

    // start TRT
    trtInitKernel(80); // 80 bytes for the idle task stack

    // --- create semaphores ----------
    // You must creat the first two semaphores if you use the uart
    trtCreateSemaphore(SEM_RX_ISR_SIGNAL, 0) ; // uart receive ISR semaphore
    trtCreateSemaphore(SEM_STRING_DONE,0) ;  // user typed <enter>

    // variable protection
    trtCreateSemaphore(SEM_SHARED, 1) ; // protect shared variables

    // --- creat tasks  ----------------
    trtCreateTask(driveLED, 100, SECONDS2TICKS(1), SECONDS2TICKS(1), &(args[0]));
    trtCreateTask(serialComm, 100, SECONDS2TICKS(0.1), SECONDS2TICKS(0.1), &(args[1]));
  
    // --- Idle task --------------------------------------
    // just sleeps the cpu to save power 
    // every time it executes
    set_sleep_mode(SLEEP_MODE_IDLE);
    sleep_enable();
    while (1) {
  	    sleep_cpu();
    }
}
