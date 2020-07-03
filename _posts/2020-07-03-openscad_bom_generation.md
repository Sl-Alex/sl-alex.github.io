---
layout: post
title: Automatic BOM creation in OpenSCAD
categories: 3D
tags: OpenSCAD, Python
author: Sl-Alex
---
# Background
After many days of playing around with free 3D CADs I've ended up with the old good OpenSCAD, which combines a high level of flexibility with low system requirements.
However, it lacks some features, e.g. the bill of materials and this is exactly what I'm going to do.
After analyzing different possibilities I came to a conclusion that the simplest way may look like this:
1. Inject a special string to a log, something like "BOM_ITEM: part_name".
2. Start OpenSCAD in a console mode, grep its output and calculate how many BOM items of each part name are there.

**_TL;DR_**
> Add this to your OpenSCAD project: [bom.scad](/attachments/bom.scad)
>
> Generate BOM using this: [generate_bom.py](/attachments/generate_bom.py)




# Injecting a string
This is the easiest part, just create a "bom.scad" with the following content:
```scad
module bom_item(name)
{
    echo(str("BOM_ITEM: ", name));
}
```

Then add the following line to each of parts you are using:
```scad
bom_item("part_name");
```

If you have a parameterizable part you can include your parameters to the part name in the following way:
```scad
bom_item(str("sfu1605_", length));
```
That's it for the preparation, all parts will be in the log and now we're ready to count them:

# Calculating
The easiest way to get the log and to parse it is to use Python. The implementation is pretty straightforward:
- Run OpenSCAD and grab its output.
- Find a "BOM_ITEM" mark and extract the part name placed after it.
- Increment the number of parts with this name.
- Proceed till the end of the output.

Here is the script, [generate_bom.py](/attachments/generate_bom.py), you can run it like this:
```shell
generate_bom.py my_complex_assembly.scad
```
Sample output:
```
Generating BOM...
Calculating...
#########################
bf12: 3
bk12: 3
m6x35_screw_lens_hex: 6
m6x45_screw_lens_hex: 6
motor: 3
motor_holder_x: 1
motor_holder_y: 1
motor_holder_z: 1
plate_x_508x450x10: 1
plate_y_290x190x10: 1
plate_z_260x190x10: 1
profile_30x30x230: 2
profile_30x60x330: 2
profile_30x60x500: 2
profile_30x60x508: 4
profile_30x60x510: 2
sfu1605_250: 1
sfu1605_450: 1
sfu1605_500: 1
sfu1605_nut: 3
sfu1605_nut_housing: 3
shaft_16x250: 2
shaft_8x60: 1
shaft_coupling_spider_8x10: 3
sk16: 4
```