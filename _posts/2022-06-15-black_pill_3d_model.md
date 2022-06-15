---
layout: post
title: Black pill F4xx 3D model
description: Editable 3D model of the "Black Pill" F4xx board.
categories: 3D
tags: OpenSCAD
author: Sl-Alex
image: 2022-06-15-black_pill_3d_model/proof_pic.png
readall: Read more and get the model 
--- 

People working in modern EDAs like KiCAD or Altium know that having a 3D view of the PCB is really a killer feature. What can be better than drinking a cup of coffee and having a final look at your nice board before sending it to the factory? And what can be more annoying than an empty space instead of some fancy components? When I started developing my custom breakout for black pill running grblHAL FW, I was missing a black pill 3D model. I know there are some on the Internet, but I'll not give any links here because they are published in a mesh form, without any source code. So, I decided to create my own model.




My favourite scriptable CAD is OpenSCAD, so I did everything there. Here is how the final 3D model looks like:

{% include image.html url="/assets/2022-06-15-black_pill_3d_model/proof_pic.png" description="Black pill F4xx 3D model" %}

If you want to download it now - take it [here][zip].

It consists of several components, like PCB, silk screen, MCU, LEDs, crystals and connectors. Some components are in separate files, some are embedded in the main file. All of them are easily editable and configurable, so feel free to use all of them in your own open-source hardware.

[zip]: /attachments/2022-06-15-black_pill_3d_model/black_pill.zip 