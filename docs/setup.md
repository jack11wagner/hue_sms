1. Download ngrok —  Go to ngrok.com/download and download for Mac OS X.
    In the terminal, go to the directory where ngrok is located and then type the following
    ->./ngrok http 5000

    * copy first Forwarding ngrok address  should look like: "http://275b58730cf9.ngrok.io"

2. Twilio Account setup
    * Get Trial Number
    * Add Webhook with ngrok address from above
    * Change HTTP POST to HTTP GET
3. Download Philips Hue App on Cellular Device
    * Make sure device is on same wifi as Philips Hub 
         - You want to be connected to MC Wireless first and then search for CSlabWPA2 wifi network
         - Password: This is the K3Y for th3 CS l@b!
    * Find Hub IP Address located in the app under settings and then click hue bridges and IP-address should be at the bottom
    * Put IP Address in hue_controller.py

4. Download Homebrew
    * go to their site here and follow directions 
      -> https://brew.sh
5. Download and Start Redis Database
    * enter in terminal:

        ->brew install redis/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        $ redis-server
6. Run createRedis.py to initialize colors in Database

8. Run hue_flask.py and press hub button at same time
9. Run plotlydash.py and click generated link for pie chart of entries
