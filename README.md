First Assignment- Research Track 1
================================

This is a simple, portable robot simulator developed by [Student Robotics](https://studentrobotics.org).
Some of the arenas and the exercises have been modified for the Research Track I course


## How to Run
-----------------------------

To run the script in the simulator, use run.py, passing it the file names.


```bash
$ python run.py Assignment.py
```

Code explanation
---------------------

For better performance of the robot, its most important tasks have been implemented into several functions:

Drive motors:
```bash
$ drive(speed, seconds)
```
By setting the "speed", it is possible to define the linear velocity of the robot. "seconds" indicates the duration of the generated speed.

Rotation:
```bash
$ turn(speed, seconds)
```
By setting the "speed", it is possible to define the angular velocity of the robot. "seconds" indicates the duration of the generated speed.

finding Silver tokens:
```bash
$ find_silver_token()
```
Generate the rotation and distance form the Silver Token respect to the robot. Retuens: 1)distance respect to the robot 2)rotation respect to the robot

Obstacle avoidance:
```bash
$ avoid_collision()
```
find golden tokens and allocate the rotations to different zones to detect the distance of golden tokens respect to the robot. Returns: angle and distance of 1)right side obstacles 2)left side obstacles 3)front side obstacles


Main loop: A while()-loop to control and navigate the robot in the right path to satisfy all desiered purposes.

How it works
-------------

The robot turns away if the angle and distance between the robot and the golden token is too small.

Whenever there is a minimal distance between a robot and a golden token, the robot performs a check to determine where the path to freedom is; it measures the distance between the wall on the right and the wall on the left (the walls are represented by golden tokens) and moves to the furthest one.

In the absence of a golden token and a small distance between them (less than the distance between the robot and the closest golden token), the robot turns against the silver token and continues.

It grabs the silver token when it is close enough, moves it behind itself, and then continues on its way.




Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/
