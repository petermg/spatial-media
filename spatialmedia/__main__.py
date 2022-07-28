#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2016 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Spatial Media Metadata Injector 

Tool for examining and injecting spatial media metadata in MP4/MOV files.
"""

import argparse
import os
import re
import sys

path = os.path.dirname(sys.modules[__name__].__file__)
path = os.path.join(path, '..')
sys.path.insert(0, path)
from spatialmedia import metadata_utils
from argparse import RawTextHelpFormatter


def console(contents):
  print(contents)


def main():
  """Main function for printing and injecting spatial media metadata."""

  parser = argparse.ArgumentParser(
      formatter_class=RawTextHelpFormatter,
      usage=
      "%(prog)s [options] [files...]\n\nBy default prints out spatial media "
      "metadata from specified files.")
  parser.add_argument(
      "-i",
      "--inject",
      action="store_true",
      help=
      "injects spatial media metadata into the first file specified (.mp4 or "
      ".mov) and saves the result to the second file specified")
  parser.add_argument(
      "-b",
      "--show-atoms",
      action="store_true",
      help=
      "Displays the atom layout for the movie. Note the MOV/MP4 format is not self-parsable"
      "e.g. there is no way to know the containts of a container atom without documentation.")

  video_group = parser.add_argument_group("Spherical Video")
  video_group.add_argument(
      "-s",
      "--stereo",
      action="store",
      dest="stereo_mode",
      metavar="STEREO-MODE",
      choices=["none", "top-bottom", "left-right", "custom", "right-left"],
      default=None,
      help="stereo mode (none | top-bottom | left-right | custom | right-left)")
  video_group.add_argument(
      "-m",
      "--projection",
      action="store",
      dest="projection",
      metavar="SPHERICAL-MODE",
      choices=["equirectangular", "cubemap", "mesh", "full-frame", "equi-mesh"],
      default=None,
      help="projection (equirectangular | cubemap | mesh | full-frame | equi-mesh)")
  video_group.add_argument(
      "-y",
      "--yaw",
      action="store",
      dest="yaw",
      metavar="YAW",
      default=0,
      help="yaw")
  video_group.add_argument(
      "-p",
      "--pitch",
      action="store",
      dest="pitch",
      metavar="PITCH",
      default=0,
      help="pitch")
  video_group.add_argument(
      "-r",
      "--roll",
      action="store",
      dest="roll",
      metavar="ROLL",
      default=0,
      help="roll")
  video_group.add_argument(
      "-d",
      "--degrees",
      action="store",
      dest="degrees",
      metavar="DEGREES",
      choices=["180", "360"],
      default=180,
      help="degrees")
  video_group.add_argument(
       "-c",
       "--correction",
       action="store",
       dest="fisheye_correction",
       metavar="FISHEYE-CORRECTION",
       default="0:0:0:0",
       help="polynomial fisheye lens correction (n1:n2:n3:n4) e.g 0.5:-0.1:0.2:-0.0005")
  video_group.add_argument(
       "-v",
       "--view",
       action="store",
       dest="field_of_view",
       metavar="FIELD-OF-VIEW",
       default="0x0",
       help="Field of view for equi_mesh or full frame. e.g. 180x180 or 16x9")
  video_group.add_argument(
      "-1",
      "--force_v1_360_equi_metadata",
      action="store_true",
      help="Add v1 metadata as well as v2 metadata to the video.\n" 
      "This is only really valid for 360 equirectangular videos, but some video players only enable VR if they recognise v1 metadata")
  video_group.add_argument(
      "-u",
      "--mesh_uv",
      action="store",
      dest="uv_offsets",
      metavar="UV_OFFSETS",
      default="0:1:0:1:0:1:0:1",
      help="UV offset, needed when then fisheye images have padding in the video i.e.\n" 
      "the two fisheye images don't touch the edges and each other in the middle.\n" 
      "Should be a set of eight numbers ':' delimted\n"
      "\tu_min:u_scale:v_min:v_scale:u_min:u_scale:v_min:v_scale, where each value is a fraction of 1.0\n"
      "The first 4 number for the left eye, the second for the right eye\n"
      "e.g. for a 4000x8000 image, consider it being two 4000x4000 images,\n"
      "if both fisheye images are inset by 40 pixels all around then the parameter would be...\n\n"
      "0.01:0.98:0.01:0.98:0.01:0.98:0.01:0.98\n\n"
      "0.01 is the inset value on the left or top (40/4000), the image covers 0.98 of each half frame (4000 - (20 + 20))/4000\n"
      "if both fisheye images touch the left but have a 40 pixels gap between them\n"
      " and a 80 pixel padding top and bottom then the parameter would be...\n\n"
      "0.00:0.995:0.02:0.96:0.005:0.995:0.02:0.96\n\n"
      "0.00 is the inset value on the left the image covers 0.995 i.e. all bar 20 pixels of each half frame (4000 - (40 + 40))/4000\n"
      "The right hand image starts 20 pixels in so the u_min for the right eye is 0.005, the rest of the value match the left eye"
      )

  audio_group = parser.add_argument_group("Spatial Audio")
  audio_group.add_argument(
      "-a",
      "--spatial-audio",
      action="store_true",
      help=
      "spatial audio. First-order periphonic ambisonics with ACN channel "
      "ordering and SN3D normalization")
  parser.add_argument("file", nargs="+", help="input/output files")

  args = parser.parse_args()

  if args.inject:
    if len(args.file) != 2:
      console("Injecting metadata requires both an input file and output file.")
      return

    metadata = metadata_utils.Metadata()

    if args.stereo_mode:
      metadata.stereo = args.stereo_mode

    if args.projection:
      metadata.spherical = args.projection
      if metadata.spherical == "equirectangular":
          metadata.clip_left_right = 0 if args.degrees == "360" else 1073741823

    if args.spatial_audio:
      parsed_metadata = metadata_utils.parse_metadata(args.file[0], console)
      if not metadata.audio:
        spatial_audio_description = metadata_utils.get_spatial_audio_description(
            parsed_metadata.num_audio_channels)
        if spatial_audio_description.is_supported:
          metadata.audio = metadata_utils.get_spatial_audio_metadata(
              spatial_audio_description.order,
              spatial_audio_description.has_head_locked_stereo)
        else:
          console("Audio has %d channel(s) and is not a supported "
                  "spatial audio format." % (parsed_metadata.num_audio_channels))
          return


    if args.fisheye_correction:
        metadata.fisheye_correction = [float(x) for x in args.fisheye_correction.split(':')]

    if args.uv_offsets:
        metadata.uv_offsets = [float(x) for x in args.uv_offsets.split(':')]

    if args.field_of_view:
      metadata.fov = [float(x) for x in args.field_of_view.split('x')]
      if metadata.fov[0] == 0 or metadata.fov[1] == 0 :
        if args.projection == "full-frame" :
           metadata.fov[0] = 16.0
           metadata.fov[1] = 9.0       
        else :
           metadata.fov[0] = 180 
           metadata.fov[1] = 180;       

    if args.force_v1_360_equi_metadata:
      console("generating metadata.")
      metadata.v1_xml = metadata_utils.generate_spherical_xml(args.stereo_mode)
      console(metadata.v1_xml)

    if metadata.stereo or metadata.spherical or metadata.audio:
      metadata.orientation = {"yaw": args.yaw, "pitch": args.pitch, "roll": args.roll}
      metadata_utils.inject_metadata(args.file[0], args.file[1], metadata,
                                     console, args.force_v1_360_equi_metadata)
    else:
      console("Failed to generate metadata.")
    return



  if len(args.file) > 0:
    for input_file in args.file:
      if args.spatial_audio:
        parsed_metadata = metadata_utils.parse_metadata(input_file, console)
        metadata.audio = metadata_utils.get_spatial_audio_description(
            parsed_metadata.num_channels)
      metadata_utils.parse_metadata(input_file, console)
      metadata_utils.show_atoms(input_file, console)
      
    return

  parser.print_help()
  return


if __name__ == "__main__":
  main()
