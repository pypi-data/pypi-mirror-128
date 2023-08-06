# ACE Client

## How to use client files
1. Download ACE builds
    - [https://github.com/ajaxorg/ace-builds](https://github.com/ajaxorg/ace-builds)
    - Copy one of the `src` next to the client files
2. Configure ACE server in `./script.js`
    - `var api_url = "http://my.server/ACE/api.py";`
3. Open web browser.
    - Local
        - Open `index.html` in web browser directly.
            - `file:///C:/aceditor/aceditor/example/client/index.html`
        - ACE server must allow cross origin requests
    - Remote
        - Visit the URL where the client files are served.
            - `http://my.server/ACE/index.html`
        - Learn more at [../server/](../server/)
    
