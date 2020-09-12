### 14: Refactoring the codebase

We have a lot of mismatched code and repetition that we can improve. We also have security loopholes that we want to fix.

Now we can run our test suite and be confident we don't break anything, we can refactor the code and improve security, move towards a more streamlined session management (drop either firebase_admin or pyrebase) and improve the speed and maintainability of the app.

For this exercise I had a senior developer review the code for the user authentication model for FireFlask. For this code I hacked together a mix of pyrebase and firebase sdk, and basically ignoring the google firebase auth token, which we should improve on now it's working.

He spent a couple hours and review this code like I'd get if I was a junior engineer in a company, and gave me pointers on how I should be thinking about improving the way I do authentication. I provided a [data model diagram](https://docs.google.com/drawings/d/1iHwyDp2xvUah0UQ1L7LmMN61pT43rqso054p29lncz4/edit?usp=sharing), and access to the [github repository](https://github.com/mjt145/FireFlask) where he could find the [code for user auth](https://github.com/mjt145/FireFlask/blob/master/app/auth/models.py) and also this tutorial where I had [helpfully documented](https://github.com/mjt145/FireFlask/blob/master/tutorial/004_auth.md) what I'd done. 

From that feedback we'll review the code and implement changes, running our test suite using the red-green-refactor process to make sure we are confident we haven't broken anything with our changes.