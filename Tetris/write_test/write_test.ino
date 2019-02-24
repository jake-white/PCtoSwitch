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
  delay(25);                       // wait for a second
  digitalWrite(2, LOW);   // turn the LED on (HIGH is the voltage level)
}

void right() {
  digitalWrite(3, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(25);                       // wait for a second
  digitalWrite(3, LOW);   // turn the LED on (HIGH is the voltage level)
}

void drop() {
  digitalWrite(4, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(25);                       // wait for a second
  digitalWrite(4, LOW);   // turn the LED on (HIGH is the voltage level)  
}

void rotate() {
  digitalWrite(5, HIGH);   // turn the LED on (HIGH is the voltage level)
  delay(25);                       // wait for a second
  digitalWrite(5, LOW);   // turn the LED on (HIGH is the voltage level)
  rematch();
}

void rematch() {
  digitalWrite(5, HIGH);
  delay(1000);
  digitalWrite(5, LOW);
}

int distance = 0, rotations = 0;
bool dropped = true;
int data = "";
void loop() {
  Serial.print("Ready\n");
  while(Serial.available()==0) {
  }
  delay(100);
  data = Serial.parseInt();
  distance = (data/10)%10;
  rotations = abs(data%10);
  Serial.print(distance);
  Serial.print(rotations);
  dropped = false;
  while(rotations > 0) {
    rotate();
    delay(25);
    rotations--;
  }
  while(distance > 0) {
    right();
    delay(25);
    distance--;
  }
  while(distance < 0) {
    left();
    delay(25);
    distance++;
  }
  drop();
}
