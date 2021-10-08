---
layout: post
title: HD44780 and WS0010&#58; universal initialization
description: A simple and universal 4-bit initialization sequence.
categories: Embedded
tags: LCD OLED
author: Sl-Alex
image: 2021-10-08-universal_initialization_of_hd44780_and_ws0010_displays/proof_pic.jpg
--- 

Most of character displays are based on HD44780 or another compatible controller, e.g. KS0066. The
initialization sequence is normally the same for all of them. Unfortunately, OLED character displays
are not 100% compatible. They are based on WS0010 (or similar) controller and this controller has a bit
different set of commands. I'm not sure about 8-bit mode (never used it), but in 4-bit mode old HD44780
initialization sequence simply does not work for WS0010. Fortunately there is a simple, reliable and
universal solution.



The first thing that comes to mind looks like this:

```cpp
void display_init(void)
{
    #ifdef DISPLAY_HD44780
    display_init_hd44780();
    #endif

    #ifdef DISPLAY_WS0010
    display_init_ws0010();
    #endif
}
```

This will definitely work, but requires rebuilding the project after replacing the display. Fortunately, there is another way:

```cpp
void display_init(void)
{
    // Initialize all pins to default values
    display_init_pins()

    // Send default HD44780 initialization commands (taken from BC1602 datasheet)
    display_send_nibble(0x3);
    display_send_nibble(0x3);
    display_send_nibble(0x3);
    display_send_nibble(0x2);

    // Send WS0010 bus reset commands
    display_send_nibble(0x0);
    display_send_nibble(0x0);
    display_send_nibble(0x0);
    display_send_nibble(0x0);
    display_send_nibble(0x0);

    // Continue with the common initialization
    display_send_nibble(0x02);  // 4-bit mode
    display_send_command(0x28); // 4-bit mode 2 lines
    display_send_command(0x08); // Turn off
    display_send_command(0x06); // Cursor moves to the right
    display_send_command(0x01); // Clear the display
    display_send_command(0x0C); // Turn on
}
```

From WS0010 point of view there is a bus reset during initialization (five 0x00 nibbles), while HD44780 just ignores it.

The result is below. WH1602B (VATN LCD) is on the left, REC001602E (OLED display) is on the right.

{% include image.html url="/assets/2021-10-08-universal_initialization_of_hd44780_and_ws0010_displays/proof_pic.jpg" description="Test circuit" %}

This initialization procedure works fine even if you reset your MCU while keeping the display powered.
I intentionally removed all delays in the sample code to get better focus on the commands. You can easily
add missing delays by comparing WS0010 and HD44780 specs and choosing the highest value.