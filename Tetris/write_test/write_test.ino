void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(2, OUTPUT); 
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  rematch();
}

void left() {
  digitalWrite(2, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(50);                       // wait for a second
  digitalWrite(2, LOW);   // turn the LED on (HIGH is the voltage level)
}

void right() {
  digitalWrite(3, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(50);                       // wait for a second
  digitalWrite(3, LOW);   // turn the LED on (HIGH is the voltage level)
}

void drop() {
  digitalWrite(4, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(100);                       // wait for a second
  digitalWrite(4, LOW);   // turn the LED on (HIGH is the voltage level)  
}

void rotate() {
  digitalWrite(5, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(100);                       // wait for a second
  digitalWrite(5, LOW);   // turn the LED on (HIGH is the voltage level)
  rematch();
}

void rematch() {
  digitalWrite(5, HIGH);
  delay(1000);
  digitalWrite(5, LOW);
}

int distance = 0;
bool dropped = true;
void loop() {
  while(Serial.available()==0) { // Wait for User to Input Data  
    
  }
  distance = Serial.parseInt();
  dropped = false;
  while(distance > 0) {
    right();
    delay(50);
    distance--;
  }
  while(distance < 0) {
    left();
    delay(50);
    distance++;
  }
  drop();
}
