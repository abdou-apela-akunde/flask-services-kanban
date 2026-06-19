\#Service 2 - Statistiques JSON



Ce service permet de faire des calculs statistiques avec des données envoyées en JSON.



\#POST /stats/describe



Cette route calcule :

\- la moyenne

\- la médiane

\- l'écart-type

\- la variance

\- le minimum

\- le maximum

\- q1

\- q3

\- l'étendue



\#POST /stats/correlation



Cette route calcule la corrélation de Pearson entre deux listes.



Le résultat `r` signifie :

\- `r` proche de 1 : forte corrélation positive

\- `r` proche de -1 : forte corrélation négative

\- `r` proche de 0 : faible corrélation



\#POST /stats/test\_normalite



Cette route utilise le test de Shapiro-Wilk pour vérifier si les données suivent une loi normale.



Si "p\_value > 0.05", les données sont considérées comme normales.



\#Installation



pip install -r requirements.txt



\#Lancement



python app.py



Le service tourne sur le port 5002.



\#Tests curl



\#Tester /stats/describe



curl -X POST http://127.0.0.1:5002/stats/describe \\

\-H "Content-Type: application/json" \\

\-d '{"data":\[12.5,15.3,8.7,21.0,13.2,9.8,17.6,11.4]}'



\#Tester /stats/correlation



curl -X POST http://127.0.0.1:5002/stats/correlation \\

\-H "Content-Type: application/json" \\

\-d '{"x":\[1,2,3,4,5],"y":\[2,4,6,8,10]}'



\#Tester /stats/test\_normalite



curl -X POST http://127.0.0.1:5002/stats/test\_normalite \\

\-H "Content-Type: application/json" \\

\-d '{"data":\[12,13,14,15,16,14,13,15]}'



\#Tests client



Le fichier client\_test.html permet de tester les routes avec des boutons.



Le fichier tests/test\_service2.py permet de tester les routes avec Python.



CORS est utilisé pour autoriser la page HTML à appeler l'API Flask.

