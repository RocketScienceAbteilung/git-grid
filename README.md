# git grid

Control git from your grid controller


## Installation

Install Python and PortMidi (on OSX)

    brew install python --framework
    brew install portmidi

Create virtualenv

    virtualenv midihack
    cd midihack


### Installing git grid

Clone repository (make sure you're **not inside `isobar/`**)

    git clone git@github.com:RocketScienceAbteilung/git-grid.git gitgrid
    cd gitgrid
    pip install -e .

Run gitgrid

    git grid


#### Options

 - `-c` switch between supported grid controllers.
   - `launchpad`: Novation Launchpad Mini
   - `push`: Akai Ableton Push
   - `mpl`: Matplotlib software emulation
