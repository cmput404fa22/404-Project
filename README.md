# 404-Project - Social Distribution Application

## appname
*appname* is a socializing app for authors to create blog posts, keep up to date with their friends, and discover other authors! 
Starting at the beginning, you can [signup](https://cmsjmnet.herokuapp.com/signup/) for an account and wait for approval from an admin. Once you are approved, you can easily create a new post in the following formats: plain text, commonmark, or image. You can then decide to share privately with just a few friends or have it shared publically with all your followers. You can also make this post unlisted if you wish. 
* The [strean](https://cmsjmnet.herokuapp.com/stream/) page is where and posts shared with you will appear. This is also where you can discover other authors on the app. To follow another author, simply choose them from the list to view their public profile and click follow. Here you can also see any of their public posts and their github activity.
* The [your posts](https://cmsjmnet.herokuapp.com/authorposts/) page is where you can view all of your posts, including the unlisted posts. Here you can edit or delete posts, or view a post on it's own by clicking on the title of it. 
* The [notifications](https://cmsjmnet.herokuapp.com/notifications/) page is where you are updated on the activity of your account. Follow requests from other authors will appear here, along with notice that posts have been shared with you.
* The [profile](https://cmsjmnet.herokuapp.com/profile/) page is private to you and is where you can view or edit your profile information, including a profile image or github url.

### For marking
Some of our authors are willing to showcase their accounts for you to observe and use as you see fit. Below are their login information. 
* user: jesse --- pass: jesse
* user: mark --- pass: mark
* user: michael --- pass: michael
* user: sim --- pass: sim
* user: cameron --- pass: cameron
Our admins will be away on holidays after 5:00pm on December 9th, so if you wish to join *appname* and sign up a new account, make sure to register your new user [here](https://cmsjmnet.herokuapp.com/admin) with the super secret admin login: *user: admin --- pass: admin*

### Changes we've recently made
If you're a long time *appname* user, you may know that we've made some changes to our application since our latest release on December 5th 2022. Below are some details about or new features and updates.
* Commenting on posts
* Only one content type for a post - image posts are now standalone
* Github activity stream in public profile

### Remote Connections

For other teams:

- Register at https://cmsjmnet.herokuapp.com/signup-node, fill out the form to register your node
- ping our team to finish registering your node
- access API using basic auth with your username and password
- API schema can be found here: https://cmsjmnet.herokuapp.com/authors/swagger/

For admins:

- Go to /admin dashboard -> authors
- Select authors with username (hostname) of the remote node
- go to action drop down and select 'Register selected nodes'
