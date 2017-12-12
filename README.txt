Description:
   A web application that lists items within various categories, using a Google OAuth2.0 login system. Registered users can add, edit and delete their own items, they can't delete other users' items.

How to run it:
   1.Install virtualbox and vagrant first.
   2.cd into the folder named vagrant.
   3.Run "vagrant up" and "vagrant ssh" to log into the virtual environment.
   4.Run "python /vagrant/catalog/application.py" to bring up the web application.
   5.Visit "http://localhost:8000" in the browser.
   6.Use your Google account to log into the website.
   7.Add new items from the "Add Item" option on the home page.
   8.Click each item to see its description.
   9.Edit and delete your own items in each item's description page.
   10.In case you want to initialize the database again, delete catalog.db, and run "database_setup.py", then run "add_items.py" in their own folder.
