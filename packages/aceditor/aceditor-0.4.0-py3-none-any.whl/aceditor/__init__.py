__version__ = "0.4.0"
__keywords__ = ["ace editor js python cgi apache"]


if not __version__.endswith(".0"):
    import re
    print("version {} is deployed for automatic commitments only".format(__version__), flush=True)
    print("install version " + re.sub(r"([0-9]+\.[0-9]+\.)[0-9]+", r"\g<1>0", __version__) + " instead")
    import os
    os._exit(1)


import os
print("See example at", os.path.join(os.path.dirname(os.path.abspath(__file__)), "example"))

