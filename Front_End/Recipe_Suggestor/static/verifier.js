 function verify() {
     if (document.getElementById('ingredient').checked) {
         document.getElementById('game').style.visibility = 'visible';
                document.getElementById('game1').style.visibility = 'hidden';
                }
     if (document.getElementById('image').checked) {
         document.getElementById('game').style.visibility = 'hidden';
                document.getElementById('game1').style.visibility = 'visible'; }
 }