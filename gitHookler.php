<?php
$data = json_decode(file_get_contents('php://input'), true);

if ( $data['repository'] ) {
    if( strcmp($data['repository']['full_name'], "thiagohersan/FATA2016-Cata") == 0 ){
        echo "Generating Catalog";
        shell_exec( 'cd /home/tgh/FATA2016-Cata && git reset --hard HEAD && git pull origin master' );
        shell_exec( 'cd /home/tgh/FATA2016-Cata && ./makeBook.py' );
        shell_exec( 'cp /home/tgh/FATA2016-Cata/xbook.pdf /home/tgh/WWW' );
    }
    echo "Book Ready";
}
elseif ( $data['repository'] ) {
    if( strcmp($data['repository']['full_name'], "thiagohersan/FATA2016-Site") == 0 ){
        echo "Generating Site";
        //shell_exec( 'cd /home/tgh/FATA2016-Site && git reset --hard HEAD && git pull origin master' );
        //shell_exec( 'cd /home/tgh/FATA2016-Site && hugo' );
        //shell_exec( 'cd /home/tgh/WWW && rm -rf FATA2016/*' );
        //shell_exec( 'cp -r /home/tgh/FATA2016-Cata/public/* /home/tgh/WWW/FATA2016/' );
    }
    echo "Site Ready";
}

?>
