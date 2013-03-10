function inspect(node) {
    var message = 'Node: ' + node + '\n'
    message += 'Type: ' + typeof(node) + '\n'

    var showValueProps = new Array('nodeName', 'nodeType', 'nodeValue',
	'className')
    for (var i = 0; i < showValueProps.length; i++)
	message += showValueProps[i] + ': ' + node[showValueProps[i]] + '\n'

    var properties = new Array()
    var functions = new Array();
    var inaccessable = new Array();
    for (name in node) {
	try {
	    if (typeof(node[name]) == 'function')
		functions.push(name)
	    else
		properties.push(name)
	} catch(ex) {
	    inaccessable.push(name)
	}
    }
    message += 'Properties: ' + properties.sort().join(', ') + '\n'
    message += 'Functions: ' + functions.sort().join(', ') + '\n'
    message += 'inaccessable: ' + inaccessable.sort().join(', ') + '\n'

    return message
}

var showNewsContentItemPreviousNode = new Object()
showNewsContentItemPreviousNode.style = new Object()
function showNewsContentItem(link) {
    as = document.getElementsByTagName('a')
    for (var i = 0; i < as.length; i++) {
	var a = as[i]
	if (a.name.length < 1)  continue
	var ieName = '#' + unescape(a.name)
	var name =  '#' + escape(a.name)
	if (link.href.indexOf(name) < 0 && link.href.indexOf(ieName) < 0)
	    continue
	showNewsContentItemPreviousNode.style.display = 'none'
	showNewsContentItemPreviousNode = a.parentNode
	showNewsContentItemPreviousNode.style.display = 'block'
	break
    }
    return false
}
