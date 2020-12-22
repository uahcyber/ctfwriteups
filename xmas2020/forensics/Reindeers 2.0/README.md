# X-MAS CTF 2020 

### Solver: Will Green ([Ducky](https://github.com/wlg0005))
### Challenge: Reindeers 2.0 
### Category: Forensics 

## Description: 

![](Reindeers%202.0%20Writeup.001.png)

## Walkthrough: 

We’re given the following image: 

![](Reindeers%202.0%20Writeup.002.png)

Since we’re just given an image, it seems this is some sort of steganography challenge. Running the usual tools (e.g., exiftool, foremost, binwalk, etc.) didn’t really lead me anywhere, so I began examining the actual image.  

I did notice that the RGB values for the color white on the left side of the image were strange in that each pixel had slightly different values from the white on the right side. This led me down a rabbit hole where I tried things such as decoding the hex values for each color, generating a color histogram, image noise analysis, and a few other things all of which didn’t really lead me anywhere. 

Eventually the hint above was posted which I figured referred to the language GO. Searching on Github for steganography tools that are programmed in GO introduced me to a tool called Stegify: 

![](Reindeers%202.0%20Writeup.003.png)

After downloading and reading the documentation on Github, I was able to execute the following command: 

`stegify decode --carrier “North Pole.png” --result result` 

Doing so generates a file called result. Let’s try running the file command on it: 

![](Reindeers%202.0%20Writeup.004.png)

It seems there was a ZIP file hidden in the image. Progress! Let’s change the file extension and unzip it: 

![](Reindeers%202.0%20Writeup.005.png)

Cool, it extracted two images, but it seems that one file failed to extract?  

![](Reindeers%202.0%20Writeup.006.png)

During the competition I was able to get the third image to extract by fixing the header of zip file, but this turned out to not be necessary to actually solve the challenge. The header contained a DOS MZ header: 

![](Reindeers%202.0%20Writeup.007.png)

Simply replacing the MZ with PK (the header of a ZIP file), allowed me to extract the third image: 

![](Reindeers%202.0%20Writeup.008.png)

But as I said this was not necessary. I again performed the standard steganography tools, and exiftool revealed the flag in the metadata of r2.png: 

![](Reindeers%202.0%20Writeup.009.png)

It looks like it’s been encoded using a rotation cipher of some sort, let’s try ROT-13 first: 

![](Reindeers%202.0%20Writeup.010.png)

Nice! 

### Flag: X-MAS{4hh\_y0u\_g0t\_m3\_in\_th3\_v3ry\_3nd} 
