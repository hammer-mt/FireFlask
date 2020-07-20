# Creating a new Flask app
I'm going to make a starter Flask app with user login based on a GCP Firebase backend complete with a NoSQL database, testing suite, blueprints, Google Cloud functions, version control, virtual environments, React and generation of static assets. I'll use this for all new projects going forward. In the future I'll add stripe payments, teams and other important admin functionality.

In this notes section I'll document everything I did to create this project step by step, so I can keep coming back to it and improving it. It'll act as a changelog but also a tutorial if I ever need to spin one up slightly differently.

This project came about because I found Django a little confusing, always ran into problems with developing using SQL databases (configuring and devops) and thought if I can just use a lightweight flask application with a firebase backend I'll be in a good position. 

I also think there's an unmet need for a kind of '[rails for saas](https://www.indiehackers.com/post/ror-saas-boilerplate-app-market-need-fb7af3d8db)' type boilerplate code, something that implements 90% of the same features every saas application needs. 

## Tutorials I used for inspiration / unmerciful copypasting
- [The Flask Mega Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- [Flask Tutorial](https://flask.palletsprojects.com/en/1.1.x/tutorial/)
- [Flask and Firebase and Pyrebase Oh My](https://blog.upperlinecode.com/flask-and-firebase-and-pyrebase-oh-my-f30548d68ea9)
- [Heating up with firebase tutorial on how to integrate firebase into your app](https://blog.devcolor.org/heating-up-with-firebase-tutorial-on-how-to-integrate-firebase-into-your-app-6ce97440175d)
- [Materialize CSS the Net Ninja](https://www.youtube.com/watch?v=gCZ3y6mQpW0)

## Step by step instructions for recreating
This is where I'll record as I go exactly what I did to create this project. It can serve as a kind of tutorial. I will assume at this point you have Python3 and VSCode installed on your computer and you're using windows, and are ssh'd into github.

I've been writing these notes as I go along, sometimes very late at night, so there are definitely mistakes or areas I missed. If you notice please let me know and I'll fix!