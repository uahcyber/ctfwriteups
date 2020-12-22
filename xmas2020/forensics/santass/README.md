# X-MAS CTF 2020 

### Solver: Will Green ([Ducky](https://github.com/wlg0005)) 
### Challenge: santass 
### Category: Forensics 

## Description: 

![](santass%20Writeup.001.png)

## Walkthrough: 

Opening up the pcap and scrolling through, it seems like pretty standard HTTP GET requests, most of which resulted in 404 Not Found. So let’s try exporting those http objects and see if there’s anything interesting: 

![](santass%20Writeup.002.png)

Wow, that’s a lot of files! Opening them up we can see that most of them are just the 404 Not Found error message for the GET requests, as expected: 

![](santass%20Writeup.003.png)

There are two files however named “santass.jpg” and “santass.jog” which contain the following text: 

![](santass%20Writeup.004.png)

This led me down a rabbit hole of running the usual forensics tools (e.g., exiftool, foremost, binwalk, etc.) And even comparing the two files since there was slight differences between the two. All of which led me nowhere. 

It took me quite some time, and a hint from the challenge author that suggested we play close attention to what can be imported, that I took a closer look at the filenames: 

![](santass%20Writeup.005.png)

There’s only three objects that don’t contain regular English text, so maybe if we combine them we can Base64 decode them? 

![](santass%20Writeup.006.png)

Sure enough! 

### Flag: X-MAS{ggwireshark} 
