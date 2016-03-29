PiSNES for Raspberry Pi by Squid
================================

INTRODUCTION
------------

This is a SNES Emulator port based on SNES9X 1.39. This is an old version of SNES9X but was chosen as it runs mostly at full speed on the Raspberry Pi unlike the more recent versions of SNES9X. Game support is therefore not as good as the newer SNES9X versions and graphics & sound is not as accurate.

Games that will not work, for example, are Yoshi's Island, Street Fighter Alpha 2, Star Fox.

This port supports keyboard and USB joystick input and are configurable. It uses GLES2/dispmanx for graphics so can run equally well in the Console or under X-Windows. The audio uses the ALSA API and SDL is used for input.

Web page for downloads, news, source, additional information:
https://sourceforge.net/projects/pisnes

(No asking for ROMS)

CONTROLS
--------
                     KEYBOARD     XBOX360 CONTROLS
    Up direction     up arrow     
    Down direction   down arrow
    Left direction   left arrow
    Right direction  right arrow
    X button         s            Y
    Y button         x            X
    A button         d            B
    B button         c            A
    TL button        a            TL
    TR button        f            TR
    Start button     return       START
    Select button    tab          BACK
    Turbo            backspace
    Quit             escape       BACK+START
    Quickload 1-4    F1-F4        RIGHT THUMB
    Quicksave 1-4    Shift F1-F4  LEFT THUMB

The joystick layout defaults to XBOX 360 controller button layout.

Additionally to quit with the joystick you can press SELECT+START.

All controls are configurable by editing the "snes9x.cfg" file.

Quickload and Quicksave, load and save snapshots of the game. Game saves are automatically loaded and saved when PiSNES starts and quits.

INSTALLATION
------------

    snes9x      -> Game binary
    snes9x.gui  -> Frontend binary
    snes9x.cfg  -> MAME configuration file, limited support to only the options in the supplied file (not the full MAME settings).
    preview/    -> Box art in jpg format, must be 640x480 or smaller, matching name of ROM file.
    roms/       -> ROMs directory (Put your game ROMs in here)
    skins/      -> Frontend skins directory
    $HOME/.snes96_snapshots/ -> SRM and snapshot saves are stored here

To run PiSNES simple run the "snes9x.gui" executable. At the command line "./snes9x.gui".
This runs the GUI frontend. To simply run PiSNES without the GUI enter "./snes9x roms/{gamerom}" where "{gamerom}" is the game rom filename to run.

It will work in X-Windows or in the Console.

Pi CONFIGURATION
----------------

I highly recommend overclocking your Raspberry Pi to gain maximum performance
as PiSNES is very CPU intensive and overclocking will make most games run at full speed.
The Pi 2 does not need overclocking.

My overclocking settings which work well, (/boot/config.txt)

    arm_freq=900
    sdram_freq=500

NOTE: Make sure overclocking is actually working by checking "cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor" should be "ondemand". Later kernels appear to set it to "powersave" by default.

If your sound is too quiet then do the following to fix that:

* First get the playback device, type "amixer controls"
* This will show the numid for the playback device, probably 3.
* Now set the volume, type "amixer cset numid=3 90%".
* Then reboot to make it permanent.

If you're having problems with HDMI audio then it is likely PulseAudio
is causing the issues as it has problems with the ALSA drivers. To fix
this simply remove PulseAudio:

* sudo apt-get --purge remove pulseaudio
* sudo apt-get autoremove

If you're getting a black screen when running in Console mode with
Composite output, try removing/commenting out the "overscan_" parameters from "/boot/config.txt" as follows (using disable_overscan doesn't appear to fix it):

    #overscan_left=16
    #overscan_right=16
    #overscan_top=16
    #overscan_bottom=16

GRAPHICS AND SOUND EFFECTS
--------------------------

Postprocessing can be enabled by setting "DisplayEffect" in snes9x.cfg. In addition you can disable anti-aliasing smoothing ("DisplaySmoothStretch" in snes9x.cfg). The postprocessing "phospher" effect does not run at full speed - i.e. it taxes the Pi GPU a little too much.

To improve the sound on the RPi 2 you can set "InterpolatedSound=1". This setting on the RPi 1 slows it down too much.

ORIGINAL CREDITS
----------------

  * The SNES9X team for their wonderful emulator (http://www.snes9x.com/)

PORT CREDITS
------------

  * Ported to Raspberry Pi by Squid.
  * Based on the Dingoo SDL version of SNES9X v1.39

CHANGE LOG
----------

September 2015:

  * Added boxart preview window.
  * DPAD configurable as buttons (resolves new xpad driver causing HAT issues)
   
February 21, 2015:

  * Added 2 player support.

February 12, 2015:

  * Joystick controls default to XBOX 360 controller.
  * More joystick axis support.
  * Initial HAT/DPAD support (seems to have issues on the XBOX 360 controller).

August 15, 2013:

  * Joystick axis are now configurable.

May 25, 2013:

  * Graphics backend rewritten to use GLES2 instead of Dispmanx, to enable GPU postprocessing.
  * Graphics smoothing (anti-aliasing) can be disabled.
  * Added postprocessing graphics effects, i.e. scanlines, phospher.
  * Vsync support is better meaning less stuttering.

May 11, 2013:

  * Added joystick button presses SELECT+TL quickload, SELECT+TR quicksave.
  * Fixed potential corruption to quicksaves using joystick.

May 08, 2013:

  * Added more configuration to the snes9x.cfg for graphics and sound.
  * Added options for aspect ratio, stretching and video border.
  * Pass command line options from frontend to runtime snes9x.
  * Fix config file not being read when calling snes9x binary outside of CWD.

May 02, 2013:

  * Added two joystick support.
  * The joystick buttons SELECT+START now quit.
  * Reduced sensitivity of the analog joystick.

April 24, 2013:

  * Initial release.
