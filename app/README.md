<p align="center">
    <img src="https://github.com/IAmGitau/freelancer-backend/blob/master/templates/img/Kromon.png">
    <br>
    <br>
    <img height="20px" src="https://api.netlify.com/api/v1/badges/88afbb86-1657-4de0-b211-79371fd3004a/deploy-status">
    <img height="20px" src="https://github.com/IAmGitau/freelancer-backend/workflows/Unit%20Tests/badge.svg">
    <img height="20px" src="https://github.com/IAmGitau/freelancer-backend/workflows/Linting/badge.svg">
</p>
<p align="center">
Kromon is a growing 🚀 custom paper writing company. Ready to work for customer all over the world. We mainly focus on writing for english speaking countries or students.
</p>

## 🎭 Authapp Application
This application holds/contains the logic for **app**. This app handles anything used globally, individually or some login not enough to be considered as an app.

### 🍡 Models
This a list of the models in the app applications with their fields with a small description.


   - #### 🪀 Discipline
   
   Handles all allowed disciplines
   
   Field | Description
   --- | ---
   name | unique name of the discipline
   description | a brief description of the description
   
   - ### 🍽 PaperType
   
   Handles all allowed paper types
    
   Field | Description
   --- | ---
   name | unique name of the paper type
   description | a brief description of the paper type 
   
   - ### 🍚 RATING
   
   Defines user default variables
   
   Field | Description
   --- | ---
   rate | number of what the client rates our services
   client | The client who rates us

## 🍟 URLs

Urls defined in order application

CURRENTLY EMPTY 

## 🛴 Choices

This file contain enumerations choice for the models

   - ### 🎍 AdminCategory
    - USER
    - ADMIN
    - MASTER 

## 🍟 Serializers

This file contains serializer only which are used to serialize the models defined in the models.py

- PaperTypeSerializer - serializer for paperType model 
- DisciplineSerializer - serializer for Discipline Model
- LoginUserSerializer - serializer for USER Model used to login a user in to the server

## 🎞 Views

This file contain or class based views that takes a Web request and returns a Web response. This response can be an error or data in json format
 
 CURRENTLY EMPTY
