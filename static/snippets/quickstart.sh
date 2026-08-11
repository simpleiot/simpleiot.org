# Download the release for your platform from
# https://github.com/simpleiot/simpleiot/releases

chmod +x simpleiot-vX.Y.Z-linux-x86_64
mv simpleiot-vX.Y.Z-linux-x86_64 siot
./siot

# Open http://localhost:8118 and log in with admin / admin.

# Run it as a systemd service (Linux):
sudo ./siot install

# Later, update in place:
siot update
