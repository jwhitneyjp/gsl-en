
function kyoinPopup(url) {
	var x=0;
        var y=200;
	var w=560;
	var h=600;
	var str="";
	str+="directories=no,location=no,menubar=no,scrollbars=yes,status=no,toolbar=no,resizable=no,";
	str+="width="+w+",height="+h+",top="+x+",left="+y;
	var newwindow=window.open(url,"teacher",str,false);
        newwindow.focus();
	return false;
}

function openExternal(url){
window.opener.location.href = url;
window.close();
}

function purgeHrefs() {
    var contents = document.getElementsByClassName("content");
    if (contents && contents.length) {
        var nodes = contents[0].getElementsByTagName("a");
        if (nodes && nodes.length) {
            for (var i = 0, ilen = nodes.length; i < ilen; i += 1) {
                if (nodes[i].hasAttribute("onclick")) {
                    nodes[i].removeAttribute("href");
                }
            }
        }
    }
}
