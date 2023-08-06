.. _admin:

NAME
====

 **GENOCIDE** - it's done.

SYNOPSIS
========

 genocide \<cmd\> \[key=value\] \[key==value\] 

DESCRIPTION
===========

 **GENOCIDE** provides a IRC bot that can run as a background daemon for 24/7
 day presence in a IRC channel. You can use it to display RSS feeds,
 act as a UDP to IRC gateway, and program your own commands for.

 GENOCIDE runs as a single channel bot and is 
 programmable with your own commands, which makes it suitable for server
 administation and can serve rss feeds to the channel.

 GENOCIDE stores it's data as JSON files  on disk, every object is timestamped,
 readonly of which the latest is served to the user layer. File paths have the
 type included so reconstructing from json file is made easy.

 GENOCIDE is intended to be programmable in a static, only code, no popen,
 no imports and no reading modules from a directory, way that **should** make
 it secure.
 

INSTALL
=======

 pip3 install genocide
    
CONFIGURATION
=============

 | cp /usr/local/share/genocide/genocide.service /etc/systemd/system
 | systemctl enable genocide --now

irc
===

 | genocide cfg server=<server> channel=<channel>
 | genocide cfg nick=<nick> 

 default channel/server is #genocide on localhost

sasl
====

  | genocide pwd <nickservnick> <nickservpass>
  | genocide cfg password=<outputfrompwd>

users
=====

  | genocide cfg users=True
  | genocide met <userhost>

rss
===

  | genocide rss <url>

