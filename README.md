# Pic2Hubble

This project is intended to produce images composed of 16x16 pixel clusters of space images mostly from by Hubble Space Telescope. The algorithm is written in Python. The app web runs with streamlit.
You can try it at: [PENDING]

-------
## Some examples: 
![FRtiGynXwAAFtka](https://user-images.githubusercontent.com/36217766/166343384-8e91849f-bb6f-42ab-af99-eaf973ec9562.jpg)

![278845614_4918775891565098_3132902473234924174_n](https://user-images.githubusercontent.com/36217766/166343038-d1171d18-f226-422b-9ae5-5a879899ae3e.jpg)

-------

## Approaches

### Algorithm v1
1) Save as a CSV file the average color per channel of all the images of the dataset.
2) Import the data from the CSV into a Pandas DataFrame.
3) Iterate over the input image with a slicing window of 16x16, calculate the average color per channel in the window and find the
the element k nearset in DataFrame. 
    1) Select a random image from the k images.
    2) Replace the window using the choosen astro mini photo.

### Algorithm v2
1) Save the average color of all the images in the dataset and save them in a CSV file.
2) Import the data from the CSV into a Pandas DataFrame.
3) Graph is generated, from color interval (0, 0, 0) to (step, step, step), where the step can be [3, 5, 15, 17, 51, 85], and then for each color channel, the interval is increased with by step value and the same process is continued for each color interval until the color reaches (255, 255, 255) and for each color interval a search is performed to find the 3 closest images based on the mean color over the Dataframe.
4) Iterate over the input image with a slicing window of 16x16, calculate the average color per channel in the window and then search the replacing image on the graph using DFS.
    1) Select a random image from the images available.
    2) Replace the slice for the image.

-------

## Setup

**Requeriments**

- [miniconda](https://docs.conda.io/projects/miniconda/en/latest/)


**Create virtual environment and install Python dependencies**

`make setup`

-------

## Run web app

**Activate virtual env**

`conda activate pic2hubble-streamlit`

**Run web app**

`streamlit run app.py`

-------

## Contribute
Feel free to open/help with issues. Fork the repo, create a branch from `main` branch, work your changes and open a Pull Request. 
