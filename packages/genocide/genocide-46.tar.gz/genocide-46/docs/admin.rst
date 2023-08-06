.. _admin:

admin
#####

**GENOCIDE** provides a IRC bot that can run as a background daemon for 24/7
day presence in a IRC channel. You can use it to display RSS feeds,
act as a UDP to IRC gateway, and program your own commands for.

NAME
====

 **GENOCIDE** - king netherlands commits genocide.

SYNOPSIS
--------

 ``genocidectl <cmd> [key=value] [key==value]``

DESCRIPTION
-----------

 **GENOCIDE** is a python3 program that holds evidence that the king of the
 netherlands is doing a genocide, a written response where the king of
 the netherlands confirmed taking note of “what i have written”, namely
 proof that medicine he uses in treatement laws like zyprexa, haldol,
 abilify and clozapine are poison. Poison that makes impotent, is both
 physical (contracted muscles) and mental (let people hallucinate) torture
 and kills members of the victim groups.

INSTALL
-------

 ``pip3 install genocide``
    
CONFIGURATION
-------------

 | ``cp /usr/local/share/genocide/genocide.service /etc/systemd/system``
 | ``systemctl enable genocide --now``

irc
---

 | ``genocidectl cfg server=<server> channel=<channel>``
 | ``genocidectl cfg nick=<nick>``

default channel/server is #genocide on localhost

sasl
----

 | ``genocidectl pwd <nickservnick> <nickservpass>``
 | ``genocidectl cfg password=<outputfrompwd>``

users
-----

 | ``genocidectl cfg users=True``
 | ``genocidectl met <userhost>``

rss
---

 | ``genocidectl rss <url>``

SEE ALSO
--------

 | ``/usr/local/share/genocide``
 | ``/usr/local/share/doc/genocide``
 | ``/usr/local/share/man/man1/genocide.1.gz``
