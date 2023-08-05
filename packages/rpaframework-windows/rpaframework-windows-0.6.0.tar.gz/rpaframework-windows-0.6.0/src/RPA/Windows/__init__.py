import logging
import platform
import warnings

# pylint: disable=wrong-import-position
from robotlibcore import DynamicCore


from RPA.Windows.keywords import (
    ActionKeywords,
    ElementKeywords,
    LocatorKeywords,
    WindowKeywords,
)


class Windows(DynamicCore):
    """The `Windows` is a library that can be used for Windows desktop automation.

    This library is at this moment in "BETA" stage as an alternative
    library for `RPA.Desktop.Windows`. Main difference being that this
    library is using `uiautomation`_ dependency instead of `pywinauto`.

    .. _uiautomation: https://github.com/yinkaisheng/Python-UIAutomation-for-Windows

    **About terminology**

    ***ControlType***

    Value referred to by locator keys `type:` or `control`. Represents type of application
    object, which can be e.g. `Window`, `Button` or `ListItem`.

    ***Element***

    Entity of an application structure (e.g. certain button in a window), which can be
    identified by a locator.

    **Locators**

    Locators are based on different strategies that can used identify Control object.

    Available strategies that can be used for the locators:

    =============== =======================
    Key             Maps to search property
    =============== =======================
    name            Name
    class           ClassName
    type            ControlType
    control         ControlType
    id              AutomationId
    automationid    AutomationId
    regex           RegexName
    subname         SubName
    index           foundIndex (int)
    offset          offset coordinates (x (int), y (int)) from control center
    executable      target window by its executable name
    handle          target window handle (int)
    desktop         target desktop
    process         *NOT YET SUPPORTED* target window by its executable's process id
    depth           searchDepth (int) for finding Control (default 8)
    =============== =======================

    Getting control over application object (Control) is done usually by first executing
    keyword ``Control Window`` which by default will search from desktop ControlType
    WindowControl objects with the given locator.

    Keyword ``Control Window`` can also be used to target application child WindowControl objects.

    Keyword examples:

    .. code-block:: robotframework

        Control Window    name:Calculator
        Control Window    Calculator  # will execute search by 'name:Calculator'
        Control Window    executable:Spotify.exe

    some example locators:

    .. code-block:: bash

        id:clearButton
        type:Group and name:'Number pad' > type:Button and index:4
        type:Group and name:'Number pad' > control:Button index:5
        id:Units1 > name:${unit}
        class:Button offset:370,0


    **Keyboard and mouse**

    Keyword

    **How to inspect**

    Most common and recommended by Microsoft, inspector tool for Windows, is `Accessibility Insights`_ that
    can be installed separately. Other options are tools `Inspect Object`_  and `UI Automation Verify`_, which
    can be accessed by installing Windows SDK.

    .. _Accessibility Insights: https://github.com/yinkaisheng/Python-UIAutomation-for-Windows
    .. _Inspect Object: https://docs.microsoft.com/en-us/windows/win32/winauto/inspect-objects
    .. _UI Automation Verify: https://docs.microsoft.com/en-us/windows/win32/winauto/ui-automation-verify

    **Recording**

    The package provides some rudimentary inspecting and recording via script SCRIPT_NAME

    ADD GUIDE HERE

    **Examples**

    Both Robot Framework and Python examples follow.

    The library must be imported first.

    .. code-block:: robotframework

        *** Settings ***
        Library    RPA.Windows


    Windows Calculator steps

    .. code-block:: robotframework

        *** Keywords ***
        Do some calculations
            Control Window    name:Calculator
            Click    id:clearButton
            Send Keys   96+4=
            ${result}=    Access Attribute or Method    id:CalculatorResults    Name
            Log To Console    n${result}


    """  # noqa: E501

    ROBOT_LIBRARY_SCOPE = "GLOBAL"
    ROBOT_LIBRARY_DOC_FORMAT = "REST"

    def __init__(self):
        # , timeout: float = None, simulate_move: bool = False
        self.logger = logging.getLogger(__name__)
        self.timeout = 0.5
        self.simulate_move = False
        self.window = None
        self.anchor_element = None

        # Register keyword libraries to LibCore
        libraries = [
            ActionKeywords(self),
            ElementKeywords(self),
            LocatorKeywords(self),
            WindowKeywords(self),
        ]
        super().__init__(libraries)
