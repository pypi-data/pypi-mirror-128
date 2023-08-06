# ACE Server

## How to use server files
1. Locate the machine where documents are served for editing
2. Install interpreter `python3` and module `aceditor`
3. Install and configure `apache` for python CGI
4. Copy `./ACE` to `apache` host document root
    - `cp /usr/local/lib/python3.6/site-packages/aceditor/example/server/ACE /var/www/html`
5. Change related file/directory permissions
    - `chmod -R 755 /var/www/html/ACE`
    - `chown www-data:www-data /var/www/html/ACE`
6. Configure `api.py`
    - `DOCUMENT_ROOT = "/mnt/myshare"`
    - `authentication = implement_your_own_method`
      - Learn more at [/pythoncgi/pythoncgi/example/user_authentication.py](/pythoncgi/pythoncgi/example/user_authentication.py)
7. Test it at `POST http://127.0.0.1/ACE/api.py`

## How to use client files
1. Same as setting an ACE client
2. Put client files under `/var/www/html/ACE`
3. `api_url` in `./script.js` can remain unchanged
4. Test it at `http://127.0.0.1/ACE/index.html`
