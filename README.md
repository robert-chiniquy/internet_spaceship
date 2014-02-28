internet_spaceships
========
Fork this repository to make your very own internet spaceship. You'll want to
edit firmware.py with your own logic. When the firmware is run,
it will start reading in JSON data from the command line,
and saving all the information the server sends. Then it will call your
input() method in firmware.py. That's where you should use the data you've
been given to make intelligent decisions. When your function finishes,
it will print out the results to the command line, which will be sent back
to the server.

Check docs/input_example.json to see the kind of information you'll be given.
docs/output_example should represent about what will be printed after your
function is run and sent back to the server.

To get started:

    git clone YOUR_FORK_URL

    cd internet_spaceship

    python internet_spaceships/test.py

It will call your firmware.py and send it the data from test_files/input.json
. We advise you do this before uploading your ship. If your ship throws an
error, it will be destroyed and you lose precious Dogecoin (or will,
when we implement that).

Check out example_firmware.py to see a basic ship.
