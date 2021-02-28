# Tenable CTF 2021

### Solver: Will Green ([Ducky](https://github.com/wlg0005))
### Challenge: Follow The Rabbit Hole
### Category: Web

## Description:
#### [100 pts]: Follow the rabbit hole and get the flag.
#### http://167.71.246.232:8080/rabbit_hole.php

## Walkthrough:

This was a nice challenge that highlighted the importance of knowing how to automate tasks using a scripting language like python or bash.

Navigating to the provided URL, we're presented with the following:

![](Follow%20The%20Rabbit%20Hole%20Writeup.001.png)

That is the only text on the page. Admittedly this had be confused for a little bit until I noticed the URL had changed from when we initially navigated to the page:

`http://167.71.246.232:8080/rabbit_hole.php?page=cE4g5bWZtYCuovEgYSO1`

Interesting, that page parameter looks to be about the same length as the random string of characters that we see on the page. So what happens if we take that data and supply it to the page parameter?

`http://167.71.246.232:8080/rabbit_hole.php?page=4O48APmBiNJhZBfTWMzD`

![](Follow%20The%20Rabbit%20Hole%20Writeup.002.png)

Ah, we're presented with similar but different information. You could continue doing this, but as you will soon see this would be quite the task to do by hand.

So it seems that each page contains 
1. Some number, possibly the order of each page 
2. Some hex data and 
3. The url for the next page

I am most comfortable in Python, so I decided to solve this challenge using it but this challenge could also be solved with Bash or really any other language.

I first started with crafting the following script:

```python
import requests

# base url
url = "http://167.71.246.232:8080/rabbit_hole.php?page="

# value of the page parameter
page = "cE4g5bWZtYCuovEgYSO1"

# Until we're out of pages
while True:
    # Navigate to the page
    r = requests.get(url+page)

    # Get the content of the page
    data = r.content

    # Decode so that we're dealing with UTF-8
    # and replace the newline characters so that it's all on one line
    data = data.decode().replace('\n',' ')

    # update the page variable with the next page
    page = data.split()[2]

    # Write all of the data to a file named data
    with open("data",'a') as f:
        f.write(str(data) + '\n')
```

This generates a file that I named `data` with all of the data from each page, which looks like this:

![](Follow%20The%20Rabbit%20Hole%20Writeup.003.png)

And as I said before, doing this by hand would be quite the task because this file is a whopping 1,582 lines long. 

Ok, so we have the data from each page, let's see if we can figure out what this hex data is supposed to be. Using ctrl + f and using this Regex: `^\[0,` 

Brief Regex explanation: 
- ^ = "Starts with"
- \\[ = escape the bracket to include it in our search, 
- 0, = number followed by comma so we don't get other numbers

we can extract the hex data for the actual first few pages just by updating 0 to 1, to 2, etc. Doing this for the first 4 pages we get: `89 50 4E 47` Let's decode that using [CyberChef](https://gchq.github.io/CyberChef/):

![](Follow%20The%20Rabbit%20Hole%20Writeup.004.png)

Cool, the hex data seems to make up a PNG file! Now all we have to do is write each byte of hex to a file, so I crafted a script to do that:

```python
# function to sort the data
def my_sort(line):
    # split the line and grab the first number (page number)
    val = int(line.split()[0][1:-1])
    return val

# list to store the bytes
img_bytes = []

with open("data",'r') as f:
    # read all of the lines in data
    lines = f.readlines()

    # sort the lines using my_sort function
    lines.sort(key=my_sort)

    # for each line
    for line in lines:
        # split the line and grab the hex value
        hex_val = line.split()[1][1:-2]
        # convert the hex value to a bytes object and append to img_bytes list
        img_bytes.append(bytes.fromhex(hex_val))

# create a file named rabbit_hole.png in a: append mode and b: binary mode
with open("rabbit_hole.png",'ab') as f1:
    # join all of the bytes in img_bytes together and write to the file
    f1.write(b''.join(img_bytes))
```

Running the script we get this image:

![](Follow%20The%20Rabbit%20Hole%20Writeup.005.png)

Indeed, it is!

### Flag: flag{automation_is_handy}
