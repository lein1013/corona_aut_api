# corona_aut_api
API service for Austria corona open data

## Aim of the API
The data is provided as large json dataset by the Austrian goverment and updated each friday (approximately 12:00).

For most applications only a very reduced dataset is needed, e.g. just the warning level of a specific city or region. 
This webservice downloads, caches and preprocesses the json dataset and only provides the relevant data to the requester.

See test folder for api urls examples. Therefore the REST Client https://marketplace.visualstudio.com/items?itemName=humao.rest-client in Visual Studio Code is used.


## Server:
This webservice is currently running at:
 - http://lein1013.pythonanywhere.com/

Feel free to run the code on your own server


## Links
 - Corona Ampel Austria: https://corona-ampel.gv.at/
   - Data Source Overview: https://www.data.gv.at/katalog/dataset/52abfc2b-031c-4875-b838-653abbfccf4e
 - Open Data: https://corona-ampel.gv.at/datendownload/
   - source 1: https://corona-ampel.gv.at/sites/corona-ampel.gv.at/files/assets/Warnstufen_Corona_Ampel_aktuell.json
   - source 2: https://corona-ampel.gv.at/sites/corona-ampel.gv.at/files/assets/Warnstufen_Corona_Ampel_Gemeinden_aktuell.json

