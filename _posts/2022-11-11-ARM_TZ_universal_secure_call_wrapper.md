---
layout: post
title: ARM TZ universal secure call wrapper
description: How to create a universal wrapper for secure functions in ARM TrustZone MCUs.
categories: Embedded
tags: Assembler C
author: Sl-Alex
readall: Reveal the secret
--- 

In one of the projects I've been working on we had quite a lot of functions in the Secure world and the OS running in the Nonsecure world. The OS was preemptive and could interrupt any secure function, so we had to reserve a secure stack for each task in addition to the non-secure stack. Moreover, some of the secure functions were using the HW secure engine, so there was a need to serialize secure function calls. The easiest way would be to create a wrapper for each secure function:
```c
__attribute__((cmse_nonsecure_entry)) uint32_t SecureFunction(uint32_t param);

uint32_t NonSecureWrapper(uint32_t param)
{
    uint32_t ret;
    OS_LOCK_SECURE_MUTEX();
    ret = SecureFunction(param);
    OS_UNLOCK_SECURE_MUTEX();
    return ret;
}
```

This definitely can work, but imagine you have 100+ functions with different number of arguments and you need a quick and universal solution.



At some point you might think of creating a variadic wrapper, like this:
```c
uint32_t UniversalNonSecureWrapper(void *SecureFunctionPtr, ...);
```

The problem is that it is not possible to pass the variadic part containing secure function parameters to the secure function, because the number of parameters to pass and their types are not hardcoded. There can be from 0 to 4 parameters.

You might also think of using some preprocessor macros, but trust me - it will not work as intended.

Let's stop at this point and think which language doesn't care too much about the types (no, it's not Javascript!) and which language forces you to take care of everything? 

Of course, I'm talking about the Assembler. Don't afraid of it, it's really easy if you follow the ABI for your platform.
For ARM32 it is [here](https://github.com/ARM-software/abi-aa/tree/main/aapcs32). We would need to:

- Registers R0-R3 should be used to pass parameters to the function, R0-R1 should be used to return the result.
- If there are more than 4 parameters (it's not the case for secure functions), then they should put them on stack.
- Registers R0-R4 can be freely used, the rest should be saved before use.
- Restore registers R4-R7 if saved before
- Stack pointer should be set to the original value before we return from our assembler function
- Return from the function should be done using the return address stored in LR register

Here is how the final solution might look like:

```armasm
;// GNU Assembler treats all undefined symbols as external, no need to declare
.extern SecureCallerPreHook
.extern SecureCallerPostHook

;// Secure functions do not accept parameters passed on stack, so maximum 4 parameters (R0-R3) are allowed
;// R4 - Original fourth parameter
;// R5 - Function pointer
;// R6 - Original LR
;// R7 - Not used
SecureCaller:
        push {r4,r5,r6,r7}  ;// Save caller registers, we will use them here

        add r5, sp, #16     ;// Go back by 16 bytes, this is the address of the fourth original parameter (if any)
        ldr r4, [r5], #0    ;// Load original fourth parameter (if any)
        mov r5, r0          ;// Save the pointer to the secure function to call. In fact, it points to NSC
        mov r6, lr          ;// Save original LR

        ;// SP -= 16
        push {r1,r2,r3,r4}  ;// Save original function parameters

        bl SecureCallerPreHook ;// Call a NS function before calling secure function

        pop {r0,r1,r2,r3}   ;// Restore original function parameters to R0-R3
                            ;// NSC functions do not support passing parameters over stack
        blx r5              ;// Call the secure function by calling NSC
        push {r0,r1}        ;// Save return values

        bl SecureCallerPostHook  ;// Call a NS function after calling secure function

        mov lr, r6          ;// Restore original LR
        pop {r0,r1}         ;// Restore secure function result
        pop {r4,r5,r6,r7}   ;// Restore caller registers

        bx lr               ;// Return to LR
```

In C this function has the following prototype:
```c
uint64_t SecureCaller(void *SecureFunction, ...);
```

You can cast the return value to the type you need (either void or any 32/64-bit type).

```SecureCallerPreHook``` and ```SecureCallerPostHook``` can be declared in C as functions without any parameters returning void:
```c
void SecureCallerPreHook(void);
void SecureCallerPostHook(void);
```

This wrapper has been tested on ARM Cortex M33 with the TrustZone. The only issue is that C compiler can't give you any hints on how many parameters to feed to the SecureCaller, so be careful.