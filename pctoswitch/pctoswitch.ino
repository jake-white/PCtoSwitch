void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(2, OUTPUT); 
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
}

bool left,right,up,down,a,b, lymin, lymax, lxmin, lxmax;
void loop() {
  while(Serial.available() == 0){}
  char command = Serial.read();
  if(command=='0') {
    left = !left;
    digitalWrite(2, left);
  }
  if(command=='1') {
    right = !right;
    digitalWrite(3, right);
  }
  if(command=='2') {
    up = !up;
    digitalWrite(4, up);
  }
  if(command=='3') {
    down = !down;
    digitalWrite(5, down);
  }
  if(command=='4') {
    a = !a;
    digitalWrite(6, a);
  }
  if(command=='5') {
    b = !b;
    digitalWrite(7, b);
  }
  if(command=='6') {
    lymin = !lymin;
    digitalWrite(8, lymin);
  }
  if(command=='7') {
    lymax = !lymax;
    digitalWrite(9, lymax);
  }
  if(command=='8') {
    lxmin = !lxmin;
    digitalWrite(10, lxmin);
  }
  if(command=='9') {
    lxmax = !lxmax;
    digitalWrite(11, lxmax);
  }
}
