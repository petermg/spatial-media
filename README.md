This fork is designed to fake googles VR180 camera metadata.

Please download using the 'Clone or download' button, the releases have been inherited from the original Google repository
and do not work for VR180.

It uses Spherical Video V2 metadata and gives a choice between Mesh Projection for fisheye videos
or equi-rectangular projection with the left and right crop set to 1073741823 which is 0x3FFFFFFF or 1/4 of 0xFFFFFFFF.
It can also be used to display full frame SBS 3D video (ala 3D movies) in Youtube using VR180 compatibility
with some limitation without requiring a re-encode to fisheye or equirectangular.

To use it you need a copy of python 2.7 or 3.6  and use the command line or GUI.

Typical usage:

python spatialmedia -i -s left-right -m equirectangular Test_180_3D.mp4 Test_STV2_180_3D.mp4

or

python spatialmedia -i -s top-bottom -m equirectangular Test_180_3D.mp4 Test_STV2_180_3D.mp4

or

python spatialmedia -i -s left-right -m mesh Test_180_3D.mp4 Test_STV2_180_3D.mp4

or

python spatialmedia -i -s left-right -m full-frame Test_sbs_ff_3D.mp4 Test_STV2_ff_3D.mp4

This will take the first file, inject the metadata and write the result out to the second file.

or alternatively

cd spatialmedia
python gui.py

to use the simple GUI. Note on the GUI mesh is called fisheye after the style of video it works with.

Please note that nearly all the mesh and equirectangular options will create the correct metadata
(the exeception being -m mesh will ignore --degree=360) but not all the options are accepted by Youtube.

As of 5th, June 2018 Youtube will accept...

-m equirectangular with all options except the combination of 180 degree and mono.
-m mesh is restricted to stereo 3D at 180 degrees
-m full-frame is targeted at 16x9 video at the moment and Youtube probably don't support it, it just happens to work.


So mesh is restricted to 180 degree 3D videos in a 1:1 ratio.
Equirectangular will work for all 360 formats but 180 degree videos have to have stereo image pairs.

There is no way to do mono 180 without resorting to SBS or OU stereo image pairs with the same 
image duplicated in the frame.


This is basically kodabb/spatial-media sphericaltoolsv2 branch with some hacking around
merged into master so anyone wanting to use this doesn't have to play around with branches.

THe original readme details below.

# Spatial Media

A collection of specifications and tools for 360&deg; video and spatial audio, including:

- [Spatial Audio](docs/spatial-audio-rfc.md) metadata specification
- [Spherical Video](docs/spherical-video-rfc.md) metadata specification
- [Spherical Video V2](docs/spherical-video-v2-rfc.md) metadata specification
- [Spatial Media tools](spatialmedia/) for injecting spatial media metadata in media files

Try out [Jump Inspector](https://g.co/jump/inspector), an Android app for previewing VR videos with spatial audio.
