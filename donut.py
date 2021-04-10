#!/usr/bin/env python

# Author: Guy Turner
# Date: 10/04/2021
# Description: Based on implementation of Andy Sloane's Donut in Python: https://www.a1k0n.net/2011/07/20/donut-math.html
# Produces a 3D animated 'donut'/torus rendered within a 2D ascii window, rotating about the x and z axis in space.
# The luminance of each  point is also calculated and represented using a different ascii character, choosing the point
# (0, 1, -1) (behind the viewers head) as the source of light.
# License: MIT
# Credits: Initial concept, documentation, and math simplifactions used from a1k0n.net (Andy Sloane)

from math import sin, cos, pi, ceil
from os import system

### USER VARIABLES ###

width = 50  # pixel width of window
height = 50  # pixel height of window
k1 = None  # field of view within window. If None, automatically calculated
k2 = 5  # arbitrary distance of object from viewer
r1 = 1  # radius of circle within torus
r2 = 2  # radius of torus revolution
A = 1.0  # initial position of x-axis rotation
B = 1.0  # initial position of z-axis rotation
theta_spacing = 0.07  # spacing between points on circle within torus
phi_spacing = 0.02  # spacing between points on torus of revolution
luminance = ".,-~:;=!*#$@"  # characters used to represent luminance (low->high)

### END OF USER VARIABLES ###

# clear command window - supports linux and windows
clear = lambda: system("cls||clear")

def render_frame(A, B):
    # Precompute sines and cosines of A & B
    cosA = cos(A)
    sinA = sin(A)
    cosB = cos(B)
    sinB = sin(B)

    # used to store z co-ords of all points. Used to ensure the front-most
    # point is always rendered. Zeros list of size width, height.
    z_buffer = [[0 for col in range(width)] for row in range(height)]

    # list of output characters for frame. ' ' list of size width, height.
    output = [[' ' for col in range(width)] for row in range(height)]

    # iterate through angular steps of circle within  cross-section of torus
    theta = 0
    while (theta < 2*pi):
        # precompute sine and cosine of theta
        costheta = cos(theta)
        sintheta = sin(theta)

        # compute x,y coordinates of the circle before torus revolution
        circlex = r2 +r1*costheta
        circley = r1*sintheta

        # iterate through angular steps of torus revolution
        phi = 0
        while (phi < 2*pi):
            # precompute sine and cosine of phi
            cosphi = cos(phi)
            sinphi = sin(phi)

            # final x,y, z coordinates after torus rotation
            x = circlex*(cosB*cosphi + sinA*sinB*sinphi) - circley*cosA*sinB
            y = circlex*(sinB*cosphi - sinA*cosB*sinphi) + circley*cosA*cosB
            z = k2 + cosA*circlex*sinphi + circley*sinA
            invz = 1/z

            # calculate projected x,y for 2d display.
            xp = int(width/2 + k1*invz*x)
            yp = int(height/2 - k1*invz*y)

            # calculate luminance
            l = cosphi*costheta*sinB - cosA*costheta*sinphi - sinA*sintheta + \
                cosB*(cosA*sintheta - costheta*sinA*sinphi)

            # l ranges from -sqrt(2) -> sqrt(2). If l is < 0, the surface is
            # pointing away from us (behind) so is ignored
            if l > 0:
                # test against the z_buffer. If invz is greater than existing,
                # the pixel is closer than the existing calculated.
                if invz > z_buffer[xp][yp]:
                    z_buffer[xp][yp] = invz
                    # 0 < l =< sqrt(2). We need this to translate to an
                    # index value 0->11 for the luminance string.
                    luminance_index = round(l*8)

                    # set the pixel output for this point using the luminance
                    output[xp][yp] = luminance[luminance_index]
            phi += phi_spacing
        theta += theta_spacing

    clear()  # clear terminal previous frame
    for i in range(height):
        row = ''
        for j in range(width):
            row += output[i][j]
        print(row)



# if user has not defined k1, calculate POV using a reasonable equation
if k1 is None: k1 = width*k2*3/(8*(r1+r2))

# animation loop:
while True:
    render_frame(A, B)
    A += 0.08  # speed of rotation about x-axis
    B += 0.03  # speed of rotation about z-axis
