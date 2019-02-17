#!/bin/bash
php5.6 /var/www/html/install_i_am_a_sinner_forgive_me.php
service apache2 stop && service apache2 start && /var/www/html/sleep.sh