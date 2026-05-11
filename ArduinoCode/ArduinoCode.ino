const int trigPin = 9;
const int echoPin = 10;
const int buzzer = 3;
const int motorIN1 = 4;
const int motorIN2 = 5;

long duration;
int distance;

void setup() {
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  pinMode(buzzer, OUTPUT);
  pinMode(motorIN1, OUTPUT);
  pinMode(motorIN2, OUTPUT);
  digitalWrite(motorIN2, LOW);
  Serial.begin(9600);
}

void loop() {
  // Send ultrasonic pulse
  digitalWrite(trigPin, LOW);
  delayMicroseconds(3);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read echo
  duration = pulseIn(echoPin, HIGH);
  distance = duration * 0.034 / 2;
  Serial.println(distance);


  if ( distance < 50) {
    digitalWrite(buzzer, HIGH);
    digitalWrite(motorIN1, HIGH);
  } else {
    digitalWrite(buzzer, LOW);
    digitalWrite(motorIN1, LOW);
  }
  delay(200);
}
