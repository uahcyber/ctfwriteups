﻿# X-MAS CTF 2020 

### Solver: Will Green ([Ducky](https://github.com/wlg0005)) 
### Challenge: Bobi’s Whacked 
### Category: Misc 

## Description: 

![](Bobi's%20Whacked%20Writeup.001.png)

## Walkthrough: 

This challenge confused me at first because, unlike the majority of the other challenges, nothing was linked. After solving some other challenges, I realized that this is probably some sort of OSINT challenge. A simple google search of the challenge name takes us to the challenge author’s YouTube channel: 

![](Bobi's%20Whacked%20Writeup.002.png)

Some searching around and we find an interesting string in the About section: 

![](Bobi's%20Whacked%20Writeup.003.png)

Lets throw that in CyberChef and Hex decode it: 

![](Bobi's%20Whacked%20Writeup.004.png)

“middlepart”, interesting.. 

At first I thought this might be referring to the middle part of a video or maybe the middle video in the channel history? Nope. It admittedly took me way too long to connect the challenge description with the solution: “Warm socks and warm wine, so the caption said.” Let’s see if there’s any videos with captions! 

![](Bobi's%20Whacked%20Writeup.005.png)

YouTube kindly shows us that there’s only two videos on his channel with captions enabled. You could go through both videos and find the captions, but surely there’s a better way? My teammate [dayt0n](https://github.com/dayt0n), suggested I take a look at a program called youtube-dl, which worked perfectly. 

Using youtube-dl we can download all subtitles/captions: 

`youtube-dl --all-subs --skip-download [video link]`

Opening up the two files generated by youtube-dl we reveal the remaining parts of the flag: 

![](Bobi's%20Whacked%20Writeup.006.png)

Combining everything with the “middlepart” string we get the flag, nice! 

### Flag: X-MAS{nice\_thisisjustthefirstpartmiddlepart\_congrats} 
