FROM lscr.io/linuxserver/swag as swag

# Tried to setup a custom init script, but it's not needed.
# Use custom-cont-init.d instead
# COPY proxy-image-builder/root/ /

COPY proxy-image-builder/config/nginx/.htpasswd /defaults/nginx
COPY proxy-image-builder/config/nginx/proxy-confs/*.conf /defaults/nginx/proxy-confs

RUN mkdir -p /custom-cont-init.d
COPY proxy-image-builder/root/etc/s6-overlay/s6-rc.d/init-prawn-config/run  /custom-cont-init.d
