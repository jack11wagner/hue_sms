1. Download ngrok —  Go to ngrok.com/download and download for Mac OS X.
    * Open Terminal type in:

    ->cd Downloads
    ->./ngrok http 5000

    * copy first Forwrding ngrok address  should look like: "http://275b58730cf9.ngrok.io"

2. Twilio Account setup
    * Get Trial Number
    * Add Webhook with ngrok address from above
    * Change HTTP POST to HTTP GET
3. Download Philips Hue App
    * Make sure computer is on same wifi as Philips Hub
    * Find Hub IP Address
    * Put IP Address in hue_controller.py

4. Download Homebrew
    * enter below in terminal:

        ->/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

5. Download and Start Redis Database
    * enter in terminal:

        ->brew install redis/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        $ redis-server
6. Run createRedis.py to initialize colors in Database

7. Change hue_controller.py line 31 to self.light = self.bridge.lights[0]
8. Run hue_flask.py and press hub button at same time
