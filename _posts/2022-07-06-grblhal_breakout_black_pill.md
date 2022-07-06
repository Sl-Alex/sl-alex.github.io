---
layout: post
title: GrblHal breakout for black pill
description: A simple breakout board for black pill (F411 minimal board).
categories: HW
tags: USB grblHAL
author: Sl-Alex
readall: Here it is  
--- 

My open-source CNC step by step starts to work, so now it's time to share some info about the stepper board.
At the very beginning of the project I had to choose the board which will run grbl and after searching for a while I decided to use blackpill and grblHal.
I'd say, this decision hit the spot. [GrblHAL project](https://github.com/grblHAL) is constantly evolving, main developer introduced new features, that are extremely useful.
The only thing was missing: the breakout board for blackpill with isolated inputs.




{% include image.html url="/assets/2022-07-06-grblhal_breakout_black_pill/pinout.webp" description="Here is how it looks like" %}

The board is compatible with the default grblHAL black pill mpin mapping. The schematic is really simple: 12 inputs (4 of them are not used, so can be connected to any blackpill pin manually), 17 outputs (6 are not used at the moment).
Here is how the input is implemented:

{% include image.html url="/assets/2022-07-06-grblhal_breakout_black_pill/input.png" description="Sample isolated input" %}

Please pay attention that the optocoupler is powered by 5V and the output of the optocoupler divides it to roughly 3.3V.

Here is how the output is implemented:

{% include image.html url="/assets/2022-07-06-grblhal_breakout_black_pill/output.png" description="Sample output" %}

All outputs provide 12V, so be careful connecting step motor drivers without any current limiting circuit. Some drivers have just one resistor in series with the optocoupler LED, others have a bit more complex constant current circuits, like this:

{% include image.html url="/assets/2022-07-06-grblhal_breakout_black_pill/ConstantCurrent.png" description="Constant current circuit" %}

Most of the drivers without the constant current circuit expect 5V input, so adding a resistor in series with the driver input would be a good solution. As an alternative, 5V power supply could be used for the output part.