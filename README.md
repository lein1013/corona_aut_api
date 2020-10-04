# corona_aut_api
API service for Austria corona open data

## Aim of the API
The data is provided as large json dataset by the austrian goverment and updated approximately once a week (on friday).

For most applications only a very reduced dataset is needed, e.g. just the warning level of a specific city. 
This webservice downloads, caches and preprocesses the json dataset and only provides the relevant data to the requester.

see test for 


## Links
 - webservice running on python anywhere.com: 
http://lein1013.pythonanywhere.com/

 - Corona Ampel Austria: https://corona-ampel.gv.at/
 - Open Data: https://corona-ampel.gv.at/datendownload/
   - source 1: https://corona-ampel.gv.at/sites/corona-ampel.gv.at/files/assets/Warnstufen_Corona_Ampel_aktuell.json
   - source 2: https://corona-ampel.gv.at/sites/corona-ampel.gv.at/files/assets/Warnstufen_Corona_Ampel_Gemeinden_aktuell.json
   - source 3 (not maintained): https://corona-ampel.gv.at/sites/corona-ampel.gv.at/files/coronadata/CoronaKommissionV2.json
