### 14: Refactoring the codebase

We have a lot of mismatched code and repetition that we can improve. We also have security loopholes that we want to fix.

Now we can run our test suite and be confident we don't break anything, we can refactor the code and improve security, move towards a more streamlined session management (drop either firebase_admin or pyrebase) and improve the speed and maintainability of the app.