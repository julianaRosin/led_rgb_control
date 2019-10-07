/***********************************************************
File name: 09_rgbLed.ino
Description: Control the RGB LED
Author: Juliana
 
*************************************************************/
String cor;
String red;
String green;
String blue;
int R,G,B;

//Function color

void color_led(int r, int g, int b){
  analogWrite(9,255-b); // PWM signal output
  analogWrite(10,255-g); // PWM signal output
  analogWrite(11,255-r); // PWM signal output
}
 
void setup()
{
   Serial.begin(9600);
  
   pinMode(9, OUTPUT); //blue
   pinMode(10, OUTPUT);//green
   pinMode(11, OUTPUT); //red
}
 
void loop()
{
  if(Serial.available()){
    cor = Serial.readString();
    red = cor.substring(0,3);
    green = cor.substring(3,6);
    blue = cor.substring(6,9); 
    R = red.toInt();
    G = green.toInt();
    B = blue.toInt();
    color_led(R,G,B);
  } 
}
