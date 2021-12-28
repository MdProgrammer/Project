#NOTTER
####Video Demo: <https://youtu.be/z2UcqvFPlyQ>
####Description:
    NOTTER is a note taking Responsive web app that allows you to take notes that will saved in your account, after creating notes you can edit them delete them,
    or even invite friends to your note which they can also edit and intrect with, the site is designed in a responsive way that makes the design looks good for both computres and mobiles.

####the user experience:
    when you first enter the site you are asked to login but you can acces the register page from the navbar or by clicking the "sign up" button after registering and signing up you get redirected
    to the main page where you can view, creat and edit your notes, assuming you clicked the add note link in the navbar you then can creat your note wich contains a title, the note,
    and optionally add the id's of the people you want to share this note with, after you creat the note by clicking the "add note" button you get redirected to the main page and your note get displayed
    as note card if your note is longer then the note card you can drag your mouse into the card and scroll and that wil allow you to see the note, you also edit your note by clicikng the "View and Edit note"
    button when clicking that button you will be redirected to the edit note page where you can edit your note's title, content and the peopke that you have invited, after editing it you save the edited version
    of the note by clicking the "edit note" button and your note gets edited and you get redirected to the main page, in the main page you can also delter your note by hovering over the three dots that
    will be positioned on the top right of your note card when clicking it your note will get deleted.

#####application.py:
     is the main file where all the GET and POST requests are handeled, the code that makes the web app run based on certain lines of code that makes certain dissisions based on the user input is also implemented in there

#####notter.db:
     the database where the user info and notes get stored.

#####style.css:
     is the main Cascading Style Sheet that almost every elment in the pages takes style from.

#####holder.css:
     is a helping Style Sheet that edit a few elments style.

#####layout.html:
     is the HTML code that get shared trought multiple HTML files.

#####register.html:
     is the registering page from there you can creat an account it can be accesble trough the nav bar or the login page.

#####login.html:
     is the page where you can login if you already have an account it can be accesble trough the nav bar or the reigster page.

#####index.html:
     is the page where or your notes are displayed as note cards, you can view long notes trough scrolling in the card from there you can delete them or access the add note and edit page.

#####edit.html:
     is the page that you can edit your notes from, you can also invite your friends by writing they're id, it can be accesble trough clicking the "View and Edit" button in the main page.

#####add_note.html:
     is the page tha you can creat your notes from, you can also invite your friends by writing they're id, it can be accesble trough clicking the "Add note" button in the navbar.

#####error.html:
     is the page that renders when an error happens.
