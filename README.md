# reportstar

## Description

TODO

# License

reportstar is released under the GPLv3, a copy of the license should have been 
included with the project in the root folder in a file named COPYING. If you 
require a more commercial friendly license, please contact me at 
<furious.luke@gmail.com>.

# Dependencies

TODO

# Installation

After downloading and upacking the archive, `cd` into the project
directory and run the file `setup_environ.py`. This will prepare a
virtual environment and download all the necessary packages to
run a server. The default environment is a deveopment environment.

Source the newly installed environment with `source environ/bin/activate`.

Next, `cd` into the site root with `cd reportstar`. Now you need to
prepare your database with `./manage.py migrate`.

Optional: Load a fixture.

Now you can run a test server with `./manage.py runserver`.
