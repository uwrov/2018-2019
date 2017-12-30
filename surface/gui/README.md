# ROV Interface GUI
##Features##
* Three camera feeds
  * One main, large one
  * Two small, secondary ones
  * All are displayed simultaneously and can be swapped
* Sensor data display
  * Updated several times a second and shown in a display feed
* Resizable/Collapsable panel areas
* Configuration panel
  * Camera feed IP and port configuration
  * Ability to send acton to the camera (e.g. quit, restart)
  * Links to camera config file settings
  * Slider for fundamental config options (e.g. brightness, contrast)
* Gamepad Input
  * Panel with visual output of controller buttons and axes
  * Controller button mapping

## Interface Basics
**Layout**  
The interface is divided into 6 resizable, collapsible panes. To resize any, drag the bars dividing them. To hide or show a pane, click on the darker section in the center of the resizing bar. By default the _config_ and _controller_ panes are hidden (respectively at the top and bottom of the interface).  

**Config Options**
The top panel, when expanded, will display configurable options for the camera IPs, ports, and settings. IP and ports can be set by entering them into the text boxes in the left section of the panel. On the right side, links to each camera's full config settings appears next to their name. Additionally, _quit_ and _restart_ actions are available for each camera, in the same location. Beneath sliders for changing basic settings of _ALL_ cameras.  
[List of all configurable options](http://www.lavrsen.dk/foswiki/bin/view/Motion/MotionGuideBasicFeatures)

**Gamepad Display**
The bottom panel will display the button and axe values of any connected controllers. The pane will be empty and grayed out when no controllers are detected.

## Controls
**Xbox:**  
**Back** - Cycle cameras  

**Mouse/Keyboard:**  
**Double click main camera** - Cycle cameras  

[Gamepad API](https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API/Using_the_Gamepad_API#Browser_compatibility)