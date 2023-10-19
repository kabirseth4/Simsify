# Simsify README
#### by kabirseth4

## About
This web app is a habit tracker based on the Needs mechanic used in The Sims game franchise by EA:

![Sims 4 Needs mechanic example](https://github.com/me50/kabirseth4/assets/37245872/adc0b996-90a8-4858-a99d-5b6fb84447e9)

The idea is to have a set of *Needs*, that will decrease or increase over time, which represent habits you would like to maintain or avoid respectively. Then you can then set up repeatable *Actions* that will change the level of a specific *Need* by fixed amounts. For example, if your *Need* was Exercise, you could create multiple *Actions* for different workouts that would increase your Exercise level by different amounts.

The *Needs* are presented to you on the homepage with colour-changing level bars, as is done in game. This gives you a simple overview of which habits you are neglecting.

## Running and Using the Application

Nothing special is required to run the application. Once you have downloaded the code, simply run `python manage.py runserver` and access the given URL in your browser. From here, you'll be prompted to register, and then you can start creating *Needs* and *Actions*.

To create a *Need*, click the **Add need** button in the nav-bar. Here you will be propted for a name and a decay time, which is how long the *Need* will take to fully deplete or recover. You will also be asked whether the *Need* should have the default behaviour and decrease over time (Normal), or represent a bad habit and increase over time (Negative).

Once you have created your *Needs*, you can move on to creating *Actions*. Click the **Add action** button in the nav-bar and choose a name, which *Need* this *Action* will affect, and how much it will increase (Normal) or decrease (Negative) the related *Need*.

To enact an *Action*, click the **Act** dropdown in the nav-bar. You will be shown a list of *Needs* which you can hover over to see the related *Actions* and how much they will impact the *Need*. Click on your desired *Action* and the related *Need* level will be updated.

That's it! You can now view all of your *Needs* and their levels and create and enact *Actions* to prevent any of them getting too low.
