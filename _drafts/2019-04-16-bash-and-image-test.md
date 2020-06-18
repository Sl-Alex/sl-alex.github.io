---
layout: post
title: Markdown test
categories: Test
tags: test markdown
author: Sl-Alex
---

You can write regular [markdown](http://markdowntutorial.com/) here and Jekyll will automatically convert it to a nice webpage.  I strongly encourage you to [take 5 minutes to learn how to write in markdown](http://markdowntutorial.com/) - it'll teach you how to transform regular text into bold/italics/headings/tables/etc.




**Here is some bold text**

## Here is a secondary heading

Here's a useless table:

| Number | Next number | Previous number |
| :------ |:--- | :--- |
| Five | Six | Four |
| Ten | Eleven | Nine |
| Seven | Eight | Six |
| Two | Three | One |


How about a yummy crepe?

![Crepe](https://s3-media3.fl.yelpcdn.com/bphoto/cQ1Yoa75m2yUFFbY2xwuqw/348s.jpg)

Here's a code chunk:

~~~
var foo = function(x) {
  return(x + 5);
}
foo(3)
~~~

And here is the same code with syntax highlighting:

Javascript:
```javascript
var foo = function(x) {
  return(x + 5);
}
foo(3)
```

OpenSCAD:
```scad
module bom_item(name)
{
    echo(str("BOM_ITEM: ", name));
}
```

VHDL code:

```vhdl
-- add_g.vhdl

library IEEE;
use IEEE.std_logic_1164.all;

entity add_g is
  generic(left : natural := 31;         -- top bit
          prop : time := 100 ps);
    port (a    : in  std_logic_vector (left downto 0);
          b    : in  std_logic_vector (left downto 0);
          cin  : in  std_logic;
          sum  : out std_logic_vector (left downto 0);
          cout : out std_logic);
end entity add_g;

architecture behavior of add_g is
begin  -- behavior
  adder: process
           variable carry : std_logic; -- internal
           variable isum : std_logic_vector(left downto 0);  -- internal
         begin
           carry := cin;
           for i in 0 to left loop
             isum(i) := a(i) xor b(i) xor carry;
             carry  := (a(i) and b(i)) or (a(i) and carry) or (b(i) and carry);
           end loop;
           sum  <= isum;
           cout <= carry;
           wait for prop;   -- signals updated after prop delay
         end process adder;
end architecture behavior;  -- of add_g
```
