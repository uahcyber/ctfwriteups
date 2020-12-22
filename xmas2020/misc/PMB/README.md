# X-MAS CTF 2020 

### Solver: Will Green ([Ducky] (https://github.com/wlg0005)) 
### Challenge: PMB 
### Category: Misc 

## Description: 

![](PMB%20Writeup.001.png)

## Walkthrough: 

Connecting to the target greets us with a cool “hacker-friendly” bank terminal 

![](PMB%20Writeup.002.png)

The option for opening an account is automatically chosen for us so we’re asked to input an interest rate with the only limitation being that its modulus (absolute value) is less than 100. 

So what happens if we just enter a number? 

![](PMB%20Writeup.003.png)

Unfortunately, as the description stated, law enforcement yoinks all of our funds :( 
Ok, so what if we enter a floating point number instead of an integer?  

![](PMB%20Writeup.004.png)

Same thing occurs.. So since the terminal explicitly tells us we can use *any* number, I decided to do a simple google search to remind myself of the numeric types within Python: 

![](PMB%20Writeup.005.png)

Oh! Let’s try a big complex number whose modulus is less than 100: 

![](PMB%20Writeup.006.png)

### Flag: X-MAS{th4t\_1s\_4n\_1nt3r3st1ng\_1nt3r3st\_r4t3-0116c512b7615456} 
