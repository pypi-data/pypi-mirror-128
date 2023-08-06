"""
    domonic.events
    ====================================

    https://developer.mozilla.org/en-US/docs/Web/Events

"""

# from typing import *
import time


class EventTarget(object):
    """ EventTarget is a class you can extend to give your obj event dispatching abilities """

    def __init__(self, *args, **kwargs):
        self.listeners = {}

    def hasEventListener(self, _type):
        return _type in self.listeners

    # TODO - event: str, function, useCapture: bool
    # def addEventListener(self, event: str, function, useCapture: bool) -> None:
    def addEventListener(self, _type, callback, *args, **kwargs):
        if _type not in self.listeners:
            self.listeners[_type] = []
        self.listeners[_type].append(callback)

    def removeEventListener(self, _type, callback):
        if _type not in self.listeners:
            return

        stack = self.listeners[_type]

        for thing in stack:
            if thing == callback:
                stack.remove(thing)
                return

    def dispatchEvent(self, event):
        if event.type not in self.listeners:
            return True  # huh?. surely false?

        stack = self.listeners[event.type]
        # .slice()
        event.target = self  # TODO/NOTE - is this correct? - cant think where else would set it

        for thing in stack:
            try:
                thing(event)
                # type(thing, (Event,), self)
            except Exception as e:
                print(e)
                thing()  # try calling without params, user may not create param

        return not event.defaultPrevented


EventDispatcher = EventTarget  #: legacy alias


class Event(object):
    """ event """
    EMPTIED = "emptied"  #:
    ABORT = "abort"  #:
    AFTERPRINT = "afterprint"  #:
    BEFOREPRINT = "beforeprint"  #:
    BEFOREUNLOAD = "beforeunload"  #:
    CANPLAY = "canplay"  #:
    CANPLAYTHROUGH = "canplaythrough"  #:
    CHANGE = "change"  #:
    DURATIONCHANGE = "durationchange"  #:
    ENDED = "ended"  #:
    ERROR = "error"  #:
    FULLSCREENCHANGE = "fullscreenchange"  #:
    FULLSCREENERROR = "fullscreenerror"  #:
    INPUT = "input"  #:
    INVALID = "invalid"  #:
    LOAD = "load"  #:
    LOADEDDATA = "loadeddata"  #:
    LOADEDMETADATA = "loadedmetadata"  #:
    MESSAGE = "message"  #:
    OFFLINE = "offline"  #:
    ONLINE = "online"  #:
    OPEN = "open"  #:
    PAUSE = "pause"  #:
    PLAY = "play"  #:
    PLAYING = "playing"  #:
    PROGRESS = "progress"  #:
    RATECHANGE = "ratechange"  #:
    RESIZE = "resize"  #:
    RESET = "reset"  #:
    SCROLL = "scroll"  #:
    SEARCH = "search"  #:
    SEEKED = "seeked"  #:
    SEEKING = "seeking"  #:
    SELECT = "select"  #:
    SHOW = "show"  #:
    STALLED = "stalled"  #:
    SUBMIT = "submit"  #:
    SUSPEND = "suspend"  #:
    TOGGLE = "toggle"  #:
    UNLOAD = "unload"  #:
    VOLUMECHANGE = "volumechange"  #:
    WAITING = "waiting"  #:

    CAPTURING_PHASE = 1
    AT_TARGET = 2
    BUBBLING_PHASE = 3

    def __str__(self):
        return self.type + ":" + str(self.timeStamp)

    # Event("look", {"bubbles":true, "cancelable":false});
    def __init__(self, _type=None, *args, **kwargs):
        # print('type', _type)
        self.type = _type
        self.bubbles = None
        self.cancelable = None
        self.cancelBubble = None
        self.composed = None
        self.currentTarget = None
        self.defaultPrevented = False
        self.eventPhase = None
        self.explicitOriginalTarget = None
        self.isTrusted = None
        self.originalTarget = None
        self.returnValue = None
        self.srcElement = None
        self.target = None
        # ms = time.time_ns() // 1000000 3.7 up
        self.timeStamp = int(round(time.time() * 1000))

    def composedPath(self):
        return self.type + ":" + str(self.timeStamp)

    def initEvent(self, _type=None, *args, **kwargs):
        self.__init__(_type, args, kwargs)

    def stopPropagation(self):
        """[prevents further propagation of the current event in the capturing and bubbling phases]"""
        # self.defaultPrevented = True
        # self.returnValue = None
        # self.originalTarget = None
        # self.explicitOriginalTarget = None
        # self.target = None
        # self.srcElement = None
        # self.bubbles = None
        # self.cancelable = None
        # self.cancelBubble = None
        # self.composed = None
        # self.currentTarget = None
        # self.eventPhase = None
        # self.isTrusted = None
        # self.returnValue = None
        # self.timeStamp = int(round(time.time() * 1000))
        # self.type = None
        pass

    def msConvertURL(self):
        pass

    def preventDefault(self):
        pass

    def stopImmediatePropagation(self):
        pass


