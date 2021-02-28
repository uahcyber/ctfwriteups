# Tenable CTF 2021

### Solver: Will Green ([Ducky](https://github.com/wlg0005))
### Challenge: Look at all the pixels, where do they all come from?
### Category: Stego

## Description:
#### [125 pts]: Maybe there is something hidden in this picture? (File: pip.png) 

## Walkthrough:

This was a pretty cool steganography challenge that actually had a lot fewer solves during the competition than I expected. Opening up the provided PNG file we're presented with the following:

![](look%20at%20all%20the%20pixels.001.png)

Interesting.. just looks like a bunch of noise. Since the challenge title tells us to look at the pixels, let's do that!

Opening up the PNG file in GIMP (or any other image manipulation program, e.g., Photoshop), we can zoom in to look at each individual pixel:

![](look%20at%20all%20the%20pixels.002.png)

Interesting, it does seem that each pixel is a distinct color with no real relation to the pixels around them. Perhaps the hex values for each color represent something? Let's grab the hex values of the first few couple pixels using the color picker tool:

![](look%20at%20all%20the%20pixels.003.png)

Alright, so we have the hex values `89504e` and `470d0a`, let's throw those into CyberChef to decode them real quick:

![](look%20at%20all%20the%20pixels.004.png)

Oh nice, that looks like the header for another PNG file!

So it seems that each pixel's hex value represents 3 bytes of another PNG file. So we need some automated way to extract the hex value of each pixel and then write the bytes to a file. We can use the Python Imaging Library (PIL) to help us with that, and craft something like this:

```python
from PIL import Image

# convert RGB values (tuple) to hex
def rgb2hex(val):
    r = hex(val[0])[2:].zfill(2)
    g = hex(val[1])[2:].zfill(2)
    b = hex(val[2])[2:].zfill(2)
    hexd = bytes.fromhex((r + g + b)) 
    
    return hexd

# open pip.png (given)
img = Image.open("pip.png",'r')

# get the RGB values for each pixel
vals = list(img.getdata())

# convert each pixels RGB values to hex
data = [rgb2hex(x) for x in vals]

# write each byte of hex data into a file called decoded.png
with open('decoded.png','wb') as f:
    f.write(b''.join(data))
```

Running the script we get the following image as output:

![](look%20at%20all%20the%20pixels.005.png)

Very cool!

### Flag: flag{p1ctur3_in_picture}