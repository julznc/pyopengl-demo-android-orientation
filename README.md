# pyopengl-demo-android-orientation

http://projectproto.blogspot.com/2015/09/pyopengl-demo-android-orientation.html

python [desktop] opengl demo displaying android device orientation.
android device sends sensor values via wifi connection.
opengl [desktop] displays the orientation by rotating a box object.

desktop:
    python 3.4
	PyOpenGL-3.1
	HTTPServer (http.server)

android device:
    QPython 3
	androidhelper sensors
	HTTPConnection (http.client)
