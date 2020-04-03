# Lyric-Recommender
I used unsupervised machine learning techniques to create a recommender which takes original song lyrics as input and recommends an artist with a similar writing style.

The recommender can be run simply by running the Recommender.ipynb jupyter notebook from the model_recommender folder, but I've included all of the files to show my process and to allow for partial replication.

**Tools**  
Python 3  
 - pandas  
 - numpy  
 - scipy  
 - sklearn  
 - gensim  
 - nltk  
 - textblob  
 - matplotlib  
 - selenium  
 - beautifulsoup  
 - pymongo  
MongoDB  
AWS ec2  

**Data**  
The data consists of lyrics scraped from genius.com for tracks from the albums on
Pitchfork's list of the top 200 albums of the 2010s. For the sake of getting experience
with unstructured data and mongoDB, I web-scraped the lyrics and then uploaded them to a
mongo database on an AWS ec2 instance. Since this instance is no longer running, this portion
of the project in not replicable without setting up a mongo database or changing the code to skip
this step. The code for this process in in the files '01 Lyric Data Scrape.ipynb' and
'01 Uploaded jsons to mongo.ipynb' and the functions that make these notebooks run are in
'data_acquisition_functions.py'.  

'02 Data Cleaning.ipynb' is in the 'model_recommender' folder and contains code to retrieve and clean
the text data from the mongoDB and then saves it in two csv files. 'lyric_data.csv' has the full dataset with songs as rows. This dataset is not used in the recommender so it can be discarded.
'lyrics_by_artist.csv' contains the same data but each row of data is an artist. This is
the dataset used for the recommender.  

**Model**  
'03 Model Training.ipynb' contains the code for training the model and created recommendations
based on input text. It uses 'lyrics_by_artist.csv' for the training and the pickled files
for the recommendation, but I recommend running the 'Recommender.ipynb' separately since the
recommender in the training notebook will be using previously trained pickles for the recomendation.  

**Presentation**  
'Lyric Recommender Presentation.pdf' contains slides from my presentation of this project for 
the Metis Data Science Bootcamp.
