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
This application holds/contains the logic for **authapp**. This app handles authentication, authorizations to the server  

### 🍡 Models
This a list of the models in the authapp applications with their fields with a small description.

   - #### 🎊 User
   
   Handles all registrations, authentication, login and authorization within the serer
   
   Field | Description
   --- | ---
   email | Defines the email for the user
   username | Defines the username for the user
   password | Defines the password for the user
   phone_number | Defines a user phone number
   updates | Defines if the user wants to receive any updates from our services
   user_type | Defines the type of user since the models handles different type of users eg. Admin, User
   terms | Defines if the user has confirmed to that they accept our terms and conditions
   is_active | Defines if the user is active or deactivate
   is_staff | Defines if the user is a staff member or not
   last_login | Defines when the user last logged in to their dashboard
   
   - ### 🧨 Avatar
   
   Defines the field of an avatar file for a user
    
   Field | Description
   --- | ---
   user | Defines the client who created this avatar
   avatar | The avatar file 
   
   - ### 🛍 Defaults
   
   Defines user default variables
   
   Field | Description
   --- | ---
   user | Defines the user
   writer | Defines the writer a user has set a their default 
   academic | Defines the academic level of the user/client
   native | Defines if a client wants to always have native writers work on all the paper the order
   topic | Defines a favourite topic the user will be likely to always place their order with
   format | Defines a favourite format the user will be likely to always place their order with
   
   - ### 👔 Writer
   Field | Description
   --- | ---
   first_name | Defines the first name of the writer
   last_name | Defines the last name of the writer
   username | Defines the username of the writer
   email | Defines the email of the writer
   is_active | Defines if the writer is active ord deactivated
   level | Defines the  experience of the writer
   

## 🍟 URLs

Urls defined in order application
 
Endpoint | Descriptions
--- | ---
/register | POST -> Allows potential client to register to the server 
/login | POST -> Allows user/clients to login to the server
/logout | POST -> Allows user/clients to logout user out of the server
/logoutall | POST -> Allows an admin to logout all users on the platform
/user | GET -> Allows frontend to retrieve logged in user information
/users/password/reset/<str:username> | PUT PATCH -> Allows user to change their password
/users/delete/<str:username> | DELETE -> Allows user to delete their account 
/forgot/password/reset | POST -> Allows user to reset their password through email if they forgot 
 
## 🛴 Choices

This file contain enumerations choice for the models

CURRENTLY EMPTY

## 🍟 Serializers

This file contains serializer only which are used to serialize the models defined in the models.py

- AuthUserSerializer - serializer for USER Models used for authentication 
- UserSerializer - serializer for USER Models user to retrieve users data
- AuthRegisterSerializer - serializer for USER Models user to register a user to the server
- AuthUserResetPasswordSerializer - serializer for USER Models user to reset a password

## 🎞 Views

This file contain or class based views that takes a Web request and returns a Web response. This response can be an error or data in json format
 
View | HTTP Method | Function
--- | --- | ---
RegisterAPI | POST | Register a new user to the server
LoginAPI | POST | Login a user to the server
AuthUserAPIView | GET | Retrieve Logged in user information
UserApiView | GET | Get all users of type user
UserUpdatePasswordApiView | PUT PATCH | update logged in user password
UserDeleteApiView | DELETE | Delete a user from the server
robots | GET | Returns robots.txt file
