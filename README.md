# SASSORA
#### Video Demo:  <https://youtu.be/j3VyMeYMwoQ>
#### Description:
I was initially confused as to what my final project for cs50 should be. After a few days of brainstorming , I finally decided to make a website for my father's company (which makes leather
products) through which users could log in with their id and order some products .
Essentially what the site does is : It first allows a user to either login with their existing username and password or it allows them to register for a new account asking them for their email aswell. Then it takes the user to the home page where I have displayed some of the information related to the company. I have also shown the pictures of the founder , CEO and Director of the company.
In the navigation there are two other pages - shop and cart. I have also added the logout feature in the site. When a user goes to the shop page, the site displays a number of prodoucts for the user to choose from along with their retail prices. The user is redirected to the cart on adding an item to the cart. The cart displays the products added by the user, the price of the product and it allows the user to increase/decrease the quantity of the product. Accordingly the subtotal and total in the cart get changed. Finally the user can check out using the button provided below.
This takes the user to the checkout page where they have to enter all the details such as payment information and address. Finally when the order is placed an email is sent to the user confirming that their order has been placed.
### static :
This folder contains the two css files : styles1 and styles. It also contains all the images used in the website such as the images of the products.
### templates  :
This folder contains all the html files used in the product :
> index.html
> apology.html
>cart.html
> checkout.html
> layout.html
> login.html
> register.html
> shop.html
> success.html

### application  :
This is the main python file where most of the sites's code is written. First I imported all the necessary packages into the file and then I configured the flask app with all the necessary requirements so that I could use the Flask-mail and flask-session feature.
It contains the code for all the routes such as : / , /register , /login , /shop , /cart, /register,/succcess, /logout, /edit .

#####  / :
I defined a function which simply renders the template : index.html and displays the homepage of the website.
#####  /register :
This route supports the methods GET and POST. When the method is POST , this page takes all the required information from the form and inserts it into the users table in final.db database . Before inserting into the database it checks whether any of the fields in the form are missing and it also checks if the username and email already exists in the database. If the method is GET , it renders the template : register.html.
#####  /login :
This route supports the methods GET and POST.If the method is GET , it renders the template : login.html. When the method is POST it takes the password and username from the form and checks it in the database. It alerts the user if any of the fields are empty or if the password is incorrect. If everything is correct then it lets the users into the website.
#####  /shop :
This route supports the methods GET and POST.If the method is GET , it renders the template : shop.html. When the method is POST it takes the product\_id from the form and accordingly updates the cart or inserts the product into the cart.
#####  /cart :
This route first calculates the total amount for the user using the site and then displays the cart containing the products selected by the current user.
#####  /checkout :
It renders the template : checkout.html .
#####  /success :
It sends the email to the user confirming that the order has been placed.
#####  /edit :
It supports the method POST. Depending on whether the user has chosen the "-" or "+" button ,
this route updates the cart table in the final.db database and decreases/increases the quantity and the subtotal for that product.



### final.db:
This is the database where I have stored the three tables that I have used : 1) users 2) products 3) cart.
##### users:
This table stores the username, user\_id , password hash and the email of the user.
##### products :
This tables stores the id, name, and price of the products displayed on the site.
##### cart :
This tables stores the product\_id, user\_id, product name, quantity , price , and the subtotal of each product.

### helpers :
This python file defines the functions - login\_required and apology which are both extensively used in the application.py file. The login\_required function makes sure that the user has to be logged in
to access any of the routes defined in application.py. The apology function returns a message to the user whenever something wrong happens in the website.
