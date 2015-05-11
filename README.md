# git grid

Control git from your grid controller. Works nicely with a
[plain text pattern sequencer](https://github.com/RocketScienceAbteilung/git-wig)
but works with any git reposity. 

![image](http://i.imgur.com/DdShbq2.jpg)


## Installation

Install Python and PortMidi (on OSX)

    brew install python --framework
    brew install portmidi

Create virtualenv

    virtualenv midihack
    cd midihack
    source bin/activate


### Installing git grid

    git clone git@github.com:RocketScienceAbteilung/git-grid.git gitgrid
    cd gitgrid
    pip install -e .

Run gitgrid

    git grid


#### Options

**MIDI Settings**

 - `-c` switch between supported grid controllers.
   - `lpm`: Novation Launchpad Mini
   - `lp`: Novation Launchpad S
   - `lpp`: Novation Launchpad Pro
   - `push`: Akai Ableton Push
   - `mpl`: Matplotlib software emulation
 - `-i` manually set input port
 - `-o` manually set output port

e.g to use it with the new Launchpad Pro

    git grid -c lpp

or to use it with an Ableton Push on a weird MIDI Port

    git grid -c push -i "Ableton Push Weird MIDI Port"


**Using Ableton Push LCD**

The LCD on Ableton Push can be used using the `pushcat` command. It behaves
much like the usual `cat` or `netcat` utilities by piping the input into it:

    echo MIDIHACK | pushcat
    ping www.google.de | pushcat

To use it with Git Grid, simply pipe the output into it

    git grid -c push | pushcat

You can use the **modulation wheel strip for scrolling** while `pushcat` is
running.

This means that one-shot commands (the ones that immediately quit,
like `ls`, `top` etc.) require you to keep `pushcat` running afterwards
using the `daemonize` switch:

    top | pushcat -d

and kill the process using `SIGINT` (Ctrl+C) afterwards.

Also, you can adjust the buffer size (wich defaults to 80 lines of text) that
is retained for scrolling on the Push controller

    top | pushcat -b 200
