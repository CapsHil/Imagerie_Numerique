# Imagerie_Numerique

To launch a script without python & opencv installed, go to `/dist` and launch script like bash script

./resize : `./resize [-i INPUT] [-o OUTPUT] [--crop=[X]:[Y]] [--resize=[HEIGHT]]`

Exemple : `./resize -i ./img/oklm.jpg -o ./img/oklm_cropped.jpg --crop=280:300`


./filter : `./filters [-i INPUT] [-o OUTPUT] [--pencil] [--cartoon][--darker] [--sepia] [--gray] [--thermic]`

Exemple : `./filters -i ./img/oklm.jpg -o ./img/oklm_sepia.jpg --sepia`


To run the nodejs server :

`npm install`
`npm install -g nodemon`
`npm start`

In your browser, go to `http://localhost:4200`