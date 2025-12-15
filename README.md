# FlappyBird-game

DESCRIERE

Acest proiect reprezintă o implementare a jocului clasic Flappy Bird, realizată în limbajul Python, folosind biblioteca Pygame. Jucătorul controlează o pasăre care trebuie să evite obstacolele de tip „pipe” prin apăsarea unei taste, scopul fiind obținerea unui scor cât mai mare.

FUNCTIONALITATE

Jocul permite controlul pasării prin intermediul tastaturii. La fiecare pereche de obstacole depășită cu succes, scorul jucătorului crește. Jocul se încheie atunci când pasărea intră în coliziune cu un obstacol sau iese din zona vizibilă a ecranului.
Dificultatea jocului crește progresiv pe parcursul jocului, prin:
-apariția din ce în ce mai frecventă a obstacolelor;
-creșterea vitezei de deplasare a acestora;
-micșorarea distanței dintre obstacole.
Scorul maxim obținut este salvat local și este afișat la rulările ulterioare ale jocului.

INTERFATA GRAFICA

Interfața grafică este realizată cu ajutorul bibliotecii Pygame. Jocul dispune de:
-o zonă principală de joc;
-butoane pentru pornirea și repornirea jocului;
-un ecran de start;
-un ecran de tip „Game Over”;
-o pagina informativa de tip „How to Play”.
De asemenea, aplicația oferă două moduri de joc: un mod clasic și un mod avansat, în care obstacolele se deplasează vertical pentru a crește nivelul de dificultate.

IMPLEMENTARE

Aplicația este organizată modular, folosind mai multe clase, fiecare având un rol bine definit:
-o clasă pentru gestionarea logicii principale a jocului;
-o clasă pentru jucător (pasărea);
-o clasă pentru obstacole;
-o clasă pentru gestionarea scorului maxim.
Logica jocului este separată de bucla principală și de partea de afișare, iar apariția obstacolelor este controlată pe baza timpului real, pentru a asigura un comportament constant indiferent de performanța sistemului.

TEHNOLOGII UTILIZATE

Aplicația este dezvoltată în Python 3 și utilizează următoarele tehnologii:
-Pygame – pentru interfața grafică, gestionarea inputului și bucla de joc;
-Programare orientată pe obiecte – pentru structurarea aplicației;
-Sistemul de fișiere – pentru salvarea scorului maxim.

RULARE

Pentru rularea aplicației este necesară instalarea bibliotecii Pygame. Jocul se pornește prin rularea fișierului principal al aplicației. Nu este necesară conexiune la internet, toate resursele fiind stocate local.
