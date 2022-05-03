# Pic2Hubble

This project is intended to produce images composed of 16x16 pixel clusters of space images mostly from the Hubble telescope, the algorithm is written in Python using and Flask API returning the base 64 image, and the frontend is developed in React JS.
You can try it at https://pic2hubble.herokuapp.com/

## Some examples: 
![FRtiGynXwAAFtka](https://user-images.githubusercontent.com/36217766/166343384-8e91849f-bb6f-42ab-af99-eaf973ec9562.jpg)
![278845614_4918775891565098_3132902473234924174_n](https://user-images.githubusercontent.com/36217766/166343038-d1171d18-f226-422b-9ae5-5a879899ae3e.jpg)

## Approaches
### V1
1) We save the average color of all the images in the dataset and save them in a CSV.
2) Export the data from the CSV into a Pandas Dataframe
3) Iterate all 16x16 slices of the image calculate the average and find the element k nearset in Dataframe
    1) Select a random image from the k images
    2) Replace the slice for the image
### V2
1) We save the average color of all the images in the dataset and save them in a CSV.
2) Export the data from the CSV into a Pandas Dataframe
3) Graph is generated, from color interval (0, 0, 0) to (step, step, step), where the step can be [3, 5, 15, 17, 51, 85], and then for each color channel, the interval is increased with by step value and the same process is continued for each color interval until the color reaches (255, 255, 255) and for each color interval a search is performed to find the 3 closest images based on the mean color over the Dataframe.
4) Iterate all the 16x16 slices of the image calculate the avarage search on the graph using DFS
    1) Select a random image from the images available
    2) Replace the slice for the image
## Setup Frontend
```
npm install
npm start
```
## Setup Backend

**Requeriments**

- [virtualenv](https://virtualenv.pypa.io/en/latest/)

**Create virtual env**

`virtualenv .venv --python=python3.8`

**Activate virtual env**

`source .venv/bin/activate`

**Install dependencies**

`pip install -r requirements.txt`

**Add the next variables on .venv/bin/activate**
```
export FLASK_APP="entrypoint:app"
export FLASK_ENV="development"
export APP_SETTINGS_MODULE="api.config.default"
```
```
flask run 
```
**Activate virtual env**

`source .venv/bin/activate`

**Deactivate virtual env**

`deactivate`

