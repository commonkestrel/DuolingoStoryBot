# DuolingoStoryBot

This bot uses Duolingo Stories to generate xp automatically. 
When first used, the bot will prompt you for a username and password. **This does not work with Google accounts.**
There is a work around to the *Google* account problem, which is to use the forgot password function when logging in, and changing your password.
This will update your account login to work with *Google* **and** regular login.

After inputting login, it will ask the prompt "Run in background? (y/n): " This asking wether you want the bot to run in the background or be able to see the window. Answer "y" if you would like it to run in the background, and "n" if you would like to see the window.

After this it will prompt you for the amount of xp to terminate after. This is useful for limiting how much it will earn in a time automatically. Note that it will stop **after** it reaches this goal, which means if you input 120, it may not stop until 128, for example. Enter 0 if you do not need a limit.

It will then login and go through every story that is not worth 0 xp, and complete them, earning you xp.
