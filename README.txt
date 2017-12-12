Description:
   A web application that lists items within various categories, using a Google OAuth2.0 login system. Registered users can add, edit and delete their own items, they can't delete other users' items.
   The app also has a JSON endpoint to export all categories with their items in the JSON format.

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
   11. Visit "http://localhost:8000/catalog.json" to access the JSON endpoint.
   
Credits:
   Part of this application's code uses components from Udacity's Nanodegree course in Full Stack Web Developement.
   Project:https://github.com/udacity/ud330
   License to Educational Content(https://www.udacity.com/legal/terms-of-service):

"Udacity hereby grants you a license in and to the Educational Content under the following terms and subject to the following conditions:of the Creative Commons Attribution-NonCommercial- NoDerivs 3.0 License (http://creativecommons.org/licenses/by-nc-nd/4.0 and successor locations for such license) (the "CC License"), provided that, in each case, the Educational Content is specifically marked as being subject to the CC License. As used herein, "Educational Content" means the educational materials made available to you through the Online Courses, including such on-line lectures, speeches, video lessons, quizzes, presentation materials, homework assignments, programming assignments, code samples, and other educational materials and tools. Such Educational Content will be considered the "Licensed Material" under the terms of the CC License. Without limiting the generality of the terms of the CC License, the following are types of uses that Udacity expressly defines as falling outside of the definition of "non-commercial":

(a) the sale or rental of (i) any part of the Educational Content, ((ii) any derivative works based at least in part on the Educational (Content, or (iii) any collective work that includes any part of the (Educational Content;

(b) the sale of access or a link to any part of the Educational (Content without first obtaining informed consent from the buyer (that the buyer is aware that the Educational Content, or such part (thereof, is available at the Website free of charge;

(c) providing training, support, or editorial services that use or (reference the Educational Content in exchange for a fee;

(d) the sale of advertisements, sponsorships, or promotions placed (on the Educational Content, or any part thereof, or the sale of (advertisements, sponsorships, or promotions on any website or blog (containing any part of the Educational Material, including without (limitation any "pop-up advertisements";

(e) the use of Educational Content by a college, university, school, or other educational institution for instruction where tuition is charged; and

(f) the use of Educational Content by a for-profit corporation or non-profit entity for internal professional development or training."
