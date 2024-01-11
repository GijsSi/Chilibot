#include "Relay.h"
#include "Wire.h"
#include <AccelStepper.h>
#include <mcp_can.h>
#include <SPI.h>

// CAN 'CS' pin
MCP_CAN CAN0(10);

// Relay setup
Relay solenoid_valve(9, false); 
Relay waterpump(8, false);
Relay grow_light(7, false); 

// Ultrasonic sensor setup
const int trigPin = 6;
const int echoPin = 5;
long duration;
int distance;

// I2C sensor setup for soil moisture and air parameters
#define address 0x40
uint8_t buf_air[4] = {0};
uint8_t buf_soil[4] = {0};
uint16_t data1;
float soilMoistureHumidity;

// Struct to hold air temperature and humidity
struct SensorData {
    float airTemperature;
    float airHumidity;
};

// Struct for CAN messages
struct CANMessage {
    uint8_t command;
    float data;
};

// Stepper motor setup
const int dirPin = 3;  // Adjusted as per request
const int stepPin = 4;  // Adjusted as per request

#define motorInterfaceType 1
AccelStepper myStepper(motorInterfaceType, stepPin, dirPin);

void setup() {
  // CAN bus setup
  CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ);  // Initialize CAN0
  CAN0.setMode(MCP_NORMAL);   // Set operation mode to normal so the MCP2515 sends acks to received data.

  // waterLevelDetection setup
  pinMode(0, INPUT);

  // Relay setup
  solenoid_valve.begin(); 
  waterpump.begin();
  grow_light.begin();
  
  // Ultrasonic sensor setup
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT);  
  Serial.begin(9600);      
  
  // I2C setup
  Wire.begin();

  // Reset SoilMoistureSensor
  writeI2CRegister8bit(0x20, 6);

  // Stepper motor setup
  myStepper.setMaxSpeed(1000);
  myStepper.setAcceleration(5000);
  myStepper.setSpeed(700);
  myStepper.moveTo(0); // Start at position 0 cm
}

void loop() {
  // int avgDistance = getAverageDistance();
  // Serial.print("Average Distance: ");
  // Serial.println(avgDistance);

  // float currentSoilMoisture = getSoilMoistureHumidity();
  // Serial.print("Soil Moisture(%RH): ");
  // Serial.println(currentSoilMoisture);

  // SensorData airData = readAirTemperatureAndHumidity();
  // Serial.print("Air temp(C):");
  // Serial.print(airData.airTemperature);
  // Serial.print("\n");
  // Serial.print("Air hum(%RH):");
  // Serial.println(airData.airHumidity);
  // Serial.print("\n");

  // // Example: Turn on grow light based on distance.
  // if (avgDistance < 50) {
  //     turnGrowLightOn();
  // } else {
  //     turnGrowLightOff();
  // }
  
  // // Turn on the pump and solenoid for 10 seconds every loop.
  // turn_pump_sol_on();
  // delay(10000);

  // // Stepper motor actions
  // moveUp(160);
  // delay(1000);
  // moveDown(160);
  // delay(1000);

  // Read CAN messages
  readCANMessages();
}

void turn_pump_sol_on() {
  solenoid_valve.turnOn();
  waterpump.turnOn();
  delay(10000);
  solenoid_valve.turnOff();
  waterpump.turnOff();
}

void turnGrowLightOn() {
  grow_light.turnOn();
}

void turnGrowLightOff() {
  grow_light.turnOff();
}

int getAverageDistance() {
  int totalDistance = 0;
  
  for (int i = 0; i < 10; i++) {
    digitalWrite(trigPin, LOW);
    delayMicroseconds(2);
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(10);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance = duration * 0.034 / 2;
    totalDistance += distance;
    delay(50);
  }

  return totalDistance / 10;
}

float getSoilMoistureHumidity() {
  uint16_t rawCapacitance = readI2CRegister16bit(0x20, 0);
  Serial.print("Raw Capacitance: "); // For debugging
  Serial.println(rawCapacitance);
  
  // Linearly map raw capacitance value to humidity percentage based on observed max value
  float soilHumidityPercentage = (float)rawCapacitance / 460.0 * 100.0;
  
  // Clamp the percentage between 0 and 100
  if (soilHumidityPercentage > 100.0) {
    soilHumidityPercentage = 100.0;
  } else if (soilHumidityPercentage < 0) {
    soilHumidityPercentage = 0;
  }
  
  return soilHumidityPercentage;
}

SensorData readAirTemperatureAndHumidity() {
    SensorData result;
    readReg(0x00, buf_air, 4);

    uint16_t rawData = buf_air[0] << 8 | buf_air[1];
    uint16_t rawData1 = buf_air[2] << 8 | buf_air[3];

    result.airTemperature = ((float)rawData * 165 / 65535.0) - 40.0;
    result.airHumidity = ((float)rawData1 / 65535.0) * 100;

    return result;
}

int waterLevelDetection() {
    int sensorValue = digitalRead(0);  // Reads the value from digital pin 0
    if(sensorValue == HIGH) {  // Assumes HIGH means water is detected
        return 1;
    } else {
        return 0;
    }
}

// =========== CAN bus logic ==============

