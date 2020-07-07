---
layout: post
title: Embedded C++ output size minimization
description: How to minimize C++ binary size
categories: Embedded
tags: C++ MCU
author: Sl-Alex
---

Embedded software developers normally prefer to use a pure C, however in some cases and especially in complex projects using C++ gives a more clear structured implementation.
Unfortunately, by default C++ compiler produces pretty big binaries. This can be acceptable in case of a normal OS with a big amount of memory, but things are getting complicated when it comes to microcontrollers.
I played a bit with compiler and linker options and it seems that the most size-consuming options CPP features are RTTI (run-time type information) and exceptions. I strongly believe that these are not things you can't live without.
So, I came up with the following configuration (valid for GCC toolchain):

### C++ compiler flags

| Flag            | Description                                    |
| :-------------- | :--------------------------------------------- |
| -fno-rtti       | (Don't generate run-time typed identification) |
| -fno-exceptions | (Don't catch exceptions)                       |

### Linker flags:   

| Flag            | Description                                    |
| :-------------- | :--------------------------------------------- |
| -flto           | (Use link time optimization)                   |
| -lstdc++        | Use C++ libraries. You use them, right?        |

Resulting binary size is pretty small and comparable with the equivalent C compiler output.
Of course, you can reduce the size even more, but flags above are the most effective.
