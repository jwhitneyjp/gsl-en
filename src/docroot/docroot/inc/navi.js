    function setNavi () {
      var menus = document.getElementsByClassName('nav-buttons');
      if (menus && menus.length) {
        var href = '' + document.location.href;
        var m = href.match(/https?:\/\/[^\/]*\/([a-z]+).*/);
        if (m) {
          for (var i = 0, ilen = menus.length; i < ilen; i += 1) {
            var menu = menus[i];
            var linknames = ['programs','admissions','curriculum','faculty','support','alumni'];
            var pos = linknames.indexOf(m[1]);
            var buttons = menu.getElementsByTagName('a');
            for (var j=0, jlen=buttons.length; j < jlen; j += 1) {
              if (j === pos) {
                buttons[j].setAttribute('class', 'menu-button-selected');
              } else if (j < 6) {
                buttons[j].setAttribute('class', 'menu-button-unselected');
              }
            }
          }
        }
      }
    }
    function createCookie(name,value,days) {
    	if (days) {
    		var date = new Date();
    		date.setTime(date.getTime()+(days*24*60*60*1000));
    		var expires = "; expires="+date.toGMTString();
    	}
    	else var expires = "";
    	document.cookie = name+"="+value+expires+"; path=/";
    }
    
    function readCookie(name) {
    	var nameEQ = name + "=";
    	var ca = document.cookie.split(';');
    	for(var i=0;i < ca.length;i++) {
    		var c = ca[i];
    		while (c.charAt(0)==' ') c = c.substring(1,c.length);
    		    if (c.indexOf(nameEQ) == 0) {
                    return c.substring(nameEQ.length,c.length);
                }
    	}
    	return null;
    }
    
    function eraseCookie(name) {
    	createCookie(name,"",-1);
    }
