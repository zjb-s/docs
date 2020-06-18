---
layout: default
parent: scripting
grand_parent: norns
has_children: false
title: reference
nav_order: 4
has_toc: false
---

# norns script reference

**[core](#core)** &mdash; [keys and encoders](#keys-and-encoders) &mdash; [screen](#screen) &mdash; [softcut](softcut) &mdash; [engine](#engine) &mdash; [clock](#clock) &mdash; [metro](#metro) &mdash; [paramset](#paramset)<br/>
**[devices](#devices)** &mdash; [midi](#midi) &mdash; [grid](#grid) &mdash; [arc](#arc) &mdash; [hid](#hid) &mdash; [osc](#osc) &mdash; [crow](#crow)<br/>
**[libraries](#libraries)** &mdash; [util](#util) &mdash; [musicutil](#musicutil) &mdash; [pattern time](#pattern-time) &mdash; [intonation](#intonation)<br/>
**[meta](#meta)** &mdash; [basic script](#basic-script) &mdash; [directory structure](#directory-structure) &mdash; [crone](#crone) &mdash; [audio params](#audio-params)

# core

## keys and encoders

basic interface control for the standard norns key and encoder hardware

| callbacks | |
| :-- | :-- |
key(n,z)		| n: key number<br/>z: state (1=down, 0=up)
enc(n,d)		| n: enc number<br/>d: delta (postive=CW, negative=CCW)

| functions | |
| :-- | :-- |
norns.enc.sens(n,s)	| n: enc number<br/>s: sensitivity
norns.enc.accel(n,a)	| n: enc number<br/>a: acceleration

physical key events call the `key(n,z)` function, which you define in a script:

```
function key(n,z)
  print("key number " .. n .. " = " .. z)
end
```

encoder movements call `enc(n,d)` similarly. in addition, you can configure each encoders' sensitivity and acceleration independently:

```
function init()
  norns.enc.sens(1,8)   -- slow
  norns.enc.sens(2,1)   -- fast
  norns.enc.accel(3,4)  -- accelerated
end

enc = function(n,d)
  print(n,d)
end
```

## screen

interface for the norns screen hardware, which is 128 x 64 pixels with 16 levels of brightness per pixel. currently the screen redraws at 15fps.

| functions ||
| :-- | :-- |
screen.aa(state) |	enable/disable anti-aliasing.
screen.clear() 	| clear.
screen.level(value) | 	set level(color/brightness).
screen.line_width(w) | 	set line width.
screen.line_cap(style) | 	set line cap style.
screen.line_join(style) | 	set line join style.
screen.miter_limit(limit) | 	set miter limit.
screen.move(x, y) | 	move drawing position.
screen.move_rel(x, y) | 	move drawing position relative to current position.
screen.line(x, y) | 	draw line to specified point.
screen.line_rel(x, y) | 	draw line to specified point relative to current position.
screen.arc(x, y, r, angle1, angle2) | 	draw arc.
screen.circle(x, y, r) | 	draw circle.
screen.rect(x, y, w, h) | 	draw rectangle.
screen.curve(x1, y1, x2, y2, x3, y3) | 	draw curve (cubic Bézier spline).
screen.curve_rel(x1, y1, x2, y2, x3, y3) | 	draw curve (cubic Bézier spline) relative coordinates.
screen.close() | 	close current path.
screen.stroke() | 	stroke current path.
screen.fill() | fill current path.
screen.text(str) | 	draw text(left aligned).
screen.text_right(str) | 	draw text, right aligned.
screen.text_center(str) | 	draw text, center aligned.
screen.text_extents(str) | 	calculate width of text.
screen.font_face(index) | 	select font face.
screen.font_size(size) | 	set font size.
screen.pixel(x, y) | 	draw single pixel (requires integer x/y, fill afterwards).
screen.display_png(filename, x, y) | 	display png.


**notes:**
- place ALL screen function calls within the `redraw()` function, which is managed by the norns menu. putting screen calls outside of `redraw` may interfere with the menu.
- optimization tip: there is no need to call `redraw` faster than 15fps as you will not see the update. consider using a `clock` to call `redraw` at a fixed rate of `1/15`.
- see the [cairo tutorial](https://www.cairographics.org/tutorial/)

```
function redraw()
  screen.clear()
  screen.move(10,10)
  screen.text("hello world")
  screen.update()
end
```

## softcut


## engine

Specify an engine at the top of your script, see the [engine docs](https://monome.org/norns/classes/engine.html) for more details.

```lua
engine.name = 'PolySub'
```

If you want to use an engine from another project make sure to install that project first.
If the engine comes with an accompanying Lua file make sure to import it:

```lua
engine.name = 'R'

local R = require 'r/lib/r'
```

- `engine.list_commands()` shows the commands.

For example to set the command `cutoff` to 500:

```lua
engine.cutoff(500)
```

To see a list of all locally installed engines:

```lua
tab.print(engine.names)
```

## clock


## metro

The metro API allows for high-resolution scheduling, see the [metro docs](https://monome.org/norns/classes/metro.html) for more details.

```
re = metro.init()
re.time = 1.0 / 15
re.event = function()
  redraw()
end
```

- `re:start()`, starts metro.
- `re:stop()`, stops metro.

## paramset

The paramset API allows to read and write temporary data and files, see the [paramset docs](https://monome.org/norns/classes/paramset.html) for more details.

A parameter can be installed with the following:

```
params:add{type = "number", id = "someparam", name = "Some Param", min = 1, max = 48, default = 4}
```

- `params:set(index, value)`, writes a parameter.
- `params:get(index)`, reads a parameter.


# devices

## midi

`midi.connect(n)` to create device, returns object with handler, see the [midi docs](https://monome.org/norns/classes/midi.html) for more details.

```lua
m = midi.connect()
```

- `m:note_on(value,velocity,channel)`, sends `note_on` message.
- `m:note_off(value,velocity,channel)`, sends `note_off` message.
- `m.event`, midi event handler function.

## grid

`grid.connect(n)` to create device, returns object with handler, see the [grid docs](https://monome.org/norns/classes/grid.html) for more details.

```lua
g = grid.connect()
```

- `g:led(x, y, val)`, sets state of single LED on this grid device.
- `g:all(val)`, sets state of all LEDs on this grid device.
- `g:refresh()`, update any dirty quads on this grid device.
- `g.key(x, y, state)`, key event handler function.

## arc

`arc.connect(n)` to create device, returns object with handler, see the [arc docs](https://monome.org/norns/classes/arc.html) for more details.

```lua
a = arc.connect()
```

- `a:led(ring, x, val)`, sets state of single LED on this arc device.
- `a:all(val)`, sets state of all LEDs on this arc device.
- `a:segment(ring, from, to, level)`, creates an anti-aliased point to point arc - segment/range on a specific LED ring.
- `a:refresh()`, updates any dirty quads on this arc device.
- `a.delta(n, delta)`, encoder event handler function.

## hid

`hid.connect(n)` to create device, returns object with handler, see the [hid docs](https://monome.org/norns/classes/hid.html) for more details.

```lua
h = hid.connect()
```

## osc

to send from norns to another device:

- `osc.send(to, path, args)`, sends osc event. `to` is a table with IP/port pair, ie `{"192.168.0.11",30001}`

norns receives OSC on port 10111:

- `osc.event(path, args, from)` handler function called when an osc event is received.

params may be controlled remotely if `/params/` is matched on the same port. see param id numbers in the mapping screen of the param menu. for example:

```
/params/output_level 0.5
```

key and encoder actions can also be emulated, for example:

```
/remote/key 1 1
/remote/enc 2 -1
```

## crow


# libraries

## util

## musicutil

## pattern time

## intonation


# meta

## basic script

```lua
-- scriptname: short script description
-- v1.0.0 @author
-- llllllll.co/t/22222

engine.name = 'PolySub'

function init()
  -- initialization
end

function key(n,z)
  -- key actions: n = number, z = state
end

function enc(n,d)
  -- encoder actions: n = number, d = delta
end

function redraw()
  -- screen redraw
end

function cleanup()
  -- deinitialization
end
```

## directory structure

Scripts are located in `~/dust/code/`, and are what make norns do things. A script consists of at least a Lua file but can additionally also contain supporting Lua libraries, SuperCollider engines and data.

```
myscript/
  myscript.lua -- main version, shows up as MYSCRIPT
  mod.lua -- alt version, shows up as MYSCRIPT/MOD
  README.md -- main docs/readme
  data/
    myscript-01.pset -- pset, loaded via params:read(1) or via menu
  lib/
    somelib.lua -- arbitrary lib, imported via require 'lib/somelib'
    some-engine.sc -- engine file
    some-engine.lua -- engine lib, require lib/some-engine'
  docs/ -- more documentation, won't be shown in SELECT
    more-docs.md
```

## libraries

Lua libraries can be used by using `include("path/to/library")`, remember not to include `.lua` in the library name.

### local libraries

`include()` will first look in the directory of the current script. This allows using relative paths to use libraries local to the script. For example, with the following structure:

```
myscript/
  myscript.lua
  lib/
    somelib.lua
```

`myscript.lua` can include `somelib.lua` using:

```lua
include("lib/somelib")
```

### third-party libraries

Third party libraries can be included using their full path starting from the `~/dust/code/` directory. For example, with the following structure in `~/dust/code/`:

```
myscript/
  myscript.lua
  lib/
    somelib.lua
otherscript/
  otherscript.lua
  lib/
    otherlib.lua
```

`myscript.lua` can include `otherlib.lua` using:

```lua
include("otherscript/lib/otherlib")
```


## crone

![](../image/crone-process-routing.png)

[pdf version](../crone-process-routing.pdf)


## audio params

(from PLAY)

