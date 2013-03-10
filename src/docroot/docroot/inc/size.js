    function adjustTextSize() {
        var node = document.getElementsByClassName("content");
        if (node && node.length) {
           var size = readCookie("textSize");
           if (size && size === "Small") {
               node[0].setAttribute("style", "font-size:smaller;");
           } else if (size && size === "Large") {
               node[0].setAttribute("style", "font-size:larger;");
           }
        }
    }
