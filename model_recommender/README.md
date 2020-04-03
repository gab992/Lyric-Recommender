# Data Files  
**lyrics_data.csv**  
Contains all lyrics separated by song. This dataset is not used in the modeling or recommender
so it can be discarded.  

**lyrics_by_artist.csv**  
Contains all lyrics separated by artist. This dataset is used by '03 Modeling and recommender.ipynb'.  

# Code  
**02 Data Cleaning.ipynb**  
Contains code for retrieving data from mongoDB, cleaning it, and creating
both lyrics_data.csv and .csv.  

**03 Modeling and recommender.ipynb**  
Contains code for training the models, creating all necessary pickled objects,
and running the recommender. **NOTE:** the recommender will be using the pickled objects that
exist prior to this notebook being run, so I recommend running the separate recommender notebook
after retraining the models if you are retraining the models.  

**Recommender.ipynb**  
Runs the recommender as long as all pickled objects are present.  

**model_functions.py**  
Contains all functions necessary to make the jupyter notebooks in this directory work.  

# Pickled objects  
- count_vec.pickle  
- hiphop_vec.pickle  
- other_vec.pickle  
- first_lda.pickle  
- hiphop_lda.pickle  
- other_lda.pickle  
- full_hiphop.pickle  
- full_other.pickle  
