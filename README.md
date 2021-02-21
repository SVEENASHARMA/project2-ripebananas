## Welcome to RIPE BANANAS

![bb1](https://user-images.githubusercontent.com/71414243/107602050-6bd24000-6bf6-11eb-9485-caf55b6e0d92.jpg)
https://Ripe-Bananas-6.herokuapp.com/

## Project Goal

A video streaming service is an on demand online entertainment source for movies, TV shows and other streaming media. These services provide an alternative to cable and satellite on demand service, often at a lower cost. Our goal is to have a simple, user friendly experience to finding a TV show or movie all in one application. The use of streaming services often requires fees and subscriptions to watch. Some services feature numerous devices such as smart TVs, tablets, computers, streaming media receivers and smartphones. There are other services that are ad-supported, or run on a freemium model and also offer some full feature movies at a cost. Also, there are other services that may be more limited in the type of devices, or tailored to a specific device, much like iTunes for Apple devices. There are so many services out there that it can get very overwhelming when looking for a movie or tv show and where to watch it. Our inspiration for the project is having all the information readily availabile about what and where the media can be streamed and you can get some user comparison data as well. Having all this information in one area will make it a lot easier to find what you looking for in a jiffy.

We have created a web application called "RIPE BANANAS" on the different streaming services available. You can browse through various TV shows and movies available online through this application and with one click you will be able to easyily go on that site and watch your desirable media content. You can search by title of the movie or TV show. It will also give u similar movie reccomendations you can pick from. The app was created for a quick and better user experience. 

## Question for our project:

Is there an application where we can find extensive comparison data on different streaming services and what they have to offer?

Answer: 

RIPEBANANAS! 
![loho-v-y](https://user-images.githubusercontent.com/71414243/107602159-a63bdd00-6bf6-11eb-9066-48a76d7bc833.png)


# Process: 

![image](https://user-images.githubusercontent.com/71414243/107602176-b5228f80-6bf6-11eb-9d98-398f02feefce.png)

# Extraction of the Data

Our data is sourced from Reelgood.com, various streaming service websites and we got user review analysis extracted from Nielsen Insights and derived 10,000 synthetic data using the analysis provided to analyze various components surround streaming services and their users based on, gender, age, genre, titles of media and much more. 

To transform the data we scraped, we cleaned and transformed it by using Python Jupyter Notebook and made various comparison visualizations using pandas. 

## Visualizations  
<img width="1318" alt="Screen Shot 2021-02-12 at 7 44 13 PM" src="https://user-images.githubusercontent.com/71414243/107836339-c5f41200-6d6a-11eb-8462-09388e909bec.png">

<img width="1372" alt="Screen Shot 2021-02-12 at 10 22 29 PM" src="https://user-images.githubusercontent.com/71414243/107840538-871d8680-6d81-11eb-8de9-1dbbe145f036.png">

<img width="1373" alt="Screen Shot 2021-02-12 at 10 22 39 PM" src="https://user-images.githubusercontent.com/71414243/107840545-913f8500-6d81-11eb-945d-7a8ec2014fbb.png">

We used Leaflet and GEO mapping on JavaScript 

<img width="854" alt="Screen Shot 2021-02-10 at 10 50 04 PM" src="https://user-images.githubusercontent.com/71414243/107602345-28c49c80-6bf7-11eb-9b51-d6020162a9d5.png">

<img width="854" alt="Screen Shot 2021-02-10 at 10 50 18 PM" src="https://user-images.githubusercontent.com/71414243/107602359-367a2200-6bf7-11eb-8115-e1d291679437.png">

### Load 

For this project to efficiently work we used Python Jupyter Notebook to load the clean transformed data in to MongoDB & MySQL database. 
Python Flask powered a restful API were used to deploy the data into the web, and using API end point links were created. API links store our cleaned and transformed data in a json format and are publicly accessible for visitors of our website.

## Deployment 

The app is deployed in Heroku in order to access the page click the following link 

https://Ripe-Bananas-6.herokuapp.com/

## The Ripe Bananas Team Members
* Desiree Herschnberger (Des)
* Redeat Bekele
* Sveena Sharma
* Taslemun Nahar (Tas)
* Thomas Keane (Tom)
* William Pappas (Billy)