// Send CAN messages
void sendCANMessage(uint8_t command, float data) {
    CANMessage message;
    message.command = command;
    message.data = data;
    CAN0.sendMsgBuf(0x100, 0, sizeof(message), (uint8_t*)&message);  // send data:  id = 0x100, standard frame, data len = sizeof(message), data buf = message
}

// Read CAN messages
void readCANMessages() {
    long unsigned int rxId;
    unsigned char len = 0;
    unsigned char rxBuf[8];
    if (CAN0.checkReceive() == CAN_MSGAVAIL) {
        CAN0.readMsgBuf(&rxId, &len, rxBuf);    // Read data: len = data length, buf = data byte(s)
        CANMessage* message = (CANMessage*)rxBuf;
        
        // Display received data on Serial Monitor
        Serial.print("Received CAN Message. Command: ");
        Serial.print(message->command, HEX);  // Print command in HEX
        Serial.print(", Data: ");
        Serial.println(message->data, DEC);  // Print data in DEC
        
        executeCommand(message->command, message->data);
    }
}

// void readCANMessages() {
//     long unsigned int rxId;
//     unsigned char len = 0;
//     unsigned char rxBuf[8];
//     if (CAN0.checkReceive() == CAN_MSGAVAIL) {
//         CAN0.readMsgBuf(&rxId, &len, rxBuf);    // Read data: len = data length, buf = data byte(s)
//         CANMessage* message = (CANMessage*)rxBuf;
//         executeCommand(message->command, message->data);
//     }
// }


void executeCommand(uint8_t command, float data) {
    switch (command) {
        case 0x01:  // Command to move motor to a specific position
            moveToPosition((int)data);
            break;
        case 0x02:  // Command to request average distance
            sendCANMessage(0x02, getAverageDistance());
            break;
        case 0x03:  // Command to request soil moisture
            sendCANMessage(0x03, getSoilMoistureHumidity());
            break;
        case 0x04:{  // Command to request air temperature and humidity
            SensorData airData = readAirTemperatureAndHumidity();
            sendCANMessage(0x04, airData.airTemperature);  // Sending temperature
            sendCANMessage(0x05, airData.airHumidity);    // Sending humidity
            break;
            }
        case 0x06:  // Command to turn on grow light
            turnGrowLightOn();
            break;
        case 0x07:  // Command to turn off grow light
            turnGrowLightOff();
            break;
        case 0x08:  // Command to turn on pump and solenoid valve for 10 seconds
            turn_pump_sol_on();
            break;
        case 0x09:  // Command to move motor up by a certain number of centimeters
            moveUp((int)data);
            break;
        case 0x0A:  // Command to move motor down by a certain number of centimeters
            moveDown((int)data);
            break;
        case 0x0B:  // Command to check water level
            sendCANMessage(0x0B, waterLevelDetection());
            break;
        default:
            // Unknown command
            Serial.println("Unknown command received");
            break;
    }
}

uint8_t readReg(uint8_t reg, const void* pBuf, size_t size) {
  if (pBuf == NULL) {
    Serial.println("pBuf ERROR!! : null pointer");
    return 0;
  }
  uint8_t * _pBuf = (uint8_t *)pBuf;
  Wire.beginTransmission(address);
  Wire.write(&reg, 1);
  if (Wire.endTransmission() != 0) {
    return 0;
  }
  delay(20);
  Wire.requestFrom(address, (uint8_t) size);
  for (uint16_t i = 0; i < size; i++) {
    _pBuf[i] = Wire.read();
  }
  return size;
}
unsigned int readI2CRegister16bit(int addr, int reg) {
  Wire.beginTransmission(addr);
  Wire.write(reg);
  Wire.endTransmission();
  delay(20);
  Wire.requestFrom(addr, 2);
  unsigned int t = Wire.read() << 8;
  t = t | Wire.read();
  return t;
}

void writeI2CRegister8bit(int addr, int value) {
  Wire.beginTransmission(addr);
  Wire.write(value);
  Wire.endTransmission();
}
// ========= STEPPER MOTOR CONTROL =========

// Function to move the motor up by a certain number of centimeters
void moveUp(int cm) {
  long steps = cm * 200; // Example: 200 steps per centimeter
  myStepper.move(steps);
  while (myStepper.distanceToGo() != 0) {
    myStepper.run();
  }
}

// Function to move the motor down by a certain number of centimeters
void moveDown(int cm) {
  long steps = cm * 200; // Example: 200 steps per centimeter
  myStepper.move(-steps);
  while (myStepper.distanceToGo() != 0) {
    myStepper.run();
  }
}

void moveToPosition(int targetPosCm) {
    int tolerance = 1;  // Tolerance in cm, adjust as needed
    int measuredDistance;

    do {
        measuredDistance = getAverageDistance();  // Get the current measured distance

        if (abs(measuredDistance - targetPosCm) <= tolerance) {
            // Close enough, stop the motor
            myStepper.stop();
        } else if (measuredDistance > targetPosCm) {
            // Measured distance is too far, move down
            myStepper.move(-200);  // Move 1 cm down
        } else {
            // Measured distance is too close, move up
            myStepper.move(200);  // Move 1 cm up
        }

        while (myStepper.distanceToGo() != 0) {
            myStepper.run();
        }

    } while (abs(measuredDistance - targetPosCm) > tolerance);  // Continue until within tolerance
}


