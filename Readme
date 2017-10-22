Trendiest
---------


Trendiest is a simple daemon that watches directories and manages a symlink named 'latest' which always points to the most recently modified file in the directory. This is useful for pointing at your Downloads or screenshots folder.


Examples:
---------


```
# Download powerpoint presentation

libreoffice ~/Downloads/latest
```


```
# Take screenshot

feh ~/Pictures/latest
```

```
# insert usb stick
# Download ubuntu iso 
sudo dd if=~/Downloads/latest of=/dev/sdb # Probably don't actually do this
```


Details
-------

Trendiest uses inotify to get file events. It fires once the file has been closed for writing. It uses a new symlink and a move operation to atomically replace the target symlink. There shouldn't be any race conditions but YMMV.


Installation
------------

Unfortunately, the state of inotify python libraries is not great. There is an old unmaintained version packaged for debian, and a new unpackaged version on pypi. My solution to this is to create a virtualenv for the daemon and run it out of there with systemd.



```
cd local
git clone https://github.com/nibalizer/trendiest
cd trendiest/
virtualenv --python=python3 venv
source venv/bin/activate
pip install -r requirements.txt 
cp example_config.yaml config.yaml
vim config.yaml # make whatever modifications
vim contrib/trendiest.service # make whatever modifications to make yours work
sudo cp contrib/trendiest.service /etc/systemd/system/
systemctl daemon-reload 
sudo systemctl start trendiest.service
sudo systemctl status trendiest.service

# optional 
sudo systemctl enable trendiest.service
```


Name
----

This daemon keeps the latest file easy to get at with a symlink, so you could say it's very trendy. Or maybe the trendiest. Yeah.. it's bad. Names are hard ok.











