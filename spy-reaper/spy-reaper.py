# Author Jamiel, Tyler, and Michael.
import sys
import os
from distutils.version import StrictVersion, LooseVersion
from platform import python_version

# System sanity checks
python_version_req = StrictVersion("3.1")
if StrictVersion(python_version()) < python_version_req:
    sys.stderr.write("Python 3.1 or greater is required.\n")
    sys.exit(1)
if os.name == "nt":
    alternate_path = "C:\\TWS API\\source\\pythonclient"
else:
    alternate_path = "/opt/twsapi/pythonclient"

try:
    import ibapi
except ImportError:
    try:
        sys.path.append(alternate_path)
        import ibapi
    except ImportError:
        sys.stderr.write("twsapi 973.05 must be installed under a system path or '{0}'\n".format(alternate_path))
        sys.exit(1)

tws_api_ver = StrictVersion(ibapi.get_version_string())
tws_req_ver = StrictVersion("9.73.2")

if tws_api_ver != tws_req_ver:
    sys.stderr.write("twsapi version '{0}' required, version installed is '{1}'\n".format(tws_req_ver, tws_api_ver))
    sys.exit(1)
                
# Import our modules
script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(script_dir + "/../lib/")
from client import ClientApp

def main():
    # Connect to the paper account port
    port = 7497

    client_app = ClientApp()
    sys.stderr.write("Connecting to TWS on port '{0}'.\n".format(port))
    client_app.connect("127.0.0.1", port, clientId=0)
    sys.stderr.write("serverVersion:{0}\nconnectionTime:{1}\n".format(client_app.serverVersion(), client_app.twsConnectionTime()))
    sys.stderr.write("Handling incoming messages.\n")
    server_ver_req = LooseVersion("124")
    server_ver = LooseVersion(str(client_app.serverVersion()))
    if server_ver < server_ver_req:
        sys.stderr.write("Server version required is '{0}', server version installed '{1}' \n".format(server_ver_req, server_ver))
        sys.exit(1)
    client_app.run()
    

if __name__ == "__main__":
    main()
