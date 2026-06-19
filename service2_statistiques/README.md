\#Service 2



ça permet de faire des calculs statistiques avec des données envoyées en JSON.



\#Routes



POST /stats/describe



Cette route calcule tout ce qui est:

moyenne, médiane, écart-type, variance, minimum, maximum



Puis POST /stats/correlation



qui calcule la corrélation entre deux listes de nombres.



POST /stats/test\_normalite



Permet de savoir si les données suivent une loi normale.



Installation



Installer les bibliothèques avec pip install -r requirements.txt





Lancer le programme :



python app.py



Le service fonctionne sur le port 5002.



Les Tests ont étaient fait avec Curl.



Le fichier client\_test.html est utile pour faire des tests des routes avec des boutons. CORS sert à autoriser la page HTML à appeler l'API Flask.

