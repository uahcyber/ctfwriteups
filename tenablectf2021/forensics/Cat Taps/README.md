# Tenable CTF 2021

### Solver: Will Green ([Ducky](https://github.com/wlg0005))
### Challenge: Cat Taps
### Category: Forensics

## Description:
#### [100 pts]: My cat has been using the computer a lot lately. I have no idea what a cat would use a computer for, but you might. (File: usb.pcap)

## Walkthrough:

Opening up the provided pcap file, we can see that this is not a packet capture of network traffic but rather it is a packet capture of USB traffic as the file name would suggest. I've analyzed USB traffic before in the [HTB x Uni 2020 Quals CTF](https://github.com/uahcyber/ctfwriteups/blob/master/hackthebox-uni-2020/forensics/Plug.pdf) but that particular challenge didn't require me to fully analyze keystrokes which, given the challenge name, is what I assumed I would have to do in this challenge.

Ok, so after doing some research and reading a few [writeups](https://abawazeeer.medium.com/kaizen-ctf-2018-reverse-engineer-usb-keystrok-from-pcap-file-2412351679f4) from previous ctfs, I was able to figure out the information I would need to solve this challenge:

#### 1. Determine which device we want to look at:

When a new device is plugged into a host computer, there are a few things that the host requests from the device to get as many details about the device as it feels it needs, so that it can eventually load the proper device driver. One of those requests is called "Get Device Descriptor" which contains information about the USB device as a whole. 

If we look at the traffic we can see the very first two packets are the descriptor request from the host to the device, and the devices response:
![](Cat%20Taps%20Writeup.001.png)

Cool, so let's take a look at that response packet to see what the host received from this device:
![](Cat%20Taps%20Writeup.002.png)

One could figure out the meaning of each field name just by googling, but for this challenge we really only need to look at the `idVendor` and `idProduct` fields. As we can see this is the device descriptor response from a Logitech G400 Optical Mouse. If we wanted to we could track the mouse location, but given the name of the challenge "Cat Taps" I'm assuming we're concerned with keystrokes.

Looking at the next device descriptor response we find this packet:
![](Cat%20Taps%20Writeup.003.png)

If we Google "Holtek Semiconductor, Inc." We can figure out that this company produces parts for keyboards and so this is most likely the device that we want to look at. Looking at the address for the device, we can determine that this is device 2:
![](Cat%20Taps%20Writeup.004.png)

#### 2. Extract the leftover data (keystrokes) from the device:

Cool, so we know which device we need to look at, now let's extract the keystrokes. We can use the following filter to look at only this device's traffic:

#### `usb.device_address == 2`

Doing so presents us with the following traffic:
![](Cat%20Taps%20Writeup.005.png)

As you can see, there are various descriptor requests and responses that setup the device for use, and then around 800 `URB_INTERRUPT in` packets if you continue scrolling. 

`URB_INTERRUPT in` packets are regularly scheduled IN or OUT transactions between the host and the USB device. These are the type of packets that mice and keyboards use to send data to the host. 

Looking at the screenshot above, you can see the `URB_INTERRUPT in` packets seem to alternate in length between 35 and 27. The packets that are longer contain the actual data that is being sent to the host from the device, while the shorter packets can be thought of as a confirmation from the host that it received the data.

The actual data for each keystroke can be found in the `Leftover Capture Data` field of each packet:
![](Cat%20Taps%20Writeup.006.png)

As you might have been able to guess, we are concerned with the third byte of each leftover capture data. This is the byte that contains the data for the actual keystroke in hex. There is a nice [document](https://www.usb.org/sites/default/files/documents/hut1_12v2.pdf) that contains the usage tables for USB HID (Human Interface Devices) which contains a table for keyboards:
![](Cat%20Taps%20Writeup.007.png)

Cool! We're just about done, we just need to extract all of the leftover data for each packet. We can apply the `Leftover Capture Data` field as a column in Wireshark and then export the packet dissections as a CSV. This will generate a CSV with all of the packets from our keyboard device, including the `Leftover Capture Data` column that we applied.

#### 3. Decode and win
Now all we have to do is craft a script to map each hex value to the table value, and output it to us:

```python
# Dictionary generated from table in the document linked above
table_map = {
2: "PostFail",
4: "a",
5: "b",
6: "c",
7: "d",
8: "e",
9: "f",
10: "g",
11: "h",
12: "i",
13: "j",
14: "k",
15: "l",
16: "m",
17: "n",
18: "o",
19: "p",
20: "q",
21: "r",
22: "s",
23: "t",
24: "u",
25: "v",
26: "w",
27: "x",
28: "y",
29: "z",
30: "1",
31: "2",
32: "3",
33: "4",
34: "5",
35: "6",
36: "7",
37: "8",
38: "9",
39: "0",
40: "Enter",
41: "esc",
42: "del",
43: "tab",
44: "space",
45: "_", # can also be - 
47: "{", # can also be [
48: "}", # can also be ]
56: "/",
57: "CapsLock",
79: "RightArrow",
80: "LetfArrow"
}

keys = [] # list to store the decoded keystrokes

# open the generated csv
with open("leftover.csv",'r') as f:
    lines = f.readlines() # read all lines

    # for each line in leftover.csv
    for line in lines:
        # split on each comma, and grab the leftover data column
        leftover = line.split(',')[6]
        try:
            # slice the leftover data column, grabbing only the 3rd byte
            # convert that value from hex to decimal, and grab the table_map
            # value that matches, and then append to the keys list
            keys.append(table_map[int(leftover[5:7],16)])
        except:
            continue

# join and print the data
print("".join(keys))
```

Running the above script we get this output:

`nnottepaadexeEnterohspacehhispaceyoouuspacefiigurredspaceitspaceooutspacegoodspacejjobspaceimmspacegonnaspacegoospaceaheeaadspaceandspacetyypespaceaaspaceffeewspacetthiinngsspacettoospacemakespacetthhisspacepprrettyyspaceannooyiingspacessospaceyoouuspacecantspacejusstspaceitspacedeldeldeldoospaceitspacemanuallyspaceookspacetthhaatsspaceenooughspaceflaag{usb_pcaps_arre_fun}cq`

Nice, we figured out what the cat was doing!

### Flag: flag{usb_pcaps_are_fun}

![](Cat%20Taps%20Writeup.008.gif)





