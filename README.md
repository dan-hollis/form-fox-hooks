This is a simple Flask app for handling [Form Fox](https://github.com/dan-hollis/form-fox) hooks on my World of Warcraft guild's Discord server.

Currently handles the following:

* Assigns `Guild Member` role if user answers `Yes` to "Are you a guild member?" question

* Assigns a role depending on which submission accept type is given
  
  * `Accept - Prebis`

    * Assigns the `Prebis` role

  * `Accept - Trial Raider`

    * Assigns the `Trial Raider` role

  * `Accept - Raider`

    * Assigns the `Raider` role

  * `Accept - PUG Raider`

    * Assigns the `PUG Raider` role