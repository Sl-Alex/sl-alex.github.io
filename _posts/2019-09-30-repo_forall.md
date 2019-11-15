---
layout: post
title: Show project name using "repo forall" alias
categories: Linux
tags: repo
author: Sl-Alex
---

Repo is a wonderful tool which simplifies my daily work across multiple Git repositories.
One of the most useful commands in my opinion is ```repo forall```.
However, it does not show project name before performing a command on a specific repository.
There is a ```-p``` parameter, which does exactly what I need, but some part of the output seems to be missing (at least in my case with 50+ repositories).
After playing a bit around command-line parameters I came up with a simple solution. Just add the following to your bash alias list:
``` bash
repo_forall () { repo forall -c "echo -e \"\\e[32m\"\$REPO_PROJECT\"\\e[39m\"; $@" ;}
```
After that just pass the command to this function:
``` bash
repo_forall "git branch"
```
Here is a sample output:

![Sample usage](/assets/repo_forall.png)
