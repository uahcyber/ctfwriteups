# Tenable CTF 2021

### Solver: Will Green ([Ducky](https://github.com/wlg0005))
### Challenge: A3S Turtles
### Category: Stego

## Description:
#### [250 pts]: Turtles all the way down. (File: turtles128.zip)

## Walkthrough:

This was an interesting steganography challenge that required a little bit of everything: Password cracking, scripting, and even some Encryption

Upon trying to open the given ZIP file, I realized that it was actually protected by a password:

![](A3S%20Turtles%20Writeup.001.png)

I tried some easy passwords like `Password`, `Tenable`, `A3S`, `Turtles`, etc. None of these worked so I assumed that I would need to crack the ZIP password. I switched over to my laptop running ParrotOS and ran `zip2john` on the zip file like so:

`zip2john turtles128.zip > turtles128.hash`

This generated a hash which I then fed to John the Ripper:

`john --wordlist=/usr/share/wordlists/rockyou.txt turtles128.hash`

`john --show turtles128.hash`

This revealed the password to be `0` for `turtles128.zip`. Cool, let's extract the contents of the zip file. Doing so, we get another ZIP file named `turtles127.zip` which is also password protected. Running the same commands on `turtles127.zip`, reveals the password to also be `0` for this ZIP file. Extracting it we get `turtles126.zip`. 

Oh boy, nested ZIP files! This presumably goes all the way down to 0 or 1 which is a lot of passwords to crack by hand so there has to be some trick, right? If we try to extract `turtles126.zip` with a password of `0`, we get an incorrect password error. Cracking `turtles126.zip` reveals the password to be `1` this time. Hm.. interesting..

I cracked the first 4 or 5 files by hand during the competition and each time the password seemed to be either `0` or `1` which screams binary data. But this is obviously a lot of work to do by hand, so I crafted a Python script to do it for me:

```python
from zipfile import ZipFile

# base file name
file = "turtles"

# file number
num = 128

# list to store the binary values
binary = []

# while there are still zip files to extract
while True:
    
    # open the current zip file
    with ZipFile(file+str(num)+".zip") as zf:
        try:
            # try to extract with a password of 1
            # and append "1" to the binary list
            zf.extractall(pwd=b'1')
            binary.append("1")
        except:
            # if 1 doesn't work, extract with a password
            # of 0, and append "0" to the binary list
            zf.extractall(pwd=b'0')
            binary.append("0")

    # decrement num by 1 for the next zip file name
    num -= 1

    # if num == 0, we've extracted all of our zip files
    if num == 0:
        break

# write all of the binary data to a file named data
with open("data","w") as f:
    f.write(" ".join(binary)
```

This generated a file that I named `data` which contained the password for each file (binary data):
![](A3S%20Turtles%20Writeup.002.png)

As well as revealed a file named `key.png`, which was extracted from the last zip file, which looked like this:
![](A3S%20Turtles%20Writeup.003.png)

Hm.. so we have some binary data and a key which most likely means that this data is encrypted somehow. I had recently solved a challenge that involved a Multibyte XOR cipher so, out of instinct from seeing the key, that was the first thing I tried. This did not lead me anywhere and I was confused for a little bit.

Taking a step back from everything, I realized what the challenge name was hinting at: A3S = AES!

Let's use CyberChef to AES decrypt the data with the following settings:
![](A3S%20Turtles%20Writeup.004.png)

Doing so reveals the flag:

![](A3S%20Turtles%20Writeup.005.png)

Nice! Very cool challenge.

### Flag: flag{steg0_a3s}