class UIEvent(Event):
    """ UIEvent """
    def __init__(self, _type, *args, **kwargs):
        self.detail = None
        self.view = None
        self.detail = None
        self.layerX = None
        self.layerY = None
        self.which = None
        self.sourceCapabilities = None
        super().__init__(_type, *args, **kwargs)

    def initUIEvent(self, _type, canBubble, cancelable, view, detail):
        self._type = _type
        self.canBubble = canBubble
        self.cancelable = cancelable
        self.view = view
        self.detail = detail


class MouseEvent(UIEvent):
    """ mouse events """
    CLICK = "click"  #:
    CONTEXTMENU = "contextmenu"  #:
    DBLCLICK = "dblclick"  #:
    MOUSEDOWN = "mousedown"  #:
    MOUSEENTER = "mouseenter"  #:
    MOUSELEAVE = "mouseleave"  #:
    MOUSEMOVE = "mousemove"  #:
    MOUSEOVER = "mouseover"  #:
    MOUSEOUT = "mouseout"  #:
    MOUSEUP = "mouseup"  #:

    def __init__(self, _type, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        self.x = 0
        self.y = 0
        self._clientX = 0
        self._clientX = 0
        self._altKey = False
        self._ctrlKey = False
        self._shiftKey = False
        self._metaKey = False
        self._button = None
        self._buttons = []

        super().__init__(_type, *args, **kwargs)

    def initMouseEvent(self, _type=None, canBubble=True, cancelable=True, view=None,
                       detail=None, screenX=0, screenY=0, clientX=0, clientY=0,
                       ctrlKey=False, altKey=False, shiftKey=False, metaKey=False,
                       button=None, relatedTarget=None, from_json={}, *args, **kwargs):
        # print('initMouseEvent')
        self._type = _type
        self.canBubble = canBubble
        self.cancelable = cancelable
        self.view = view
        self.detail = detail
        self.screenX = screenX
        self.screenY = screenY
        self._clientX = clientX
        self._clientY = clientY
        self._ctrlKey = ctrlKey
        self._altKey = altKey
        self._shiftKey = shiftKey
        self._metaKey = metaKey
        self._button = button
        self.relatedTarget = relatedTarget
        # TODO - parse from_json - so can relay

    @property
    def clientX(self):
        return self.x

    @property
    def clientY(self):
        return self.y

    @property
    def altKey(self):
        return self._altKey

    @property
    def ctrlKey(self):
        return self._ctrlKey

    @property
    def shiftKey(self):
        return self._shiftKey

    @property
    def metaKey(self):
        return self._metaKey

    @property
    def button(self):
        return self._button

    @property
    def buttons(self):
        return self._buttons

    @property
    def which(self):
        return self._button

    # MOUSE_EVENT
    def getModifierState(self):
        """Returns an array containing target ranges that will be affected by the insertion/deletion"""
        pass

    # MovementX Returns the horizontal coordinate of the mouse pointer relative to the position of the last mousemove event MouseEvent
    # MovementY Returns the vertical coordinate of the mouse pointer relative to the position of the last mousemove event   MouseEvent
    # offsetX   Returns the horizontal coordinate of the mouse pointer relative to the position of the edge of the target element   MouseEvent
    # offsetY   Returns the vertical coordinate of the mouse pointer relative to the position of the edge of the target element MouseEvent
    # pageX Returns the horizontal coordinate of the mouse pointer, relative to the document, when the mouse event was triggered    MouseEvent
    # pageY Returns the vertical coordinate of the mouse pointer, relative to the document, when the mouse event was triggered  MouseEvent
    # region        MouseEvent
    # relatedTarget Returns the element related to the element that triggered the mouse event   MouseEvent, FocusEvent


class KeyboardEvent(UIEvent):
    """ keyboard events """
    KEYDOWN = "keydown"  #:
    KEYPRESS = "keypress"  #:
    KEYUP = "keyup"  #:

    DOM_KEY_LOCATION_LEFT = 0  #:
    DOM_KEY_LOCATION_STANDARD = 1  #:
    DOM_KEY_LOCATION_RIGHT = 2  #:
    DOM_KEY_LOCATION_NUMPAD = 3  #:
    DOM_KEY_LOCATION_MOBILE = 4  #:
    DOM_KEY_LOCATION_JOYSTICK = 5  #:

    def __init__(self, _type, *args, **kwargs):
        # self.args = args
        # self.kwargs = kwargs
        self._altKey = False
        self._ctrlKey = False
        self._shiftKey = False
        self._metaKey = False

        self.charCode = None
        self.code = None
        self.key = None
        self.keyCode = None

        super().__init__(_type, *args, **kwargs)

    def initKeyboardEvent(self, typeArg, canBubbleArg, cancelableArg, viewArg, charArg, keyArg,
                          locationArg, modifiersListArg, repeat):
        self._type = typeArg
        self.canBubbleArg = canBubbleArg
        self.cancelableArg = cancelableArg
        self.viewArg = viewArg
        self.charArg = charArg
        self.keyArg = keyArg
        self.locationArg = locationArg
        self.modifiersListArg = modifiersListArg
        self.repeat = repeat

    @property
    def altKey(self):
        return self._altKey

    @property
    def ctrlKey(self):
        return self._ctrlKey

    @property
    def shiftKey(self):
        return self._shiftKey

    @property
    def metaKey(self):
        return self._metaKey

    @property
    def unicode(self):
        return self.key

    # @property
    # def keyCode(self):
    #     return self.keyCode

    # @property
    # def charCode(self):
    #     return self.charCode

    # @property
    # def code(self):
    #     return self.code

    # @property
    # def key(self):
    #     return self.key

    # def isComposing(self, *args, **kwargs):
    #     pass

    # KeyboardEvent
    # isComposing   Returns whether the state of the event is composing or not  InputEvent, KeyboardEvent
    # repeat    Returns whether a key is being hold down repeatedly, or not KeyboardEvent
    # location  Returns the location of a key on the keyboard or device KeyboardEvent


class CompositionEvent(UIEvent):
    """ CompositionEvent """

    START = "compositionstart"
    END = "compositionend"
    UPDATE = "compositionupdate"

    def __init__(self, _type, *args, **kwargs):
        self.data = None  #: Returns the characters generated by the input method that raised the event
        self.locale = None
        super().__init__(_type, *args, **kwargs)


class FocusEvent(UIEvent):
    """ FocusEvent """
    BLUR = "blur"  #:
    FOCUS = "focus"  #:
    FOCUSIN = "focusin"  #:
    FOCUSOUT = "focusout"  #:

    def __init__(self, _type, *args, **kwargs):
        self.relatedTarget = None
        super().__init__(_type, *args, **kwargs)


class TouchEvent(UIEvent):
    """ TouchEvent """
    TOUCHCANCEL = "touchcancel"  #:
    TOUCHEND = "touchend"  #:
    TOUCHMOVE = "touchmove"  #:
    TOUCHSTART = "touchstart"  #:

    def __init__(self, _type, *args, **kwargs):
        self.shiftKey = None
        self.altKey = None
        self.changedTouches = None
        self.ctrlKey = None
        self.metaKey = None
        self.shiftKey = None
        self.targetTouches = None
        self.touches = None
        super().__init__(_type, *args, **kwargs)


class WheelEvent(UIEvent):
    """ WheelEvent """
    MOUSEWHEEL = "mousewheel"  # DEPRECATED - USE WHEEL  #:
    WHEEL = "wheel"  #:

    def __init__(self, _type, *args, **kwargs):
        self.deltaX = None
        self.deltaY = None
        self.deltaZ = None
        self.deltaMode = None
        super().__init__(_type, *args, **kwargs)


class AnimationEvent(Event):
    """ AnimationEvent """
    ANIMATIONEND = "animationend"  #:
    ANIMATIONITERATION = "animationiteration"  #:
    ANIMATIONSTART = "animationstart"  #:

    def __init__(self, _type, *args, **kwargs):
        self.animationName = None
        """ Returns the name of the animation """
        self.elapsedTime = None
        """ Returns the number of seconds an animation has been running """
        self.pseudoElement = None
        """ Returns the name of the pseudo-element of the animation """
        super().__init__(_type, *args, **kwargs)


class ClipboardEvent(Event):
    """ ClipboardEvent """
    COPY = "copy"  #:
    CUT = "cut"  #:
    PASTE = "paste"  #:

    def __init__(self, _type, *args, **kwargs):
        self.clipboardData = None
        """ Returns an object containing the data affected by the clipboard operation """
        super().__init__(_type, *args, **kwargs)


class ErrorEvent(Event):
    """ ErrorEvent """
    ERROR = "error"  #:

    def __init__(self, _type, *args, **kwargs):
        self.message = None
        # self.filename=None
        # self.lineno=0
        # self.colno=0
        # self.error={}
        super().__init__(_type, *args, **kwargs)


class SubmitEvent(Event):
    """ SubmitEvent """
    SUBMIT = "submit"  #:

    def __init__(self, _type, *args, **kwargs):
        super().__init__(_type, *args, **kwargs)


class PointerEvent(Event):
    """ PointerEvent """
    POINTER = "pointer"  #:
    POINTERCANCEL = "pointercancel"  #:
    POINTERDOWN = "pointerdown"  #:
    POINTERENTER = "pointerenter"  #:
    POINTERLEAVE = "pointerleave"  #:
    POINTERMOVE = "pointermove"  #:
    POINTEROUT = "pointerout"  #:
    POINTEROVER = "pointerover"  #:
    POINTERUP = "pointerup"  #:

    def __init__(self, _type, *args, **kwargs):
        self.pointerId = None
        self.width = None
        self.height = None
        self.pressure = None
        self.tangentialPressure = None
        self.tiltX = None
        self.tiltY = None
        self.twist = None
        self.pointerType = None
        self.isPrimary = None
        super().__init__(_type, *args, **kwargs)

    def getCoalescedEvents(self):
        pass

    def getPredictedEvents(self):
        pass

    # def getCurrentPoint(self, element):
    #     """ Returns the current coordinates of the specified element relative to the viewport. """
    #     pass

    # def getIntermediatePoints(self, element):
    #     """ Returns the coordinates of all the intermediate points of the pointer along the path of the pointer. """
    #     pass


class BeforeUnloadEvent(Event):
    BEFOREUNLOAD = "beforeunload"  #:
    """ BeforeUnloadEvent """
    def __init__(self, _type, *args, **kwargs):
        super().__init__(_type, *args, **kwargs)


class SVGEvent(Event):
    """ SVGEvent """
    ABORT = "abort"  #:
    LOAD = "load"  #:
    LOADEDDATA = "loadeddata"  #:
    LOADEDMETADATA = "loadedmetadata"  #:
    LOADSTART = "loadstart"  #:
    PROGRESS = "progress"  #:
    SCROLL = "scroll"  #:
    UNLOAD = "unload"  #:
    ERROR = "error"  #:

    def __init__(self, _type, *args, **kwargs):
        super().__init__(_type, *args, **kwargs)

    # def initEvent(self, eventTypeArg, canBubbleArg, cancelableArg):
    #     pass


class TimerEvent(Event):
    TIMER = "timer"  #:
    TIMER_COMPLETE = "timercomplete"  #:
    """ TimerEvent """
    def __init__(self, _type, *args, **kwargs):
        super().__init__(_type, *args, **kwargs)

    # def initTimerEvent(self, type, bubbles, cancelable, detail):
    #     """ initTimerEvent() """
    #     pass


class DragEvent(Event):
    """ DragEvent """
    DRAG = "drag"  #:
    END = "dragend"  #:
    ENTER = "dragenter"  #:
    EXIT = "dragexit"  #:
    LEAVE = "dragleave"  #:
    OVER = "dragover"  #:
    START = "dragstart"  #:
    DROP = "drop"  #:

    def __init__(self, _type, *args, **kwargs):
        self.dataTransfer = None
        """ Returns the data that is dragged/dropped """
        super().__init__(_type, *args, **kwargs)


class HashChangeEvent(Event):
    """ HashChangeEvent """
    CHANGE = "hashchange"  #:

    def __init__(self, _type, *args, **kwargs):
        self.newURL = None
        self.oldURL = None
        super().__init__(_type, *args, **kwargs)


class InputEvent(UIEvent):
    """ InputEvent """
    CHANGE = "change"  #:
    SELECT = "select"  #:
    INPUT = "input"  #:

    def __init__(self, _type, *args, **kwargs):
        self.data = None
        """ Returns the inserted characters """
        self.dataTransfer
        """ Returns an object containing information about the inserted/deleted data """
        self.inputType
        """ Returns the type of the change (i.e "inserting" or "deleting") """
        self.isComposing
        """ Returns whether the state of the event is composing or not """
        super().__init__(_type, *args, **kwargs)

    def getTargetRanges(self):
        """ Returns an array containing target ranges that will be affected by the insertion/deletion """
        pass


class PageTransitionEvent(Event):
    """ PageTransitionEvent """
    PAGEHIDE = "pagehide"  #:
    PAGESHOW = "pageshow"  #:

    def __init__(self, _type, *args, **kwargs):
        self.persisted = None
        """ Returns whether the webpage was cached by the browser """
        super().__init__(_type, *args, **kwargs)


class PopStateEvent(Event):
    """ PopStateEvent """
    POPSTATE = "popstate"  #:
    # ONPOPSTATE = "onpopstate"  #:??

    def __init__(self, _type, *args, **kwargs):
        self.state = None
        """ Returns an object containing a copy of the history entries """
        super().__init__(_type, *args, **kwargs)


class StorageEvent(Event):
    """ StorageEvent """
    STORAGE = "storage"  #:

    def __init__(self, _type, *args, **kwargs):
        self.key = None
        """ Returns the key of the changed storage item """
        self.newValue = None
        """ Returns the new value of the changed storage item """
        self.oldValue = None
        """ Returns the old value of the changed storage item """
        self.storageArea = None
        """ Returns an object representing the affected storage object """
        self.url = None
        """ Returns the URL of the changed item's document """
        super().__init__(_type, *args, **kwargs)


class TransitionEvent(Event):
    """ TransitionEvent """
    TRANSITIONEND = "transitionend"  #:

    def __init__(self, _type, *args, **kwargs):
        self.propertyName = None
        """ Returns the name of the transition"""
        self.elapsedTime = None
        """  Returns the number of seconds a transition has been running """
        self.pseudoElement = None
        """ Returns the name of the pseudo-element of the transition """
        super().__init__(_type, *args, **kwargs)


class ProgressEvent(Event):
    """ ProgressEvent """
    LOADSTART = "loadstart"  #:
    PROGRESS = "progress"  #:
    ABORT = "abort"  #:
    ERROR = "error"  #:
    LOAD = "load"  #:
    LOADED = "loaded"  #:
    LOADEND = "loadend"  #:
    TIMEOUT = "timeout"  #:

    def __init__(self, _type, *args, **kwargs):
        super().__init__(_type, *args, **kwargs)


class CustomEvent(Event):
    """ CustomEvent """
    def __init__(self, _type, *args, **kwargs):
        self.detail = None
        super().__init__(_type, *args, **kwargs)

    def initCustomEvent(self):
        pass


class GamePadEvent(Event):
    """ GamePadEvent """
    START = "gamepadconnected"  #:
    STOP = "gamepaddisconnected"  #:

    def __init__(self, _type, *args, **kwargs):
        self.gamepad = None
        super().__init__(_type, *args, **kwargs)


# TODO - tests and service worker API
class FetchEvent(Event):
    """ FetchEvent """
    FETCH = "fetch"  #:

    def __init__(self, _type, *args, **kwargs):
        self.clientId = None
        """ Returns the client ID of the fetch request """
        self.request = None
        """ Returns the request object """
        self.isReload = None
        """ Returns whether the request is a reload or not """
        super().__init__(_type, *args, **kwargs)

    @property
    def isReload(self):
        return self.request.url == self.request.referrer

    @property
    def replacesClientId(self):
        return self.clientId != self.request.clientId

    @property
    def resultingClientId(self):
        return self.clientId if self.replacesClientId else self.request.clientId

    def respondWith(self, response):
        """ Returns a promise that resolves to the response object """
        pass

    def waitUntil(self, promise):
        """ Returns a promise that resolves when the response is available """
        pass


class ExtendableEvent(Event):
    """ ExtendableEvent """

    # CAPTURING_PHASE = 1
    # AT_TARGET = 2
    # BUBBLING_PHASE = 3

    def __init__(self, _type, *args, **kwargs):
        self.extendable = None
        """ Returns whether the event is extendable or not """
        self.timeStamp = None
        """ Returns the time stamp of the event """
        # self.waitUntil(promise)
        """ Returns a promise that resolves when the event is handled """
        super().__init__(_type, *args, **kwargs)


class SyncEvent(ExtendableEvent):
    """ SyncEvent """
    SYNC = "sync"  #:

    def __init__(self, _type, *args, **kwargs):
        self.tag = None
        """ Returns the tag of the sync event """
        self.lastChance = None
        """ Returns whether the sync event is the last chance or not """
        super().__init__(_type, *args, **kwargs)

# class InstallEvent()

# class DeviceMotionEvent(Event):
#     """ DeviceMotionEvent """
#     def __init__(self, _type, *args, **kwargs):
#         self.acceleration = None
#         """ Returns the acceleration of the device """
#         self.accelerationIncludingGravity = None
#         """ Returns the acceleration of the device, including gravity """
#         self.rotationRate = None
#         """ Returns the rotation rate of the device """
#         self.interval = None
#         """ Returns the time interval between the previous and the current event """
#         super().__init__(_type, *args, **kwargs)


# class DeviceOrientationEvent(Event):
#     """ DeviceOrientationEvent """
#     def __init__(self, _type, *args, **kwargs):
#         self.absolute = None
#         """ Returns true if the orientation is absolute """
#         self.alpha = None
#         """ Returns the orientation of the device in degrees, relative to the Earth's coordinate system """
#         self.beta = None
#         """ Returns the orientation of the device in degrees, relative to the Earth's coordinate system """
#         self.gamma = None
#         """ Returns the orientation of the device in degrees, relative to the Earth's coordinate system """
#         self.interval = None
#         """ Returns the time interval between the previous and the current event """
#         super().__init__(_type, *args, **kwargs)


# class DeviceLightEvent(Event):
#     """ DeviceLightEvent """
#     def __init__(self, _type, *args, **kwargs):
#         self.value = None
#         """ Returns the value of the ambient light sensor """
#         super().__init__(_type, *args, **kwargs)


# class DeviceProximityEvent(Event):
#     """ DeviceProximityEvent """
#     def __init__(self, _type, *args, **kwargs):
#         self.value = None
#         """ Returns the value of the proximity sensor """
#         self.min = None
#         """ Returns the minimum value of the proximity sensor """
#         self.max = None
#         """ Returns the maximum value of the proximity sensor """
#         super().__init__(_type, *args, **kwargs)


class TweenEvent(Event):
    """ TweenEvent """
    START = "onStart"  #:
    STOP = "onStop"  #:
    RESET = "onReset"  #:
    PAUSE = "onPause"  #:
    UNPAUSE = "onUnPause"  #:
    UPDATE_START = "onUpdateStart"  #:
    UPDATE_END = "onUpdateEnd"  #:
    COMPLETE = "onComplete"  #:

    TIMER = "onTimer"  #:
    _source = None

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, source):
        self._source = source

    def __init__(self, _type, source=None, bubbles=False, cancelable=False):
        # super.__init__(self, type, bubbles, cancelable)
        super().__init__(_type)  # TODO -
        self.source = source


