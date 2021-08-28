#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Based on work with the following copyright
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


SPHERICAL_UUID_ID = (
    b"\xff\xcc\x82\x63\xf8\x55\x4a\x93\x88\x14\x58\x7a\x02\x52\x1f\xdd")

# XML contents.
RDF_PREFIX = " xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" "

SPHERICAL_XML_HEADER = \
    "<?xml version=\"1.0\"?>"\
    "<rdf:SphericalVideo\n"\
    "xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n"\
    "xmlns:GSpherical=\"http://ns.google.com/videos/1.0/spherical/\">"

SPHERICAL_XML_CONTENTS = \
    "<GSpherical:Spherical>true</GSpherical:Spherical>"\
    "<GSpherical:Stitched>true</GSpherical:Stitched>"\
    "<GSpherical:StitchingSoftware>"\
    "Spherical Metadata Tool"\
    "</GSpherical:StitchingSoftware>"\
    "<GSpherical:ProjectionType>equirectangular</GSpherical:ProjectionType>"

SPHERICAL_XML_CONTENTS_TOP_BOTTOM = \
    "<GSpherical:StereoMode>top-bottom</GSpherical:StereoMode>"
SPHERICAL_XML_CONTENTS_LEFT_RIGHT = \
    "<GSpherical:StereoMode>left-right</GSpherical:StereoMode>"

SPHERICAL_XML_FOOTER = "</rdf:SphericalVideo>"
