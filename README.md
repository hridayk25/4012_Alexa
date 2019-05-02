# 4012_Alexa
To use the CFA ordering skill with Alexa:
1. Go to https://developer.amazon.com/alexa/console/ask and sign in using an Amazon Developer account
2. Click on _Create Skill_
3. Choose a skill name, choose _Custom_ as the model, choose _Provision your own_ as the method to host your skill's backend resources, and press _Create Skill_
4. Once created, scroll down and find _JSON Editor_ in the left toolbar
5. Inside _JSON Editor_, click on _Drag and drop a .json file_ and load the _skill.json_ file


To set up the backend server:
1. Download _ngrok_ and set up your account
2. In a shell, start ngrok with http settings on port 5500
3. In another shell, run _server.py_ and install any reported dependencies.
4. Once _server.py_ is running go to the Amazon skill and find the _Endpoint_ tab and select _HTTPS_
5. In your ngrok shell, copy the https address and paste it into the Default Region URL box.
6. Finally, select the wildcard certificate option in the Enpoint tab.
7. The skill should now be active on an Alexa attached to your developer account.
