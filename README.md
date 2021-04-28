# Food-Search-Engine

## Introduction:

With world facing grievous pandemic, more and more business and industries have moved online and work from home is becoming more and more popular. Some of the industry leading organizations have already announced that they will be allowing employees to permanently work from home even after the pandemic. This change is starting to affect many different industries in the way how they function. One such industry is food delivery platforms such as uber eats and skip the dishes. Food delivery platforms are seeing surge in customer base all around the globe due to work from home and less and less restaurants offering in house dinning due to covid. 

These food delivery platform offers you functionality to order from affiliated restaurants in metro city areas. A user can search based on restaurants and dishes. Some platform also offers feature to search based on food cuisine. 
 
This project proposes feature that can further optimise user experience of these food delivery platform by promoting all type of customer base and most importantly reinforce trust of many sceptical customer who are quite selective in their food choices due to various reasons such as religious obligations, health limitations and most of the times due to personal preferences. Currently these food delivery platforms are quite limited in terms of information they provide about food and what ingredients are used to prepare them. 

![alt text](https://github.com/kishanpatel-hub/Food-Search-Engine/blob/main/Project/static/WhatsApp%20Image%202021-03-23%20at%204.08.56%20PM%20(1).jpeg)

## Problem Description:


Due to pandemic, More and more restaurants are relying on food delivery platform as their primary source of revenue which is quite competitive but rewarding as well. These restaurants boost their businesses by offering different types of cuisine and variety of food options. This is good news for the delivery platform since they have more and more food options which leads to increase in customer base. 

As the customer base increases so does the diversity among them. Particularly in multi cultured cities like Vancouver, people belonging to different culture and background are trying different types of cuisines without any kind of prior knowledge about the food and how it is prepared.  Some restaurants also offer fusion of different cuisine. Each of these different cuisines have their own signature ingredients to offer unique dishes. 

This leads to good news for foodies as with single click there are wide range of food options available. But this also leads to growing concern for users who are too specific about their food and do not want certain ingredients, or they might be allergic to some things. Such customers are always sceptical ordering online as they are not sure which dishes suits their requirement and which does not. Food delivery platforms offers features to provide instructions to define their choices. this can be used when someone is ordering dish which they have never tried before, but what if restaurants are unable to make that dish without those ingredients. 

For example, in the following image we can see this bakery item is available but there is no way to know for sure if it contains eggs or not. Or even if it can be made without eggs or not. In reality, Torte shown in the image above contains eggs. In fact, eggs are one of the main ingredients. If this item is ordered with instructions of making it eggless, it results in either restaurants cancelling the order or customer receiving order which they do not want. Either way this is not a good customer experience. But what if these kinds of situations can be avoided by simply offering customers more options while ordering food? What if we can help customers who do not know about particular dish but know what they would like in their food?


![alt text](https://github.com/kishanpatel-hub/Food-Search-Engine/blob/main/Project/static/WhatsApp%20Image%202021-03-23%20at%204.08.56%20PM.jpeg)
 

## Solution Proposed:

This proposal offers solution to this issue by integrating two-way customised food search functionality where users can search for dishes while specifying things they do not want, or search based on specific ingredients they want to have. This type of search features instantly solves issues described earlier and offers customer more flexibility in their food search. 

The solution can be achieved by appropriate indexing of dish information such as ingredients and custom ranking model which supports various query formats from field query to phrase query. Ranking can be performed based exact query match and relevance to the user query. Ranking model can retrieve fix set of dishes fitting the user criteria. 

The proposed search uses specified data source and Food search APIs specified below to search for the ingredients of the dishes and show the dishes which does or does not contain specific ingredients. Multiple Source of data is used in order to avoid discrepancy among ingredient of particular dish. 

## Datasets:

### Static Datasets:

Link to dataset: https://www.kaggle.com/pes12017000148/food-ingredients-and-recipe-dataset-with-images

### About: Food Ingredients and Recipe Dataset with Image Name Mapping, contains 5 columns, as follows:
•	Title: Represents the Title of the Food Dish.

•	Ingredients: Contains the ingredients as they were scraped from the website.

•	Instructions: Has the recipe instructions to be followed to recreate the dish.

•	Image_Name: Has the name of the image as stored in the Food Images zipped folder.

•	Cleaned_Ingredients: Contains the ingredients after being processed and cleaned.

The Food Images zipped folder contains all the images corresponding to the rows in the CSV file, named according to the Image_Name column.

This dataset was created by scraping from the Epicurious Website.

### API for Recipe Data Retrieval:

Link to API: https://rapidapi.com/edamam/api/recipe-search-and-diet/details
•	Recipe Search and Diet

•	Search over 1.5 million recipes

•	The Edamam Recipe Search and Diet API lets you integrate recipes and faceted recipe search into your websites or mobile applications.

•	Free subscription of API, lets you search 5000 query in a month.

## System Architecture:

 
![alt text](https://github.com/kishanpatel-hub/Food-Search-Engine/blob/main/Project/static/Capture.JPG)

### Indexing with Solr:

Static datasets mentioned below containing more than 13K recipe is used to create cache index of popular dishes. Each dish is considered as single document and it’s ingredients are indexed accordingly. Given data was in the CSV format which is one of the acceptable format for Solr. Solr is used to create collection named fooddishes where indexed data is stored. Solr collection configuration details are as follows.

Collection Name: fooddishes

Number of shards: 2

Number of Replicas: 2

Configuration: fooddish_configs

Schema: Custom Schema

Fooddish_configs is a custom configuration file created for this project which supports custom spell checker and suggestion search components and respective request handlers which are configured to support some of the features provided by system such as spell check and recommendation for ingredients. 

### 1.	Search Component – spell check

This search component was created to support spell checking of ingredients. Class of this spell check was set to DirectSolrSpellChecker which uses terms from the solr index without the need to build parallel index. It also benefits from not having to rebuild index everytime the main index is updated. Following is the configuration of this spell check.

Field: field was set to ingredients since we need suggestions for ingredients.

maxEdits: maxedits were configured to 2 which allows search component to search for teams which can be achieved by changing two letters in user query.

minPrefix: min prefix was set to 1 which means that user query needs to have one common letter with terms in order to be suggested.

minQueryLength: it defines how many characters must be in the query before suggestions are provided. It is set to 1 to configure suggestive feature along with spell check. 

All the other parameters were set to default. 

### 2.	RequestHandler 

Corresponding request handler called spell was created to support above defined search component while querying. Suggestion count was set to 8 to get most relevant 8 suggestions for any query. 

Although Solr offers field guessing feature which basically guess field type based on data and sets up schema accordingly automatically without any configuration required from user end. But this field guessing features has limitation and sometimes results in miss identification of fields. To avoid such scenario, following standard practice of solr custom schema was created based on the data. 

### Indexed Fields:

1.	Dish Title

2.	Dish Ingredients

### Non-Indexed stored Fields:

1.	Dish Recipe Instructions

2.	Dish Image info

Copy Field was created from title and ingredients which is used for the query where specific field to search is not specified. 

Standard Solr posting feature was used to index the dataset directly from the CSV file after doing some of the pre-processing of CSV file where unwanted fields were removed, and CSV was restructured for seamless indexing. 

## Search and Ranking:

After indexing 13K recipes, Solr search API is used to query results using select and spell request handlers. Select request handler is used to final query submission and appropriate food dishes are returned as a result. On the other hand, spell request handler is used to give suggestions for query being entered by user in real time.

### Search query using Python:

In user interface, user can enter ingredients they want to have and ingredients they do not want to have in two separate inputs and search shows dishes that fits the given input by creating custom search query based on input which is performed on ingredients field since we need dishes with specific criteria for ingredients. 

Example Query: Ingredients:(bread+-eggs+)

Search query uses binary operators supported by solr to create custom query in python. This custom query is sent to Solr jetty server in form of request and server response with relevant results in json format. Which are then processed in python to extract document information of relevant documents. Result limit is initially set to 10 most relevant document but since their could be many dishes fitting the same criteria, option to fetch more document based on the same query is also provided. 

CORS supported was added to solr server configuration files to support request from cross origin platform.
 
### Spell check and suggestion using javascript:

Spell check and Suggestion engine for ingredients displays ingredients as user enters query based on the indexed data which improves user experience by not having to type all the ingredients. This is supported by Solr Javascript API and spell search component discussed earlier. 

Recipes are ranked using Vector space Model and Boolean model used in combination by lucene scoring function. the simple idea behind the VSM is the more times a query term appears in a document relative to the number of times the term appears in all the documents in the collection, the more relevant that document is to the query. It uses the Boolean model to first narrow down the documents that need to be scored based on the use of Boolean logic in the Query specification. 

Advanced features such as auto spell check has been implemented as proposed. 

## User Interface using Flask 

Flask micro web framework is used to create simple user interface. This UI mainly consist of 2 pages. First is the landing page where user is prompt to enter two-fold query. Where in one text field user can enter ingredients, they want to have and the ones they don’t have to have are entered in the second text field.  User Interface gives suggestions and offer spell checking while user is entering query. Search button is provided which redirects to results page. 
 
 
![alt text](https://github.com/kishanpatel-hub/Food-Search-Engine/blob/main/Project/static/Picture1.png)

![alt text](https://github.com/kishanpatel-hub/Food-Search-Engine/blob/main/Project/static/Picture2.png)

 
Suggestions can be seen in the image above. 


![alt text](https://github.com/kishanpatel-hub/Food-Search-Engine/blob/main/Project/static/Picture3.png)

Selected entries can be seen in the above image.

Result page includes query details like query text and number of recipes available which fits the criteria along with the actual result which consist of image of the recipe, name of the recipe along with ingredient which could be used to verify search criteria and instructions of make the recipe is also provided. 

![alt text](https://github.com/kishanpatel-hub/Food-Search-Engine/blob/main/Project/static/Picture4.png) 

## Conclusion

This prototype search engine is a demonstration of how food search options can be improved to support for customer requirements. Prototype works perfectly for the limited dataset which can be scale in real time system. The development of this project gave me clear picture and knowledge of how solr can be used to offer vast set of features and internal workings of solr. I spend quite a lot of time, making different APIs work in python and JavaScript which was great learning experience.  
