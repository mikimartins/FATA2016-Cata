<?php
$data = json_decode(file_get_contents('php://input'), true);

if ( $data['repository'] ) {
    if( strcmp($data['repository']['full_name'], "thiagohersan/FATA2016-Cata") == 0 ){
        echo "Doing stuff";
        shell_exec( 'cd /home/tgh/FATA2016-Cata && git reset --hard HEAD && git pull origin master' );
        shell_exec( 'cd /home/tgh/FATA2016-Cata && ./makeBook.py' );
        shell_exec( 'cp /home/tgh/FATA2016-Cata/xbook.pdf /home/tgh/WWW' );        
    }
    echo "Book Ready";
}

?>
