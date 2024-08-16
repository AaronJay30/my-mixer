# Mixer

#### Video Demo: https://www.youtube.com/watch?v=N7rn-byrN_Y

###Description: A social network website purely based on Flask. A twitter liked website where you and your friends can create an account for the website and you can post your thoughts without restriction. You can also like the post of others or comment to their post.
###

**Note**: I started learning Flask on CS50 course and I decided for my Final Project to build a Twitter Clone which you can post, comment and react. At first my ideas is to create a website that will help you decide what movie you will watched. But after a day I reject that idea and start working with a social network, 
		  because I think I can do better than my old idea and challenge myself. It took me 3 days to finish this project but it's worth it because it taught me a lot of information i dont know before
		  
**Motivational Quotes**: `"I’ve failed over and over and over again in my life and that is why I succeed."- *Michael Jackson*`


**Languages & Database Used**:
  1. Python(The God)
  2. Flask(The Servant)
  3. Html - CSS (Interior Designer) (ik people do not consider it as a language but yeah)
  4. Sqlite (The library to store info)
  
**Route**:
- account: This is where you can view your personal information and you can change your name or password by pressing a button
- comment: This is where you can give your feedback or suggestion to the post
- edit: This route is simply where you can edit your the text in your post
- edit_account_name: with the account route earlier when you press the change name you will have the access to change your name
- edit_account_password: with the account route earlier when you press the change password you will have the access to change your password
- following: This part is like the index but instead of seeing all the post from every user this section lets you see all the post of the people you follow
- friends_profile: This will let you visit the profile of others and see their post, following, followers.
- index: This is the main page of the web app, this is where you can see the post of everyone and discover someone.
- layout: This is the layout I use and just put some jinja so I can lessen the work
- login: This is where you login your account.
- mix: This is where you can post your thoughts.
- profile: This is your own profile where you can delete or edit your post.
- register: This is the part where you will create your account so you can access the index route
- search: You can search a user name in the search bar and it will prompt you the user that you search
- userfollower: This will display all the user that is following you
- userfollower: This will display all the user that you follow

**Features**:
  1. User-Login and Registration 
  2. Friends (Following and Unfollowing)
  3. User Search
  4. Edit or Delete a post
  5. Changing password and name
  6. Commenting and liking post
  7. You can see your followers and who you follow
  8. And some small features that you'll see for sure while using
  
**Future Plans**:
  1. Making the UI more comfy,stable and also suitable for mobile devices(currently only desktop users can properly access it)
  2. Email Verification(Function is present in the code just gotta impliment it properly)
  3. User Chats
  4. Some API implimentation to get user data in json format for debugging or testing
  5. Implimenting Ajax(so my pages wont load again and again on specific actions like <b>likes and comments</b>

**Special Mention** 
### I would like to thank `**Mr. David Malan**` for the free course which helps me understand programming and to Brian Yu and Doug Lloyd that discuss the shorts and problem set so that we can understand the topic. Also to the staff of CS50 without them this will never happen
### To my classmate thank you for sharing your information in Discord and Facebook it really helps me especially when I'm having hard time in the error. 