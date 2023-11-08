# EMA-GalaTablePlacer

This application predict a good enought table placement to satisfy those requirements:  
- Codes should be automaticaly modified by pre processing algortihme.
- Each table should be as close as possible to the friend table.  

## 📚 How to use

### [Visit this website to use this app](https://ema-galatableplacer.streamlit.app/)  
Soon ...


## ⚙️ How it works
### Preprocessing data
The application will first load the data and will aplly filters to stabilalise them.
- Column "Prénom" we will lower case the text and upper case the first letter.
- Column "Nom" we will upper case the text
- Column "Code table" to prevent code error from users, we will relace all the none values with "NOTABLE", next we will remove or replace accent and special caractere and upper case everything, finally we only keep letters and digits.
- Column "Code table ami" to prevent code error from users, we will remove or replace accent and special caractere and upper case everything, finally we only keep letters and digits.  

The code is in [loaders.py](src/loaders.py)
### Cast data to processable data for algorithm
The code is in [calculators.py](src/calculators.py)
### Search solution
The code is in [tables.y](src/tables.py)

## 🐳 How to deploy on premise
**You'll need to have Docker and docker-compose installed.**  

Clone this git repository
> git clone git@github.com:ChadEstoupStreiff/EMA-GalaTablePlacer.git

Edit .env with your parameters
> nano .env

Launch the app with docker compose
> docker-compose up -d