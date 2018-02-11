This fork is designed to fake googles VR180 camera metadata.
It uses Spherical Video V2 metadata with the left and right crop set to 
1073741823 which is 0x3FFFFFFF or 1/4 of 0xFFFFFFFF.

Note this breaks 360 video's at the momenti as I've haven't coded any options I just wanted to get
this out to the public.

Note 2. Google may decide to break this as they do not seem to be interested in telling people how to do this.

To use it you need a copy of python 2.7 (I've not tried it with 3.x)  and use the command line.
It seems to work with top bottom and side by side layouts.

Typical usage:

python spatialmedia -i -s left-right -m equirectangular Test_180_3D.mp4 Test_STV2_180_3D.mp4
or
python spatialmedia -i -s top-bottom -m equirectangular Test_180_3D.mp4 Test_STV2_180_3D.mp4

This will take the first file, inject the metadata and write the result out to the second file.

This is basically kodabb/spatial-media sphericaltoolsv2 branch with two lines changed and
merged into master so anyone wanting to use this doesn't have to play around with branches.

THe original readme details below.

# Spatial Media

A collection of specifications and tools for 360&deg; video and spatial audio, including:

- [Spatial Audio](docs/spatial-audio-rfc.md) metadata specification
- [Spherical Video](docs/spherical-video-rfc.md) metadata specification
- [Spherical Video V2](docs/spherical-video-v2-rfc.md) metadata specification
- [Spatial Media tools](spatialmedia/) for injecting spatial media metadata in media files

Try out [Jump Inspector](https://g.co/jump/inspector), an Android app for previewing VR videos with spatial audio.
