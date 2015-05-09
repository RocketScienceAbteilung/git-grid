# git grid

Control git from your grid controller


## Installation

Install Python and PortMidi (on OSX)

    brew install python --framework
    brew install portmidi

Create virtualenv

    virtualenv midihack
    cd midihack
    source bin/activate


### Installing git grid

Clone repository (make sure you're **not inside `isobar/`**)

    git clone git@github.com:RocketScienceAbteilung/git-grid.git gitgrid
    cd gitgrid
    pip install -e .

Run gitgrid

    git grid


#### Options

 - `-c` switch between supported grid controllers.
   - `lpm`: Novation Launchpad Mini
   - `lp`: Novation Launchpad S
   - `lpp`: Novation Launchpad Pro
   - `push`: Akai Ableton Push
   - `mpl`: Matplotlib software emulation
 - `-i` manually set input port
 - `-o` manually set output port
