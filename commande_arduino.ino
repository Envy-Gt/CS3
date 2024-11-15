#include <Adafruit_Keypad.h>


const byte ROWS = 3; // Trois lignes
const byte COLS = 3; // Trois colonnes

byte ROW_PINS[ROWS] = {20, 10, 0};    // Broches des lignes (à adapter selon votre câblage)
byte COL_PINS[COLS] = {7, 8, 1};      // Broches des colonnes (à adapter selon votre câblage)

char keys[ROWS][COLS] = {
  {'U', 'L', 'D'},
  {'R', 'S', 'R'},
  {'A', 'B', '9'}
};

Adafruit_Keypad keypad = Adafruit_Keypad(makeKeymap(keys), ROW_PINS, COL_PINS, ROWS, COLS);

// Variables pour gérer le maintien de touche
bool keyHeld[ROWS][COLS] = {false};  // État de maintien de chaque touche
unsigned long keyHoldTime[ROWS][COLS] = {0}; // Temps de maintien de chaque touche
const unsigned long holdThreshold = 500; // Durée en millisecondes pour considérer comme "maintenu"

void setup() {
  Serial.begin(115200);
  Serial.println("Hello from Arduino!");
  keypad.begin();
}

void loop() {
  keypad.tick();
  if (Serial.available() > 0) {
    String data = Serial.readString();
    // Traitez les données reçues ici si nécessaire
  }

  while (keypad.available()) {
    keypadEvent e = keypad.read();
    char key = e.bit.KEY;

    if (e.bit.EVENT == KEY_JUST_PRESSED) {
      // Quand une touche est pressée
      if (key == 'U') {
        Serial.println("UP");
      } else if (key == 'D') {
        Serial.println("DOWN");
      } else if (key == 'A') {
        Serial.println("RIGHT");
      } else if (key == 'B') {
        Serial.println("LEFT");
      }
      // Initialiser le maintien de la touche
      keyHeld[e.bit.ROW][e.bit.COL] = true;
      keyHoldTime[e.bit.ROW][e.bit.COL] = millis(); // Enregistrer le temps de pression
    } else if (e.bit.EVENT == KEY_JUST_RELEASED) {
      // Quand une touche est relâchée
      Serial.print("Key released: ");
      Serial.println(key);
      // Réinitialiser l'état de maintien
      keyHeld[e.bit.ROW][e.bit.COL] = false;
    }
  }

  // Vérifier les touches maintenues
  for (byte row = 0; row < ROWS; row++) {
    for (byte col = 0; col < COLS; col++) {
      if (keyHeld[row][col]) {
        // Vérifier si la durée de maintien a dépassé le seuil
        if (millis() - keyHoldTime[row][col] >= holdThreshold) {
          // Imprimer le message de maintien
          if (keys[row][col] == 'U') {
            Serial.println("UP (held)");
          } else if (keys[row][col] == 'D') {
            Serial.println("DOWN (held)");
          } else if (keys[row][col] == 'A') {
            Serial.println("RIGHT (held)");
          } else if (keys[row][col] == 'B') {
            Serial.println("LEFT (held)");
          }
        }
      }
    }
  }
}