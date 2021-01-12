// Vibracoes e Ondas 
// Trabalho Experimental - SONAR
// Codigo base (sonar.ino)
// Carlos Vinhais, Out 2020

const int TRIG_PIN = 2;
const int ECHO_PIN = 3;

unsigned long t0;
unsigned long t;
unsigned long t_acq;
unsigned long t_eco;

void setup() {  
  Serial.begin( 9600 );
  pinMode( TRIG_PIN, OUTPUT );
  pinMode (ECHO_PIN, INPUT );
  t0 = millis();                    // initial, t0
}

void loop() {
  
  /* ultrasonic pulse */
  digitalWrite( TRIG_PIN, HIGH );	// SONAR trigger
  delayMicroseconds( 10 );     		// wait 10 us
  digitalWrite( TRIG_PIN, LOW );	// end of pulse
 
  /* wait for echo pulse ... */
  /* echo time, t_eco (us)   */
  t_eco  = pulseIn( ECHO_PIN, HIGH );
  
  /* acquisition time, t_acq (us) */
  t = millis();
  t_acq = t - t0;
  
  /* SONAR calibration => v_som (m/s) */
  float v_som = 343.31;

  /* measured distance, d (mm) */
  int distance = 0.5 * v_som * (float)t_eco / 1000.0;
   distance = ((0.5*0.3427*(float)t_eco)-0.2853); 
  /* send data to serial port */
  Serial.print( t_acq );
  Serial.print( " " );
  //Serial.println( t_eco );    // for SONAR calibration
  Serial.println( distance );   // iif SONAR is calibrated 
  
  delay( 50 );                  // wait, 50 ms?
}
