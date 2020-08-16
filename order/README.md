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

## 🎭 Order Application
This application holds/contains the logic for **orders**.An Order is a paper that our client will create. We receive the order an if order is ok and paid for we work on the the paper.  

### 🍡 Models
This a list of the models in the orders applications with their fields with a small description.

   - #### Order
   Field | Description
   --- | ---
   User |  Defines The user who placed the paper/order
   paper_type | Defines the type of paper of the paper/order
   discipline | Defines the discipline of the paper/order
   academic | Defines the academic level of the user who placed the paper/order
   title | Defines the title of the paper/order
   instructions | Defines the instructions of the paper/order
   additional_materials | Defines the additional_materials of the paper/order ie files uploaded by client
   format | Defines the format of the paper eg APA6, MLA
   spacing | Defines the spacing of the order eg DOUBLE or SINGLE
   preference | Defines the writer preference chosen by user
   deadline | Defines the deadline of the paper/order 
   pages | Defines the number of pages of the paper/order 
   sources | Defines the number of sources of the paper/order 
   charts | Defines the number of charts of the paper/order 
   powerpoint | Defines the number of powerpoint of the paper/order 
   native | Defines if the client wants the order to be done by a native writer 
   progressive | Defines if the client wants the order to be progressively delivered 
   status | Defines the status of the order eg canceled, Active 
   payments_url | Defines the payments url where the user paid the order  
   cost | Defines the cost of the paper/order eg 100  
   smart | Defines if the order is a smart paper or not
   paid | Defines if the order is paid
   is_paper | Defines if an order is deleted
   confirmed | Defines if an order is confirmed
   dispute | Defines if an order was ever on dispute
   revision | Defines if an order was ever on revision
   
   - ### 🤳 Notification
   Field | Description
   --- | ---
   user | Defines the client who will receive the notifications also the owner ot the order been sent
   content | Defines what to communicate to the user
   created | Defines the admin or master admin who writes the notification
   notify | Defines what is type of notification being sent
   read | Defines if the notification is read/unread
   
   - ### 🎃 Files
   Field | Description
   --- | ---
   description | Defines what the user/client describe the file eg instructions
   file | The file uploaded
   is_deleted | Defines if a files is deleted or not 
   
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
 
Endpoint | HTTP Methods | Descriptions
--- | --- | ---
/ | GET | Allows user/clients to retrieve details/information of a all orders specific to them 
/create | POST | Allows user/clients to create an order
/details/<uuid:uuid> | GET | Allows user/clients to retrieve details/information of a single specific order
/delete/<uuid:uuid> | DELETE | Allows user/clients to delete an order
 
## 🛴 Choices

This file contain enumerations choice for the models

   - ### 🍲 StatusChoices
    - DRAFT
    - REVISION
    - ACTIVE
    - CANCELED
    - DISPUTE
    - FINISHED
   
   - ### 🍭 SpacingChoices
    - SINGLE
    - DOUBLE
   
   - ### 🥞 FormatChoices
    - MLA
    - APA6   
    - APA7
    - CHICAGO/TURABIAN   
   
   - ### 📞 NotificationChoices
    - UPDATE
    - NOTIFICATIONS
    
   - ### 🍖 EducationLevelChoices
    - HIGHSCHOOL
    - PHD
    - GRADUATE
    - UNDEGRADUATE_1_2 (Undergraduate (yrs. 1-2))   
    - UNDEGRADUATE_3-4 (Undergraduate (yrs. 3-4))
   
   - ### 📃 PreferencesChoices
    - STANDARD
    - TOP5
    - EXPERT
     
## 🍟 Serializers

This file contains serializer only which are used to serialize the models defined in the models.py

- OrderSerializer - serializer for Order Models
- OrderFilesSerializer - serializer for Files Models
- NotificationSerializer - serializer for Notifications Models

## 🎞 Views

This file contain or class based views that takes a Web request and returns a Web response. This response can be an error or data in json format
 
View | HTTP Method | Function
--- | --- | ---
OrderApiView | POST | Create an order for the client
UsersSpecificOrders | GET | Retrieve orders created by user
GetOrdersApiView | GET | Retrieve an order created by user
OrderUpdateApiView | PUT PATCH | Update an order details/files
OrderDeleteApiView | DELETE | Delete an order
SingleTOAdminsOrderApiView | GET | Retrieve an order for the admin
OrderFilesApiView | POST | Create a file for an order
OrderFilesDeleteApiView | DELETE | Delete a file from an order