class PromiseRejectionEvent(Event):  # TODO - put in the js class?

    # constants
    UNHANDLED = "unhandledrejection"  #:
    HANDLED = "rejectionhandled"  #:

    """ PromiseRejectionEvent """
    def __init__(self, _type, *args, **kwargs):
        self.promise = None
        """ Returns the promise that was rejected """
        self.reason = None
        """ Returns the reason of the rejection """
        self.isRejected = None
        """ Returns whether the promise was rejected or not """
        super().__init__(_type, *args, **kwargs)


class GlobalEventHandler:  # (EventDispatcher):

    # def __init__(self):
    #     super().__init__(self)
    #     self.addEventListener(KeyboardEvent.KEYDOWN, self.onkeydown)
    #     self.addEventListener(KeyboardEvent.KEYUP, self.onkeyup)

    #     self.addEventListener(MouseEvent.MOUSEMOVE, self.onmousemove)
    #     self.addEventListener(MouseEvent.MOUSEDOWN, self.onmousedown)
    #     self.addEventListener(MouseEvent.MOUSEUP, self.onmouseup)

    #     self.addEventListener(DragEvent.DRAG, self.ondrag)
    #     self.addEventListener(DragEvent.END, self.ondragend)
    #     self.addEventListener(DragEvent.ENTER, self.ondragenter)
    #     self.addEventListener(DragEvent.EXIT, self.ondragexit)
    #     self.addEventListener(DragEvent.LEAVE, self.ondragleave)
    #     self.addEventListener(DragEvent.OVER, self.ondragover)
    #     self.addEventListener(DragEvent.START, self.ondragstart)
    #     self.addEventListener(DragEvent.DROP, self.ondrop)

    #     self.addEventListener(ClipboardEvent.CUT, self.oncut)
    #     self.addEventListener(ClipboardEvent.COPY, self.oncopy)
    #     self.addEventListener(ClipboardEvent.PASTE, self.onpaste)

    def onabort(self, event):
        print(event)
        raise NotImplementedError

    def onblur(self, event):
        print(event)
        raise NotImplementedError

    def oncancel(self, event):
        print(event)
        raise NotImplementedError

    def oncanplay(self, event):
        print(event)
        raise NotImplementedError

    def oncanplaythrough(self, event):
        print(event)
        raise NotImplementedError

    def onchange(self, event):
        print(event)
        raise NotImplementedError

    def onclick(self, event):
        print(event)
        raise NotImplementedError

    def onclose(self, event):
        print(event)
        raise NotImplementedError

    def oncontextmenu(self, event):
        print(event)
        raise NotImplementedError

    def oncuechange(self, event):
        print(event)
        raise NotImplementedError

    def ondblclick(self, event):
        print(event)
        raise NotImplementedError

    def ondrag(self, event):
        print(event)
        raise NotImplementedError

    def ondragend(self, event):
        print(event)
        raise NotImplementedError

    def ondragenter(self, event):
        print(event)
        raise NotImplementedError

    def ondragexit(self, event):
        print(event)
        raise NotImplementedError

    def ondragleave(self, event):
        print(event)
        raise NotImplementedError

    def ondragover(self, event):
        print(event)
        raise NotImplementedError

    def ondragstart(self, event):
        print(event)
        raise NotImplementedError

    def ondrop(self, event):
        print(event)
        raise NotImplementedError

    def ondurationchange(self, event):
        print(event)
        raise NotImplementedError

    def onemptied(self, event):
        print(event)
        raise NotImplementedError

    def onended(self, event):
        print(event)
        raise NotImplementedError

    def onerror(self, event):
        print(event)
        raise NotImplementedError

    def onfocus(self, event):
        print(event)
        raise NotImplementedError

    def ongotpointercapture(self, event):
        print(event)
        raise NotImplementedError

    def oninput(self, event):
        print(event)
        raise NotImplementedError

    def oninvalid(self, event):
        print(event)
        raise NotImplementedError

    def onkeydown(self, event):
        print(event)
        raise NotImplementedError

    def onkeypress(self, event):
        print(event)
        raise NotImplementedError

    def onkeyup(self, event):
        print(event)
        raise NotImplementedError

    def onload(self, event):
        print(event)
        raise NotImplementedError

    def onloadeddata(self, event):
        print(event)
        raise NotImplementedError

    def onloadedmetadata(self, event):
        print(event)
        raise NotImplementedError

    def onloadend(self, event):
        print(event)
        raise NotImplementedError

    def onloadstart(self, event):
        print(event)
        raise NotImplementedError

    def onlostpointercapture(self, event):
        print(event)
        raise NotImplementedError

    def onmouseenter(self, event):
        print(event)
        raise NotImplementedError

    def onmouseleave(self, event):
        print(event)
        raise NotImplementedError

    def onmousemove(self, event):
        print(event)
        raise NotImplementedError

    def onmouseout(self, event):
        print(event)
        raise NotImplementedError

    def onmouseover(self, event):
        print(event)
        raise NotImplementedError

    def onmouseup(self, event):
        print(event)
        raise NotImplementedError

    def onpause(self, event):
        print(event)
        raise NotImplementedError

    def onplay(self, event):
        print(event)
        raise NotImplementedError

    def onplaying(self, event):
        print(event)
        raise NotImplementedError

    def onpointercancel(self, event):
        print(event)
        raise NotImplementedError

    def onpointerdown(self, event):
        print(event)
        raise NotImplementedError

    def onpointerenter(self, event):
        print(event)
        raise NotImplementedError

    def onpointerleave(self, event):
        print(event)
        raise NotImplementedError

    def onpointermove(self, event):
        print(event)
        raise NotImplementedError

    def onpointerout(self, event):
        print(event)
        raise NotImplementedError

    def onpointerover(self, event):
        print(event)
        raise NotImplementedError

    def onpointerup(self, event):
        print(event)
        raise NotImplementedError

    def onprogress(self, event):
        print(event)
        raise NotImplementedError

    def onratechange(self, event):
        print(event)
        raise NotImplementedError

    def onreset(self, event):
        print(event)
        raise NotImplementedError

    def onresize(self, event):
        print(event)
        raise NotImplementedError

    def onscroll(self, event):
        print(event)
        raise NotImplementedError

    def onseeked(self, event):
        print(event)
        raise NotImplementedError

    def onseeking(self, event):
        print(event)
        raise NotImplementedError

    def onselect(self, event):
        print(event)
        raise NotImplementedError

    def onselectionchange(self, event):
        print(event)
        raise NotImplementedError

    def onselectstart(self, event):
        print(event)
        raise NotImplementedError

    def onshow(self, event):
        print(event)
        raise NotImplementedError

    def onstalled(self, event):
        print(event)
        raise NotImplementedError

    def onsubmit(self, event):
        print(event)
        raise NotImplementedError

    def onsuspend(self, event):
        print(event)
        raise NotImplementedError

    def ontimeupdate(self, event):
        print(event)
        raise NotImplementedError

    def onvolumechange(self, event):
        print(event)
        raise NotImplementedError

    def onwaiting(self, event):
        print(event)
        raise NotImplementedError

    def onwheel(self, event):
        print(event)
        raise NotImplementedError

    def onanimationcancel(self, event):
        print(event)
        raise NotImplementedError

    def onanimationend(self, event):
        print(event)
        raise NotImplementedError

    def onanimationiteration(self, event):
        print(event)
        raise NotImplementedError

    def onauxclick(self, event):
        print(event)
        raise NotImplementedError

    def onformdata(self, event):
        print(event)
        raise NotImplementedError

    def onmousedown(self, event):
        print(event)
        raise NotImplementedError

    def ontouchcancel(self, event):
        print(event)
        raise NotImplementedError

    def ontouchstart(self, event):
        print(event)
        raise NotImplementedError

    def ontransitioncancel(self, event):
        print(event)
        raise NotImplementedError

    def ontransitionend(self, event):
        print(event)
        raise NotImplementedError


