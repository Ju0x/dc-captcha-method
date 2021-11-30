<h1>Discord Captcha Method</h1>
<h4>This is an example, of a verification trough a check, if the user loads the picture send with the verification-message.
This makes it possible to tell if the user uses a client or an automated script. Please note that this can not detect 100% whether the user uses the discord client or an automated script.</h4>

<h1>Explanation</h1>
<p>When a user is loading an image on discord, the image will be requested by the Google CDN. But if the verification is performed by an automated script, that isn't using the Client, than the image won't be loaded in the most cases. Basically, the image gets an identifier to the URL, to tell if the user loaded the picture. Please add an IP-Check, if you want to use this method, to check if the IP is from the Google CDN.</p>

> <h3>This example is only EXPERIMENTAL. I cannot ensure, if this will work.</h3>
