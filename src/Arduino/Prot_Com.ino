//VMOT
//GND
//AMARILLO
//AZUL
//MARRON
//ROJO
//VCC
//GND

#include <math.h>
#include <stdio.h>

int const stp1 = 2;
int const stp2 = 6;
int const dir1 = 3;
int const dir2 = 5;
float yaw=0;
float pitch=0;
int pos=0;
float ang;

void setup() 
{
    pinMode(stp1,OUTPUT);
    pinMode(stp2,OUTPUT);
    pinMode(dir1,OUTPUT);
    pinMode(dir2,OUTPUT);
    Serial.begin(9600);
}
 
void loop()
{
   if (Serial.available()>0) 
   {
      String str=Serial.readStringUntil('\n');
      float L=str.length();
      float posDP= str.indexOf(":");
      String inst=str.substring(0,posDP);
      String angulos=str.substring(posDP+1,L);
      float l=angulos.length();
      float pos=angulos.indexOf(".");
      int entero=angulos.substring(0,pos).toInt();
      int decimal=angulos.substring(pos+1,l).toInt();
      float ent=float(entero);
      float dec=float(decimal);
      if (entero>0)
      {
        ang=ent+(dec/1000.0);
      }
      if (entero<0)
      {
        ang=ent-(dec/1000.0);
      }
      if (entero==0)
      {
        if (str.substring(0,1)=="-")
        {
          ang=ent-(dec/1000.0);
        }
        else
        {
          ang=ent+(dec/1000.0);
        }
      }
      
        if(ang>0)
        {
          if (inst=="pitch")
          {
            pos=ang-pitch;
            if (pos>0)digitalWrite(dir1,HIGH);
            if (pos<0)digitalWrite(dir1,LOW);
            delay(100);
            if (pos>0)pasosTILT(pos);
            if (pos<0)pasosTILT(pos*-1);
            pitch=ang;
            Serial.print(pitch);
            Serial.print(":");
            Serial.println(yaw);
          }
          if (inst=="inc_pitch")
          {
            digitalWrite(dir1,HIGH);
            pasosTILT(ang);
            pitch=pitch+ang;
            Serial.print(pitch);
            Serial.print(":");
            Serial.println(yaw);
          }
          if (inst=="dec_pitch")
          {
            digitalWrite(dir1,LOW);
            pasosTILT(ang);
            pitch=pitch-ang;
            Serial.print(pitch);
            Serial.print(":");
            Serial.println(yaw);
          }
          if (inst=="yaw")
          {
            pos=ang-yaw;
            if (pos>0)digitalWrite(dir2,HIGH);
            if (pos<0)digitalWrite(dir2,LOW);
            delay(100);
            if (pos>0)pasosPAN(pos);
            if (pos<0)pasosPAN(pos*-1);
            yaw=ang;
            Serial.print(pitch);
            Serial.print(":");
            Serial.println(yaw);
          }
          if (inst=="inc_yaw")
          {
            digitalWrite(dir2,HIGH);
            pasosPAN(ang);
            yaw=yaw+ang;
            Serial.print(pitch);
            Serial.print(":");
            Serial.println(yaw);
          }
          if (inst=="dec_yaw")
          {
            digitalWrite(dir2,LOW);
            pasosPAN(ang);
            yaw=yaw-ang;
            Serial.print(pitch);
            Serial.print(":");
            Serial.println(yaw);
          }
        }
        if(ang==0)
        {
          if (inst=="pitch")
          {
            pos=ang-pitch;
            if (pos>0)digitalWrite(dir1,HIGH);
            if (pos<0)digitalWrite(dir1,LOW);
            delay(100);
            if (pos>0)pasosTILT(pos);
            if (pos<0)pasosTILT(pos*-1);
            pitch=ang;
            Serial.print(pitch);
            Serial.print(":");
            Serial.println(yaw);
          }
          if (inst=="yaw")
          {
            pos=ang-yaw;
            if (pos>0)digitalWrite(dir2,HIGH);
            if (pos<0)digitalWrite(dir2,LOW);
            delay(100);
            if (pos>0)pasosPAN(pos);
            if (pos<0)pasosPAN(pos*-1);
            yaw=ang;
            Serial.print(pitch);
            Serial.print(":");
            Serial.println(yaw);
          }
        }
        if(ang<0)
        {
          if (inst=="pitch")
          {
            digitalWrite(dir1,LOW);
            delay(100);
            pasosTILT(ang*-1);
            //ptotal=ptotal+ang;
            Serial.print(pitch);
            Serial.print(":");
            Serial.println(yaw);
          }
          if (inst=="yaw")
          {
            digitalWrite(dir2,LOW);
            delay(100);
            pasosPAN(ang*-1);
            //ptotal=ptotal+ang;
            Serial.print(pitch);
            Serial.print(":");
            Serial.println(yaw);
          }
        }
   }
}

int pasosTILT (float grados)
{ 
  long pulso=grados*442.294;  //convertir de grados a pulsos
  long pulsos=round(pulso);     //redondear al entero mas cercano
  for (long i=0;i<pulsos;i++)
    {
    digitalWrite(stp1,HIGH);
    delayMicroseconds(100);
    digitalWrite(stp1,LOW);
    delayMicroseconds(100);
    }
}


void pasosPAN (float grados)
{ 
  long pulso=grados*442.294;  //convertir de grados a pulsos
  long pulsos=round(pulso);     //redondear al entero mas cercano
  for (long i=0;i<pulsos;i++)
    {
    digitalWrite(stp2,HIGH);
    delayMicroseconds(100);
    digitalWrite(stp2,LOW);
    delayMicroseconds(100);
    }
}