class WindowEventHandler:  # (EventHandler): # TODO - put in the window module?
    def __init__(self, window):
        super().__init__()
        self.window = window

    def onabort(self, event):
        print(event)
        raise NotImplementedError

    def onafterprint(self, event):
        print(event)
        raise NotImplementedError

    def onbeforeprint(self, event):
        print(event)
        raise NotImplementedError

    def onbeforeunload(self, event):
        print(event)
        raise NotImplementedError

    def onblur(self, event):
        print(event)
        raise NotImplementedError

    def oncanplay(self, event):
        print(event)
        raise NotImplementedError

    def oncanplaythrough(self, event):
        print(event)
        raise NotImplementedError

    def onchange(self, event):
        print(event)
        raise NotImplementedError

    def onclick(self, event):
        print(event)
        raise NotImplementedError

    def oncontextmenu(self, event):
        print(event)
        raise NotImplementedError

    def oncopy(self, event):
        print(event)
        raise NotImplementedError

    def oncuechange(self, event):
        print(event)
        raise NotImplementedError

    def oncut(self, event):
        print(event)
        raise NotImplementedError

    def ondblclick(self, event):
        print(event)
        raise NotImplementedError

    def ondrag(self, event):
        print(event)
        raise NotImplementedError

    def ondragend(self, event):
        print(event)
        raise NotImplementedError

    def ondragenter(self, event):
        print(event)
        raise NotImplementedError

    def ondragleave(self, event):
        print(event)
        raise NotImplementedError

    def ondragover(self, event):
        print(event)
        raise NotImplementedError
