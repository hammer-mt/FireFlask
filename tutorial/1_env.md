### 1: Create folder set up environment
First open VSCode and get to the projects folder on your computer, then create a folder for your new project.

`cd Documents\Projects`

`mkdir FireFlask`

`cd FireFlask`

Let's create a virtual environment with this command.

`python -m venv venv`

Now you can activate it with this command.

`venv\Scripts\activate`

If you want to deactive it, just type this.

`deactivate`

Now you want to install Flask.

`pip install flask`

Now let's initialize git

`git init`

You also want to add a .gitignore file.

Make sure the encoding to UTF-8 or git can't read it.

Copy and paste a template across, like this one:

[Python.gitignore](https://github.com/github/gitignore/blob/master/Python.gitignore)

You want to save your commitments and a readme.

`echo "# FireFlask" > readme.md`

`pip freeze > requirements.txt`

Now do your first commit.

`git status`

`git add .`

`git commit -m "set up folder, requirements, gitignore, added readme"`

Next step is to connect to github. Log in and create a new repository.

Give it a unique name and brief description, and add the MIT license if making it public.

Now click 'Clone or download' and copy the SSH key.

`git remote add origin git@github.com:mjt145/FireFlask.git`

`git remote -v`

`git push --set-upstream origin master`

If git push not working, you need to pull the license changes first

`git pull origin master --allow-unrelated-histories`

This lets you ignore the problem with different histories.


