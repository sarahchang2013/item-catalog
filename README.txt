Description:
   A web application that lists items within various categories, using a Google OAuth2.0 login system. Registered users can add, edit and delete their own items, they can't delete other users' items.

How to run it:
   1.Install virtualbox and vagrant first.
   2.Run "vagrant up" and "vagrant ssh" to log into the virtual environment.
   3.Run "python /vagrant/catalog/application.py" to bring up the web application.
   4.Visit "http://localhost:8000" in the browser.
   5.Use your Google account to log into the website.
   6.Add new items from the "Add Item" option on the home page.
   7.Click each item to see its description.
   8.Edit and delete your own items in each item's description page.
