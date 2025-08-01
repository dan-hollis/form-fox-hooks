This is a simple Flask app for handling [Form Fox](https://github.com/dan-hollis/form-fox) hooks on my World of Warcraft guild's Discord server.

Currently handles the following:

* When a form is accepted and the user is a guild member (has `Guild Member` role):

    * Assigns them the `Raider` role

* When a form is accepted and the user is not a guild member:

    * Assigns them the `PUG Raider` role
    * Adds their username to a Google Doc to track PUG Raiders